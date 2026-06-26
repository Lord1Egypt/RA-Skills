#!/usr/bin/env python3
"""
股票MA20数值识别工具（ctypes版本）

使用Python ctypes直接调用Windows API
无需pywin32依赖

使用方法：
    python capture_ma20_ctypes.py --stock-code 000001
"""

import subprocess
import sys
import os
import re
import time
import ctypes
from ctypes import wintypes
from pathlib import Path
from datetime import datetime

# Windows API 定义
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

# 常量
VK_RETURN = 0x0D
VK_ESCAPE = 0x1B
VK_F5 = 0x74
VK_F8 = 0x77
KEYEVENTF_KEYUP = 0x0002
SW_RESTORE = 9

# 回调函数类型
EnumWindowsProc = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)


def find_window_by_title(title_pattern: str) -> tuple:
    """查找包含指定标题的窗口"""
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
    
    if result['hwnd']:
        return result['hwnd'], result['title']
    return None, None


def list_all_windows():
    """列出所有可见窗口"""
    windows = []
    
    def callback(hwnd, lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buffer, length + 1)
                title = buffer.value
                if title:
                    windows.append((hwnd, title))
        return True
    
    user32.EnumWindows(EnumWindowsProc(callback), 0)
    return windows


def set_foreground_window(hwnd):
    """将窗口设置为前台"""
    # 先恢复窗口
    user32.ShowWindow(hwnd, SW_RESTORE)
    # 设置前台
    user32.SetForegroundWindow(hwnd)


def send_key(vk_code: int):
    """发送单个按键"""
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def send_keys(text: str):
    """发送按键字符串"""
    for char in text:
        if char == '\n' or char == '\r':
            send_key(VK_RETURN)
        elif char == '\x1b':
            send_key(VK_ESCAPE)
        else:
            vk = user32.VkKeyScanW(ord(char))
            if vk != -1:
                vk_code = vk & 0xFF
                shift_state = (vk >> 8) & 1
                
                if shift_state:
                    user32.keybd_event(0x10, 0, 0, 0)  # Shift down
                
                user32.keybd_event(vk_code, 0, 0, 0)
                time.sleep(0.03)
                user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)
                
                if shift_state:
                    user32.keybd_event(0x10, 0, KEYEVENTF_KEYUP, 0)  # Shift up
        
        time.sleep(0.05)


def input_stock_code(hwnd, stock_code: str):
    """输入股票代码"""
    set_foreground_window(hwnd)
    time.sleep(0.2)
    
    # 按ESC清除
    send_key(VK_ESCAPE)
    time.sleep(0.1)
    
    # 输入代码
    send_keys(stock_code)
    time.sleep(0.3)
    
    # 回车确认
    send_key(VK_RETURN)
    print(f"  - 已输入股票代码: {stock_code}")


def switch_to_daily_kline(hwnd):
    """切换到日K线"""
    set_foreground_window(hwnd)
    time.sleep(0.2)
    
    # F5切换到K线图
    send_key(VK_F5)
    print("  - 按下F5切换到K线图")
    time.sleep(0.5)
    
    # F8切换到日K
    for i in range(3):
        send_key(VK_F8)
        print(f"  - 按下F8切换K线周期 ({i+1}/3)")
        time.sleep(0.3)


def capture_window(hwnd, output_path: str) -> bool:
    """截图窗口"""
    import struct
    
    # 获取窗口矩形
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    
    width = rect.right - rect.left
    height = rect.bottom - rect.top
    
    # 获取窗口DC
    hdc_window = user32.GetWindowDC(hwnd)
    hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_window)
    hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc_window, width, height)
    ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)
    
    # 截图
    ctypes.windll.gdi32.BitBlt(hdc_mem, 0, 0, width, height, hdc_window, 0, 0, 0x00CC0020)  # SRCCOPY
    
    # 保存为BMP
    # 创建BITMAPINFOHEADER
    bmi = struct.pack(
        'LLLHHLLLLLL',
        40,  # biSize
        width,  # biWidth
        height,  # biHeight
        1,  # biPlanes
        24,  # biBitCount
        0,  # biCompression (BI_RGB)
        0,  # biSizeImage
        0,  # biXPelsPerMeter
        0,  # biYPelsPerMeter
        0,  # biClrUsed
        0,  # biClrImportant
    )
    
    # 获取位图数据
    bufsize = width * height * 3
    buffer = ctypes.create_string_buffer(bufsize)
    ctypes.windll.gdi32.GetDIBits(hdc_mem, hbitmap, 0, height, buffer, bmi, 0)
    
    # 保存BMP文件
    with open(output_path, 'wb') as f:
        # BITMAPFILEHEADER
        f.write(struct.pack('HLHHL', 0x4D42, 54 + bufsize, 0, 0, 54))
        # BITMAPINFOHEADER
        f.write(bmi)
        # 位图数据
        f.write(buffer)
    
    # 清理
    ctypes.windll.gdi32.DeleteObject(hbitmap)
    ctypes.windll.gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(hwnd, hdc_window)
    
    return os.path.exists(output_path)


