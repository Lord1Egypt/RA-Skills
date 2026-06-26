# 微信小程序项目初始化模板

## 目录结构

```
project/
├── project.config.json          # 项目配置（含云函数目录）
├── sitemap.json                  # 微信索引配置
├── cloudfunctions/               # 云函数目录
│   ├── login/                   # 登录云函数
│   │   ├── index.js
│   │   ├── package.json
│   │   └── node_modules/
│   ├── getUserInfo/
│   │   ├── index.js
│   │   └── package.json
│   └── aggregateData/
│       ├── index.js
│       └── package.json
├── miniprogram/                  # 小程序主目录（可改名）
│   ├── app.js
│   ├── app.json
│   ├── app.wxml
│   ├── app.wxss
│   ├── components/              # 公共组件
│   │   ├── my-header/
│   │   ├── my-table/
│   │   └── my-form/
│   ├── pages/                   # 主包页面
│   │   ├── index/
│   │   └── logs/
│   ├── subpackages/             # 分包目录（初始为空）
│   │   ├── pkg-a/
│   │   └── pkg-b/
│   ├── static/                  # 公共静态资源
│   │   ├── images/
│   │   └── fonts/
│   └── utils/
│       ├── auth.js              # 权限守卫
│       ├── cloud.js             # 云能力封装
│       ├── eventBus.js          # 跨分包通信
│       └── mathSymbol.js        # 数学公式工具
└── cloudbaserc.json             # 云开发环境配置（腾讯云）
```

---

## 1. project.config.json

```json
{
  "description": "项目配置文件",
  "packOptions": {
    "ignore": [
      { "type": "file", "value": "miniprogram_dist" },
      { "type": "file", "value": "node_modules" }
    ]
  },
  "setting": {
    "urlCheck": false,
    "es6": true,
    "enhance": true,
    "postcss": true,
    "minified": true,
    "newFeature": true,
    "coverView": true,
    "nodeModules": false,
    "autoAudits": false,
    "minifyWXSS": true,
    "minifyWXML": true,
    "babelSetting": {
      "ignore": [],
      "disablePlugins": [],
      "outputPath": ""
    }
  },
  "compileType": "miniprogram",
  "libVersion": "3.4.6",
  "appid": "your-appid",
  "projectname": "your-project-name",
  "condition": {},
  "cloudfunctionTemplateRoot": "cloudfunctions/template",
  "cloudbase": {
    "env": "env-xxx",
    "servicePrefix": "",
    "containerRegions": ["ap-shanghai"],
    "showLog": true
  }
}
```

---

## 2. app.json（全局配置）

```json
{
  "pages": [
    "pages/index/index",
    "pages/logs/logs"
  ],
  "subpackages": [],
  "window": {
    "backgroundTextStyle": "light",
    "navigationBarBackgroundColor": "#ffffff",
    "navigationBarTitleText": "小程序名称",
    "navigationBarTextStyle": "black"
  },
  "tabBar": {
    "color": "#7A7E83",
    "selectedColor": "#3cc51f",
    "borderStyle": "black",
    "backgroundColor": "#ffffff",
    "list": [
      { "pagePath": "pages/index/index", "text": "首页", "iconPath": "static/images/tab-home.png", "selectedIconPath": "static/images/tab-home-active.png" },
      { "pagePath": "pages/logs/logs", "text": "日志", "iconPath": "static/images/tab-logs.png", "selectedIconPath": "static/images/tab-logs-active.png" }
    ]
  },
  "style": "v2",
  "sitemapLocation": "sitemap.json",
  "lazyCodeLoading": "requiredComponents",
  "usingComponents": {
    "my-header": "/components/my-header/index",
    "my-table": "/components/my-table/index"
  }
}
```

---

## 3. app.js（应用入口）

```javascript
App({
  globalData: {
    userInfo: null,
    openid: '',
    envId: 'env-xxx',     // 云开发环境 ID
    isLogin: false,
  },

  onLaunch() {
    // 初始化云开发
    this.initCloud()

    // 静默登录检查
    this.autoLogin()
  },

  initCloud() {
    if (!wx.cloud) {
      console.warn('请使用微信开发者工具 2.2.3+ 版本')
      return
    }
    wx.cloud.init({
      env: this.globalData.envId,
      traceUser: true,
      timeout: 10000,
    })
  },

  async autoLogin() {
    const openid = wx.getStorageSync('openid')
    if (openid) {
      wx.checkSession({
        success: () => {
          this.globalData.isLogin = true
          this.globalData.openid = openid
        },
        fail: () => {
          this.doSilentLogin()
        }
      })
    } else {
      this.doSilentLogin()
    }
  },

  async doSilentLogin() {
    try {
      const res = await wx.cloud.callFunction({
        name: 'login',
        data: {},
      })
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

---

## 4. 工具函数模板

### 4.1 云能力封装 utils/cloud.js

```javascript
const cloud = wx.cloud

