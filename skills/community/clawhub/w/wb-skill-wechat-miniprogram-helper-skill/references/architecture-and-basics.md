# 微信小程序架构与基础

## 一、双线程架构（必须理解）

微信小程序不是普通网页，而是**双线程**模型：

- **逻辑层（AppService）**：运行 `js`，处理数据、业务逻辑。只有一个 JS 线程。
- **视图层（WebView）**：渲染 `wxml/wxss`，每个页面一个 WebView 实例。

两者通过 **Native 中转** 通信：`setData` 把逻辑层数据序列化后发给视图层渲染。**逻辑层和视图层不能直接互相调用**，也没有 `window`/`document` 等 DOM API。因此：
- 不能用 `document.getElementById`、`window`、`jQuery`。
- Canvas 必须用小程序自有 API（`type="2d"` + `SelectorQuery`），不能直接拿 DOM canvas。
- 耗时同步操作会卡住整个逻辑层（只有一个线程）。

## 二、四件套（每个页面四个文件）

```
pages/index/
├── index.wxml   # 结构（类似 HTML，但标签是 <view>/<text>/<button>）
├── index.wxss   # 样式（类似 CSS，但用 rpx，选择器受限）
├── index.js     # 逻辑（Page({ data, 生命周期, 方法 })）
└── index.json   # 页面配置（标题、usingComponents、disableScroll 等）
```

根目录还有：`app.js`（App 实例）、`app.json`（全局页面注册+窗口样式）、`app.wxss`（全局样式）、`project.config.json`（项目/AppID）、`sitemap.json`。

## 三、WXML 与数据绑定

```xml
<view class="container">
  <text>{{title}}</text>
  <button bindtap="onTap">点击</button>
  <view wx:for="{{list}}" wx:key="id">{{item.name}}</view>
</view>
```

- 数据来自 `Page({ data: { title: '...' } })`。
- 事件用 `bindtap`（冒泡）/ `catchtap`（阻止冒泡），值是方法名字符串。
- 列表渲染 `wx:for`，务必加 `wx:key`（用字段名或 `*this`）。
- 条件渲染 `wx:if` / `hidden`。

## 四、WXSS 与 rpx

- **rpx（responsive pixel）**：750rpx = 屏幕宽度。iPhone 6 上 1rpx ≈ 0.5px，自动适配不同屏。UI 尺寸优先用 rpx。
- 选择器只支持部分（类、id、element、伪类 `::after/::before`），**不支持通配符 `*`、属性选择器、嵌套**。
- 样式隔离：页面样式默认不影响其他页面；`app.wxss` 全局生效。
- 不能用 `*` 重置，背景图用网络地址或 base64（本地路径在 wxss 里受限，建议用 `<image>` 标签）。

## 五、setData（核心，也是性能关键）

```js
this.setData({ title: '新标题', count: this.data.count + 1 })
```

规则与坑：
- 只传**变化的字段**，不要每次 `setData(this.data)` 整体覆盖（浪费通信）。
- 单次 `setData` 数据量 **≤ 256KB**，否则报错；大列表分页/节流。
- 高频动画（如粒子）不要每帧 `setData` 大对象——Canvas 绘制走 Canvas API，不靠 setData 渲染帧。
- `setData` 是异步的，回调里才能拿到视图更新后的结果。

## 六、生命周期

App（`app.js`）：`onLaunch`（启动一次）、`onShow`、`onHide`、`onError`。
Page（`page.js`）：`onLoad`（参数）、`onShow`、`onReady`（首次渲染完）、`onHide`、`onUnload`（离开销毁）。
资源释放（定时器、监听）放在 `onUnload` / `onHide` 清理，避免泄漏。

## 七、Canvas 2D（特效/绘图首选）

```js
// wxml: <canvas type="2d" id="cv" style="width:100%;height:300px;"></canvas>
Page({
  onReady() {
    const query = wx.createSelectorQuery()
    query.select('#cv').fields({ node: true, size: true }).exec((res) => {
      const canvas = res[0].node
      const ctx = canvas.getContext('2d')
      const dpr = Math.min(wx.getSystemInfoSync().pixelRatio, 2) // dpr 封顶 2
      canvas.width = res[0].width * dpr
      canvas.height = res[0].height * dpr
      ctx.scale(dpr, dpr)
      this.canvas = canvas; this.ctx = ctx
      this.loop()
    })
  },
  loop() {
    const ctx = this.ctx
    // 绘制...
    this.canvas.requestAnimationFrame(() => this.loop())
  }
})
```

要点：
- 必须用 `type="2d"`，旧版 `wx.createCanvasContext` 已废弃。
- `ctx` 要在 `exec` 回调里拿到并保存（`this.ctx`），绘制函数里直接用，避免 "ctx is not defined"。
- dpr 封顶 2，防止高像素屏粒子爆炸卡顿。
- 动画用 `canvas.requestAnimationFrame`，不要用 `setInterval` 驱动帧。

## 八、网络请求 wx.request

```js
wx.request({
  url: 'https://your-api.com/api/list',
  method: 'GET',
  success: (res) => { this.setData({ list: res.data }) },
  fail: (err) => { wx.showToast({ title: '请求失败', icon: 'none' }) }
})
```

- 正式环境**必须配置合法域名**（小程序后台 → 开发 → 开发设置 → 服务器域名）。
- 本地开发可在 DevTools 勾选「不校验合法域名、TLS、HTTPS」临时绕过。
- 默认超时 60s，大文件走 `wx.downloadFile`/`wx.uploadFile`。

## 九、路由与导航

- `wx.navigateTo`（保留当前页，进子页，栈最多 10 层）
- `wx.redirectTo`（替换当前页）
- `wx.switchTab`（跳 tabBar 页面）
- `wx.navigateBack`（返回）
- tabBar 在 `app.json` 的 `tabBar` 字段配置，至少 2 个、至多 5 个。
