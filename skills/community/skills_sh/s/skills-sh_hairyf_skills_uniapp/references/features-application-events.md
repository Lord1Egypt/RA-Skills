---
name: features-application-events
description: uni-app 应用级事件 onPageNotFound、onError、onAppShow、onAppHide
---

# 应用级事件

通过 `uni.on*` 监听，与 App.vue 中生命周期回调时机一致；非 App.vue 中调用时，需在适当时机用 `uni.off*` 取消，避免重复监听。

## uni.onPageNotFound(CALLBACK)

要打开的页面不存在时触发（如通过分享卡片打开未配置的页面）。回调参数：`path`、`query`、`isEntryPage`。可在回调中**同步**重定向到有效页面；异步重定向无效。未监听且未声明 App.onPageNotFound 时，会进入客户端原生「页面不存在」页。

## uni.onError(CALLBACK)

脚本错误或 API 调用报错时触发。回调参数为错误信息字符串（含堆栈）。与 App.onError 一致。

## uni.onAppShow(CALLBACK) / uni.onAppHide(CALLBACK)

应用切前台/切后台。onAppShow 回调参数含 path、query、scene 等，各端略有差异。支付宝小程序需真机预览才能测到；勿用匿名函数否则无法 off。

## 取消监听

- **uni.offPageNotFound** / **uni.offError** / **uni.offAppShow** / **uni.offAppHide**：取消对应监听。在非 App.vue 中 on 的，应在页面卸载或业务结束时 off。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/application
-->
