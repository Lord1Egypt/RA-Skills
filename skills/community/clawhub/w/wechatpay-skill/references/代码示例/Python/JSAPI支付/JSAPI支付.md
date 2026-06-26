# JSAPI支付 - Python实现

> 基于微信支付V3 API，使用Python实现JSAPI支付下单

## 依赖

```bash
pip install requests cryptography
```

## 完整代码

```python
import json
import time
import random
import string
import base64
import hashlib
from urllib.parse import urlparse

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


class WechatPayV3:
    """微信支付V3 API Python实现"""
    
    def __init__(self, mchid, serial_no, private_key, appid, api_v3_key):
        self.mchid = mchid                    # 商户号
        self.serial_no = serial_no            # 证书序列号
        self.private_key = private_key        # 商户私钥
        self.appid = appid                    # AppID
        self.api_v3_key = api_v3_key          # APIv3密钥
        self.base_url = "https://api.mch.weixin.qq.com"
    
    def _generate_nonce(self, length=32):
        """生成随机字符串"""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def _sign(self, sign_str):
        """V3签名"""
        private_key = serialization.load_pem_private_key(
            self.private_key.encode(),
            password=None,
            backend=default_backend()
        )
        signature = private_key.sign(
            sign_str.encode(),
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode()
    
    def _get_authorization(self, method, url_path, body=""):
        """生成Authorization头"""
        timestamp = str(int(time.time()))
        nonce = self._generate_nonce()
        
        # 签名串构造（5行格式）
        sign_str = f"{method}\n{url_path}\n{timestamp}\n{nonce}\n{body}\n"
        
        signature = self._sign(sign_str)
        
        # Authorization格式
        auth = (f'WECHATPAY2-SHA256-RSA2048 '
                f'mchid="{self.mchid}",'
                f'nonce_str="{nonce}",'
                f'timestamp="{timestamp}",'
                f'serial_no="{self.serial_no}",'
                f'signature="{signature}"')
        return auth
    
    def _request(self, method, url_path, body=None):
        """发送HTTP请求"""
        url = self.base_url + url_path
        headers = {
            "Authorization": self._get_authorization(
                method, url_path, json.dumps(body) if body else ""
            ),
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        if method == "GET":
            resp = requests.get(url, headers=headers)
        else:
            resp = requests.post(url, headers=headers, json=body)
        
        return resp.json()
    
    def jsapi_prepay(self, out_trade_no, description, total_fee, openid, notify_url):
        """
        JSAPI下单
        
        Args:
            out_trade_no: 商户订单号（全局唯一）
            description: 订单描述
            total_fee: 金额（分，整数）
            openid: 用户openid
            notify_url: 回调通知地址
        
        Returns:
            dict: 包含prepay_id
        """
        url_path = "/v3/pay/transactions/jsapi"
        body = {
            "appid": self.appid,
            "mchid": self.mchid,
            "description": description,
            "out_trade_no": out_trade_no,
            "notify_url": notify_url,
            "amount": {
                "total": total_fee,      # 金额，单位分
                "currency": "CNY"
            },
            "payer": {
                "openid": openid
            }
        }
        
        # 注意：POST请求的body参与签名，所以要用相同的body
        result = self._request("POST", url_path, body)
        
        if "prepay_id" in result:
            return {"code": 0, "prepay_id": result["prepay_id"]}
        else:
            return {"code": 1, "error": result}
    
    def close_order(self, out_trade_no):
        """关闭订单"""
        url_path = f"/v3/pay/transactions/out-trade-no/{out_trade_no}/close"
        body = {"mchid": self.mchid}
        return self._request("POST", url_path, body)
    
    def query_order_by_out_trade_no(self, out_trade_no):
        """查询订单（商户订单号）"""
        url_path = f"/v3/pay/transactions/out-trade-no/{out_trade_no}"
        params = {"mchid": self.mchid}
        url = f"{self.base_url}{url_path}?mchid={self.mchid}"
        return self._request("GET", url_path)


# ============ 使用示例 ============

if __name__ == "__main__":
    # 配置（请替换为你的真实配置）
    config = {
        "mchid": "1234567890",                    # 商户号
        "serial_no": "XXXXXXXXXXXXXXXXXXXXXXXX", # 证书序列号
        "private_key": """-----BEGIN PRIVATE KEY-----
...你的私钥...
-----END PRIVATE KEY-----""",
        "appid": "wxa5f5c1d6e8f9a2b3",           # AppID
        "api_v3_key": "0123456789abcdef0123456789abcdef"  # 32字节
    }
    
    wechat = WechatPayV3(**config)
    
    # 下单示例
    result = wechat.jsapi_prepay(
        out_trade_no=f"ORDER{int(time.time())}",  # 订单号（请确保唯一）
        description="测试商品",
        total_fee=1,                               # 金额1分
        openid="oUpF8xxxxxxxxxxxx",               # 用户openid
        notify_url="https://yourdomain.com/pay/notify"
    )
    
    print(result)
```

## 调起支付签名（前端）

后端需要返回调起支付签名参数：

```python
def get_jsapi_sign_params(self, prepay_id):
    """
    获取小程序/JSAPI调起支付签名参数
    
    Args:
        prepay_id: 下单返回的prepay_id
    
    Returns:
        dict: 包含appId, timeStamp, nonceStr, package, signType, paySign
    """
    timestamp = str(int(time.time()))
    nonce = self._generate_nonce()
    
    # 调起签名串（4行）
    sign_str = f"{self.appid}\n{timestamp}\n{nonce}\nprepay_id={prepay_id}\n"
    signature = self._sign(sign_str)
    
    return {
        "appId": self.appid,
        "timeStamp": timestamp,
        "nonceStr": nonce,
        "package": f"prepay_id={prepay_id}",
        "signType": "RSA",
        "paySign": signature
    }
```

## 注意事项

| 注意点 | 说明 |
|--------|------|
| 金额单位 | 必须是整数（分），1元=100分 |
| 订单号唯一 | 每次下单必须生成新的out_trade_no |
| openid获取 | 需要通过微信授权获取，不同AppID的openid不同 |
| prepay_id有效期 | 2小时，过期需重新下单 |
| 签名算法 | 使用SHA256-RSA，私钥必须是PKCS8格式 |

## 错误码参考

| 错误码 | 含义 |
|--------|------|
| INVALID_REQUEST | 参数问题 |
| SIGN_ERROR | 签名错误 |
| ORDER_NOT_EXISTS | 订单不存在 |
| ORDER_CLOSED | 订单已关闭 |
