#!/usr/bin/env python3
"""
使用在线OCR API进行图片文字识别

支持多种OCR服务：
1. 百度OCR API
2. 腾讯云OCR API
3. 阿里云OCR API

使用方法：
    python ocr_with_api.py --image screenshot.png --provider baidu
"""

import base64
import json
import sys
from pathlib import Path


def image_to_base64(image_path: str) -> str:
    """将图片转换为base64编码"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def baidu_ocr(image_base64: str, access_token: str) -> str:
    """
    使用百度OCR API识别图片
    
    文档: https://cloud.baidu.com/doc/OCR/s/1k3h7y3db
    """
    import requests
    
    url = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={access_token}"
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'image': image_base64,
        'language_type': 'CHN_ENG'  # 中英文混合
    }
    
    response = requests.post(url, headers=headers, data=data)
    result = response.json()
    
    if 'words_result' in result:
        texts = [item['words'] for item in result['words_result']]
        return '\n'.join(texts)
    else:
        raise Exception(f"百度OCR错误: {result}")


def tencent_ocr(image_base64: str, secret_id: str, secret_key: str) -> str:
    """
    使用腾讯云OCR API识别图片
    
    文档: https://cloud.tencent.com/document/product/866/33526
    """
    import hashlib
    import hmac
    import time
    import requests
    
    # 构造请求参数
    timestamp = int(time.time())
    date = time.strftime('%Y-%m-%d', time.gmtime(timestamp))
    
    host = "ocr.tencentcloudapi.com"
    service = "ocr"
    region = "ap-guangzhou"
    action = "GeneralAccurateOCR"
    version = "2018-11-19"
    
    payload = {
        "ImageBase64": image_base64,
        "LanguageType": "auto"
    }
    
    # 计算签名
    def sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
    
    # ... (签名计算过程省略，建议使用官方SDK)
    
    # 建议使用官方SDK
    try:
        from tencentcloud.common import credential
        from tencentcloud.ocr.v20181119 import ocr_client, models
        
        cred = credential.Credential(secret_id, secret_key)
        client = ocr_client.OcrClient(cred, region)
        
        req = models.GeneralAccurateOCRRequest()
        req.ImageBase64 = image_base64
        
        resp = client.GeneralAccurateOCR(req)
        
        texts = [item.DetectedText for item in resp.TextDetections]
        return '\n'.join(texts)
        
    except ImportError:
        print("请安装腾讯云SDK: pip install tencentcloud-sdk-python-ocr")
        raise


def aliyun_ocr(image_base64: str, access_key_id: str, access_key_secret: str) -> str:
    """
    使用阿里云OCR API识别图片
    
    文档: https://help.aliyun.com/document_detail/442274.html
    """
    try:
        from alibabacloud_ocr_api20210707.client import Client
        from alibabacloud_tea_openapi import models as open_api_models
        from alibabacloud_ocr_api20210707 import models as ocr_models
        
        config = open_api_models.Config(
            access_key_id=access_key_id,
            access_key_secret=access_key_secret
        )
        config.endpoint = "ocr-api.cn-hangzhou.aliyuncs.com"
        
        client = Client(config)
        request = ocr_models.RecognizeGeneralRequest()
        request.body = image_base64
        
        response = client.recognize_general(request)
        result = json.loads(response.body.data)
        
        if 'prism_wordsInfo' in result:
            texts = [item['word'] for item in result['prism_wordsInfo']]
            return '\n'.join(texts)
        
    except ImportError:
        print("请安装阿里云SDK: pip install alibabacloud-ocr-api20210707")
        raise


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='在线OCR识别工具')
    parser.add_argument('--image', required=True, help='图片路径')
    parser.add_argument('--provider', choices=['baidu', 'tencent', 'aliyun'], 
                       default='baidu', help='OCR服务提供商')
    
    args = parser.parse_args()
    
    # 读取图片
    image_base64 = image_to_base64(args.image)
    
    # 根据provider选择OCR服务
    if args.provider == 'baidu':
        # 需要设置环境变量 BAIDU_ACCESS_TOKEN
        import os
        access_token = os.environ.get('BAIDU_ACCESS_TOKEN')
        if not access_token:
            print("请设置环境变量 BAIDU_ACCESS_TOKEN")
            print("获取方式: https://console.bce.baidu.com/ai/#/ai/ocr/overview/index")
            sys.exit(1)
        
        text = baidu_ocr(image_base64, access_token)
        
    elif args.provider == 'tencent':
        import os
        secret_id = os.environ.get('TENCENT_SECRET_ID')
        secret_key = os.environ.get('TENCENT_SECRET_KEY')
        if not secret_id or not secret_key:
            print("请设置环境变量 TENCENT_SECRET_ID 和 TENCENT_SECRET_KEY")
            sys.exit(1)
        
        text = tencent_ocr(image_base64, secret_id, secret_key)
        
    elif args.provider == 'aliyun':
        import os
        access_key_id = os.environ.get('ALIYUN_ACCESS_KEY_ID')
        access_key_secret = os.environ.get('ALIYUN_ACCESS_KEY_SECRET')
        if not access_key_id or not access_key_secret:
            print("请设置环境变量 ALIYUN_ACCESS_KEY_ID 和 ALIYUN_ACCESS_KEY_SECRET")
            sys.exit(1)
        
        text = aliyun_ocr(image_base64, access_key_id, access_key_secret)
    
    print("识别结果:")
    print("-" * 40)
    print(text)
    print("-" * 40)
    
    return text


if __name__ == "__main__":
    main()
