#!/usr/bin/env python3
"""
快速截图工具 - 简化版本的屏幕截图
提供简单易用的命令行界面
"""

import argparse
import sys
import os
from datetime import datetime

try:
    from PIL import ImageGrab
    import pyautogui
except ImportError as e:
    print(f"错误: 缺少必要的库。请运行: pip install pillow pyautogui")
    print(f"错误详情: {e}")
    sys.exit(1)

def quick_capture(output=None, region=None, show_info=False):
    """
    快速截图函数
    
    Args:
        output: 输出文件路径，如果为None则自动生成
        region: 截图区域，格式为 "x1,y1,x2,y2"
        show_info: 是否显示屏幕信息
    """
    
    # 获取屏幕信息
    screen_width, screen_height = pyautogui.size()
    mouse_x, mouse_y = pyautogui.position()
    
    if show_info:
        print("=== 屏幕信息 ===")
        print(f"分辨率: {screen_width}x{screen_height}")
        print(f"鼠标位置: ({mouse_x}, {mouse_y})")
        print("================")
    
    # 设置输出文件名
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"screen_capture_{timestamp}.png"
    
    # 执行截图
    try:
        if region:
            # 解析区域
            coords = region.split(',')
            if len(coords) != 4:
                print("错误: 区域格式应为 'x1,y1,x2,y2'")
                return False
            x1, y1, x2, y2 = map(int, coords)
            bbox = (x1, y1, x2, y2)
            img = ImageGrab.grab(bbox=bbox)
            print(f"区域截图: {bbox}")
        else:
            # 全屏截图
            img = ImageGrab.grab()
            print(f"全屏截图: {screen_width}x{screen_height}")
        
        # 保存图片
        img.save(output)
        file_size = os.path.getsize(output) / 1024  # KB
        
        print(f"✅ 截图成功!")
        print(f"📁 文件: {os.path.abspath(output)}")
        print(f"📏 尺寸: {img.size[0]}x{img.size[1]}")
        print(f"💾 大小: {file_size:.1f} KB")
        
        return True
        
    except Exception as e:
        print(f"❌ 截图失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='快速截图工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                    # 全屏截图，自动命名
  %(prog)s -o my_screen.png   # 保存为指定文件
  %(prog)s -r "0,0,500,500"   # 截取指定区域
  %(prog)s -i                 # 显示屏幕信息
  %(prog)s -r "0,0,500,500" -o region.png  # 区域截图并指定文件名
        """
    )
    
    parser.add_argument('-o', '--output', 
                       help='输出文件路径（默认: screen_capture_时间戳.png）')
    parser.add_argument('-r', '--region',
                       help='截图区域，格式: x1,y1,x2,y2')
    parser.add_argument('-i', '--info', action='store_true',
                       help='显示屏幕信息')
    
    args = parser.parse_args()
    
    # 执行截图
    success = quick_capture(
        output=args.output,
        region=args.region,
        show_info=args.info
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()