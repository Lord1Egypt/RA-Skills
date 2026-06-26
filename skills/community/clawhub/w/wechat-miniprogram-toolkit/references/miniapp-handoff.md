# 微信小程序互跳全指南

## 激活契约

**符合以下任一场景时加载：**
- 小程序跳转 APP、navigateToApp
- APP 跳转小程序、launchMiniProgram
- URL Scheme 跳转、deep link、deeplink
- Universal Link（iOS）、App Link（Android）
- 小程序互跳、另一个小程序
- H5 跳转小程序、扫一扫打开小程序
- 微信开放标签、wx-open-launch-app

---

## 一、互跳全场景矩阵

| 跳转路径 | 技术方案 | 需要用户操作 |
|---------|---------|------------|
| 小程序 → 另一个小程序 | `wx.navigateToMiniProgram` | 用户点按钮触发（禁止自动跳转）|
| 小程序 → APP | `wx.navigateToApp` | 同上，需 APP 已安装 |
| APP → 小程序 | 调起微信 SDK | APP 内调用 SDK |
| H5（微信内）→ 小程序 | 开放标签 `wx-open-launch-app` | 点击开放标签 |
| H5（非微信）→ 小程序 | URL Scheme / 短链 | 扫码或点击链接 |
| 小程序 → H5 | web-view 组件 | 需 web-view 已绑定域名 |

---

## 二、小程序跳转另一个小程序

### 2.1 小程序端调用

```javascript
// utils/app-jump.js

/**
 * 跳转到另一个小程序
 * @param {string} appId - 目标小程序 AppID
 * @param {string} path - 目标页面路径（不含参数）
 * @param {object} extraData - 传递给目标小程序的数据
 * @param {string} envVersion - 版本：'release' | 'trial' | 'develop'
 */
function navigateToMiniProgram(appId, path = '', extraData = {}, envVersion = 'release') {
  // ⚠️ 每月只能跳转 50 个不同的小程序
  // ⚠️ 禁止在用户无感知情况下自动跳转（违规会被下架）
  wx.navigateToMiniProgram({
    appId,
    path,              // 如 'pages/index/index?id=123'
    extraData,          // 目标小程序可从 App.onLaunch/onShow 获取
    envVersion,         // 体验版/开发版慎用，测试完改回 release

    success(res) {
      console.log('[互跳] 跳转成功', res)
    },

    fail(err) {
      console.error('[互跳] 跳转失败', err)
      // err.errMsg 可能包含 'cancel'（用户取消）/ 'fail'
      if (err.errMsg?.includes('cancel')) {
        wx.showToast({ title: '已取消', icon: 'none' })
      } else {
        wx.showModal({
          title: '跳转失败',
          content: '请确保目标小程序已发布，或检查 AppID 是否正确',
          showCancel: false,
        })
      }
    },

    // ⚠️ 小程序跳转回当前小程序时的回调
    // 仅在当前小程序被打开时触发
    notSupportProxy() {
      console.warn('[互跳] 代理不支持')
    },
  })
}
```

```javascript
// 接收从另一个小程序带过来的数据
// app.js
App({
  onLaunch(options) {
    // 从另一个小程序跳转过来时，options.referrerInfo.appId 有来源小程序 ID
    // options.referrerInfo.extraData 有来源传过来的数据
    if (options.referrerInfo?.extraData) {
      console.log('[来自小程序的跳转]', options.referrerInfo.extraData)
    }
  },

  onShow(options) {
    // 每次从后台切回前台时也会触发
    if (options.scene === 1037 || options.scene === 1038) {
      // scene 1037: 从另一个小程序启动
      // scene 1038: 从另一个小程序返回
    }
  },
})
```

### 2.2 跳转路径构造最佳实践

```javascript
// 构造带参数的路径（需 URL 编码）
function buildMiniProgramPath(path, params) {
  const queryString = Object.entries(params)
    .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
    .join('&')
  return queryString ? `${path}?${queryString}` : path
}

// 示例：跳转到商品详情页
const targetPath = buildMiniProgramPath('pages/goods/detail', {
  id: 'goods_12345',
  from: 'share',
})
navigateToMiniProgram('wx_target_appid', targetPath, { orderId: 'xxx' })
```

---

## 三、小程序跳转 APP

### 3.1 前提条件

1. **APP 已绑定小程序**：在微信开放平台（open.weixin.qq.com）绑定同一主体的 APP 和小程序
2. **APP 已开通小程序跳转权限**：开放平台绑定后自动开通
3. **目标 APP 已安装**：未安装时需要在 `fail` 回调中引导用户下载

### 3.2 小程序端实现

