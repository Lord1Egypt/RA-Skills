---
name: features-keyboard
description: uni-app 键盘 hideKeyboard、onKeyboardHeightChange、getSelectedTextRange
---

# 键盘 API

## uni.hideKeyboard()

隐藏已显示的软键盘；若未显示则不操作。百度小程序不支持。

## uni.onKeyboardHeightChange(CALLBACK)

监听键盘高度变化。回调参数：`res.height`（键盘高度，单位 px）。支持：App 2.2.3+、H5、微信 2.7+、支付宝 3.6.8+、QQ/快手/京东/元服务等；HarmonyOS Next 4.23+。抖音、百度、小红书等不支持。

## uni.offKeyboardHeightChange(CALLBACK)

取消监听键盘高度变化。需传入与 on 时相同的回调引用。支持范围见官方文档。在页面 onUnload 时建议取消监听，避免泄漏。

## uni.getSelectedTextRange(OBJECT)

在 **input、textarea** 等 **focus 之后**调用，可获取当前光标位置。success 返回 **start**、**end**（选中区域起止位置）。用于实现@提及、选中文字等。部分平台支持，见官方「key」文档。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/key
-->
