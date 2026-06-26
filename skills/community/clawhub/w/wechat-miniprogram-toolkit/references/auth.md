# 微信小程序登录鉴权指南

> 本文档整合腾讯云官方认证最佳实践，权威覆盖 openid / unionid 身份机制。

---

## 激活契约

### ✅ 首次激活时

**符合以下任一场景，立即加载本 skill：**
- 需要在小程序中识别用户身份
- 涉及 openid、unionid、wx.cloud 身份注入
- 用户登录、注册、权限校验
- 云函数内需要知道"谁在调用"

**触发路由：**
```
openid / unionid 不清楚？       → 本文档 Scenario 2
wx.cloud.init 不生效？          → Scenario 1
想用手机号登录？               → Scenario 5
云函数拿不到用户身份？          → Scenario 2 + 3
做了 Web 风格的登录页？         → ❌ 立即停止，看 Scenario 0
```

### ❌ 不要这样做

| ❌ 不要这样做 | ✅ 正确做法 |
|---|---|
| 在小程序里做 Web 风格登录页 + OAuth 跳转 | 小程序身份由微信原生处理，无需自定义 OAuth |
| 把 openid 从云函数返回给前端再传回来 | openid 在云函数内通过 `cloud.getWXContext()` 自动注入，无需前端传输 |
| 在小程序端调用 `wx.login()` 获取 code 再自己换 openid | 用云函数自动获取，云开发已封装好身份链路 |
| 把 openid / unionid 当作普通 user_id 暴露 | openid 是私密标识，避免直接暴露在前端代码/日志中 |
| unionid 拿不到就放弃 | 检查是否绑定了微信开放平台，同一主体下 unionid 才一致 |

---

## 核心概念（权威）

### 小程序身份体系

微信小程序的身份体系有三个层级：

```
OPENID     ─ 用户的唯一标识（当前小程序内唯一）
APPID      ─ 小程序本身的 ID
UNIONID    ─ 同一微信开放平台下多个应用共享的身份（需绑定）
```

| 标识 | 获取位置 | 条件 | 用途 |
|------|----------|------|------|
| `OPENID` | 云函数 `cloud.getWXContext().OPENID` | 始终可用 | 用户身份核心标识，存数据库 |
| `APPID` | 云函数 `cloud.getWXContext().APPID` | 始终可用 | 识别小程序来源 |
| `UNIONID` | 云函数 `cloud.getWXContext().UNIONID` | 必须绑定微信开放平台 | 跨应用识别同一用户 |

**安全原则（腾讯云官方）：**
> `openid`、`appid`、`unionid` 由微信自动验证和注入，**完全可信**，无需二次验证。
> 不要在代码里校验这些值的格式，直接使用。

### 小程序认证的三个核心原则

1. **原生自动**：用户无需显式登录，微信已完成认证
2. **无感传递**：身份信息在 wx.cloud 调用链中自动传递，云函数无需前端传参
3. **服务端可信**：openid 等身份信息只在云函数中获取，避免前端伪造

---

## Scenario 0：不要这样做——Web 风格登录 ❌

**典型错误：**
```javascript
// ❌ 不要这样做：在小程序里做了类似 Web OAuth 的流程
wx.redirectTo({ url: '/pages/login/login' }) // 显示登录页
wx.login({ success: res => {
  // 自己调用微信接口换 session
  fetch('/api/login', { code: res.code })
}})
```

**为什么错：**
- 小程序不是 Web，无法在客户端做 OAuth 重定向
- 微信已内置身份系统，重复实现反而破坏安全性
- 正确方式是：微信自动注入身份 → 云函数接收 → 直接使用

**正确认知：**
> 小程序的身份获取是**微信自动完成的**，开发者只需要在云函数里调用 `getWXContext()` 即可，无需任何登录页面。

---

## Scenario 1：初始化云开发（必须）

```javascript
// app.js — 全局初始化，整个小程序只调用一次
App({
  onLaunch() {
    if (!wx.cloud) {
      console.error('请使用 2.9.0 以上的基础库以使用云能力')
      return
    }

    wx.cloud.init({
      env: 'your-env-id',               // ⚠️ 填入实际环境 ID，或 wx.cloud.DYNAMIC_CURRENT_ENV（SDK ≥ 2.x）
      traceUser: true,                   // 在控制台追踪用户访问
    })
  }
})
```

