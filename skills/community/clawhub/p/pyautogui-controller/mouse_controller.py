#!/usr/bin/env python3
"""
鼠标控制器 - 精准鼠标控制模块
用于精确控制鼠标移动、点击、拖拽等操作
"""

import pyautogui
import time
from typing import Tuple, Optional, List

class MouseController:
    """精准鼠标控制器"""
    
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"屏幕分辨率: {self.screen_width}x{self.screen_height}")
    
    def get_screen_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        return pyautogui.size()
    
    def get_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        return pyautogui.position()
    
    def move_to(self, x: int, y: int, duration: float = 0.3):
        """移动鼠标到指定坐标"""
        pyautogui.moveTo(x, y, duration=duration)
    
    def move_rel(self, x: int, y: int, duration: float = 0.3):
        """相对移动"""
        pyautogui.moveRel(x, y, duration=duration)
    
    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = 'left', clicks: int = 1):
        """点击鼠标"""
        if x is not None and y is not None:
            pyautogui.click(x, y, button=button, clicks=clicks)
        else:
            pyautogui.click(button=button, clicks=clicks)
    
    def double_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """双击"""
        if x is not None and y is not None:
            pyautogui.doubleClick(x, y)
        else:
            pyautogui.doubleClick()
    
    def right_click(self, x: Optional[int] = None, y: Optional[int] = None):
        """右键点击"""
        self.click(x, y, button='right')
    
    def drag_to(self, x: int, y: int, duration: float = 0.5):
        """拖拽到指定位置"""
        pyautogui.dragTo(x, y, duration=duration)
    
    def drag_rel(self, x: int, y: int, duration: float = 0.5):
        """相对拖拽"""
        pyautogui.dragRel(x, y, duration=duration)
    
    def scroll(self, amount: int, x: Optional[int] = None, y: Optional[int] = None):
        """滚动鼠标"""
        if x is not None and y is not None:
            pyautogui.scroll(amount, x, y)
        else:
            pyautogui.scroll(amount)
    
    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        """获取指定位置的像素颜色"""
        return pyautogui.pixel(x, y)
    
    def locate_on_screen(self, image_path: str, confidence: float = 0.9):
        """在屏幕上查找图片位置"""
        try:
            return pyautogui.locateOnScreen(image_path, confidence=confidence)
        except Exception as e:
            print(f"查找失败: {e}")
            return None
    
    def locate_center_on_screen(self, image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int]]:
        """查找图片中心位置"""
        try:
            return pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        except Exception as e:
            print(f"查找失败: {e}")
            return None
    
    def click_image(self, image_path: str, confidence: float = 0.9):
        """点击图片"""
        location = self.locate_center_on_screen(image_path, confidence)
        if location:
            self.click(location[0], location[1])
            return True
        return False


class WindowManager:
    """窗口管理器"""
    
    def __init__(self):
        self.controller = MouseController()
    
    def activate_window(self, window_name: str):
        """激活指定窗口"""
        # Windows: Alt+Tab 切换
        pyautogui.keyDown('alt')
        pyautogui.keyDown('tab')
        pyautogui.keyUp('tab')
        pyautogui.keyUp('alt')
        time.sleep(0.5)
    
    def minimize_window(self):
        """最小化窗口"""
        pyautogui.keyDown('win')
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
        pyautogui.keyUp('win')
    
    def maximize_window(self):
        """最大化窗口"""
        pyautogui.keyDown('win')
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
        pyautogui.keyUp('win')
    
    def close_window(self):
        """关闭窗口"""
        pyautogui.keyDown('alt')
        pyautogui.keyDown('f4')
        pyautogui.keyUp('f4')
        pyautogui.keyUp('alt')


# 测试代码
if __name__ == "__main__":
    print("鼠标控制器测试")
    print("=" * 50)
    
    controller = MouseController()
    
    # 测试1: 获取屏幕信息
    print(f"\n1. 屏幕尺寸: {controller.get_screen_size()}")
    print(f"2. 当前鼠标位置: {controller.get_position()}")
    
    # 测试2: 移动到屏幕中心
    print("\n3. 移动到屏幕中心...")
    center_x = controller.screen_width // 2
    center_y = controller.screen_height // 2
    controller.move_to(center_x, center_y)
    print(f"   位置: ({center_x}, {center_y})")
    
    # 测试3: 点击测试
    print("\n4. 点击测试 (5秒后开始)")
    time.sleep(5)
    controller.click()
    print("   点击完成")
    
    print("\n测试完成!")