```javascript
// 跳转 APP
function navigateToApp(appId, extraData = {}, downloadUrl = '') {
  wx.navigateToApp({
    appId,
    extraData,        // 传递给 APP 的数据（APP 端需接入微信 Open SDK）
    fail(err) {
      if (err.errMsg?.includes('app is not installed')) {
        // APP 未安装，引导用户下载
        wx.showModal({
          title: '下载 APP',
          content: '体验完整功能，请先下载安装 APP',
          confirmText: '去下载',
          success(res) {
            if (res.confirm) {
              // ⚠️ navigateToApp 第二次调用同样会失败
              // 正确做法：直接打开应用市场下载页或提供运营下载链接
              if (downloadUrl) {
                // 跳 H5 落地页（含 URL Scheme 自动跳转 + 手动下载入口）
                wx.navigateTo({ url: `/pages/webview/webview?url=${encodeURIComponent(downloadUrl)}` })
              } else {
                wx.showToast({ title: '请前往应用商店下载', icon: 'none' })
              }
            }
          },
        })
      } else if (err.errMsg?.includes('cancel')) {
        // 用户取消，不提示
      }
    },
  })
}
```

### 3.3 APP 端接收数据（Android）

```kotlin
// Android（微信 Open SDK）
// WXEntryActivity.kt
class WXEntryActivity : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val token = intent.getStringExtra("token")
        val ext = intent.getStringExtra("ext")

        // 处理来自小程序的跳转
        Log.d("WXEntry", "token=$token, ext=$ext")
    }
}
```

### 3.4 APP 端接收数据（iOS）

```swift
// iOS（微信 Open SDK）
// AppDelegate.swift
func onResp(_ resp: BaseResp!) {
    if resp is LaunchFromWX.Resp {
        let response = resp as! LaunchFromWX.Resp
        let token = response.extData["token"] as? String
        // 处理来自小程序的跳转
    }
}
```

---

## 四、URL Scheme（微信外跳转小程序）

### 4.1 获取 URL Scheme

> ⚠️ URL Scheme 有效期最长 1 年，需定期续期或使用.shortLink

**方式 A：通过 API 生成（服务端）**

```javascript
// 云函数生成 URL Scheme
exports.main = async (event, context) => {
  const cloud = require('wx-server-sdk')
  cloud.init()

  const res = await cloud.cloudAPI.urlscheme.generate({
    // ⚠️ 参数名是 snake_case，不是 camelCase
    jump_wxa: {
      path: 'pages/index/index',       // 目标页面路径（已在 app.json 注册）
      query: 'from=share&scene=123',  // 查询字符串（无前缀 ?，直接拼在 path? 后）
      env_version: 'release',          // ⚠️ 不是 envVersion，是 env_version
    },
    expire_type: 1,                    // 1=到期失效, 2=按 expire_time 指定时间失效
    expire_time: Math.floor(Date.now() / 1000) + 3600 * 24 * 30,  // 30天后过期（秒级时间戳）
  })

  return { code: 0, scheme: res.url }
}
```

**方式 B：公众平台手动生成**
微信公众平台 → 设置 → 基础配置 → 小程序码 → URL Scheme → 生成

### 4.2 在非微信环境使用 URL Scheme

```html
<!-- H5 落地页（Android / iOS Safari 均可）-->
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width">
  <title>打开小程序</title>
</head>
<body>
  <script>
    // 跳转到小程序
    window.location.href = 'weixin://dl/business/?t=YOUR_URL_SCHEME'
  </script>

  <!-- 备用方案：显示引导页面 -->
  <noscript>
    <p>请允许打开微信小程序</p>
    <a href="weixin://dl/business/?t=YOUR_URL_SCHEME">如果未自动跳转，点击这里</a>
  </noscript>
</body>
</html>
```

---

## 五、扫一扫打开小程序

### 5.1 生成小程序太阳码（带参数）

> ⚠️ URL Scheme 和太阳码是**两个不同的 API**：URL Scheme 用于"从外部拉起小程序"，太阳码用于"生成可扫码的二维码/小程序码图片"。
> **不要混淆！**

```javascript
// 云函数生成太阳码
exports.main = async (event, context) => {
  const cloud = require('wx-server-sdk')
  cloud.init()

  // ✅ 太阳码用 openAPI，不是 urlscheme.generate
  // 场景：小程序码（扫码后进入指定页面，适合海报/地推）
  const res = await cloud.cloudAPI.openapi.wxacode.get({
    path: 'pages/scan-result/index',  // 已注册页面路径（不带 ?）
    scene: 'id=123,from=poster',       // 最多32个字符，多参数用 , 分隔
    // width: 430,                       // 二维码宽度，默认 430
    // auto_color: false,
    // line_color: { r: 0, g: 0, b: 0 },
    // is_hyaline: false,
    env_version: 'release',             // release / trial / develop
  })

  // res.buffer 是图片二进制 Buffer，直接上传到云存储
  const uploadRes = await cloud.uploadFile({
    cloudPath: `qrcode/${Date.now()}.png`,
    fileContent: Buffer.from(res.buffer),
  })

  // 获取可访问的 URL
  const { fileList } = await cloud.getTempFileURL({ fileList: [uploadRes.fileID] })

  return { fileID: uploadRes.fileID, url: fileList[0].tempFileURL }
}
```

