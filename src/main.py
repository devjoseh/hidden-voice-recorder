import pystray
from pystray import MenuItem as item, Menu
from PIL import Image, ImageDraw
import threading
from functools import partial
from recorder import Recorder, get_input_devices

def create_icon_image():
    # Create a simple icon image (a red circle for recording)
    width = 64
    height = 64
    color1 = (0, 0, 0, 0)  # Transparent background
    color2 = (255, 0, 0)    # Red circle

    image = Image.new("RGBA", (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.ellipse([(8, 8), (width - 8, height - 8)], fill=color2)

    return image

class VoiceRecorderApp:
    def __init__(self):
        self.recorder = Recorder()
        self.icon = None

    def on_start_recording(self, icon, item):
        print("Iniciando gravação pelo menu")
        self.recorder.start_recording()
        self.update_menu()

    def on_stop_recording(self, icon, item):
        print("Parando gravação pelo menu")
        self.recorder.stop_recording()
        self.update_menu()

    def on_exit(self, icon, item):
        print("Saindo...")
        if self.recorder.is_recording:
            self.recorder.stop_recording()
        self.icon.stop()

    def on_device_selected(self, device_index, icon, item):
        # The icon and item arguments are passed by pystray, so we must accept them.
        self.recorder.set_device(device_index)
        self.update_menu()

    def create_devices_menu(self):
        devices = get_input_devices()
        if not devices:
            return [item('Nenhum microfone encontrado', None, enabled=False)]

        menu_items = []
        for index, name in devices.items():
            # Use partial to freeze the index value for the callback
            # The callback will be called with (icon, item), and our frozen index will be passed first.
            action = partial(self.on_device_selected, index)
            menu_items.append(item(
                name,
                action,
                checked=lambda item, index=index: self.recorder.device == index,
                radio=True
            ))
        return menu_items

    def get_menu(self):
        is_recording = self.recorder.is_recording
        
        devices_submenu = Menu(*self.create_devices_menu())

        return (
            item(
                'Iniciar Gravação',
                self.on_start_recording,
                enabled=not is_recording and self.recorder.device is not None
            ),
            item(
                'Parar Gravação',
                self.on_stop_recording,
                enabled=is_recording
            ),
            Menu.SEPARATOR,
            item('Dispositivo de Entrada', devices_submenu),
            Menu.SEPARATOR,
            item('Sair', self.on_exit)
        )

    def update_menu(self):
        if self.icon:
            self.icon.menu = self.get_menu()

    def run(self):
        icon_image = create_icon_image()
        self.icon = pystray.Icon("VoiceRecorder", icon_image, "Voice Recorder", self.get_menu())
        self.icon.run()

if __name__ == "__main__":
    app = VoiceRecorderApp()
    app.run()
