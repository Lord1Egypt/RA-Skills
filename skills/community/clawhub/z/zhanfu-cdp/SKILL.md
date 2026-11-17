---
name: zhanfu-cdp
description: >-
  站斧 WebDriver 版 Playwright 自动化（Windows≥5.2.12、macOS 高于 5.2.10、有界面、连不上即停）。
  仅开店=立刻跑 node scripts/open_mall.mjs 后一句话结束；禁止事先 GetBrowserList/阶段B/设备检测/扩写。
  页面自动化才 CDP。战斧=站斧。适用于站斧/战斧/WebDriver/Playwright/店铺自动化。
---

# 站斧 Playwright 自动化

## 仅开店（最高优先级 · 读完本节即可执行 · 勿往下翻）

客户意图只要是「打开店铺 / 打开战斧店铺 / 拿 WebDriverPort」且**未**要求填表、抓取、点页面时：

1. 缺店名 → 只问店名，问完就停；有店名继续。
2. 在 Skill 目录**唯一动作**：
   ```bash
   node scripts/open_mall.mjs --mall-name {店铺名}
   ```
3. 只看结尾 `RESULT_JSON=`，按下表**一句话回复客户后立即结束本回合**。

| `status` | 对客户原样短回复（禁止扩写、禁止追问关店、禁止阶段 B） |
|----------|------------------------------------------------------|
| `already_open` / `opened` | `已打开 {mall_name}，mall_id={mall_id}，WebDriverPort={WebDriverPort}` |
| `zhanfu_down` | `请打开最新的站斧` |
| `open_failed` / `no_webdriver_port` | 转述脚本失败信息（可含 IP/设备绑定与内核提示）；本店停止 |

**失败恢复由脚本处理**：取端口 20 次仍失败即结束并释放本地占位，不自动关闭店铺、不在本轮反复重开。下次客户明确要求打开时，先复用存活端口或单次探测（1.5s），未取得端口再尝试 OpenBrowser。旧版遗留的无端口失败占位会自动清理；真正执行中的任务仍禁止重复打开。不要把无端口失败记录说成「仍在启动」，也不要建议「等待端口退出」。

**仅开店禁止**（违反即慢）：事先 `GetBrowserList` / 8s 登录轮询 / 手调 `GetMallByName`·`OpenBrowser`·`GetBrowserWebDriver` / 读 `reference.md` / 进阶段 B / `check_device_security.mjs` / 多段解释 / 再问「是否关闭」。

多家：`node scripts/open_malls.mjs --mall-name 店A --mall-name 店B`。对话结束/暂停：`node scripts/stop_open_malls.mjs`。

**【macOS】** 成功 JSON 里若 `KernalNumber ≤ 130`：不进阶段 B，按后文「macOS 低内核对客户话术」提示后停。

---

通过站斧 WebDriver 版 **HTTP API** 控制店铺；**拿到 WebDriverPort 之后**才用 Playwright `connect_over_cdp` 做页面自动化（**仅页面操作意图**）。

**本技能不支持**打开 / 关闭 / 重启站斧客户端。HTTP 端口**只读**站斧非多开 `Http.ini` 的 `[Common] httpport`（**不要**用 `api_port.json`）。Windows：`%APPDATA%\ZhanFu\Http.ini`；macOS：`~/Library/Application Support/ZhanFu/Http.ini`。连不上 → **原样「请打开最新的站斧」**。

**Agent 提示**：技能**首次安装**、客户问「怎么用」时，再发下方「客户使用指南」（可摘要）。**仅开店不要先发指南。**

**前置（Agent）**：站斧 **Windows ≥ 5.2.12**，**macOS > 5.2.10**；已装 Node ≥18；首次运行脚本会自动 npm install（含 playwright）。

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
| 打开店铺          | **打开店铺 ztest126**（把 `ztest126` 换成您的店铺名）    |
| 关闭某个店铺        | **关闭 ztest126 店铺** / **关闭店铺 ztest126**     |
| **创建新店铺**     | **创建店铺**，并按提示提供下方参数（见「七、创建店铺」）             |
| **修改店铺账号密码**  | **修改店铺账号密码**，提供店铺名与新账号/密码（见「十二、修改店铺账号密码」） |
| **查看我的店铺列表**  | **获取店铺列表** / **列出店铺**（见「八、查看店铺列表」）         |
| **设置浏览器下载目录** | **设置下载目录到 D:\downloads**（见「十、下载与缓存」）       |
| **清除店铺/全部缓存** | **清除 xxx 店铺缓存** / **清除全部缓存**（见「十、下载与缓存」）   |
| **设置店铺默认插件**  | **设置店铺插件**，提供插件名称；插件 ID 可省略或留空（见「十一、店铺插件」） |
| **清空店铺插件列表**  | **清除默认插件列表** / **清空店铺插件**（见「十一、店铺插件」）      |


