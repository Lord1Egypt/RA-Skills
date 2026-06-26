# 微信小程序客服与消息推送全指南

## 激活契约

**符合以下任一场景时加载：**
- 客服消息、客服会话、customer service、客服组件
- 订阅消息、模板消息、wx.requestSubscribeMessage
- 微信通知、消息推送、下发通知
- 客服自动回复、关键词回复、机器人客服
- 用户反馈、投诉建议、客服评价

---

## 一、消息类型全览

| 消息类型 | 触发方式 | 是否需用户许可 | 适用范围 |
|---------|---------|--------------|---------|
| 客服消息 | 客服组件 | 用户主动发起会话后 24h 内 | 任意小程序 |
| 订阅消息 | API 调用 | ✅ 用户点击订阅/全屏授权 | 一次性订阅/长期订阅 |
| 模板消息 | API 调用（已废弃）| ✅ 已废弃 | ⚠️ 已不再支持 |
| 微信支付通知 | 支付回调 | ❌ 不需要 | 仅支付成功通知 |
| 系统通知 | 微信官方 | ❌ 不需要 | 审核通知等官方消息 |

---

## 二、客服消息（客服组件）

### 2.1 开通客服

1. 微信公众平台 → 功能 → 客服 → 添加客服人员
2. 下载「微信客服」App（手机端接待）
3. 配置客服消息推送（接收消息的 URL 或企业微信）

### 2.2 小程序端接入客服按钮

```xml
<!-- 方式 A：button 组件（推荐）-->
<button open-type="contact" session-from="来源于:index,用户:{{userInfo.nickName}}">
  <image src="/assets/service-icon.png" />
  <text>联系客服</text>
</button>

<!-- 方式 B：内置客服图标（需基础库 ≥ 1.9.94）-->
<official-account>
  <!-- 关注公众号组件，同页面只能有一个 -->
</official-account>
```

```javascript
// 方式 C：在页面加载时自动显示客服入口（适合交易类页面）
Page({
  data: {
    showContact: false,
  },

  onShow() {
    // 交易类页面建议显示客服按钮
    const orderStatus = this.data.order?.status
    if (orderStatus === 'paid' || orderStatus === 'shipped') {
      this.setData({ showContact: true })
    }
  },
})
```

### 2.3 携带用户信息进入客服

```xml
<button
  open-type="contact"
  session-from="{{userInfo.nickName}};{{userInfo.avatarUrl}};{{orderId}}"
  bindcontact="onContact"
>
  联系客服
</button>
```

```javascript
// 接收客服回调（用户从客服会话返回）
Page({
  onContact(e) {
    // 用户从客服会话返回时的回调
    console.log('客服会话事件:', e.detail)

    // e.detail.eventType: 'userEnterFromSession'（从客服会话进入）
    // e.detail.expireTime: number（会话有效期截止时间戳）

    if (e.detail.eventType === 'userEnterFromSession') {
      // 用户从客服会话返回小程序，记录来源
      this.reportServiceEntry()
    }
  },
})
```

### 2.4 云函数接收客服消息

> ⚠️ 客服消息推送需要在公众平台配置消息推送地址

```javascript
// cloudfunctions/kefuMessage/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { MsgType, Content, FromUserName, CreateTime } = event

  // MsgType: text（文本）/ image（图片）/ card（小程序卡片）/ miniprogrampage（图文链接）
  console.log(`[客服消息] ${FromUserName}: ${Content}`)

  // 自动回复
  const reply = getAutoReply(Content)

  return {
    MsgType: 'text',
    Content: reply,
  }
}

// 关键词自动回复
function getAutoReply(content) {
  const rules = [
    { keyword: /退款|退货/i, reply: '您好，如需退款退货，请提供订单号，小二会尽快处理~' },
    { keyword: /运费|快递/i, reply: '我们的商品包邮哦，默认使用顺丰/中通快递~' },
    { keyword: /发票/i, reply: '请联系客服提供开票信息，我们会在 3 个工作日内开具电子发票~' },
    { keyword: /人工|客服/i, reply: '人工客服工作时间为 9:00-21:00，当前为您转接中...' },
  ]

  for (const rule of rules) {
    if (rule.keyword.test(content)) return rule.reply
  }

  return '感谢您的留言，小二稍后会回复您，请稍候~'
}
```