> ⚠️ **权威写法**：云函数内用 `cloud.DYNAMIC_CURRENT_ENV`，**不要硬编码** env ID。
> 这样在开发/测试/生产环境切换时无需修改代码。

---

## Scenario 2：云函数中获取用户身份（核心）

```javascript
// cloudfunctions/getUserInfo/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })  // ✅ 动态环境

exports.main = async (event, context) => {
  // 身份信息由微信自动注入，完全可信，无需验证
  const { OPENID, APPID, UNIONID } = cloud.getWXContext()

  console.log('用户身份:', { OPENID, APPID, UNIONID })

  // 业务逻辑：查询/写入用户数据
  const db = cloud.database()
  const { total } = await db.collection('users').where({ _openid: OPENID }).count()

  if (total === 0) {
    await db.collection('users').add({
      data: {
        _openid: OPENID,                        // 核心：用 openid 关联用户数据
        unionid: UNIONID,                        // 可能为 undefined
        appid: APPID,
        createdAt: db.serverDate(),
        status: 'active',
      }
    })
  }

  return {
    code: 0,
    openid: OPENID,
    hasUnionid: !!UNIONID,
  }
}
```

**关键点：**
- `OPENID` 始终可用，唯一标识当前小程序内的用户
- `UNIONID` 只有绑定了微信开放平台才可用
- openid **不在前端传输**，直接从云函数获取，安全性最高

---

## Scenario 3：小程序端调用云函数获取身份

```javascript
// pages/profile/profile.js
Page({
  data: { userInfo: null },

  onLoad() {
    this.loadUserInfo()
  },

  async loadUserInfo() {
    try {
      const res = await wx.cloud.callFunction({
        name: 'getUserInfo',
        data: {},
      })
      if (res.result.code === 0) {
        this.setData({ userInfo: res.result })
      }
    } catch (e) {
      console.error('获取用户信息失败', e)
    }
  },
})
```

---

## Scenario 4：静默登录（用户无感知）

在 `app.js` 的 `onLaunch` 中执行，用户全程无感知：

```javascript
// app.js
App({
  globalData: {
    openid: '',
    isLogin: false,
  },

  onLaunch() {
    this.initCloud()
    this.autoLogin()
  },

  initCloud() {
    wx.cloud.init({ env: 'your-env-id', traceUser: true })  // ⚠️ 填入实际环境 ID
  },

  autoLogin() {
    const openid = wx.getStorageSync('openid')

    if (openid) {
      // 已登录 → 检查 session 是否有效
      wx.checkSession({
        success: () => {
          this.globalData.openid = openid
          this.globalData.isLogin = true
        },
        fail: () => {
          // session 过期，重新静默登录
          this.doSilentLogin()
        },
      })
    } else {
      // 无 openid，首次静默登录
      this.doSilentLogin()
    }
  },

  async doSilentLogin() {
    try {
      const res = await wx.cloud.callFunction({ name: 'silentLogin', data: {} })
      if (res.result.openid) {
        wx.setStorageSync('openid', res.result.openid)
        this.globalData.openid = res.result.openid
        this.globalData.isLogin = true
      }
    } catch (e) {
      console.error('静默登录失败', e)
    }
  },
})
```

**云函数 silentLogin.js：**
```javascript
// cloudfunctions/silentLogin/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const openid = cloud.getWXContext().OPENID
  return { openid }
}
```

---

## Scenario 5：用户主动授权登录（现代方案 2024+）

> ⚠️ `open-type="getUserInfo"` + `bindgetuserinfo` 已在 2021 年后逐步废弃，微信已不再支持通过按钮直接获取用户昵称头像。
> 现代方案使用：`chooseAvatar`（头像）+ 用户手动输入昵称（或直接用手机号登录，见 Scenario 6）。

### 小程序端

