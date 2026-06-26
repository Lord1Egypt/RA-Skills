---
name: features-other-apis
description: uni-app 其它常用 API getAccountInfoSync、getEnvInfoSync、getUpdateManager、navigateToMiniProgram、exit、nextTick、base64
---

# 其它常用 API

## 运行环境

- **uni.getAccountInfoSync()**：获取当前账号信息（**仅小程序**）。返回 miniProgram（appId、envVersion、version）、plugin 等。App/H5 不支持。
- **uni.getEnvInfoSync()**：获取运行环境信息（如 SDK 版本、宿主等）。各端返回字段见官方文档。

## 小程序更新与跳转

- **uni.getUpdateManager()**：获取小程序更新管理器（**仅小程序**）。可监听 onCheckForUpdate、onUpdateReady、onUpdateFailed，并调用 applyUpdate 应用新版本。
- **uni.navigateToMiniProgram(OBJECT)**：打开其它小程序。参数 appId、path、extraData 等。**uni.navigateBackMiniProgram**：返回上一个小程序。

## 应用与界面

- **uni.exit(OBJECT)**：退出当前应用。**仅 App 支持**；H5 不支持；小程序须在点击行为内调用，且部分端不支持真正退出。
- **uni.nextTick(callback)**：在下次 DOM 更新循环后执行回调，用于在数据变更后立即操作 DOM。

## 数据转换

- **uni.base64ToArrayBuffer(base64)**：Base64 字符串转 ArrayBuffer。
- **uni.arrayBufferToBase64(arrayBuffer)**：ArrayBuffer 转 Base64 字符串。

## 调试与配置

- **uni.getExtConfig(OBJECT)** / **uni.getExtConfigSync()**：获取第三方平台自定义的扩展配置。
- **uni.setEnableDebug(OBJECT)**：设置是否打开调试（小程序等）。

## 组件上下文

- **uni.createWebviewContext(webviewId, component)**：创建 web-view 组件的上下文，用于与 web-view 内页通信（如 postMessage、evalJS 等）。**仅 HarmonyOS 支持**；其它端与 web-view 通信见官方「web-view」组件文档。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/other/getAccountInfoSync
- https://uniapp.dcloud.net.cn/api/other/getEnvInfoSync
- https://uniapp.dcloud.net.cn/api/other/update
- https://uniapp.dcloud.net.cn/api/other/open-miniprogram
- https://uniapp.dcloud.net.cn/api/exit
- https://uniapp.dcloud.net.cn/api/ui/nextTick
- https://uniapp.dcloud.net.cn/api/base64ToArrayBuffer
- https://uniapp.dcloud.net.cn/api/arrayBufferToBase64
- https://uniapp.dcloud.net.cn/api/create-webview-context
-->
