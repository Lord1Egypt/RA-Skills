---
name: features-ui-prompt
description: uni-app 交互反馈 showToast、showLoading、showModal、showActionSheet
---

# 交互反馈

## uni.showToast(OBJECT)

消息提示框。常用参数：`title`（必填）、`icon`（success/error/loading/none 等）、`duration`（默认 1500ms）、`mask`（是否防触摸穿透）。部分平台 `icon` 为 success/error 时 title 有长度限制；`icon: 'none'` 可多行。App 可设 `position`（top/center/bottom）。关闭用 `uni.hideToast()`。

## uni.showLoading(OBJECT)

Loading 提示，需主动调用 `uni.hideLoading()` 关闭。参数：`title`（必填）、`mask`（默认 false）。同一时间只存在一个 showLoading；showToast 会隐藏 showLoading。

## uni.hideToast() / uni.hideLoading()

隐藏对应提示框。

## uni.showModal(OBJECT)

模态弹窗，带确定/取消。参数：`title`、`content`、`showCancel`、`cancelText`、`confirmText`、`success`（回调中 `res.confirm` 为 true 表示点击确定）。可用于二次确认、简单提示。

## uni.showActionSheet(OBJECT)

从底部弹出菜单列表。参数：`itemList`（字符串数组）、`itemColor`、`success`（`res.tapIndex` 为点击项索引）。取消或遮罩点击时 `res.cancel` 为 true。

## 使用注意

- 部分小程序对 title 长度、icon 类型有平台差异，见官方「prompt」文档。
- App 端需更多 toast 能力可用 plus.nativeUI.toast。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/ui/prompt
-->
