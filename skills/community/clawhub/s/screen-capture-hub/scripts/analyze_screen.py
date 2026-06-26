#!/usr/bin/env python3
"""
屏幕分析工具
提供多种屏幕分析功能
"""

import argparse
import sys
import os
import json
from datetime import datetime

try:
    from PIL import ImageGrab, Image, ImageDraw, ImageFont
    import pyautogui
    import cv2
    import numpy as np
except ImportError as e:
    print(f"错误：缺少必要的库。请安装：pip install pillow pyautogui opencv-python numpy")
    print(f"导入错误：{e}")
    sys.exit(1)

def capture_screenshot(output_path=None, region=None):
    """捕获屏幕截图"""
    try:
        if region:
            coords = region.split(',')
            if len(coords) != 4:
                print("区域格式错误，应为 'x1,y1,x2,y2'")
                return None
            x1, y1, x2, y2 = map(int, coords)
            bbox = (x1, y1, x2, y2)
            screenshot = ImageGrab.grab(bbox=bbox)
        else:
            screenshot = ImageGrab.grab()
        
        if output_path:
            screenshot.save(output_path)
            print(f"截图已保存：{output_path}")
        
        return screenshot
    except Exception as e:
        print(f"截图失败：{e}")
        return None

def find_text_on_screen(search_text, screenshot=None, lang='eng+chi_sim'):
    """在屏幕上查找特定文字"""
    try:
        import pytesseract
        
        # 如果没有提供截图，先捕获屏幕
        if screenshot is None:
            screenshot = capture_screenshot()
            if screenshot is None:
                return None
        
        # 转换为灰度图
        gray = screenshot.convert('L')
        
        # 使用Tesseract获取文字和位置信息
        data = pytesseract.image_to_data(gray, lang=lang, output_type=pytesseract.Output.DICT)
        
        found_positions = []
        
        # 搜索匹配的文字
        for i in range(len(data['text'])):
            text = data['text'][i].strip()
            if search_text.lower() in text.lower():
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]
                conf = data['conf'][i]
                
                found_positions.append({
                    'text': text,
                    'position': (x, y, w, h),
                    'confidence': conf,
                    'index': i
                })
        
        return found_positions
        
    except ImportError:
        print("错误：未找到pytesseract。请安装：pip install pytesseract")
        return None
    except Exception as e:
        print(f"文字搜索失败：{e}")
        return None

def find_color_on_screen(target_color, screenshot=None, tolerance=10):
    """在屏幕上查找特定颜色"""
    try:
        # 如果没有提供截图，先捕获屏幕
        if screenshot is None:
            screenshot = capture_screenshot()
            if screenshot is None:
                return None
        
        # 转换为RGB
        rgb_img = screenshot.convert('RGB')
        width, height = rgb_img.size
        
        # 将目标颜色转换为RGB元组
        if isinstance(target_color, str):
            # 解析十六进制颜色
            if target_color.startswith('#'):
                target_color = target_color[1:]
            r = int(target_color[0:2], 16)
            g = int(target_color[2:4], 16)
            b = int(target_color[4:6], 16)
            target_rgb = (r, g, b)
        else:
            target_rgb = target_color
        
        # 查找匹配颜色的像素
        matches = []
        
        # 为了性能，可以采样检查
        for y in range(0, height, 5):  # 每5个像素采样一次
            for x in range(0, width, 5):
                pixel = rgb_img.getpixel((x, y))
                
                # 计算颜色差异
                diff = sum(abs(p - t) for p, t in zip(pixel, target_rgb))
                if diff <= tolerance:
                    matches.append((x, y))
        
        return matches
        
    except Exception as e:
        print(f"颜色搜索失败：{e}")
        return None

def detect_edges_on_screen(screenshot=None):
    """检测屏幕边缘"""
    try:
        # 如果没有提供截图，先捕获屏幕
        if screenshot is None:
            screenshot = capture_screenshot()
            if screenshot is None:
                return None
        
        # 转换为OpenCV格式
        cv_img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        
        # 转换为灰度图
        gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
        
        # 应用Canny边缘检测
        edges = cv2.Canny(gray, 50, 150)
        
        # 计算边缘数量
        edge_pixels = np.sum(edges > 0)
        total_pixels = edges.size
        edge_percentage = (edge_pixels / total_pixels) * 100
        
        return {
            'edge_image': edges,
            'edge_pixels': edge_pixels,
            'total_pixels': total_pixels,
            'edge_percentage': edge_percentage
        }
        
    except Exception as e:
        print(f"边缘检测失败：{e}")
        return None