class CloudService {
  constructor(envId) {
    this.db = wx.cloud.database({ env: envId || 'env-xxx' })
    this.envId = envId
  }

  async call(name, data = {}) {
    try {
      const res = await wx.cloud.callFunction({
        name,
        data,
      })
      if (res.errMsg && res.errMsg.includes('ok')) {
        return res.result
      }
      throw new Error(res.result?.msg || '云函数调用失败')
    } catch (e) {
      console.error(`cloud.call ${name} error:`, e)
      throw e
    }
  }

  async upload(filePath, dir = 'uploads') {
    const ext = filePath.match(/\.(\w+)$/)?.[1] || 'jpg'
    const cloudPath = `${dir}/${Date.now()}.${ext}`
    const res = await cloud.uploadFile({ cloudPath, filePath })
    return res.fileID
  }

  async getTempURL(fileID) {
    const res = await cloud.getTempFileURL({ fileList: [fileID] })
    return res.fileList[0]?.tempFileURL || ''
  }

  // 数据库操作快捷方法
  collection(name) { return this.db.collection(name) }
}

module.exports = CloudService
```

### 4.2 权限守卫 utils/auth.js

```javascript
const app = getApp()

function requireAuth(callback, options = {}) {
  const { showModal = true, redirectTo = '/pages/login/login' } = options

  if (app.globalData.isLogin) {
    return typeof callback === 'function' && callback()
  }

  if (showModal) {
    wx.showModal({
      title: '提示',
      content: '请先登录后再操作',
      success(res) {
        if (res.confirm) {
          wx.navigateTo({ url: redirectTo })
        }
      }
    })
  }
  return false
}

function requireAuthAsync() {
  return new Promise((resolve) => {
    requireAuth(() => resolve(true), { showModal: false })
    wx.showModal({
      title: '提示',
      content: '请先登录',
      success(res) {
        if (res.confirm) {
          wx.navigateTo({ url: '/pages/login/login' })
          const observer = wx.createIntersectionObserver()
          observer.relativeToViewport().observe('#app', () => {
            resolve(false)
          })
        } else {
          resolve(false)
        }
      }
    })
  })
}

module.exports = { requireAuth, requireAuthAsync }
```

### 4.3 事件总线 utils/eventBus.js

```javascript
const events = {}

function emit(name, data) {
  const handlers = events[name] || []
  handlers.forEach(fn => {
    try { fn(data) } catch (e) { console.error(e) }
  })
}

function on(name, fn) {
  if (!events[name]) events[name] = []
  events[name].push(fn)
}

function off(name, fn) {
  if (!events[name]) return
  events[name] = events[name].filter(h => h !== fn)
}

function once(name, fn) {
  const wrapper = (data) => {
    fn(data)
    off(name, wrapper)
  }
  on(name, wrapper)
}

module.exports = { emit, on, off, once }
```

### 4.4 数学公式 utils/mathSymbol.js

```javascript
const GREEK_MAP = {
  alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ',
  epsilon: 'ε', zeta: 'ζ', eta: 'η', theta: 'θ',
  iota: 'ι', kappa: 'κ', lambda: 'λ', mu: 'μ',
  nu: 'ν', xi: 'ξ', omicron: 'ο', pi: 'π',
  rho: 'ρ', sigma: 'σ', tau: 'τ', upsilon: 'υ',
  phi: 'φ', chi: 'χ', psi: 'ψ', omega: 'ω',
  Gamma: 'Γ', Delta: 'Δ', Theta: 'Θ', Lambda: 'Λ',
  Xi: 'Ξ', Pi: 'Π', Sigma: 'Σ', Phi: 'Φ',
  Psi: 'Ψ', Omega: 'Ω',
}

const SYMBOL_MAP = {
  '\\sum': '∑', '\\int': '∫', '\\infty': '∞',
  '\\sqrt': '√', '\\partial': '∂', '\\nabla': '∇',
  '\\pm': '±', '\\times': '×', '\\div': '÷',
  '\\cdot': '·', '\\leq': '≤', '\\geq': '≥',
  '\\neq': '≠', '\\approx': '≈', '\\equiv': '≡',
  '\\in': '∈', '\\notin': '∉', '\\subset': '⊂',
  '\\subseteq': '⊆', '\\cup': '∪', '\\cap': '∩',
  '\\forall': '∀', '\\exists': '∃', '\\neg': '¬',
  '\\land': '∧', '\\lor': '∨', '\\to': '→',
  '\\gets': '←', '\\iff': '⟺', '\\Rightarrow': '⇒',
  '\\Leftarrow': '⇐', '\\rightarrow': '→',
  '\\alpha': 'α', '\\beta': 'β',
}

