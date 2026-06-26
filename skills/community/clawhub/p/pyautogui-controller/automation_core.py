#!/usr/bin/env python3
"""
自动化核心 - 整合鼠标、键盘、屏幕控制
用于构建复杂的自动化任务
"""

import time
from typing import Optional, Callable, Any
from mouse_controller import MouseController, WindowManager
from keyboard_controller import KeyboardController, ClipboardManager
from screen_controller import ScreenController

class AutomationCore:
    """自动化核心控制器"""
    
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()
        self.screen = ScreenController()
        self.window = WindowManager()
        self.clipboard = ClipboardManager()
    
    def click_and_type(self, x: int, y: int, text: str, 
                       use_clipboard: bool = False,
                       clear_first: bool = True):
        """
        点击并输入文本
        
        Args:
            x: X坐标
            y: Y坐标
            text: 要输入的文本
            use_clipboard: 是否使用剪贴板（支持中文）
            clear_first: 是否先清空输入框
        """
        # 点击位置
        self.mouse.click(x, y)
        time.sleep(0.3)
        
        # 清空输入框
        if clear_first:
            self.keyboard.clear_input()
            time.sleep(0.2)
        
        # 输入文本
        if use_clipboard:
            self.keyboard.type_text_clipboard(text)
        else:
            self.keyboard.type_text(text)
    
    def click_and_send(self, x: int, y: int, text: str,
                       use_clipboard: bool = False,
                       send_key: str = 'return'):
        """
        点击、输入并发送
        
        Args:
            x: X坐标
            y: Y坐标
            text: 要输入的文本
            use_clipboard: 是否使用剪贴板
            send_key: 发送键，默认回车
        """
        self.click_and_type(x, y, text, use_clipboard)
        time.sleep(0.3)
        self.keyboard.press_key(send_key)
    
    def find_and_click(self, image_path: str, confidence: float = 0.9,
                       timeout: int = 10) -> bool:
        """
        查找图片并点击
        
        Args:
            image_path: 图片路径
            confidence: 置信度
            timeout: 超时时间
        
        Returns:
            是否成功
        """
        location = self.screen.wait_for_image(image_path, timeout, confidence)
        if location:
            center_x = location[0] + location[2] // 2
            center_y = location[1] + location[3] // 2
            self.mouse.click(center_x, center_y)
            return True
        return False
    
    def wait_and_click(self, x: int, y: int, delay: float = 1.0):
        """
        等待后点击
        
        Args:
            x: X坐标
            y: Y坐标
            delay: 等待时间
        """
        time.sleep(delay)
        self.mouse.click(x, y)
    
    def wait_for_pixel(self, x: int, y: int, 
                       expected_color: tuple,
                       timeout: int = 10,
                       check_interval: float = 0.5) -> bool:
        """
        等待指定位置出现特定颜色
        
        Args:
            x: X坐标
            y: Y坐标
            expected_color: 期望的RGB颜色
            timeout: 超时时间
            check_interval: 检查间隔
        
        Returns:
            是否成功
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            current_color = self.screen.get_pixel(x, y)
            if current_color == expected_color:
                return True
            time.sleep(check_interval)
        return False
    
    def repeat_action(self, action: Callable, times: int, 
                      interval: float = 1.0):
        """
        重复执行动作
        
        Args:
            action: 要执行的动作函数
            times: 重复次数
            interval: 间隔时间
        """
        for i in range(times):
            action()
            if i < times - 1:
                time.sleep(interval)
    
    def sequence(self, *actions: Callable):
        """
        按顺序执行一系列动作
        
        Args:
            *actions: 动作函数列表
        """
        for action in actions:
            action()
            time.sleep(0.3)


class TaskRecorder:
    """任务记录器 - 记录和回放操作"""
    
    def __init__(self):
        self.actions = []
    
    def record_click(self, x: int, y: int, button: str = 'left'):
        """记录点击"""
        self.actions.append({
            'type': 'click',
            'x': x,
            'y': y,
            'button': button
        })
    
    def record_type(self, text: str):
        """记录输入"""
        self.actions.append({
            'type': 'type',
            'text': text
        })
    
    def record_wait(self, seconds: float):
        """记录等待"""
        self.actions.append({
            'type': 'wait',
            'seconds': seconds
        })
    
    def save(self, filepath: str):
        """保存记录"""
        import json
        with open(filepath, 'w') as f:
            json.dump(self.actions, f, indent=2)
    
    def load(self, filepath: str):
        """加载记录"""
        import json
        with open(filepath, 'r') as f:
            self.actions = json.load(f)
    
    def replay(self, core: AutomationCore):
        """回放记录"""
        for action in self.actions:
            if action['type'] == 'click':
                core.mouse.click(action['x'], action['y'], action['button'])
            elif action['type'] == 'type':
                core.keyboard.type_text(action['text'])
            elif action['type'] == 'wait':
                time.sleep(action['seconds'])


# 测试代码
if __name__ == "__main__":
    print("自动化核心测试")
    print("=" * 50)
    
    core = AutomationCore()
    
    # 测试1: 获取屏幕信息
    print(f"\n1. 屏幕尺寸: {core.screen.get_size()}")
    print(f"2. 当前鼠标位置: {core.mouse.get_position()}")
    
    # 测试2: 点击并输入
    print("\n3. 点击并输入测试 (5秒后开始)")
    time.sleep(5)
    
    # 移动到屏幕中心并点击
    center_x = core.screen.width // 2
    center_y = core.screen.height // 2
    core.mouse.click(center_x, center_y)
    print(f"   点击屏幕中心: ({center_x}, {center_y})")
    
    # 输入测试文本
    core.keyboard.type_text("Test from AutomationCore!")
    print("   输入完成")
    
    print("\n测试完成!")