### 2.5 发送客服消息（主动推送）

> 在用户发起会话后的 24 小时内，可向用户推送消息

```javascript
// cloudfunctions/sendKefuMessage/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { touser, msgType, content, imageUrl } = event

  // ⚠️ 需要 AccessToken（需公众号/小程序 AppSecret）
  const accessToken = await getAccessToken()

  const payload = {
    touser: touser,
    msgtype: msgType,
    [msgType === 'text' ? 'text' : msgType === 'image' ? 'image' : 'miniprogrampage']: msgType === 'text'
      ? { content }
      : msgType === 'image'
      ? { media_id: imageUrl }
      : { ...buildMiniProgramPage(content) },
  }

  const res = await cloud.cloudAPI.message.send({
    access_token: accessToken,
    ...payload,
  })

  return res
}
```

---

## 三、订阅消息（核心推送能力）

> ⚠️ 2023 年后新小程序**只能使用订阅消息**，模板消息已废弃。

### 3.1 订阅消息类型

| 类型 | 说明 | 用户操作 |
|------|------|---------|
| 一次性订阅 | 每次触发都需用户授权 | 点击"允许" |
| 长期订阅 | 用户一次订阅，多次触发（需特定类目资质）| 勾选"总是保持以上选择" |

**支持长期订阅的类目**（部分）：教育（课程通知）、医疗（就诊提醒）、政府（民生通知）、交通（出行提醒）

### 3.2 申请订阅消息模板

微信公众平台 → 功能 → 订阅消息 → 添加模板 → 搜索关键词组合

常用模板示例：

| 场景 | 模板标题 | 关键词组合 |
|------|---------|---------|
| 订单支付成功 | 订单支付成功通知 | 订单号、商品名称、支付金额、支付时间 |
| 订单发货 | 订单发货通知 | 订单号、快递公司、快递单号 |
| 预约提醒 | 预约成功提醒 | 预约项目、预约时间、地点 |
| 会员到期 | 会员到期提醒 | 会员类型、到期时间 |
| 审核结果 | 内容审核结果通知 | 审核内容、审核结果、审核时间 |

### 3.3 小程序端请求订阅

```javascript
// utils/subscribe.js

// 订阅消息工具类
class SubscribeManager {
  constructor() {
    // 已在微信公众平台申请并获取的模板 ID
    this.templateIds = {
      orderPaid: '_TEMPLATE_ID_ORDER_PAID_',      // 订单支付成功
      orderShipped: '_TEMPLATE_ID_ORDER_SHIPPED_', // 订单发货
      refundSuccess: '_TEMPLATE_ID_REFUND_',        // 退款成功
      appointment: '_TEMPLATE_ID_APPOINTMENT_',    // 预约提醒
    }
  }

  // 请求单个订阅（一次性）
  async requestOne(templateId, shortId = null) {
    try {
      const result = await wx.requestSubscribeMessage({
        tmplIds: [templateId],
      })

      return {
        accepted: result[templateId] === 'accept',
        rejected: result[templateId] === 'reject',
        banned: result[templateId] === 'ban',   // 被后台封禁
      }
    } catch (err) {
      return { accepted: false, error: err }
    }
  }

  // 订单支付成功后请求订阅发货通知
  async requestShipNotice(orderId) {
    const { accepted } = await this.requestOne(this.templateIds.orderShipped)

    if (accepted) {
      // 保存用户订阅状态（云函数侧发送时需要筛选）
      await wx.cloud.callFunction({
        name: 'saveSubscribeStatus',
        data: {
          openid: wx.getStorageSync('openid'),
          templateId: this.templateIds.orderShipped,
          orderId,
        }
      })
      wx.showToast({ title: '已订阅发货通知', icon: 'success' })
    } else {
      // 用户拒绝后不再提示，尊重用户选择
      console.log('用户拒绝订阅发货通知')
    }
  }

  // 批量请求多个模板（每次最多 3 个）
  async requestMultiple(templateIds) {
    const limited = templateIds.slice(0, 3)
    const result = await wx.requestSubscribeMessage({ tmplIds: limited })

    const accepted = Object.entries(result)
      .filter(([, v]) => v === 'accept')
      .map(([k]) => k)

    return accepted
  }
}

export const subscribeManager = new SubscribeManager()
```

