#!/usr/bin/env python3
"""
微信支付V3签名演示脚本

用途：演示微信支付V3 API的签名流程
注意：此脚本仅用于学习和理解，实际使用时私钥必须通过安全方式加载
"""

import json
import time
import random
import string
import base64
import hashlib
from urllib.parse import urlparse

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


class SignatureDemo:
    """签名演示类"""
    
    def __init__(self, mchid, serial_no, private_key_path=None, private_key_pem=None):
        self.mchid = mchid
        self.serial_no = serial_no
        
        # 加载私钥
        if private_key_path:
            with open(private_key_path, 'r') as f:
                self.private_key = f.read()
        elif private_key_pem:
            self.private_key = private_key_pem
        else:
            raise ValueError("必须提供私钥文件路径或私钥内容")
    
    @staticmethod
    def generate_nonce(length=32):
        """生成随机字符串"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def sign(self, sign_str):
        """
        V3签名
        
        Args:
            sign_str: 待签名串
        
        Returns:
            str: Base64编码的签名
        """
        # 加载私钥
        private_key = serialization.load_pem_private_key(
            self.private_key.encode(),
            password=None,
            backend=default_backend()
        )
        
        # 签名
        signature = private_key.sign(
            sign_str.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode()
    
    def get_authorization(self, method, url_path, body=""):
        """
        生成Authorization头
        
        Args:
            method: HTTP方法（GET/POST）
            url_path: URL路径（不含域名）
            body: 请求体（GET请求为空）
        
        Returns:
            str: Authorization头值
        """
        timestamp = str(int(time.time()))
        nonce = self.generate_nonce()
        
        # 签名串构造（5行格式）
        sign_str = f"{method}\n{url_path}\n{timestamp}\n{nonce}\n{body}\n"
        
        print("=" * 50)
        print("签名串构造:")
        print("=" * 50)
        print(f"方法: {method}")
        print(f"路径: {url_path}")
        print(f"时间戳: {timestamp}")
        print(f"随机串: {nonce}")
        print(f"请求体: {body}")
        print("-" * 50)
        print("签名串内容:")
        print(sign_str)
        print("=" * 50)
        
        signature = self.sign(sign_str)
        
        # Authorization格式
        auth = (f'WECHATPAY2-SHA256-RSA2048 '
                f'mchid="{self.mchid}",'
                f'nonce_str="{nonce}",'
                f'timestamp="{timestamp}",'
                f'serial_no="{self.serial_no}",'
                f'signature="{signature}"')
        
        return auth
    
    def demo_jsapi_sign(self, prepay_id):
        """
        演示JSAPI/小程序调起签名
        
        注意：JSAPI和小程序的调起签名格式相同
        """
        print("\n" + "=" * 50)
        print("JSAPI/小程序调起签名演示")
        print("=" * 50)
        
        timestamp = str(int(time.time()))
        nonce = self.generate_nonce()
        
        # 调起签名串（4行）
        # 注意：第四行是 prepay_id=xxx 格式！
        sign_str = f"{self.mchid}\n{timestamp}\n{nonce}\nprepay_id={prepay_id}\n"
        
        print(f"appId/mchid: {self.mchid}")
        print(f"时间戳: {timestamp}")
        print(f"随机串: {nonce}")
        print(f"package: prepay_id={prepay_id}")
        print("-" * 50)
        print("签名串内容:")
        print(sign_str)
        
        signature = self.sign(sign_str)
        print("-" * 50)
        print(f"签名结果: {signature}")
        
        return {
            "appId": self.mchid,
            "timeStamp": timestamp,
            "nonceStr": nonce,
            "package": f"prepay_id={prepay_id}",
            "signType": "RSA",
            "paySign": signature
        }
    
    def demo_app_sign(self, prepay_id):
        """
        演示APP调起签名
        
        注意：APP的调起签名与JSAPI不同，第四行是纯prepay_id
        """
        print("\n" + "=" * 50)
        print("APP调起签名演示")
        print("=" * 50)
        
        timestamp = str(int(time.time()))
        nonce = self.generate_nonce()
        
        # APP调起签名串（4行）
        # 注意：第四行是纯prepay_id，不带 prepay_id= 前缀！
        sign_str = f"{self.mchid}\n{timestamp}\n{nonce}\n{prepay_id}\n"
        
        print(f"appId: {self.mchid}")
        print(f"时间戳: {timestamp}")
        print(f"随机串: {nonce}")
        print(f"prepayId: {prepay_id}")
        print("-" * 50)
        print("签名串内容:")
        print(sign_str)
        
        signature = self.sign(sign_str)
        print("-" * 50)
        print(f"签名结果: {signature}")
        
        return {
            "appid": self.mchid,
            "partnerid": self.mchid,
            "prepayid": prepay_id,
            "package": "Sign=WXPay",
            "timestamp": timestamp,
            "noncestr": nonce,
            "sign": signature
        }


def main():
    # 示例配置
    mchid = "1234567890"
    serial_no = "XXXXXXXXXXXXXXXXXXXXXXXX"
    
    # 示例私钥（请替换为你的真实私钥）
    private_key_pem = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDxxx...（请替换）
-----END PRIVATE KEY-----"""
    
    demo = SignatureDemo(mchid, serial_no, private_key_pem=private_key_pem)
    
    # 演示接口请求签名
    print("\n" + "=" * 60)
    print("微信支付V3 API签名演示")
    print("=" * 60)
    
    # JSAPI下单签名
    auth = demo.get_authorization(
        method="POST",
        url_path="/v3/pay/transactions/jsapi",
        body=json.dumps({
            "appid": "wxa5f5c1d6e8f9a2b3",
            "mchid": mchid,
            "description": "测试商品",
            "out_trade_no": "ORDER123456",
            "amount": {"total": 1, "currency": "CNY"},
            "payer": {"openid": "oUpF8xxxxxxxxxxxx"}
        })
    )
    print("\nAuthorization头:")
    print(auth)
    
    # 演示调起签名
    prepay_id = "wx201410272009395522657a690389285100"
    
    # JSAPI调起签名
    jsapi_params = demo.demo_jsapi_sign(prepay_id)
    
    # APP调起签名
    app_params = demo.demo_app_sign(prepay_id)
    
    print("\n" + "=" * 60)
    print("签名演示完成")
    print("=" * 60)


if __name__ == "__main__":
    main()
