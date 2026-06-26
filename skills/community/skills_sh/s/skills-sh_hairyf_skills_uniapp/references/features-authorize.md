---
name: features-authorize
description: uni-app 授权与设置 authorize、getSetting、openSetting、scope 列表
---

# 授权与设置

## uni.authorize(OBJECT)

提前向用户发起授权请求（如位置、相册、录音等）。用户已授权则直接成功；已拒绝则进入 fail，可引导至 openSetting。**仅小程序支持**；App 需用原生权限方案或插件（如权限判断插件）。参数：`scope`（必填，见下方）、success/fail/complete。scope 需在 manifest 配置 permission 的，要一并配置。

### 常用 scope

| scope | 对应能力 |
|-------|----------|
| scope.userInfo | getUserInfo 用户信息 |
| scope.userLocation | getLocation、chooseLocation 位置 |
| scope.record | 录音 |
| scope.writePhotosAlbum | 保存到相册 |
| scope.camera | 摄像头 |
| scope.address | chooseAddress 通信地址 |
| scope.invoiceTitle | chooseInvoiceTitle 发票抬头 |

## uni.getSetting(OBJECT)

获取用户当前授权与设置。success 返回 authSetting（各 scope 的授权状态）等。用于判断某权限是否已开启。

## uni.openSetting(OBJECT)

打开小程序设置页，用户可修改授权。用户拒绝某权限后，部分端无法再次弹出授权框，需引导用户点击按钮后调用 openSetting 打开设置页自行开启。

## 流程建议

需要某权限前先 getSetting 判断；未授权则调用 authorize；若用户拒绝，提示后通过 button open-type="openSetting" 或调用 openSetting 打开设置页。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/other/authorize
- https://uniapp.dcloud.net.cn/api/other/setting
-->
