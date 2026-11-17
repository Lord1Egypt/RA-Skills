---
name: zhanfu-playwright
description: >-
  站斧 WebDriver 版 Playwright 自动化（Windows≥5.2.12、macOS 版本高于 5.2.10、强制有界面、通讯失败即停）。
  获取 WebDriver 端口前仅 HTTP 调用 WebDriverModule；获取端口后 CDP 执行业务。
  「战斧」同义「站斧」（如打开战斧=打开站斧）。
  适用于站斧、战斧、ZhanFu、WebDriver、Playwright、店铺自动化、小龙虾 OpenClaw RPA。
---

# 站斧 Playwright 自动化

通过站斧 WebDriver 版 **HTTP API** 控制客户端与店铺；**拿到 WebDriverPort 之后**才用 Playwright `connect_over_cdp` 做页面自动化。

**Agent 提示**：技能**首次安装**、客户问「怎么用 / 如何使用」时，**先向客户发送下方「客户使用指南」**（可摘要，不必全文照搬）。

**前置（Agent）**：站斧版本要求 **Windows ≥ 5.2.12**，**macOS > 5.2.10**；环境已安装 `playwright`、`requests`。

> **macOS 限制**：`SetDownLoadPath`、`ClearCacheFolder`、`ClearCache`、`SetInstallPlugins` **目前不支持**。客户在 Mac 上提出这些需求时，应直接说明暂不支持并停止，勿调用对应 HTTP 接口。
>
> **macOS 内核限制**：macOS **不支持 130 及以下内核**的店铺自动化。打开店铺后 `GetBrowserWebDriver` 返回的 `KernalNumber` **≤ 130** 时，**立即停止**阶段 B，按「macOS 低内核对客户话术」提示客户切换到 **130 以上**内核（或由主账号切换），并请客户**手动重启站斧**后再继续。

---

## 客户使用指南（安装技能时向客户说明）

以下内容可直接复制或摘要发给客户。

### 一、使用前准备

1. **站斧版本**：请确认站斧版本要求（**Windows ≥ 5.2.12**，**macOS > 5.2.10**）。
2. **首次打开店铺会下载浏览器内核**，耗时较长，建议您先在站斧客户端里**手动打开一次**目标店铺，等内核下载完成后再用自动化。
3. **不同店铺可能使用不同内核**。若自动化打开失败或提示内核相关错误，请先在站斧里**手动打开一次该店铺**（或与您要用的店铺**同内核**的店铺），内核就绪后再发指令。
4. 店铺须已**绑定 IP / 设备**；未绑定时打开会失败，请在站斧客户端检查店铺设备绑定。
5. **macOS 暂不支持**：设置下载目录、清除缓存（单店/全部）、设置店铺插件（`SetDownLoadPath` / `ClearCache` / `ClearCacheFolder` / `SetInstallPlugins`）。请在 Windows 上使用这些能力。
6. **macOS 内核**：自动化仅支持店铺内核 **> 130**。若提示当前内核 ≤ 130，请在站斧中将该店铺切换到 **130 以上**内核（无权限时请**主账号**切换），然后**手动重启站斧**，再发指令继续。

### 二、最常用的说法（推荐）


| 您想做什么         | 直接发送（示例）                                   |
| ------------- | ------------------------------------------ |
| 启动站斧并打开店铺     | **打开站斧打开 ztest126**（把 `ztest126` 换成您的店铺名）  |
| 仅打开店铺（站斧已在运行） | **打开店铺 ztest126**                          |
| 关闭某个店铺        | **关闭 ztest126 店铺** / **关闭店铺 ztest126**     |
| 退出站斧客户端       | **关闭站斧**                                   |
| **创建新店铺**     | **创建店铺**，并按提示提供下方参数（见「七、创建店铺」）             |
| **修改店铺账号密码**  | **修改店铺账号密码**，提供店铺名与新账号/密码（见「十二、修改店铺账号密码」） |
| **查看我的店铺列表**  | **获取店铺列表** / **列出店铺**（见「八、查看店铺列表」）         |
| **设置浏览器下载目录** | **设置下载目录到 D:\downloads**（见「十、下载与缓存」）       |
| **清除店铺/全部缓存** | **清除 xxx 店铺缓存** / **清除全部缓存**（见「十、下载与缓存」）   |
| **设置店铺默认插件**  | **设置店铺插件**，提供插件名称；插件 ID 可省略或留空（见「十一、店铺插件」） |
| **清空店铺插件列表**  | **清除默认插件列表** / **清空店铺插件**（见「十一、店铺插件」）      |


> 说法可略有不同，只要包含「打开站斧」「打开店铺」和**店铺名称**即可；站斧已在运行时，一般**不会**重启站斧，直接开/关店铺。
>
> **同义说法**：客户发「**打开战斧**」「关闭战斧」「重启战斧」等时，**等同于**「打开站斧 / 关闭站斧 / 重启站斧」——「战斧」一律按「站斧」理解，**不要**当成未知产品或要求客户改口。

### 三、首次未登录时

若提示「站斧未登录，请提供账号和密码」，请提供您的**站斧老板账号**和密码（自动化仅使用您当场提供的账号，不会使用内测账号）。

### 四、店铺已经打开时

若您要的店铺**已经在运行**，系统会先问：**是否需要关闭该店铺？** 按您的选择回复即可；不需要关闭则可直接继续后续操作。

### 五、页面自动化（进阶）

店铺打开后，可继续用自然语言描述要在**店铺浏览器里**做的事，例如：

- 「在 B 站搜索并播放某某视频」
- 「打开某网址并填写表单」
- 「抓取当前页面某某信息」

此类操作会先等设备安全检测通过（约 15 秒），再自动操作页面。

### 七、创建店铺

发送 **「创建店铺」** 或 **「打开站斧并创建店铺 xxx」**，按提示提供信息即可（须已登录站斧）。

**必填信息**


| 您需提供                    | 说明                                             |
| ----------------------- | ---------------------------------------------- |
| **店铺名** `mall_name`     | 不能与已有店铺重名                                      |
| **所属平台** `platform`     | 如「自定义平台」「Temu前台」等                              |
| **平台网址** `platform_url` | 当平台选 **「自定义平台」** 时必填，如 `https://www.baidu.com` |


**建议提供**


| 您需提供                     | 说明                                               |
| ------------------------ | ------------------------------------------------ |
| **绑定设备 IP** `ip_content` | 须是站斧里**已有设备**的 IP；不知道时可先说「从已有店铺复用 IP」；未绑定时打开可能失败 |


**选填信息**（有则提供，没有可留空）


| 字段        | 说明                             |
| --------- | ------------------------------ |
| 店铺账号 / 密码 | `mall_account`、`mall_password` |
| 店铺地址      | `mall_address`                 |
| 标签        | `tags`                         |
| 授权成员      | `authorizationMember`          |
| 浏览器内核版本   | 不指定填 **0**                     |
| 备注        | `remark`                       |


**创建成功后**：系统会等列表同步，再按店铺名查询并**打开**新店铺。若创建失败，请检查店铺名是否重复、IP 是否有效、自定义平台是否填写了网址。

**说法示例**

