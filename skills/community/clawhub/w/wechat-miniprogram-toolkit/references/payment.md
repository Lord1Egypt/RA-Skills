# 微信小程序支付能力全指南

## 激活契约

**符合以下任一场景时加载：**
- 涉及微信支付功能（购买商品、付费会员、打赏等）
- 需要在小程序内完成下单→支付→回调全流程
- 处理支付结果通知、退款、查询订单
- 涉及微信支付分（免押金）、商家转账到银行卡等高级能力

**不适用的场景：**
- 纯展示型小程序（无需支付）
- 已在服务端完成签名，直接传已完成订单的支付参数

---

## 一、支付能力概述

### 1.1 微信支付商户类型

| 商户类型 | 说明 | 开通入口 |
|---------|------|---------|
| 直连商户 | 自己申请微信支付商户号 | 微信支付商家平台 |
| 服务商 | 帮子商户申请支付能力 | 微信支付服务商平台 |
| 电商收付通 | 电商平台多商家场景 | 微信支付电商收付通 |

> 💡 **小程序接入微信支付的前提**：已申请微信支付商户号（mch_id）并完成入驻

### 1.2 支付能力矩阵

```
小程序 + 微信支付能力
├── Native 支付（扫码付）      ← 小程序内一般不用
├── JSAPI 支付（公众号/小程序） ← ✅ 小程序主要方式
├── APP 支付（移动端）          ← App和小程序互跳场景
├── H5 支付（网页）             ← 需绑定域名
├── 付款码支付（面对面）         ← 店员扫码
├── 人脸支付                   ← 特定行业
└── 小程序内支付（JSAPI 特化）  ← ✅ 小程序常用
```

---

## 二、JSAPI 支付全流程（小程序端）

### 2.1 整体流程图

```
用户点击购买
    ↓
① 小程序 → 云函数/服务端：创建订单，获取 prepay_id
    ↓
② 服务端返回：{ timeStamp, nonceStr, package, signType, paySign }
    ↓
③ 小程序调用：wx.requestPayment({...})
    ↓
④ 微信支付中间页（用户输入密码）
    ↓
⑤ 支付成功 → 微信服务器 → 商户后台（支付结果通知）
    ↓
⑥ 微信返回小程序：支付成功/失败回调
    ↓
⑦ 小程序展示结果，引导下一步
```

### 2.2 小程序端代码

```javascript
// pages/pay/pay.js
Page({
  data: {
    orderId: '',
    totalFee: 0.01,  // 单位：元（最低 0.01）
    goodsName: '会员月卡',
    loading: false,
  },

  // 步骤1：下单（获取 prepay_id）
  async createOrder() {
    const { totalFee, goodsName } = this.data

    this.setData({ loading: true })

    try {
      // ⚠️ 必须从服务端获取统一下单参数，绝不能在小程序端生成！
      const res = await wx.cloud.callFunction({
        name: 'createOrder',  // 云函数创建订单
        data: {
          totalFee: Math.round(totalFee * 100),  // 单位：分
          goodsName,
          userOpenid: wx.getStorageSync('openid'),
        },
      })

      if (res.result.code !== 0) {
        wx.showToast({ title: res.result.message, icon: 'none' })
        return
      }

      // 步骤2：调起微信支付
      await this.requestPayment(res.result.payParams)

    } catch (err) {
      wx.showToast({ title: '下单失败', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },

  // 步骤2：调起微信支付
  requestPayment(payParams) {
    return new Promise((resolve, reject) => {
      wx.requestPayment({
        ...payParams,
        // payParams 包含：
        // timeStamp: 时间戳（字符串）
        // nonceStr: 随机字符串
        // package: prepay_id=xxxx（统一下单返回）
        // signType: 'MD5' | 'HMAC-SHA256'
        // paySign: 签名

        success: () => {
          wx.showToast({ title: '支付成功', icon: 'success' })
          resolve('success')
        },

        fail: (err) => {
          // 用户取消或支付失败
          if (err.errMsg === 'requestPayment:fail cancel') {
            wx.showToast({ title: '用户取消支付', icon: 'none' })
          } else {
            wx.showToast({ title: '支付失败', icon: 'none' })
          }
          reject(err)
        },
      })
    })
  },

  // 步骤3：支付成功后查询订单状态（防伪造）
  async onPaySuccess() {
    const { orderId } = this.data
    const res = await wx.cloud.callFunction({
      name: 'queryOrder',
      data: { orderId },
    })

    if (res.result.tradeState === 'SUCCESS') {
      // ✅ 真正支付成功，更新本地状态
      this.setData({ paid: true })
      // 发放权益：会员、虚拟商品等
    } else {
      // ⚠️ 支付状态异常，进入异常处理流程
      await this.handlePayException(orderId)
    }
  },

  handlePayException(orderId) {
    wx.showModal({
      title: '支付状态核查中',
      content: '如已扣款，请联系客服处理。订单号：' + orderId,
      confirmText: '联系客服',
      success: (res) => {
        if (res.confirm) {
          wx.showToast({ title: '请联系客服处理', icon: 'none' })
        }
      },
    })
  },
})
```

