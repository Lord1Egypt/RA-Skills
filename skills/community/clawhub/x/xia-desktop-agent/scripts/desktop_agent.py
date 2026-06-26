"""桌面自动化核心操作类 - DesktopAgent"""

import os
import time
import logging
import subprocess
from pathlib import Path

import pyautogui
import cv2
import numpy as np
from PIL import Image, ImageGrab

# 安全设置：防误操作
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.3

# 截图保存目录
SCREENSHOT_DIR = Path(r"C:\temp\desktop_agent")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)


class DesktopAgent:
    """Windows 桌面自动化代理"""

    def __init__(self, screenshot_dir: str | None = None):
        self.screenshot_dir = Path(screenshot_dir) if screenshot_dir else SCREENSHOT_DIR
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)
        self.screen_width, self.screen_height = pyautogui.size()

    def screenshot(self, save_path: str | None = None) -> str:
        """截取屏幕截图，返回保存路径"""
        img = ImageGrab.grab()
        if save_path is None:
            save_path = str(self.screenshot_dir / f"screenshot_{int(time.time())}.png")
        img.save(save_path)
        logger.info(f"截图已保存: {save_path}")
        return save_path

    def click(self, x: int, y: int, button: str = "left", clicks: int = 1):
        """点击指定坐标"""
        pyautogui.click(x=x, y=y, button=button, clicks=clicks)
        logger.info(f"点击 ({x}, {y}), 按钮={button}, 次数={clicks}")

    def double_click(self, x: int, y: int):
        """双击指定坐标"""
        self.click(x, y, clicks=2)

    def type_text(self, text: str, interval: float = 0.05):
        """输入文字 - 优先使用SendMessage，降级到pyautogui

        在OpenClaw exec环境下，键盘模拟(pyautogui/pyperclip+Ctrl+V)可能失效，
        但Windows消息API(SendMessage EM_REPLACESEL)可以直接向控件发送文字。
        """
        if self._send_message_type(text):
            logger.info(f"[SendMessage] 输入文字: {text[:50]}")
        else:
            # 降级：英文直接用pyautogui.write，中文用剪贴板+Ctrl+V
            import pyperclip
            pyperclip.copy(text)
            pyautogui.hotkey('ctrl', 'v')
            logger.info(f"[Ctrl+V fallback] 输入文字: {text[:50]}")

    def _send_message_type(self, text: str) -> bool:
        """通过SendMessage EM_REPLACESEL向当前焦点控件发送文字

        查找前台窗口的RichEdit/Edit/TextBox控件，直接发送文字。
        绕过键盘模拟，在OpenClaw exec环境下可靠工作。
        """
        try:
            import win32gui
            import win32con

            # 获取前台窗口
            fg_hwnd = win32gui.GetForegroundWindow()
            if not fg_hwnd:
                return False

            # 常见的编辑控件类名
            edit_classes = ['RichEditD2DPT', 'RichEdit20W', 'RichEdit20A',
                            'Edit', 'NotepadTextBox', 'WEBCanvasNode',
                            'Chrome_RenderWidgetHostHWND', 'Chrome_WidgetWin_1',
                            'TextBlock', 'TextBox']

            # 查找编辑控件
            edit_hwnd = None
            def enum_children(hwnd, _):
                nonlocal edit_hwnd
                cls = win32gui.GetClassName(hwnd)
                if cls in edit_classes:
                    edit_hwnd = hwnd

            win32gui.EnumChildWindows(fg_hwnd, enum_children, None)

            if not edit_hwnd:
                return False

            # 用EM_REPLACESEL发送文字（在光标位置插入）
            win32gui.SendMessage(edit_hwnd, win32con.EM_REPLACESEL, 0, text)
            return True
        except Exception as e:
            logger.debug(f"SendMessage输入失败: {e}")
            return False

    def send_message_type(self, text: str) -> bool:
        """公开方法：通过SendMessage向控件发送文字（不降级）"""
        return self._send_message_type(text)

    def find_edit_control(self, window_title: str | None = None) -> int | None:
        """查找指定窗口中的编辑控件句柄

        Args:
            window_title: 窗口标题关键词，None则使用前台窗口
        Returns:
            编辑控件句柄，未找到返回None
        """
        import win32gui

        if window_title:
            # 按标题查找窗口
            target = None
            def enum_wins(hwnd, _):
                nonlocal target
                title = win32gui.GetWindowText(hwnd)
                if window_title in title and win32gui.IsWindowVisible(hwnd):
                    target = hwnd
            win32gui.EnumWindows(enum_wins, None)
            if not target:
                return None
        else:
            target = win32gui.GetForegroundWindow()

        if not target:
            return None

        edit_classes = ['RichEditD2DPT', 'RichEdit20W', 'RichEdit20A',
                        'Edit', 'NotepadTextBox', 'WEBCanvasNode',
                        'Chrome_RenderWidgetHostHWND', 'Chrome_WidgetWin_1',
                        'TextBlock', 'TextBox']

        edit_hwnd = None
        def enum_children(hwnd, _):
            nonlocal edit_hwnd
            cls = win32gui.GetClassName(hwnd)
            if cls in edit_classes:
                edit_hwnd = hwnd
        win32gui.EnumChildWindows(target, enum_children, None)
        return edit_hwnd

    def press_key(self, key: str, presses: int = 1):
        """按键 - 通过SendMessage模拟（在exec环境下更可靠）

        支持特殊按键: enter, escape, tab, backspace, delete,
        以及功能键: f1-f12
        注意: 组合键(如ctrl+c)在此环境下不可靠
        """
        import win32gui
        import win32con

        # 虚拟键码映射
        vk_map = {
            'enter': 0x0D, 'return': 0x0D, 'escape': 0x1B, 'esc': 0x1B,
            'tab': 0x09, 'backspace': 0x08, 'delete': 0x2E, 'del': 0x2E,
            'space': 0x20, ' ': 0x20,
            'home': 0x24, 'end': 0x23,
            'pageup': 0x21, 'pagedown': 0x22,
            'up': 0x26, 'down': 0x28, 'left': 0x25, 'right': 0x27,
            'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
            'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
            'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
            'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
            'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A,
        }
        # 功能键
        for i in range(1, 13):
            vk_map[f'f{i}'] = 0x6F + i

        key_lower = key.lower()
        if key_lower in vk_map:
            vk = vk_map[key_lower]
            # 找前台编辑控件发送WM_KEYDOWN/WM_KEYUP
            fg = win32gui.GetForegroundWindow()
            edit_hwnd = None
            edit_classes = ['RichEditD2DPT', 'RichEdit20W', 'RichEdit20A',
                            'Edit', 'NotepadTextBox', 'WEBCanvasNode',
                            'Chrome_RenderWidgetHostHWND', 'Chrome_WidgetWin_1']
            def _enum(hwnd, _):
                nonlocal edit_hwnd
                if win32gui.GetClassName(hwnd) in edit_classes:
                    edit_hwnd = hwnd
            win32gui.EnumChildWindows(fg, _enum, None)
            target = edit_hwnd or fg
            win32gui.SendMessage(target, win32con.WM_KEYDOWN, vk, 0)
            time.sleep(0.05)
            win32gui.SendMessage(target, win32con.WM_KEYUP, vk, 0)
            logger.info(f"按键(SendMessage): {key}")
        else:
            # 降级到pyautogui
            keys = key.split("+")
            if len(keys) > 1:
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(keys[0], presses=presses)
            logger.info(f"按键(pyautogui): {key}")

    def scroll(self, amount: int, x: int | None = None, y: int | None = None):
        """滚动鼠标滚轮，正数向上，负数向下"""
        pyautogui.scroll(amount, x=x, y=y)
        logger.info(f"滚动: {amount}")

    def get_active_window(self) -> str:
        """获取当前活动窗口标题"""
        try:
            import pygetwindow as gw
            win = gw.getActiveWindow()
            return win.title if win else ""
        except Exception:
            return ""

    def list_windows(self) -> list[dict]:
        """列出所有可见窗口"""
        try:
            import pygetwindow as gw
            windows = gw.getAllWindows()
            return [
                {"title": w.title, "left": w.left, "top": w.top,
                 "width": w.width, "height": w.height, "visible": w.visible}
                for w in windows if w.title
            ]
        except Exception as e:
            logger.error(f"获取窗口列表失败: {e}")
            return []

    def find_on_screen(self, template_path: str, confidence: float = 0.8) -> tuple[int, int] | None:
        """在屏幕上查找模板图像，返回中心坐标或None"""
        screenshot_path = self.screenshot()
        screen = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)
        if screen is None or template is None:
            return None

        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val >= confidence:
            h, w = template.shape[:2]
            center = (max_loc[0] + w // 2, max_loc[1] + h // 2)
            logger.info(f"找到模板于 {center}, 置信度={max_val:.2f}")
            return center
        logger.info(f"未找到模板, 最高置信度={max_val:.2f}")
        return None

    def open_app(self, app_name: str) -> bool:
        """打开应用程序"""
        try:
            # 常见应用名映射
            app_map = {
                "notepad": "notepad.exe",
                "记事本": "notepad.exe",
                "calc": "calc.exe",
                "计算器": "calc.exe",
                "explorer": "explorer.exe",
                "chrome": "start chrome",
                "edge": "start msedge",
                "微信": r"WeChat\WeChat.exe",
                "wechat": r"Weixin\Weixin.exe",
                "weixin": r"Weixin\Weixin.exe",
                "code": "code",
            }
            cmd = app_map.get(app_name.lower(), app_name)
            subprocess.Popen(cmd, shell=True)
            logger.info(f"启动应用: {app_name} -> {cmd}")
            return True
        except Exception as e:
            logger.error(f"启动应用失败: {e}")
            return False

    def wait(self, seconds: float):
        """等待指定秒数"""
        time.sleep(seconds)
        logger.info(f"等待 {seconds}s")


if __name__ == "__main__":
    import sys
    agent = DesktopAgent()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "screenshot"

    if cmd == "screenshot":
        path = agent.screenshot()
        print(f"截图: {path}")
    elif cmd == "click" and len(sys.argv) >= 4:
        agent.click(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "type_text" and len(sys.argv) >= 3:
        agent.type_text(sys.argv[2])
    elif cmd == "press_key" and len(sys.argv) >= 3:
        agent.press_key(sys.argv[2])
    elif cmd == "open_app" and len(sys.argv) >= 3:
        agent.open_app(sys.argv[2])
    elif cmd == "list_windows":
        for w in agent.list_windows():
            print(w)
    else:
        print(f"未知命令: {cmd}")
