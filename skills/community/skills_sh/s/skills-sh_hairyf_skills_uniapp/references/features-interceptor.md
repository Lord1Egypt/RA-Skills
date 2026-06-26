---
name: features-interceptor
description: uni-app API 拦截器 addInterceptor、removeInterceptor
---

# 拦截器

对指定 API 的调用进行拦截与改写，仅支持**异步接口**（不支持 *Sync、create*、*Manager）。

## uni.addInterceptor(apiName, OBJECT)

- **apiName**：要拦截的 API 名称，如 `'request'` 即拦截 `uni.request()`。
- **OBJECT**：`invoke`（调用前）、`returnValue`（调用后处理返回值）、`success`/`fail`/`complete`（回调拦截）。

常见用途：请求前统一改 url、加 header；请求后统一改返回 data；或对返回值做 Promise 封装（如 Vue2/Vue3 Promise 格式统一）。

## uni.addInterceptor(OBJECT)

不传 apiName 时，对**所有**异步 API 生效，通常只写 `returnValue`，用于统一封装 Promise 等。

## uni.removeInterceptor(apiName)

移除对某 API 的拦截。

## 注意

- uniCloud 请求云端（callFunction、uploadFile 等）也会走 uni.request，拦截器内注意不要误伤。
- 仅异步 API 可被拦截。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/interceptor
-->