```xml
<!-- pages/pay/pay.wxml -->
<view class="pay-container">
  <view class="goods-info">
    <text class="goods-name">{{goodsName}}</text>
    <text class="goods-price">¥{{totalFee}}</text>
  </view>

  <button
    type="primary"
    loading="{{loading}}"
    bindtap="createOrder"
    disabled="{{loading}}"
  >
    {{loading ? '下单中...' : '立即支付 ¥' + totalFee}}
  </button>

  <view class="agreement">
    <text>支付即表示同意</text>
    <text class="link" bindtap="openAgreement">《支付服务协议》</text>
  </view>
</view>
```

---

## 三、云函数：创建订单（服务端）

> ⚠️ **安全红线**：支付签名的所有逻辑必须在服务端（云函数）完成，绝不能在小程序前端生成！

### 3.1 创建订单云函数

```javascript
// cloudfunctions/createOrder/index.js
const cloud = require('wx-server-sdk')
const crypto = require('crypto')  // Node.js 内置，无需安装
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

const db = cloud.database()

// ⚠️ 以下信息必须从商户后台获取，存入云函数环境变量
const MCH_ID    = process.env.MCH_ID            // 商户号（mch_id），从云函数环境变量获取
const MCH_KEY   = process.env.MCH_KEY           // 微信支付密钥（32位），从云函数环境变量获取
// ⚠️ 绝对不要在前端暴露这些信息！
const APPID     = cloud.getWXContext().APPID
const NOTIFY_URL = 'https://your-cloudfunction.com/payNotify'  // 支付结果通知地址

// 云函数入口
exports.main = async (event, context) => {
  const { totalFee, goodsName, userOpenid } = event

  // 参数校验
  if (!totalFee || totalFee < 1) {
    return { code: -1, message: '金额不能少于0.01元' }
  }

  // 生成商户订单号（商户自行生成，不能重复）
  const outTradeNo = `${MCH_ID}${Date.now()}${Math.random().toString(36).slice(2, 8)}`

  try {
    // 调用微信支付统一下单 API
    const unifiedOrderRes = await cloud.cloudAPI.unifiedOrder({
      appid: APPID,
      mch_id: MCH_ID,
      nonce_str: generateNonceStr(),
      body: goodsName,
      out_trade_no: outTradeNo,
      total_fee: totalFee,        // 单位：分（必须是整数）
      spbill_create_ip: '127.0.0.1', // 用户 IP（小程序端传真实 IP）
      notify_url: NOTIFY_URL,
      trade_type: 'JSAPI',
      openid: userOpenid,
    })

    if (unifiedOrderRes.return_code !== 'SUCCESS') {
      return { code: -2, message: unifiedOrderRes.return_msg }
    }

    if (unifiedOrderRes.result_code !== 'SUCCESS') {
      return { code: -3, message: unifiedOrderRes.err_code_des }
    }

    // 统一下单成功，获取 prepay_id
    const prepayId = unifiedOrderRes.prepay_id

    // 生成小程序端调起支付所需的签名参数
    const payParams = {
      timeStamp: String(Math.floor(Date.now() / 1000)),
      nonceStr: generateNonceStr(),
      package: `prepay_id=${prepayId}`,
      signType: 'HMAC-SHA256',
      paySign: generatePaySign({
        appid: APPID,
        timeStamp: String(Math.floor(Date.now() / 1000)),
        nonceStr: generateNonceStr(),
        package: `prepay_id=${prepayId}`,
      }),
    }

    // 保存订单到数据库（状态：待支付）
    await db.collection('orders').add({
      data: {
        _id: outTradeNo,
        outTradeNo,
        userOpenid,
        goodsName,
        totalFee: Number(totalFee) / 100,
        status: 'pending',
        prepayId,
        createdAt: db.serverDate(),
      }
    })

    return {
      code: 0,
      message: '下单成功',
      orderId: outTradeNo,
      payParams,
    }

  } catch (err) {
    console.error('创建订单失败', err)
    return { code: -99, message: '系统异常，请稍后重试' }
  }
}

// 生成随机字符串
function generateNonceStr() {
  return crypto.randomBytes(16).toString('hex')
}

// 生成支付签名（HMAC-SHA256）
function generatePaySign(params) {
  const keys = Object.keys(params).sort()
  const str = keys.map(k => `${k}=${params[k]}`).join('&')
  const signStr = `${str}&key=${MCH_KEY}`
  return crypto.createHmac('sha256', MCH_KEY)
    .update(signStr, 'utf8')
    .digest('hex')
    .toUpperCase()
}
```