> 说法可略有不同，只要包含「打开店铺」和**店铺名称**即可。
>
> **同义说法**：客户发「**战斧**」时一律按「**站斧**」理解（业务用语同义，如「打开战斧店铺」=「打开店铺」）——**不要**当成未知产品或要求客户改口。本技能**不支持**打开 / 关闭 / 重启站斧客户端。

### 三、首次未登录时

若提示「站斧未登录，请提供账号和密码」，请提供您的**站斧老板账号**和密码（自动化仅使用您当场提供的账号，不会使用内测账号）。

### 四、店铺已经打开时

若您要的店铺**已经在运行**，系统会**直接复用**现有自动化端口并告知您，**不会**先问是否关闭。若要关掉或关掉后重开，请明确说「关闭店铺」或「关闭后重开」。

### 五、页面自动化（进阶）

店铺打开后，可继续用自然语言描述要在**店铺浏览器里**做的事，例如：

- 「在 B 站搜索并播放某某视频」
- 「打开某网址并填写表单」
- 「抓取当前页面某某信息」

此类操作会先等设备安全检测通过（约 15 秒），再自动操作页面。

### 七、创建店铺

发送 **「创建店铺」**，按提示提供信息即可（须已登录站斧）。

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

> 设置默认插件名称为紫竹自动化插件，插件 ID 为空，再打开店铺 ztest144  
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
| 请打开最新的站斧 | 本机 WebDriver 端口连不上；请打开最新站斧后再发指令 |
| 创建店铺失败  | 检查店铺名是否重复、IP 是否已绑定、自定义平台是否填了网址     |
| 看不到店铺列表 | 先登录站斧；或说明要查第几页、每页多少条               |


---

## 硬规矩（红线，最高优先级）

以下规则覆盖本 Skill 其他所有「等待 / 重试 / 备用方案」描述，**冲突时以本节为准**。

### 1. 获取端口前：禁止写脚本

在 `**OpenBrowser` 打开店铺并成功拿到 `WebDriverPort` 之前**：

- **禁止**新建或运行任何临时可执行脚本（含 `_tmp_*.mjs` / `.js` / `.sh` 等业务脚本）
- **禁止**为完成任务而编写「一次性自动化脚本」
- **只允许**调用本 Skill 提供的 **HTTP 接口**（见 [reference.md](reference.md)）或 Shell 直接发 HTTP 请求
- **允许**读写临时**数据文件**（如 `mall_cache.json`、`opening_malls.json` 状态文件），但数据文件不可执行；**禁止**读写 `api_port.json`

> **例外（内置脚本）**：打开店铺运行 [`scripts/open_mall.mjs`](scripts/open_mall.mjs)；关店 / 列表 / 登录 / 创建与插件等分别运行 `close_mall.mjs`、`list_malls.mjs`、`login_zhanfu.mjs`、`zhanfu_ops.mjs`。**禁止**另写一次性脚本。阶段 B 页面自动化仍禁止落盘为业务 `.mjs`/`.js`。

### 2. 通讯失败或关键操作报错：立即结束

出现以下情况，**马上停下并向客户报告**（**仅开店**走 `open_mall.mjs`，脚本内取端口重试除外；其他意图的 `GetBrowserList` 登录探测、以及 OpenBrowser 前 `GetBrowserWebDriver` **单次 1.5s** 超时后仍 `OpenBrowser` 除外）：

- HTTP **连不上**站斧（`Http.ini` 缺失、连接拒绝、超时、无响应）→ **提示「请打开最新的站斧」并停止**
- 端口有 HTTP 响应但**不是**站斧 WebDriver 结构 → **提示「请打开最新的站斧」并停止**
- 除登录/运行态探测用 `GetBrowserList` 外，关键 API 返回失败（`returnObj.success == false`、缺必需字段）
- Login / GetMallByName / CreateBrowser / UpdateAccount / SetInstallPlugins / OpenBrowser（`returnObj !== true`）/ GetBrowserWebDriver 失败（**例外**：OpenBrowser **前**探测 `GetBrowserWebDriver` 超时 1.5s → 仍执行 `OpenBrowser`）

**禁止**：

- 反复重试同一失败操作（**非开店意图**的 `GetBrowserList` **8s 轮询**、以及 OpenBrowser 前 `GetBrowserWebDriver` **仅允许单次 1.5s，超时改走 OpenBrowser**除外）
- **仅开店**时：先手搓 `GetBrowserList` / 8s 登录轮询 / 阶段 B / `check_device_security.mjs` / 继续通读本 Skill 后文 / 对客户多段解释或追问关店
- 打开 / 关闭 / 重启站斧客户端（含杀进程、启动可执行文件、任何客户端启停流程）
- 全盘 / 跨盘符搜索站斧安装包（Windows：`where.exe`、`-Recurse`、glob `**\站斧.exe`；macOS：全盘 `mdfind` / `find`）
- 遍历桌面**全部** `.lnk` 或解析快捷方式以启动客户端
- 翻代码库「研究」原因
- 写「等通讯好了再跑」的备用方案或延迟任务
- 自行换端口 / 换路径 / 换工具碰运气（**禁止**盲扫 8081/8082 碰已运行站斧）
- 将 `OpenBrowser` / `GetBrowserWebDriver` 的 `browserId` 传成 **JSON 数字**（必须为**字符串**，如 `"3514488"`）
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

