#!/usr/bin/env python3
"""
股票MA20数值识别工具 - 纯Python版本
使用urllib发送请求，无需外部依赖
"""

import ctypes
import ctypes.wintypes
import os
import re
import struct
import sys
import time
import urllib.request
import urllib.parse
import json
from datetime import datetime
from http.client import HTTPConnection

# Windows API
user32 = ctypes.windll.user32
EnumWindowsProc = ctypes.WINFUNCTYPE(
    ctypes.wintypes.BOOL, 
    ctypes.wintypes.HWND, 
    ctypes.wintypes.LPARAM
)
SW_RESTORE = 9
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B
VK_F5 = 0x74
VK_F8 = 0x77
KEYEVENTF_KEYUP = 0x0002


def find_window(title_pattern):
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


def send_key(vk_code):
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def send_char(char):
    vk = user32.VkKeyScanW(ord(char))
    if vk != -1:
        vk_code = vk & 0xFF
        user32.keybd_event(vk_code, 0, 0, 0)
        time.sleep(0.03)
        user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def capture_window_region(hwnd, left, top, width, height, output_path):
    """截取窗口指定区域并保存为BMP"""
    hdc_window = user32.GetWindowDC(hwnd)
    hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_window)
    hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc_window, width, height)
    ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)
    
    # 截图
    ctypes.windll.gdi32.BitBlt(
        hdc_mem, 0, 0, width, height,
        hdc_window, left, top, 0x00CC0020  # SRCCOPY
    )
    
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


def bmp_to_jpeg_in_memory(bmp_path, max_size_kb=900):
    """将BMP转换为JPEG并压缩到指定大小（纯Python实现）"""
    # 直接返回BMP数据
    actual_size_kb = os.path.getsize(bmp_path) / 1024
    
    if actual_size_kb > max_size_kb:
        return None, actual_size_kb
    
    with open(bmp_path, 'rb') as f:
        return f.read(), actual_size_kb


def ocr_space_api(image_data, filename="image.bmp"):
    """调用OCR.space API"""
    boundary = "----WebKitFormBoundary" + ''.join([str(i) for i in range(16)])
    
    body = []
    
    # file field
    body.append(f'--{boundary}'.encode())
    body.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"'.encode())
    body.append(b'Content-Type: image/bmp')
    body.append(b'')
    body.append(image_data)
    
    # apikey field
    body.append(f'--{boundary}'.encode())
    body.append(b'Content-Disposition: form-data; name="apikey"')
    body.append(b'')
    body.append(b'K82897662288957')
    
    # language field
    body.append(f'--{boundary}'.encode())
    body.append(b'Content-Disposition: form-data; name="language"')
    body.append(b'')
    body.append(b'chs')
    
    # isOverlayRequired field
    body.append(f'--{boundary}'.encode())
    body.append(b'Content-Disposition: form-data; name="isOverlayRequired"')
    body.append(b'')
    body.append(b'false')
    
    # end boundary
    body.append(f'--{boundary}--'.encode())
    
    body_data = b'\r\n'.join(body)
    
    # 发送请求
    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'Content-Length': str(len(body_data))
    }
    
    try:
        req = urllib.request.Request(
            'https://api.ocr.space/parse/image',
            data=body_data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('OCRExitCode') == 1:
                return result['ParsedResults'][0]['ParsedText']
            else:
                print(f"OCR错误: {result.get('ErrorMessage', result)}")
                return None
    except Exception as e:
        print(f"请求失败: {e}")
        return None


def extract_ma_values(text):
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
    parser.add_argument('--keep-screenshot', action='store_true', help='保留截图')
    
    args = parser.parse_args()
    
    # 查找窗口
    print(f"正在查找窗口: {args.window_title}")
    hwnd, title = find_window(args.window_title)
    
    if not hwnd:
        print("❌ 未找到窗口")
        return
    
    print(f"✅ 找到窗口: {title}")
    
    # 激活窗口
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    
    # 输入股票代码
    print(f"\n正在输入股票代码: {args.stock_code}")
    send_key(VK_ESCAPE)
    time.sleep(0.1)
    for c in args.stock_code:
        send_char(c)
        time.sleep(0.05)
    time.sleep(0.3)
    send_key(VK_RETURN)
    print("  - 已输入股票代码")
    time.sleep(1.0)
    
    # 切换到日K线
    print("正在切换到日K线...")
    send_key(VK_F5)
    time.sleep(0.5)
    for _ in range(3):
        send_key(VK_F8)
        time.sleep(0.3)
    print("  - 已切换到日K线")
    time.sleep(0.5)
    
    # 获取窗口大小
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    win_width = rect.right - rect.left
    win_height = rect.bottom - rect.top
    
    print(f"\n窗口大小: {win_width}x{win_height}")
    
    # 截取上半部分（均线通常在上方）
    region_width = win_width
    region_height = win_height // 2
    region_left = 0
    region_top = 0
    
    print(f"截图区域: ({region_left}, {region_top}) {region_width}x{region_height}")
    
    # 截图
    print("\n正在截图...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bmp_path = f"ma_region_{timestamp}.bmp"
    
    success = capture_window_region(
        hwnd, region_left, region_top, region_width, region_height, bmp_path
    )
    
    if not success:
        print("❌ 截图失败")
        return
    
    size_kb = os.path.getsize(bmp_path) / 1024
    print(f"✅ 截图已保存: {bmp_path} ({size_kb:.1f}KB)")
    
    # 检查大小
    if size_kb > 900:
        print("⚠️ 图片太大，尝试截取更小的区域...")
        # 截取左上角（均线通常显示在K线图左上角）
        region_width = min(300, win_width)
        region_height = min(200, win_height)
        success = capture_window_region(
            hwnd, 0, 30, region_width, region_height, bmp_path  # 略微向下偏移
        )
        if success:
            size_kb = os.path.getsize(bmp_path) / 1024
            print(f"新截图大小: {size_kb:.1f}KB")
    
    # OCR识别
    print("\n正在进行OCR识别...")
    
    image_data, actual_size = bmp_to_jpeg_in_memory(bmp_path)
    
    if image_data is None:
        print(f"❌ 图片太大({actual_size:.1f}KB)，无法上传")
        print("请使用更小的窗口或安装Pillow进行压缩")
        return
    
    text = ocr_space_api(image_data, os.path.basename(bmp_path))
    
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
            print("\n⚠️ 未找到均线数值")
    else:
        print("❌ OCR识别失败")
    
    # 清理
    if not args.keep_screenshot:
        try:
            os.remove(bmp_path)
            print(f"\n已删除临时截图: {bmp_path}")
        except:
            pass


if __name__ == "__main__":
    main()
