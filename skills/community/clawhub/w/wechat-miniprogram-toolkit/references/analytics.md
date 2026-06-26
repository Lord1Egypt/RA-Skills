# 微信小程序数据分析与用户行为埋点全指南

## 激活契约

**符合以下任一场景时加载：**
- 小程序数据统计、数据分析、DAU/MAU、访问分析
- 用户行为埋点、事件追踪、customEvent
- 小程序数据助手、性能监控、报错监控
- 转化漏斗、留存分析、访问路径
- 用户画像、分群运营、A/B 测试

---

## 一、数据分析能力矩阵

| 能力 | 来源 | 说明 |
|------|------|------|
| 基础数据 | 小程序数据助手（官方） | DAU、访问量、留存，无需接入 |
| 自定义分析 | 数据分析模块 | 需在小程序后台开通 |
| 实时访问 | 数据实时日志 | 可看当前在线人数 |
| 自定义埋点 | `wx.reportEvent` /数据分析 SDK | 用户行为精细化追踪 |
| 性能监控 | 微信性能面板 | 启动性能、FPS、内存 |
| 错误监控 | `App.onError` / 监控 SDK | JS 错误、API 报错 |

---

## 二、无需代码的官方数据分析

在 **小程序后台 → 数据分析** 可直接查看：

### 2.1 核心指标

| 指标 | 说明 |
|------|------|
| DAU / MAU | 日活/月活用户数 |
| 累计用户数 | 历史累计去重用户 |
| 页面访问次数 | PV（Page View） |
| 访问时长 | 人均停留时长 |
| 留存率 | 次日/7日/30日留存 |
| 转化漏斗 | 页面跳转路径转化率 |
| 访问来源 | 发现入口（搜索/扫码/分享等） |

### 2.2 小程序数据助手（手机端）

```javascript
// 无需接入，在微信「小程序数据助手」小程序中直接查看
// 适合：快速了解核心数据，无需额外开发
```

---

## 三、实时在线用户数

```javascript
// pages/monitor/realtime.js
// 实时查看当前在线用户（通过心跳机制）

Page({
  data: { onlineCount: 0, history: [] },

  onShow() {
    this.startHeartbeat()
  },

  onHide() {
    this.stopHeartbeat()
  },

  // 上报心跳（页面可见时）
  startHeartbeat() {
    this._heartbeatTimer = setInterval(() => {
      this.reportOnline()
    }, 30000)  // 每 30 秒上报一次
    this.reportOnline()  // 立即上报
  },

  stopHeartbeat() {
    if (this._heartbeatTimer) {
      clearInterval(this._heartbeatTimer)
    }
    // 用户离开时上报离线
    this.reportOffline()
  },

  async reportOnline() {
    await wx.cloud.callFunction({
      name: 'reportOnline',
      data: {
        openid: wx.getStorageSync('openid'),
        page: getCurrentPages().slice(-1)[0]?.route || '',
        timestamp: Date.now(),
      }
    })
  },

  reportOffline() {
    wx.cloud.callFunction({
      name: 'reportOffline',
      data: { openid: wx.getStorageSync('openid') },
    })
  },
})
```

### 实时在线用户云函数

```javascript
// cloudfunctions/reportOnline/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })
const db = cloud.database()
const _ = db.command
const COL = 'online_users'

// 在线用户集合数据结构：
// { _id: openid, lastSeen: timestamp, page: string }

exports.main = async (event, context) => {
  const openid = event.openid

  await db.collection(COL).doc(openid).set({
    data: { lastSeen: event.timestamp, page: event.page }
  })

  // 清理 2 分钟内无心跳的用户（离线）
  const threshold = Date.now() - 2 * 60 * 1000
  await db.collection(COL)
    .where({ lastSeen: _.lt(threshold) })
    .remove()

  // 统计当前在线人数
  const { total } = await db.collection(COL).count()

  // 通过订阅消息/广播通知前端更新在线人数
  // （可结合 WebSocket 或 微信订阅消息实现推送）

  return { onlineCount: total }
}
```