```xml
<!-- pages/login/login.wxml -->
<view class="login-container">
  <!-- 微信头像选择按钮（提供悬浮头像选择器） -->
  <button class="avatar-btn" open-type="chooseAvatar" bindchooseavatar="handleChooseAvatar">
    <image
      class="avatar"
      src="{{avatarUrl || '/assets/default-avatar.png'}}"
      mode="aspectFill"
    />
    <text class="avatar-tip">点击更换头像</text>
  </button>

  <!-- 昵称输入（type="nickname" 唤起微信昵称键盘） -->
  <input
    type="nickname"
    class="nickname-input"
    placeholder="点击设置微信昵称"
    value="{{nickName}}"
    bindinput="handleNicknameInput"
  />

  <!-- 确认登录 -->
  <button type="primary" bindtap="handleLogin" loading="{{loading}}">
    确认登录
  </button>
</view>
```

```javascript
// pages/login/login.js
Page({
  data: { avatarUrl: '', nickName: '', loading: false },

  // 获取微信头像
  handleChooseAvatar(e) {
    const { avatarUrl } = e.detail  // 本地临时路径，需上传到云存储
    this.setData({ avatarUrl })
  },

  // 捕获昵称输入
  handleNicknameInput(e) {
    this.setData({ nickName: e.detail.value })
  },

  async handleLogin() {
    const { avatarUrl, nickName } = this.data
    if (!nickName.trim()) {
      wx.showToast({ title: '请输入昵称', icon: 'none' }); return
    }

    this.setData({ loading: true })
    try {
      // 1. 上传头像到云存储（如有）
      let cloudAvatarUrl = ''
      if (avatarUrl && !avatarUrl.includes('/assets/')) {
        const up = await wx.cloud.uploadFile({
          cloudPath: `avatars/${Date.now()}.jpg`,
          filePath: avatarUrl,
        })
        cloudAvatarUrl = up.fileID
      }

      // 2. 调用云函数完成注册/登录
      const res = await wx.cloud.callFunction({
        name: 'login',
        data: { userInfo: { nickName: nickName.trim(), avatarUrl: cloudAvatarUrl } },
      })

      const { result } = res
      if (result.code === 0) {
        wx.setStorageSync('nickName', nickName.trim())
        wx.setStorageSync('avatarUrl', cloudAvatarUrl)
        wx.setStorageSync('openid', result.openid)
        wx.setStorageSync('isLogin', true)
        wx.showToast({
          title: result.action === 'register' ? '注册成功' : '欢迎回来',
          icon: 'success',
        })
        setTimeout(() => wx.switchTab({ url: '/pages/index/index' }), 1500)
      }
    } catch (err) {
      wx.showToast({ title: '登录失败', icon: 'none' })
    } finally {
      this.setData({ loading: false })
    }
  },
})
```

### 云函数 login.js

```javascript
// cloudfunctions/login/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

const db = cloud.database()

exports.main = async (event, context) => {
  const { userInfo } = event
  const openid = cloud.getWXContext().OPENID

  if (!openid) return { code: -1, msg: '无法获取用户身份' }

  const { total } = await db.collection('users').where({ _openid: openid }).count()

  if (total === 0) {
    // 新用户 → 注册
    await db.collection('users').add({
      data: {
        _openid: openid,
        name: userInfo?.nickName || '微信用户',
        avatar: userInfo?.avatarUrl || '',
        gender: userInfo?.gender || 0,
        country: userInfo?.country || '',
        province: userInfo?.province || '',
        city: userInfo?.city || '',
        language: userInfo?.language || 'zh_CN',
        createdAt: db.serverDate(),
        lastLoginAt: db.serverDate(),
        status: 'active',
        role: 'user',
      }
    })
    return { code: 0, action: 'register', openid }
  } else {
    // 老用户 → 更新最后登录时间
    await db.collection('users')
      .where({ _openid: openid })
      .update({ data: { lastLoginAt: db.serverDate() } })
    return { code: 0, action: 'login', openid }
  }
}
```

---

## Scenario 6：手机号快速登录

### 小程序端

```xml
<button open-type="getPhoneNumber" bindgetphonenumber="getPhoneNumber">
  微信手机号登录
</button>
```

