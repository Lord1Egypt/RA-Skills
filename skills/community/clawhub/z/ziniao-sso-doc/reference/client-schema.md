# 客户端 Schema URL 协议

> 本文件是 ziniao-sso-doc 的 Level 2 参考文档。
> 仅在需要查阅 superbrowser:// Schema URL 的详细参数与用法时加载。

## 概述

通过 `superbrowser://` 自定义 URL 协议控制紫鸟浏览器，支持打开/关闭账号和退出程序。
调用方式有两种：

1. **浏览器链接**：在浏览器地址栏打开 `superbrowser://...`（需通过安装程序安装紫鸟）
2. **命令行**：`SuperBrowser.exe "superbrowser://..."` （需主程序路径正确）

---

## Action: OpenStrore（打开账号）

### 完整示例

```
superbrowser://OpenStrore?storeId=xxxxxxx&openapiToken=xxxxxxxxx&userId=xxxxxxx&lanuchUrl=aHR0cHM6Ly93d3cuYmFpZHUuY29t&autoopen=true&debuggPort=60001&notPromptForDownload=1&forceDownloadPath=Rjpc5a6J6KOF5YyF --disable-gpu start-maximized
```

### 必须参数

| 参数 | 说明 |
|------|------|
| storeId | 账号 ID |
| userId | 紫鸟的用户 ID（如果发生变化需要重新登录） |
| openapiToken | 鉴权 token（通过 `user-login` 接口获取） |

> 如果本地已登录紫鸟客户端，且 userId 与本地登录用户一致，openapiToken 可不传（客户端版本 v5.290 或 v6.25 以上）。

### 可选参数

| 参数 | 说明 |
|------|------|
| lanuchUrl | 将要打开的目标地址，需 Base64 编码（如 `https://www.baidu.com` → `aHR0cHM6Ly93d3cuYmFpZHUuY29t`） |
| autoopen | 设为 `true` 时自动打开 lanuchUrl 配置的地址 |
| debuggPort | 指定 debug 端口号 |
| notPromptForDownload | `1`=下载文件不弹出选择路径提示框，直接下载；`0` 或不传则弹出选择路径提示框 |
| forceDownloadPath | 设置默认下载路径，路径需 Base64 编码 |

### 命令行参数

命令参数添加在链接后面，用空格隔开，多个参数也用空格隔开。

> 添加的命令参数需要向管理员申请使用权限，否则不生效。

### 响应结果

启动紫鸟浏览器并打开对应账号。

---

## Action: exit（退出浏览器）

### 请求格式

```
superbrowser://exit
```

### 说明

退出紫鸟浏览器程序，关闭所有账号。

> 如果上次打开的程序未完全退出，下次调用打开账号将会发生异常。建议在重新打开前先调用 exit。

---

## Action: CloseStrore（关闭账号）

### 请求格式

```
superbrowser://CloseStrore?storeId=268682156400
```

### 参数

| 参数 | 说明 |
|------|------|
| storeId | 要关闭的账号 ID |

### 说明

关闭指定账号，每次只能关闭 1 个账号。如需关闭多个，需多次调用。
