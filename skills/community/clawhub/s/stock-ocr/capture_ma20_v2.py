#!/usr/bin/env python3
"""
股票MA20数值获取工具 v2.0
改进:
1. 集成多种OCR引擎 (Windows内置/百度高精度/Tesseract/RapidOCR)
2. 优化数字识别准确率
3. 支持OCR引擎对比测试

使用示例:
    python capture_ma20_v2.py 07226
    python capture_ma20_v2.py 000001 --engine baidu
    python capture_ma20_v2.py 07226 --compare-ocr
"""

import argparse
import ctypes
import ctypes.wintypes
import os
import re
import subprocess
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

# 导入OCR引擎模块
try:
    from ocr_engines import recognize_with_engine, compare_engines, get_available_engines
except ImportError:
    # 如果直接运行,尝试从同目录导入
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    from ocr_engines import recognize_with_engine, compare_engines, get_available_engines


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
    
    # PowerShell截图命令
    ps_script = '''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$bitmap = New-Object System.Drawing.Bitmap {0}, {1}
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$size = New-Object System.Drawing.Size({0}, {1})
$graphics.CopyFromScreen({2}, {3}, 0, 0, $size)
$bitmap.Save("{4}", [System.Drawing.Imaging.ImageFormat]::Png)
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


def extract_ma_values(text):
    """
    从OCR文本中提取所有MA数值
    
    支持多种格式:
    - MA5:3.720  MA10:3.922  MA20:3.953  MA60:4.780
    - MA5  3.720  MA10  3.922
    - M5:3720  M10:3922
    """
    ma_values = {}
    
    # 清理文本
    text = text.replace('：', ':')
    text = text.replace('０', '0')
    
    # 预期的MA周期
    periods = ['5', '10', '20', '60']
    
    # 尝试多种匹配模式
    patterns = [
        # 标准格式: MA5:3.720 或 MA5  3.720
        r'MA(\d+)[\s:]+(\d+\.?\d*)',
        # 简写格式: M5:3.720
        r'M(\d+)[\s:]+(\d+\.?\d*)',
        # 无MA前缀,但有数字冒号数字格式
        r'(\d+):(\d+\.?\d*)',
    ]
    
    found_values = []
    
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_values = matches
            break
    
    if not found_values:
        # 尝试提取所有数字序列
        numbers = re.findall(r'\d+\.?\d*', text)
        if len(numbers) >= 4:
            # 假设前4个数字对应MA5/MA10/MA20/MA60
            for i, num in enumerate(numbers[:4]):
                if i < len(periods):
                    ma_values[f'MA{periods[i]}'] = normalize_ma_value(num, periods[i])
    
    # 处理匹配到的值
    for i, (period, value) in enumerate(found_values[:4]):
        if period in periods:
            ma_values[f'MA{period}'] = normalize_ma_value(value, period)
        elif i < len(periods):
            # 如果周期不在预期列表中,按位置推断
            ma_values[f'MA{periods[i]}'] = normalize_ma_value(value, periods[i])
    
    return ma_values


def normalize_ma_value(value_str, period):
    """
    规范化MA数值
    股价通常是 X.XXX 格式（如 3.720）
    """
    # 清理常见OCR错误
    value_str = value_str.replace('囗', '0')
    value_str = value_str.replace('O', '0')
    value_str = value_str.replace('o', '0')
    value_str = value_str.replace('I', '1')
    value_str = value_str.replace('l', '1')
    
    # 移除所有非数字和非小数点字符
    value_str = re.sub(r'[^\d.]', '', value_str)
    
    # 如果已经有小数点，直接返回
    if '.' in value_str:
        # 确保小数点后有3位
        parts = value_str.split('.')
        if len(parts) == 2:
            integer_part = parts[0]
            decimal_part = parts[1].ljust(3, '0')[:3]
            return f"{integer_part}.{decimal_part}"
        return value_str
    
    # 没有小数点，需要智能添加
    if len(value_str) <= 1:
        return value_str
    
    # 如果是4位数，假设格式为 X.XXX
    if len(value_str) == 4:
        return f"{value_str[0]}.{value_str[1:]}"
    
    # 如果是3位数，补0
    if len(value_str) == 3:
        return f"{value_str[0]}.{value_str[1:]}0"
    
    # 其他情况，在倒数第3位加小数点
    if len(value_str) > 4:
        return f"{value_str[:-3]}.{value_str[-3:]}"
    
    return value_str


def main():
    parser = argparse.ArgumentParser(
        description='股票MA20数值获取工具 v2.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  %(prog)s 07226                     # 使用默认OCR引擎
  %(prog)s 000001 --engine baidu     # 使用百度高精度OCR
  %(prog)s 07226 --compare-ocr       # 对比所有OCR引擎结果
  %(prog)s --list-engines            # 列出可用OCR引擎
        '''
    )
    
    parser.add_argument('stock_code', nargs='?', help='股票代码')
    parser.add_argument('--engine', choices=['windows', 'baidu', 'tesseract', 'rapidocr', 'auto'],
                       default='auto', help='OCR引擎 (默认: auto)')
    parser.add_argument('--keep-screenshot', action='store_true', help='保留截图文件')
    parser.add_argument('--compare-ocr', action='store_true', help='对比所有OCR引擎')
    parser.add_argument('--list-engines', action='store_true', help='列出可用OCR引擎')
    parser.add_argument('--delay', type=float, default=1.0, help='输入后等待时间(秒)')
    
    args = parser.parse_args()
    
    # 列出可用引擎
    if args.list_engines:
        print("可用OCR引擎:")
        for name, available in get_available_engines().items():
            status = "✅" if available else "❌"
            desc = {
                'windows': 'Windows内置OCR (免费)',
                'baidu': '百度OCR高精度版 (需要API密钥)',
                'tesseract': 'Tesseract OCR (本地)',
                'rapidocr': 'RapidOCR (本地PaddleOCR)'
            }.get(name, '')
            print(f"  {status} {name:12s} - {desc}")
        return
    
    # 检查股票代码
    if not args.stock_code:
        parser.print_help()
        return
    
    stock_code = args.stock_code
    
    print(f"{'='*60}")
    print(f"股票MA20数值获取工具 v2.0")
    print(f"股票代码: {stock_code}")
    print(f"OCR引擎: {args.engine}")
    print(f"{'='*60}\n")
    
    # 查找窗口
    print(f"[1/5] 查找窗口: 金长江")
    hwnd, title = find_window("金长江")
    
    if not hwnd:
        print("❌ 未找到金长江窗口")
        print("   请确保金长江网上交易财智版已打开")
        return
    
    print(f"  ✅ 找到窗口: {title}")
    
    # 激活窗口
    user32.ShowWindow(hwnd, SW_RESTORE)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    
    # 输入股票代码
    print(f"\n[2/5] 输入股票代码: {stock_code}")
    send_key(VK_ESCAPE)
    time.sleep(0.1)
    for c in stock_code:
        send_char(c)
        time.sleep(0.05)
    time.sleep(0.3)
    send_key(VK_RETURN)
    print("  ✅ 已输入股票代码")
    time.sleep(args.delay)
    
    # 输入96回车切换到日K线
    print("\n[3/5] 切换到日K线: 输入96 + 回车")
    send_key(VK_ESCAPE)
    time.sleep(0.1)
    send_key(VK_9)
    time.sleep(0.1)
    send_key(VK_6)
    time.sleep(0.2)
    send_key(VK_RETURN)
    time.sleep(0.8)
    print("  ✅ 已切换到日K线")
    
    # 获取窗口大小
    rect = ctypes.wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    win_width = rect.right - rect.left
    win_height = rect.bottom - rect.top
    
    # 截取左上角均线区域 (扩大宽度到550以完整显示MA60)
    region_width = min(550, win_width)
    region_height = min(100, win_height)
    
    print(f"\n[4/5] 截图均线区域 ({region_width}x{region_height})")
    
    output_dir = os.path.dirname(os.path.abspath(__file__))
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    png_path = os.path.join(output_dir, f"ma_region_{timestamp}.png")
    
    success = capture_with_powershell(hwnd, 0, 0, region_width, region_height, png_path)
    
    if not success:
        print("  ❌ 截图失败")
        return
    
    size_kb = os.path.getsize(png_path) / 1024
    print(f"  ✅ 截图成功: {size_kb:.1f}KB")
    
    # OCR识别
    print(f"\n[5/5] OCR识别MA数值")
    
    if args.compare_ocr:
        # 对比所有引擎
        print("  对比所有OCR引擎结果...\n")
        results = compare_engines(png_path)
        
        best_result = None
        best_values = {}
        
        for engine_name, text in results.items():
            print(f"  {'='*50}")
            print(f"  引擎: {engine_name.upper()}")
            print(f"  {'='*50}")
            print(f"  原始结果: {text[:100]}...")
            
            # 提取MA数值
            ma_values = extract_ma_values(text)
            if ma_values:
                print(f"  提取结果:")
                for period in ['MA5', 'MA10', 'MA20', 'MA60']:
                    if period in ma_values:
                        print(f"    {period}: {ma_values[period]}")
                
                # 记录最佳结果
                if len(ma_values) > len(best_values):
                    best_values = ma_values
                    best_result = engine_name
            else:
                print("  ⚠️ 未能提取MA数值")
            print()
        
        # 显示最佳结果
        if best_values:
            print(f"\n{'='*60}")
            print(f"📊 最佳识别结果 (来自: {best_result})")
            print(f"{'='*60}")
            for period in ['MA5', 'MA10', 'MA20', 'MA60']:
                if period in best_values:
                    print(f"   {period}: {best_values[period]}")
            
            if 'MA20' in best_values:
                print(f"\n✅ MA20 = {best_values['MA20']}")
    else:
        # 使用指定引擎
        success, text = recognize_with_engine(png_path, args.engine)
        
        if not success:
            print(f"  ❌ OCR识别失败: {text}")
            return
        
        print(f"\n  OCR原始结果:")
        print("  " + "-" * 50)
        for line in text.strip().split('\n')[:5]:  # 只显示前5行
            if line.strip():
                print(f"  {line[:60]}")
        print("  " + "-" * 50)
        
        # 提取MA数值
        ma_values = extract_ma_values(text)
        
        if ma_values:
            print(f"\n{'='*60}")
            print("📊 均线数值:")
            print(f"{'='*60}")
            
            for period in ['MA5', 'MA10', 'MA20', 'MA60']:
                if period in ma_values:
                    print(f"   {period}: {ma_values[period]}")
            
            if 'MA20' in ma_values:
                print(f"\n✅ MA20 = {ma_values['MA20']}")
            else:
                print("\n⚠️ 未找到MA20数值")
        else:
            print("\n⚠️ 未能提取MA数值")
    
    # 清理临时文件
    if not args.keep_screenshot:
        try:
            os.remove(png_path)
        except:
            pass
    else:
        print(f"\n截图已保留: {png_path}")


if __name__ == "__main__":
    main()
