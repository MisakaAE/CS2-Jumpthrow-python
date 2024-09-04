import ctypes
import sys
import tkinter as tk
from pynput import keyboard, mouse

# 检查是否具有管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 如果没有管理员权限，则请求权限
if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
else:
    # 创建鼠标控制器
    mouse_controller = mouse.Controller()

    # 创建键盘控制器
    keyboard_controller = keyboard.Controller()

    listener = None
    custom_key = keyboard.Key.alt_l  # 默认监听左Alt键

    def on_press(key):
        try:
            if key == custom_key:
                # 模拟松开鼠标左键和右键
                mouse_controller.release(mouse.Button.left)
                mouse_controller.release(mouse.Button.right)
                # 模拟按下并松开空格键
                keyboard_controller.press(keyboard.Key.space)
                keyboard_controller.release(keyboard.Key.space)
        except AttributeError:
            pass

    def start_listening():
        global listener
        if listener is None:
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            status_label.config(text="监听已启动", fg="green")
            current_key_label.config(text=f"当前监听按键: {custom_key}")

    def stop_listening():
        global listener
        if listener is not None:
            listener.stop()
            listener = None
            status_label.config(text="监听未启动", fg="red")

    def set_custom_key():
        status_label.config(text="请按下要监听的按键...", fg="black")
        def on_press_custom(key):
            global custom_key
            custom_key = key
            status_label.config(text="监听已启动", fg="green")
            current_key_label.config(text=f"当前监听按键: {custom_key}")
            listener_custom.stop()
        listener_custom = keyboard.Listener(on_press=on_press_custom)
        listener_custom.start()

    def reset_to_default():
        global custom_key
        custom_key = keyboard.Key.alt_l
        current_key_label.config(text=f"当前监听按键: {custom_key}")

    # 创建GUI
    root = tk.Tk()
    root.title("CS2 JT")

    # 移除最小化按钮
    root.attributes("-toolwindow", 1)

    # 锁定窗口大小
    root.resizable(False, False)

    start_button = tk.Button(root, text="开始监听", command=start_listening)
    start_button.pack(pady=10)

    stop_button = tk.Button(root, text="停止监听", command=stop_listening)
    stop_button.pack(pady=10)

    custom_key_button = tk.Button(root, text="自定义监听按键", command=set_custom_key)
    custom_key_button.pack(pady=10)

    reset_button = tk.Button(root, text="恢复默认按键", command=reset_to_default)
    reset_button.pack(pady=10)

    status_label = tk.Label(root, text="监听未启动", fg="red")
    status_label.pack(pady=10)

    current_key_label = tk.Label(root, text=f"当前监听按键: {custom_key}")
    current_key_label.pack(pady=10)

    root.mainloop()
