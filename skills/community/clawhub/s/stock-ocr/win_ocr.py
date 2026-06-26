#!/usr/bin/env python3
"""使用Windows内置OCR识别图片文字"""

import subprocess
import sys
import os

def ocr_with_windows(image_path: str) -> str:
    """
    使用Windows PowerShell调用内置OCR
    需要: Windows 10/11
    """
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

$imgPath = "{image_path.replace(chr(92), '/')}"

$storageFile = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($imgPath))
$stream = Await ($storageFile.OpenAsync([Windows.Storage.FileAccessMode]::Read))
$decoder = Await ([Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream))
$bitmap = Await ($decoder.GetSoftwareBitmapAsync())
$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
$result = Await ($engine.RecognizeAsync($bitmap))
$result.Text
'''
    
    try:
        result = subprocess.run(
            ['powershell', '-Command', ps_script],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        return result.stdout.strip()
    except Exception as e:
        print(f"Windows OCR错误: {e}")
        return ""


def extract_ma20(text: str) -> str:
    """提取MA20数值"""
    import re
    
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python win_ocr.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}")
        sys.exit(1)
    
    print("正在使用Windows内置OCR识别...")
    text = ocr_with_windows(image_path)
    
    if text:
        print("\n识别结果:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        
        ma20 = extract_ma20(text)
        if ma20:
            print(f"\n✅ MA20数值: {ma20}")
        else:
            print("\n⚠️ 未找到MA20数值")
    else:
        print("❌ OCR识别失败")