function latexToUnicode(latex) {
  let result = latex

  // 先处理希腊字母
  for (const [k, v] of Object.entries(GREEK_MAP)) {
    result = result.replace(new RegExp(k.replace(/[A-Z]/g, c => `[${c}${c.toLowerCase()}]`)), v)
  }
  // 通用符号
  for (const [k, v] of Object.entries(SYMBOL_MAP)) {
    result = result.replace(new RegExp(k.replace(/\\/g, '\\\\'), 'g'), v)
  }
  // 上下标
  result = result.replace(/\^{([^}]+)}/g, (m, g) => {
    const sup = { '0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','n':'ⁿ','+':'⁺','-':'⁻','=':'⁼','(':'⁽',')':'⁾' }
    return [...g].map(c => sup[c] || c).join('')
  })
  result = result.replace(/_{([^}]+)}/g, (m, g) => {
    const sub = { '0':'₀','1':'₁','2':'₂','3':'₃','4':'₄','5':'₅','6':'₆','7':'₇','8':'₈','9':'₉','n':'ₙ','+':'₊','-':'₋','=':'₌','(':'₍',')':'₎' }
    return [...g].map(c => sub[c] || c).join('')
  })
  // 分数
  result = result.replace(/\\frac{([^}]+)}{([^}]+)}/g, '($1)⁄($2)')
  // 移除多余空格
  result = result.replace(/\s+/g, ' ')
  return result.trim()
}

module.exports = { GREEK_MAP, latexToUnicode }
```

---

## 5. 云函数模板

### 5.1 login 云函数

**package.json:**
```json
{ "name": "login", "dependencies": { "wx-server-sdk": "latest" } }
```

**index.js:**
```javascript
const cloud = require('wx-server-sdk')
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

const db = cloud.database()

exports.main = async (event, context) => {
  const { userInfo } = event
  const openid = cloud.getWXContext().OPENID

  if (!openid) return { code: -1, msg: '无法获取 openid' }

  const { total } = await db.collection('users').where({ _openid: openid }).count()

  if (total === 0) {
    await db.collection('users').add({
      data: {
        _openid: openid,
        name: userInfo?.nickName || '微信用户',
        avatar: userInfo?.avatarUrl || '',
        createdAt: db.serverDate(),
        lastLoginAt: db.serverDate(),
        status: 'active',
      }
    })
    return { code: 0, action: 'register', openid }
  }

  await db.collection('users').where({ _openid: openid }).update({
    data: { lastLoginAt: db.serverDate() }
  })
  return { code: 0, action: 'login', openid }
}
```

### 5.2 aggregateData 云函数（聚合查询）

```javascript
// cloudfunctions/aggregateData/index.js
exports.main = async (event, context) => {
  const { page = 1, pageSize = 10 } = event
  const openid = cloud.getWXContext().OPENID

  const countRes = await db.collection('posts').where({ _openid: openid }).count()
  const listRes = await db.collection('posts')
    .aggregate()
    .match({ _openid: openid })
    .sort({ createdAt: -1 })
    .skip((page - 1) * pageSize)
    .limit(pageSize)
    .end()

  return { total: countRes.total, list: listRes.list }
}
```

---

## 6. 分包结构示例

```
subpackages/
├── pkg-a/                       # 分包 A
│   ├── package.json             # 可选
│   ├── app.js                   # 可选（分包独立配置）
│   └── pages/
│       ├── detail/
│       │   ├── index.js
│       │   ├── index.wxml
│       │   ├── index.json
│       │   └── index.wxss
│       └── settings/
│           └── index.js / index.wxml / ...
└── pkg-b/                       # 分包 B
    ├── package.json
    └── pages/
        └── profile/
            └── index.*
```

---

## 7. 分包页面跳转

```javascript
// 同分包内跳转
wx.navigateTo({ url: './settings/index' })

// 跨分包跳转
wx.navigateTo({ url: '/subpackages/pkg-b/pages/profile/index' })

// 分包内 reLaunch
wx.reLaunch({ url: '/subpackages/pkg-a/pages/detail/index?id=1' })
```
