# APP支付 - Python实现

> iOS/Android原生App调起微信支付

## APP支付特点

| 特点 | 说明 |
|------|------|
| 调起参数 | appId, partnerId, prepayId, packageValue, timestamp, nonceStr, sign |
| 调起签名串 | 4行，第四行是纯prepay_id（不带prepay_id=前缀！） |
| package值 | 固定为 Sign=WXPay |
| SDK | 需要集成微信OpenSDK |

## 完整代码

```python
import json
import time
import random
import string
import base64

import requests
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend


class WechatPayApp:
    """微信APP支付"""
    
    def __init__(self, mchid, serial_no, private_key, appid, api_v3_key):
        self.mchid = mchid
        self.serial_no = serial_no
        self.private_key = private_key
        self.appid = appid        # 移动应用AppID（在开放平台申请）
        self.api_v3_key = api_v3_key
        self.base_url = "https://api.mch.weixin.qq.com"
    
    def _generate_nonce(self, length=32):
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def _sign(self, sign_str):
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
        timestamp = str(int(time.time()))
        nonce = self._generate_nonce()
        sign_str = f"{method}\n{url_path}\n{timestamp}\n{nonce}\n{body}\n"
        signature = self._sign(sign_str)
        
        return (f'WECHATPAY2-SHA256-RSA2048 '
                f'mchid="{self.mchid}",'
                f'nonce_str="{nonce}",'
                f'timestamp="{timestamp}",'
                f'serial_no="{self.serial_no}",'
                f'signature="{signature}"')
    
    def _request(self, method, url_path, body=None):
        url = self.base_url + url_path
        headers = {
            "Authorization": self._get_authorization(
                method, url_path, json.dumps(body) if body else ""
            ),
            "Content-Type": "application/json"
        }
        
        resp = requests.post(url, headers=headers, json=body)
        return resp.json()
    
    def prepay(self, out_trade_no, description, total_fee, notify_url):
        """
        APP下单
        """
        url_path = "/v3/pay/transactions/app"
        body = {
            "appid": self.appid,           # 移动应用AppID
            "mchid": self.mchid,
            "description": description,
            "out_trade_no": out_trade_no,
            "notify_url": notify_url,
            "amount": {
                "total": total_fee,
                "currency": "CNY"
            }
        }
        
        result = self._request("POST", url_path, body)
        
        if "prepay_id" in result:
            return {"code": 0, "prepay_id": result["prepay_id"]}
        else:
            return {"code": 1, "error": result}
    
    def get_app_sign_params(self, prepay_id):
        """
        获取APP调起支付签名参数
        
        **重要**：APP调起签名的第四行是纯prepay_id，不带prepay_id=前缀！
        
        Returns:
            dict: 调起参数
                - appid: 应用AppID
                - partnerid: 商户号
                - prepayid: 预下单ID
                - package: 固定值Sign=WXPay
                - timestamp: 时间戳
                - noncestr: 随机串
                - sign: 签名
        """
        timestamp = str(int(time.time()))
        nonce = self._generate_nonce()
        
        # APP调起签名串（4行）
        # 注意：第四行是纯prepay_id，不是prepay_id=xxx！
        sign_str = f"{self.appid}\n{timestamp}\n{nonce}\n{prepay_id}\n"
        signature = self._sign(sign_str)
        
        return {
            "appid": self.appid,
            "partnerid": self.mchid,       # 商户号
            "prepayid": prepay_id,          # 纯prepay_id
            "package": "Sign=WXPay",        # 固定值
            "timestamp": timestamp,
            "noncestr": nonce,
            "sign": signature
        }


# ============ 使用示例 ============

if __name__ == "__main__":
    config = {
        "mchid": "1234567890",
        "serial_no": "XXXXXXXXXXXXXXXXXXXXXXXX",
        "private_key": """-----BEGIN PRIVATE KEY-----
...你的私钥...
-----END PRIVATE KEY-----""",
        "appid": "wx1234567890abcdef",    # 开放平台移动应用AppID
        "api_v3_key": "0123456789abcdef0123456789abcdef"
    }
    
    app_pay = WechatPayApp(**config)
    
    # 1. 下单
    result = app_pay.prepay(
        out_trade_no=f"APP{time.time()}",
        description="App内购商品",
        total_fee=100,  # 1元
        notify_url="https://yourdomain.com/app/notify"
    )
    
    if result["code"] == 0:
        prepay_id = result["prepay_id"]
        
        # 2. 获取调起参数
        sign_params = app_pay.get_app_sign_params(prepay_id)
        print(f"调起参数: {sign_params}")
        
        # 3. 返回给App端（JSON）
        # App端使用这些参数调起微信支付
```

## Android端调起示例（Kotlin）

```kotlin
// Android端调起微信支付
val payReq = PayReq().apply {
    appId = result.appid           // 应用AppID
    partnerId = result.partnerid   // 商户号
    prepayId = result.prepayid     // 预下单ID
    packageValue = result.package  // Sign=WXPay
    timeStamp = result.timestamp    // 时间戳
    nonceStr = result.noncestr     // 随机串
    sign = result.sign             // 签名
}

// 调起微信支付
api.sendReq(payReq)
```

## iOS端调起示例（Objective-C）

```objc
// iOS端调起微信支付
PayReq *req = [[PayReq alloc] init];
req.appId = result[@"appid"];
req.partnerId = result[@"partnerid"];
req.prepayId = result[@"prepayid"];
req.package = result[@"package"];
req.timeStamp = [result[@"timestamp"] intValue];
req.nonceStr = result[@"noncestr"];
req.sign = result[@"sign"];

// 调起微信支付
[WXApi sendReq:req completion:nil];
```

## 注意事项

| 注意点 | 说明 |
|--------|------|
| AppID来源 | 开放平台移动应用AppID，不是公众号AppID |
| 调起签名第四行 | **纯prepay_id**，不是`prepay_id=xxx`！ |
| packageValue | 固定为`Sign=WXPay` |
| 包名一致性 | Android包名、iOS bundle ID必须与开放平台配置一致 |
| 签名一致性 | 调试签名、发布签名都要在开放平台配置 |

## 常见错误

| 错误 | 原因 |
|------|------|
| 调起失败 | AppID填错或包名不匹配 |
| 签名错误 | prepay_id带前缀/不带前缀混淆 |
| 收银台拉不起 | 微信未安装或签名配置问题 |
