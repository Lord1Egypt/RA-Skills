#!/usr/bin/env python3
"""
股票MA20数值获取工具 v2.0
1. 输入股票代码
2. 按96切换到日K线界面
3. 截图左上角均线区域
4. OCR识别MA20数值
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
VK_9 = 0x39
VK_6 = 0x36
KEYEVENTF_KEYUP = 0x0002


def find_window(title_pattern):
    """查找窗口"""
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
    """发送按键"""
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.05)
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def send_char(char):
    """发送字符"""
    vk = user32.VkKeyScanW(ord(char))
    if vk != -1:
        vk_code = vk & 0xFF
        user32.keybd_event(vk_code, 0, 0, 0)
        time.sleep(0.03)
        user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)


def capture_region(hwnd, left, top, width, height, output_path):
    """截图 - 使用更稳定的方式"""
    try:
        # 获取窗口DC
        hdc_window = user32.GetWindowDC(hwnd)
        if not hdc_window:
            print("  错误: 无法获取窗口DC")
            return False
        
        # 创建兼容DC和位图
        hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_window)
        hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc_window, width, height)
        
        if not hbitmap:
            print("  错误: 无法创建位图")
            ctypes.windll.gdi32.DeleteDC(hdc_mem)
            user32.ReleaseDC(hwnd, hdc_window)
            return False
        
        # 选入位图
        old_bitmap = ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)
        
        # 复制图像
        result = ctypes.windll.gdi32.BitBlt(hdc_mem, 0, 0, width, height, hdc_window, left, top, 0x00CC0020)
        if not result:
            print("  错误: BitBlt失败")
            ctypes.windll.gdi32.SelectObject(hdc_mem, old_bitmap)
            ctypes.windll.gdi32.DeleteObject(hbitmap)
            ctypes.windll.gdi32.DeleteDC(hdc_mem)
            user32.ReleaseDC(hwnd, hdc_window)
            return False
        
        # 准备BITMAPINFO
        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ('biSize', ctypes.wintypes.DWORD),
                ('biWidth', ctypes.wintypes.LONG),
                ('biHeight', ctypes.wintypes.LONG),
                ('biPlanes', ctypes.wintypes.WORD),
                ('biBitCount', ctypes.wintypes.WORD),
                ('biCompression', ctypes.wintypes.DWORD),
                ('biSizeImage', ctypes.wintypes.DWORD),
                ('biXPelsPerMeter', ctypes.wintypes.LONG),
                ('biYPelsPerMeter', ctypes.wintypes.LONG),
                ('biClrUsed', ctypes.wintypes.DWORD),
                ('biClrImportant', ctypes.wintypes.DWORD),
            ]
        
        bmi = BITMAPINFOHEADER()
        bmi.biSize = 40
        bmi.biWidth = width
        bmi.biHeight = height  # 正数表示从下到上
        bmi.biPlanes = 1
        bmi.biBitCount = 24
        bmi.biCompression = 0
        bmi.biSizeImage = width * height * 3
        
        # 分配缓冲区
        bufsize = width * height * 3
        buffer = ctypes.create_string_buffer(bufsize)
        
        # 获取位图数据
        result = ctypes.windll.gdi32.GetDIBits(
            hdc_mem, hbitmap, 0, height, 
            buffer, ctypes.byref(bmi), 0  # DIB_RGB_COLORS
        )
        
        if not result:
            print("  错误: GetDIBits失败")
            ctypes.windll.gdi32.SelectObject(hdc_mem, old_bitmap)
            ctypes.windll.gdi32.DeleteObject(hbitmap)
            ctypes.windll.gdi32.DeleteDC(hdc_mem)
            user32.ReleaseDC(hwnd, hdc_window)
            return False
        
        # 写入BMP文件
        with open(output_path, 'wb') as f:
            # BITMAPFILEHEADER
            f.write(b'BM')  # bfType
            f.write(ctypes.wintypes.DWORD(54 + bufsize))  # bfSize
            f.write(ctypes.wintypes.WORD(0))  # bfReserved1
            f.write(ctypes.wintypes.WORD(0))  # bfReserved2
            f.write(ctypes.wintypes.DWORD(54))  # bfOffBits
            
            # BITMAPINFOHEADER
            f.write(ctypes.string_at(ctypes.byref(bmi), 40))
            
            # 像素数据
            f.write(buffer)

        # 清理资源
        ctypes.windll.gdi32.SelectObject(hdc_mem, old_bitmap)
        ctypes.windll.gdi32.DeleteObject(hbitmap)
        ctypes.windll.gdi32.DeleteDC(hdc_mem)
        user32.ReleaseDC(hwnd, hdc_window)
        
        return os.path.exists(output_path)
    except Exception as e:
        print(f"  截图异常: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("用法: python ma20_v2.py <股票代码>")
        return

    stock_code = sys.argv[1]
    keep_screenshot = '--keep' in sys.argv

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

    # 1. 输入股票代码
    print(f"\n步骤1: 输入股票代码 {stock_code}")
    send_key(VK_ESCAPE)
    time.sleep(0.1)
    for c in stock_code:
        send_char(c)
        time.sleep(0.05)
    time.sleep(0.3)
    send_key(VK_RETURN)
    print("  ✅ 已输入")
    time.sleep(1.0)

    # 2. 按96切换到日K线
    print("\n步骤2: 按96回车切换到日K线")
    send_key(VK_ESCAPE)  # 先清空可能的输入
    time.sleep(0.1)
    send_key(VK_9)
    time.sleep(0.1)
    send_key(VK_6)
    time.sleep(0.2)
    send_key(VK_RETURN)  # 回车确认
    time.sleep(0.8)
    print("  ✅ 已切换到日K线")

    # 3. 获取窗口大小
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    win_width = rect.right - rect.left
    win_height = rect.bottom - rect.top

    # 4. 截取左上角均线区域
    # 均线区域在"日线 前复权"右边，通常是左上角
    region_width = min(450, win_width)
    region_height = min(100, win_height)
    region_left = 0
    region_top = 0

    print(f"\n步骤3: 截图均线区域 ({region_width}x{region_height})")

    # 截图
    output_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bmp_path = os.path.join(output_dir, f"ma_region_{timestamp}.bmp")

    success = capture_region(hwnd, region_left, region_top, region_width, region_height, bmp_path)

    if success:
        size_kb = os.path.getsize(bmp_path) / 1024
        print(f"✅ 截图已保存: {bmp_path} ({size_kb:.1f}KB)")
        print(f"\n请查看截图获取MA20数值")
        
        # 尝试OCR
        print("\n步骤4: OCR识别...")
        try:
            import urllib.request
            import json
            
            # 读取图片
            with open(bmp_path, 'rb') as f:
                img_data = f.read()
            
            # 如果图片太大，无法OCR
            if len(img_data) > 900 * 1024:
                print("  ⚠️ 图片太大，需要压缩")
            else:
                # 发送OCR请求
                url = "https://api.ocr.space/parse/image"
                boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
                
                body = f'--{boundary}\r\nContent-Disposition: form-data; name="apikey"\r\n\r\nK82897662288957\r\n--{boundary}\r\nContent-Disposition: form-data; name="language"\r\n\r\nchs\r\n--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="image.bmp"\r\nContent-Type: image/bmp\r\n\r\n'.encode()
                body += img_data
                body += f'\r\n--{boundary}--\r\n'.encode()
                
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers={'Content-Type': f'multipart/form-data; boundary={boundary}'}
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode())
                    if result.get('ParsedResults'):
                        text = result['ParsedResults'][0].get('ParsedText', '')
                        print(f"  识别结果:\n{text}")
                        
                        # 提取MA20
                        import re
                        match = re.search(r'MA20[:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
                        if match:
                            print(f"\n✅ MA20 = {match.group(1)}")
                        else:
                            print("\n⚠️ 未找到MA20数值")
        except Exception as e:
            print(f"  OCR失败: {e}")
        
        if not keep_screenshot:
            try:
                os.remove(bmp_path)
                print(f"\n已删除临时截图")
            except:
                pass
        else:
            print(f"\n截图已保留: {bmp_path}")
    else:
        print("❌ 截图失败")


if __name__ == "__main__":
    main()
