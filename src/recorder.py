
import sounddevice as sd
import numpy as np
import wavio
import threading
import os
from datetime import datetime

def get_input_devices():
    """Gets a cleaned-up list of unique input devices, prioritizing WASAPI."""
    devices = sd.query_devices()
    hostapis = sd.query_hostapis()
    
    wasapi_index = -1
    for i, api in enumerate(hostapis):
        if api['name'] == 'Windows WASAPI':
            wasapi_index = i
            break

    input_devices = {}
    seen_names = set()

    # Prioritize WASAPI devices
    for i, dev in enumerate(devices):
        if dev['hostapi'] == wasapi_index and dev['max_input_channels'] > 0:
            # Clean up common system device names
            if '@' in dev['name'] or 'Mapeador' in dev['name']:
                continue
            
            if dev['name'] not in seen_names:
                input_devices[i] = dev['name']
                seen_names.add(dev['name'])

    # If no WASAPI devices found, fall back to any input device
    if not input_devices:
        for i, dev in enumerate(devices):
            if dev['max_input_channels'] > 0:
                if '@' in dev['name'] or 'Mapeador' in dev['name']:
                    continue
                
                if dev['name'] not in seen_names:
                    input_devices[i] = dev['name']
                    seen_names.add(dev['name'])

    return input_devices

class Recorder:
    def __init__(self, output_folder="recordings"):
        self.output_folder = output_folder
        self.is_recording = False
        self.stream = None
        self.frames = []
        self.thread = None
        self.samplerate = 44100
        self.channels = 1
        try:
            # Set default device
            self.device = sd.default.device['input']
        except (ValueError, TypeError):
            # Fallback if no default input device is configured
            devices = get_input_devices()
            if devices:
                self.device = list(devices.keys())[0]
            else:
                self.device = None
                print("ERRO: Nenhum microfone encontrado.")

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def set_device(self, device_index):
        print(f"Microfone alterado para o dispositivo: {device_index}")
        self.device = device_index

    def _record_thread(self):
        self.frames = []
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.frames.append(indata.copy())

        try:
            with sd.InputStream(samplerate=self.samplerate, channels=self.channels, device=self.device, callback=callback) as self.stream:
                while self.is_recording:
                    sd.sleep(100)
        except Exception as e:
            print(f"Erro ao abrir o stream de áudio: {e}")
            self.is_recording = False # Stop recording state if stream fails

    def start_recording(self):
        if self.is_recording:
            print("Já gravando.")
            return
        
        if self.device is None:
            print("Não é possível iniciar a gravação: nenhum microfone selecionado ou disponível.")
            return

        self.is_recording = True
        self.thread = threading.Thread(target=self._record_thread)
        self.thread.start()
        print("Gravação iniciada.")

    def stop_recording(self):
        if not self.is_recording:
            # This can be triggered if the stream failed to open, so don't print "Not recording"
            return

        self.is_recording = False
        if self.thread is not None:
            self.thread.join()
        
        self.stream = None

        print("Gravação parada.")
        self.save_recording()

    def save_recording(self):
        if not self.frames:
            print("Nenhum frame para salvar.")
            return

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
        filepath = os.path.join(self.output_folder, filename)
        
        recording = np.concatenate(self.frames, axis=0)
        
        wavio.write(filepath, recording, self.samplerate, sampwidth=2)
        
        print(f"Gravação salva em {filepath}")
        self.frames = []
