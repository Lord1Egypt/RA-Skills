---
name: core-app
description: App.vue 应用生命周期、globalData、全局样式
---

# App.vue / App.uvue

应用入口组件，所有页面在其下切换。**不能写 `<template>`**，仅用于：监听应用生命周期、配置全局样式、配置 globalData。

应用生命周期**只能在 App.vue 中监听**，在页面中监听无效。

## 应用生命周期

| 函数名 | 说明 |
|--------|------|
| onLaunch | 应用初始化完成时触发（全局只触发一次），参数同 `uni.getLaunchOptionsSync()` 返回值 |
| onShow | 应用启动或从后台进入前台时触发 |
| onHide | 应用从前台进入后台时触发 |
| onError | 应用报错时触发（app-uvue 不支持） |
| onUnhandledRejection | 未处理的 Promise 拒绝（2.8.1+，app-uvue 暂不支持） |
| onPageNotFound | 页面不存在时触发（实际已打开页面后发现不存在才触发，API 跳转不存在的页面不触发） |
| onThemeChange | 系统主题变化（app-uvue 不支持） |
| onLastPageBackPress | 最后一个页面按 Android 返回键（app-uvue-android 3.9+） |
| onExit | 应用退出（app-uvue-android 3.9+） |

组合式 API 使用时，Vue2 与 Vue3 有区别，见官方「Vue2/Vue3 组合式 API」文档。

## globalData

在 App.vue 的 `export default { globalData: { text: 'text' } }` 中定义。在 js 中通过 `getApp().globalData.text` 读写。  
onLaunch 时 `getApp()` 可能尚未可用，可暂用 `this.globalData`。若需在页面展示 globalData，建议在页面 onShow 中重新赋值到页面 data。

状态管理推荐使用 vuex（在 main.js 中定义），而非仅依赖 globalData。

## 全局样式

在 App.vue 的 `<style>` 中编写，会作用于所有页面。若项目同时有 vue 与 nvue，nvue 不支持的 CSS 会报警，可将仅非 nvue 使用的样式放在条件编译中（如 `#ifndef APP-PLUS-NVUE`）。

<!--
Source references:
- https://uniapp.dcloud.net.cn/collocation/App
-->
