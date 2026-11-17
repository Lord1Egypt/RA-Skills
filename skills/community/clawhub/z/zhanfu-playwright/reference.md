# 站斧 WebDriver API 参考

> 模块固定为 `WebDriverModule`，通过 HTTP 服务调用。本文与官方《站斧 WebDriver 接口文档》对齐。

HTTP 入口：`POST http://127.0.0.1:{api_port}`，Body 为 JSON。

**默认 API 端口**：`12678`（优先）。Skill 目录 [`api_port.json`](api_port.json) 记录上次成功端口与安装目录；任务开始先探测该端口（用 `GetBrowserList`，**禁止**用 `LoadSuccess` 判断）。无响应或被非站斧占用 → 空闲端口冷启动并写回；**禁止**盲扫 8081/8082 碰已运行站斧；**禁止**因 12678 被占用而要求客户先释放。

> **识别非站斧占用**：POST `GetBrowserList` 后若响应不是 `WebDriverModule` 结构（如「Electron 本地打包控制台」），视为其他服务占用 → 换空闲端口冷启动，**勿**停止占用方。

**店铺 ID 缓存**：Skill 目录 [`mall_cache.json`](mall_cache.json) 记录 `mall_name` → `mall_id` 映射。需要 `mall_id` 时**先读缓存**，未命中再 `GetMallByName` 并写回；`GetBrowserList` 返回的 `mall_list` 亦应批量写入缓存。

**打开意图配置**：Skill 目录 [`opening_malls.json`](opening_malls.json) 记录客户已下达「打开」指令的店铺名。关店 / 关站斧时清理。OpenBrowser 前用 `GetBrowserWebDriver` **只请求 1 次、超时 5s**；超时仍执行 `OpenBrowser`。

**请求方式**：阶段 A **优先 Python `requests`（`timeout=1.5`）**；**禁止**为同一探测在 PowerShell/curl/Python 间换工具试错；**禁止** Windows `curl` 手工转义 JSON。

## 通用约定

### 请求结构

| 字段 | 说明 |
|------|------|
| `action` | 接口动作名 |
| `module` | 固定为 `WebDriverModule` |
| `args` | JSON 字符串，承载业务参数 |
| `browserId` | 部分接口需要的店铺 ID（与 `mall_id` 相同）；**必须为 JSON 字符串**（如 `"3514488"`），**禁止**传数字 |

### 响应结构

| 字段 | 说明 |
|------|------|
| `ret` | HTTP 分发状态码：`200` 表示请求已正常分发处理；`400` / `500` 表示异常请求或框架级错误 |
| `returnObj` | 业务返回值；结构因接口而异 |
| `action` | 回显请求动作 |
| `module` | 回显请求模块 |

框架级错误示例（`ret=500`）：

```json
{
  "ret": 500,
  "error": "未找到方法",
  "action": "XXX",
  "module": "WebDriverModule"
}
```

### 业务成功判断

| 返回类型 | 判断方式 |
|----------|----------|
| `{ success, msg, ... }` | 以 `returnObj.success` 为准（如 `Login`、`GetMallByName`、`UpdateAccount`、`GetBrowserWebDriver`） |
| `true` / `false` | 如 `OpenBrowser`：成功 `returnObj === true`，失败 `returnObj === false` |
| `null` | 如 `CloseBrowser`、`ExitClient` 成功时 `returnObj` 为 `null`；`CloseBrowser` 失败时 `returnObj === false` |

### 典型调用流程

```
Login → SetInstallPlugins（可选，仅 Windows）→ GetBrowserList / GetMallByName → CreateBrowser（可选）
→ SetDownLoadPath（可选，仅 Windows）→ GetWebDriver（Selenium 可选，Playwright 跳过）
→ OpenBrowser → GetBrowserWebDriver → 自动化操作
→ CloseBrowser → ExitClient（结束）
```

> **macOS 暂不支持**：`SetDownLoadPath`、`ClearCacheFolder`、`ClearCache`、`SetInstallPlugins`。Agent 不得在 Mac 上调用这些 action。
>
> **macOS 内核**：`KernalNumber ≤ 130` 的店铺**不支持**自动化；须提示切换到 130 以上内核（或主账号切换）并让客户**手动重启站斧**。

## 启动站斧