---

## 四、自定义埋点（精细化行为追踪）

### 4.1 基础埋点（数据分析 SDK）

> 需要在小程序后台 → 数据分析 → 自定义分析 → 事件管理 → 创建事件

```javascript
// app.js
App({
  onLaunch() {
    // 启用数据分析（需在后台先创建事件）
    wx.AnalyticsReportName = 'my_event'  // ⚠️ 不是标准 API，实际用法如下
  }
})

// 单次事件上报
wx.reportEvent('purchase', {
  goods_id: 'G001',
  goods_name: '会员月卡',
  price: 30,
  payment_method: 'wechat',
})

wx.reportEvent('share', {
  page_name: 'index',
  share_channel: 'timeline',  // timeline / friend / 其他
})

wx.reportEvent('video_play', {
  video_id: 'V001',
  duration: 120,
  complete: false,
})
```

### 4.2 通用埋点封装（推荐）

```javascript
// utils/analytics.js

// 事件注册表（在数据分析后台配置后获得）
const EVENT_IDS = {
  PAGE_VIEW: 'page_view',
  PURCHASE: 'purchase',
  SHARE: 'share',
  VIDEO_PLAY: 'video_play',
  FORM_SUBMIT: 'form_submit',
  CLICK: 'btn_click',
}

class Analytics {
  constructor() {
    this._userInfo = wx.getStorageSync('userInfo') || {}
    this._commonParams = {}  // 通用参数（版本、渠道等）
  }

  // 设置通用参数（每个事件自动附带）
  setCommonParams(params) {
    this._commonParams = { ...this._commonParams, ...params }
  }

  // 上报事件
  track(eventName, params = {}) {
    // 合并通用参数
    const fullParams = {
      ...this._commonParams,
      ...params,
      timestamp: Date.now(),
      openid: wx.getStorageSync('openid') || 'unknown',
    }

    // 调用埋点（微信数据分析 SDK 方式）
    if (wx.reportEvent) {
      wx.reportEvent(eventName, fullParams)
    }

    // 同时上报到自己的数据分析服务（可选）
    this.trackToCloud(eventName, fullParams)
  }

  // 上报到自己的数据库（支持更多维度分析）
  async trackToCloud(eventName, params) {
    try {
      await wx.cloud.callFunction({
        name: 'trackEvent',
        data: { event: eventName, params, ts: Date.now() },
      })
    } catch (e) {
      // 埋点失败不影响主流程，静默处理
    }
  }

  // 页面浏览（自动在 onShow 时调用）
  trackPage(page, referrer = '') {
    this.track(EVENT_IDS.PAGE_VIEW, {
      page_name: page.route || page.__route__,
      referrer,
      scene: wx.getLaunchOptionsSync().scene,
    })
  }

  // 业务事件快捷方法
  trackPurchase(goodsId, amount, method) {
    this.track(EVENT_IDS.PURCHASE, {
      goods_id: goodsId,
      amount,
      payment_method: method,
    })
  }

  trackShare(page, channel) {
    this.track(EVENT_IDS.SHARE, {
      page_name: page,
      share_channel: channel,
    })
  }
}

// 全局实例
App({
  analytics: new Analytics(),

  onShow(options) {
    // 每次进入页面自动上报
    const pages = getCurrentPages()
    const currentPage = pages[pages.length - 1]
    if (currentPage && this.analytics) {
      this.analytics.trackPage(currentPage, options.referrer || '')
    }
  },
})

// 快捷调用
function track(eventName, params) {
  const app = getApp()
  app?.analytics?.track(eventName, params)
}

module.exports = { track, EVENT_IDS }
```

### 4.3 在页面中自动注入埋点

