
import sounddevice as sd
import numpy as np
import wavio
import threading
import os
from datetime import datetime

class Recorder:
    def __init__(self, output_folder="recordings"):
        self.output_folder = output_folder
        self.is_recording = False
        self.stream = None
        self.frames = []
        self.thread = None
        self.samplerate = 44100
        self.channels = 1

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def _record_thread(self):
        self.frames = []
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.frames.append(indata.copy())

        with sd.InputStream(samplerate=self.samplerate, channels=self.channels, callback=callback) as self.stream:
            while self.is_recording:
                sd.sleep(100)

    def start_recording(self):
        if self.is_recording:
            print("Already recording.")
            return

        self.is_recording = True
        self.thread = threading.Thread(target=self._record_thread)
        self.thread.start()
        print("Recording started.")

    def stop_recording(self):
        if not self.is_recording:
            print("Not recording.")
            return

        self.is_recording = False
        if self.thread is not None:
            self.thread.join()
        
        if self.stream is not None:
            # The stream is managed by the 'with' statement, but let's be safe
            # self.stream.stop() 
            # self.stream.close()
            self.stream = None

        print("Recording stopped.")
        self.save_recording()

    def save_recording(self):
        if not self.frames:
            print("No frames to save.")
            return

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".wav"
        filepath = os.path.join(self.output_folder, filename)
        
        recording = np.concatenate(self.frames, axis=0)
        
        wavio.write(filepath, recording, self.samplerate, sampwidth=2)
        
        print(f"Recording saved to {filepath}")
        self.frames = []
