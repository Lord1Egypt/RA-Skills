# JSAPI支付 - Node.js实现

> 基于微信支付V3 API，使用Node.js实现JSAPI支付下单

## 依赖

```bash
npm install axios crypto fs
```

## 完整代码

```javascript
const crypto = require('crypto');
const axios = require('axios');
const fs = require('fs');

class WechatPayV3 {
    constructor(config) {
        this.mchid = config.mchid;                    // 商户号
        this.serialNo = config.serialNo;            // 证书序列号
        this.privateKey = config.privateKey;        // 商户私钥
        this.appid = config.appid;                  // AppID
        this.apiV3Key = config.apiV3Key;             // APIv3密钥
        this.baseURL = 'https://api.mch.weixin.qq.com';
    }

    /**
     * 生成随机字符串
     */
    generateNonce(length = 32) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    /**
     * V3签名
     */
    sign(signStr) {
        const sign = crypto.sign('RSA-SHA256', Buffer.from(signStr), this.privateKey);
        return sign.toString('base64');
    }

    /**
     * 生成Authorization头
     */
    getAuthorization(method, urlPath, body = '') {
        const timestamp = Math.floor(Date.now() / 1000).toString();
        const nonce = this.generateNonce();

        // 签名串构造（5行格式）
        const signStr = `${method}\n${urlPath}\n${timestamp}\n${nonce}\n${body}\n`;
        const signature = this.sign(signStr);

        return `WECHATPAY2-SHA256-RSA2048 mchid="${this.mchid}",nonce_str="${nonce}",timestamp="${timestamp}",serial_no="${this.serialNo}",signature="${signature}"`;
    }

    /**
     * 发送请求
     */
    async request(method, urlPath, body = null) {
        const url = this.baseURL + urlPath;
        const headers = {
            'Authorization': this.getAuthorization(method, urlPath, body ? JSON.stringify(body) : ''),
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        };

        let response;
        if (method === 'GET') {
            response = await axios.get(url, { headers });
        } else {
            response = await axios.post(url, body, { headers });
        }

        return response.data;
    }

    /**
     * JSAPI下单
     */
    async jsapiPrepay(outTradeNo, description, totalFee, openid, notifyUrl) {
        const urlPath = '/v3/pay/transactions/jsapi';
        const body = {
            appid: this.appid,
            mchid: this.mchid,
            description: description,
            out_trade_no: outTradeNo,
            notify_url: notifyUrl,
            amount: {
                total: totalFee,      // 金额，单位分
                currency: 'CNY'
            },
            payer: {
                openid: openid
            }
        };

        try {
            const result = await this.request('POST', urlPath, body);
            if (result.prepay_id) {
                return { code: 0, prepayId: result.prepay_id };
            }
            return { code: 1, error: result };
        } catch (error) {
            return { code: 1, error: error.response?.data || error.message };
        }
    }

    /**
     * 获取JSAPI调起支付签名参数
     */
    getJsapiSignParams(prepayId) {
        const timestamp = Math.floor(Date.now() / 1000).toString();
        const nonce = this.generateNonce();

        // 调起签名串（4行）
        // 第四行必须是 prepay_id=xxx 格式！
        const signStr = `${this.appid}\n${timestamp}\n${nonce}\nprepay_id=${prepayId}\n`;
        const signature = this.sign(signStr);

        return {
            appId: this.appid,
            timeStamp: timestamp,
            nonceStr: nonce,
            package: `prepay_id=${prepayId}`,
            signType: 'RSA',
            paySign: signature
        };
    }

    /**
     * 查询订单
     */
    async queryOrder(outTradeNo) {
        const urlPath = `/v3/pay/transactions/out-trade-no/${outTradeNo}`;
        return this.request('GET', urlPath);
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
    // 配置
    const config = {
        mchid: '1234567890',
        serialNo: 'XXXXXXXXXXXXXXXXXXXXXXXX',
        privateKey: fs.readFileSync('apiclient_key.pem', 'utf8'),  // 从文件加载
        appid: 'wxa5f5c1d6e8f9a2b3',
        apiV3Key: '0123456789abcdef0123456789abcdef'
    };

    const wechat = new WechatPayV3(config);

    // 1. 下单
    const orderResult = await wechat.jsapiPrepay(
        `ORDER${Date.now()}`,           // 订单号（唯一）
        '测试商品',
        1,                                // 金额1分
        'oUpF8xxxxxxxxxxxx',             // 用户openid
        'https://yourdomain.com/pay/notify'
    );

    if (orderResult.code === 0) {
        console.log('下单成功，prepay_id:', orderResult.prepayId);

        // 2. 获取调起参数（返回给前端）
        const signParams = wechat.getJsapiSignParams(orderResult.prepayId);
        console.log('调起参数:', signParams);
    } else {
        console.error('下单失败:', orderResult.error);
    }
}

main();
```

## Express路由示例

```javascript
const express = require('express');
const router = express.Router();
const WechatPayV3 = require('./WechatPayV3');

const wechat = new WechatPayV3({
    mchid: '1234567890',
    serialNo: 'XXXXXXXXXXXXXXXXXXXXXXXX',
    privateKey: fs.readFileSync('apiclient_key.pem', 'utf8'),
    appid: 'wxa5f5c1d6e8f9a2b3',
    apiV3Key: '0123456789abcdef0123456789abcdef'
});

/**
 * 创建JSAPI支付订单
 * POST /api/jsapi/create-order
 */
router.post('/create-order', async (req, res) => {
    const { openid, goodsId, totalFee } = req.body;

    try {
        const outTradeNo = `ORDER${Date.now()}`;
        const result = await wechat.jsapiPrepay(
            outTradeNo,
            '商品描述',
            totalFee,  // 单位：分
            openid,
            'https://yourdomain.com/pay/notify'
        );

        if (result.code === 0) {
            // 返回调起参数给前端
            const signParams = wechat.getJsapiSignParams(result.prepayId);
            res.json({ success: true, data: signParams });
        } else {
            res.status(400).json({ success: false, error: result.error });
        }
    } catch (error) {
        console.error('创建订单失败:', error);
        res.status(500).json({ success: false, error: '服务器错误' });
    }
});

module.exports = router;
```

## 前端H5调用示例

```html
<script src="https://res.wx.qq.com/open/js/jweixin-1.6.0.js"></script>
<script>
async function createOrder() {
    // 获取openid（通过微信授权获取）
    const openid = await getOpenid();

    // 调用后端创建订单
    const response = await fetch('/api/jsapi/create-order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ openid, goodsId: 'xxx', totalFee: 100 })
    });
    const result = await response.json();

    if (result.success) {
        // 调起微信支付
        WeixinJSBridge.invoke('getBrandWCPayRequest', {
            appId: result.data.appId,
            timeStamp: result.data.timeStamp,
            nonceStr: result.data.nonceStr,
            package: result.data.package,
            signType: result.data.signType,
            paySign: result.data.paySign
        }, function(res) {
            if (res.err_msg === 'get_brand_wcpay_request:ok') {
                console.log('支付成功');
            } else {
                console.log('支付失败', res.err_msg);
            }
        });
    }
}
</script>
```

## 注意事项

| 注意点 | 说明 |
|--------|------|
| 金额单位 | 必须是整数（分），1元=100分 |
| 订单号唯一 | 每次下单必须生成新的out_trade_no |
| openid获取 | 需要通过微信授权获取 |
| prepay_id有效期 | 2小时，过期需重新下单 |
| 签名算法 | 使用RSA-SHA256 |
