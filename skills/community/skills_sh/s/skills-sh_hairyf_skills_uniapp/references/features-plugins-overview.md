---
name: features-plugins-overview
description: uni-app 登录、支付、分享、推送等插件 API 概述 login、getUserInfo、requestPayment、share、getProvider、push
---

# 登录、支付、分享与推送概述

## 登录

- **uni.login(OBJECT)**：统一封装各端登录（App 一键登录/三方、小程序内置登录等）。可传 provider（通过 **uni.getProvider** 获取）。success 返回 authResult、code 等，各端不同；小程序常用 code 换 openid/session_key。
- **uni.getUserInfo(OBJECT)** / **uni.getUserProfile(OBJECT)**：获取用户信息；部分端需用户主动触发（如 button open-type="getUserInfo"）。涉及隐私，各端策略见官方「login」文档。
- **uni.getProvider(OBJECT)**：获取服务供应商（如 oauth、payment、share），用于判断当前环境支持的登录/支付/分享方式。

## 支付

- **uni.requestPayment(OBJECT)**：调起支付（微信、支付宝等）。参数：provider、orderInfo 等，各支付方式字段不同，见官方「payment」文档。小程序端需先统一下单获取参数。

## 分享

- **uni.share(OBJECT)**：调起分享（图文、链接等）。参数：provider、type、title、href、imageUrl 等。
- **uni.shareWithSystem(OBJECT)**：使用系统分享。
- **uni.showShareMenu** / **uni.hideShareMenu**：显示/隐藏分享菜单（如右上角）。页面中可定义 **onShareAppMessage** 返回分享配置。

## 推送

- **uni.getPushClientId(OBJECT)**：获取推送客户端 ID。
- **uni.onPushMessage(callback)** / **uni.offPushMessage(callback)**：监听/取消推送消息。
- 更多见「push」「getChannelManager」「createPushMessage」等文档；与 uniCloud、uni-push 服务配合使用。

## 其它插件能力

- **uni.requestVirtualPayment**：虚拟支付（如内购）。
- **uni.requestMerchantTransfer**：商家转账用户确认。
- **uni.getFacialRecognitionMetaInfo** / **uni.startFacialRecognitionVerify**：实人认证。
- 各 API 需在对应平台申请/配置后使用，详见官方「plugins」文档。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/plugins/login
- https://uniapp.dcloud.net.cn/api/plugins/provider
- https://uniapp.dcloud.net.cn/api/plugins/payment
- https://uniapp.dcloud.net.cn/api/plugins/share
- https://uniapp.dcloud.net.cn/api/plugins/push
-->
