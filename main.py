import keyboard
from PIL import ImageGrab
import win32clipboard
import io
import os
from datetime import datetime
from windows_toasts import Toast, WindowsToaster

# directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAPTURES_DIR = os.path.join(SCRIPT_DIR, "captures")

# creates a directory for captures if it doesn't already exist
os.makedirs(CAPTURES_DIR, exist_ok=True)

# initialise desktop notification
toaster = WindowsToaster("Python Screenshot Utility")
toast = Toast()
toast.text_fields = ["Copied Screenshot", "The screenshot has also been saved to your captures directory."]

# define action on notification click
def open_explorer(activated_args):
    os.startfile(CAPTURES_DIR)


# capture and copy a screenshot
def capture_n_copy():
    print("Capturing Screenshot...")

    img = ImageGrab.grab()

    # save img to /captures
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(CAPTURES_DIR, f"screenshot_{timestamp}.png")
    img.save(file_path)
    print(f"Saved a capture to {file_path}")

    # send desktop notification
    toast.on_actived = open_explorer
    toaster.show_toast(toast)
    

    # win clipboard expects device independent bitmap (DIB) format
    output = io.BytesIO()
    img.convert("RGB").save(output, "BMP")

    # strip 14 byte BMP file header to get the pure DIB data
    data = output.getvalue()[14:]
    output.close()

    # clipboard shenanigans
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        print("Screenshot successfully copied to clipboard!")
    except Exception as error:
        print(f"Failed to copy to clipboard: {error}")

# register the hotkey
keyboard.add_hotkey('ctrl+shift+s', capture_n_copy)

print("Background screenshot tool is running.")
print("Press CTRL + SHIFT + S to capture a screenshot.")
print("Press CTRL + SHIFT + L to quit the script.")

# keep running until ctrl+shift+esc
keyboard.wait('ctrl+shift+l')
