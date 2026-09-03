import keyboard
import PIL from ImageGrab
import win32clipboard
import io

def capture_n_copy():
    print("Capturing Screenshot...")

    img = ImageGrab.grab()

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