```javascript
// utils/pageTracker.js  — 自动追踪所有页面的 onShow/onHide

function wrapPage(Page) {
  const originalOnShow = Page.prototype.onShow
  const originalOnHide = Page.prototype.onHide

  Page.prototype.onShow = function (options) {
    track('page_show', { page: this.route })
    originalOnShow?.call(this, options)
  }

  Page.prototype.onHide = function () {
    track('page_hide', { page: this.route })
    originalOnHide?.call(this)
  }

  return Page
}

// 在 app.js 中使用
const originalApp = App
App = function(config) {
  if (config.onShow) {
    const orig = config.onShow
    config.onShow = function(opts) {
      track('app_show', { scene: opts?.scene })
      orig.call(this, opts)
    }
  }
  originalApp(config)
}
```

---

## 五、转化漏斗分析

```javascript
// utils/funnel.js  — 转化漏斗追踪

class FunnelTracker {
  constructor(funnelName) {
    this.funnelName = funnelName
    this.steps = []
  }

  // 定义漏斗步骤
  step(name) {
    this.steps.push({ name, ts: Date.now() })
    track('funnel_step', {
      funnel: this.funnelName,
      step: name,
      step_index: this.steps.length - 1,
    })
  }

  // 完成漏斗
  complete(conclusion) {
    this.step('complete')
    track('funnel_complete', {
      funnel: this.funnelName,
      duration: Date.now() - this.steps[0].ts,
      conclusion,
    })
  }

  // 漏斗中断
  abandon(reason) {
    track('funnel_abandon', {
      funnel: this.funnelName,
      last_step: this.steps[this.steps.length - 1]?.name,
      reason,
    })
  }
}

// 使用示例：购买转化漏斗
Page({
  onLoad() {
    this._funnel = new FunnelTracker('purchase')

    this._funnel.step('product_view')   // 浏览商品
  },

  onAddToCart() {
    this._funnel.step('add_to_cart')    // 加入购物车
  },

  onCheckout() {
    this._funnel.step('checkout')       // 进入结算
  },

  onPaySuccess() {
    this._funnel.complete('success')    // 支付成功
  },

  onPayFail() {
    this._funnel.abandon('pay_fail')     // 支付失败放弃
  },
})
```

---

## 六、性能监控（启动性能 & FPS）

### 6.1 启动性能监控

```javascript
// app.js — 监控启动时间
App({
  onLaunch(options) {
    // 记录启动时间
    const launchTime = Date.now() - (wx.getEnterOptionsSync?.()?.timestamp || Date.now())

    // 上报启动性能
    this.reportLaunchPerf(launchTime, options)
  },

  reportLaunchPerf(launchTime, options) {
    wx.reportPerformance?.(
      1001,  // 启动耗时（ms）
      launchTime
    )

    // 同时上报到自己的监控服务
    wx.cloud.callFunction({
      name: 'reportPerf',
      data: {
        type: 'launch',
        value: launchTime,
        scene: options?.scene,
        version: wx.getAccountInfoSync().miniProgram.version,
      }
    })
  },
})
```

### 6.2 FPS 帧率监控

```javascript
// utils/fpsMonitor.js  — 监测页面卡顿
let lastTime = Date.now()
let fps = 60
let frameCount = 0

function startFPSMonitor() {
  const observer = wx.createRewardedVideoAd && wx.createAnimation ? {
    // 使用 WXS 监测
  } : null

  // 简化版：每 500ms 检查一次帧数
  const checkFPS = () => {
    const now = Date.now()
    const elapsed = now - lastTime
    fps = Math.round(frameCount / (elapsed / 1000))
    frameCount = 0
    lastTime = now

    if (fps < 30) {
      // 帧率过低，上报警告
      track('perf_fps_low', { fps, page: getCurrentPages().slice(-1)[0]?.route })
    }

    setTimeout(checkFPS, 500)
  }
  checkFPS()
}

// 在 Page 的 onShow 中启动
function onPageShow() {
  frameCount++
  requestAnimationFrame(onPageShow)
}
```

---

## 七、错误监控

### 7.1 JS 错误监控