> **`browserId` 类型硬规矩**：`OpenBrowser`、`GetBrowserWebDriver`（以及同样传 `browserId` 的 `CloseBrowser` / `UpdateAccount` / `ClearCache` 等）的 **`browserId` 必须是 JSON 字符串**（如 `"3514488"`），**禁止**传数字（如 `3514488`）。从 `mall_id` 取值后一律 `String(mall_id)` 再写入请求。

**API 端口**：以站斧 `Http.ini` 的 `httpport` 为准（脚本 `preferred_port()` 已读）。**禁止** `api_port.json`，**禁止**盲扫 8081/8082。

#### HTTP 请求方式（阶段 A · 禁止 curl / 禁止换工具试错）

**Agent 默认只用内置 Node 脚本**（稳定、无引号逃逸坑）。**禁止**为同一探测在 PowerShell / curl / Node 之间来回换工具（浪费时间）。

**单次探测超时**：`timeout=1.5` 秒（够判通断，勿用 3～30s 长超时堵死）。

非开店若必须手搓 HTTP，端口从 `Http.ini` 读取（与脚本相同路径）。连接拒绝 / 超时 / 无响应 / 非站斧占用 / 无 `Http.ini` → **提示「请打开最新的站斧」并停止**；**不要**改用 PowerShell 再探一次；**不要**由本技能启动客户端。

**备选（仅人工调试）** PowerShell 手动拼 JSON：

```powershell
$body = '{"module":"WebDriverModule","action":"GetBrowserList","args":"{\"page\":1,\"limit\":20}"}'
Invoke-RestMethod -Uri "http://127.0.0.1:12678" -Method Post -Body $body -ContentType "application/json"
```

**禁止** Windows `curl` 手工转义 JSON；**禁止** PowerShell `ConvertTo-Json` 嵌套 `args`。

#### 打开店铺快速路径

**以文首「仅开店」为准**，此处不重复。Agent 命中开店意图时**停止阅读**后续章节（关店/创建/插件/阶段 B 等），直接跑脚本并一句话结束。

关闭店铺：`node scripts/close_mall.mjs --mall-name xxx`。

#### 阶段 B — 拿到 WebDriverPort 之后


| 工具 / 方法                                | 用途                                |
| -------------------------------------- | --------------------------------- |
| `playwright.chromium.connect_over_cdp` | 接管站斧店铺浏览器                         |
| `scripts/check_device_security.mjs`     | **仅页面自动化**前设备安全检测（**禁止**仅开店时运行） |
| `ensureHeadedMode()`                 | 强制有界面（见 `scripts/headed_mode.mjs`） |


**禁止**：`playwright.chromium.launch`、`browser_navigate`（MCP）、Puppeteer `launch`。

---

## 两阶段工作流

```
仅开店（默认）→ 文首卡片：open_mall.mjs → 一句话 → 结束（禁止读后文）

其他阶段 A（关店/列表/登录/创建/插件）
  Http.ini → GetBrowserList → … → 对应脚本

阶段 B（仅明确页面操作）
  设备安全检测 15s → connect_over_cdp → 业务
```

```
Task Progress（仅开店 · 仅此两项）：
- [ ] 1. `node scripts/open_mall.mjs --mall-name {店铺名}`
- [ ] 2. 按文首表格一句话回复后结束

Task Progress（非开店）：
- [ ] A. 读 Http.ini → 单次 GetBrowserList；失败 →「请打开最新的站斧」
- [ ] B. 关店/列表/登录/创建/插件按对应脚本
- [ ] C. 仅页面自动化：设备检测 → CDP → 业务
```

---

## 禁止无头模式

1. 站斧必须以 WebDriver 模式**有界面**运行
2. 只能 `connect_over_cdp`，禁止 `launch(headless=True)`
3. 执行 Playwright 前调用 `ensureHeadedMode()`，设置 `PLAYWRIGHT_HEADLESS=0`
4. 禁止使用 Cursor 内置 browser MCP 替代站斧浏览器

---

## 执行前：向客户收集参数

缺少必填项时先询问，**不要猜测账号密码或 IP**。

### 登录态探测与 Login

**仅开店不走本节**：直接 `open_mall.mjs`，不要为开店做 8s `GetBrowserList`。

