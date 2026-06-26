---
name: core-manifest
description: manifest.json 应用配置要点（应用名、版本、超时、各端配置）
---

# manifest.json 应用配置

应用配置文件，指定应用名称、图标、权限等。HBuilderX 工程在根目录，CLI 工程常见在 src 目录。

## 常用顶层配置

| 属性 | 说明 |
|------|------|
| name | 应用名称 |
| appid | 应用标识（DCloud 分配，勿随意改） |
| versionName | 版本名，如 1.0.0 |
| versionCode | 版本号，如 36 |
| description | 应用描述 |
| locale | 默认语言，见 uni.getLocale / setLocale |
| networkTimeout | 各类网络超时（request、connectSocket、uploadFile、downloadFile），单位 ms，默认 60000 |
| app-plus | App 特有（启动图、模块、分发等） |
| h5 | H5 特有 |
| mp-weixin / mp-alipay / ... | 各小程序特有 |

## networkTimeout

统一设置请求超时时间，例如：

```json
"networkTimeout": {
  "request": 60000,
  "connectSocket": 60000,
  "uploadFile": 60000,
  "downloadFile": 60000
}
```

## 平台与权限

- 微信/支付宝等小程序的 appid、密钥等写在对应 `mp-xxx` 节点，不要写在 app-plus。
- 推荐在 HBuilderX 可视化界面中配置 manifest，部分项（如证书）在打包时补全。

<!--
Source references:
- https://uniapp.dcloud.net.cn/collocation/manifest
-->
