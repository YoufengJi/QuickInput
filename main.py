import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from pystray import MenuItem as item, Icon
from PIL import Image, ImageDraw
import pyautogui
import time
import win32gui
import csv
import threading
import logging
from typing import Dict, Optional
import os
import sys

# 设置日志 - 修复中文乱码问题
import sys
import locale

# 设置控制台编码
if sys.platform == 'win32':
    # Windows系统设置UTF-8编码
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.detach())

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class QuickInputApp:
    """QuickInput 应用程序主类"""
    
    def __init__(self):
        self.texts: Dict[str, str] = {}
        self.active_popup: Optional[tk.Toplevel] = None
        self.root: Optional[tk.Tk] = None
        self.icon: Optional[Icon] = None
        self.load_texts()
        self.setup_gui()
        
    def load_texts(self) -> None:
        """从CSV文件加载文本数据"""
        try:
            csv_path = 'text.csv'
            if not os.path.exists(csv_path):
                logger.error(f"找不到文件: {csv_path}")
                return
                
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # 跳过标题行
                for row in reader:
                    if len(row) >= 2:
                        key, text = row[0], row[1]
                        self.texts[key] = text
            logger.info(f"成功加载 {len(self.texts)} 条文本")
        except Exception as e:
            logger.error(f"加载文本失败: {e}")
            
    def setup_gui(self) -> None:
        """设置GUI界面"""
        self.root = tk.Tk()
        self.root.title("QuickInput - 快速输入工具")
        self.root.withdraw()  # 隐藏主窗口
        
        # 设置应用图标
        try:
            if os.path.exists("icon.png"):
                icon_img = tk.PhotoImage(file="icon.png")
                self.root.iconphoto(False, icon_img)
        except Exception as e:
            logger.warning(f"无法加载图标: {e}")
            
    def focus_force(self, window: tk.Widget) -> None:
        """强制窗口获得焦点"""
        try:
            import win32con
            import win32process
            window.update_idletasks()
            window_id = window.winfo_id()
            
            # 获取当前前台窗口
            current_window = win32gui.GetForegroundWindow()
            current_thread = win32process.GetWindowThreadProcessId(current_window)[0]
            target_thread = win32process.GetWindowThreadProcessId(window_id)[0]
            
            # 附加输入线程
            if current_thread != target_thread:
                win32process.AttachThreadInput(current_thread, target_thread, True)
            
            # 设置窗口为前台
            win32gui.ShowWindow(window_id, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(window_id)
            win32gui.SetActiveWindow(window_id)
            win32gui.SetFocus(window_id)
            
            # 分离输入线程
            if current_thread != target_thread:
                win32process.AttachThreadInput(current_thread, target_thread, False)
                
        except Exception as e:
            logger.warning(f"设置焦点失败: {e}")
            
    def create_popup(self) -> None:
        """创建弹窗界面"""
        if self.active_popup:
            self.close_popup()
            return
            
        logger.info("创建弹窗")
        x, y = pyautogui.position()
        
        # 创建现代化的弹窗
        popup = tk.Toplevel(self.root)
        popup.title("QuickInput - 选择选项")
        popup.geometry(f"420x500+{x+10}+{y+10}")
        popup.resizable(False, False)
        
        # 设置弹窗样式
        popup.configure(bg='#2c3e50')
        
        # 设置弹窗属性
        popup.attributes("-topmost", True)
        popup.grab_set()  # 模态窗口
        
        self.active_popup = popup
        
        # 创建样式
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Custom.TFrame', background='#2c3e50')
        style.configure('Title.TLabel', background='#2c3e50', foreground='#ecf0f1', 
                       font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', background='#2c3e50', foreground='#bdc3c7', 
                       font=('Segoe UI', 10))
        style.configure('Option.TLabel', background='#34495e', foreground='#ecf0f1', 
                       font=('Segoe UI', 10), relief='flat', padding=10)
        
        # 主框架
        main_frame = ttk.Frame(popup, style='Custom.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🚀 QuickInput", style='Title.TLabel')
        title_label.pack(pady=(0, 5))
        
        # 副标题
        subtitle_label = ttk.Label(main_frame, text="按数字键 (1-9) 快速输入文本", style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 20))
        
        # 分隔线
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.pack(fill='x', pady=(0, 15))
        
        # 选项框架
        options_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        options_frame.pack(fill='both', expand=True)
        
        # 创建选项列表
        for i, (key, text) in enumerate(self.texts.items()):
            option_frame = tk.Frame(options_frame, bg='#34495e', relief='raised', bd=1)
            option_frame.pack(fill='x', pady=2, padx=5)
            
            # 添加鼠标移入移出效果
            def on_enter(event, frame=option_frame):
                frame.configure(bg='#3498db')
                
            def on_leave(event, frame=option_frame):
                frame.configure(bg='#34495e')
                
            option_frame.bind("<Enter>", on_enter)
            option_frame.bind("<Leave>", on_leave)
            
            # 键位标签
            key_label = tk.Label(option_frame, text=f" {key} ", bg='#e74c3c', fg='white', 
                               font=('Segoe UI', 10, 'bold'), width=3)
            key_label.pack(side='left', padx=(10, 10), pady=8)
            
            # 文本标签
            text_label = tk.Label(option_frame, text=text, bg='#34495e', fg='#ecf0f1', 
                                font=('Segoe UI', 10), anchor='w')
            text_label.pack(side='left', fill='x', expand=True, padx=(0, 10), pady=8)
            
        # 底部提示
        bottom_frame = ttk.Frame(main_frame, style='Custom.TFrame')
        bottom_frame.pack(fill='x', pady=(15, 0))
        
        hint_label = ttk.Label(bottom_frame, text="💡 提示：按 ESC 关闭窗口", style='Subtitle.TLabel')
        hint_label.pack()
        
        # 绑定键盘事件
        def on_key_press(event):
            key = event.char
            if key in self.texts:
                logger.info(f"按键 {key} 被按下")
                self.close_popup()
                time.sleep(0.1)
                pyautogui.write(self.texts[key], interval=0.01)
            elif event.keysym == 'Escape':
                self.close_popup()
                
        # 绑定键盘事件到弹窗和所有子控件
        popup.bind('<Key>', on_key_press)
        popup.bind('<KeyPress>', on_key_press)
        
        # 为所有子控件也绑定键盘事件
        def bind_all_widgets(widget):
            widget.bind('<Key>', on_key_press)
            widget.bind('<KeyPress>', on_key_press)
            for child in widget.winfo_children():
                bind_all_widgets(child)
                
        bind_all_widgets(popup)
        
        # 窗口关闭事件
        popup.protocol("WM_DELETE_WINDOW", self.close_popup)
        
        # 设置焦点 - 使用更可靠的方法
        popup.lift()
        popup.focus_set()
        popup.update()
        popup.focus_force()
        
        # 延迟设置焦点以确保窗口完全显示后再获取焦点
        def set_focus():
            try:
                popup.focus_set()
                self.focus_force(popup)
                # 模拟键盘事件来激活窗口焦点
                popup.event_generate('<FocusIn>')
                popup.tk.call('focus', popup)
            except Exception as e:
                logger.warning(f"设置焦点失败: {e}")
                
        popup.after(200, set_focus)
        
    def close_popup(self) -> None:
        """关闭弹窗"""
        if self.active_popup:
            try:
                self.active_popup.destroy()
                self.active_popup = None
                logger.info("弹窗已关闭")
            except Exception as e:
                logger.error(f"关闭弹窗失败: {e}")
                
    def on_hotkey(self) -> None:
        """热键回调函数"""
        logger.info("热键被按下")
        self.create_popup()
        
    def setup_hotkey(self) -> None:
        """设置全局热键"""
        try:
            from pynput import keyboard
            
            def on_activate():
                self.on_hotkey()
                
            with keyboard.GlobalHotKeys({'<ctrl>+[': on_activate}) as h:
                logger.info("热键 Ctrl+[ 已设置")
                h.join()
        except Exception as e:
            logger.error(f"设置热键失败: {e}")
            
    def exit_action(self, icon, item) -> None:
        """退出应用程序"""
        logger.info("正在退出应用程序")
        if self.icon:
            self.icon.stop()
        if self.active_popup:
            self.close_popup()
        if self.root:
            self.root.destroy()
            self.root.quit()
            
    def create_default_icon(self) -> Image.Image:
        """创建默认图标"""
        # 创建一个简单的默认图标
        width, height = 64, 64
        image = Image.new('RGB', (width, height), color='#3498db')
        draw = ImageDraw.Draw(image)
        
        # 绘制一个简单的"Q"字
        draw.text((width//2-10, height//2-10), "Q", fill='white')
        return image
        
    def run_icon(self) -> None:
        """运行系统托盘图标"""
        try:
            if os.path.exists("icon.png"):
                image = Image.open("icon.png")
            else:
                image = self.create_default_icon()
                
            menu = (
                item('QuickInput - 快速输入工具', lambda: None, enabled=False),
                item('热键: Ctrl+[', lambda: None, enabled=False),
                item('退出', self.exit_action),
            )
            
            self.icon = Icon("QuickInput", image, "QuickInput - 快速输入工具", menu)
            logger.info("系统托盘图标已启动")
            self.icon.run()
        except Exception as e:
            logger.error(f"运行系统托盘图标失败: {e}")
            
    def run(self) -> None:
        """运行应用程序"""
        if not self.texts:
            logger.error("没有加载到任何文本，请检查 text.csv 文件")
            return
            
        try:
            # 启动系统托盘图标线程
            icon_thread = threading.Thread(target=self.run_icon, daemon=True)
            icon_thread.start()
            
            # 启动热键监听线程
            hotkey_thread = threading.Thread(target=self.setup_hotkey, daemon=True)
            hotkey_thread.start()
            
            logger.info("QuickInput 应用程序已启动")
            logger.info("使用 Ctrl+[ 调出快速输入窗口")
            
            # 运行主循环
            self.root.mainloop()
            
        except KeyboardInterrupt:
            logger.info("收到中断信号，正在退出...")
        except Exception as e:
            logger.error(f"应用程序运行失败: {e}")
        finally:
            if self.icon:
                self.icon.stop()

def main():
    """主函数"""
    try:
        app = QuickInputApp()
        app.run()
    except Exception as e:
        logger.error(f"程序启动失败: {e}")
        input("按任意键退出...")

if __name__ == "__main__":
    main()