其他意图（关店 / 列表 / 登录 / 创建 / 插件 / 页面自动化）在站斧 API 可用后，**必须在 8s 内**通过 `GetBrowserList` 判断站斧是否**已打开**且已登录（**禁止**用 `CheckClientOpen` / `LoadSuccess` / `LoadFailed` 判断）：

```json
{"action": "GetBrowserList", "module": "WebDriverModule", "args": "{\"page\":1,\"limit\":20}"}
```


| `GetBrowserList` 结果（8s 内）                                  | 动作                                                               |
| ---------------------------------------------------------- | ---------------------------------------------------------------- |
| `returnObj.success == true` 且能取到 `mall_list`（可解析，非 `null`） | **站斧已打开且已登录**，跳过 `Login`（`Login` 会关闭已开店铺）                        |
| 有 HTTP 响应但 `success == false`、`data=null`、无法解析 `mall_list` | 站斧进程可能在跑但**未登录** → **停止**，提示客户：**「站斧未登录，请提供账号和密码」** |
| 连接拒绝 / 无响应 / 非站斧占用 / 无 Http.ini / 8s 超时仍无任何可用 WebDriver 响应 | **提示「请打开最新的站斧」并停止**                                  |
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

缺 `mall_name` 先问客户。有店名则走「打开店铺快速路径」，**不要**在本节逐步调 HTTP。

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
4. `node scripts/open_mall.mjs --mall-name xxx`（脚本内 OpenBrowser 后等 **200ms** 再取端口）

`returnObj.success != true` → **立即结束**，原样报告 `returnObj.msg`。

### 设备安全检测（仅业务自动化）

客户提出**页面级自动化**（填表、抓取、播放视频等）时，阶段 B 必须先等设备安全检测成功（15s 超时）。**仅开店铺 / 关店铺禁止**跑 `check_device_security.mjs`，禁止 `connect_over_cdp`。

超时或未成功 → 告知客户：**「没检测成功无法进行自动化」**，立即结束。

---

## 打开店铺 / 关闭店铺（意图路由）

**打开店铺**：**不要**先探测，直接 `open_mall.mjs`（脚本失败 `zhanfu_down` →「请打开最新的站斧」）。**关闭店铺**及其他非开店意图：读 `Http.ini` 的 `httpport` 并对该端口做单次 `GetBrowserList`（**禁止**用 `LoadSuccess` 判断）。

> **同义**：客户说「**战斧**」=「**站斧**」（业务用语同义）。本技能**不支持**打开 / 关闭 / 重启站斧客户端；此类意图 → **停止**并说明不支持。


| 客户意图                       | `GetBrowserList` 探测        | 动作                                                                                                                                                    |
| -------------------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **打开店铺**                   | **跳过**（禁止事先探测）            | 按文首「仅开店」：`open_mall.mjs` → 一句话结束（勿读后文） |
| **关闭店铺**                   | **能取到数据**或有 HTTP 响应        | 直接 HTTP：resolve mall_id → `CloseBrowser` → **从 `opening_malls.json` 去掉该店铺名**                                           |
| **创建店铺**                   | **能取到数据**或有 HTTP 响应        | `CreateBrowser` → 等待同步 → resolve mall_id → `OpenBrowser`（参数见客户指南「七、创建店铺」）                                                                    |
| **修改店铺账号密码**               | **能取到数据**或有 HTTP 响应        | resolve mall_id → `UpdateAccount`（`browserId`=`mall_id`，`args.username`/`password` 由客户提供，可空；见「十二、修改店铺账号密码」）                              |
| **获取店铺列表**                 | **能取到数据**或有 HTTP 响应        | `GetBrowserList`（默认 `page=1, limit=10`，可按客户指定分页）→ 展示 `mall_list`；**同时将列表中 `mall_name` → `mall_id` 写入 `mall_cache.json`**                     |
| **设置下载目录**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：`SetDownLoadPath`（`FilePath` 由客户提供）                                                                           |
| **设置店铺插件**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：`SetInstallPlugins`（须在 `OpenBrowser` 前）                                                                       |
| **清空插件列表**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：`SetInstallPlugins([])` → `ClearCache` → `OpenBrowser`                                                        |
| **清除全部缓存**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：确认后 `ClearCacheFolder` → 清空 `opening_malls.json`                                                              |
| **清除单店缓存**                 | **能取到数据**或有 HTTP 响应        | **仅 Windows**；macOS → 告知暂不支持并停止。Windows：确认后 `ClearCache` → 从 `opening_malls.json` 去掉该店                                                                |
| **打开 / 关闭 / 重启站斧（客户端）**    | 任意                         | **本技能不支持客户端启停** → **停止**并说明不支持                                                                                                                         |
| **打开 / 关闭店铺**              | **无响应** / **非站斧占用** / 无 Http.ini | **提示「请打开最新的站斧」并停止**                                                                                                                         |


