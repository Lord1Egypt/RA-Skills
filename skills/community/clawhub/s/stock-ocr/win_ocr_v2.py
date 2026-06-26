#!/usr/bin/env python3
"""
Windows内置OCR引擎 (优化版)
修复编码问题,提高稳定性
"""

import os
import subprocess
import sys
import tempfile
from typing import Tuple


def ocr_with_windows(image_path: str) -> Tuple[bool, str]:
    """
    使用Windows内置OCR识别图片
    
    优势:
    - 免费,无需API密钥
    - Windows 10/11内置,无需安装
    - 支持多语言
    
    劣势:
    - PowerShell调用较慢
    - 数字识别精度一般
    
    Returns:
        (success, text or error_message)
    """
    # 创建临时PowerShell脚本文件
    ps_script = f'''
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? {{ $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' }})[0]

Function Await($WinRtTask) {{
    $asTask = $asTaskGeneric.MakeGenericMethod($WinRtTask.GetType().GenericTypeArguments)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}}

[Windows.Globalization.Language, Windows.Globalization, ContentType = WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.Streams.RandomAccessStreamReference, Windows.Storage.Streams, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.SoftwareBitmap, Windows.Graphics.Imaging, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Graphics.Imaging, ContentType = WindowsRuntime] | Out-Null

$imgPath = "{image_path.replace(os.sep, '/')}"

try {{
    $storageFile = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($imgPath))
    $stream = Await ($storageFile.OpenAsync([Windows.Storage.FileAccessMode]::Read))
    $decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream))
    $bitmap = Await ($decoder.GetSoftwareBitmapAsync())
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
    $result = Await ($engine.RecognizeAsync($bitmap))
    Write-Output $result.Text
}} catch {{
    Write-Error $_.Exception.Message
    exit 1
}}
'''
    
    # 写入临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8') as f:
        f.write(ps_script)
        ps_file = f.name
    
    try:
        # 执行PowerShell脚本
        result = subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        
        if result.returncode == 0 and result.stdout.strip():
            return True, result.stdout.strip()
        else:
            error_msg = result.stderr.strip() if result.stderr else "未知错误"
            return False, f"Windows OCR错误: {error_msg}"
            
    except subprocess.TimeoutExpired:
        return False, "Windows OCR超时"
    except Exception as e:
        return False, f"Windows OCR异常: {e}"
    finally:
        # 清理临时文件
        try:
            os.unlink(ps_file)
        except:
            pass


def ocr_with_windows_simple(image_path: str) -> Tuple[bool, str]:
    """
    使用Windows OCR的简化版本 (直接使用PowerShell命令)
    更稳定但功能受限
    """
    # 先转换BMP为PNG (Windows OCR对PNG支持更好)
    try:
        from PIL import Image
        
        img = Image.open(image_path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 创建临时PNG文件
        temp_png = image_path.replace('.bmp', '_temp.png')
        img.save(temp_png, 'PNG')
        
    except ImportError:
        temp_png = image_path
    except Exception as e:
        return False, f"图片转换错误: {e}"
    
    # 使用简化的PowerShell命令
    ps_cmd = f'''
$imagePath = "{temp_png.replace(os.sep, '/')}"

Add-Type -AssemblyName System.Runtime.WindowsRuntime

$asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() | ? {{ $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' }})[0]

Function Await($WinRtTask) {{
    $asTask = $asTaskGeneric.MakeGenericMethod($WinRtTask.GetType().GenericTypeArguments)
    $netTask = $asTask.Invoke($null, @($WinRtTask))
    $netTask.Wait(-1) | Out-Null
    $netTask.Result
}}

[Windows.Globalization.Language,Windows.Globalization,ContentType=WindowsRuntime] > $null
[Windows.Media.Ocr.OcrEngine,Windows.Foundation,ContentType=WindowsRuntime] > $null
[Windows.Storage.StorageFile,Windows.Storage,ContentType=WindowsRuntime] > $null
[Windows.Storage.Streams.RandomAccessStreamReference,Windows.Storage.Streams,ContentType=WindowsRuntime] > $null
[Windows.Graphics.Imaging.SoftwareBitmap,Windows.Graphics.Imaging,ContentType=WindowsRuntime] > $null
[Windows.Graphics.Imaging.BitmapDecoder,Windows.Graphics.Imaging,ContentType=WindowsRuntime] > $null

$file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($imagePath))
$stream = Await ($file.OpenAsync([Windows.Storage.FileAccessMode]::Read))
$decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream))
$bitmap = Await ($decoder.GetSoftwareBitmapAsync())
$ocr = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$result = Await ($ocr.RecognizeAsync($bitmap))
$result.Text
'''
    
    try:
        # 使用UTF-8编码写入临时文件
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ps1', delete=False, encoding='utf-8-sig') as f:
            f.write(ps_cmd)
            ps_file = f.name
        
        result = subprocess.run(
            ['powershell', '-ExecutionPolicy', 'Bypass', '-File', ps_file],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        
        # 清理临时文件
        try:
            os.unlink(ps_file)
            if temp_png != image_path:
                os.unlink(temp_png)
        except:
            pass
        
        if result.returncode == 0 and result.stdout.strip():
            return True, result.stdout.strip()
        else:
            return False, f"OCR识别失败: {result.stderr.strip() if result.stderr else '未知错误'}"
            
    except Exception as e:
        return False, f"OCR异常: {e}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python win_ocr_v2.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}")
        sys.exit(1)
    
    print("正在使用Windows内置OCR识别...")
    
    # 尝试简化版本
    success, text = ocr_with_windows_simple(image_path)
    
    if success:
        print("\n识别结果:")
        print("-" * 40)
        print(text)
        print("-" * 40)
    else:
        print(f"错误: {text}")
        sys.exit(1)