```javascript
// app.js — 全局错误处理
App({
  onLaunch() {
    // 监听未处理的 Promise 拒绝
    wx.onUnhandledRejection?.((result) => {
      this.reportError('unhandled_rejection', result.reason)
    })
  },

  onError(errMsg) {
    this.reportError('js_error', errMsg)
  },

  reportError(type, msg) {
    wx.cloud.callFunction({
      name: 'reportError',
      data: {
        type,
        message: typeof msg === 'string' ? msg : JSON.stringify(msg),
        openid: wx.getStorageSync('openid'),
        version: wx.getAccountInfoSync().miniProgram.version,
        timestamp: Date.now(),
        scene: wx.getLaunchOptionsSync().scene,
      }
    })
  },
})
```

### 7.2 错误记录云函数

```javascript
// cloudfunctions/reportError/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { type, message, openid, version, timestamp, scene } = event

  await cloud.database().collection('error_logs').add({
    data: {
      type,
      message,
      openid,
      version,
      scene,
      timestamp: new Date(timestamp),
      status: 'new',  // new / read / resolved
    }
  })

  // 错误数量告警（超过阈值发通知）
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const todayErrors = await cloud.database().collection('error_logs')
    .where({
      timestamp: cloud.database().command.gte(today),
      type: 'js_error',
    })
    .count()

  if (todayErrors.total > 100) {
    // 触发告警（订阅消息/企业微信机器人通知）
    await cloud.callFunction({
      name: 'sendAlert',
      data: { message: `JS 错误告警：今日已发生 ${todayErrors.total} 次` }
    })
  }

  return { code: 0 }
}
```

---

## 八、用户分群与标签

```javascript
// cloudfunctions/userProfile/index.js
// 基于行为数据给用户打标签

const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { openid } = event
  const db = cloud.database()

  // 查询该用户最近30天的行为
  const thirtyDaysAgo = Date.now() - 30 * 24 * 60 * 60 * 1000

  // 聚合查询该用户的各类型行为数量
  const res = await db.collection('events')
    .aggregate()
    .match({ openid, ts: _.command.gte(thirtyDaysAgo) })
    .group({ _id: '$event', count: $.sum(1) })
    .end()

  // 计算标签
  const eventCounts = {}
  res.list.forEach(item => { eventCounts[item._id] = item.count })

  const tags = []
  if (eventCounts['purchase'] >= 5) tags.push('high_value')
  if (eventCounts['share'] >= 3) tags.push('active_sharer')
  if (eventCounts['video_play'] >= 10) tags.push('video_lover')
  if (Object.values(eventCounts).reduce((a, b) => a + b, 0) === 0) tags.push('dormant')

  // 更新用户标签
  await db.collection('users').where({ _openid: openid }).update({
    data: { tags, lastActive: db.serverDate() }
  })

  return { tags }
}
```

---

## 九、Common Mistakes（数据分析高频错误）

| 错误 | 正确做法 |
|------|---------|
| 在 onLoad 中埋 PV | 应在 onShow 中埋（页面每次展示都算一次访问）|
| 埋点失败不处理 | 埋点应静默失败，不影响主业务流程 |
| 埋点数据存本地 | 及时上报到服务端，防止卸载丢失数据 |
| 所有事件用同一个事件名 | 按数据类型分层命名：`purchase`、`video_play`、`share` |
| 敏感信息进埋点 | 用户名/手机号/密码等严禁作为埋点参数 |
| 不监控 FPS | 小程序帧率低于 30fps 严重影响体验，需告警 |
| 启动耗时不管 | 启动超 3s 用户流失率显著上升，必须优化 |

---

## 十、官方文档链接

- 数据分析后台：https://developers.weixin.qq.com/miniprogram/analysis/
- 自定义分析：https://developers.weixin.qq.com/miniprogram/analysis/custom/
- 事件管理：https://developers.weixin.qq.com/miniprogram/analysis/自定义分析/事件配置/
- 数据实时日志：https://developers.weixin.qq.com/miniprogram/analysis/实时日志/
- 性能监控：https://developers.weixin.qq.com/miniprogram/dev/performance/
