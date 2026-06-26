---
name: features-network
description: uni-app 网络状态 getNetworkType、onNetworkStatusChange、offNetworkStatusChange
---

# 网络状态

## uni.getNetworkType(OBJECT)

获取当前网络类型。success 返回 **networkType**：wifi、2g、3g、4g、5g、ethernet（App）、unknown、none。小程序端为**同步**接口，其它平台为异步；不传回调则返回 Promise。

## uni.onNetworkStatusChange(CALLBACK)

监听网络状态变化。回调参数：isConnected、networkType。需在适当时机 **uni.offNetworkStatusChange(CALLBACK)** 取消监听，避免泄漏。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/system/network
-->