```javascript
// pages/login/login.js
async getPhoneNumber(e) {
  const { errMsg, code } = e.detail

  if (errMsg !== 'getPhoneNumber:ok') {
    wx.showToast({ title: '未授权手机号', icon: 'none' })
    return
  }

  wx.showLoading({ title: '登录中...' })

  try {
    const res = await wx.cloud.callFunction({
      name: 'getPhone',
      data: { code },
    })

    const phone = res.result.phoneInfo?.phoneNumber
    if (phone) {
      wx.showToast({ title: `手机号: ${phone}`, icon: 'none' })
    }
  } catch (e) {
    wx.showToast({ title: '登录失败', icon: 'none' })
  } finally {
    wx.hideLoading()
  }
}
```

### 云函数 getPhone.js

```javascript
// cloudfunctions/getPhone/index.js
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

exports.main = async (event, context) => {
  const { code } = event
  const openid = cloud.getWXContext().OPENID

  if (!code) return { code: -1, msg: '缺少 code 参数' }

  try {
    // 获取手机号的推荐方式（优先使用 HTTP API 调用，不依赖特定 SDK 版本）：
    // 微信官方文档：https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-info/phone-number/getPhoneNumber.html
    //
    // 方式 A：wx-server-sdk（需确认当前 SDK 版本支持）
    // const phoneInfo = await cloud.cloudAPI.openMobile.getPhoneNumber({ code })
    //
    // 方式 B（更稳定，推荐）：直接调用微信 HTTP API
    const phoneInfo = await cloud.cloudAPI.util.request({
      url: `https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token=`,
      method: 'POST',
      data: { code },
    })

    // ⚠️ access_token 需从微信接口获取（建议配合云函数定时刷新 token 并存入云存储/数据库）
    // ⚠️ 此处仅为示意，生产环境请配合 token 管理机制

    // 关联到用户
    const db = cloud.database()
    await db.collection('users').where({ _openid: openid }).update({
      data: {
        phone: phoneInfo.phoneNumber,
        updatedAt: db.serverDate(),
      }
    })

    return { code: 0, phoneInfo }
  } catch (e) {
    return { code: -2, msg: e.message }
  }
}
```

---

## Scenario 7：权限守卫（页面级）

```javascript
// utils/auth.js
function requireAuth(callback, options = {}) {
  const { showModal = true, redirectTo = '/pages/login/login' } = options
  const app = getApp()

  if (app.globalData.isLogin) {
    typeof callback === 'function' && callback()
    return true
  }

  if (showModal) {
    wx.showModal({
      title: '提示',
      content: '请先登录后操作',
      confirmText: '去登录',
      success(res) {
        if (res.confirm) {
          wx.navigateTo({ url: redirectTo })
        }
      }
    })
  }
  return false
}

// 使用示例
Page({
  onLoad() {
    requireAuth(() => {
      this.loadMyData()
    })
  }
})
```

---

## 数据库安全规则配置

在云开发控制台 → 数据库 → 权限设置，为 users 集合配置：

```json
{
  "read": "doc._openid == auth.openid",
  "write": "doc._openid == auth.openid"
}
```

| 规则 | 效果 |
|------|------|
| `doc._openid == auth.openid` | 只有创建者可读写自己的数据 |
| `"openid"` | 所有登录用户可读，仅创建者可写 |
| `true` | 所有用户可读可写（慎用） |
| `false` | 仅管理员可写（需云函数权限） |

> 生产环境推荐：`read: doc._openid == auth.openid`，确保用户只能读写自己的数据。

---

## 常见问题 FAQ

### Q: 云函数获取不到 openid？
A: 确保在小程序端通过 `wx.cloud.init()` 初始化后调用，云函数内通过 `cloud.getWXContext().OPENID` 获取。

### Q: 提示 "getUserProfile:fail must be called by user tap gesture"？
A: 微信已废弃 `wx.getUserInfo` 和 `wx.getUserProfile`。现代方案：头像用 `button open-type="chooseAvatar"`，昵称用 `input type="nickname"` 或直接用手机号登录（Scenario 6）。

### Q: unionid 为 undefined？
A: 需要同时满足：① 小程序绑定微信开放平台账号；② 用户已授权。两者缺一不可。

### Q: 静默登录和手动登录用哪个？
A: **静默登录**：无需用户操作，适合大多数场景；**手动登录**：需要获取用户信息（昵称头像）时使用按钮触发。

### Q: 用户拒绝授权 userInfo？
A: 引导用户开启：`wx.openSetting()` → 用户手动开启授权后重试。