**Windows**（**四项缺一不可，禁止减少/省略任一参数**）：

```
站斧.exe --multip --run_type=web_driver --ipc_type=http --httpport={api_port}
```

| 参数 | 可否省略 |
|------|----------|
| `--multip` | **否** |
| `--run_type=web_driver` | **否** |
| `--ipc_type=http` | **否** |
| `--httpport={api_port}` | **否**（值可变，键不可少） |

**macOS**（**四项缺一不可，禁止减少/省略任一参数**，与 Windows 相同；用 `open -a` 启动）：

```
open -a /Applications/站斧.app --args --multip --run_type=web_driver --ipc_type=http --httpport={api_port}
```

也可：`open -a 站斧 --args --multip --run_type=web_driver --ipc_type=http --httpport={api_port}`

| 参数 | 可否省略 |
|------|----------|
| `--multip` | **否** |
| `--run_type=web_driver` | **否** |
| `--ipc_type=http` | **否** |
| `--httpport={api_port}` | **否**（值可变，键不可少） |

`{api_port}` = `get_available_port(首选)`，首选默认 `12678`（占用则递增）。

关闭旧进程：

- Windows：`taskkill /f /t /im 站斧.exe`
- macOS：`killall 站斧`

- **禁止减少启动参数**（Windows / macOS 均不得去掉 `--multip` / `--run_type` / `--ipc_type` / `--httpport` 任一）
- `run_type` 必须为 `web_driver`
- `ipc_type` 必须为 `http`
- 冷启动端口写入 Skill 目录 `api_port.json`

### 查找站斧（冷启动前）

**先读** `api_port.json` 的 `install_dir`，验证有效则直接用；无效再按 OS 顺序尝试，命中即停；**禁止**全盘搜索。

#### Windows

0. **`api_port.json` 的 `install_dir`**（本地缓存，优先；验证 `{install_dir}\站斧.exe`）
1. **桌面快捷方式（仅文件名含「站斧」）**：在用户桌面与公共桌面查找 `站斧.lnk`、`站斧浏览器.lnk`、`*站斧*.lnk`；解析 `TargetPath` 所在目录，取该目录下 `站斧.exe`（或目标本身即为 `站斧.exe`）。**不得**解析文件名不含「站斧」的快捷方式。
2. `%LOCALAPPDATA%\Programs\ZhanFu\站斧.exe`
3. `C:\Program Files\ZhanFu\站斧.exe`
4. **向客户索要** `folder_path`：**快捷方式与常见目录均未命中时必须停止询问客户**，禁止猜路径或全盘搜索

#### macOS

0. **`api_port.json` 的 `install_dir`**（须为存在的 `站斧.app`，或目录内含 `站斧.app`）
1. `/Applications/站斧.app`
2. `~/Applications/站斧.app`
3. **向客户索要** `.app` 路径；**禁止**全盘 `mdfind` / `find`

**任一顺序命中后**：立即写入 `api_port.json` 的 `install_dir`。客户提供路径后按 OS 验证再写入。

## 端口探测（阶段 A 第一步）

1. 读 `api_port.json` 的 `api_port`；无文件则用 `12678`
2. 对该端口 POST `GetBrowserList`（正确 JSON，单次）
3. **确认为站斧 WebDriver** 且能取到 `mall_list` → **站斧已打开**，复用，刷新 `api_port.json`
4. **确认为站斧 WebDriver** 但取不到 `mall_list` → 可能未登录；**禁止冷启动**，走登录提示
5. **非站斧 HTTP**（如 Electron 控制台）或 **连接拒绝/超时** → **立刻清空 `opening_malls.json`** → 查安装路径 → 杀站斧进程（勿停占用方）→ **`get_available_port(首选)` 空闲端口冷启动** → 写 `api_port.json`

> **禁止**用 `CheckClientOpen` / `LoadSuccess` / `LoadFailed` 判断站斧是否已打开。
> **禁止**因 12678 被占用而要求客户先停掉其他服务。

## 打开店铺 / 关闭店铺（HTTP 正常则不重启）

> **同义**：「战斧」=「站斧」。客户发「打开战斧 / 关闭战斧 / 重启战斧」按「打开站斧 / 关闭站斧 / 重启站斧」执行。

