#!/usr/bin/env python3
"""
键盘控制器 - 精准键盘控制模块
用于精确控制键盘输入、快捷键等操作
"""

import pyautogui
import time
import pyperclip
from typing import List, Optional

class KeyboardController:
    """精准键盘控制器"""
    
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
    
    def type_text(self, text: str, interval: float = 0.01):
        """
        输入文本
        
        Args:
            text: 要输入的文本
            interval: 每个字符之间的间隔（秒）
        """
        pyautogui.write(text, interval=interval)
    
    def type_text_clipboard(self, text: str):
        """
        使用剪贴板输入文本（支持中文）
        
        Args:
            text: 要输入的文本
        """
        # 保存当前剪贴板内容
        original_clipboard = pyperclip.paste()
        
        # 复制新内容到剪贴板
        pyperclip.copy(text)
        time.sleep(0.1)
        
        # 粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        
        # 恢复原始剪贴板内容
        pyperclip.copy(original_clipboard)
    
    def press_key(self, key: str):
        """
        按单个键
        
        Args:
            key: 键名，如 'enter', 'tab', 'esc' 等
        """
        pyautogui.press(key)
    
    def press_keys(self, keys: List[str]):
        """
        按多个键
        
        Args:
            keys: 键名列表
        """
        pyautogui.press(keys)
    
    def hotkey(self, *keys: str):
        """
        按组合键
        
        Args:
            *keys: 键名，如 'ctrl', 'c'
        """
        pyautogui.hotkey(*keys)
    
    def key_down(self, key: str):
        """按住键"""
        pyautogui.keyDown(key)
    
    def key_up(self, key: str):
        """释放键"""
        pyautogui.keyUp(key)
    
    def select_all(self):
        """全选"""
        pyautogui.hotkey('ctrl', 'a')
    
    def copy(self):
        """复制"""
        pyautogui.hotkey('ctrl', 'c')
    
    def paste(self):
        """粘贴"""
        pyautogui.hotkey('ctrl', 'v')
    
    def cut(self):
        """剪切"""
        pyautogui.hotkey('ctrl', 'x')
    
    def undo(self):
        """撤销"""
        pyautogui.hotkey('ctrl', 'z')
    
    def redo(self):
        """重做"""
        pyautogui.hotkey('ctrl', 'y')
    
    def save(self):
        """保存"""
        pyautogui.hotkey('ctrl', 's')
    
    def delete(self):
        """删除"""
        pyautogui.press('delete')
    
    def backspace(self, times: int = 1):
        """
        退格
        
        Args:
            times: 退格次数
        """
        for _ in range(times):
            pyautogui.press('backspace')
    
    def clear_input(self):
        """清空输入框"""
        self.select_all()
        time.sleep(0.1)
        self.delete()
    
    def newline(self):
        """换行"""
        pyautogui.press('return')
    
    def tab(self):
        """Tab键"""
        pyautogui.press('tab')
    
    def escape(self):
        """Esc键"""
        pyautogui.press('esc')
    
    def space(self, times: int = 1):
        """
        空格键
        
        Args:
            times: 空格次数
        """
        for _ in range(times):
            pyautogui.press('space')


class ClipboardManager:
    """剪贴板管理器"""
    
    def __init__(self):
        pass
    
    def copy_text(self, text: str):
        """复制文本到剪贴板"""
        pyperclip.copy(text)
    
    def paste_text(self) -> str:
        """从剪贴板粘贴文本"""
        return pyperclip.paste()
    
    def copy_and_paste(self, text: str):
        """复制并粘贴文本"""
        original = pyperclip.paste()
        pyperclip.copy(text)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.1)
        pyperclip.copy(original)


# 特殊键名参考
SPECIAL_KEYS = {
    'enter': 'return',
    'return': 'return',
    'tab': 'tab',
    'esc': 'esc',
    'escape': 'esc',
    'space': 'space',
    'backspace': 'backspace',
    'delete': 'delete',
    'up': 'up',
    'down': 'down',
    'left': 'left',
    'right': 'right',
    'home': 'home',
    'end': 'end',
    'pageup': 'pageup',
    'pagedown': 'pagedown',
    'f1': 'f1',
    'f2': 'f2',
    'f3': 'f3',
    'f4': 'f4',
    'f5': 'f5',
    'f6': 'f6',
    'f7': 'f7',
    'f8': 'f8',
    'f9': 'f9',
    'f10': 'f10',
    'f11': 'f11',
    'f12': 'f12',
    'ctrl': 'ctrl',
    'alt': 'alt',
    'shift': 'shift',
    'win': 'win',
    'command': 'command',
}


# 测试代码
if __name__ == "__main__":
    print("键盘控制器测试")
    print("=" * 50)
    
    controller = KeyboardController()
    clipboard = ClipboardManager()
    
    # 测试1: 英文输入
    print("\n1. 英文输入测试 (5秒后开始)")
    time.sleep(5)
    controller.type_text("Hello World!")
    print("   完成")
    
    # 测试2: 中文输入（使用剪贴板）
    print("\n2. 中文输入测试 (3秒后开始)")
    time.sleep(3)
    controller.type_text_clipboard("你好，世界！")
    print("   完成")
    
    # 测试3: 快捷键
    print("\n3. 快捷键测试 (全选)")
    controller.select_all()
    print("   完成")
    
    print("\n测试完成!")
