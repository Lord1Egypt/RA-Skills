# 核心工作流接口

> 本文件是 ziniao-webdriver-doc 的 Level 2 参考文档。
> 仅在需要查阅 applyAuth / getBrowserList / startBrowser 的请求/响应格式与状态码时加载。

## 概述

紫鸟 WebDriver 共提供 11 个 HTTP API，均为 POST 请求，JSON 格式，UTF-8 编码。
请求地址：`http://127.0.0.1:{port}`（port 为启动参数 `--port` 指定的端口）。

通用字段说明：
- `action`：接口标识（必须）
- `requestId`：全局唯一请求标识（必须）
- `statusCode`：返回状态码，`0` 表示成功
- `err`：异常信息

---

## 1. applyAuth — 申请设备授权

**请求：**
```json
{
  "company": "公司",
  "username": "用户名",
  "password": "密码",
  "action": "applyAuth",
  "requestId": "全局唯一标识"
}
```

**响应：**
```json
{
  "statusCode": "状态码",
  "err": "异常信息",
  "action": "applyAuth",
  "requestId": "全局唯一标识"
}
```

**状态码：**
| 码值 | 说明 |
|------|------|
| 0 | 成功 |
| -10000 | 未知异常 |
| -10002 | Socket参数非法 |
| -10003 | 申请流程异常 |
| -10004 | 申请失败 |

---

## 2. getBrowserList — 获取店铺列表

**请求：**
```json
{
  "company": "公司",
  "username": "用户名",
  "password": "密码",
  "action": "getBrowserList",
  "requestId": "全局唯一标识"
}
```

**响应：**
```json
{
  "statusCode": "状态码",
  "err": "异常信息",
  "action": "getBrowserList",
  "requestId": "全局唯一标识",
  "browserList": [{
    "browserOauth": "店铺ID（加密）",
    "browserName": "店铺名称",
    "browserIp": "店铺IP",
    "siteId": "店铺所属站点",
    "isExpired": false,
    "platform_id": "平台id",
    "platform_name": "平台名称"
  }]
}
```

SiteId 说明文档：https://cdn-superbrowser-attachment.ziniao.com/webdriver/doc/SiteId%E8%AF%B4%E6%98%8E20250703.txt

**状态码：**
| 码值 | 说明 |
|------|------|
| 0 | 成功 |
| -10000 | 未知异常 |
| -10002 | Socket参数非法 |
| -10003 | 登录失败（需开通webdriver权限/关闭登录验证） |
| -10004 | 获取店铺列表时服务器返回异常 |
| -10013 | 需要设备认证 |

---

## 3. startBrowser — 启动店铺窗口

连续两次调用 startBrowser 会视为重启。关闭店铺需调用 stopBrowser。

**请求：**
```json
{
  "company": "公司",
  "username": "用户名",
  "password": "密码",
  "action": "startBrowser",
  "browserOauth": "店铺ID（加密）",
  "browserId": "店铺ID（未加密，优先取此值）",
  "isHeadless": true,
  "isWaitPluginUpdate": true,
  "privacyMode": true,
  "requestId": "全局唯一标识",
  "runMode": "运行模式 1轻量/2均衡(默认)/3极速",
  "pluginIdList": "id1,id2,id3",
  "pluginIdType": 0,
  "proxyTagFiter": "name1,name2,name3",
  "cookieTypeLoad": 0,
  "cookieTypeSave": 0,
  "injectJsInfo": "{\"url\":\"http://...\",\"username\":\"用户名\"}",
  "notPromptForDownload": 1,
  "isLoadUserPlugin": true,
  "windowRatio": 100,
  "forceDownloadPath": "文件下载路径（绝对路径）",
  "preSetting": "{\"profile.managed_default_content_settings.images\": 2}"
}
```

参数说明：
- `browserOauth` / `browserId`：二选一指定目标店铺。如果直接使用 `getBrowserList` 返回的数据来打开店铺，**只需传 `browserOauth` 即可**（它已包含加密店铺标识）；仅当用户需要使用明文店铺 ID 打开时，才需要赋值 `browserId`。两者同时存在时 `browserId` 优先。
- `isHeadless`：无头模式（开启后需自行检测网络）
- `isWaitPluginUpdate`：等待插件热更新完成（仅 V5）
- `runMode`：仅 V5 支持
- `pluginIdType`：0=插件版本id，1=插件id
- `cookieTypeLoad`：固定传 0
- `cookieTypeSave`：0=默认，1=不提交
- `notPromptForDownload`：1=不弹窗，0=弹窗
- `windowRatio`：0-100，0=不控制，100=全屏
- `preSetting`：浏览器配置 JSON，支持无图模式

**响应：**
```json
{
  "statusCode": "状态码",
  "err": "异常信息",
  "action": "startBrowser",
  "browserOauth": "店铺ID",
  "requestId": "全局唯一标识",
  "LastError": "内部错误信息",
  "ip": "代理IP",
  "isDynamicIp": "是否动态IP",
  "browserPath": "允许的下载路径",
  "launcherPage": "平台默认启动页面",
  "ipDetectionPage": "IP检测页地址",
  "debuggingPort": "调试端口",
  "reportPluginId": "报表插件id",
  "duplicate": "副本标志",
  "proxyTag": "当前启动的代理标志",
  "proxyType": 5,
  "mainHandle": "窗口句柄",
  "core_version": "内核版本",
  "core_type": "内核类型",
  "coreVersion": "内核版本",
  "coreType": "内核类型",
  "downloadPath": "文件下载路径"
}
```

`proxyType` 取值：-1=错误数据，0=站群，1=云平台，2=自有IP，5=本地IP

使用 Selenium 连接时需根据 `core_type` 及 `core_version` 选取对应版本 ChromeDriver：
```java
ChromeOptions options = new ChromeOptions();
options.setExperimentalOption("debuggerAddress", "127.0.0.1:" + debuggingPort);
```

**状态码：**
| 码值 | 说明 |
|------|------|
| 0 | 成功 |
| -10000 | 未知异常 |
| -10001 | 内核窗口创建失败 |
| -10002 | Socket参数非法 |
| -10003 | 登录失败 |
| -10004 | browserOauth缺失 |
| -10006 | 上次 startBrowser 还未执行结束 |
| -10013 | 需要设备认证 |
| 1 | 初始化数据失败 |
| 2 | 当前IP无法正常使用 |
| 4 | 初始化时区失败 |
| 5 | 初始化代理失败 |
| 6 | 初始化黑白名单失败 |
| 7 | 启动内核失败 |
| 8 | 初始化浏览器个人目录失败 |
| 9 | 初始化Cookies失败 |
| 11 | 初始化浏览器设置文件失败 |
| 13 | 初始化代理信息配置失败 |

`LastError` 字段包含具体错误信息。