| 客户意图 | `GetBrowserList` 确认为站斧 / 有响应 | 动作 |
|----------|--------------------------------------|------|
| 打开店铺 | 是（站斧 WebDriver） | **不重启**；写入 `opening_malls.json` → resolve mall_id → `GetBrowserWebDriver` **单次 5s** 判是否已开（超时仍 `OpenBrowser`）→ 已开则询问是否关闭 → 未开则 `OpenBrowser` |
| 关闭店铺 | 是 | **不重启**；resolve mall_id → `CloseBrowser` → 从 `opening_malls.json` 去掉该店；**勿**调用 `ExitClient`（除非客户明确要求退出站斧） |
| 关闭站斧 / 关闭战斧 | — | `ExitClient` → **清空** `opening_malls.json` |
| **打开站斧** / **打开战斧** | 否（无响应或非站斧占用） | **立刻清空 `opening_malls.json`** → 查安装目录 → **空闲端口**冷启动 → 站斧就绪后再写店铺名/开店 |
| 打开 / 关闭 | 否（无响应或非站斧占用） | **立刻清空 `opening_malls.json`** → 空闲端口冷启动后再走上述 HTTP 流程 |

**已打开 + 客户要求打开**：询问「是否需要关闭店铺？」；确认关闭 → `CloseBrowser` → 清理配置 → 再视客户意愿 `OpenBrowser`。

**客户明确要求关闭**：直接 `CloseBrowser` 并清理 `opening_malls.json`，无需再问。

## CheckClientOpen（已弃用为运行态判断）

**不再用于判断站斧是否已打开**。流程以 `GetBrowserList` 能取到数据为准。接口仍可能存在于客户端，但 Agent **勿**依赖其 `LoadSuccess` / `LoadFailed`。

```json
{"action": "CheckClientOpen", "module": "WebDriverModule"}
```

## GetBrowserList

**判断站斧是否已打开 + 登录态探测（阶段 A 必调）**：冷启动或复用后**直接**调用；**轮询总计最多 8s**。`returnObj.success == true` 且 `returnObj.data.mall_list` 可解析 → **站斧已打开且已登录**；有站斧 HTTP 响应但取不到数据 → 未登录，**停止**并提示客户提供账号密码（禁止因此冷启动）；无 HTTP 响应或非站斧占用 → 站斧未打开，空闲端口冷启动。

**也可用于客户「查看店铺列表」**：按 `page` / `limit` 分页返回账号下店铺。

请求：

```json
{
  "action": "GetBrowserList",
  "module": "WebDriverModule",
  "args": "{\"page\":1,\"limit\":10}"
}
```

| args 字段 | 说明 |
|-----------|------|
| `page` | 页码，从 1 开始 |
| `limit` | 每页店铺数量 |

响应示例：

```json
{
  "action": "GetBrowserList",
  "ret": 200,
  "returnObj": {
    "success": true,
    "data": {
      "total": 669,
      "page_count": 67,
      "mall_list": [
        {
          "mall_id": 2786463,
          "mall_name": "测试WebDriver随机950317",
          "platform_name": "自定义平台",
          "ip_address": "ip",
          "created_at": "2025-12-25 17:49:55",
          "updated_at": "2025-12-25 17:49:55"
        }
      ]
    },
    "msg": ""
  },
  "module": "WebDriverModule"
}
```

| 响应字段 | 说明 |
|----------|------|
| `data.total` | 店铺总数 |
| `data.page_count` | 总页数 |
| `mall_list[].mall_id` | 店铺 ID |
| `mall_list[].mall_name` | 店铺名称 |
| `mall_list[].platform_name` | 平台名称 |
| `mall_list[].ip_address` | 绑定 IP |
| `mall_list[].created_at` / `updated_at` | 创建/更新时间 |

## Login

登录或切换账号。**会关闭所有已打开店铺**；若当前已登录目标账号，无需重复调用。`GetBrowserList` 已成功时勿重复调用。

仅使用**客户提供的**账号密码；`isboss` **固定** `true`（老板账号）。**禁止**在 Skill 或脚本中写入内测/示例账号。

请求：

```json
{
  "action": "Login",
  "module": "WebDriverModule",
  "args": "{\"username\":\"admin\",\"password\":\"***\",\"isboss\":true}"
}
```

响应：`returnObj.success`、`returnObj.msg`

## GetMallByName