### 3.2 支付结果通知云函数

```javascript
// cloudfunctions/payNotify/index.js
const cloud = require('wx-server-sdk')
const crypto = require('crypto')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

const MCH_KEY = 'YOUR_MCH_KEY'  // 微信支付密钥

exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()
  const XMLParser = require('xml2js')  // 需安装：npm install xml2js

  // 微信支付通知是 XML 格式
  const rawXml = wxContext.request.body  // 原始 XML
  const notify = await XMLParser.parseStringPromise(rawXml)

  const { xml } = notify
  const {
    return_code,           // SUCCESS / FAIL
    transaction_id,         // 微信支付订单号
    out_trade_no,          // 商户订单号
    total_fee,             // 订单金额（分）
    cash_fee,              // 现金支付金额
    bank_type,             // 付款银行
    time_end,              // 支付时间
    sign,                  // 微信返回的签名
  } = xml

  // ⚠️ 验签：必须验证签名，防止伪造
  const isValid = verifySign(xml, MCH_KEY)
  if (!isValid) {
    return '<xml><return_code><![CDATA[FAIL]]></return_code><return_msg><![CDATA[签名验证失败]]></return_msg></xml>'
  }

  if (return_code[0] !== 'SUCCESS') {
    return '<xml><return_code><![CDATA[FAIL]]></return_code></xml>'
  }

  // 订单已处理过（防止重复通知）
  const db = cloud.database()
  const order = await db.collection('orders').doc(out_trade_no[0]).get()
  if (!order.data) {
    return '<xml><return_code><![CDATA[FAIL]]></return_code></xml>'
  }
  if (order.data.status === 'paid') {
    return '<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>'
  }

  // 更新订单状态
  await db.collection('orders').doc(out_trade_no[0]).update({
    data: {
      status: 'paid',
      transactionId: transaction_id[0],
      totalFee: Number(total_fee[0]) / 100,
      paidAt: time_end[0],
    }
  })

  // 触发后续业务逻辑：发货、发放会员等
  await cloud.callFunction({
    name: 'deliverGoods',
    data: { outTradeNo: out_trade_no[0] },
  })

  // 返回 SUCCESS 告知微信不要重发通知
  return '<xml><return_code><![CDATA[SUCCESS]]></return_code></xml>'
}

// 验证微信返回的签名
function verifySign(params, key) {
  const { sign, ...rest } = params
  const keys = Object.keys(rest).sort()
  const str = keys.map(k => `${k}=${Array.isArray(params[k]) ? params[k][0] : params[k]}`).join('&')
  const signStr = `${str}&key=${key}`
  const mySign = crypto.createHmac('sha256', key)
    .update(signStr, 'utf8')
    .digest('hex')
    .toUpperCase()
  return mySign === sign[0]
}
```

---

## 四、订单查询与退款

### 4.1 订单查询云函数

```javascript
// cloudfunctions/queryOrder/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { outTradeNo } = event

  // 1. 先查本地数据库
  const db = cloud.database()
  const localOrder = await db.collection('orders').doc(outTradeNo).get()

  // 2. 再查微信支付系统（验证真实状态）
  const wxRes = await cloud.cloudAPI.orderQuery({
    appid: cloud.getWXContext().APPID,
    mch_id: process.env.MCH_ID,
    out_trade_no: outTradeNo,
    nonce_str: require('crypto').randomBytes(16).toString('hex'),
  })

  return {
    code: 0,
    localStatus: localOrder.data?.status,
    tradeState: wxRes.trade_state,  // SUCCESS / NOTPAY / CLOSED / REFUND / ...
    wxData: wxRes,
  }
}
```

### 4.2 退款云函数

