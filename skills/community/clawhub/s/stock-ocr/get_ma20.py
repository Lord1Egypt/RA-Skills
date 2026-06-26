#!/usr/bin/env python3
"""
截取均线数值区域并识别
"""

import subprocess
import sys
import os
import re
import time
import ctypes
from ctypes import wintypes
from datetime import datetime
import struct

# Windows API
user32 = ctypes.windll.user32
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
SW_RESTORE = 9
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B
VK_F5 = 0x74
VK_F8 = 0x77
KEYEVENTF_KEYUP = 0x0002


def find_window(title_pattern: str):
    result = {'hwnd': None, 'title': None}
    
    def callback(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buffer, length + 1)
                title = buffer.value
                if title_pattern.lower() in title.lower():
                    result['hwnd'] = hwnd
                    result['title'] = title
                    return False
        return True
    
    user32.EnumWindows(EnumWindowsProc(callback), 0)
    return result['hwnd'], result['title']


def send_key(vk_code: int):
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def send_keys(text: str):
    for char in text:
        if char == '\n':
            send_key(VK_RETURN)
        elif char == '\x1b':
            send_key(VK_ESCAPE)
        else:
            vk = user32.VkKeyScanW(ord(char))
            if vk != -1:
                vk_code = vk & 0xFF
                user32.keybd_event(vk_code, 0, 0, 0)
                time.sleep(0.03)
                user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.05)


def capture_region(hwnd, left, top, width, height, output_path):
    """截取窗口指定区域"""
    # 获取窗口DC
    hdc_window = user32.GetWindowDC(hwnd)
    hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_window)
    hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc_window, width, height)
    ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)
    
    # 截图指定区域
    ctypes.windll.gdi32.BitBlt(hdc_mem, 0, 0, width, height, hdc_window, left, top, 0x00CC0020)
    
    # 获取位图数据
    bmi = struct.pack('LLLHHLLLLLL', 40, width, height, 1, 24, 0, 0, 0, 0, 0, 0)
    bufsize = width * height * 3
    buffer = ctypes.create_string_buffer(bufsize)
    ctypes.windll.gdi32.GetDIBits(hdc_mem, hbitmap, 0, height, buffer, bmi, 0)
    
    # 保存BMP
    with open(output_path, 'wb') as f:
        f.write(struct.pack('HLHHL', 0x4D42, 54 + bufsize, 0, 0, 54))
        f.write(bmi)
        f.write(buffer)
    
    # 清理
    ctypes.windll.gdi32.DeleteObject(hbitmap)
    ctypes.windll.gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(hwnd, hdc_window)
    
    return os.path.exists(output_path)


def bmp_to_png(bmp_path, png_path):
    """转换BMP到PNG"""
    try:
        from PIL import Image
        img = Image.open(bmp_path)
        img.save(png_path)
        os.remove(bmp_path)
        return png_path
    except:
        return bmp_path


def ocr_space(image_path: str) -> str:
    """使用OCR.space免费API"""
    import requests
    import base64
    
    # 读取并压缩图片
    try:
        from PIL import Image
        import io
        
        img = Image.open(image_path)
        
        # 如果是RGBA，转换为RGB
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        
        # 缩小尺寸以控制大小
        max_dimension = 1500
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        # 压缩质量递减直到小于1MB
        quality = 70
        while quality > 20:
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=quality)
            img_data = output.getvalue()
            size_kb = len(img_data) / 1024
            
            if size_kb < 1000:  # 留一点余量
                break
            quality -= 10
        
        print(f"压缩后图片大小: {len(img_data)/1024:.1f}KB (质量={quality})")
        
    except ImportError:
        with open(image_path, 'rb') as f:
            img_data = f.read()
    
    files = {'file': ('image.jpg', img_data, 'image/jpeg')}
    data = {
        'apikey': 'K82897662288957',
        'language': 'chs',
        'isOverlayRequired': 'false'
    }
    
    try:
        response = requests.post(
            'https://api.ocr.space/parse/image',
            files=files,
            data=data,
            timeout=30
        )
        result = response.json()
        
        if result.get('OCRExitCode') == 1:
            return result['ParsedResults'][0]['ParsedText']
        else:
            print(f"OCR错误: {result.get('ErrorMessage', result)}")
            return ""
    except Exception as e:
        print(f"请求失败: {e}")
        return ""


