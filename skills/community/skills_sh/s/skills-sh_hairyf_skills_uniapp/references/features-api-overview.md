---
name: features-api-overview
description: uni-app API 概述、Promise 化、各端特色 API、canIUse
---

# API 概述

uni-app 的 JS API 由**标准 ECMAScript** 与 **uni 扩展 API**（挂载在 `uni` 对象上）组成。非 Web 端（小程序、App）运行在 JSCore/V8，**没有** window、document、navigator 等浏览器对象，但支持标准 JS 语法与数据类型。

## 调用约定

- 多数 API 接受一个 **OBJECT**，其中可指定 `success`、`fail`、`complete` 回调。
- `uni.on*` 开头的为**监听类** API，传入回调函数。
- 异步 API 返回结果中常有 `errMsg`；同步 API（如 `getXxxSync`）无 `errMsg`。
- 各端特色 API 可通过**条件编译**使用，App 端可参考 html5plus.org、原生插件文档。

## Promise 化

- 异步 API **不传** success/fail/complete 时，将返回 **Promise**（如 `uni.getImageInfo()`）。
- 若 API 本身会返回对象（如 `uni.connectSocket` 返回 task），且需要拿到该对象，则**必须**至少传入 success/fail/complete 之一，否则得到的是 Promise 而非 task。
- **不参与 Promise 化**：同步方法（*Sync）、create 开头的方法、*Manager 结尾的方法。

## Vue2 与 Vue3 的 Promise 差异

- **Vue2**：Promise 化后 then 收到的是 `[err, res]` 数组，catch 拿不到错误（被内部拦截）。
- **Vue3**：then 收到成功结果，catch 收到失败。  
若需统一行为，可在 main.js 中用 `uni.addInterceptor` 的 `returnValue` 对 Promise 做一层封装（详见官方「API Promise 化」文档）。

## 能力检测

使用 `uni.canIUse(api/回调/参数/组件)` 判断当前版本是否支持某 API 或能力。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/README
-->