### 3.4 小程序端使用

```javascript
// pages/order/pay-success/pay-success.js
Page({
  data: {
    orderId: '',
    paid: false,
  },

  async onLoad(options) {
    const { orderId } = options
    this.setData({ orderId })

    // 支付成功 → 引导订阅发货通知（放在结果页，非侵入式）
    setTimeout(() => {
      subscribeManager.requestShipNotice(orderId)
    }, 1000)
  },
})
```

---

## 四、云函数发送订阅消息

### 4.1 发送订阅消息（云函数侧）

```javascript
// cloudfunctions/sendSubscribeMessage/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { touser, templateId, page, data } = event
  // touser: 用户 openid
  // templateId: 模板消息 ID
  // page: 点击消息后跳转的页面路径（如 "pages/order/detail?orderId=xxx"）
  // data: 模板数据，格式：{ keyword1: { value: 'xxx', color: '#ff0000' } }

  // 获取 AccessToken（小程序）
  const accessToken = await getAccessToken(process.env.WEIXIN_APP_ID, process.env.WEIXIN_APP_SECRET)

  const payload = {
    touser,
    template_id: templateId,
    page,
    data,
    miniprogram_state: 'formal',  // formal（正式版）/ trial（体验版）/ developer（开发版）
  }

  const res = await cloud.cloudAPI.request({
    url: `https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token=${accessToken}`,
    method: 'POST',
    data: payload,
  })

  if (res.errcode !== 0) {
    console.error('[订阅消息发送失败]', res)
    // errcode 40001 = access_token 过期，需重新获取
    if (res.errcode === 40001) {
      // 重新获取 access_token 后重试
    }
  }

  return { code: res.errcode === 0 ? 0 : -1, message: res.errmsg }
}

// 获取 AccessToken（建议缓存，不要每次调用都重新获取）
async function getAccessToken(appId, appSecret) {
  // 先查缓存（AccessToken 有效期 2 小时）
  const cached = await wx.cloud.database().collection('access_tokens')
    .where({ _id: appId })
    .get()

  if (cached.data.length > 0) {
    const token = cached.data[0]
    if (token.expiresAt > Date.now()) {
      return token.accessToken  // 未过期，直接用
    }
  }

  // 重新获取
  const res = await cloud.cloudAPI.request({
    url: `https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=${appId}&secret=${appSecret}`,
    method: 'GET',
  })

  if (!res.access_token) throw new Error('获取 access_token 失败')

  // 缓存到数据库（提前 5 分钟过期）
  await wx.cloud.database().collection('access_tokens').upsert({
    data: {
      _id: appId,
      accessToken: res.access_token,
      expiresAt: Date.now() + (res.expires_in - 300) * 1000,
    }
  })

  return res.access_token
}
```

### 4.2 触发发送订阅消息（业务逻辑）

```javascript
// cloudfunctions/orderNotify/index.js
// 在支付成功回调后调用此函数
exports.main = async (event, context) => {
  const { orderId, eventType } = event  // eventType: 'paid' | 'shipped' | 'refunded'

  const order = await cloud.database().collection('orders').doc(orderId).get()
  if (!order.data) return { code: -1, message: '订单不存在' }

  const openid = order.data.userOpenid

  const templateConfigs = {
    paid: {
      templateId: 'TEMPLATE_ID_PAID',
      page: `pages/order/detail?orderId=${orderId}`,
      data: {
        character_string1: { value: orderId },
        amount2: { value: `¥${order.data.totalFee}` },
        date3: { value: new Date().toLocaleString() },
      },
    },
    shipped: {
      templateId: 'TEMPLATE_ID_SHIPPED',
      page: `pages/order/detail?orderId=${orderId}`,
      data: {
        character_string1: { value: orderId },
        name4: { value: order.data.expressCompany || '顺丰速运' },
        character_string5: { value: order.data.expressNo || '' },
      },
    },
  }

  const config = templateConfigs[eventType]
  if (!config) return { code: -2, message: '未知事件类型' }

  await cloud.callFunction({
    name: 'sendSubscribeMessage',
    data: {
      touser: openid,
      ...config,
    }
  })

  return { code: 0 }
}
```

