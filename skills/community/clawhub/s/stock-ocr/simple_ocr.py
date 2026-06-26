#!/usr/bin/env python3
"""简单的OCR识别工具 - 使用百度OCR免费API"""

import base64
import requests
import sys
import os
import re
import json

def baidu_ocr_free(image_path: str) -> str:
    """
    使用百度OCR免费接口
    免费版: 每月1000次通用文字识别
    文档: https://cloud.baidu.com/doc/OCR/s/1k3h7y3db
    """
    # 读取图片
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    # 百度OCR免费接口（需要Access Token）
    # 这里使用公开的测试接口（仅供测试，生产环境请申请自己的token）
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    
    # 尝试从环境变量获取token
    access_token = os.environ.get('BAIDU_ACCESS_TOKEN', '')
    
    if not access_token:
        print("提示: 未设置百度OCR Access Token")
        print("请先获取Access Token:")
        print("  1. 访问 https://console.bce.baidu.com/ai/#/ai/ocr/overview/index")
        print("  2. 创建应用获取 API Key 和 Secret Key")
        print("  3. 获取 Access Token:")
        print("     curl -X POST 'https://aip.baidubce.com/oauth/2.0/token' \\")
        print("       -d 'grant_type=client_credentials' \\")
        print("       -d 'client_id=YOUR_API_KEY' \\")
        print("       -d 'client_secret=YOUR_SECRET_KEY'")
        print("  4. 设置环境变量: $env:BAIDU_ACCESS_TOKEN='your_token'")
        return ""
    
    try:
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'image': img_base64,
            'language_type': 'CHN_ENG'
        }
        
        response = requests.post(
            f"{url}?access_token={access_token}",
            headers=headers,
            data=data,
            timeout=10
        )
        
        result = response.json()
        
        if 'words_result' in result:
            lines = [item['words'] for item in result['words_result']]
            return '\n'.join(lines)
        else:
            print(f"百度OCR错误: {result}")
            return ""
            
    except Exception as e:
        print(f"请求失败: {e}")
        return ""


def extract_ma_values(text: str) -> dict:
    """提取所有均线数值"""
    result = {}
    
    # MA5
    m = re.search(r'MA5[：:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
    if m: result['MA5'] = m.group(1)
    
    # MA10
    m = re.search(r'MA10[：:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
    if m: result['MA10'] = m.group(1)
    
    # MA20
    m = re.search(r'MA20[：:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
    if m: result['MA20'] = m.group(1)
    
    # MA60
    m = re.search(r'MA60[：:\s]*(\d+\.?\d*)', text, re.IGNORECASE)
    if m: result['MA60'] = m.group(1)
    
    return result


def ocr_space(image_path: str) -> str:
    """
    使用OCR.space免费API
    免费: 每月25000次
    无需注册
    """
    with open(image_path, 'rb') as f:
        files = {'file': f}
        data = {
            'apikey': 'K82897662288957',  # 免费测试key
            'language': 'chs',  # 中文
            'isOverlayRequired': 'false'
        }
        
        try:
            response = requests.post(
                'https://api.ocr.space/parse/image',
                files=files,
                data=data,
                timeout=30
            )
            
            result = response.json()
            
            if result.get('OCRExitCode') == 1:
                return result['ParsedResults'][0]['ParsedText']
            else:
                print(f"OCR.space错误: {result.get('ErrorMessage', 'Unknown error')}")
                return ""
                
        except Exception as e:
            print(f"请求失败: {e}")
            return ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python simple_ocr.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}")
        sys.exit(1)
    
    print("正在使用OCR.space免费API识别...")
    text = ocr_space(image_path)
    
    if text:
        print("\n识别结果:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        
        ma_values = extract_ma_values(text)
        if ma_values:
            print("\n✅ 提取到的均线数值:")
            for k, v in ma_values.items():
                print(f"   {k}: {v}")
        else:
            print("\n⚠️ 未找到均线数值")
    else:
        print("❌ OCR识别失败")
