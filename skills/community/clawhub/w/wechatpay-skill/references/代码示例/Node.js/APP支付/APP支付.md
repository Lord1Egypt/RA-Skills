# APP支付 - Node.js实现

> iOS/Android原生App调起微信支付

## APP支付特点

| 特点 | 说明 |
|------|------|
| 调起参数 | appId, partnerId, prepayId, packageValue, timestamp, nonceStr, sign |
| 调起签名串 | 4行，第四行是纯prepay_id（不带prepay_id=前缀！） |
| package值 | 固定为 Sign=WXPay |
| SDK | 需要集成微信OpenSDK |

## 完整代码

```javascript
const crypto = require('crypto');
const axios = require('axios');
const fs = require('fs');

class WechatPayApp {
    constructor(config) {
        this.mchid = config.mchid;
        this.serialNo = config.serialNo;
        this.privateKey = config.privateKey;
        this.appid = config.appid;        // 移动应用AppID
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
     * APP下单
     */
    async prepay(outTradeNo, description, totalFee, notifyUrl) {
        const urlPath = '/v3/pay/transactions/app';
        const body = {
            appid: this.appid,           // 移动应用AppID
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
            if (result.prepay_id) {
                return { code: 0, prepayId: result.prepay_id };
            }
            return { code: 1, error: result };
        } catch (error) {
            return { code: 1, error: error.response?.data || error.message };
        }
    }

    /**
     * 获取APP调起支付签名参数
     * 
     * **重要**：APP调起签名的第四行是纯prepay_id，不带prepay_id=前缀！
     */
    getAppSignParams(prepayId) {
        const timestamp = Math.floor(Date.now() / 1000).toString();
        const nonce = this.generateNonce();

        // APP调起签名串（4行）
        // 注意：第四行是纯prepay_id，不是 prepay_id=xxx！
        const signStr = `${this.appid}\n${timestamp}\n${nonce}\n${prepayId}\n`;
        const signature = this.sign(signStr);

        return {
            appid: this.appid,
            partnerid: this.mchid,       // 商户号
            prepayid: prepayId,          // 纯prepay_id
            package: 'Sign=WXPay',        // 固定值
            timestamp: timestamp,
            noncestr: nonce,
            sign: signature
        };
    }
}


// ============ 使用示例 ============

async function main() {
    const config = {
        mchid: '1234567890',
        serialNo: 'XXXXXXXXXXXXXXXXXXXXXXXX',
        privateKey: fs.readFileSync('apiclient_key.pem', 'utf8'),
        appid: 'wx1234567890abcdef',    // 开放平台移动应用AppID
        apiV3Key: '0123456789abcdef0123456789abcdef'
    };

    const appPay = new WechatPayApp(config);

    // 1. 下单
    const orderResult = await appPay.prepay(
        `APP${Date.now()}`,
        'App内购商品',
        100,  // 1元
        'https://yourdomain.com/app/notify'
    );

    if (orderResult.code === 0) {
        console.log('下单成功，prepay_id:', orderResult.prepayId);

        // 2. 获取调起参数
        const signParams = appPay.getAppSignParams(orderResult.prepayId);
        console.log('调起参数:', signParams);

        // 3. 返回给App端
        // {
        //   appid: "wx1234567890abcdef",
        //   partnerid: "1234567890",
        //   prepayid: "wx201410272009395522657a690289100",
        //   package: "Sign=WXPay",
        //   timestamp: "1600000000",
        //   noncestr: "C5BE8E6B1B7A5D3E",
        //   sign: "xxxxx"
        // }
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
const WechatPayApp = require('./WechatPayApp');

const appPay = new WechatPayApp({
    mchid: '1234567890',
    serialNo: 'XXXXXXXXXXXXXXXXXXXXXXXX',
    privateKey: fs.readFileSync('apiclient_key.pem', 'utf8'),
    appid: 'wx1234567890abcdef',    // 开放平台移动应用AppID
    apiV3Key: '0123456789abcdef0123456789abcdef'
});

/**
 * 创建APP支付订单
 * POST /api/app/create-order
 */
router.post('/create-order', async (req, res) => {
    const { goodsId, amount } = req.body;

    try {
        const outTradeNo = `APP${Date.now()}`;
        const result = await appPay.prepay(
            outTradeNo,
            'App内购商品',
            amount,
            'https://yourdomain.com/app/notify'
        );

        if (result.code === 0) {
            // 返回调起参数给App端
            const signParams = appPay.getAppSignParams(result.prepayId);
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

// 注册WXEntryActivity（用于接收回调）
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

// WXApiDelegate接收回调
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