---

## 五、小程序内消息订阅 UI（引导设计）

```xml
<!-- components/subscribe-popup/index.wxml -->
<view class="popup" wx:if="{{visible}}">
  <view class="mask" bindtap="close" />
  <view class="content">
    <image class="icon" src="/assets/bell-icon.png" />
    <text class="title">{{title}}</text>
    <text class="desc">{{description}}</text>

    <view class="btn-group">
      <button
        class="primary"
        bindtap="onSubscribe"
        data-template-id="{{templateId}}"
      >
        {{primaryBtn}}
      </button>
      <text class="secondary" bindtap="close">暂不需要</text>
    </view>

    <view class="tip">点击即表示同意接收通知，通知完全免费</view>
  </view>
</view>
```

```javascript
// components/subscribe-popup/index.js
Component({
  properties: {
    templateId: String,
    title: { type: String, value: '开启通知提醒' },
    description: { type: String, value: '订单状态变更时，我们会第一时间通知您' },
    primaryBtn: { type: String, value: '立即订阅' },
  },

  data: { visible: false },

  methods: {
    show() { this.setData({ visible: true }) },
    close() { this.setData({ visible: false }) },

    async onSubscribe(e) {
      const templateId = e.currentTarget.dataset.templateId
      const { accepted } = await subscribeManager.requestOne(templateId)

      if (accepted) {
        wx.showToast({ title: '订阅成功', icon: 'success' })
      }
      this.close()
    },
  },
})
```

---

## 六、消息推送频率限制

| 消息类型 | 限制 |
|---------|------|
| 订阅消息（一次性）| 无明确总量限制，但每次发送需用户单独授权；微信有权根据生态情况调整 |
| 订阅消息（长期订阅）| 每个用户每天最多 3 条（部分类目例外）|
| 客服消息 | 48 小时内最多 5 条（每条消息间隔至少 5 分钟）|
| AccessToken | 每天最多获取 200 次（建议缓存 2 小时）|

---

## 七、Common Mistakes（客服/消息高频错误）

| 错误 | 正确做法 |
|------|---------|
| 用户拒绝订阅后反复弹窗 | 尊重用户选择，拒绝后不再提示（可下次时机再提示）|
| 模板 ID 写错 | 模板 ID 区分大小写，复制后检查 |
| 订阅消息 data 格式错误 | 格式必须是 `{ keyword1: { value: 'xxx' } }`，不能直接传字符串 |
| 发送时 AccessToken 过期 | 必须实现缓存 + 自动续期逻辑，不要每次发送都重新获取 |
| 客服消息超 24 小时发送 | 用户主动发消息后 24 小时内才能发送，需记录会话时间戳 |
| 页面路径写错导致无法跳转 | 路径必须是在 app.json 中已注册页面，且支持 query 参数 |
| 一次性订阅用长期订阅逻辑 | 一次性订阅每次都要授权，长期订阅才可多次触发 |

---

## 八、官方文档链接

- 客服消息：https://developers.weixin.qq.com/miniprogram/dev/component/custom-adapter.html
- 订阅消息：https://developers.weixin.qq.com/miniprogram/dev/api/open-api/subscribe-message/wx.requestSubscribeMessage.html
- 订阅消息发送：https://developers.weixin.qq.com/miniprogram/dev/api/open-api/subscribe-message/subscribeMessage.send.html
- 微信客服（新版）：https://work.weixin.qq.com/api/doc/part/PID-A09051-本接口何时需要验证
