---
name: features-system-device
description: uni-app 设备能力 振动、扫码、拨打电话、电量、内存警告
---

# 设备能力

## 振动

- **uni.vibrate(OBJECT)**：触发振动（HarmonyOS Next 不支持）。
- **uni.vibrateShort(OBJECT)**：短振动。
- **uni.vibrateLong(OBJECT)**：长振动（约 400ms）。

## 扫码

- **uni.scanCode(OBJECT)**：调起扫码界面。success 返回 **result**（内容）、**scanType**（barCode/qrCode 等）。可设 onlyFromCamera、scanType 等。H5 不支持。

## 拨打电话

- **uni.makePhoneCall(OBJECT)**：拨打电话。参数 **phoneNumber**（必填）。会调起系统拨号界面。

## 电量与内存

- **uni.getBatteryInfo(OBJECT)** / **uni.getBatteryInfoSync()**：获取电量信息（level、isCharging 等）。部分平台支持。
- **uni.onMemoryWarning(CALLBACK)**：监听内存告警（如系统内存不足）。**uni.offMemoryWarning** 取消监听。可用于释放缓存、提示用户。

## 其它

- **uni.addPhoneContact(OBJECT)**：添加联系人。
- **uni.onUserCaptureScreen(CALLBACK)**：监听用户截屏。部分平台支持。
- 蓝牙、NFC、陀螺仪、加速度计、罗盘等见官方「system」分类文档。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/system/vibrate
- https://uniapp.dcloud.net.cn/api/system/barcode
- https://uniapp.dcloud.net.cn/api/system/phone
- https://uniapp.dcloud.net.cn/api/system/batteryInfo
- https://uniapp.dcloud.net.cn/api/system/memory
-->
