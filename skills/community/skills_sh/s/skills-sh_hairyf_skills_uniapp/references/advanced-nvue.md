---
name: advanced-nvue
description: uni-app nvue 简介、与 vue 差异、原生渲染、requireNativePlugin
---

# nvue 简介

nvue 为 **App 端原生渲染**页面，使用 weex 或 uni-app 编译模式，样式与布局能力与 vue 有差异（如 CSS 为子集、仅支持 flex 等），详见「nvue 样式」文档。**小程序与 H5 无 nvue**。

## 与 vue 的差异

- 渲染：vue 为 webview，nvue 为原生控件，性能与流畅度更好，但 CSS 支持受限。
- 样式：推荐 flex 布局；单位 weex 模式下 px 等价于 vue 的 rpx，wx 等价于 vue 的 px；不支持百分比等，见 nvue-css 文档。
- 生命周期：无 onShow 等页面生命周期时可用 weex 的 addEventListener 等替代；建议优先用 uni-app 编译模式。
- 组件：部分 vue 组件在 nvue 下不可用或表现不同；原生组件无层级问题。

## uni.requireNativePlugin(PluginName)

在 nvue（或 App 端）引入 **App 原生插件**，PluginName 为插件名。也可引入项目 nativeplugins 或插件市场云打包的插件，需在 manifest 中配置并打自定义基座。vue 页面若需用原生能力，通常通过 nvue 子页或原生插件提供的 API。

## 使用场景

需要高性能长列表、复杂动效、避免 webview 兼容问题时，可考虑 nvue；否则 vue 即可。纯 nvue 项目可设置 render 为 native；混合项目下首页可为 nvue 以加快首屏。

<!--
Source references:
- https://uniapp.dcloud.net.cn/tutorial/nvue-api
- https://uniapp.dcloud.net.cn/tutorial/nvue-css
- https://uniapp.dcloud.net.cn/plugin/native-plugin
-->
