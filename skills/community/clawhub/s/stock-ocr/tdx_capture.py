#!/usr/bin/env python3
"""通达信金融终端 - 日均线截图OCR (支持命令行参数指定股票代码)"""

import argparse
import ctypes
import ctypes.wintypes
import subprocess
import os
import sys
import time
import re
from datetime import datetime

# Windows API
user32 = ctypes.windll.user32
EnumWindowsProc = ctypes.CFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)

# 查找通达信窗口
result = {'hwnd': None, 'title': None}
def callback(hwnd, lparam):
    if user32.IsWindowVisible(hwnd):
        length = user32.GetWindowTextLengthW(hwnd)
        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buffer, length + 1)
            title = buffer.value
            if '通达信' in title:
                result['hwnd'] = hwnd
                result['title'] = title
                return False
    return True

user32.EnumWindows(EnumWindowsProc(callback), 0)
hwnd = result['hwnd']
title = result['title']

if not hwnd:
    print('未找到通达信窗口')
    sys.exit(1)

# 获取命令行参数
stock_code = '00700'
if len(sys.argv) > 1:
    stock_code = sys.argv[1]

print(f'找到窗口: {title}')

# 激活窗口
user32.ShowWindow(hwnd, 9)
user32.SetForegroundWindow(hwnd)
time.sleep(0.3)

# 输入股票代码
print(f'输入股票代码: {stock_code}')
VK_ESCAPE = 0x1B
VK_RETURN = 0x0D
KEYEVENTF_KEYUP = 0x0002

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

send_key(VK_ESCAPE)
time.sleep(0.1)
for c in stock_code:
    send_char(c)
    time.sleep(0.05)
time.sleep(0.3)
send_key(VK_RETURN)
print('已输入股票代码')
time.sleep(1.0)

# 输入96切换日K线
print('切换日K线 (96+回车)')
send_key(VK_ESCAPE)
time.sleep(0.1)
send_key(0x39)  # 9
time.sleep(0.1)
send_key(0x36)  # 6
time.sleep(0.2)
send_key(VK_RETURN)
time.sleep(1.0)
print('已切换日K线')

# 获取窗口位置
rect = ctypes.wintypes.RECT()
user32.GetWindowRect(hwnd, ctypes.byref(rect))
win_width = rect.right - rect.left
win_height = rect.bottom - rect.top

# 截取左上角均线区域
region_width = min(600, win_width)
region_height = min(80, win_height)
abs_left = rect.left
abs_top = rect.top

script_dir = r'C:\Users\Administrator\.workbuddy\skills\stock-ocr\scripts'
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
png_path = os.path.join(script_dir, f'tdx_ma_{timestamp}.png')

print(f'截图区域: ({abs_left},{abs_top}) {region_width}x{region_height}')

ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bitmap = New-Object System.Drawing.Bitmap {region_width}, {region_height}
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$size = New-Object System.Drawing.Size({region_width}, {region_height})
$graphics.CopyFromScreen({abs_left}, {abs_top}, 0, 0, $size)
$bitmap.Save("{png_path}", [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
Write-Output "OK"
'''

ps_result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True, timeout=10)
print(f'截图结果: {ps_result.stdout.strip()}')
if ps_result.stderr:
    print(f'stderr: {ps_result.stderr[:200]}')

if os.path.exists(png_path):
    size_kb = os.path.getsize(png_path) / 1024
    print(f'截图成功: {png_path} ({size_kb:.1f}KB)')
else:
    print('截图失败')
    sys.exit(1)

# OCR识别
sys.path.insert(0, script_dir)
from ocr_engines import recognize_with_engine

# 先用百度OCR
success, text = recognize_with_engine(png_path, 'baidu')
print(f'\n百度OCR结果: {success}')
print(f'原始文本: {text[:300]}')

if not success:
    print('\n百度OCR失败, 尝试Windows OCR...')
    success, text = recognize_with_engine(png_path, 'windows')
    print(f'Windows OCR结果: {success}')
    print(f'原始文本: {text[:300]}')

if success and text:
    # 提取MA数值
    # 提取股票名称
    stock_name = stock_code
    name_match = re.search(r'(\S+)[（(]日线[）)]', text)
    if name_match:
        stock_name = name_match.group(1)

    print(f'\n{"="*60}')
    print(f'📊 通达信 - {stock_name}({stock_code}) 日均线数值:')
    print(f'{"="*60}')
    
    # 尝试多种匹配模式
    patterns = [
        r'MA(\d+)[\s:：]+(\d+\.?\d*)',
        r'M(\d+)[\s:：]+(\d+\.?\d*)',
    ]
    
    found = {}
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            for period, value in matches:
                if period in ['5', '10', '20', '60']:
                    found[f'MA{period}'] = value
            if found:
                break
    
    if found:
        for k in ['MA5', 'MA10', 'MA20', 'MA60']:
            if k in found:
                print(f'  {k}: {found[k]}')
    else:
        # 如果没有匹配到MA格式，输出原始文本供分析
        print(f'  未能提取MA数值, 原始识别文本:')
        for line in text.strip().split('\n'):
            if line.strip():
                print(f'  {line.strip()}')

print(f'\n截图文件保留: {png_path}')
