#!/usr/bin/env python3
"""
股票MA20数值识别工具（PowerShell版本）

使用PowerShell代替pywin32进行窗口操作和截图
适用于pywin32不可用的环境

依赖：
- PowerShell 5.1+ (Windows内置)
- .NET Framework (Windows内置)
- Pillow: 图像处理
- pytesseract: OCR识别（可选）

使用方法：
    python capture_ma20_ps.py --stock-code 000001
"""

import subprocess
import sys
import os
import re
import time
from pathlib import Path
from datetime import datetime


def find_window_by_title(title_pattern: str) -> tuple:
    """
    使用PowerShell查找窗口
    
    Returns:
        (hwnd, title) 或 (None, None)
    """
    ps_script = f'''
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class Win32 {{
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  }}
"@

Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class EnumWindows {{
    public delegate bool CallBack(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern int EnumWindows(CallBack cb, IntPtr lParam);
    [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);
  }}
"@

$pattern = "{title_pattern}"
$foundHwnd = $null
$foundTitle = $null

$callback = {{
  param([IntPtr]$hWnd, [IntPtr]$lParam)
  if ([Win32]::IsWindowVisible($hWnd)) {{
    $sb = New-Object System.Text.StringBuilder 256
    [EnumWindows]::GetWindowText($hWnd, $sb, 256) | Out-Null
    $title = $sb.ToString()
    if ($title -and $title.Contains($pattern)) {{
      $script:foundHwnd = $hWnd
      $script:foundTitle = $title
      return $false
    }}
  }}
  return $true
}}

[EnumWindows]::EnumWindows($callback, [IntPtr]::Zero)

if ($foundHwnd) {{
  Write-Output $foundHwnd
  Write-Output $foundTitle
}}
'''
    result = subprocess.run(
        ['powershell', '-Command', ps_script],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    lines = result.stdout.strip().split('\n')
    if len(lines) >= 2:
        try:
            hwnd = lines[0].strip()
            title = lines[1].strip()
            return hwnd, title
        except:
            pass
    
    return None, None


def list_all_windows():
    """列出所有可见窗口"""
    ps_script = '''
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class Win32 {{
    [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr hWnd);
  }}
"@

Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class EnumWindows {{
    public delegate bool CallBack(IntPtr hWnd, IntPtr lParam);
    [DllImport("user32.dll")] public static extern int EnumWindows(CallBack cb, IntPtr lParam);
    [DllImport("user32.dll", CharSet=CharSet.Auto)] public static extern int GetWindowText(IntPtr hWnd, System.Text.StringBuilder lpString, int nMaxCount);
  }}
"@

$callback = {{
  param([IntPtr]$hWnd, [IntPtr]$lParam)
  if ([Win32]::IsWindowVisible($hWnd)) {{
    $sb = New-Object System.Text.StringBuilder 256
    [EnumWindows]::GetWindowText($hWnd, $sb, 256) | Out-Null
    $title = $sb.ToString()
    if ($title) {{
      Write-Output "$hWnd|$title"
    }}
  }}
  return $true
}}

[EnumWindows]::EnumWindows($callback, [IntPtr]::Zero)
'''
    result = subprocess.run(
        ['powershell', '-Command', ps_script],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    windows = []
    for line in result.stdout.strip().split('\n'):
        if '|' in line:
            parts = line.split('|', 1)
            if len(parts) == 2:
                hwnd, title = parts
                windows.append((hwnd.strip(), title.strip()))
    
    return windows


def send_fkey(key_code: int):
    """发送F键"""
    ps_script = f'''
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class Input {{
    [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    public const int KEYEVENTF_KEYUP = 0x0002;
  }}
"@

[Input]::keybd_event({key_code}, 0, 0, [UIntPtr]::Zero)
Start-Sleep -Milliseconds 50
[Input]::keybd_event({key_code}, 0, [Input]::KEYEVENTF_KEYUP, [UIntPtr]::Zero)
'''
    subprocess.run(['powershell', '-Command', ps_script])


def send_keys(keys: str):
    """发送按键字符串"""
    # 构建按键码列表
    key_events = []
    for char in keys:
        if char == '\n' or char == '\r':
            key_events.append((13, False))  # VK_RETURN
        elif char == '\t':
            key_events.append((9, False))   # VK_TAB
        elif char == '\x1b':
            key_events.append((27, False))  # VK_ESCAPE
        else:
            key_events.append((ord(char.upper()), char.isupper()))
    
    ps_parts = []
    for vk, shift in key_events:
        if shift:
            ps_parts.append(f'''
[Input]::keybd_event(16, 0, 0, [UIntPtr]::Zero)  # Shift down
[Input]::keybd_event({vk}, 0, 0, [UIntPtr]::Zero)
Start-Sleep -Milliseconds 30
[Input]::keybd_event({vk}, 0, [Input]::KEYEVENTF_KEYUP, [UIntPtr]::Zero)
[Input]::keybd_event(16, 0, [Input]::KEYEVENTF_KEYUP, [UIntPtr]::Zero)  # Shift up
''')
        else:
            ps_parts.append(f'''
[Input]::keybd_event({vk}, 0, 0, [UIntPtr]::Zero)
Start-Sleep -Milliseconds 30
[Input]::keybd_event({vk}, 0, [Input]::KEYEVENTF_KEYUP, [UIntPtr]::Zero)
''')
    
    ps_script = f'''
Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class Input {{
    [DllImport("user32.dll")] public static extern void keybd_event(byte bVk, byte bScan, uint dwFlags, UIntPtr dwExtraInfo);
    public const int KEYEVENTF_KEYUP = 0x0002;
  }}
"@

{''.join(ps_parts)}
'''
    subprocess.run(['powershell', '-Command', ps_script])


def capture_window(hwnd: str, output_path: str) -> bool:
    """截图窗口"""
    ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Add-Type @"
  using System;
  using System.Runtime.InteropServices;
  public class Rect {{
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [StructLayout(LayoutKind.Sequential)] public struct RECT {{ public int Left, Top, Right, Bottom; }}
  }}
"@

$handle = [IntPtr]{hwnd}
$rect = New-Object Rect+RECT
[Rect]::GetWindowRect($handle, [ref]$rect) | Out-Null

$width = $rect.Right - $rect.Left
$height = $rect.Bottom - $rect.Top

$bitmap = New-Object System.Drawing.Bitmap $width, $height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($rect.Left, $rect.Top, 0, 0, $bitmap.Size)
$graphics.Dispose()

$bitmap.Save("{output_path.replace(chr(92), chr(92)+chr(92))}")
$bitmap.Dispose()

Write-Output "OK"
'''
    result = subprocess.run(
        ['powershell', '-Command', ps_script],
        capture_output=True,
        text=True,
        encoding='utf-8'
    )
    
    return 'OK' in result.stdout and os.path.exists(output_path)


def input_stock_code(stock_code: str):
    """输入股票代码"""
    # 先按ESC清除
    send_keys('\x1b')
    time.sleep(0.1)
    
    # 输入代码
    send_keys(stock_code)
    time.sleep(0.3)
    
    # 回车确认
    send_keys('\n')


def switch_to_daily_kline():
    """切换到日K线"""
    # F5切换到K线图 (VK_F5 = 0x74 = 116)
    send_fkey(116)
    time.sleep(0.5)
    
    # F8切换K线周期 (VK_F8 = 0x77 = 119)
    for _ in range(3):
        send_fkey(119)
        time.sleep(0.3)


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
    
    parser = argparse.ArgumentParser(description='股票MA20数值识别工具(PowerShell版)')
    parser.add_argument('-s', '--stock-code', required=True, help='股票代码')
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
    input_stock_code(args.stock_code)
    time.sleep(args.delay)
    
    # 切换到日K线
    print("正在切换到日K线界面...")
    switch_to_daily_kline()
    print("✅ 已切换到日K线")
    
    # 截图
    print("\n正在截图...")
    screenshot_path = args.output or f"stock_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    success = capture_window(hwnd, screenshot_path)
    
    if success:
        print(f"✅ 截图已保存: {screenshot_path}")
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