def extract_ma_values(text: str) -> dict:
    """提取均线数值"""
    result = {}
    patterns = {
        'MA5': r'MA5[：:\s]*(\d+\.?\d*)',
        'MA10': r'MA10[：:\s]*(\d+\.?\d*)',
        'MA20': r'MA20[：:\s]*(\d+\.?\d*)',
        'MA60': r'MA60[：:\s]*(\d+\.?\d*)',
    }
    for name, pattern in patterns.items():
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            result[name] = m.group(1)
    return result


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='获取股票MA20数值')
    parser.add_argument('-s', '--stock-code', required=True, help='股票代码')
    parser.add_argument('-w', '--window-title', default='金长江', help='窗口标题')
    parser.add_argument('--region', default='top-right', help='截图区域: full/top-right/ma-panel')
    parser.add_argument('--keep-screenshot', action='store_true', help='保留截图')
    
    args = parser.parse_args()
    
    # 查找窗口
    print(f"正在查找窗口: {args.window_title}")
    hwnd, title = find_window(args.window_title)
    
    if not hwnd:
        print(f"❌ 未找到窗口")
        return
    
    print(f"✅ 找到窗口: {title}")
    
    # 将窗口带到前台
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.2)
    
    # 输入股票代码
    print(f"\n正在输入股票代码: {args.stock_code}")
    send_key(VK_ESCAPE)
    time.sleep(0.1)
    send_keys(args.stock_code)
    time.sleep(0.3)
    send_key(VK_RETURN)
    print("  - 已输入股票代码")
    time.sleep(1.0)
    
    # 切换到日K线
    print("正在切换到日K线...")
    send_key(VK_F5)
    time.sleep(0.5)
    for i in range(3):
        send_key(VK_F8)
        time.sleep(0.3)
    print("  - 已切换到日K线")
    time.sleep(0.5)
    
    # 获取窗口大小
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    win_width = rect.right - rect.left
    win_height = rect.bottom - rect.top
    
    print(f"\n窗口大小: {win_width}x{win_height}")
    
    # 确定截图区域（假设均线显示在右上角）
    if args.region == 'top-right':
        # 截取右上角区域
        region_left = win_width // 2
        region_top = 0
        region_width = win_width // 2
        region_height = win_height // 3
    elif args.region == 'ma-panel':
        # 截取均线面板区域（通常在左上角）
        region_left = 0
        region_top = 50
        region_width = min(200, win_width)
        region_height = min(150, win_height - 50)
    else:
        # 全窗口
        region_left = 0
        region_top = 0
        region_width = win_width
        region_height = win_height
    
    print(f"截图区域: ({region_left}, {region_top}) {region_width}x{region_height}")
    
    # 截图
    print("\n正在截图...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bmp_path = f"ma_region_{timestamp}.bmp"
    
    success = capture_region(hwnd, region_left, region_top, region_width, region_height, bmp_path)
    
    if success:
        png_path = bmp_to_png(bmp_path, f"ma_region_{timestamp}.png")
        print(f"✅ 截图已保存: {png_path}")
        
        # OCR识别
        print("\n正在进行OCR识别...")
        text = ocr_space(png_path)
        
        if text:
            print("\n识别结果:")
            print("-" * 40)
            print(text)
            print("-" * 40)
            
            ma_values = extract_ma_values(text)
            if ma_values:
                print("\n✅ 均线数值:")
                for k, v in ma_values.items():
                    print(f"   {k}: {v}")
            else:
                print("\n⚠️ 未找到均线数值，请调整截图区域")
                print("   提示: 尝试 --region full 或 --region ma-panel")
        else:
            print("❌ OCR识别失败")
        
        # 清理
        if not args.keep_screenshot:
            try:
                os.remove(png_path)
                print(f"\n已删除临时截图: {png_path}")
            except:
                pass
    else:
        print("❌ 截图失败")


if __name__ == "__main__":
    main()