按店铺名称查 `mall_id`。**仅在 `mall_cache.json` 未命中时调用**；成功后立即写入缓存。

```json
{
  "action": "GetMallByName",
  "module": "WebDriverModule",
  "args": "{\"mallName\":\"WebDriverTest\"}"
}
```

| args 字段 | 说明 |
|-----------|------|
| `mallName` | 店铺名称（也支持 `mall_name`、`name`） |

响应字段：`returnObj.data.mall_id`、`mall_name`、`platform_name`、`ip_address`、`remark`、`created_at`、`updated_at`。

## CreateBrowser

创建新店铺。`ret=200` 且 `returnObj.success=true` 表示成功；`successCount` 为成功创建数量。

请求：

```json
{
  "action": "CreateBrowser",
  "module": "WebDriverModule",
  "args": "{\"mall_name\":\"测试WebDriver随机950317\",\"mall_account\":\"test_account\",\"mall_password\":\"test_password\",\"platform\":\"自定义平台\",\"platform_url\":\"https://www.baidu.com\",\"mall_address\":\"\",\"tags\":\"\",\"authorizationMember\":\"\",\"ip_content\":\"IP\",\"browser_kernel_version\":0,\"window_ua\":\"\",\"mac_ua\":\"\",\"android_ua\":\"\",\"remark\":\"这是一个用于测试的店铺\"}"
}
```

响应示例：

```json
{
  "action": "CreateBrowser",
  "ret": 200,
  "returnObj": {
    "success": true,
    "data": {
      "errorCount": 0,
      "errorMsgData": null,
      "successCount": 1
    },
    "msg": ""
  },
  "module": "WebDriverModule"
}
```

| args 字段 | 必填 | 说明 |
|-----------|------|------|
| `mall_name` | 是 | 店铺名，**不能重复** |
| `mall_account` | 否 | 店铺账号 |
| `mall_password` | 否 | 店铺密码 |
| `platform` | 是 | 所属平台 |
| `platform_url` | 自定义平台时必填 | 如 `https://www.baidu.com` |
| `mall_address` | 否 | 店铺地址 |
| `tags` | 否 | 标签 |
| `authorizationMember` | 否 | 授权成员 |
| `ip_content` | 否 | 绑定已有设备 IP |
| `browser_kernel_version` | 否 | 不指定内核填 `0` |
| `window_ua` / `mac_ua` / `android_ua` | 否 | UA |
| `remark` | 否 | 备注 |

创建成功后需**等待列表同步**，再 `GetMallByName` 取 `mall_id` 并 `OpenBrowser`。

## UpdateAccount

根据店铺 ID（`browserId`）修改店铺登录账号与密码。`browserId` 为店铺 `mall_id`；`args.username` 对应 `mall_account`，`args.password` 对应 `mall_password`（可空字符串）。

请求：

