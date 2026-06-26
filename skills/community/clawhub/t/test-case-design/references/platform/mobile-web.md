# 移动 Web 端专项测试点

> 本文件定义移动 Web（H5）区别于其他平台的专项测试维度和策略要点。
> 用例输出格式见 `references/examples/format-spec.md`，检查清单见 `references/checklists/mobile-web-checklist.md`。

---

## 一、响应式布局

### 专项关注点
- 关键断点适配：320px / 375px / 414px / 768px
- 媒体查询断点是否覆盖全部目标设备
- 刘海屏/挖孔屏安全区域适配（env(safe-area-inset-*)）
- 横屏布局切换
- 长屏幕（19.5:9）与短屏幕（16:9）的内容显示差异

### 常见缺陷
- 小屏幕下文字截断或重叠
- 横屏时布局错乱
- 刘海屏内容被遮挡

---

## 二、触摸交互

### 专项关注点
- 点击态视觉反馈（:active 伪类在移动端的兼容性）
- 300ms 点击延迟与 touch-action 处理
- 滑动翻页/轮播的流畅度
- 双指缩放限制与页面级别缩放控制
- 嵌套滚动区域的手势冲突
- 惯性滚动与橡皮筋效果

### 常见缺陷
- 点击无视觉反馈，用户不确定是否点中
- 快速滑动时页面卡顿
- 嵌套列表内外层滑动冲突

---

## 三、浏览器兼容

### 专项关注点
- iOS Safari / Android Chrome / 微信内置浏览器 / QQ 浏览器 / UC 浏览器
- WebView 容器差异（WKWebView vs Android WebView）
- CSS 特性兼容（flexbox gap、aspect-ratio 等）
- JavaScript API 兼容（IntersectionObserver、ResizeObserver 等）
- 隐私模式/无痕模式对 Storage 的影响

### 常见缺陷
- iOS Safari 日期格式解析差异（需兼容 yyyy-MM-dd）
- 微信内置浏览器长按识别二维码干扰页面交互
- 隐私模式下 localStorage 写入报错

---

## 四、视口与输入

### 专项关注点
- viewport meta 配置（width、initial-scale、viewport-fit）
- 虚拟键盘弹出时布局调整（100vh 在移动端的表现）
- 输入框聚焦后被键盘遮挡
- 不同 input type 触发的键盘类型（number/tel/email/url）
- 中文输入法组合事件（compositionstart/end）

### 常见缺陷
- 键盘弹出后输入框被遮挡
- 100vh 包含地址栏高度导致页面高度计算错误
- 中文输入法搜索时触发多次请求

---

## 五、第三方登录与支付

### 专项关注点
- 微信 H5 授权登录（需在微信浏览器内，使用 OAuth2.0）
- 微信 H5 支付（需配置支付目录和域名）
- 支付宝 H5 支付流程
- 授权回调 URL 的参数传递与状态恢复
- 登录态在多标签页间的同步

### 常见缺陷
- 非微信浏览器内无法调起微信登录
- 支付回调 URL 配置错误导致支付失败
- 登录态跨标签页不同步

---

## 六、H5 特有功能

### 专项关注点
- tel:/sms:/mailto: 链接的触发与参数
- Web Share API 的浏览器支持与降级
- PWA：添加到主屏幕、Service Worker 离线缓存
- 地理定位/相机调用（需 HTTPS + 用户授权）
- 滚动穿透与弹窗锁定

### 常见缺陷
- 弹窗打开时背景仍可滚动（滚动穿透）
- PWA manifest 配置错误导致添加到主屏幕失败
- HTTP 环境下地理位置 API 不可用

---

## 七、缓存与离线

### 专项关注点
- Service Worker 缓存策略：Cache First / Network First / Stale While Revalidate
- HTTP 缓存头配置（Cache-Control / ETag / Last-Modified）
- 离线访问降级：哪些功能可用、哪些需提示
- 缓存更新机制：版本更新后如何让用户获取最新资源
- 预缓存关键资源（App Shell 模式）

### 常见缺陷
- 缓存策略错误导致用户始终看到旧版本
- 离线时白屏无任何降级提示
- 缓存更新后旧资源未失效
- Service Worker 异常导致页面永久无法加载

---

## 八、SEO 与分享

### 专项关注点
- 微信分享卡片：标题/描述/封面图（依赖 JS-SDK 或 meta 标签）
- Open Graph 标签配置
- 页面标题与 meta description
- URL 参数在分享链接中的传递

### 常见缺陷
- 微信分享未调用 JS-SDK 导致默认抓取页面内容
- 分享封面图未配置
- URL 参数在分享中丢失
