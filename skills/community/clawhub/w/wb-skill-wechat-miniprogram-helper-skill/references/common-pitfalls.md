# 小程序常见报错与修复

按出现频率整理，给 WorkBuddy 在用户贴报错时直接对照修复。

## 1. 无效的 app.json window["disableScroll"]

**报错**：`无效的 app.json window["disableScroll"] ...`
**原因**：`disableScroll` 只允许在**页面级** `json`（`pages/index/index.json`）里设置，全局 `app.json` 的 `window` 不支持该字段。
**修复**：
- 从 `app.json` 的 `window` 删除 `disableScroll`。
- 放到需要禁止滚动的页面 `index.json`：`{ "disableScroll": true }`。
- 注意 `index.json` 是纯 JSON，**不能写注释、不能有尾随逗号**。

## 2. ReferenceError: ctx is not defined（Canvas 绘制时）

**报错**：`ctx is not defined` 或 `ctx.fillText is not a function`。
**原因**：在 `onReady` 的 `SelectorQuery` 回调外（如 `loop()`、`explode()`）使用 `ctx`，但 `ctx` 是回调的局部变量，外部访问不到。
**修复**：在回调里把 `ctx` 存到实例：`this.ctx = canvas.getContext('2d')`，绘制函数内用 `const ctx = this.ctx`。同理 `canvas` 存 `this.canvas`。

```js
query.select('#cv').fields({ node: true, size: true }).exec((res) => {
  const canvas = res[0].node
  const ctx = canvas.getContext('2d')
  this.canvas = canvas
  this.ctx = ctx
  this.loop()
})
loop() {
  const ctx = this.ctx   // 关键：从实例取，不要依赖外部作用域
  // ...
}
```

## 3. 体验起来卡 / 掉帧 / 发热

**原因**：Canvas 每帧绘制太重（阴影、重复测量、像素过多）。
**修复清单**：
- **禁用 `shadowBlur`**：阴影是高开销操作，逐帧用直接卡死。用纯色/简单渐变替代。
- **dpr 封顶 2**：`const dpr = Math.min(pixelRatio, 2)`，高像素屏像素量暴涨。
- **文字宽度一次性测量并缓存**：不要在每帧 `ctx.measureText`，在创建文字时测一次存起来。
- **控制粒子/对象数量**：烟花、星辰这类按屏幕面积设上限，避免指数增长。
- **动画用 `canvas.requestAnimationFrame`**，不用 `setInterval`。
- 星空/云/喜鹊等静态或低频元素，能预渲染就预渲染，不要每帧重算。

## 4. 扫码预览提示「暂无体验权限」

**现象**：别人扫预览码进不去，提示暂无体验权限。
**原因**：用的是**测试号 / 游客模式**（`touristappid`），测试号**没有体验成员入口**，只能开发者本人预览。
**修复**：
- 到 [mp.weixin.qq.com](https://mp.weixin.qq.com) 注册正式小程序，拿到 **AppID**。
- 把 AppID 填进 `project.config.json` 的 `appid` 字段（或 DevTools 详情里改）。
- 后台 → **成员管理 → 体验成员** → 添加对方微信号 → 对方接受 → 即可扫码体验/预览。
- 注意：测试号也看不到「用户身份/成员管理」菜单，那是正式账号才有。

## 5. 解析 app.json 失败 / 格式错误

**现象**：`app.json 错误: 文件格式错误` 或项目打不开。
**原因**：JSON 不支持注释、不支持尾随逗号、键必须双引号。
**修复**：删除 `//` 注释、去掉最后一个元素的逗号、确保全部双引号。改完用 DevTools 重新编译。

## 6. wx.request 本地接口不通 / 报错

**原因**：正式环境要求 HTTPS + 已配置合法域名；本地未配域名会失败。
**修复**：DevTools 右上角「详情 → 本地设置」勾选「不校验合法域名、TLS 版本以及 HTTPS 证书」即可本地联调；上线前在后台配好服务器域名。

## 7. 图片 / 字体不显示

- 网络图片需在后台配置 `downloadFile` 合法域名；本地图片放项目内用相对路径或 `<image src="/assets/x.png">`。
- 自定义字体用 `wx.loadFontFace`，字体文件需 HTTPS 且配置域名。

## 8. setData 频繁导致卡顿 / 失败

- 单条 `setData` 数据 > 256KB 会报错；大列表改为分页、增量更新、或走 Canvas 直接绘制（不依赖 setData 渲染）。
- 动画帧不要每次 `setData` 整个 data，只更新必要字段。