```json
{
  "action": "UpdateAccount",
  "module": "WebDriverModule",
  "browserId": "3061488",
  "args": "{\"username\":\"admin\",\"password\":\"cyt123456A\"}"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `browserId` | string | 店铺 `mall_id` |
| `username` | string | 店铺账号（对应 `mall_account`，可空） |
| `password` | string | 店铺密码（对应 `mall_password`，可空） |

成功：

```json
{
  "action": "UpdateAccount",
  "ret": 200,
  "returnObj": {
    "success": true,
    "data": {},
    "msg": ""
  },
  "module": "WebDriverModule"
}
```

失败：

```json
{
  "action": "UpdateAccount",
  "ret": 200,
  "returnObj": {
    "success": false,
    "msg": "缺少 browserId"
  },
  "module": "WebDriverModule"
}
```

| 字段 | 说明 |
|------|------|
| `success` | 是否修改成功 |
| `msg` | 提示信息 |
| `data` | 成功时的接口返回数据 |

以 `returnObj.success` 为准；`success != true` → 立即结束并原样报告 `msg`。调用前须 resolve `mall_id`（先读 `mall_cache.json`，未命中再 `GetMallByName`）。

## OpenBrowser

根据店铺 `mall_id` 打开店铺。

```json
{
  "action": "OpenBrowser",
  "module": "WebDriverModule",
  "browserId": "3061488",
  "args": "{\"isDownLoadConfirm\":false,\"isOpenMallIndex\":true,\"isSwitchDynamicNetwork\":false}"
}
```

| 字段 | 说明 |
|------|------|
| `browserId` | 店铺 `mall_id`；**必须为 JSON 字符串**（`"3061488"`），**禁止**传数字 `3061488` |
| `isDownLoadConfirm` | 下载前是否询问每个文件的保存位置 |
| `isOpenMallIndex` | 是否默认打开店铺首页 |
| `isSwitchDynamicNetwork` | 绑定了动态 IP 的店铺，传 `true` 则切换动态网络 |

**成功**：`returnObj === true`（布尔值，非 `{success}` 对象）

**失败**：`returnObj === false`

**打开失败时**：向客户提醒检查店铺是否已**绑定 IP/设备**。

## GetBrowserWebDriver

获取店铺 CDP 端口；**也用于判断目标店铺是否已打开**（`success=true` 且 `WebDriverPort` 有值 → 已打开）。

- 客户要求**打开**且已开 → 询问是否需要**关闭店铺**；未确认不调用 `OpenBrowser` / `CloseBrowser`
- 客户要求**关闭** → 直接 `CloseBrowser`，并清理 `opening_malls.json`
- **OpenBrowser 前探测**：一律 **只请求 1 次、`timeout=5`**；超时则**仍执行 `OpenBrowser`**，不因此结束流程；禁止二次探测、禁止 15s 长超时

```json
{
  "action": "GetBrowserWebDriver",
  "module": "WebDriverModule",
  "browserId": "2786463"
}
```

> **`browserId` 必须为 JSON 字符串**（`"2786463"`），**禁止**传数字。从 API/`mall_cache` 取到的 `mall_id` 一律先 `str(mall_id)` 再写入。

需在店铺**已打开**后调用（OpenBrowser 前探测时：未开或超时则视为未确认已开）。

响应：

```json
{
  "action": "GetBrowserWebDriver",
  "ret": 200,
  "returnObj": {
    "success": true,
    "msg": "",
    "WebDriverPort": 12635,
    "MainHandle": "3020652",
    "KernalNumber": 137
  },
  "module": "WebDriverModule"
}
```

| 字段 | 说明 |
|------|------|
| `WebDriverPort` | 外部 WebDriver 开发端口（Playwright CDP 用） |
| `MainHandle` | 主窗口句柄 |
| `KernalNumber` | 内核版本；**macOS** 下若 **≤ 130** 则**不支持** Playwright 自动化，须提示客户切换到 **130 以上**内核（或主账号切换）并**手动重启站斧**后停止 |

失败示例：`returnObj.success === false`，`msg` 如「浏览器未启动」。

Playwright 使用 `WebDriverPort`：`connect_over_cdp("http://127.0.0.1:{WebDriverPort}")`

> **macOS 内核限制**：拿到 `WebDriverPort` 后进入 CDP 前，必须检查 `KernalNumber`。`KernalNumber ≤ 130` → 立即停止并提示：
>
> ```
> 当前为 macOS，店铺 {mall_name} 的内核为 {kernel}（≤130），暂不支持自动化。
> 请将该店铺切换到 130 以上内核；若无权限请让主账号切换。切换完成后请您手动重启站斧，再告诉我继续。
> ```
>
> **Windows** 无此限制。Agent **禁止**在低内核场景下自行改内核或自动重启站斧。

## CloseBrowser

关闭指定店铺浏览器。**`api_port` HTTP 正常时直接调用，勿重启站斧。**

```json
{
  "action": "CloseBrowser",
  "module": "WebDriverModule",
  "browserId": "2786463",
  "args": ""
}
```

**成功**：`returnObj === null`  
**失败**：`returnObj === false`

流程：`GetMallByName` 取 `mall_id` → `CloseBrowser`。开/关店铺均**不要**顺带 `ExitClient`。

## ExitClient

关闭站斧客户端。调用后客户端将退出，无额外业务返回值。

```json
{"action": "ExitClient", "module": "WebDriverModule", "args": ""}
```

成功：`returnObj === null`

## SetDownLoadPath

设置站斧浏览器文件下载路径。目录不存在时自动创建，成功后写入全局配置 `BrowserFileDwonPath`。

> **平台**：仅 **Windows**。**macOS 目前不支持**——Agent 须直接告知客户并停止，勿调用本接口。

```json
{
  "action": "SetDownLoadPath",
  "module": "WebDriverModule",
  "args": "{\"FilePath\": \"H:\\\\downloads\"}"
}
```

| args 字段 | 说明 |
|-----------|------|
| `FilePath` | 下载目录路径（不能为空） |

响应：`returnObj.success`、`returnObj.msg`

## ClearCacheFolder

关闭所有店铺后，清除用户数据目录（保留 `Core`、`Down`）及日志目录。不计算缓存大小，不上报进度，直接删除。

> **平台**：仅 **Windows**。**macOS 目前不支持**——Agent 须直接告知客户并停止，勿调用本接口。

```json
{
  "action": "ClearCacheFolder",
  "module": "WebDriverModule",
  "args": "{}"
}
```

响应：`returnObj.success`、`returnObj.msg`

## ClearCache

关闭指定店铺后，删除该店铺的用户数据缓存目录（`RuxWorkbench` 目录跳过）。

> **平台**：仅 **Windows**。**macOS 目前不支持**——Agent 须直接告知客户并停止，勿调用本接口。

```json
{
  "action": "ClearCache",
  "module": "WebDriverModule",
  "browserId": "2786463",
  "args": ""
}
```

响应：`returnObj.success`、`returnObj.msg`；缺少 `browserId` 时 `msg` 如「缺少 browserId」。

## SetInstallPlugins

WebDriver 模式下，设置打开店铺时默认加载的插件列表。成功后写入 `ClientGlobal.Data.InstallPlugins`，在后续 `OpenBrowser` 时生效。

> **平台**：仅 **Windows**。**macOS 目前不支持**——Agent 须直接告知客户并停止，勿调用本接口。
>
> **须在 `OpenBrowser` 之前调用**；传空数组 `[]` 表示不额外指定插件。

请求：

```json
{
  "action": "SetInstallPlugins",
  "module": "WebDriverModule",
  "args": "{\"installPlugins\":[{\"plugin_name\":\"RXMallHelper\",\"chrome_id\":\"abcdefghijklmnop\"}]}"
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `installPlugins` | array | 是 | 插件列表 |
| `installPlugins[].plugin_name` | string | 是 | 插件名称，非空字符串 |
| `installPlugins[].chrome_id` | string | 否 | 插件 ID；可省略或传空字符串 `""` |

**`chrome_id` 省略示例**：

```json
{
  "action": "SetInstallPlugins",
  "module": "WebDriverModule",
  "args": "{\"installPlugins\":[{\"plugin_name\":\"RXMallHelper\"}]}"
}
```

**`chrome_id` 传空字符串示例**：

```json
{
  "action": "SetInstallPlugins",
  "module": "WebDriverModule",
  "args": "{\"installPlugins\":[{\"plugin_name\":\"RXMallHelper\",\"chrome_id\":\"\"}]}"
}
```

**清空插件列表示例**：

> **备注**：通过自动化安装的插件，清空列表之后需要**清除店铺本地缓存**（`ClearCache`）才能生效。

```json
{
  "action": "SetInstallPlugins",
  "module": "WebDriverModule",
  "args": "{\"installPlugins\":[]}"
}
```

**清空插件并使其生效的推荐流程**（针对目标店铺）：

```
SetInstallPlugins([]) → ClearCache（browserId=mall_id）→ OpenBrowser
```

若店铺已打开，须先 `CloseBrowser` 或依赖 `ClearCache` 自动关店后再 `OpenBrowser`。

响应：`returnObj.success`、`returnObj.msg`

| 常见失败 `msg` | 说明 |
|----------------|------|
| `args 必须为 JSON 对象` | `args` 格式不正确 |
| `缺少 installPlugins 参数` | 未传 `installPlugins` 字段 |
| `installPlugins 必须为数组` | `installPlugins` 不是数组 |
| `installPlugins[n].plugin_name 必须为非空字符串` | 第 n 项插件名无效 |
| `installPlugins[n].chrome_id 必须为字符串` | 第 n 项 `chrome_id` 类型无效（传了非字符串且非空值） |

## GetWebDriver（仅 Selenium）

仅 **Selenium API** 自动化需要；Playwright / CDP **跳过**此接口。

将内核目录中的 `webdriver` 文件复制到指定目录（**不可为磁盘根目录**）。

```json
{
  "action": "GetWebDriver",
  "module": "WebDriverModule",
  "args": "{\"FilePath\": \"H:\\\\webdrivers\"}"
}
```

| args 字段 | 说明 |
|-----------|------|
| `FilePath` | 目标 webdriver 存放目录，不可为根目录 |

响应：`returnObj.success`、`returnObj.msg`

## 注意事项（文档 5.x）

1. 客户端版本要求：**Windows ≥ 5.2.12**，**macOS > 5.2.10**；安装技能时向客户说明「客户使用指南」（见 `SKILL.md`）。冷启动后 8s 内未能建立 WebDriver 通讯时，按 `SKILL.md`「通讯失败对客户话术」提示（版本无误、卡顿可延迟时可再试，请客户说「打开站斧」；**禁止**再说「WebDriver 版且不低于 5.2.12」）。
2. **首次**打开店铺会下载内核，建议客户先在站斧客户端手动打开一次；不同内核的店铺需分别手动打开一次后再自动化。
3. 同时安装普通版与 WebDriver 版时，需使用 WebDriver 版。
4. 用 `GetBrowserList` **能取到数据**判断站斧已打开；**禁止**用 `LoadSuccess` 判断。确认为站斧 WebDriver 时**勿杀进程重启**；打开/关闭店铺均继续 HTTP。仅目标端口无响应、被非站斧占用、或客户明确要求时才冷启动（**空闲端口**，优先 12678，占用则递增）。**打开站斧且探测未打开/非站斧占用时，立刻清空 `opening_malls.json`**；安装目录须按快捷方式/常见目录查找，找不到则向客户索要。**禁止**因 12678 被占用而要求客户先停掉其他服务。
5. 访问本地 HTTP 服务：单次探测 `timeout=1.5`；冷启动后**立刻轮询** `GetBrowserList`（间隔 0.5s，最多 8s），勿固定干等。`OpenBrowser` 成功后固定等待 **10s** 再取 `WebDriverPort`。
6. 自动创建店铺后再打开，中间需**等待**列表同步。
7. 客户要求**打开**但目标店铺已打开时，须询问是否需要**关闭店铺**；客户明确要求**关闭**时直接 `CloseBrowser` 并清理 `opening_malls.json`。
8. 打开店铺指令（**站斧已打开后**）写入 `opening_malls.json`；OpenBrowser 前 `GetBrowserWebDriver` **单次 5s**，超时仍 `OpenBrowser`。关店 / 关站斧 / **探测站斧未打开**时清理该配置。
9. `OpenBrowser` / OpenBrowser 后 `GetBrowserWebDriver` 失败时，提醒客户确认店铺是否已绑定 IP/设备，以及是否已手动打开过该店铺下载内核。
10. 需默认加载插件时，在 `OpenBrowser` **之前**调用 `SetInstallPlugins`；`chrome_id` 可省略或传 `""`；传 `[]` 可清空插件列表。
11. **清空插件列表**（`installPlugins: []`）后，若插件曾通过自动化安装，须再对该店铺调用 **`ClearCache`** 清除本地缓存后重新 `OpenBrowser`，清空才生效。
12. Agent 阶段 A **只用 Python requests**，禁止为通断探测切换 PowerShell/curl；杀进程后最多等 1s（Win:`taskkill` / Mac:`killall 站斧`），勿固定等 3s。
13. **macOS** 不得调用 `SetDownLoadPath` / `ClearCacheFolder` / `ClearCache` / `SetInstallPlugins`（目前不支持）。
14. **macOS** 打开/复用店铺后若 `GetBrowserWebDriver.KernalNumber ≤ 130`：立即停止自动化，提示客户切换到 **130 以上**内核（或请主账号切换），并请客户**手动重启站斧**后再继续。
15. **启动参数禁止减少**：Windows / macOS **均须四项齐全**：`--multip --run_type=web_driver --ipc_type=http --httpport=`（macOS 通过 `open -a … --args` 传入）。
16. **`OpenBrowser` / `GetBrowserWebDriver` 的 `browserId` 必须为 JSON 字符串**（如 `"3514488"`），**禁止**传数字；resolve 后一律 `str(mall_id)`。
17. 客户口误「**战斧**」一律按「**站斧**」理解（如「打开战斧」=「打开站斧」），勿当成未知指令。