> 创建店铺，店铺名 test001，平台自定义平台，网址 [https://www.baidu.com，绑定](https://www.baidu.com，绑定) IP 118.x.x.x

### 八、查看店铺列表

发送 **「获取店铺列表」**、**「列出我的店铺」** 或 **「店铺列表第 1 页」** 即可。

- 系统会拉取您账号下的店铺，默认第 **1** 页、每页 **10** 条（可说「第 2 页」「每页 20 条」调整 `page` / `limit`）。
- 列表中通常包含：**店铺名**、**平台**、**绑定 IP**、**创建/更新时间** 等。
- **能正常拉到列表** = 站斧**已登录**；拉不到或报错 = 需要先登录（见「三、首次未登录时」）。

**说法示例**

> 获取店铺列表  
> 列出店铺，第 2 页，每页 20 个

### 十、下载与缓存（进阶）


| 您想做什么     | 直接发送（示例）                      |
| --------- | ----------------------------- |
| 设置浏览器下载目录 | **设置下载目录到 D:\downloads**      |
| 清除某个店铺缓存  | **清除 ztest126 店铺缓存**（会先关闭该店铺） |
| 清除全部店铺缓存  | **清除全部缓存**（会先关闭所有店铺）          |


> 清除缓存为不可逆操作，执行前系统会向您确认。
>
> **macOS 暂不支持**本节全部能力（`SetDownLoadPath` / `ClearCache` / `ClearCacheFolder`）。

### 十一、店铺插件（进阶）

发送 **「设置店铺插件」**，在**打开店铺之前**指定默认加载的插件（`SetInstallPlugins` → `OpenBrowser`）。

**您需提供**


| 字段            | 必填  | 说明                          |
| ------------- | --- | --------------------------- |
| `plugin_name` | 是   | 插件名称（非空）                    |
| `chrome_id`   | 否   | 插件 ID；**可省略**，或显式传空字符串 `""` |


可一次提供多个插件；说 **「清空店铺插件」**、**「清除默认插件列表」** 或传空列表 `[]` 表示不额外指定插件。

> **重要**：若插件曾通过自动化安装，清空列表后还须**清除该店铺本地缓存**（`ClearCache`），再重新打开店铺，清空才生效。
>
> **macOS 暂不支持** `SetInstallPlugins`（及依赖的 `ClearCache`）。

**说法示例**

> 打开站斧，设置默认插件名称为紫竹自动化插件，插件 ID 为空，再打开店铺 ztest144  
> 设置店铺插件，插件名 RXMallHelper（省略插件 ID）  
> 设置店铺插件，插件名 紫竹自动化插件，插件 ID 为空  
> 清除默认插件列表，重新打开 ztest144（会先 `SetInstallPlugins([])` → `ClearCache` → 再开店铺）

> 设置会在后续 `OpenBrowser` 时生效；若店铺已打开，需先关闭再重新打开才加载新插件。

### 十二、修改店铺账号密码

发送 **「修改店铺账号密码」** / **「改店铺账号」**，按店铺修改登录账号与密码（`UpdateAccount`）。

**您需提供**


| 字段 | 必填 | 说明 |
| ---- | --- | ---- |
| **店铺名** `mall_name`（或已有 `mall_id`） | 是 | 用于 resolve `browserId`（=`mall_id`） |
| **账号** `username` | 否 | 对应 `mall_account`；可空字符串 `""` |
| **密码** `password` | 否 | 对应 `mall_password`；可空字符串 `""` |


> 缺少账号/密码时先向客户询问，**禁止猜测**。账号与密码均可显式传空以清空对应字段。

**说法示例**

> 修改店铺 ztest126 的账号为 admin，密码为 cyt123456A  
> 修改店铺账号密码，店铺名 ztest126，账号 admin，密码留空

### 九、常见问题


| 现象      | 建议                                 |
| ------- | ---------------------------------- |
| 打开店铺失败  | 检查店铺是否已绑定 IP/设备；首次使用是否已手动开过该店以下载内核 |
| macOS 提示内核过低 | 将店铺切换到 **130 以上**内核（或请主账号切换），**手动重启站斧**后再试 |
| 提示未登录   | 提供站斧账号和密码                          |
| 站斧未启动   | 发送「**打开站斧打开 {店铺名}**」，会自动冷启动站斧再开店铺  |
| 想完全重启站斧 | 明确说「**重启站斧**」                      |
| 创建店铺失败  | 检查店铺名是否重复、IP 是否已绑定、自定义平台是否填了网址     |
| 看不到店铺列表 | 先登录站斧；或说明要查第几页、每页多少条               |


---

## 硬规矩（红线，最高优先级）

以下规则覆盖本 Skill 其他所有「等待 / 重试 / 备用方案」描述，**冲突时以本节为准**。

### 1. 获取端口前：禁止写脚本

在 `**OpenBrowser` 打开店铺并成功拿到 `WebDriverPort` 之前**：

- **禁止**新建或运行任何 `.py` / `.js` / `.sh` 等可执行脚本文件（含 `_tmp_*.py`、临时业务脚本）
- **禁止**为完成任务而编写「一次性自动化脚本」
- **只允许**调用本 Skill 提供的 **HTTP 接口**（见 [reference.md](reference.md)）或 Shell 直接发 HTTP 请求
- **允许**读写临时**数据文件**（如 `api_port.json`、`mall_cache.json`、`opening_malls.json` 状态文件），但数据文件不可执行

> **例外（内置脚本）**：打开站斧运行 [`scripts/open_zhanfu.py`](scripts/open_zhanfu.py)；打开店铺运行 [`scripts/open_mall.py`](scripts/open_mall.py)；关店 / 列表 / 关站斧 / 登录 / 创建与插件等分别运行 `close_mall.py`、`list_malls.py`、`close_zhanfu.py`、`login_zhanfu.py`、`zhanfu_ops.py`。**禁止**另写一次性脚本。阶段 B 页面自动化仍禁止落盘为业务 `.py`。

### 2. 通讯失败或关键操作报错：立即结束

出现以下情况，**马上停下并向客户报告**（`**GetBrowserList` 探测轮询**、以及「OpenBrowser 前 `GetBrowserWebDriver` **单次 5s** 超时后仍 `OpenBrowser`」除外，见下节）：

- HTTP **连不上**站斧（连接拒绝、超时、无响应）
- 除登录/运行态探测用 `GetBrowserList` 外，关键 API 返回失败（`returnObj.success == false`、缺必需字段）
- Login / GetMallByName / CreateBrowser / UpdateAccount / SetInstallPlugins / OpenBrowser（`returnObj !== true`）/ GetBrowserWebDriver 失败（**例外**：OpenBrowser **前**探测 `GetBrowserWebDriver` 超时 5s → 仍执行 `OpenBrowser`）

**禁止**：

- 反复重试同一失败操作（`GetBrowserList` 的 **8s 轮询**、以及 OpenBrowser 前 `GetBrowserWebDriver` **仅允许单次 5s，超时改走 OpenBrowser**除外）
- 全盘 / 跨盘符搜索站斧安装包（Windows：`where.exe`、`-Recurse`、glob `**\站斧.exe`；macOS：全盘 `mdfind` / `find`）
- 遍历桌面**全部** `.lnk` 或解析**文件名不含「站斧」**的快捷方式（如逐个扫 GitHub、VS Code、其他浏览器快捷方式）
- 翻代码库「研究」原因
- 写「等通讯好了再跑」的备用方案或延迟任务
- 自行换端口 / 换路径 / 换工具碰运气（**例外**：冷启动前用 `get_available_port(首选)`——首选默认 `12678`，占用则递增 `12679…`；**禁止**盲扫 8081/8082 碰已运行站斧；**禁止**因端口占用要求客户先释放）
- **减少/省略**站斧启动参数（Windows / macOS **均须四项齐全**：`--multip --run_type=web_driver --ipc_type=http --httpport=`）
- 将 `OpenBrowser` / `GetBrowserWebDriver` 的 `browserId` 传成 **JSON 数字**（必须为**字符串**，如 `"3514488"`）
- 客户仅要求**打开店铺**或**关闭店铺**时，在 `api_port` HTTP 通讯正常的情况下仍执行杀进程、冷启动或 `ExitClient`（**除非客户明确要求重启站斧**）
- 用 `CheckClientOpen` / `LoadSuccess` / `LoadFailed` **判断站斧是否已打开**（改用 `GetBrowserList`，见下）
- 在 **macOS** 上调用 `SetDownLoadPath` / `ClearCacheFolder` / `ClearCache` / `SetInstallPlugins`（**目前不支持**，应直接告知客户）
- 在 **macOS** 上对 `KernalNumber ≤ 130` 的店铺继续 `connect_over_cdp` / 页面自动化（应提示切内核并让客户手动重启站斧后停止）

### 3. 获取端口前：只能 HTTP，禁止浏览器工具

在拿到 `**WebDriverPort` 之前**：

- **只允许**向 `http://127.0.0.1:{api_port}` 发 HTTP POST（`WebDriverModule`）
- **禁止**打开系统 Chrome / Edge / Firefox
- **禁止**使用 Playwright / Puppeteer（含 `launch`、`connect_over_cdp`）
- **禁止**使用 Cursor browser MCP / CDP 浏览器工具绕开站斧

拿到端口之后，**仅允许** `playwright.chromium.connect_over_cdp("http://127.0.0.1:{WebDriverPort}")` 接管**站斧店铺浏览器**。

### 4. 工具名必须来自清单

**禁止瞎编** action、工具名、命令名。只能使用下方「接口清单」中的 `action` 名称。

#### 阶段 A — 获取端口前（仅 HTTP）


| action                | 用途                                                                     |
| --------------------- | ---------------------------------------------------------------------- |
| `GetBrowserList`      | **判断站斧是否已打开** / 探测登录态 / 列表（**能取到数据 = 站斧已打开**；**禁止**用 `LoadSuccess` 判断） |
| `Login`               | 登录（已登录则跳过；会关闭所有已开店铺）                                                   |
| `GetMallByName`       | 按名称查店铺（`mallName` / `mall_name` / `name`）                              |
| `CreateBrowser`       | 创建店铺                                                                   |
| `UpdateAccount`       | 按 `browserId`（`mall_id`）修改店铺登录账号/密码（`username`→`mall_account`，`password`→`mall_password`，可空） |
| `OpenBrowser`         | 打开店铺（成功 `returnObj===true`）                                            |
| `GetBrowserWebDriver` | 获取 WebDriverPort（须店铺已打开；也可探测店铺是否已开）                                    |
| `CloseBrowser`        | 关闭店铺（成功 `returnObj===null`）                                            |
| `ExitClient`          | 退出站斧                                                                   |
| `SetDownLoadPath`     | 设置浏览器下载目录（**仅 Windows**；macOS 不支持）                                     |
| `SetInstallPlugins`   | 设置打开店铺时默认加载的插件（须在 `OpenBrowser` 前；**仅 Windows**；macOS 不支持）             |
| `ClearCacheFolder`    | 清除全部店铺缓存（**仅 Windows**；macOS 不支持）                                      |
| `ClearCache`          | 清除单个店铺缓存（**仅 Windows**；macOS 不支持）                                      |
| `GetWebDriver`        | 仅 Selenium；Playwright **跳过**                                           |
| `CheckClientOpen`     | **不再用于判断站斧是否已打开**（勿依赖 `LoadSuccess` / `LoadFailed`）                    |


> **macOS**：客户要求下载目录 / 清缓存 / 设插件时，**立即停止**并告知「macOS 暂不支持该功能」，**禁止**调用上表标注「仅 Windows」的 action。

HTTP 格式（固定）：

```json
POST http://127.0.0.1:{api_port}
Content-Type: application/json

{
  "module": "WebDriverModule",
  "action": "<上表 action>",
  "browserId": "<mall_id 字符串，可选>",
  "args": "<JSON 字符串，可选>"
}
```

> **`browserId` 类型硬规矩**：`OpenBrowser`、`GetBrowserWebDriver`（以及同样传 `browserId` 的 `CloseBrowser` / `UpdateAccount` / `ClearCache` 等）的 **`browserId` 必须是 JSON 字符串**（如 `"3514488"`），**禁止**传数字（如 `3514488`）。从 `mall_id` 取值后一律 `str(mall_id)` 再写入请求。

站斧启动命令行参数（按操作系统）：

**Windows**（**四项缺一不可，禁止减少/省略任一参数**；`{api_port}` 为分配到的空闲端口）：

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

**禁止**减少启动参数（例如去掉 `--multip` / `--ipc_type=http`，或只留 `--httpport`）。**默认 API 端口**：首选 `12678`。冷启动前须 `get_available_port(首选)`：**若首选端口已被占用则自动用下一空闲端口（12679…）**，**禁止**因此停下来要求客户释放端口；启动成功后把实际端口写入 Skill 目录 `[api_port.json](api_port.json)`（见下节）。

#### HTTP 请求方式（阶段 A · 禁止 curl / 禁止换工具试错）

**Agent 默认只用 Python `requests`**（稳定、无引号逃逸坑）。**禁止**为同一探测在 PowerShell / curl / Python 之间来回换工具（浪费时间）。

**单次探测超时**：`timeout=1.5` 秒（够判通断，勿用 3～30s 长超时堵死）。

**推荐模板**（直接复制，勿改成复杂转义；`{api_port}` 换成 `api_port.json` 中的端口，默认 `12678`）：

```python
import requests, json
api_port = 12678  # 读自 api_port.json，无文件则用 12678
r = requests.post(
    f"http://127.0.0.1:{api_port}",
    json={"module": "WebDriverModule", "action": "GetBrowserList",
          "args": json.dumps({"page": 1, "limit": 20})},
    timeout=1.5,
)
print(r.text)
```

连接拒绝 / 超时 → 视为**站斧未打开**，立刻清空 `opening_malls.json` 并冷启动；**不要**改用 PowerShell 再探一次。

**冷启动分配空闲端口**（判定站斧未打开之后、启动之前必做；直接复制）：

```python
import socket
def get_available_port(start=12678):
    port = max(1, int(start))
    while port < 65535:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("127.0.0.1", port))
                return port
            except OSError:
                port += 1
    raise RuntimeError(f"自 {start} 起未找到可用端口")

# preferred = api_port.json 的 api_port（默认 12678）
api_port = get_available_port(preferred)
print(api_port)  # 若 12678 被占用，会得到 12679…
```

> 首选端口被占用（含非站斧服务、TIME_WAIT 等）→ **换下一空闲端口继续启动**，**禁止**要求客户先释放 12678；**禁止**盲扫 8081/8082 碰已运行站斧。

**备选（仅人工调试）** PowerShell 手动拼 JSON：

```powershell
$body = '{"module":"WebDriverModule","action":"GetBrowserList","args":"{\"page\":1,\"limit\":20}"}'
Invoke-RestMethod -Uri "http://127.0.0.1:12678" -Method Post -Body $body -ContentType "application/json"
```

**禁止** Windows `curl` 手工转义 JSON；**禁止** PowerShell `ConvertTo-Json` 嵌套 `args`。

#### 打开站斧快速路径（优先按此执行，少读少试）

客户说「打开站斧 / 打开战斧」时，在 Skill 目录运行：

```bash
python scripts/open_zhanfu.py
```

客户已提供安装路径：`--folder-path "I:\ZhanFu"`；已提供登录账号：`--username ... --password ...`。

看脚本结尾的 `RESULT_JSON=`：

| `status` | 动作 |
|----------|------|
| `already_open` / `started` / `logged_in` | 站斧已就绪；仅打开站斧则结束 |
| `need_login` | 向客户索要账号密码后带 `--username/--password` 再跑 |
| `need_install_path` | 向客户索要安装路径后带 `--folder-path` 再跑 |
| `comm_fail` | **原样**把 `msg` 发给客户，禁止重试 |

脚本内部已包含：单次 `GetBrowserList` 探测、占用换口、四项启动参数、最多 8s 轮询、写回 `api_port.json`。

#### 打开店铺快速路径

先确保站斧已开。客户说「打开店铺 xxx」时：

```bash
python scripts/open_mall.py --mall-name xxx
```

| `status` | 动作 |
|----------|------|
| `already_open` | **不要**再 OpenBrowser；把 `WebDriverPort` 告诉客户。若客户本意是「打开」且店铺已开，再问是否需要关闭 |
| `opened` | 返回 `mall_id` / `WebDriverPort` |
| `zhanfu_down` | 先跑 `open_zhanfu.py` |
| `open_failed` / `no_webdriver_port` | 停止并提醒 IP/设备绑定与内核下载 |

关闭店铺：`python scripts/close_mall.py --mall-name xxx`（成功 `returnObj === null`）。

#### 阶段 B — 拿到 WebDriverPort 之后


| 工具 / 方法                                | 用途                                |
| -------------------------------------- | --------------------------------- |
| `playwright.chromium.connect_over_cdp` | 接管站斧店铺浏览器                         |
| `scripts/check_device_security.py`     | 业务自动化前设备安全检测（Skill 内置，**仅端口拿到后**） |
| `ensure_headed_mode()`                 | 强制有界面（见 `scripts/headed_mode.py`） |


**禁止**：`playwright.chromium.launch`、`browser_navigate`（MCP）、Puppeteer `launch`。

---

## 两阶段工作流

```
阶段 A（仅 HTTP，禁止脚本 / 禁止 Playwright / 失败即停）
  [读 api_port.json → 单次 GetBrowserList 探测该端口] → 能取到数据则站斧已打开，直接继续（开/关店铺均不重启）
  → 无 HTTP 响应 / 非站斧占用 = 站斧未打开 → **立刻清空 opening_malls.json** → 查路径 → 杀站斧进程 → **get_available_port(首选)（占用则 12679…）** → 冷启动
  → 冷启动前查找站斧：api_port.json →（Windows 快捷方式/常见目录；macOS `/Applications`/`~/Applications`）；**全部找不到则停止并向客户索要安装路径**（禁止全盘搜）
  → GetBrowserList 探测运行态/登录（最多 8s；能取到数据=已打开；禁止用 LoadSuccess 判断）→ [未登录则提示 Login]
  → [SetInstallPlugins / SetDownLoadPath 可选，**仅 Windows**，须在 OpenBrowser 前；**macOS 跳过且勿调用**]
  → 打开（站斧已打开之后）：写入 opening_malls.json → resolve mall_id → GetBrowserWebDriver **单次 5s** 判是否已开（超时仍 OpenBrowser）→ OpenBrowser → GetBrowserWebDriver → **【macOS】检查 `KernalNumber`，≤130 则停并提示切内核/主账号切换 + 手动重启站斧**
  → 关闭：resolve mall_id → CloseBrowser → 从 opening_malls.json 去掉该店铺名
  → 关闭站斧：ExitClient → 清空 opening_malls.json

阶段 B（端口拿到后；macOS 且 KernalNumber≤130 禁止进入）
  connect_over_cdp → [设备安全检测 15s] → 业务 Playwright 自动化
```

```
Task Progress:
- [ ] 1. 收集客户参数（含 mall_name）
- [ ] 2. 【阶段 A】读 `api_port.json`，对**唯一目标端口**单次 `GetBrowserList`（无文件则用 **12678**）；**能取到数据 = 站斧已打开，禁止冷启动**（开/关店铺均适用；**禁止**用 `LoadSuccess` 判断）
- [ ] 3. 【阶段 A · 探测到站斧未打开】**立刻清空 `opening_malls.json`** → 查安装路径 → 杀进程（Win:`taskkill` / Mac:`killall 站斧`，最多等 1s）→ **`api_port = get_available_port(首选)`（首选被占用则递增）** → 冷启动 `--httpport={api_port}` → **立刻**轮询 `GetBrowserList`（间隔 0.5s，最多 8s）→ 写回 `api_port.json`
- [ ] 4. 【阶段 A】`GetBrowserList` 探测运行态/登录（间隔 **0.5s**，**总计最多 8s**）；能取到 `mall_list` = 已打开且已登录；仍无法确认则提示客户提供账号密码
- [ ] 5. 【阶段 A · 打开店铺 · 仅站斧已打开后】将 `mall_name` **写入** `opening_malls.json`（打开意图配置；**禁止**在站斧未打开时写入）
- [ ] 6. 【阶段 A】resolve mall_id（读 `mall_cache.json` → 未命中则 `GetMallByName` 并写缓存）/ `CreateBrowser`（失败即停）
- [ ] 7. 【阶段 A】resolve mall_id（关店则跳过 OpenBrowser 相关步骤）
- [ ] 8. 【阶段 A · 打开店铺】`GetBrowserWebDriver` **只请求一次、超时 5s** 判断是否已打开；超时/无端口则**仍执行 OpenBrowser**（禁止二次探测、禁止 15s 长超时）
- [ ] 9. 【阶段 A · 已打开】询问客户是否需要关闭店铺；未确认不操作
- [ ] 10. 【阶段 A · 需打开】OpenBrowser（失败即停）→ GetBrowserWebDriver
- [ ] 10b. 【阶段 A · macOS 内核】`GetBrowserWebDriver` 成功后若 `KernalNumber ≤ 130` → **立即停止**，按「macOS 低内核对客户话术」提示，**禁止**进入阶段 B
- [ ] 11. 【阶段 A · 关闭店铺】CloseBrowser → **从 `opening_malls.json` 去掉该店铺名**（HTTP 正常时不重启站斧）
- [ ] 12. 【阶段 A · 关闭站斧】ExitClient → **清空 `opening_malls.json`**
- [ ] 13. 【阶段 B】connect_over_cdp
- [ ] 14. 【阶段 B · 仅业务自动化】设备安全检测（15s 超时）
- [ ] 15. 【阶段 B】执行业务自动化
- [ ] 16. 收尾：CloseBrowser / ExitClient（**仅客户明确要求时** ExitClient；关店/关站斧时同步清理 `opening_malls.json`）
```

---

## 禁止无头模式

1. 站斧必须以 WebDriver 模式**有界面**启动
2. 只能 `connect_over_cdp`，禁止 `launch(headless=True)`
3. 执行 Playwright 前调用 `ensure_headed_mode()`，设置 `PLAYWRIGHT_HEADLESS=0`
4. 禁止使用 Cursor 内置 browser MCP 替代站斧浏览器

---

## 执行前：向客户收集参数

缺少必填项时先询问，**不要猜测账号密码或 IP**。

**站斧安装路径**（打开站斧 / 冷启动时）：**先读** `api_port.json` 的 `install_dir` → 无效再按操作系统查找（见「启动站斧」）。**任一方式命中后，立即把安装路径写回** `api_port.json`。**都找不到时，必须停止并向客户索要安装路径**；**禁止**全盘搜索或猜测路径。

- **Windows**：目录内需含 `站斧.exe`；客户提供后验证 `{folder_path}\站斧.exe` 存在再继续。
- **macOS**：需为 `站斧.app`（如 `/Applications/站斧.app`）；客户提供后验证 `.app` 存在再继续。

### 登录态探测与 Login

站斧启动（或复用 API）后，**必须在 8s 内**通过 `GetBrowserList` 判断站斧是否**已打开**且已登录（**禁止**用 `CheckClientOpen` / `LoadSuccess` / `LoadFailed` 判断）：

```json
{"action": "GetBrowserList", "module": "WebDriverModule", "args": "{\"page\":1,\"limit\":20}"}
```


| `GetBrowserList` 结果（8s 内）                                  | 动作                                                               |
| ---------------------------------------------------------- | ---------------------------------------------------------------- |
| `returnObj.success == true` 且能取到 `mall_list`（可解析，非 `null`） | **站斧已打开且已登录**，跳过 `Login`（`Login` 会关闭已开店铺）                        |
| 有 HTTP 响应但 `success == false`、`data=null`、无法解析 `mall_list` | 站斧进程可能在跑但**未登录** → **停止**，提示客户：**「站斧未登录，请提供账号和密码」**（**禁止**因此冷启动） |
| 连接拒绝 / 无响应 / 8s 超时仍无任何 HTTP 响应                             | **站斧未打开** → 才允许冷启动                                               |
| 客户未提供账号密码                                                  | **停止**，不猜测、不擅自登录                                                 |


**不要默认主动索要**登录信息；仅在 `GetBrowserList` 失败且后续需要操作店铺时再向客户索取。

**禁止**在 Skill、脚本或对话中保存、引用或使用任何内测/示例账号密码；**仅**使用客户当场提供的 `username` / `password` 调用 `Login`，且固定 `isboss=true`（老板账号）。

Login 请求示例：

```json
{
  "action": "Login",
  "module": "WebDriverModule",
  "args": "{\"username\":\"...\",\"password\":\"...\",\"isboss\":true}"
}
```

`Login` 返回 `success != true` → **立即结束**，原样报告 `returnObj.msg`（如密码错误）。

### 按名称打开店铺


| 参数          | 必填  |
| ----------- | --- |
| `mall_name` | 是   |


### 创建店铺


| 参数                                    | 必填       | 说明                             |
| ------------------------------------- | -------- | ------------------------------ |
| `mall_name`                           | 是        | 店铺名，不可重复                       |
| `platform`                            | 是        | 所属平台                           |
| `platform_url`                        | 自定义平台时必填 | 如 `https://www.baidu.com`      |
| `ip_content`                          | 否        | 绑定已有设备 IP（或从已有店铺复用）；未绑定时打开可能失败 |
| `mall_account` / `mall_password`      | 否        | 店铺账号密码                         |
| `mall_address`                        | 否        | 店铺地址                           |
| `tags`                                | 否        | 标签                             |
| `authorizationMember`                 | 否        | 授权成员                           |
| `browser_kernel_version`              | 否        | 不指定内核填 `0`                     |
| `window_ua` / `mac_ua` / `android_ua` | 否        | UA                             |
| `remark`                              | 否        | 备注                             |


创建成功后须等待列表同步，再 resolve mall_id → `OpenBrowser`。

### 设置店铺插件（SetInstallPlugins）

客户要求**打开店铺前加载指定插件**时，须在 `OpenBrowser` **之前**调用。

**省略 `chrome_id`**：

```json
{
  "action": "SetInstallPlugins",
  "module": "WebDriverModule",
  "args": "{\"installPlugins\":[{\"plugin_name\":\"RXMallHelper\"}]}"
}
```

`**chrome_id` 传空字符串**（客户说「插件 ID 为空」时用此写法）：

```json
{
  "action": "SetInstallPlugins",
  "module": "WebDriverModule",
  "args": "{\"installPlugins\":[{\"plugin_name\":\"紫竹自动化插件\",\"chrome_id\":\"\"}]}"
}
```


| 参数                             | 必填  | 说明                   |
| ------------------------------ | --- | -------------------- |
| `installPlugins`               | 是   | 插件数组；`[]` 表示清空/不额外指定 |
| `installPlugins[].plugin_name` | 是   | 插件名称，非空字符串           |
| `installPlugins[].chrome_id`   | 否   | 插件 ID；可省略或传 `""`     |


**清空插件列表**（`installPlugins: []`）：

```json
{
  "action": "SetInstallPlugins",
  "module": "WebDriverModule",
  "args": "{\"installPlugins\":[]}"
}
```

> 通过自动化安装的插件，**清空列表后须对该店铺调用 `ClearCache`**，再 `OpenBrowser`，清空才生效。

**清空并重新打开店铺流程**：

1. `SetInstallPlugins`（`installPlugins: []`）
2. resolve mall_id 取 `mall_id`
3. `ClearCache`（`browserId` = `mall_id`；会关闭该店铺）
4. `OpenBrowser` → 等 10s → `GetBrowserWebDriver`

`returnObj.success != true` → **立即结束**，原样报告 `returnObj.msg`。

### 设备安全检测（仅业务自动化）

客户提出**页面级自动化**（填表、抓取、播放视频等）时，阶段 B 必须先等设备安全检测成功（15s 超时）；仅启动/开店铺不需要。

超时或未成功 → 告知客户：**「没检测成功无法进行自动化」**，立即结束。

---

## 打开店铺 / 关闭店铺（意图路由 · HTTP 正常则不重启）

客户发送**打开店铺**或**关闭店铺**指令时，**一律先**读 `api_port.json` 并对 `api_port` 做单次 `GetBrowserList` 探测（**禁止**用 `LoadSuccess` 判断）。

> **口误 / 同义**：客户说「**战斧**」=「**站斧**」。例如「打开战斧」「打开战斧打开 xxx」「关闭战斧」「重启战斧」分别按「打开站斧」「打开站斧打开 xxx」「关闭站斧」「重启站斧」执行。


| 客户意图                       | `GetBrowserList` 探测        | 动作                                                                                                                                                    |
| -------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **打开店铺**                   | **能取到数据**（站斧已打开）或有 HTTP 响应 | **禁止**杀进程 / 冷启动 / `ExitClient`；将 `mall_name` 写入 `opening_malls.json` → resolve mall_id → `GetBrowserWebDriver` **单次 5s** 判是否已开 → 未开/超时则 `OpenBrowser` |
| **关闭店铺**                   | **能取到数据**或有 HTTP 响应        | **禁止**杀进程 / 冷启动 / `ExitClient`；直接 HTTP：resolve mall_id → `CloseBrowser` → **从 `opening_malls.json` 去掉该店铺名**                                           |
| **关闭站斧** / **关闭战斧** / `ExitClient`    | 任意                         | `ExitClient` → **清空 `opening_malls.json`**                                                                                                            |
| **创建店铺**                   | **能取到数据**或有 HTTP 响应        | **禁止**重启；`CreateBrowser` → 等待同步 → resolve mall_id → `OpenBrowser`（参数见客户指南「七、创建店铺」）                                                                    |
| **修改店铺账号密码**               | **能取到数据**或有 HTTP 响应        | **禁止**重启；resolve mall_id → `UpdateAccount`（`browserId`=`mall_id`，`args.username`/`password` 由客户提供，可空；见「十二、修改店铺账号密码」）                              |
| **获取店铺列表**                 | **能取到数据**或有 HTTP 响应        | **禁止**重启；`GetBrowserList`（默认 `page=1, limit=10`，可按客户指定分页）→ 展示 `mall_list`；**同时将列表中 `mall_name` → `mall_id` 写入 `mall_cache.json`**                     |
| **设置下载目录**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：`SetDownLoadPath`（`FilePath` 由客户提供）                                                                           |
| **设置店铺插件**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：`SetInstallPlugins`（须在 `OpenBrowser` 前）                                                                       |
| **清空插件列表**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：`SetInstallPlugins([])` → `ClearCache` → `OpenBrowser`                                                        |
| **清除全部缓存**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：确认后 `ClearCacheFolder` → 清空 `opening_malls.json`                                                              |
| **清除单店缓存**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：确认后 `ClearCache` → 从 `opening_malls.json` 去掉该店                                                                |
| **打开站斧** / **打开战斧** / **打开站斧打开 {店铺}** | **无响应**（站斧未打开）             | **立刻清空 `opening_malls.json`** → 查安装目录（快捷方式/常见目录找不到则**向客户索要**）→ `get_available_port(首选)`（占用则递增）→ 冷启动 → 站斧就绪后再按需写入店铺名并开店铺                                                                |
| **打开 / 关闭店铺**              | **无响应**（连接拒绝 / 超时）         | **立刻清空 `opening_malls.json`** → 才允许冷启动站斧（见「启动站斧」，含端口占用则换口）；**禁止**为关店单独重启（关店只需 HTTP，站斧未运行则先冷启动再继续 HTTP）                                                         |
| **重启站斧** / **重启战斧**                   | 任意                         | 仅当客户**明确要求**时才杀进程 + `get_available_port` 冷启动（Win:`taskkill` / Mac:`killall 站斧`）→ **立刻清空 `opening_malls.json`**                                                             |


> **核心**：开店铺、关店铺都是 **HTTP 操作**；`GetBrowserList` **能取到数据** = 站斧**已打开**，**继续 HTTP 即可**，不要「顺手」重启客户端。**禁止**根据 `CheckClientOpen` 的 `LoadSuccess` / `LoadFailed` 判断站斧是否已打开。

### 关闭店铺流程（阶段 A · 仅 HTTP）

1. 读 `api_port.json` → 单次探测 `GetBrowserList`
2. 能取到数据或有 HTTP 响应 → resolve mall_id（读 `mall_cache.json` → 未命中则 `GetMallByName` 并写缓存；失败即停）
3. `CloseBrowser`（`browserId` = 字符串形式的 `mall_id`）；成功时 `returnObj === null`，失败时 `returnObj === false`
4. **从 `opening_malls.json` 去掉该 `mall_name`**
5. **不调用** `ExitClient`（除非客户明确要求退出站斧客户端）
6. **禁止**因关店而冷启动或杀站斧进程（Win:`站斧.exe` / Mac:`killall 站斧`）

```json
{"action": "CloseBrowser", "module": "WebDriverModule", "browserId": "3514488"}
```

---

## 站斧运行态复用（读本地端口 · 单次 GetBrowserList · 禁止扫端口）

客户要求**打开店铺**、**关闭店铺**或**执行业务自动化**时，**不要默认杀进程重启站斧**，也**禁止**依次试探 8081/8082 等端口。

### 本地状态记录 `api_port.json`

路径：Skill 目录下 `[api_port.json](api_port.json)`（与 `SKILL.md` 同级）。

```json
{
  "api_port": 12678,
  "install_dir": "I:\\ZhanFu",
  "updated_at": "2026-06-17T12:00:00"
}
```


| 字段            | 说明                                                                                          |
| ------------- | ------------------------------------------------------------------------------------------- |
| `api_port`    | 站斧 HTTP API 端口（首选默认 `12678`；冷启动时若占用则写入实际分配端口）                                                                  |
| `install_dir` | 站斧安装路径：Windows 为含 `站斧.exe` 的文件夹；macOS 为 `站斧.app` 路径（如 `/Applications/站斧.app`）；**查找命中后立即写入** |
| `updated_at`  | 最近一次写入时间                                                                                    |



| 时机                                 | 动作                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| 每次任务开始                             | **先读** `api_port.json` 的 `api_port`；文件不存在则用 **12678**                                |
| 冷启动前查找站斧                           | **先读** `install_dir`：Windows 验证 `{install_dir}\站斧.exe`；macOS 验证 `.app` 存在；无效则走原始查找逻辑 |
| 原始逻辑命中安装路径                         | **立即写入** `install_dir` 到 `api_port.json`                                             |
| 客户提供路径且验证通过                        | **写入** `install_dir`                                                                 |
| `GetBrowserList` 能取到数据 / 有 HTTP 响应 | **刷新写入** `api_port`（保留已有 `install_dir`）                                              |
| 冷启动站斧成功                            | **写入** `api_port`（若有 `install_dir` 一并保留/更新）                                          |


### 单次探测（仅一个端口 · 用 GetBrowserList，禁止 LoadSuccess）

对目标端口（本地记录或 12678）发**一次** POST，Body 为正确 JSON 的 `GetBrowserList`：

```json
{"module":"WebDriverModule","action":"GetBrowserList","args":"{\"page\":1,\"limit\":20}"}
```


| HTTP / 业务结果                                   | 判定              | 动作                                                                    |
| --------------------------------------------- | --------------- | --------------------------------------------------------------------- |
| `success==true` 且能取到 `mall_list`（可解析）         | **站斧已打开**（且已登录） | 记录 `api_port`，**跳过**杀进程与冷启动                                           |
| 有 HTTP 响应体，但取不到 `mall_list` / `success=false` | 站斧进程在跑但可能未登录    | 记录 `api_port`，**禁止冷启动**；进入登录提示流程                                      |
| 有 HTTP 响应但**不是**站斧 WebDriver 结构               | **非站斧占用**       | **立刻清空 `opening_malls.json`** → 杀站斧进程（勿停占用方）→ `get_available_port(首选)` 换口冷启动 |
| **连接拒绝 / 超时 / 无响应**                           | **站斧未打开**       | **立刻清空 `opening_malls.json`** → 杀站斧进程 → `get_available_port(首选)`（占用则递增）→ 冷启动 |


> **禁止**再用 `CheckClientOpen` 的 `LoadSuccess` / `LoadFailed` 判断站斧是否已打开。「模块 undefined 未加载」等说明该端口上**已有 HTTP 服务**；若确认为站斧 WebDriver，用正确 JSON 的 `GetBrowserList` 重发即可；若是**非站斧**服务，走 `get_available_port` 换口冷启动，**不要**停占用方、**不要**要求客户释放端口。


| 场景                       | 动作                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| 站斧已打开 + **打开店铺**         | **不重启**；写入 `opening_malls.json` → resolve mall_id → 已开确认 → 未开则 `OpenBrowser`               |
| 站斧已打开 + **关闭店铺**         | **不重启**；resolve mall_id → `CloseBrowser` → 清理 `opening_malls.json`                         |
| 站斧已打开 + 阶段 B 业务          | **不重启**；`GetBrowserWebDriver` 拿端口                                                          |
| **打开站斧** / 目标端口无 HTTP 响应 | **立刻清空 `opening_malls.json`** → 查安装目录（找不到则向客户索要）→ `get_available_port(首选)` → 冷启动，写 `api_port.json` |
| 客户明确要求「重启站斧」             | 允许杀进程 + `get_available_port` 冷启动（Win:`taskkill` / Mac:`killall 站斧`），**立刻清空 `opening_malls.json`** |


> 复用已运行实例时，**直接**用 `GetBrowserList`（最多 **8s**）判断是否已打开/已登录。**无论冷启动还是复用，探测总耗时不超过约 8s**（不再先等 `CheckClientOpen` / `LoadSuccess`）。

---

## 打开意图配置 `opening_malls.json`

路径：Skill 目录下 `[opening_malls.json](opening_malls.json)`（与 `SKILL.md` 同级）。

用于记录客户**已发出「打开某店铺」指令**的店铺名；关店 / 关站斧时清理。OpenBrowser 前用 `GetBrowserWebDriver` **统一单次 5s** 探测（与是否已在列表无关）。

```json
{
  "malls": ["ztest126"],
  "updated_at": "2026-07-14T10:00:00"
}
```


| 字段           | 说明                              |
| ------------ | ------------------------------- |
| `malls`      | 客户已下达「打开」意图、且尚未通过关店/关站斧清理的店铺名列表 |
| `updated_at` | 最近一次写入时间                        |



| 时机                                                         | 动作                                     |
| ---------------------------------------------------------- | -------------------------------------- |
| 客户发送**打开店铺 / 打开站斧打开 {店铺名}**（**仅当站斧已打开之后**拿到 `mall_name`）   | **写入**该 `mall_name`（已存在则跳过）            |
| **打开站斧** / 探测到**站斧未打开**（`GetBrowserList` 无 HTTP 响应）        | **立刻清空**整个 `malls` 列表（丢弃此前写入的店铺名），再冷启动 |
| 客户发送**关闭店铺 {店铺名}** 且 `CloseBrowser` 成功                     | **去掉**该 `mall_name`                    |
| 客户发送**关闭站斧** / `ExitClient` / 冷启动重启站斧 / `ClearCacheFolder` | **清空**整个 `malls` 列表                    |
| 清除单店缓存 `ClearCache` 成功                                     | **去掉**该店铺名                             |


> `opening_malls.json` 只记店铺名，与 `mall_cache.json`（店铺 ID）无关。**禁止**在站斧未打开时写入店铺名。

---

## 本地店铺 ID 缓存 `mall_cache.json`

路径：Skill 目录下 `[mall_cache.json](mall_cache.json)`（与 `SKILL.md` 同级）。

```json
{
  "mall_map": {
    "ztest126": "2786463",
    "测试WebDriver随机950317": "2786500"
  },
  "updated_at": "2026-06-24T16:30:00"
}
```


| 字段           | 说明                                                                         |
| ------------ | -------------------------------------------------------------------------- |
| `mall_map`   | 店铺名 → 店铺 ID（`mall_id`）映射；键为**客户提供的店铺名**（与 `GetMallByName` 的 `mallName` 一致） |
| `updated_at` | 最近一次写入时间                                                                   |


### resolve mall_id（统一查 ID 流程）

凡需 `mall_id` 的操作（开/关店铺、`ClearCache`、`GetBrowserWebDriver` 等），**一律先走缓存**：

```
1. 读 mall_cache.json → mall_map[mall_name] 有值？
   ├─ 是 → 直接用该 mall_id（跳过 GetMallByName）
   └─ 否 → 调用 GetMallByName → 成功后立即写入 mall_map
2. 使用 mall_id 调用后续 API
3. 若后续 API 因店铺 ID 无效失败（如 CloseBrowser returnObj===false）：
   → 删除 mall_map 中该 mall_name 条目
   → 重新 GetMallByName 取 id 并写回缓存
   → 用新 id 重试一次（仍失败则立即结束）
```


| 时机                                                                    | 动作                                                             |
| --------------------------------------------------------------------- | -------------------------------------------------------------- |
| 开/关店铺、清缓存、取 WebDriver 等需 `mall_id`                                    | **先读** `mall_cache.json`；命中则**跳过** `GetMallByName`             |
| 缓存未命中                                                                 | `GetMallByName` 成功后**立即写入** `mall_map`                         |
| `GetBrowserList`（登录探测或客户查列表）                                          | 将 `mall_list` 中每条 `mall_name` → `mall_id` **批量写入**缓存（已有且相同则跳过） |
| `CreateBrowser` 成功后                                                   | 等待同步 → `GetMallByName` → 写入缓存                                  |
| 使用缓存 id 调用 `CloseBrowser` / `OpenBrowser` / `GetBrowserWebDriver` 等失败 | **删除**该条缓存 → `GetMallByName` 刷新 → 写回 → **仅重试一次**               |


> **注意**：`mall_cache.json` 记录的是店铺 ID，与站斧「清除店铺缓存」(`ClearCache`) 无关；清浏览器缓存**不要**清空 `mall_cache.json`。

---

## 已打开店铺的确认（OpenBrowser 前）

客户要求**打开**某店铺时：

1. **立刻**将 `mall_name` 写入 `opening_malls.json`（见「打开意图配置」；站斧须已打开）
2. resolve mall_id 拿到 `mall_id`
3. **先**调 `GetBrowserWebDriver` 判断目标店铺是否已打开——**只请求一次，超时固定 5 秒**

```json
{"action": "GetBrowserWebDriver", "module": "WebDriverModule", "browserId": "3514488"}
```

> **`browserId` 必须为字符串**（如 `"3514488"`），**禁止**传 JSON 数字。

**判定已打开**：5s 内 `returnObj.success == true` 且 `WebDriverPort` 有值。

### 探测规则（一律单次 5s，禁止加长或重试）


| 步骤                     | 规则                                                                              |
| ---------------------- | ------------------------------------------------------------------------------- |
| 次数 / 超时                | **只请求 1 次**，HTTP `timeout=5`；**禁止**先用 15s 再探测、**禁止**连打第二次                       |
| 5s 内拿到端口               | 按「已打开」处理（询问是否关闭）                                                                |
| **5s 超时 / 连接异常 / 无端口** | **视为未开**，**不要结束流程**，**直接 `OpenBrowser`** → 等 10s → 再 `GetBrowserWebDriver`（取端口） |



| 情况                         | 动作                                                                                                                                   |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 目标店铺**未打开**（含探测 **5s 超时**） | 直接 `OpenBrowser` → 等 10s → `GetBrowserWebDriver`                                                                                     |
| 目标店铺**已打开**                | **必须先询问客户**：「店铺 {mall_name} 已打开（WebDriverPort={port}），是否需要关闭店铺？」                                                                     |
| 客户确认**需要关闭**               | `CloseBrowser` → 从 `opening_malls.json` 去掉该名 → 确认关闭成功后，再询问是否重新 `OpenBrowser`；确认后再写入配置并 `OpenBrowser` → 等 10s → `GetBrowserWebDriver` |
| 客户确认**不需要关闭** / 继续使用当前店铺   | **跳过** `OpenBrowser` 与 `CloseBrowser`，直接用现有 `WebDriverPort` 进入阶段 B 或结束                                                               |
| 客户未明确表态                    | **不得**擅自 `OpenBrowser` 或 `CloseBrowser`，等待客户回复                                                                                       |


**禁止**：

- 检测到店铺已打开仍静默调用 `OpenBrowser`（会干扰客户当前页面）
- 检测到店铺已打开未经确认就调用 `CloseBrowser`
- OpenBrowser 前因 `GetBrowserWebDriver` **超时**而整流程失败退出（应改走 `OpenBrowser`）
- OpenBrowser 前对 `GetBrowserWebDriver` **重试或拉长超时**（整体只许 **1 次 × 5s**）

**与客户说「关闭店铺」的区别**：客户**明确说关闭**且 HTTP 正常 → 直接 `CloseBrowser` 并清理 `opening_malls.json`，无需再问是否关闭；客户**说打开**但检测到已开 → 才须询问是否关闭。

---

## 启动站斧（阶段 A · 仅冷启动时）

**仅当** 目标端口无 HTTP 响应，或端口上是**非站斧 WebDriver** 服务时，才执行：

1. **立刻清空 `opening_malls.json`**（打开站斧命令检测到未打开时必须清理已写入的店铺名）
2. 杀进程（按 OS；**只杀站斧，不要停掉占用端口的其他服务**）：

**Windows**：

```bat
taskkill /f /t /im 站斧.exe
```

**macOS**：

```bash
killall 站斧
```

杀进程后**最多等 1s**（可用短轮询看进程是否消失）；进程已退出则**立刻**继续，**禁止**固定干等 3s。

3. **分配空闲端口**（判定站斧未打开后必做）：`api_port = get_available_port(首选)`（首选 = `api_port.json` 的 `api_port` 或默认 `12678`）；用 `socket.bind(("127.0.0.1", port))` 探测——**能 bind = 空闲**；失败则 `port += 1` 继续。12678 被占用则自动用 12679…，**禁止**因此停下来要求客户释放端口，**禁止**盲扫 8081/8082。
4. 再以 WebDriver 参数启动（见上文接口清单；**Win/Mac 均四项缺一不可、禁止减少**；**macOS 用 `open -a`，同样带 `--multip`**），`--httpport=` 用上一步分配的端口。
5. 启动后**立刻**轮询 `GetBrowserList`（对**实际端口**，间隔 **0.5s**，总计最多 **8s**），端口/列表就绪即继续；**禁止**启动后再固定 sleep 再探测。
6. **8s 内仍无 WebDriver 通讯** → **立即停止、禁止重试**，按「通讯失败对客户话术」提示客户。

### 通讯失败对客户话术（冷启动后 8s 内无 WebDriver 通讯 · 必须原样）

冷启动后轮询 `GetBrowserList` **总计 8s 仍无 HTTP 响应 / 未能建立 WebDriver 通讯**时：

- **立即停止**，**禁止**重复尝试、换端口、再冷启动
- **必须**向客户报告以下模板（`{install_path}` 换成已确认路径，如 `I:\ZhanFu\站斧.exe` 或 `/Applications/站斧.app`）：

```
站斧启动后 8 秒内未能建立 WebDriver 通讯，已按技能规则停止操作，未重复尝试。
安装位置已确认：{install_path}。请确认站斧版本要求（Windows ≥ 5.2.12，macOS > 5.2.10）无误；若电脑因卡顿导致启动有延迟，可尝试再次打开站斧，请告诉我“打开站斧”。
```

**禁止**再说「请先手动打开站斧并确认版本为 WebDriver 版且不低于 5.2.12」；版本提醒**一律**写：**Windows ≥ 5.2.12，macOS > 5.2.10**。

### 查找站斧（冷启动前 · 禁止全盘搜索）

**必须按顺序、逐项尝试，命中即停**；**禁止** `where.exe` / `mdfind` 全盘扫、递归 glob、跨盘符搜索、翻代码库猜路径。

#### Windows


| 顺序  | 方式                                                    | 说明                                             |
| --- | ----------------------------------------------------- | ---------------------------------------------- |
| 0   | `**api_port.json` 的 `install_dir`**                   | 验证 `{install_dir}\站斧.exe` 存在则直接使用；不存在则**跳过**   |
| 1   | 桌面「站斧」快捷方式                                            | **仅**按文件名匹配含「站斧」的 `.lnk`，解析其 `TargetPath` 所在目录 |
| 2   | `C:\Users\{用户名}\AppData\Local\Programs\ZhanFu\站斧.exe` | `{用户名}` 取当前 Windows 登录名                        |
| 3   | `C:\Program Files\ZhanFu\站斧.exe`                      | 固定路径                                           |
| 4   | **向客户索要**                                             | 提示：「未找到站斧安装目录，请提供站斧安装路径（含 站斧.exe 的文件夹）」        |


#### macOS


| 顺序  | 方式                                  | 说明                                                             |
| --- | ----------------------------------- | -------------------------------------------------------------- |
| 0   | `**api_port.json` 的 `install_dir`** | 验证为存在的 `站斧.app`（或目录内含 `站斧.app`）则直接使用；无效则**跳过**                 |
| 1   | `/Applications/站斧.app`              | 系统 Applications                                                |
| 2   | `~/Applications/站斧.app`             | 用户 Applications                                                |
| 3   | **向客户索要**                           | 提示：「未找到站斧.app，请提供路径（如 /Applications/站斧.app）」；**禁止**全盘 `mdfind` |


**任一顺序命中后**：立即把该路径写入 `api_port.json` 的 `install_dir`，再冷启动。

**客户提供路径后**：

- Windows：仅检查 `{folder_path}\站斧.exe` 是否存在
- macOS：仅检查路径为 `站斧.app` 或目录内含 `站斧.app`

验证通过后**写入** `install_dir`；不存在则**立即结束**并再次提示路径无效。

#### 快捷方式解析规则（Windows 顺序 1 · 只查名为「站斧」的快捷方式）

**只查找快捷方式文件名中含「站斧」的 `.lnk`**，**禁止**遍历桌面全部快捷方式，**禁止**解析文件名不含「站斧」的 `.lnk`（无论其目标 exe 名称为何）。

查找范围：当前用户桌面 + 公共桌面（`Desktop`、`Public\Desktop`）。

**文件名匹配**（按序尝试，解析到有效 `站斧.exe` 即停）：

1. 精确名：`站斧.lnk`、`站斧浏览器.lnk`
2. 通配：`*站斧*.lnk`（**仅**文件名包含「站斧」者，如 `站斧浏览器完成版.lnk`）

对每个命中的 `.lnk`：

1. 解析 `TargetPath`（PowerShell `WScript.Shell.CreateShortcut` 或等价方式）
2. 取目标文件所在目录为 `install_dir`
3. 若 `TargetPath` 本身为 `站斧.exe` → 直接使用
4. 否则检查 `{install_dir}\站斧.exe`；存在则使用

全部快捷方式均未解析出 `站斧.exe` → 进入顺序 2（固定安装路径），**不得**改用其他命名规则的快捷方式兜底。

---

## 阶段 A 操作要点（HTTP only，失败即停）

### GetBrowserList（判断站斧是否已打开 + 登录态 · 必做 · 总计最多 8s）

**禁止**用 `CheckClientOpen` / `LoadSuccess` / `LoadFailed` 判断站斧是否已打开。冷启动或复用后**直接**轮询 `GetBrowserList`：

```json
{"action": "GetBrowserList", "module": "WebDriverModule", "args": "{\"page\":1,\"limit\":20}"}
```

- **轮询** `GetBrowserList`，间隔 **0.5s**，**总计最多 8s**
- `returnObj.success == true` **且** `returnObj.data.mall_list` 可解析（非 `null`）→ **站斧已打开且已登录**，**禁止**无故调用 `Login`；**同时将 `mall_list` 中 `mall_name` → `mall_id` 写入 `mall_cache.json`**
- 有 HTTP 响应但 **8s 内**仍 `success=false`、`data=null`、无法解析 `mall_list` → **停止**，提示客户：**「站斧未登录，请提供账号和密码」**；拿到凭证后再 `Login`（**禁止**因此冷启动）
- 连接拒绝 / 无响应 → **站斧未打开**，走冷启动
- 客户未提供账号密码 → **停止**，不猜测、不擅自登录
- **单次请求** `timeout=1.5`；Agent **只用 Python requests**，禁止为通断探测切换 PowerShell/curl

> `CheckClientOpen` **不再作为流程步骤**；勿等待 `LoadSuccess`。

### Login

仅在 `GetBrowserList` 表明未登录且**客户已提供**账号密码时调用；`isboss` **固定** `true`。**禁止**使用内测或历史会话中的账号。`success != true` → **立即结束**。

### GetMallByName / resolve mall_id / CreateBrowser

**resolve mall_id**：先读 `mall_cache.json`；未命中才调 `GetMallByName`，成功后立即写缓存。

任一步 `GetMallByName` / `CreateBrowser` 的 `success != true` 或缺字段 → **立即结束**，不重试（缓存 id 导致后续 API 失败时的**一次**刷新重试除外，见「本地店铺 ID 缓存」）。

### UpdateAccount（修改店铺账号密码）

客户要求**修改店铺登录账号/密码**时调用。须站斧已打开且已登录；先 resolve `mall_id`，再：

```json
{
  "action": "UpdateAccount",
  "module": "WebDriverModule",
  "browserId": "3514488",
  "args": "{\"username\":\"admin\",\"password\":\"cyt123456A\"}"
}
```


| 字段 | 必填 | 说明 |
| ---- | --- | ---- |
| `browserId` | 是 | 店铺 `mall_id`（**必须为字符串**） |
| `args.username` | 否 | 店铺账号（对应 `mall_account`；可空字符串） |
| `args.password` | 否 | 店铺密码（对应 `mall_password`；可空字符串） |


- 缺少店铺名/`mall_id` 或客户未说明要改的账号/密码时 → **先询问**，禁止猜测
- `returnObj.success != true` → **立即结束**，原样报告 `returnObj.msg`（如「缺少 browserId」）
- 成功：`success == true`（`data` 可为 `{}`）

### OpenBrowser（须先过「已打开店铺确认」）

```json
{"action": "OpenBrowser", "module": "WebDriverModule", "browserId": "3514488", "args": "{\"isDownLoadConfirm\":false,\"isOpenMallIndex\":true,\"isSwitchDynamicNetwork\":false}"}
```

- **`browserId` 必须是字符串**（`"3514488"`），**禁止**数字 `3514488`
- **仅站斧已打开后**再写入 `opening_malls.json`（探测未打开时已清空，禁止未打开就写入）
- 目标店铺**未打开**（含 OpenBrowser 前探测 **5s 超时**）→ 可直接 `OpenBrowser`
- 目标店铺**已打开**（客户要求**打开**该店）→ 须先询问客户**是否需要关闭店铺**；确认关闭后再视情况 `CloseBrowser` / `OpenBrowser`（见「已打开店铺的确认」）
- 客户**明确说关闭店铺**且 HTTP 正常 → 直接 `CloseBrowser`，清理 `opening_malls.json`，**不重启**站斧
- `OpenBrowser` 本身 `returnObj !== true` 或 `ret != 200` → **立即结束**，并**提醒客户**：
  > **打开店铺失败，请确认该店铺是否已绑定 IP / 设备。** 可在站斧客户端查看店铺绑定设备后再试。
- `OpenBrowser` **之后**的 `GetBrowserWebDriver` 失败（含「超时未获取到」）→ 同上，**一并提醒检查 IP/设备绑定**；并提醒客户：**首次使用请先在站斧客户端手动打开该店铺以下载内核；不同内核的店铺需分别手动打开一次**

### GetBrowserWebDriver

```json
{"action": "GetBrowserWebDriver", "module": "WebDriverModule", "browserId": "3514488"}
```

- **`browserId` 必须是字符串**（`"3514488"`），**禁止**数字 `3514488`
- **OpenBrowser 前探测（是否已开）**：**只请求 1 次，`timeout=5`**；超时/无端口 → **仍 `OpenBrowser`**；禁止重试、禁止加长超时
- **OpenBrowser 后取端口**：`WebDriverPort` 为空或请求失败 → **立即结束**（禁止循环重试、禁止「再等一会」方案）
- `OpenBrowser` 后允许**单次**固定等待 10s 再调 `GetBrowserWebDriver`（不算重试）；若仍失败则结束。
- **macOS 内核检查（拿到端口后、进入阶段 B 前必做）**：若当前 OS 为 **macOS**，且 `returnObj.KernalNumber` 存在且 **≤ 130** → **立即停止**，**禁止** `connect_over_cdp` / 页面自动化，按下方「macOS 低内核对客户话术」提示客户；**Windows 不校验此限制**。复用已开店铺（客户确认不关闭、直接用现有端口）时同样要检查 `KernalNumber`。

### macOS 低内核对客户话术（KernalNumber ≤ 130 · 必须原样）

当 **macOS** 且打开店铺后 `GetBrowserWebDriver` 返回 `KernalNumber ≤ 130`（含已打开店铺复用端口的场景）时：

- **立即停止**，**禁止**进入阶段 B，**禁止**代客户改内核或自动重启站斧
- **必须**向客户报告以下模板（`{kernel}` 换成实际 `KernalNumber`，`{mall_name}` 换成店铺名）：

```
当前为 macOS，店铺 {mall_name} 的内核为 {kernel}（≤130），暂不支持自动化。
请将该店铺切换到 130 以上内核；若无权限请让主账号切换。切换完成后请您手动重启站斧，再告诉我继续。
```

---

## 阶段 B：Playwright CDP（端口拿到后）

> **macOS**：进入本节前须已确认 `KernalNumber > 130`；否则不得 `connect_over_cdp`。
```python
from headed_mode import ensure_headed_mode
from playwright.sync_api import sync_playwright

ensure_headed_mode()
browser = sync_playwright().start().chromium.connect_over_cdp(
    f"http://127.0.0.1:{webdriver_port}"
)
```

连接失败 → **立即结束**，禁止换系统浏览器替代。

### 设备安全检测

找 URL 含 `check.html` 的标签页，**15s 内**轮询，满足以下**任一**条件即视为检测通过：

1. **「打开店铺」按钮未禁用**（`.openMallOpenBtn`，且非 `disabled` / `aria-disabled=true` / `is-disabled`）
2. **标签页数量 ≥ 2**（通常表示店铺页已打开）

15s 内仍不满足 → 告知「没检测成功无法进行自动化」，立即结束。

可运行 Skill 内置（**仅阶段 B**）：

```bash
python scripts/check_device_security.py --port {webdriver_port} --wait --timeout 15
```

### 业务自动化

检测通过后，按客户需求用 Playwright 操作页面。**禁止**在 Skill 目录新增业务脚本；临时逻辑在对话中执行，不落盘为 `.py`。

---

## 收尾（阶段 A · HTTP）

**关闭店铺**（客户明确要求时）：

```json
{"action": "CloseBrowser", "module": "WebDriverModule", "browserId": "3514488"}
```

成功后**从 `opening_malls.json` 去掉该 `mall_name`**。

**退出站斧客户端**（仅客户明确要求「退出站斧」时；开/关店铺**不要**顺带调用）：

```json
{"action": "ExitClient", "module": "WebDriverModule", "args": ""}
```

成功后（或冷启动重启前）**清空 `opening_malls.json`**。

---

## 失败处理（统一）


| 情况                                                 | 动作                                                                                                                  |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 目标端口无 HTTP 响应 / **打开站斧且站斧未打开**                     | **立刻清空 `opening_malls.json`** → 查安装目录（快捷方式/常见目录找不到则向客户索要）→ **`get_available_port(首选)`（占用则递增）** → 冷启动并写 `api_port.json`；冷启动后 **8s 仍无通讯** → 按「通讯失败对客户话术」报告（版本无误且卡顿可延迟时可再试，请客户说「打开站斧」） |
| `GetBrowserList` 能取到数据 + **打开店铺**                  | **站斧已打开，不重启**；写入 `opening_malls.json` → HTTP 开店铺流程                                                                  |
| `GetBrowserList` 能取到数据 + **关闭店铺**                  | **不重启**；resolve mall_id → `CloseBrowser` → 清理 `opening_malls.json`                                                  |
| API 已运行 + 开新店铺                                     | **不重启**站斧，直接 HTTP 开店铺                                                                                               |
| 目标店铺已打开（客户要求**打开**）                                | **询问客户**是否需要关闭店铺；未确认不调用 `OpenBrowser` / `CloseBrowser`                                                              |
| OpenBrowser 前 `GetBrowserWebDriver` **5s 超时**      | **不结束**；继续 `OpenBrowser`（只许探测 1 次）                                                                                  |
| 客户明确要求关闭已开店铺                                       | 直接 `CloseBrowser` → 清理 `opening_malls.json`                                                                         |
| 客户明确要求关闭站斧                                         | `ExitClient` → **清空** `opening_malls.json`                                                                          |
| GetBrowserList 8s 内仍无法确认登录（**确认为站斧** WebDriver 有响应） | **停止**，提示客户提供账号密码；**禁止**擅自或内测账号 Login；**禁止**用 `LoadSuccess` 判断。若其实是非站斧占用，应走空闲端口冷启动而非要密码 |
| OpenBrowser / OpenBrowser 后 GetBrowserWebDriver 失败 | 立即结束；`OpenBrowser` 以 `returnObj===true` 判成功；提醒检查 **IP/设备绑定** 及 **是否已手动打开该店铺下载内核**（版本要求：Windows ≥ 5.2.12，macOS > 5.2.10）                     |
| **macOS** 且 `KernalNumber ≤ 130`（打开/复用店铺后） | **立即停止**；按「macOS 低内核对客户话术」提示：切换到 **130 以上**内核或请**主账号**切换，并请客户**手动重启站斧**后再继续；**禁止**阶段 B |
| CloseBrowser 返回 `returnObj===false`                | 立即结束，报告关闭失败                                                                                                         |
| 其他关键 API 失败                                        | 立即结束，原样报告 `returnObj.msg`（`OpenBrowser`/`CloseBrowser` 无 `msg` 时报告 `returnObj` 值）                                   |
| OpenBrowser 后拿不到 WebDriverPort                     | 立即结束，不 retry                                                                                                        |
| 设备安全检测 15s 超时                                      | 立即结束，告知「没检测成功无法进行自动化」                                                                                               |
| CDP 连接失败                                           | 立即结束，禁止换浏览器                                                                                                         |


**禁止**：重试、翻代码、写备用脚本、写「稍后重跑」方案；**禁止**用 `LoadSuccess` 判断站斧是否已打开。

---

## 参考脚本（Agent 应按意图运行，禁止另写一次性脚本）

| 意图 | 命令 |
|------|------|
| 打开站斧 | `python scripts/open_zhanfu.py` |
| 打开店铺 | `python scripts/open_mall.py --mall-name ztest126` |
| 关闭店铺 | `python scripts/close_mall.py --mall-name ztest126` |
| 店铺列表 | `python scripts/list_malls.py` |
| 关闭站斧 | `python scripts/close_zhanfu.py` |
| 登录 | `python scripts/login_zhanfu.py --username ... --password ...` |
| 创建店铺 | `python scripts/zhanfu_ops.py create-mall --mall-name ... --platform ...` |
| 改店铺账号 | `python scripts/zhanfu_ops.py update-account --mall-name ... --username ... --password ...` |
| 下载目录 | `python scripts/zhanfu_ops.py set-download --file-path D:\downloads` |
| 店铺插件 | `python scripts/zhanfu_ops.py set-plugins --plugin-name 紫竹自动化插件 --chrome-id ""` |
| 清缓存 | `python scripts/zhanfu_ops.py clear-cache --mall-name ztest126` 或 `--all` |

- [scripts/zhanfu_http.py](scripts/zhanfu_http.py) — 公共 HTTP 库（`browserId` 强制字符串）
- [scripts/zhanfu_playwright.py](scripts/zhanfu_playwright.py) — 全流程参考实现
- [scripts/check_device_security.py](scripts/check_device_security.py) — 阶段 B 设备检测
- [scripts/headed_mode.py](scripts/headed_mode.py) — 强制有界面

API 详情（含通用约定与全部接口）：[reference.md](reference.md)