> **核心**：开店铺、关店铺都是 **HTTP 操作**；端口以 `Http.ini` 为准。`GetBrowserList` **能取到数据** = 站斧**已打开**。无 HTTP / 非站斧占用 = **提示「请打开最新的站斧」并停止**。**禁止**根据 `CheckClientOpen` 的 `LoadSuccess` / `LoadFailed` 判断站斧是否已打开。

### 关闭店铺流程（阶段 A · 仅 HTTP）

1. 读 `Http.ini` 的 `httpport` → 单次探测 `GetBrowserList`
2. 能取到数据或有 HTTP 响应 → resolve mall_id（读 `mall_cache.json` → 未命中则 `GetMallByName` 并写缓存；失败即停）
3. 无响应 / 非站斧占用 / 无 Http.ini → **提示「请打开最新的站斧」并停止**
4. `CloseBrowser`（`browserId` = 字符串形式的 `mall_id`）；成功时 `returnObj === null`，失败时 `returnObj === false`
5. **从 `opening_malls.json` 去掉该 `mall_name`**

```json
{"action": "CloseBrowser", "module": "WebDriverModule", "browserId": "3514488"}
```

---

## 通讯失败策略（无 HTTP / 非站斧占用 / 无 Http.ini）

目标端口**无 HTTP 响应**，或有响应但**不是**站斧 WebDriver 结构，或找不到 `Http.ini` 时：

1. **立即停止**
2. **向客户原样报告：「请打开最新的站斧」**
3. **禁止**：由本技能启动 / 关闭 / 重启客户端、杀进程、查找安装路径、换端口再试、改用其他口令

---

## 站斧运行态复用（读本地端口 · 单次 GetBrowserList · 禁止扫端口）

客户要求**打开店铺**时**不要**先做本节探测，直接 `open_mall.mjs`。关闭店铺或执行其他 HTTP 业务时，**禁止**依次试探 8081/8082 等端口。

### 端口来源 `Http.ini`（非多开 · 禁止 api_port.json）

| 系统 | 路径 |
| ---- | ---- |
| Windows | `%APPDATA%\ZhanFu\Http.ini`（即 `C:\Users\<用户名>\AppData\Roaming\ZhanFu\Http.ini`） |
| macOS | `~/Library/Application Support/ZhanFu/Http.ini` |

```ini
[Common]
httpport=12678
```

通讯**只认**该文件的 `httpport`。默认路径上的 `Http.ini` **读不到**时：仅当该文件或其所在 `ZhanFu` 目录是外联（目录联接 / 符号链接，可能指到其他目录）时，再读链接目标里的 `Http.ini`。**没有外联则逻辑不变**（不改路径、不搜索其他目录）。文件不存在、读不到合法端口、或该端口连不上 → **「请打开最新的站斧」**。不写 Skill 目录端口缓存。

| 时机                                 | 动作                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------ |
| 仅开店                                 | **跳过**本节探测，直接 `open_mall.mjs`（脚本自己读 Http.ini）                                        |
| 其他任务开始                             | **先读** `Http.ini` 的 `httpport`                                                        |


### 单次探测（仅 Http.ini 中的端口 · 用 GetBrowserList，禁止 LoadSuccess）

对该端口发**一次** POST，Body 为正确 JSON 的 `GetBrowserList`：

```json
{"module":"WebDriverModule","action":"GetBrowserList","args":"{\"page\":1,\"limit\":20}"}
```


| HTTP / 业务结果                                   | 判定              | 动作                                                                    |
| --------------------------------------------- | --------------- | --------------------------------------------------------------------- |
| `success==true` 且能取到 `mall_list`（可解析）         | **站斧已打开**（且已登录） | 继续开/关店铺等 HTTP 操作                                           |
| 有 HTTP 响应体，但取不到 `mall_list` / `success=false` | 站斧进程在跑但可能未登录    | 进入登录提示流程                                      |
| 有 HTTP 响应但**不是**站斧 WebDriver 结构               | **非站斧占用**       | **提示「请打开最新的站斧」并停止** |
| **连接拒绝 / 超时 / 无响应**                           | **连不上**       | **提示「请打开最新的站斧」并停止** |


> **禁止**再用 `CheckClientOpen` 的 `LoadSuccess` / `LoadFailed` 判断站斧是否已打开。「模块 undefined 未加载」等说明该端口上**已有 HTTP 服务**；若确认为站斧 WebDriver，用正确 JSON 的 `GetBrowserList` 重发即可；若是**非站斧**服务，提示「请打开最新的站斧」并停止。


| 场景                       | 动作                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------ |
| **打开店铺**                   | `node scripts/open_mall.mjs --mall-name {店铺名}`（禁止事先 GetBrowserList）           |
| 站斧已打开 + **关闭店铺**         | resolve mall_id → `CloseBrowser` → 清理 `opening_malls.json`                         |
| 站斧已打开 + 阶段 B 业务          | `GetBrowserWebDriver` 拿端口                                                          |
| 目标端口无 HTTP 响应 / 非站斧占用   | **提示「请打开最新的站斧」并停止** |


