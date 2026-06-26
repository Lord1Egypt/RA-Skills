---
name: features-location
description: uni-app 位置 getLocation、chooseLocation、openLocation、位置更新、createMapContext、坐标系
---

# 位置 API

## uni.getLocation(OBJECT)

获取当前经纬度、速度等。常用参数：`type`（wgs84/gcj02，gcj02 可用于 openLocation 和 map 组件）、`altitude`（是否返回高度）、`geocode`（是否解析地址，仅 App 支持且需配置）、`success`。success 返回 latitude、longitude、speed、accuracy、address（geocode 为 true 时）等。App/H5 使用 gcj02 需在 manifest 配置地图 SDK key；H5 4.24+ 需配置地图 key，见官方说明。

## uni.chooseLocation(OBJECT)

打开地图选点，用户选完后返回位置名称、地址、经纬度。success 返回 name、address、latitude、longitude 等。需用户授权；部分平台需配置地图 key。

## uni.openLocation(OBJECT)

打开内置地图查看位置。参数：latitude、longitude（必填）、name、address、scale 等。坐标系建议与 getLocation/chooseLocation 一致，统一使用 **gcj02**（国测局坐标），多端兼容。

## 位置更新（持续定位）

需先 **uni.startLocationUpdate(OBJECT)** 或 **uni.startLocationUpdateBackground(OBJECT)** 开启监听，再通过 **uni.onLocationChange(CALLBACK)** 接收位置变化；**uni.offLocationChange** 取消监听。**uni.stopLocationUpdate()** 停止监听。startLocationUpdate 仅前台接收；startLocationUpdateBackground 前后台均接收。部分平台不支持；H5/Web 4.24+ 需配置地图 key。**uni.onLocationChangeError** / **uni.offLocationChangeError** 监听/取消定位失败。

## 地图组件控制

**uni.createMapContext(mapId, componentInstance)**：创建 map 组件上下文，mapId 为 `<map>` 的 id；自定义组件内传 this。返回 **mapContext**，可调用 getCenterLocation、moveToLocation、translateMarker、includePoints、getRegion、getScale 等控制地图中心、视野、marker 等。详见官方「map」文档。

## 坐标系

- **wgs84**：GPS 原始坐标。
- **gcj02**：国测局坐标，uni-app 推荐统一使用，可与 openLocation、map 组件配合。老版 5+ 百度定位/百度地图为 bd09ll，需转换。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/location/location
- https://uniapp.dcloud.net.cn/api/location/open-location
- https://uniapp.dcloud.net.cn/api/location/location-change
- https://uniapp.dcloud.net.cn/api/location/map
-->
