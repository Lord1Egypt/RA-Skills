#!/usr/bin/env python3
"""
股票MA20数值获取工具 v3.0
1. 输入股票代码
2. 输入96回车切换到日K线界面
3. 截图左上角均线区域（使用PowerShell）
4. OCR识别MA20数值
"""

import ctypes
import ctypes.wintypes
import os
import sys
import time
import subprocess
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


def capture_with_powershell(hwnd, left, top, width, height, output_path):
    """使用PowerShell截图"""
    # 获取窗口位置
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    abs_left = rect.left + left
    abs_top = rect.top + top
    
    # PowerShell截图命令 - 使用format避免花括号冲突
    ps_script = '''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$bitmap = New-Object System.Drawing.Bitmap {0}, {1}
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$size = New-Object System.Drawing.Size({0}, {1})
$graphics.CopyFromScreen({2}, {3}, 0, 0, $size)
$bitmap.Save("{4}", [System.Drawing.Imaging.ImageFormat]::Bmp)
$graphics.Dispose()
$bitmap.Dispose()
Write-Output "OK"
'''.format(width, height, abs_left, abs_top, output_path.replace(os.sep, '/'))
    
    try:
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        return os.path.exists(output_path)
    except Exception as e:
        print(f"  PowerShell截图错误: {e}")
        return False


def ocr_image(image_path):
    """OCR识别"""
    try:
        import urllib.request
        import json
        
        # 读取图片
        with open(image_path, 'rb') as f:
            img_data = f.read()
        
        size_kb = len(img_data) / 1024
        print(f"  图片大小: {size_kb:.1f}KB")
        
        if size_kb > 900:
            print("  ⚠️ 图片太大，尝试压缩...")
            try:
                from PIL import Image
                import io
                
                img = Image.open(image_path)
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # 缩小尺寸
                max_dim = 1000
                if max(img.size) > max_dim:
                    ratio = max_dim / max(img.size)
                    new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
                    img = img.resize(new_size, Image.LANCZOS)
                
                # 压缩
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=60)
                img_data = output.getvalue()
                print(f"  压缩后: {len(img_data)/1024:.1f}KB")
            except:
                pass
        
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
        
        print("  正在OCR识别...")
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            if result.get('ParsedResults'):
                return result['ParsedResults'][0].get('ParsedText', '')
        return ''
    except Exception as e:
        print(f"  OCR错误: {e}")
        return ''


def extract_ma20(text):
    """提取MA20数值"""
    import re
    
    # 清理文本，替换常见的OCR错误
    text = text.replace('囗', '0')
    text = text.replace('０', '0')
    text = text.replace('：', ':')
    text = text.replace(' ', '')
    
    # 尝试匹配标准格式 MA20:123.45
    match = re.search(r'MA20[:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
    if match:
        return match.group(1), 'MA20'
    
    # 尝试匹配 M2囗 或 M20 格式（OCR可能识别错误）
    match = re.search(r'M2[0O]?[:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
    if match:
        return match.group(1), 'MA20'
    
    # 尝试匹配所有MA值（包括OCR错误格式）
    ma_values = {}
    
    # 标准格式
    for match in re.finditer(r'MA(\d+)[:\s]*(\d+\.?\d*)', text, re.IGNORECASE):
        ma_values[f'MA{match.group(1)}'] = match.group(2)
    
    # OCR错误格式：M5、M10、M2囗、M5囗 等
    for match in re.finditer(r'M(\d+)[0O]?[:\s]*(\d+\.?\d*)', text, re.IGNORECASE):
        period = match.group(1)
        if period in ['5', '10', '20', '60']:
            ma_values[f'MA{period}'] = match.group(2)
    
    # 尝试从连续格式中提取：MA5:123MA10:456MA20:789MA60:012
    # OCR可能变成：0M5：372囗MAI1322M2囗：353M5囗：478
    continuous = re.findall(r'[MA]*0?M(\d+)[0OI]?[:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
    for period, value in continuous:
        if period in ['5', '10', '20', '60']:
            ma_values[f'MA{period}'] = value
    
    if ma_values:
        return ma_values, 'ALL_MA'
    
    return None, None


def main():
    if len(sys.argv) < 2:
        print("用法: python ma20_v3.py <股票代码> [--keep]")
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
    print("  ✅ 已输入股票代码")
    time.sleep(1.0)

    # 2. 输入96回车切换到日K线
    print("\n步骤2: 输入96回车切换到日K线")
    send_key(VK_ESCAPE)  # 清空可能的输入
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

    # 4. 截取左上角均线区域（450x100）
    region_width = min(450, win_width)
    region_height = min(100, win_height)

    print(f"\n步骤3: 截图均线区域 ({region_width}x{region_height})")

    output_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bmp_path = os.path.join(output_dir, f"ma_region_{timestamp}.bmp")

    success = capture_with_powershell(hwnd, 0, 0, region_width, region_height, bmp_path)

    if not success:
        print("❌ 截图失败")
        return

    size_kb = os.path.getsize(bmp_path) / 1024
    print(f"✅ 截图成功: {bmp_path} ({size_kb:.1f}KB)")

    # 5. OCR识别
    print("\n步骤4: OCR识别MA20数值")
    text = ocr_image(bmp_path)
    
    if text:
        print(f"\n识别结果:")
        print("-" * 40)
        print(text.strip())
        print("-" * 40)
        
        value, match_type = extract_ma20(text)
        if match_type == 'MA20':
            print(f"\n✅ MA20 = {value}")
        elif match_type == 'ALL_MA':
            print(f"\n📊 找到的均线数值:")
            for name, val in value.items():
                print(f"   {name}: {val}")
            if 'MA20' in value:
                print(f"\n✅ MA20 = {value['MA20']}")
        else:
            print("\n⚠️ 未能提取MA20数值")
    else:
        print("❌ OCR识别失败")

    # 清理
    if not keep_screenshot:
        try:
            os.remove(bmp_path)
            print(f"\n已删除临时截图")
        except:
            pass
    else:
        print(f"\n截图已保留: {bmp_path}")


if __name__ == "__main__":
    main()
