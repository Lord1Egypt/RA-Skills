---
name: features-launch-options
description: uni-app 启动参数 getLaunchOptionsSync、getEnterOptionsSync、path/query/scene
---

# 启动参数

## uni.getLaunchOptionsSync()

**同步**获取本次启动时的参数，与 **App.onLaunch** 回调参数一致。适用场景：在非 App.vue 中需要拿到启动 path、query、scene 等。返回：path（启动页路径）、scene（场景值）、query（启动 query 对象）、referrerInfo（来源信息）、channel/launcher（App 渠道与启动来源）等，各端字段见官方文档。App 3.4.10+、Web（Vue2 3.5.1+ / Vue3 3.2.13+）、各小程序支持；京东/百度等部分端不支持。

## uni.getEnterOptionsSync()

**同步**获取启动时的参数。与 getLaunchOptionsSync 区别：**小程序**冷启动时与 onLaunch 一致，**热启动**时与 onShow 一致；App/Web 与 onLaunch 一致。返回字段同 getLaunchOptionsSync。部分小程序不支持，见官方「getEnterOptionsSync」兼容表。

## 常见字段

- **path**：启动页面路径（代码包路径）。
- **query**：启动时的 query 对象，如从链接 `pages/detail/detail?id=1` 打开则 query 为 `{ id: '1' }`。
- **scene**：场景值，各端含义见各平台文档；App/Web 恒为 1001。
- **referrerInfo**：来源小程序/应用信息（appId、extraData 等）。

<!--
Source references:
- https://uniapp.dcloud.net.cn/api/getLaunchOptionsSync
- https://uniapp.dcloud.net.cn/api/getEnterOptionsSync
-->
