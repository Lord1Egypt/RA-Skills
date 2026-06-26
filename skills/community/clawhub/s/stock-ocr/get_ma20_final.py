#!/usr/bin/env python3
"""
股票MA20数值识别工具 - 最终版本
使用PowerShell进行图片压缩和OCR
"""

import ctypes
import ctypes.wintypes
import os
import re
import subprocess
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


def capture_window_region(hwnd, left, top, width, height, output_path):
    """截取窗口指定区域并保存为BMP"""
    hdc_window = user32.GetWindowDC(hwnd)
    hdc_mem = ctypes.windll.gdi32.CreateCompatibleDC(hdc_window)
    hbitmap = ctypes.windll.gdi32.CreateCompatibleBitmap(hdc_window, width, height)
    ctypes.windll.gdi32.SelectObject(hdc_mem, hbitmap)
    
    ctypes.windll.gdi32.BitBlt(
        hdc_mem, 0, 0, width, height,
        hdc_window, left, top, 0x00CC0020
    )
    
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


def compress_and_ocr(image_path):
    """使用PowerShell压缩图片并调用OCR.space API"""
    ps_script = f'''
# 压缩图片
Add-Type -AssemblyName System.Drawing

$img = [System.Drawing.Image]::FromFile("{image_path.replace(chr(92), chr(92)+chr(92))}")

# 计算缩放比例
$maxDim = 1000
$ratio = [Math]::Min($maxDim / $img.Width, $maxDim / $img.Height)
if ($ratio -lt 1) {{
    $newWidth = [int]($img.Width * $ratio)
    $newHeight = [int]($img.Height * $ratio)
    $newImg = New-Object System.Drawing.Bitmap($newWidth, $newHeight)
    $g = [System.Drawing.Graphics]::FromImage($newImg)
    $g.DrawImage($img, 0, 0, $newWidth, $newHeight)
    $g.Dispose()
    $img.Dispose()
    $img = $newImg
}}

# 保存为JPEG
$jpegPath = "{image_path.replace(chr(92), chr(92)+chr(92))}.jpg"
$encoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object {{$_.MimeType -eq "image/jpeg"}}
$params = New-Object System.Drawing.Imaging.EncoderParameters(1)
$params.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, 60)
$img.Save($jpegPath, $encoder, $params)
$img.Dispose()

$fileSize = (Get-Item $jpegPath).Length / 1KB
Write-Host "压缩后大小: $fileSize KB"

# 读取文件并转Base64
$bytes = [System.IO.File]::ReadAllBytes($jpegPath)
$base64 = [Convert]::ToBase64String($bytes)

# 调用OCR.space API
$boundary = "----FormBoundary" + [Guid]::NewGuid().ToString("N")
$LF = "`r`n"

$body = @(
    "--$boundary",
    "Content-Disposition: form-data; name=`"file`"; filename=`"image.jpg`"",
    "Content-Type: image/jpeg",
    "",
    [System.Text.Encoding]::UTF8.GetString($bytes),
    "--$boundary",
    "Content-Disposition: form-data; name=`"apikey`"",
    "",
    "K82897662288957",
    "--$boundary",
    "Content-Disposition: form-data; name=`"language`"",
    "",
    "chs",
    "--$boundary",
    "Content-Disposition: form-data; name=`"isOverlayRequired`"",
    "",
    "false",
    "--$boundary--"
) -join $LF

try {{
    $response = Invoke-RestMethod -Uri "https://api.ocr.space/parse/image" `
        -Method Post `
        -ContentType "multipart/form-data; boundary=$boundary" `
        -Body ([System.Text.Encoding]::UTF8.GetBytes($body)) `
        -TimeoutSec 60
    
    if ($response.OCRExitCode -eq 1) {{
        Write-Host "---OCR_RESULT---"
        Write-Host $response.ParsedResults[0].ParsedText
        Write-Host "---END_RESULT---"
    }} else {{
        Write-Host "OCR Error: $($response.ErrorMessage)"
    }}
}} catch {{
    Write-Host "Request Error: $_"
}}

# 清理
Remove-Item $jpegPath -ErrorAction SilentlyContinue
'''
    
    result = subprocess.run(
        ['powershell', '-Command', ps_script],
        capture_output=True,
        text=True,
        encoding='utf-8',
        timeout=120
    )
    
    # 解析输出
    output = result.stdout
    if '---OCR_RESULT---' in output:
        start = output.index('---OCR_RESULT---') + len('---OCR_RESULT---')
        end = output.index('---END_RESULT---')
        return output[start:end].strip()
    
    print(f"PowerShell输出: {output}")
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
    
    # 截取包含均线的区域（K线图左上角）
    region_width = min(350, win_width)
    region_height = min(250, win_height)
    
    print(f"截图区域: {region_width}x{region_height}")
    
    # 截图
    print("\n正在截图...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bmp_path = os.path.abspath(f"ma_region_{timestamp}.bmp")
    
    success = capture_window_region(
        hwnd, 0, 30, region_width, region_height, bmp_path
    )
    
    if not success:
        print("❌ 截图失败")
        return
    
    size_kb = os.path.getsize(bmp_path) / 1024
    print(f"✅ 截图已保存: {bmp_path} ({size_kb:.1f}KB)")
    
    # OCR识别
    print("\n正在进行OCR识别...")
    text = compress_and_ocr(bmp_path)
    
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
