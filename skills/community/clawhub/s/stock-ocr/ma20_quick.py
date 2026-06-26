#!/usr/bin/env python3
"""
股票MA20数值获取工具 - 快速版
仅截图并保存，OCR需要单独处理
"""

import ctypes
import ctypes.wintypes
import os
import struct
import sys
import time
from datetime import datetime

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


def capture_region(hwnd, left, top, width, height, output_path):
    hdc_window = user32.GetWindowDC(hwnd)
    hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_window)
    hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc_window, width, height)
    ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)
    ctypes.windll.gdi32.BitBlt(hdc_mem, 0, 0, width, height, hdc_window, left, top, 0x00CC0020)

    bmi = struct.pack('LLLHHLLLLLL', 40, width, height, 1, 24, 0, 0, 0, 0, 0, 0)
    bufsize = width * height * 3
    buffer = ctypes.create_string_buffer(bufsize)
    ctypes.windll.gdi32.GetDIBits(hdc_mem, hbitmap, 0, height, buffer, bmi, 0)

    with open(output_path, 'wb') as f:
        f.write(struct.pack('HLHHL', 0x4D42, 54 + bufsize, 0, 0, 54))
        f.write(bmi)
        f.write(buffer)

    ctypes.windll.gdi32.DeleteObject(hbitmap)
    ctypes.windll.gdi32.DeleteDC(hdc_mem)
    user32.ReleaseDC(hwnd, hdc_window)
    return os.path.exists(output_path)


def main():
    if len(sys.argv) < 2:
        print("用法: python ma20_quick.py <股票代码>")
        return

    stock_code = sys.argv[1]

    # 查找窗口
    print(f"正在查找窗口: 金长江")
    hwnd, title = find_window("金长江")

    if not hwnd:
        print("❌ 未找到金长江窗口")
        return

    print(f"✅ 找到窗口: {title}")

    # 激活窗口
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)

    # 输入股票代码
    print(f"\n正在输入股票代码: {stock_code}")
    send_key(VK_ESCAPE)
    time.sleep(0.1)
    for c in stock_code:
        send_char(c)
        time.sleep(0.05)
    time.sleep(0.3)
    send_key(VK_RETURN)
    print("  - 已输入")
    time.sleep(1.0)

    # 切换到日K线
    print("正在切换到日K线...")
    send_key(VK_F5)
    time.sleep(0.5)
    for _ in range(3):
        send_key(VK_F8)
        time.sleep(0.3)
    print("  - 已切换")
    time.sleep(0.5)

    # 获取窗口大小
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    win_width = rect.right - rect.left
    win_height = rect.bottom - rect.top

    # 截取均线区域（通常在K线图左上角）
    region_width = min(500, win_width)
    region_height = min(400, win_height)
    region_left = 0
    region_top = 0  # 从顶部开始截取

    print(f"\n截图区域: ({region_left}, {region_top}) {region_width}x{region_height}")

    # 截图
    output_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bmp_path = os.path.join(output_dir, f"MA20_{stock_code}_{timestamp}.bmp")

    print("\n正在截图...")
    success = capture_region(hwnd, region_left, region_top, region_width, region_height, bmp_path)

    if success:
        size_kb = os.path.getsize(bmp_path) / 1024
        print(f"✅ 截图已保存: {bmp_path} ({size_kb:.1f}KB)")
        print(f"\n请查看截图获取MA20数值")
    else:
        print("❌ 截图失败")


if __name__ == "__main__":
    main()
