#!/usr/bin/env python3
"""
屏幕控制器 - 屏幕截图和图像识别模块
用于截图、图像识别、像素分析等操作
"""

import pyautogui
import time
from typing import Tuple, Optional, List
from PIL import Image

class ScreenController:
    """屏幕控制器"""
    
    def __init__(self):
        self.width, self.height = pyautogui.size()
        print(f"屏幕分辨率: {self.width}x{self.height}")
    
    def get_size(self) -> Tuple[int, int]:
        """获取屏幕尺寸"""
        return pyautogui.size()
    
    def screenshot(self, filepath: Optional[str] = None, 
                   region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        """
        截图
        
        Args:
            filepath: 保存路径
            region: 区域 (x, y, width, height)
        
        Returns:
            PIL Image 对象
        """
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()
        
        if filepath:
            screenshot.save(filepath)
        
        return screenshot
    
    def screenshot_region(self, x: int, y: int, width: int, height: int, 
                          filepath: Optional[str] = None) -> Image.Image:
        """
        截图指定区域
        
        Args:
            x: 起始X坐标
            y: 起始Y坐标
            width: 宽度
            height: 高度
            filepath: 保存路径
        """
        return self.screenshot(filepath, (x, y, width, height))
    
    def get_pixel(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        获取指定位置的像素颜色
        
        Args:
            x: X坐标
            y: Y坐标
        
        Returns:
            RGB 元组
        """
        return pyautogui.pixel(x, y)
    
    def pixel_matches(self, x: int, y: int, 
                      expected_rgb: Tuple[int, int, int], 
                      tolerance: int = 0) -> bool:
        """
        检查像素颜色是否匹配
        
        Args:
            x: X坐标
            y: Y坐标
            expected_rgb: 期望的RGB值
            tolerance: 容差
        
        Returns:
            是否匹配
        """
        return pyautogui.pixelMatchesColor(x, y, expected_rgb, tolerance)
    
    def locate_on_screen(self, image_path: str, 
                         confidence: Optional[float] = None,
                         grayscale: bool = False) -> Optional[Tuple[int, int, int, int]]:
        """
        在屏幕上查找图片
        
        Args:
            image_path: 图片路径
            confidence: 置信度 (0-1)，需要安装 opencv-python
            grayscale: 是否使用灰度匹配
        
        Returns:
            (left, top, width, height) 或 None
        """
        try:
            if confidence is not None:
                return pyautogui.locateOnScreen(image_path, 
                                                 confidence=confidence,
                                                 grayscale=grayscale)
            else:
                return pyautogui.locateOnScreen(image_path, grayscale=grayscale)
        except Exception as e:
            print(f"查找失败: {e}")
            return None
    
    def locate_all_on_screen(self, image_path: str,
                             confidence: Optional[float] = None,
                             grayscale: bool = False) -> List[Tuple[int, int, int, int]]:
        """
        查找屏幕上所有匹配的图片
        
        Args:
            image_path: 图片路径
            confidence: 置信度
            grayscale: 是否使用灰度匹配
        
        Returns:
            匹配位置列表
        """
        try:
            if confidence is not None:
                return list(pyautogui.locateAllOnScreen(image_path,
                                                        confidence=confidence,
                                                        grayscale=grayscale))
            else:
                return list(pyautogui.locateAllOnScreen(image_path, 
                                                        grayscale=grayscale))
        except Exception as e:
            print(f"查找失败: {e}")
            return []
    
    def locate_center_on_screen(self, image_path: str,
                                confidence: Optional[float] = None,
                                grayscale: bool = False) -> Optional[Tuple[int, int]]:
        """
        查找图片中心位置
        
        Args:
            image_path: 图片路径
            confidence: 置信度
            grayscale: 是否使用灰度匹配
        
        Returns:
            (x, y) 中心坐标 或 None
        """
        try:
            if confidence is not None:
                return pyautogui.locateCenterOnScreen(image_path,
                                                      confidence=confidence,
                                                      grayscale=grayscale)
            else:
                return pyautogui.locateCenterOnScreen(image_path,
                                                      grayscale=grayscale)
        except Exception as e:
            print(f"查找失败: {e}")
            return None
    
    def wait_for_image(self, image_path: str, 
                       timeout: int = 10,
                       confidence: Optional[float] = None) -> Optional[Tuple[int, int, int, int]]:
        """
        等待图片出现
        
        Args:
            image_path: 图片路径
            timeout: 超时时间（秒）
            confidence: 置信度
        
        Returns:
            位置信息 或 None
        """
        try:
            if confidence is not None:
                return pyautogui.locateOnScreen(image_path,
                                                confidence=confidence,
                                                timeout=timeout)
            else:
                return pyautogui.locateOnScreen(image_path, timeout=timeout)
        except Exception:
            return None


class ColorAnalyzer:
    """颜色分析器"""
    
    def __init__(self):
        pass
    
    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """RGB 转 Hex"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Hex 转 RGB"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def is_similar_color(self, color1: Tuple[int, int, int], 
                         color2: Tuple[int, int, int], 
                         tolerance: int = 10) -> bool:
        """
        判断两个颜色是否相似
        
        Args:
            color1: RGB1
            color2: RGB2
            tolerance: 容差
        
        Returns:
            是否相似
        """
        return all(abs(c1 - c2) <= tolerance for c1, c2 in zip(color1, color2))


# 测试代码
if __name__ == "__main__":
    print("屏幕控制器测试")
    print("=" * 50)
    
    controller = ScreenController()
    
    # 测试1: 全屏截图
    print("\n1. 全屏截图")
    controller.screenshot("C:/Users/dev/Desktop/昱昱/test_screenshot.png")
    print("   已保存到桌面")
    
    # 测试2: 区域截图
    print("\n2. 区域截图 (屏幕中心 300x200)")
    center_x = controller.width // 2 - 150
    center_y = controller.height // 2 - 100
    controller.screenshot_region(center_x, center_y, 300, 200,
                                  "C:/Users/dev/Desktop/昱昱/test_region.png")
    print("   已保存")
    
    # 测试3: 获取像素颜色
    print("\n3. 获取屏幕中心像素颜色")
    color = controller.get_pixel(controller.width // 2, controller.height // 2)
    print(f"   RGB: {color}")
    
    print("\n测试完成!")
