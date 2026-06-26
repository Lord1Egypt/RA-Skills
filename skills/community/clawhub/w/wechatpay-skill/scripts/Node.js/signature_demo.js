#!/usr/bin/env node
/**
 * 微信支付V3签名演示脚本
 * 
 * 用途：演示微信支付V3 API的签名流程
 * 注意：此脚本仅用于学习和理解，实际使用时私钥必须通过安全方式加载
 */

const crypto = require('crypto');
const fs = require('fs');

class SignatureDemo {
    constructor(config) {
        this.mchid = config.mchid;
        this.serialNo = config.serialNo;
        this.privateKey = config.privateKey;
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

        console.log('='.repeat(50));
        console.log('签名串构造:');
        console.log('='.repeat(50));
        console.log(`方法: ${method}`);
        console.log(`路径: ${urlPath}`);
        console.log(`时间戳: ${timestamp}`);
        console.log(`随机串: ${nonce}`);
        console.log(`请求体: ${body}`);
        console.log('-'.repeat(50));
        console.log('签名串内容:');
        console.log(signStr);
        console.log('='.repeat(50));

        const signature = this.sign(signStr);

        // Authorization格式
        const auth = `WECHATPAY2-SHA256-RSA2048 mchid="${this.mchid}",nonce_str="${nonce}",timestamp="${timestamp}",serial_no="${this.serialNo}",signature="${signature}"`;

        return auth;
    }

    /**
     * 演示JSAPI/小程序调起签名
     */
    demoJsapiSign(prepayId) {
        console.log('\n' + '='.repeat(50));
        console.log('JSAPI/小程序调起签名演示');
        console.log('='.repeat(50));

        const timestamp = Math.floor(Date.now() / 1000).toString();
        const nonce = this.generateNonce();

        // 调起签名串（4行）
        // 注意：第四行是 prepay_id=xxx 格式！
        const signStr = `${this.mchid}\n${timestamp}\n${nonce}\nprepay_id=${prepayId}\n`;

        console.log(`appId/mchid: ${this.mchid}`);
        console.log(`时间戳: ${timestamp}`);
        console.log(`随机串: ${nonce}`);
        console.log(`package: prepay_id=${prepayId}`);
        console.log('-'.repeat(50));
        console.log('签名串内容:');
        console.log(signStr);

        const signature = this.sign(signStr);
        console.log('-'.repeat(50));
        console.log(`签名结果: ${signature}`);

        return {
            appId: this.mchid,
            timeStamp: timestamp,
            nonceStr: nonce,
            package: `prepay_id=${prepayId}`,
            signType: 'RSA',
            paySign: signature
        };
    }

    /**
     * 演示APP调起签名
     */
    demoAppSign(prepayId) {
        console.log('\n' + '='.repeat(50));
        console.log('APP调起签名演示');
        console.log('='.repeat(50));

        const timestamp = Math.floor(Date.now() / 1000).toString();
        const nonce = this.generateNonce();

        // APP调起签名串（4行）
        // 注意：第四行是纯prepay_id，不带 prepay_id= 前缀！
        const signStr = `${this.mchid}\n${timestamp}\n${nonce}\n${prepayId}\n`;

        console.log(`appId: ${this.mchid}`);
        console.log(`时间戳: ${timestamp}`);
        console.log(`随机串: ${nonce}`);
        console.log(`prepayId: ${prepayId}`);
        console.log('-'.repeat(50));
        console.log('签名串内容:');
        console.log(signStr);

        const signature = this.sign(signStr);
        console.log('-'.repeat(50));
        console.log(`签名结果: ${signature}`);

        return {
            appid: this.mchid,
            partnerid: this.mchid,
            prepayid: prepayId,
            package: 'Sign=WXPay',
            timestamp: timestamp,
            noncestr: nonce,
            sign: signature
        };
    }
}

function main() {
    // 示例配置
    const config = {
        mchid: '1234567890',
        serialNo: 'XXXXXXXXXXXXXXXXXXXXXXXX',
        // 从文件加载私钥
        privateKey: fs.readFileSync('apiclient_key.pem', 'utf8')
    };

    const demo = new SignatureDemo(config);

    // 演示接口请求签名
    console.log('\n' + '='.repeat(60));
    console.log('微信支付V3 API签名演示');
    console.log('='.repeat(60));

    // JSAPI下单签名
    const body = JSON.stringify({
        appid: 'wxa5f5c1d6e8f9a2b3',
        mchid: config.mchid,
        description: '测试商品',
        out_trade_no: 'ORDER123456',
        amount: { total: 1, currency: 'CNY' },
        payer: { openid: 'oUpF8xxxxxxxxxxxx' }
    });

    const auth = demo.getAuthorization('POST', '/v3/pay/transactions/jsapi', body);
    console.log('\nAuthorization头:');
    console.log(auth);

    // 演示调起签名
    const prepayId = 'wx201410272009395522657a690389285100';

    // JSAPI调起签名
    const jsapiParams = demo.demoJsapiSign(prepayId);

    // APP调起签名
    const appParams = demo.demoAppSign(prepayId);

    console.log('\n' + '='.repeat(60));
    console.log('签名演示完成');
    console.log('='.repeat(60));
}

main();