def get_screen_info():
    """获取屏幕信息"""
    try:
        screen_width, screen_height = pyautogui.size()
        mouse_x, mouse_y = pyautogui.position()
        
        info = {
            'resolution': f"{screen_width}x{screen_height}",
            'mouse_position': (mouse_x, mouse_y),
            'timestamp': datetime.now().isoformat()
        }
        
        return info
        
    except Exception as e:
        print(f"获取屏幕信息失败：{e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='屏幕分析工具')
    parser.add_argument('--task', '-t', required=True,
                       choices=['find_text', 'find_color', 'detect_edges', 'screen_info'],
                       help='分析任务类型')
    parser.add_argument('--text', default='',
                       help='要搜索的文字（用于find_text任务）')
    parser.add_argument('--color', default='#FF0000',
                       help='要搜索的颜色（十六进制，用于find_color任务）')
    parser.add_argument('--tolerance', type=int, default=10,
                       help='颜色匹配容差（0-255，用于find_color任务）')
    parser.add_argument('--output', '-o', default=None,
                       help='输出文件路径')
    parser.add_argument('--region', '-r', default=None,
                       help='捕获区域，格式：x1,y1,x2,y2')
    parser.add_argument('--lang', '-l', default='eng+chi_sim',
                       help='OCR语言（用于find_text任务）')
    
    args = parser.parse_args()
    
    # 根据任务类型执行不同的分析
    if args.task == 'screen_info':
        # 获取屏幕信息
        info = get_screen_info()
        if info:
            print("屏幕信息：")
            print(f"  分辨率：{info['resolution']}")
            print(f"  鼠标位置：{info['mouse_position']}")
            print(f"  时间：{info['timestamp']}")
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(info, f, indent=2)
                print(f"信息已保存到：{args.output}")
    
    elif args.task == 'find_text':
        # 搜索文字
        if not args.text:
            print("错误：--text 参数是必需的")
            sys.exit(1)
        
        print(f"正在搜索文字：'{args.text}'")
        positions = find_text_on_screen(args.text, lang=args.lang)
        
        if positions:
            print(f"找到 {len(positions)} 个匹配：")
            for i, pos in enumerate(positions):
                x, y, w, h = pos['position']
                print(f"  {i+1}: '{pos['text']}' 位置: ({x}, {y}, {w}, {h}) 置信度: {pos['confidence']}")
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(positions, f, indent=2, default=str)
                print(f"结果已保存到：{args.output}")
        else:
            print("未找到匹配的文字")
    
    elif args.task == 'find_color':
        # 搜索颜色
        print(f"正在搜索颜色：{args.color}")
        matches = find_color_on_screen(args.color, tolerance=args.tolerance)
        
        if matches:
            print(f"找到 {len(matches)} 个匹配颜色的像素")
            
            # 显示前几个匹配位置
            print("前10个匹配位置：")
            for i, (x, y) in enumerate(matches[:10]):
                print(f"  {i+1}: ({x}, {y})")
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(matches, f, indent=2)
                print(f"结果已保存到：{args.output}")
        else:
            print("未找到匹配的颜色")
    
    elif args.task == 'detect_edges':
        # 检测边缘
        print("正在检测屏幕边缘...")
        result = detect_edges_on_screen()
        
        if result:
            print(f"边缘检测结果：")
            print(f"  边缘像素数：{result['edge_pixels']}")
            print(f"  总像素数：{result['total_pixels']}")
            print(f"  边缘比例：{result['edge_percentage']:.2f}%")
            
            if args.output:
                # 保存边缘图像
                edge_img = Image.fromarray(result['edge_image'])
                edge_img.save(args.output)
                print(f"边缘图像已保存到：{args.output}")
    
    else:
        print(f"未知任务：{args.task}")
        sys.exit(1)

if __name__ == "__main__":
    main()