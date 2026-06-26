---
name: advanced-subnvue
description: uni-app App 原生子窗体 subNVues、getSubNVueById、getCurrentSubNVue
---

# 原生子窗体（subNVues）

**仅 App 支持**（1.9.10+）。subNVue 为 nvue 编写的原生子窗体，可覆盖在普通 vue 页面上方，用于自定义导航栏、悬浮窗、弹层等，无层级问题。

## 配置

在 **pages.json** 的当前页 **style** 下配置 **app-plus.subNVues** 数组，每项含 id、path（nvue 路径）、style（宽高、位置等）、type 等。详见「app-subNVues」文档。

## API

- **uni.getSubNVueById(subNvueId)**：根据 id 获取 subNVue 实例（在 vue 页面中调用）。
- **getCurrentSubNVue()**：在 subNVue 的 nvue 页面中获取当前子窗体实例。实例可调用 **show()**、**hide()**、**setStyle()** 等。通讯建议用 **uni.$emit** / **uni.$on**，不再使用已过时的 postMessage/onMessage。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/window/subNVues
- https://uniapp.dcloud.net.cn/collocation/pages?id=app-subNVues
-->