> **非开店**复用已运行实例时，用 `GetBrowserList`（最多 **8s**）判断是否已打开/已登录。仅开店不在此轮询。

---

## 打开意图配置 `opening_malls.json`

路径：Skill 目录下 `[opening_malls.json](opening_malls.json)`（与 `SKILL.md` 同级）。

用于记录客户**已发出「打开某店铺」指令**的店铺名；关店时清理。由 `open_mall.mjs` 维护，Agent 开店时不要逐步手调探测。

```json
{
  "malls": ["ztest126"],
  "updated_at": "2026-07-14T10:00:00"
}
```


| 字段           | 说明                              |
| ------------ | ------------------------------- |
| `malls`      | 客户已下达「打开」意图、且尚未通过关店清理的店铺名列表 |
| `updated_at` | 最近一次写入时间                        |



| 时机                                                         | 动作                                     |
| ---------------------------------------------------------- | -------------------------------------- |
| 客户发送**打开店铺 {店铺名}**（**仅当站斧已打开之后**拿到 `mall_name`）   | **写入**该 `mall_name`（已存在则跳过）            |
| 探测到连不上（无 HTTP / 非站斧占用 / 无 Http.ini）        | **立刻清空**整个 `malls` 列表，并停止 |
| 客户发送**关闭店铺 {店铺名}** 且 `CloseBrowser` 成功                     | **去掉**该 `mall_name`                    |
| `ClearCacheFolder` 成功 | **清空**整个 `malls` 列表                    |
| 清除单店缓存 `ClearCache` 成功                                     | **去掉**该店铺名                             |


> `opening_malls.json` 只记店铺名，与 `mall_cache.json`（店铺 ID）无关。**禁止**在连不上时写入店铺名。

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

## 已打开店铺的确认

客户要求**打开**某店铺时跑 `open_mall.mjs`。脚本会：按名取 ID → 已有存活端口则复用 → 否则单次探测端口（1.5s）→ 未取得端口才 OpenBrowser → **等 200ms** → 最多取端口 20 次。取端口最终失败后释放本地占位；下次明确开店可重新尝试，不要求先关闭店铺。活跃任务和尚未过期的启动宽限期仍保护，遗留的无端口失败记录自动清理。

| 情况 | 动作 |
| ---- | ---- |
| `already_open` / `opened` | 文首短回复模板一句话结束；**禁止**追问是否关闭 |
| （客户明确关店/重开） | 再跑 `close_mall.mjs` / `open_mall.mjs` |
| `zhanfu_down` | **提示「请打开最新的站斧」并停止** |
| 客户确认需要关闭 | `node scripts/close_mall.mjs --mall-name xxx`；若还要再开，确认后再跑 `open_mall.mjs` |
| 客户明确说关闭店铺 | 直接 `close_mall.mjs`，无需再问 |

**禁止**：已开仍静默再 OpenBrowser；未确认就 CloseBrowser。客户说关闭且 HTTP 正常 → 直接关店，不必再问。

---

## 阶段 A 操作要点（HTTP only，失败即停）

### GetBrowserList（判断站斧是否已打开 + 登录态 · **非开店意图** · 总计最多 8s）

**仅开店禁止调用本节。** 关店 / 列表 / 登录 / 创建 / 插件等才做。

**禁止**用 `CheckClientOpen` / `LoadSuccess` / `LoadFailed` 判断站斧是否已打开。API 可用后**直接**轮询 `GetBrowserList`：

```json
{"action": "GetBrowserList", "module": "WebDriverModule", "args": "{\"page\":1,\"limit\":20}"}
```

- **轮询** `GetBrowserList`，间隔 **0.5s**，**总计最多 8s**
- `returnObj.success == true` **且** `returnObj.data.mall_list` 可解析（非 `null`）→ **站斧已打开且已登录**，**禁止**无故调用 `Login`；**同时将 `mall_list` 中 `mall_name` → `mall_id` 写入 `mall_cache.json`**
- 有 HTTP 响应但 **8s 内**仍 `success=false`、`data=null`、无法解析 `mall_list` → **停止**，提示客户：**「站斧未登录，请提供账号和密码」**；拿到凭证后再 `Login`
- 连接拒绝 / 无响应 / 非站斧占用 / 无 Http.ini → **提示「请打开最新的站斧」并停止**
- 客户未提供账号密码 → **停止**，不猜测、不擅自登录
- **单次请求** `timeout=1.5`；Agent **只用内置 Node 脚本**，禁止为通断探测切换 PowerShell/curl

> `CheckClientOpen` **不再作为流程步骤**；勿等待 `LoadSuccess`。