def convert_bmp_to_png(bmp_path: str, png_path: str):
    """将BMP转换为PNG"""
    try:
        from PIL import Image
        img = Image.open(bmp_path)
        img.save(png_path)
        os.remove(bmp_path)
        return True
    except:
        return False


def ocr_image(image_path: str, tesseract_path: str = None) -> str:
    """OCR识别图片"""
    if tesseract_path:
        os.environ['TESSERACT_CMD'] = tesseract_path
    
    try:
        import pytesseract
        from PIL import Image
        
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='chi_sim+eng')
        return text
    except ImportError:
        print("提示: 需要安装 pytesseract 和 Pillow 才能进行OCR")
        print("      pip install pytesseract Pillow")
        return ""
    except Exception as e:
        print(f"OCR错误: {e}")
        return ""


def extract_ma20_value(text: str) -> str:
    """提取MA20数值"""
    patterns = [
        r'MA20[：:\s]*(\d+\.?\d*)',
        r'MA20.*?(\d+\.?\d*)',
        r'20日均线[：:\s]*(\d+\.?\d*)',
        r'20MA[：:\s]*(\d+\.?\d*)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return ""


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='股票MA20数值识别工具(ctypes版)')
    parser.add_argument('-s', '--stock-code', required=False, help='股票代码')
    parser.add_argument('-w', '--window-title', default='金长江', help='窗口标题关键词')
    parser.add_argument('-o', '--output', help='截图保存路径')
    parser.add_argument('--keep-screenshot', action='store_true', help='保留截图')
    parser.add_argument('--tesseract-path', help='Tesseract路径')
    parser.add_argument('--list-windows', action='store_true', help='列出所有窗口')
    parser.add_argument('--delay', type=float, default=1.0, help='输入后等待时间')
    
    args = parser.parse_args()
    
    # 列出窗口模式
    if args.list_windows:
        print("正在列出所有可见窗口...")
        windows = list_all_windows()
        print(f"\n共找到 {len(windows)} 个可见窗口:")
        print("=" * 60)
        for hwnd, title in windows:
            print(f"  [{hwnd}] {title}")
        print("=" * 60)
        return
    
    # 查找窗口
    print(f"正在查找窗口: {args.window_title}")
    hwnd, title = find_window_by_title(args.window_title)
    
    if not hwnd:
        print(f"❌ 未找到包含 '{args.window_title}' 的窗口")
        print("\n提示: 使用 --list-windows 参数查看所有可见窗口")
        return
    
    print(f"✅ 找到窗口: {title} (hwnd={hwnd})")
    
    # 输入股票代码
    print(f"\n正在输入股票代码: {args.stock_code}")
    input_stock_code(hwnd, args.stock_code)
    time.sleep(args.delay)
    
    # 切换到日K线
    print("正在切换到日K线界面...")
    switch_to_daily_kline(hwnd)
    print("✅ 已切换到日K线")
    
    # 截图
    print("\n正在截图...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bmp_path = args.output or f"stock_screenshot_{timestamp}.bmp"
    png_path = bmp_path.replace('.bmp', '.png')
    
    success = capture_window(hwnd, bmp_path)
    
    if success:
        # 转换为PNG
        if convert_bmp_to_png(bmp_path, png_path):
            print(f"✅ 截图已保存: {png_path}")
            screenshot_path = png_path
        else:
            print(f"✅ 截图已保存: {bmp_path}")
            screenshot_path = bmp_path
    else:
        print("❌ 截图失败")
        return
    
    # OCR识别
    print("\n正在进行OCR识别...")
    text = ocr_image(screenshot_path, args.tesseract_path)
    
    if text:
        print("\n识别到的文字内容:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        
        # 提取MA20
        ma20 = extract_ma20_value(text)
        if ma20:
            print(f"\n✅ MA20数值: {ma20}")
        else:
            print("\n⚠️ 未能提取MA20数值")
    else:
        print("⚠️ OCR识别失败或未安装pytesseract")
        print(f"截图已保存: {screenshot_path}")
    
    # 清理
    if not args.keep_screenshot and not args.output:
        try:
            os.remove(screenshot_path)
            print(f"\n已删除临时截图: {screenshot_path}")
        except:
            pass


if __name__ == "__main__":
    main()
