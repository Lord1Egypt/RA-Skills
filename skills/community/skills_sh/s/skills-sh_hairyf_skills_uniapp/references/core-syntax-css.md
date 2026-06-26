---
name: core-syntax-css
description: uni-app 样式与布局、rpx/px 单位、预处理器、nvue 差异
---

# 页面样式与布局

vue 页面为 webview 渲染；app-nvue 为原生渲染，CSS 能力受限，见 nvue-css 文档；app-uvue 为 uni-app x 原生样式，见 uvue 文档。

## 尺寸单位

- **rpx**：响应式单位，以 750 宽为基准，750rpx = 屏幕宽度。随屏幕变宽等比放大。App（vue2 不含 nvue）和 H5（vue2）默认在宽度 ≥960px 时按 375px 基准计算，可在 globalStyle 中配置 rpxCalcMaxDeviceWidth、rpxCalcBaseDeviceWidth 等。
- **px**：设备像素。不想随宽度缩放时用 px。
- **rem/vh/vw**：vue 页面支持；nvue 不支持。rem 根字号可由 page-meta 配置。

设计稿换算：`750 * 元素宽度 / 设计稿宽度` 得到 rpx。例：设计稿 750px 宽、元素 100px → 100rpx；设计稿 375px、元素 200px → 400rpx。

## 预处理器

支持 less、sass/scss、stylus。Vue2 项目 sass 推荐用 dart-sass（manifest 可配 sassImplementationName）；Vue3 与 uni-app x 仅支持 dart-sass。dart-sass 中 `/deep/` 改为 `::v-deep`，除法用 `math.div()` 等，见官方「css 预处理器」说明。

## 注意

- 非 H5 端不支持 `*` 选择器；页面根用 `page` 不用 body。
- 非 H5 端默认未启用 scoped，需隔离时在 style 上加 `scoped`。
- nvue 不支持百分比；weex 模式下 px 与 vue 中 rpx 含义类似，wx 与 vue 中 px 含义类似。
- App 端 plus API、titleNView 等单位只支持 px，不支持 rpx。

<!--
Source references:
- https://uniapp.dcloud.net.cn/tutorial/syntax-css
- https://uniapp.dcloud.net.cn/collocation/pages?id=globalstyle
-->
