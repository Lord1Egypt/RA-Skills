---
name: core-main
description: uni-app 入口 main.js/uts、代码时序与插件
---

# 入口 main.js/uts

uni-app 的入口文件：js 引擎版为 `main.js`，uni-app x 为 `main.uts`。主要作用：初始化 Vue 实例、注册全局组件、使用插件（如 i18n、vuex）。

## Vue2 / Vue3 / uni-app x 写法

- **Vue2**：`new Vue({ ...App }).$mount()`
- **Vue3 / uni-app x**：`createSSRApp(App)`，在 `export function createApp() { ... }` 中创建并返回 `{ app }`
- 全局组件：`Vue.component('page-head', PageHead)` 或 `app.component('page-head', PageHead)`

## 代码时序（重要）

应用启动时执行顺序：

1. `main.js/uts` 中 `createApp()` **外部**的代码、任意页面/组件 script 中 `export default {}` **外部**的代码
2. `createApp()` **内部**的代码
3. `App.vue` 中 `onLaunch`
4. 首页 `onLoad`
5. 首页 `onReady`

**注意**：上述 1、2 以及 onLaunch 中的代码都会影响启动速度；且执行过早时很多 API 和界面能力不可用，需 try-catch。`export default {}` 外定义的变量在应用存活期间常驻内存，不会随页面关闭回收。

## 插件与路由

- 使用 `Vue.use` 引用插件，`Vue.prototype` 添加全局变量。
- **不支持 vue-router**，路由须在 `pages.json` 中配置；若需类似能力可到插件市场搜索「路由」。
- 推荐用 **easycom** 按需使用组件，比全局注册更省资源。

## 平台差异

- nvue 暂不支持在 main.js 注册全局组件
- uni-app x 暂不支持 i18n、vuex、pinia 等插件

<!--
Source references:
- https://uniapp.dcloud.net.cn/collocation/main
-->
