---
name: core-subpackages
description: uni-app 分包配置 subPackages、preloadRule、主包与分包划分
---

# 分包配置

小程序有体积与资源加载限制，通过分包可优化下载与启动。主包放默认启动页、TabBar 页及公共资源；分包按 pages.json 划分，进入分包页时再下载该分包。**H5 不支持** subPackages。

## subPackages

在 pages.json 中配置，值为数组，每项为一个子包：

| 属性 | 类型 | 必填 | 说明 |
|------|------|------|------|
| root | String | 是 | 分包根目录 |
| name | String | 否 | 分包别名，preloadRule 中可用 |
| pages | Array | 是 | 分包页面列表，path 为 root 下的相对路径 |

分包内 pages 的 path 是**相对 root 的路径**，不是项目根路径。分包下可有独立 `static` 目录。

## 主包与分包

- 主包：默认启动页、tabBar 页、以及各分包共用的资源/JS。
- 分包：按业务划分，用户进入分包内页面时再下载。各端分包大小与总包限制见官方文档（如微信主包+分包总 20M、单包 2M 等）。

## preloadRule

分包预下载。进入某页面时，自动预下载指定分包，加快后续进入速度。key 为页面路径，value 为配置：

- **packages**：预下载的 root 或 name 数组，`__APP__` 表示主包。
- **network**：可选 `wifi`（仅 WiFi）或 `all`。App 分包预载时网络规则无效。

支持 preloadRule 的平台：微信、QQ、抖音、支付宝、京东等小程序；App 分包同样支持（2.7.12+ vue2 也兼容分包，用于启动提速，需在 manifest 中开启）。

## App 分包

App 默认整包。2.7.12+ 可在 pages.json 中配置分包，并在 manifest 的 app 优化中开启分包，用于首页为 vue 时的启动提速，详见官方「manifest app 优化」文档。

<!--
Source references:
- https://uniapp.dcloud.net.cn/collocation/pages?id=subPackages
- https://uniapp.dcloud.net.cn/collocation/pages?id=preloadrule
-->
