---
name: features-h5-adapt
description: uni-app H5 宽屏适配 topWindow、leftWindow、rightWindow、getTopWindowStyle、setTopWindowStyle
---

# H5 宽屏适配

**仅 H5 支持**。用于大屏（如 Pad、PC）下多窗口布局：顶部栏、左侧栏、右侧栏 + 主页面。

## 配置

在 **pages.json** 中配置 **topWindow**、**leftWindow**、**rightWindow**，分别指定对应 .vue 路径与 style（如 height、width）。可配合 **matchMedia**（如 minWidth: 768）控制何时显示。globalStyle 中可设 leftWindow、topWindow、rightWindow 布尔值表示默认是否显示。

## API

- **uni.getTopWindowStyle()** / **uni.getLeftWindowStyle()** / **uni.getRightWindowStyle()**：获取对应窗口样式。
- **uni.setTopWindowStyle(OBJECT)** / **uni.setLeftWindowStyle(OBJECT)** / **uni.setRightWindowStyle(OBJECT)**：动态设置窗口样式。
- **uni.showTopWindow()** / **uni.hideTopWindow()**：显示/隐藏顶部窗口。left/right 同理。

主页面宽度 = leftWindow(可选) + 页面主体 + rightWindow(可选)；可配合 **maxWidth**（globalStyle）限制主体最大宽度，两侧留白。fixed 元素需使用 --window-left、--window-right 保证位置正确。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/adapt
- https://uniapp.dcloud.net.cn/collocation/pages?id=topwindow
-->
