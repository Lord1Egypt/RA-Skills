#!/usr/bin/env python3
"""
屏幕截图工具
支持捕获整个屏幕或指定区域
"""

import argparse
import sys
import os
from datetime import datetime

try:
    from PIL import ImageGrab
    import pyautogui
except ImportError as e:
    print(f"错误：缺少必要的库。请安装：pip install pillow pyautogui")
    print(f"导入错误：{e}")
    sys.exit(1)

def capture_full_screen(output_path):
    """捕获整个屏幕"""
    try:
        # 获取屏幕尺寸
        screen_width, screen_height = pyautogui.size()
        print(f"屏幕分辨率：{screen_width}x{screen_height}")
        
        # 捕获整个屏幕
        screenshot = ImageGrab.grab()
        
        # 保存图片
        screenshot.save(output_path)
        print(f"截图已保存到：{output_path}")
        print(f"图片尺寸：{screenshot.size[0]}x{screenshot.size[1]}")
        
        return True
    except Exception as e:
        print(f"截图失败：{e}")
        return False

def capture_region(output_path, region_str):
    """捕获指定区域"""
    try:
        # 解析区域字符串 "x1,y1,x2,y2"
        coords = region_str.split(',')
        if len(coords) != 4:
            print("区域格式错误，应为 'x1,y1,x2,y2'")
            return False
            
        x1, y1, x2, y2 = map(int, coords)
        
        # 确保坐标有效
        if x1 < 0 or y1 < 0 or x2 <= x1 or y2 <= y1:
            print("区域坐标无效")
            return False
            
        region = (x1, y1, x2, y2)
        
        # 捕获指定区域
        screenshot = ImageGrab.grab(bbox=region)
        
        # 保存图片
        screenshot.save(output_path)
        print(f"区域截图已保存到：{output_path}")
        print(f"区域：{region}")
        print(f"图片尺寸：{screenshot.size[0]}x{screenshot.size[1]}")
        
        return True
    except Exception as e:
        print(f"区域截图失败：{e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='屏幕截图工具')
    parser.add_argument('--output', '-o', default=None,
                       help='输出文件路径（默认：screenshot_时间戳.png）')
    parser.add_argument('--region', '-r', default=None,
                       help='捕获区域，格式：x1,y1,x2,y2')
    parser.add_argument('--list-displays', '-l', action='store_true',
                       help='列出所有显示器信息')
    
    args = parser.parse_args()
    
    # 设置默认输出路径
    if args.output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"screenshot_{timestamp}.png"
    
    # 列出显示器信息
    if args.list_displays:
        try:
            screen_width, screen_height = pyautogui.size()
            print(f"主显示器：{screen_width}x{screen_height}")
            
            # 尝试获取鼠标位置
            x, y = pyautogui.position()
            print(f"当前鼠标位置：({x}, {y})")
            
            # 获取所有显示器信息（需要pyautogui的支持）
            print("\n提示：使用 --region 参数指定捕获区域")
            print("示例：--region \"100,100,500,500\"")
            
        except Exception as e:
            print(f"获取显示器信息失败：{e}")
        return
    
    # 执行截图
    success = False
    if args.region:
        success = capture_region(args.output, args.region)
    else:
        success = capture_full_screen(args.output)
    
    if success:
        print(f"\n截图完成！")
        print(f"文件：{os.path.abspath(args.output)}")
        
        # 显示文件信息
        if os.path.exists(args.output):
            file_size = os.path.getsize(args.output)
            print(f"大小：{file_size / 1024:.2f} KB")
    else:
        print("截图失败")
        sys.exit(1)

if __name__ == "__main__":
    main()