**无上限太阳码（适用于海报等高频场景）：**

```javascript
// ✅ 无上限小程序码（scene 可更长，适合带多个参数的推广码）
const res2 = await cloud.cloudAPI.openapi.wxacode.getUnlimited({
  scene: 'id=123&from=poster&ref=share',  // 最多 32 个字符
  page: 'pages/scan-result/index',         // 必须是已发布小程序存在的页面
  env_version: 'release',
  width: 280,
})

const uploadRes2 = await cloud.uploadFile({
  cloudPath: `qrcode/unlimited/${Date.now()}.png`,
  fileContent: Buffer.from(res2.buffer),
})
```

### 5.2 小程序内扫码识别

```javascript
// 扫码识别商品/设备
async function scanCode() {
  const res = await wx.scanCode({
    onlyFromCamera: true,    // false=允许扫描相册图片
    scanType: ['qrCode', 'barCode', 'datamatrix'],  // 识别类型
  })

  // res.result: 扫码结果字符串
  // res.charSet: 字符集
  // res.scanType: 扫码类型

  try {
    // 解析 URL Scheme 携带的参数
    const params = parseQueryString(res.result)
    if (params.id) {
      wx.navigateTo({ url: `/pages/goods/detail?id=${params.id}` })
    } else if (params.scene) {
      // 太阳码参数在 scene 中
      const scene = decodeURIComponent(params.scene)
      const sceneParams = parseQueryString(scene)
      wx.navigateTo({ url: `/pages/scan-result/index?scene=${scene}` })
    }
  } catch (err) {
    wx.showToast({ title: '无效的二维码', icon: 'none' })
  }
}

function parseQueryString(url) {
  const [path, query] = url.split('?')
  if (!query) return {}
  return Object.fromEntries(
    query.split('&').map(p => {
      const [k, v] = p.split('=')
      return [k, v]
    })
  )
}
```

---

## 六、开放标签（微信内 H5 跳转小程序）

### 6.1 引入 JS-SDK

```html
<!-- H5 页面 -->
<script src="https://res.wx.qq.com/open/js/jweixin-1.6.0.js"></script>
<script>
wx.config({
  beta: true,           // 必须在 config 中声明为微信浏览器环境
  debug: false,
  appId: 'YOUR_APPID',
  timestamp: TIMESTAMP,
  nonceStr: NONCE_STR,
  signature: SIGNATURE,
  jsApiList: ['wx.openLaunchWeapp'],  // 必须声明此 API
})
</script>
```

### 6.2 使用开放标签

```html
<!-- 必须使用微信小程序的官方标签，否则无法识别 -->
<wx-open-launch-app
  id="launch-btn"
  appid="wx_target_appid"
  extra-data="{{extraData}}"
  style="width:200px;height:50px;"
>
  <!-- 自定义标签外观（必须放在 template 内）-->
  <template>
    <button style="background:#07c160;color:#fff;border:none;padding:10px 20px;border-radius:4px;">
      打开小程序
    </button>
  </template>
</wx-open-launch-app>
```

```javascript
document.getElementById('launch-btn').addEventListener('launch', function (e) {
  console.log('跳转成功', e.detail)
})

document.getElementById('launch-btn').addEventListener('error', function (e) {
  console.error('跳转失败', e.detail)
})
```

---

## 七、Common Mistakes（互跳高频错误）

| 错误 | 正确做法 |
|------|---------|
| 自动跳转小程序（无用户操作）| ⚠️ 违规！必须由用户点击按钮触发，违规会被微信永久封禁跳转功能 |
| 跳转路径写错导致 404 | 路径必须是已在 app.json 中注册页面，不带前导 `/` |
| 跳转 APP 但 APP 未绑定 | 需在微信开放平台绑定同一主体的 APP 和小程序 |
| URL Scheme 过期后仍在使用 | 设置 expire_time 续期，或使用.shortLink（长期有效）|
| scanCode 用 onlyFromCamera: false 识别小程序码 | 小程序太阳码只能通过相机扫码识别（不支持相册）|
| 开放标签不显示 | 检查是否引入了微信 JS-SDK 1.6+，且 config 时声明了 beta |
| extraData 传敏感信息 | extraData 仅支持纯数据，敏感信息应通过后端接口传递 |

---

## 八、官方文档链接

- 小程序跳转另一个小程序：https://developers.weixin.qq.com/miniprogram/dev/api/navigate/wx.navigateToMiniProgram.html
- 小程序跳转 APP：https://developers.weixin.qq.com/miniprogram/dev/api/navigate/wx.navigateToApp.html
- URL Scheme：https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/url-scheme.html
- 扫普通链接二维码：https://developers.weixin.qq.com/miniprogram/introduction/qrcode.html
- 开放标签：https://developers.weixin.qq.com/doc/offiaccount/OA_Web_Apps/WeChat_Open_Tag.html
