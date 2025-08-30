
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import threading
from recorder import Recorder

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
        self.stop_event = threading.Event()

    def on_start_recording(self, icon, item):
        print("Starting recording from menu")
        self.recorder.start_recording()
        self.update_menu()

    def on_stop_recording(self, icon, item):
        print("Stopping recording from menu")
        self.recorder.stop_recording()
        self.update_menu()

    def on_exit(self, icon, item):
        print("Exiting...")
        if self.recorder.is_recording:
            self.recorder.stop_recording()
        self.icon.stop()

    def get_menu(self):
        is_recording = self.recorder.is_recording
        return (
            item(
                'Iniciar Grava\u00e7\u00e3o',
                self.on_start_recording,
                enabled=not is_recording
            ),
            item(
                'Parar Grava\u00e7\u00e3o',
                self.on_stop_recording,
                enabled=is_recording
            ),
            pystray.Menu.SEPARATOR,
            item(
                'Sair',
                self.on_exit
            )
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
