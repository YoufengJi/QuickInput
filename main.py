import tkinter as tk
from pystray import MenuItem as item, Icon
from PIL import Image
import pyautogui
import time
import win32gui
import csv
import threading

texts = {}
active_popup = None  # 用于跟踪当前活跃的弹窗

with open('text.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        key, text = row
        texts[key] = text

root = tk.Tk()
root.title("Hidden Root")
root.withdraw()  # Hide the root window

def focus_force(window):
    window.update_idletasks()
    window_id = window.winfo_id()
    win32gui.SetForegroundWindow(window_id)

def create_popup():
    global active_popup
    if active_popup:
        active_popup.destroy()
        active_popup = None
        print("Popup closed")  # Debug statement for closing popup
        return

    print("Creating popup")  # Debug statement
    x, y = pyautogui.position()  # 获取当前鼠标位置
    popup = tk.Toplevel(root)
    popup.title("Select an Option")
    # 计算新窗口的位置，使其出现在光标下方稍微偏移的位置
    popup.geometry(f"300x300+{x+10}+{y+10}")
    active_popup = popup

    label = tk.Label(popup, text="Press a number (1-9):")
    label.pack(pady=20)

    # 显示每个选项的具体文本
    for key, text in texts.items():
        tk.Label(popup, text=f"{key}: {text}").pack()

    def on_key_press(event, num):
        global active_popup
        if num in texts:
            print(f"Key {num} pressed")  # Debug statement
            popup.destroy()
            active_popup = None
            time.sleep(0.1)
            pyautogui.write(texts[num], interval=0.01)

    for num in texts.keys():
        popup.bind(f'<Key-{num}>', lambda e, n=num: on_key_press(e, n))

    popup.lift()  # Bring the window to the front
    popup.focus_force()  # Force focus to the window
    popup.after(100, lambda: focus_force(popup))


def on_hotkey():
    print("Hotkey pressed")  # Debug statement
    create_popup()

def setup_hotkey():
    from pynput import keyboard

    def on_activate():
        on_hotkey()

    with keyboard.GlobalHotKeys({'<ctrl>+[': on_activate}) as h:
        h.join()

def exit_action(icon, item):
    icon.stop()
    root.destroy()
    root.quit()

def run_icon():
    image = Image.open("icon.png")
    menu = (item('Exit', exit_action),)
    icon = Icon("name", image, "QuickInput", menu)
    icon.run()

if __name__ == "__main__":
    icon_thread = threading.Thread(target=run_icon)
    icon_thread.daemon = True
    icon_thread.start()

    hotkey_thread = threading.Thread(target=setup_hotkey)
    hotkey_thread.daemon = True
    hotkey_thread.start()

    root.mainloop()
