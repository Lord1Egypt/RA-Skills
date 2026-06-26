---
name: features-router
description: uni-app 路由 API、页面传参、EventChannel、窗口动画
---

# 路由与页面跳转

路由在 `pages.json` 中配置，不可使用 vue-router。跳转只能指向已注册的页面路径；打开 Web URL 需用 web-view 或各端专有方式（如 App 的 plus.runtime.openURL）。

## 跳转 API

| API | 说明 |
|-----|------|
| uni.navigateTo | 保留当前页，跳转非 tabBar 页，可返回 |
| uni.redirectTo | 关闭当前页，跳转非 tabBar 页 |
| uni.reLaunch | 关闭所有页，打开任意页（可带参数；若为 tabBar 页则不能带参数） |
| uni.switchTab | 只能跳转 tabBar 页，url 不能带参数 |
| uni.navigateBack | 返回上一页或多级（delta） |

- 目标页必须在 pages.json 的 pages 或分包中注册。
- 页面栈有层级限制，不能无限 navigateTo。
- **不能在首页 onReady 之前**进行页面跳转。

## 传参

- **url 传参**：`url: 'pages/detail/detail?id=1&name=abc'`，目标页在 onLoad(option) 中通过 `option.id`、`option.name` 获取。注意 url 长度限制，复杂对象可 encodeURIComponent(JSON.stringify(obj)) 后传递。
- **EventChannel**（2.8.9+）：`uni.navigateTo` 的 `events` 与 `success` 中 `res.eventChannel` 用于与打开页双向通信；被打开页通过 `getOpenerEventChannel()` 拿到 channel，`emit` / `on` / `once` / `off`。需在 onUnload 时取消监听，避免内存泄漏。

## 窗口动画（仅 App）

在 navigateTo / navigateBack 的 OBJECT 中可设 `animationType`、`animationDuration`。  
也可在 pages.json 的页面 style 或 navigator 组件上配置。  
可选动画：slide-in-right、pop-in、fade-in、zoom-out 等，详见官方「窗口动画」文档。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/router
-->
