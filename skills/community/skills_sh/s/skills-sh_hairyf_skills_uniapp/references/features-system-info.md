---
name: features-system-info
description: uni-app 系统信息 getSystemInfo、getDeviceInfo、getWindowInfo、getAppBaseInfo
---

# 系统信息

uni-app 将系统信息分为 device、os、rom、host、uni、app 等层级。推荐使用拆分后的 API，微信小程序上直接使用 `uni.getSystemInfo` 会产生警告。

## uni.getSystemInfo(OBJECT) / uni.getSystemInfoSync()

异步/同步获取系统信息。返回内容较多：screenWidth、screenHeight、windowWidth、windowHeight、statusBarHeight、safeArea、safeAreaInsets、deviceId、deviceType、osName、osVersion、uniPlatform、appVersion 等。各端字段与含义见官方「系统信息」文档。

## 拆分 API（推荐）

- **uni.getDeviceInfo**：设备信息（deviceId、deviceType、deviceBrand、deviceModel 等）。
- **uni.getWindowInfo**：窗口信息（windowWidth、windowHeight、statusBarHeight、safeAreaInsets 等）。
- **uni.getAppBaseInfo**：应用基础信息（appId、appName、appVersion、appVersionCode 等）。
- **uni.getAppAuthorizeSetting** / **uni.getSystemSetting**：授权与系统设置。

按需调用可避免获取过多字段，并符合小程序最新规范。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/system/info
- https://uniapp.dcloud.net.cn/api/system/getDeviceInfo
- https://uniapp.dcloud.net.cn/api/system/getWindowInfo
- https://uniapp.dcloud.net.cn/api/system/getAppBaseInfo
-->
