# Native支付 - Node.js实现

> PC网站二维码扫码支付，适用于电脑端网页收款

## 完整代码

```javascript
const crypto = require('crypto');
const axios = require('axios');
const fs = require('fs');

class WechatPayNative {
    constructor(config) {
        this.mchid = config.mchid;
        this.serialNo = config.serialNo;
        this.privateKey = config.privateKey;
        this.appid = config.appid;
        this.apiV3Key = config.apiV3Key;
        this.baseURL = 'https://api.mch.weixin.qq.com';
    }

    generateNonce(length = 32) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    sign(signStr) {
        const sign = crypto.sign('RSA-SHA256', Buffer.from(signStr), this.privateKey);
        return sign.toString('base64');
    }

    getAuthorization(method, urlPath, body = '') {
        const timestamp = Math.floor(Date.now() / 1000).toString();
        const nonce = this.generateNonce();
        const signStr = `${method}\n${urlPath}\n${timestamp}\n${nonce}\n${body}\n`;
        const signature = this.sign(signStr);

        return `WECHATPAY2-SHA256-RSA2048 mchid="${this.mchid}",nonce_str="${nonce}",timestamp="${timestamp}",serial_no="${this.serialNo}",signature="${signature}"`;
    }

    async request(method, urlPath, body = null) {
        const url = this.baseURL + urlPath;
        const headers = {
            'Authorization': this.getAuthorization(method, urlPath, body ? JSON.stringify(body) : ''),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };

        const response = await axios.post(url, body, { headers });
        return response.data;
    }

    /**
     * Native下单
     */
    async prepay(outTradeNo, description, totalFee, notifyUrl) {
        const urlPath = '/v3/pay/transactions/native';
        const body = {
            appid: this.appid,
            mchid: this.mchid,
            description: description,
            out_trade_no: outTradeNo,
            notify_url: notifyUrl,
            amount: {
                total: totalFee,
                currency: 'CNY'
            }
        };

        try {
            const result = await this.request('POST', urlPath, body);
            if (result.code_url) {
                return { code: 0, codeUrl: result.code_url };
            }
            return { code: 1, error: result };
        } catch (error) {
            return { code: 1, error: error.response?.data || error.message };
        }
    }

    /**
     * 查询订单
     */
    async queryOrder(outTradeNo) {
        const urlPath = `/v3/pay/transactions/out-trade-no/${outTradeNo}`;
        const headers = {
            'Authorization': this.getAuthorization('GET', urlPath, ''),
            'Content-Type': 'application/json'
        };
        const url = `${this.baseURL}${urlPath}?mchid=${this.mchid}`;
        const response = await axios.get(url, { headers });
        return response.data;
    }

    /**
     * 关闭订单
     */
    async closeOrder(outTradeNo) {
        const urlPath = `/v3/pay/transactions/out-trade-no/${outTradeNo}/close`;
        const body = { mchid: this.mchid };
        return this.request('POST', urlPath, body);
    }
}


// ============ 使用示例 ============

async function main() {
    const config = {
        mchid: '1234567890',
        serialNo: 'XXXXXXXXXXXXXXXXXXXXXXXX',
        privateKey: fs.readFileSync('apiclient_key.pem', 'utf8'),
        appid: 'wxa5f5c1d6e8f9a2b3',
        apiV3Key: '0123456789abcdef0123456789abcdef'
    };

    const nativePay = new WechatPayNative(config);

    // 下单
    const result = await nativePay.prepay(
        `NATIVE${Date.now()}`,
        'PC网站购物',
        100,  // 1元
        'https://yourdomain.com/pay/notify'
    );

    if (result.code === 0) {
        console.log('code_url:', result.codeUrl);
        
        // ============ 生成二维码 ============
        // 前端使用 qrcode library 生成
        // 或后端使用 qrcode npm package
        console.log('将code_url转为二维码供用户扫码');
    } else {
        console.error('下单失败:', result.error);
    }
}

main();
```

## Express路由示例（返回二维码）

```javascript
const express = require('express');
const QRCode = require('qrcode');
const router = express.Router();
const WechatPayNative = require('./WechatPayNative');

const nativePay = new WechatPayNative({
    mchid: '1234567890',
    serialNo: 'XXXXXXXXXXXXXXXXXXXXXXXX',
    privateKey: fs.readFileSync('apiclient_key.pem', 'utf8'),
    appid: 'wxa5f5c1d6e8f9a2b3',
    apiV3Key: '0123456789abcdef0123456789abcdef'
});

/**
 * 创建Native支付订单，返回二维码
 * POST /api/native/create
 */
router.post('/create', async (req, res) => {
    const { orderId, amount } = req.body;

    try {
        const result = await nativePay.preay(
            orderId,
            '商品描述',
            amount,
            'https://yourdomain.com/pay/notify'
        );

        if (result.code === 0) {
            // 生成二维码
            const qrCodeDataUrl = await QRCode.toDataURL(result.codeUrl);
            res.json({ success: true, qrCode: qrCodeDataUrl });
        } else {
            res.status(400).json({ success: false, error: result.error });
        }
    } catch (error) {
        console.error('创建订单失败:', error);
        res.status(500).json({ success: false, error: '服务器错误' });
    }
});

/**
 * 查询订单状态（用于轮询）
 * GET /api/native/query/:outTradeNo
 */
router.get('/query/:outTradeNo', async (req, res) => {
    try {
        const result = await nativePay.queryOrder(req.params.outTradeNo);
        res.json({ success: true, data: result });
    } catch (error) {
        console.error('查询订单失败:', error);
        res.status(500).json({ success: false, error: '服务器错误' });
    }
});

module.exports = router;
```

## 前端轮询示例

```html
<!DOCTYPE html>
<html>
<head>
    <title>扫码支付</title>
    <script src="https://cdn.jsdelivr.net/npm/qrcode@1.5.1/build/qrcode.min.js"></script>
</head>
<body>
    <h2>请使用微信扫码支付</h2>
    <img id="qrcode" src="" alt="支付二维码">
    <p id="status">等待支付...</p>

    <script>
        // 获取订单ID
        const orderId = 'ORDER123456789';

        // 轮询查询支付状态
        function checkPayment() {
            fetch(`/api/native/query/${orderId}`)
                .then(r => r.json())
                .then(result => {
                    if (result.success) {
                        const tradeState = result.data.trade_state;
                        if (tradeState === 'SUCCESS') {
                            document.getElementById('status').textContent = '支付成功！';
                            // 跳转或提示
                        } else {
                            document.getElementById('status').textContent = '等待支付...';
                        }
                    }
                });
        }

        // 每3秒查询一次
        setInterval(checkPayment, 3000);
    </script>
</body>
</html>
```

## 注意事项

| 注意点 | 说明 |
|--------|------|
| 不需要openid | 直接下单即可 |
| 生成二维码 | 使用qrcode库或前端生成 |
| code_url不要截断 | 必须完整传入二维码生成器 |
| 不支持长按识别 | 微信Native支付不支持 |
| 建议设置超时 | 订单长时间未支付应关单 |