```javascript
// cloudfunctions/refund/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { outTradeNo, refundFee, reason } = event

  // 退款金额不能大于原支付金额
  const order = await cloud.database().collection('orders').doc(outTradeNo).get()
  if (!order.data || order.data.status !== 'paid') {
    return { code: -1, message: '订单状态不支持退款' }
  }

  if (refundFee > order.data.totalFee * 100) {
    return { code: -2, message: '退款金额超出支付金额' }
  }

  // 调用微信退款 API
  const refundRes = await cloud.cloudAPI.refund({
    appid: cloud.getWXContext().APPID,
    mch_id: process.env.MCH_ID,
    nonce_str: require('crypto').randomBytes(16).toString('hex'),
    transaction_id: order.data.transactionId,  // 微信订单号
    out_refund_no: `REF${outTradeNo}`,          // 商户退款单号
    total_fee: order.data.totalFee * 100,       // 原订单金额（分）
    refund_fee: refundFee,                       // 退款金额（分）
    refund_desc: reason || '用户申请退款',
  })

  if (refundRes.return_code === 'SUCCESS' && refundRes.result_code === 'SUCCESS') {
    // 更新订单状态
    await cloud.database().collection('orders').doc(outTradeNo).update({
      data: { status: 'refunded', refundFee: refundFee / 100 }
    })
    return { code: 0, message: '退款成功', refundId: refundRes.refund_id }
  }

  return { code: -3, message: '退款失败：' + (refundRes.err_code_des || refundRes.return_msg) }
}
```

---

## 五、支付安全规范（Common Mistakes）

| 错误做法 | 正确做法 |
|---------|---------|
| 在小程序前端生成签名 | 所有签名逻辑必须在云函数/服务端完成 |
| 将 MCH_KEY 硬编码在小程序前端 | 密钥存云函数环境变量，绝不暴露到前端 |
| 只依赖小程序支付回调判断支付成功 | 支付回调可能被伪造，必须查微信支付订单接口验证 |
| 订单金额前端传元（小数） | 金额必须前端传分（整数），后端校验范围 |
| 同一订单号重复发起支付 | 订单号必须有幂等性，重复支付应查订单状态 |
| 支付结果通知不验签 | 必须验证微信返回的 sign，防止伪造通知 |
| 不处理支付超时 | 设置订单超时（如30分钟），超时后关闭/标记订单 |
| refund_fee 传字符串 | 金额必须整数（分），不能有小数点 |

### 5.1 订单超时处理（定时关闭）

```javascript
// cloudfunctions/closeExpiredOrders/index.js
// 定时触发器：每小时执行一次
exports.main = async (event, context) => {
  const db = cloud.database()
  const expiredOrders = await db.collection('orders')
    .where({
      status: 'pending',
      createdAt: db.command.lt(
        // 30分钟前
        new Date(Date.now() - 30 * 60 * 1000)
      )
    })
    .limit(100)
    .get()

  let closed = 0
  for (const order of expiredOrders.data) {
    // 调用微信关闭订单 API
    await cloud.cloudAPI.closeOrder({
      appid: cloud.getWXContext().APPID,
      mch_id: process.env.MCH_ID,
      out_trade_no: order._id,
      nonce_str: require('crypto').randomBytes(16).toString('hex'),
    })
    await db.collection('orders').doc(order._id).update({
      data: { status: 'closed', closedReason: 'timeout' }
    })
    closed++
  }

  return { closed, total: expiredOrders.data.length }
}
```

---

## 六、低级坑点清单（微信支付高频错误）

1. **appid 和 mch_id 不匹配**：一个 mch_id 只能绑定一个 appid
2. **total_fee 必须整数（单位：分）**：`0.01` 传 `1`，`10元` 传 `1000`
3. **prepay_id 有效期 2 小时**：过期后需重新发起统一下单
4. **JSAPI 必须传 openid**：用户在小程序内，需传用户的 openid
5. **H5 支付域名校验**：必须在微信支付商户后台配置 H5 域名
6. **iv 字段大小写**：微信返回的 `iv` 是 Base64 字符串， AES 解密时注意填充模式
7. **退款必须原路退回**：默认退到支付账户，不能指定退款到其他账户（需服务商特殊权限）

---

## 七、官方文档链接

- 微信支付商户入驻：https://pay.weixin.qq.com/
- 小程序支付接入指引：https://pay.weixin.qq.com/doc/v3/partner/4012529174
- JSAPI 支付：https://pay.weixin.qq.com/doc/v3/partner/4012062524
- 支付结果通知：https://pay.weixin.qq.com/doc/v3/partner/4012095876
- 退款 API：https://pay.weixin.qq.com/doc/v3/partner/4012095913