### Login

仅在 `GetBrowserList` 表明未登录且**客户已提供**账号密码时调用；`isboss` **固定** `true`。**禁止**使用内测或历史会话中的账号。`success != true` → **立即结束**。

### 开店三步（由 `open_mall.mjs` 一次完成，勿逐步手调）

`GetMallByName` → `OpenBrowser` → 等 **200ms** → `GetBrowserWebDriver` 都在 [`scripts/open_mall.mjs`](scripts/open_mall.mjs) 内。`browserId` 必须是字符串。失败即停（探测已开的 1.5s 超时除外，超时仍 OpenBrowser）。OpenBrowser / 取端口失败时提醒 IP/设备绑定与手动打开下载内核。`zhanfu_down` → **提示「请打开最新的站斧」并停止**。仅开店意图拿到端口后结束，不进阶段 B。

CreateBrowser / 缓存刷新仍见「本地店铺 ID 缓存」：缓存 id 导致后续失败时删缓存、`GetMallByName` **仅重试一次**。

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

### OpenBrowser / GetBrowserWebDriver

开店请跑 `open_mall.mjs`，不要逐步手调这两步。脚本：已有存活端口则直接复用；否则单次探测（1.5s），未取得端口才 OpenBrowser，**固定等 200ms**，再最多取端口 20 次（每次 HTTP 2s，无端口隔 0.3s）。最终失败即释放本地占位并结束；下次明确开店重新探测后尝试，不自动关闭店铺。取端口期间保留活跃任务保护，不能因为端口为 0 就释放正在执行的任务。`browserId` 必须是字符串。

- 客户要求打开且脚本返回 `already_open` / `opened` → 文首短回复模板一句话结束；禁止追问是否关闭
- 客户明确关店 → `close_mall.mjs`
- 脚本返回 `zhanfu_down` → **提示「请打开最新的站斧」并停止**
- OpenBrowser `returnObj !== true` 或取不到端口 → 提醒：
  > **打开店铺失败，请确认该店铺是否已绑定 IP / 设备。** 首次使用请先在站斧客户端手动打开该店铺以下载内核。
- **macOS**：拿到端口后若 `KernalNumber ≤ 130` → 立即停止阶段 B，按下方话术提示

### macOS 低内核对客户话术（KernalNumber ≤ 130 · 必须原样）

当 **macOS** 且打开店铺后 `GetBrowserWebDriver` 返回 `KernalNumber ≤ 130`（含已打开店铺复用端口的场景）时：

- **立即停止**，**禁止**进入阶段 B，**禁止**代客户改内核或自动重启站斧
- **必须**向客户报告以下模板（`{kernel}` 换成实际 `KernalNumber`，`{mall_name}` 换成店铺名）：

```
当前为 macOS，店铺 {mall_name} 的内核为 {kernel}（≤130），暂不支持自动化。
请将该店铺切换到 130 以上内核；若无权限请让主账号切换。切换完成后请您手动重启站斧，再告诉我继续。
```

---

## 阶段 B：Playwright CDP（**仅页面自动化** · 端口拿到后）

