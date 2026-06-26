---
name: features-ui-extras
description: uni-app 媒体查询、胶囊按钮、窗口背景 createMediaQueryObserver、getMenuButtonBoundingClientRect、setBackgroundColor
---

# 媒体查询、胶囊按钮与窗口背景

## 媒体查询

**uni.createMediaQueryObserver([this])**：创建 MediaQueryObserver，监听页面 media query 状态（如宽高是否在指定范围）。自定义组件内传 this；小程序端不支持 this。调用 **observe(descriptor, callback)** 开始监听，descriptor 可设 minWidth、maxWidth、minHeight、maxHeight、width、height、orientation 等（单位 px）；callback 收到 **matches**（是否满足条件）。**disconnect()** 停止监听。部分小程序不支持动态监听，仅执行一次。用于响应式布局、横竖屏适配等。

## 胶囊按钮（小程序）

**uni.getMenuButtonBoundingClientRect()**：获取右上角**菜单/胶囊按钮**的布局信息（width、height、top、right、bottom、left，单位 px），以屏幕左上角为原点。**仅小程序支持**（App、H5 不支持）。当导航栏设为 custom 时，仍会显示胶囊按钮，可用本 API 获取位置以避开或围绕其布局。

## 窗口背景

- **uni.setBackgroundColor(OBJECT)**：动态设置窗口背景色。参数 frontColor、backgroundColor 等，各端支持见官方「bgcolor」文档。
- **uni.setBackgroundTextStyle(OBJECT)**：设置下拉时 loading、字体样式（dark/light）。部分平台支持。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/media-query-observer
- https://uniapp.dcloud.net.cn/api/ui/menuButton
- https://uniapp.dcloud.net.cn/api/ui/bgcolor
-->
