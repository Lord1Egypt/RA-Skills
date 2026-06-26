# Native支付 - Python实现

> PC网站二维码扫码支付，适用于电脑端网页收款

## Native支付特点

| 特点 | 说明 |
|------|------|
| 下单产物 | code_url（二维码内容） |
| 调起方式 | 将code_url生成二维码，用户扫码支付 |
| 不需要openid | 直接下单即可 |
| 有效期 | 无明确过期时间，建议24小时内 |

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


class WechatPayNative:
    """微信Native支付"""
    
    def __init__(self, mchid, serial_no, private_key, appid, api_v3_key):
        self.mchid = mchid
        self.serial_no = serial_no
        self.private_key = private_key
        self.appid = appid
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
        
        if method == "GET":
            resp = requests.get(url, headers=headers)
        else:
            resp = requests.post(url, headers=headers, json=body)
        
        return resp.json()
    
    def prepay(self, out_trade_no, description, total_fee, notify_url):
        """
        Native下单
        
        Args:
            out_trade_no: 商户订单号
            description: 订单描述
            total_fee: 金额（分）
            notify_url: 支付结果回调地址
        
        Returns:
            dict: 包含code_url
        """
        url_path = "/v3/pay/transactions/native"
        body = {
            "appid": self.appid,
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
        
        if "code_url" in result:
            return {"code": 0, "code_url": result["code_url"]}
        else:
            return {"code": 1, "error": result}
    
    def query_order(self, out_trade_no):
        """查询订单"""
        url_path = f"/v3/pay/transactions/out-trade-no/{out_trade_no}"
        headers = {
            "Authorization": self._get_authorization("GET", url_path, ""),
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}{url_path}?mchid={self.mchid}"
        resp = requests.get(url, headers=headers)
        return resp.json()
    
    def close_order(self, out_trade_no):
        """关闭订单"""
        url_path = f"/v3/pay/transactions/out-trade-no/{out_trade_no}/close"
        body = {"mchid": self.mchid}
        return self._request("POST", url_path, body)


# ============ 使用示例 ============

if __name__ == "__main__":
    config = {
        "mchid": "1234567890",
        "serial_no": "XXXXXXXXXXXXXXXXXXXXXXXX",
        "private_key": """-----BEGIN PRIVATE KEY-----
...你的私钥...
-----END PRIVATE KEY-----""",
        "appid": "wxa5f5c1d6e8f9a2b3",
        "api_v3_key": "0123456789abcdef0123456789abcdef"
    }
    
    native_pay = WechatPayNative(**config)
    
    # 下单
    result = native_pay.prepay(
        out_trade_no=f"NATIVE{time.time()}",
        description="PC网站购物",
        total_fee=100,  # 1元
        notify_url="https://yourdomain.com/pay/notify"
    )
    
    if result["code"] == 0:
        code_url = result["code_url"]
        print(f"二维码内容: {code_url}")
        
        # ============ 生成二维码 ============
        # 使用qrcode库生成二维码图片
        try:
            import qrcode
            from io import BytesIO
            
            img = qrcode.make(code_url)
            buf = BytesIO()
            img.save(buf, format='PNG')
            buf.seek(0)
            
            # 保存二维码
            with open("qrcode.png", "wb") as f:
                f.write(buf.getvalue())
            
            print("二维码已保存到 qrcode.png")
        
        except ImportError:
            print("请安装qrcode库: pip install qrcode pillow")
            print(f"code_url: {code_url}")
```

## Flask网页展示示例

```python
from flask import Flask, Response, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

@app.route("/pay/qrcode/<order_id>")
def show_qrcode(order_id):
    """
    生成支付二维码页面
    """
    # 1. 查询订单获取code_url（省略）
    # code_url = get_order_code_url(order_id)
    code_url = "weixin://wxpay/bizpayurl?pr=xxxxx"
    
    # 2. 生成二维码图片
    img = qrcode.make(code_url)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    # 3. 返回图片
    return send_file(buf, mimetype='image/png')


@app.route("/pay/qrcode-page/<order_id>")
def qrcode_page(order_id):
    """
    展示二维码的HTML页面
    """
    return f"""
    <html>
    <head><title>扫码支付</title></head>
    <body>
        <h2>请使用微信扫码支付</h2>
        <img src="/pay/qrcode/{order_id}" />
        <p>支付完成后请关闭页面</p>
    </body>
    </html>
    """
```

## 轮询查询支付状态

```python
import time

def wait_for_payment(out_trade_no, timeout=300, interval=3):
    """
    轮询等待支付完成
    
    Args:
        out_trade_no: 商户订单号
        timeout: 超时时间（秒）
        interval: 轮询间隔（秒）
    
    Returns:
        dict: 订单状态
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        result = native_pay.query_order(out_trade_no)
        trade_state = result.get("trade_state")
        
        if trade_state == "SUCCESS":
            print(f"支付成功: {out_trade_no}")
            return result
        
        print(f"等待支付... {trade_state}")
        time.sleep(interval)
    
    print("支付超时")
    return None
```

## 注意事项

| 注意点 | 说明 |
|--------|------|
| 不需要openid | 直接下单即可 |
| 生成二维码 | 使用qrcode库或前端生成 |
| code_url不要截断 | 必须完整传入二维码生成器 |
| 不支持长按识别 | 微信Native支付不支持 |
| 建议设置超时 | 订单长时间未支付应关单 |
