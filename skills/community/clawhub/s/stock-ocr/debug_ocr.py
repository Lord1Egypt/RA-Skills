#!/usr/bin/env python3
"""调试OCR识别结果"""

import os
import sys
import glob
import base64
import json
import urllib.request
import urllib.parse

os.environ['BAIDU_API_KEY'] = 'dNJctHLwok76vebSk8EP8aPG'
os.environ['BAIDU_SECRET_KEY'] = 'X989SIROeiQ776iBa4fCCsKFX2YWD3cA'

# 获取token
api_key = os.environ['BAIDU_API_KEY']
secret_key = os.environ['BAIDU_SECRET_KEY']
url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}"

with urllib.request.urlopen(url, timeout=10) as response:
    result = json.loads(response.read().decode())
    token = result['access_token']

# 查找最新的截图
script_dir = os.path.dirname(os.path.abspath(__file__))
png_files = glob.glob(os.path.join(script_dir, "ma_region_*.png"))
png_files.sort(key=os.path.getmtime, reverse=True)

if png_files:
    latest_png = png_files[0]
    print(f"分析截图: {os.path.basename(latest_png)}")
    print(f"文件大小: {os.path.getsize(latest_png)} bytes")
    
    # 读取图片
    with open(latest_png, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode()
    
    # 调用百度OCR
    ocr_url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={token}"
    data = urllib.parse.urlencode({'image': img_base64}).encode()
    
    req = urllib.request.Request(ocr_url, data=data)
    with urllib.request.urlopen(req, timeout=30) as response:
        result = json.loads(response.read().decode())
        
        print("\n百度OCR完整结果:")
        print("=" * 60)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        print("=" * 60)
        
        if 'words_result' in result:
            print("\n识别的文字行:")
            for i, item in enumerate(result['words_result']):
                print(f"  [{i}] {item['words']}")
else:
    print("未找到截图文件")
