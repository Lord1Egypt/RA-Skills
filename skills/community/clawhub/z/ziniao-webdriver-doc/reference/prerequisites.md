# 前置条件与排障

> 本文件是 ziniao-webdriver-doc 的 Level 2 参考文档。
> 仅在需要了解权限开通、账号配置、常见问题排查时加载。

## 概述

使用紫鸟 WebDriver 前需完成权限开通和环境准备。本文档覆盖权限申请、账号配置和常见问题排查。

## 1. 开通 WebDriver 权限

首次使用 WebDriver 时，需先在紫鸟开放平台开通权限。

详细步骤见官方文档：[如何开通webdriver权限](https://open.ziniao.com/docSupport?docId=99)

## 2. 客户端版本要求

| 操作系统 | 最低版本 |
|---------|---------|
| Windows | 紫鸟 V5 (5.X.X.X) 或 V6 (6.16.0.126+) |
| macOS | 紫鸟 V6 (6.15.0.44+) |
| Linux | 紫鸟 V6 (6.25.3.3+) |

## 3. 环境准备清单

### 3.1 关闭主进程

启动 WebDriver 前**务必**确保紫鸟浏览器主进程已完全关闭，避免端口占用或冲突。

### 3.2 清理残留进程

紫鸟启动失败或异常退出后，可能残留多个子进程（主进程 + 内核进程），不清理直接重启会导致端口占用、反复失败。**每次启动前和失败后重试前，都必须执行清理。**

已知的紫鸟相关进程名：`ziniao`、`ZiNiao`、`ziniao.exe`、`ZiNiaoBrowser` 等（不同版本命名可能不同，建议用模糊匹配）。

清理命令：

```bash
# Windows (PowerShell)
Get-Process | Where-Object { $_.ProcessName -match 'ziniao|ZiNiao' } | Stop-Process -Force

# macOS / Linux
pkill -f ziniao || true
```

验证清理结果：

```bash
# Windows (PowerShell) — 应无输出
Get-Process | Where-Object { $_.ProcessName -match 'ziniao|ZiNiao' }

# macOS / Linux — 应无输出
pgrep -f ziniao
```

### 3.3 创建自动化专用账号

- 创建专用的自动化成员账号（命名建议：`自动化_Robot`）
- 正式使用前验证该账号能否正常登录紫鸟浏览器客户端

### 3.4 配置账号权限

**问题场景**：自动化账号登录后无法获取店铺列表。

**解决方案**：
1. 登录企业管理后台
2. 检查该账号的权限配置
3. 授予查看对应账号/店铺的权限
4. 建议新建包含此权限的自定义角色并分配给自动化账号

### 3.5 超时设置

将所有 HTTP 请求的超时时间设为 **120 秒或以上**，因为启动店铺环境可能耗时较长。

### 3.6 系统资源管理

- 启动店铺窗口 CPU 消耗较大
- 根据设备配置合理控制并发启动数量
- 建议错开各任务的启动时间，避免瞬时负载过高

### 3.7 ChromeDriver 版本管理

> **关键：紫鸟内核版本 ≠ 系统 Chrome 版本。** 必须根据 `startBrowser` 返回的 `core_version` 匹配 ChromeDriver，不能使用系统 Chrome 对应的版本。

**匹配规则：**
- `core_version` 格式为 `X.Y.Z.W`（如 `119.1.0.16`），取第一段 `X` 作为大版本号
- 下载该大版本号对应的 ChromeDriver（如大版本 `119` → ChromeDriver 119.x）

**下载地址：**
- Chrome for Testing：https://googlechromelabs.github.io/chrome-for-testing/
- JSON API（便于自动化脚本解析）：https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json

**本地缓存建议：**

```
chromedriver_cache/
├── 119/
│   └── chromedriver.exe    # 对应 core_version 119.x
├── 120/
│   └── chromedriver.exe    # 对应 core_version 120.x
└── ...
```

自动化脚本应实现以下逻辑：
1. 从 `startBrowser` 响应中提取 `core_version` 大版本号
2. 检查缓存目录 `chromedriver_cache/{major_version}/` 是否存在
3. 若不存在，从 Chrome for Testing 下载对应版本并解压到缓存目录
4. 使用缓存中的 ChromeDriver 路径连接 Selenium

## 4. 通信注意事项

1. 请求/响应均为 JSON 格式，收发消息统一 UTF-8 编码
2. HTTP 模式下超时时长必须 ≥120 秒
3. 调用任何接口后务必检查 `statusCode`（0 表示成功），**出错时优先读取 `err` 字段获取中文错误描述**，这是最有价值的排障信息
4. **启动后必须首先调用 `updateCore` 接口**（需携带凭据），否则打开店铺可能出现内核缺失
5. **务必确保 HTTP 客户端以 UTF-8 解码响应体**，否则 `err` 中的中文会乱码，严重影响错误定位（Python `requests` 库需设置 `response.encoding = 'utf-8'`）
6. 所有标记"需凭据"的接口（`updateCore`、`getBrowserList`、`startBrowser`、`stopBrowser`、`ClearOnline`）每次调用都必须携带 company/username/password

## 5. 常见问题

| 现象 | 可能原因 | 解决方案 |
|------|---------|---------|
| 连接接口失败 | 客户端未启动完成 | 轮询 updateCore 直到连接成功 |
| getBrowserList 返回 -10003 | 未开通权限或未关闭登录验证 | 检查权限开通状态 |
| getBrowserList 返回 -10013 | 新设备未授权 | 调用 applyAuth 进行设备授权 |
| 店铺列表为空 | 账号无店铺权限 | 在企业管理后台配置角色权限 |
| startBrowser 返回 -10006 | 上次启动未完成 | 等待或调用 stopBrowser 后重试 |
| startBrowser 返回 7 | 内核缺失 | 确保先调用 updateCore 等待成功 |
| Selenium 连接失败 | ChromeDriver 版本不匹配 | 根据 core_version 下载匹配版本 |
| 请求超时 | 超时设置过短 | 设置超时 ≥120 秒 |
| 多账号冲突 | 端口/缓存冲突 | V5 使用 `--multip` + `--enforce-cache-path` |
| updateCore 返回错误 | 未携带凭据（company/username/password） | 所有需凭据的接口必须携带完整凭据 |
| err 字段内容乱码 | HTTP 响应体未以 UTF-8 解码 | 设置 `response.encoding = 'utf-8'` 或用 `response.content.decode('utf-8')` |
| 重启失败 / 端口占用 | 上次失败后残留紫鸟进程 | 清理所有紫鸟相关进程后重试（见§3.2） |
| Selenium 连接失败（版本不匹配） | 使用了系统 Chrome 对应的 ChromeDriver | 必须根据紫鸟 `core_version` 大版本号下载匹配的 ChromeDriver（见§3.7） |

## 6. 技术支持

如在对接过程中遇到问题，可通过以下渠道获取支持：
- 微信添加紫鸟生态管家，备注 "紫鸟webdriver"
- 官方 FAQ：https://open.ziniao.com/docSupport?docId=257