> **仅开店禁止进入本节。** 客户未要求填表/抓取/点页面等，拿到 `WebDriverPort` 即结束。
>
> **macOS**：进入本节前须已确认 `KernalNumber > 130`；否则不得 `connect_over_cdp`。
```js
import { ensureHeadedMode } from "./scripts/headed_mode.mjs";
import { chromium } from "playwright";

ensureHeadedMode();
const browser = await chromium.connectOverCDP(
  `http://127.0.0.1:${webdriver_port}`
);
```

连接失败 → **立即结束**，禁止换系统浏览器替代。

### 设备安全检测

找 URL 含 `check.html` 的标签页，**15s 内**轮询，满足以下**任一**条件即视为检测通过：

1. **「打开店铺」按钮未禁用**（`.openMallOpenBtn`，且非 `disabled` / `aria-disabled=true` / `is-disabled`）
2. **标签页数量 ≥ 2**（通常表示店铺页已打开）

15s 内仍不满足 → 告知「没检测成功无法进行自动化」，立即结束。

可运行 Skill 内置（**仅阶段 B**）：

```bash
node scripts/check_device_security.mjs --port {webdriver_port} --wait --timeout 15
```

### 业务自动化

检测通过后，按客户需求用 Playwright 操作页面。**禁止**在 Skill 目录新增业务脚本；临时逻辑在对话中执行，不落盘为 `.mjs`/`.js`。

---

## 收尾（阶段 A · HTTP）

**关闭店铺**（客户明确要求时）：

```json
{"action": "CloseBrowser", "module": "WebDriverModule", "browserId": "3514488"}
```

成功后**从 `opening_malls.json` 去掉该 `mall_name`**。

---

## 失败处理（统一）


| 情况                                                 | 动作                                                                                                                  |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 目标端口无 HTTP 响应 / 非站斧占用 / 无 Http.ini                     | **提示「请打开最新的站斧」并停止** |
| **打开店铺**（任意）                                      | 文首「仅开店」：禁止事先探测；`open_mall.mjs` → 一句话结束 |
| `GetBrowserList` 能取到数据 + **关闭店铺**                  | resolve mall_id → `CloseBrowser` → 清理 `opening_malls.json`                                                  |
| `open_mall.mjs` 返回 `zhanfu_down`                      | **提示「请打开最新的站斧」并停止**                                                                                         |
| 目标店铺已打开（客户要求**打开**）                                | 告知 `WebDriverPort` 并结束；**禁止**追问是否关闭；仅客户明确要求关店/重开才 `CloseBrowser` / 再开                                                              |
| OpenBrowser 前 `GetBrowserWebDriver` **1.5s 超时**      | **不结束**；继续 `OpenBrowser`（只许探测 1 次）                                                                                  |
| 客户明确要求关闭已开店铺                                       | 直接 `CloseBrowser` → 清理 `opening_malls.json`                                                                         |
| 客户要求打开/关闭/重启站斧客户端                                 | **本技能不支持** → 停止并说明                                                                                                          |
| GetBrowserList 8s 内仍无法确认登录（**非开店**且确认为站斧 WebDriver） | **停止**，提示客户提供账号密码；**禁止**擅自或内测账号 Login；**禁止**用 `LoadSuccess` 判断。若其实是非站斧占用，提示「请打开最新的站斧」 |
| OpenBrowser / OpenBrowser 后 GetBrowserWebDriver 失败 | 立即结束；`OpenBrowser` 以 `returnObj===true` 判成功；提醒检查 **IP/设备绑定** 及 **是否已手动打开该店铺下载内核**（版本要求：Windows ≥ 5.2.12，macOS > 5.2.10）                     |
| **macOS** 且 `KernalNumber ≤ 130`（打开/复用店铺后） | **立即停止**；按「macOS 低内核对客户话术」提示：切换到 **130 以上**内核或请**主账号**切换，并请客户**手动重启站斧**后再继续；**禁止**阶段 B |
| CloseBrowser 返回 `returnObj===false`                | 立即结束，报告关闭失败                                                                                                         |
| 其他关键 API 失败                                        | 立即结束，原样报告 `returnObj.msg`（`OpenBrowser`/`CloseBrowser` 无 `msg` 时报告 `returnObj` 值）                                   |
| OpenBrowser 后拿不到 WebDriverPort                     | 释放本地占位并结束，本轮不重开；下次客户明确开店时先探测已有端口，再尝试打开                                                                                                        |
| 仅开店却跑了设备安全检测 / 阶段 B                              | **禁止**；应拿到端口即停                                                                                                     |
| 设备安全检测 15s 超时                                      | 立即结束，告知「没检测成功无法进行自动化」（仅页面自动化）                                                                                               |
| CDP 连接失败                                           | 立即结束，禁止换浏览器                                                                                                         |


**禁止**：重试、翻代码、写备用脚本、写「稍后重跑」方案；**禁止**用 `LoadSuccess` 判断站斧是否已打开。

---

## 参考脚本（Agent 应按意图运行，禁止另写一次性脚本）

| 意图 | 命令 |
|------|------|
| 打开店铺 | `node scripts/open_mall.mjs --mall-name ztest126` |
| 关闭店铺 | `node scripts/close_mall.mjs --mall-name ztest126` |
| 店铺列表 | `node scripts/list_malls.mjs` |
| 登录 | `node scripts/login_zhanfu.mjs --username ... --password ...` |
| 创建店铺 | `node scripts/zhanfu_ops.mjs create-mall --mall-name ... --platform ...` |
| 改店铺账号 | `node scripts/zhanfu_ops.mjs update-account --mall-name ... --username ... --password ...` |
| 下载目录 | `node scripts/zhanfu_ops.mjs set-download --file-path D:\downloads` |
| 店铺插件 | `node scripts/zhanfu_ops.mjs set-plugins --plugin-name 紫竹自动化插件 --chrome-id ""` |
| 清缓存 | `node scripts/zhanfu_ops.mjs clear-cache --mall-name ztest126` 或 `--all` |

- [scripts/zhanfu_http.mjs](scripts/zhanfu_http.mjs) — 公共 HTTP 库（`browserId` 强制字符串）
- [scripts/zhanfu_playwright.mjs](scripts/zhanfu_playwright.mjs) — 全流程参考实现
- [scripts/check_device_security.mjs](scripts/check_device_security.mjs) — 阶段 B 设备检测
- [scripts/headed_mode.mjs](scripts/headed_mode.mjs) — 强制有界面

API 详情（含通用约定与全部接口）：[reference.md](reference.md)
