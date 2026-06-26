---
name: features-window-communication
description: uni-app 页面栈与全局事件 getCurrentPages、uni.$emit、uni.$on、uni.$off
---

# 页面栈与全局通讯

## getCurrentPages()

获取当前页面栈实例，返回数组：第一个为首页，最后一个为当前页。**仅用于读取**，不要修改页面栈。

每项为页面实例，常用属性/方法：`route`（当前页路径）、`$vm`（Vue 实例）。App-Vue 下还有 `$getAppWebview()` 可获取当前 webview 对象。选项式 API 下不要定义名为 `route` 的响应式变量，会覆盖实例的 route。

## 全局自定义事件（跨页通讯）

- **uni.$emit(eventName, object)**：触发全局自定义事件，附加参数传给监听回调。
- **uni.$on(eventName, callback)**：监听该事件，可多次触发。
- **uni.$once(eventName, callback)**：监听一次，触发后自动移除。
- **uni.$off(eventName, callback)**：移除监听。不传参则移除 App 级所有监听；只传 eventName 则移除该事件所有回调；同时传 eventName 与 callback 则只移除该回调（需与 $on 传入同一引用）。

使用建议：在 onLoad 里 $on 的，在 onUnload 里 $off，避免重复监听与内存泄漏；一次性通讯可用 $once。

## 页面间传参

除路由 url 传参、EventChannel（navigateTo 的 events）外，复杂数据可用 uni.$emit / $on 或全局变量（如 getApp().globalData）传递。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/window/communication
- https://uniapp.dcloud.net.cn/api/window/window
-->
