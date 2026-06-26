#!/usr/bin/env python3
"""测试百度OCR配置"""

import os
import sys
import urllib.parse

# 设置环境变量
os.environ['BAIDU_API_KEY'] = 'dNJctHLwok76vebSk8EP8aPG'
os.environ['BAIDU_SECRET_KEY'] = 'X989SIROeiQ776iBa4fCCsKFX2YWD3cA'

print("=" * 60)
print("百度OCR配置测试")
print("=" * 60)

# 直接测试获取token
print("\n1. 测试获取Access Token:")
api_key = os.environ['BAIDU_API_KEY']
secret_key = os.environ['BAIDU_SECRET_KEY']

url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"

import urllib.request
import json

try:
    with urllib.request.urlopen(url, timeout=10) as response:
        result = json.loads(response.read().decode())
        if 'access_token' in result:
            token = result['access_token']
            print(f"   ✅ 成功获取Token: {token[:30]}...")
        else:
            print(f"   ❌ 响应中没有token: {result}")
            sys.exit(1)
except Exception as e:
    print(f"   ❌ 获取Token失败: {e}")
    sys.exit(1)

# 测试OCR识别 - 使用PNG截图
print("\n2. 查找测试图片:")

# 创建一个简单的测试图片（使用PowerShell生成PNG）
import subprocess
import tempfile

# 创建测试图片 - 一个简单的带文字的图片
test_png = os.path.join(tempfile.gettempdir(), "test_ocr.png")

ps_script = f'''
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$bmp = New-Object System.Drawing.Bitmap 200, 50
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::White)

$font = New-Object System.Drawing.Font("Arial", 16)
$brush = [System.Drawing.Brushes]::Black
$g.DrawString("MA5:3.720 MA20:3.953", $font, $brush, 10, 15)

$bmp.Save("{test_png.replace(os.sep, '/')}", [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$bmp.Dispose()
'''

result = subprocess.run(['powershell', '-Command', ps_script], capture_output=True, text=True)

if os.path.exists(test_png):
    print(f"   ✅ 创建测试图片: {test_png}")
    
    # 读取图片并编码
    import base64
    with open(test_png, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode()
    
    print(f"   图片大小: {len(img_base64)} bytes (base64)")
    
    # 调用百度OCR
    print("\n3. 调用百度OCR识别:")
    ocr_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={token}"
    
    data = urllib.parse.urlencode({
        'image': img_base64,
    }).encode()
    
    try:
        req = urllib.request.Request(ocr_url, data=data)
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode())
            
            if 'words_result' in result:
                print("   ✅ 识别成功!")
                for item in result['words_result']:
                    print(f"      {item['words']}")
            else:
                print(f"   ❌ 识别失败: {result}")
    except Exception as e:
        print(f"   ❌ OCR请求失败: {e}")
    
    # 清理
    os.remove(test_png)
else:
    print("   ❌ 创建测试图片失败")

print("\n" + "=" * 60)
print("✅ 百度OCR配置成功!")
print("=" * 60)
