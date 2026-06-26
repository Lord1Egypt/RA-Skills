---
name: features-preload-page
description: uni-app 页面预加载 preloadPage、unPreloadPage 性能优化
---

# 页面预加载

提前加载页面资源与逻辑，打开时直接使用已预载实例，加快首屏。**支持范围**：App-nvue（2.7.12+）、H5（2.7.12+）。微信/支付宝等小程序、HarmonyOS Next 不支持。

## uni.preloadPage(OBJECT)

- **url**（必填）：要预加载的页面路径，与 pages.json 中 path 一致，可带参数。
- H5：预加载该页面对应的 js，不执行页面预渲染。
- App-nvue：预加载 nvue 页面并预渲染，会触发该页的 `onLoad`、`onReady`，**不触发** `onShow`。

## 使用规则

1. 打开新页时，若 url 与某次 preloadPage 的 url **完全相同**（含参数），则优先复用该预加载页，只触发 `onShow`。
2. url 不一致则正常打开新页，不复用预加载实例。
3. tabBar 页仅可预加载**尚未显示过**的页，否则返回 fail（already exists）。
4. 同一 url 同一时间只预加载一次。
5. 若预加载页已在栈中，再次 navigateTo 相同 url 会打开新的非预载页。
6. `reLaunch`、`switchTab`、`navigateBack`（含 Android 返回键）时，预加载页不销毁，只触发 `onHide`。
7. 在预加载页内调用 `redirectTo` 会销毁该页并触发 `onUnload`。

## uni.unPreloadPage(OBJECT)

取消已预加载的页面（HarmonyOS Next 不支持）。传入与 preloadPage 一致的 url。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/preload-page
-->
