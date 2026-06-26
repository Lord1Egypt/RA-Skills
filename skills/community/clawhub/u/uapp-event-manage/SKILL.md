---
name: umeng-cli-uapp-event-manage
description: 友盟自定义事件管理技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 4 个事件管理接口（2 个写入 + 2 个只读），覆盖 App 单事件创建、小程序批量事件创建、App 事件列表、小程序事件列表。当用户需要创建埋点事件定义、批量创建小程序事件、验证事件是否已创建、查询自定义事件列表时使用。同时适用于 App（Android / iOS / HarmonyOS）与小程序 / H5 / 小游戏，按平台自动分流到 com.umeng.uapp 或 com.umeng.umini 命名空间。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# 友盟自定义事件管理技能

> `umeng-cli` 是友盟提供的命令行程序，所有操作通过执行 `umeng-cli call` 命令完成。

管理友盟自定义事件（埋点）定义，覆盖两类核心需求：

- **写入**：创建 App 类型单个事件、批量创建小程序事件（友盟小程序端无单创接口，单事件也走批量接口）
- **只读辅助**：查询 App / 小程序事件列表（用于创建前重复性预检、创建后 `--verify` 回查）

共 **4 个接口**（跨 `com.umeng.uapp` + `com.umeng.umini` 两个命名空间，按平台自动分流）：

| # | 接口 | 读/写 | 命名空间 | 能力 |
|---|---|---|---|---|
| 1 | `umeng.uapp.event.create` | ✏️ **写入** | `com.umeng.uapp` | App 类型创建单个自定义事件（`eventDisplayName` 中文自动 urlEncode）|
| 2 | `umeng.umini.batchCreateEvent` | ✏️ **写入** | `com.umeng.umini` | 小程序批量创建自定义事件（单事件也走此接口）|
| 3 | `umeng.uapp.event.list` | 📖 只读 | `com.umeng.uapp` | App 类型事件列表（用于 `--verify` 回查 / 创建前预检）|
| 4 | `umeng.umini.getEventList` | 📖 只读 | `com.umeng.umini` | 小程序事件列表（用于 `--verify` 回查 / 创建前预检）|

> 🔗 **与 `umeng-cli-uapp-event` 的边界分工**：本 Skill **仅覆盖事件定义管理（写入 + 列表）**；事件触发次数、独立用户、参数列表、参数取值分布等**只读统计查询**归属 `umeng-cli-uapp-event`。
> 🔗 **与 `umeng-cli-uapp-assets` 的边界分工**：查询"账户下都有哪些 App / 小程序"归属 `umeng-cli-uapp-assets`；本 Skill 以 `appkey` / `dataSourceId` 为**输入**。
> ⚠️ **不支持的操作**：友盟 OpenAPI **不提供**事件删除、事件重命名、事件显示名编辑接口，Skill 也不承担这些能力。

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-event-manage"}'
> ```
>
> **Appkey 维度打点：** 当本轮任务中出现 Appkey（`appkey` 或小程序 `dataSourceId`）的输入操作时，在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-event-manage", "appkey":"<输入的Appkey>"}'
> ```
> 同一 Appkey 在同一会话中只打一次；若用户切换到新的 Appkey，需对新的 Appkey 再打一次。

## ⚠️ 写入风险提示（本 Skill 含 2 个写入接口）

`umeng.uapp.event.create` 和 `umeng.umini.batchCreateEvent` 均为**变更类操作**，会在用户账号下实际创建不可删除、不可重命名的事件定义（友盟 OpenAPI 未开放删除/编辑接口）。调用前**强制**遵循以下规范：

1. **参数完整校验**：`appkey` / `dataSourceId` + `eventName` + `eventDisplayName` 三者必须同时确认。
2. **命名规范校验（本地先校验，不满足不得调用）**：
   - `eventName`：正则 `^[a-zA-Z0-9_]+$`，**禁止**特殊字符 `? / . \ < >` 和空格、中文
   - `eventDisplayName`：允许中文 + 英文 + 数字 + 下划线，**禁止**特殊字符 `? / . \ < >`
3. **创建前预检（强烈建议）**：先调 `event.list` / `getEventList`，确认 `eventName` **不重复**再写入；重复创建可能报错或生成混淆记录。
4. **向用户复述并二次确认**：执行前应以自然语言向用户复述"将为 <应用名> 创建事件「<eventName>」（显示名「<eventDisplayName>」）"，获得明确"确认/继续"后再执行；批量场景需列出完整事件清单供用户核对。
5. **失败语义**：返回 `status != 0`（App）或 `success=false` / `code != 0`（小程序）时，不要自动重试写入；将 `msg` 原文透传给用户。
6. **创建后同步延迟**：事件同步需数秒，立即调 `--verify`（`event.list`）可能返回"不存在"；建议延迟 3–5 秒后再回查，或一次性延迟后核对全部事件名。
7. **不可撤销**：友盟 OpenAPI 不提供事件删除 / 重命名 / 显示名编辑接口；创建错了只能忍受历史残留，务必在写入前完成二次确认。

## 前置条件：安装 umeng-cli

本 Skill 的所有调用都依赖 `umeng-cli` 命令行工具。使用本 Skill 前，请先确保已在本机安装。

### 检查是否已安装

```bash
umeng-cli --version
```

若提示 `command not found` 或类似错误，按下述方式安装。

### 安装方式

```bash
# 方式一：通过 npm 安装（推荐，自动安装 CLI + 内置 Skills）
npm install -g @umengfe/umeng-cli

# 方式二：通过官方安装脚本（仅安装 CLI 二进制 + Skills）
curl -fsSL https://raw.githubusercontent.com/umeng/umeng-cli/main/scripts/install.sh | sh
```

安装完成后再次运行 `umeng-cli --version` 验证。

> 更多安装说明、卸载、账号管理等参考 [umeng-cli SKILL](../../../umeng-cli/SKILL.md) 或项目主页 https://github.com/umeng/umeng-cli

## 适用场景与触发词

- 用户要求"创建一个叫 xxx 的事件" / "添加埋点" / "新增一个自定义事件"
- 用户要求"批量创建这几个小程序事件" / 提供 JSON 清单一次性创建
- 用户要求"验证某事件是否已经创建"（走事件列表回查）
- 用户要求"查看当前应用有哪些自定义事件"（事件定义清单，与"事件统计"区分）
- 关键词：创建事件、添加埋点、批量创建事件、事件列表、自定义事件管理、新增埋点、事件创建、event.create、batchCreateEvent、显示名、eventName、displayName

## 鉴权方式

- **authType**: `umeng-aksk`（友盟 OpenAPI AK/SK 签名，HMAC-SHA1）
- **baseUrl**: `https://gateway.open.umeng.com/openapi`
- **endpoint 路径规则**：
  - App 接口：`param2/1/com.umeng.uapp/<接口名>`
  - 小程序接口：`param2/1/com.umeng.umini/<接口名>`
- AK/SK 由 `umeng-cli login` 自动获取并加密缓存，无需手动配置 `apiKey` / `apiSecurity`

### 登录状态检查

```bash
umeng-cli whoami
```

### 登录要求

当接口返回未登录或登录态过期时，需要执行 `umeng-cli login --no-qr` 进行登录。

**AI Agent 执行登录的正确方式：**

> `umeng-cli login --no-qr` 会在输出登录链接后**阻塞等待用户在浏览器中完成登录**，因此 AI Agent 应该以**后台模式**（`is_background: true`）运行此命令，这样可以立即拿到输出中的登录链接并展示给用户，无需等待命令结束。命令会在用户完成登录后自动退出并保存凭证。

如果终端不支持显示二维码（如 AI Agent 终端、SSH 远程终端等），可以使用 `--no-qr` 参数，仅输出可点击的登录链接：

```bash
umeng-cli login --no-qr

# 输出:
# 🔄 正在生成登录链接...
# ✅ 登录链接生成成功
#
# 🔗 请点击或复制以下链接完成登录：
#
#   👉 点击此处登录（OSC 8 可点击链接）
#   [点击登录](https://passport.umeng.com/login?redirectURL=...)
#   https://passport.umeng.com/login?redirectURL=...
#
# ⏳ 等待登录...
# ✅ 授权成功！
# ✅ 登录完成！
```

## 平台分流规则（强制）

本 Skill **同时适用于 App 和小程序**，根据 `platform` 自动选择命名空间与接口：

| `platform` 枚举 | 分类 | 写入接口 | 列表接口 |
|---|---|---|---|
| `android` / `iphone` / `ipad` / `harmonyos` | App | `umeng.uapp.event.create`（仅单事件）| `umeng.uapp.event.list` |
| `mini_wechat` | 微信小程序 | `umeng.umini.batchCreateEvent`（单 / 批量均用）| `umeng.umini.getEventList` |
| `mini_alipay` / `mini_bytedance` / `mini_baidu` / `mini_qq` | 其他小程序 | 同上 | 同上 |
| `mini_game_wechat` | 微信小游戏 | 同上 | 同上 |
| `html_5` | H5 | 同上 | 同上 |

**关键差异**：

- **App 类型无批量接口**：批量创建请循环调用 `umeng.uapp.event.create`
- **小程序无单创接口**：即使只创建 1 个事件，也走 `umeng.umini.batchCreateEvent`（`eventList` 传长度为 1 的数组）
- **App 的 `eventDisplayName` 中文需 urlEncode**（由 `umeng-cli` 内部处理，LLM 传原始中文即可）
- **小程序的 `eventList` 中 `displayName` 直接传原始中文**（小程序批量接口不要求手工 encode）

## 4 个接口速查表

| 接口 | 类型 | 必填参数 | 典型用途 |
|---|---|---|---|
| `umeng.uapp.event.create` | ✏️ 写入 | `appkey` / `eventName` / `eventDisplayName` | App 单事件创建（可选 `eventType`：`true`=计算 / `false`=计数，默认 false）|
| `umeng.umini.batchCreateEvent` | ✏️ 写入 | `dataSourceId` / `eventList`（`[{"eventName","displayName"}]`）| 小程序单 / 批量事件创建 |
| `umeng.uapp.event.list` | 📖 只读 | `appkey` / `startDate` / `endDate`（可选 `page` / `perPage` / `version`）| App 事件列表 / 回查 |
| `umeng.umini.getEventList` | 📖 只读 | `dataSourceId` | 小程序事件列表 / 回查 |

**公共约束**：

- `eventName`：`^[a-zA-Z0-9_]+$`，禁止 `? / . \ < >` 和空格、中文
- `eventDisplayName` / `displayName`：允许中文 + 英文 + 数字 + 下划线，禁止 `? / . \ < >`
- `eventType`（仅 App 可用）：`true` = 计算事件（数值型，用于累计值/均值/分布）；`false` = 计数事件（字符串型，统计消息数 + 触发设备数）；不传默认 `false`
- 小程序端**没有 eventType 概念**，`batchCreateEvent` 不接受此字段

---

## 接口 1：`umeng.uapp.event.create` — App 创建自定义事件（⚠️ 写入）

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `appkey` | String | 是 | 应用 AppKey |
| `eventName` | String | 是 | 事件英文名，满足 `^[a-zA-Z0-9_]+$` |
| `eventDisplayName` | String | 是 | 事件显示名（支持中文；由 umeng-cli 内部 urlEncode）|
| `eventType` | Boolean | 否 | `true`=计算事件（数值型），`false`=计数事件（字符串型）；默认 `false` |

### 调用示例

```bash
# 计数事件（默认）
umeng-cli call '{"name":"umeng.uapp.event.create","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.event.create","authType":"umeng-aksk"}}' '{"appkey":"5f8a123456789abcdef01234","eventName":"purchase_click","eventDisplayName":"购买点击"}'

# 计算事件（数值型）
umeng-cli call '{"name":"umeng.uapp.event.create","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.event.create","authType":"umeng-aksk"}}' '{"appkey":"5f8a123456789abcdef01234","eventName":"purchase_amount","eventDisplayName":"购买金额","eventType":true}'
```

### 返回字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `status` | integer | 响应码，`0` 表示成功 |
| `msg` | string | 响应信息 |

### 成功 / 失败判定

- 成功：`status == 0`
- 失败：`status != 0`，将 `msg` 原文透传给用户，不要自动重试

---

## 接口 2：`umeng.umini.batchCreateEvent` — 小程序批量创建事件（⚠️ 写入）

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |
| `eventList` | eventDTO[] | 是 | 事件列表，结构：`[{"eventName":"...","displayName":"..."}]` |

**`eventDTO[]` 结构：**

| 字段 | 类型 | 说明 |
|---|---|---|
| `eventName` | String | 事件英文名，满足 `^[a-zA-Z0-9_]+$` |
| `displayName` | String | 事件显示名（支持中文原文，不需手工 encode）|

### 调用示例

```bash
# 单事件（长度为 1 的数组）
umeng-cli call '{"name":"umeng.umini.batchCreateEvent","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.batchCreateEvent","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","eventList":[{"eventName":"view_page","displayName":"浏览页面"}]}'

# 批量事件
umeng-cli call '{"name":"umeng.umini.batchCreateEvent","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.batchCreateEvent","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","eventList":[{"eventName":"click_btn","displayName":"点击按钮"},{"eventName":"view_page","displayName":"浏览页面"}]}'
```

### 返回字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `success` | Boolean | 是否成功 |
| `code` | Long | 状态码，`0` / `200` 表示成功 |
| `data` | String | 数据返回结果（成功时为新建事件数量或事件 ID 摘要）|
| `msg` | String | 响应信息 |

### 成功 / 失败判定

- 成功：`success == true` 且 `code` 为成功码（`0` 或 `200`）
- 失败：整个请求失败；**友盟批量接口目前不返回每个事件的单独成败**，对失败用户应建议逐个改用 N=1 重试以定位问题事件
- 不要自动重试整个批量请求

---

## 接口 3：`umeng.uapp.event.list` — App 事件列表（📖 只读）

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `appkey` | String | 是 | 应用 AppKey |
| `startDate` | String | 是 | 查询起始日期（`YYYY-MM-DD`，建议近 30 天）|
| `endDate` | String | 是 | 查询截止日期（`YYYY-MM-DD`，建议昨日）|
| `page` | Integer | 否 | 页号，默认 1 |
| `perPage` | Integer | 否 | 每页数量，最大 100，默认 10 |
| `version` | String | 否 | 按版本过滤 |

### 调用示例

```bash
umeng-cli call '{"name":"umeng.uapp.event.list","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.event.list","authType":"umeng-aksk"}}' '{"appkey":"5f8a123456789abcdef01234","startDate":"2026-03-29","endDate":"2026-04-27","perPage":100}'
```

### 返回字段

| 字段 | 类型 | 说明 |
|---|---|---|
| `eventInfo` | EventInfo[] | 事件列表 |
| `page` | integer | 当前页数 |
| `totalPage` | integer | 总页数 |

**`EventInfo[]` 结构：** `name`（事件英文名）/ `displayName`（中文显示名）/ `count`（统计次数）/ `id`（事件 ID）

### 回查用法

```text
创建 eventName="purchase_click" 后：
  → 循环拉取全部分页
  → 判断 eventInfo[].name == "purchase_click" 是否存在
  → 存在 = 回查成功
```

---

## 接口 4：`umeng.umini.getEventList` — 小程序事件列表（📖 只读）

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |

### 调用示例

```bash
umeng-cli call '{"name":"umeng.umini.getEventList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getEventList","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91"}'
```

### 返回字段

返回结构为嵌套 `data.data[]`（也可能直接 `data[]`，需客户端兼容两种形态）：

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.data[].eventName` | String | 事件英文名 |
| `data.data[].displayName` | String | 中文显示名 |

### 回查用法

```text
创建 eventName="view_page" 后：
  → 调用 getEventList
  → 展开 data.data 或 data 数组
  → 判断其中某项 eventName == "view_page"
  → 存在 = 回查成功
```

---

## 典型工作流（W1–W5）

### W1：App 单事件创建 + 回查验证

```text
1. 确认 appkey（必要时用 umeng-cli-uapp-assets 查询）
2. 本地校验 eventName / eventDisplayName 是否合法
3. 调用 umeng.uapp.event.list 预检（可选但推荐）—— 若事件已存在则提醒并停止
4. 向用户复述并二次确认
5. 调用 umeng.uapp.event.create
6. 判断 status == 0，失败则透传 msg 不重试
7. 等待 3–5 秒
8. 调用 umeng.uapp.event.list 回查 eventName 是否出现
```

### W2：小程序单事件创建（走批量接口 N=1）

```text
1. 确认 dataSourceId
2. 本地校验 eventName / displayName
3. （可选）调用 umeng.umini.getEventList 预检
4. 向用户复述并二次确认
5. 调用 umeng.umini.batchCreateEvent，eventList=[{"eventName":"...","displayName":"..."}]
6. 判断 success == true 且 code 为成功码
7. 等待 3–5 秒
8. 调用 umeng.umini.getEventList 回查
```

### W3：小程序批量事件创建 + 回查校对

```text
1. 获取用户提供的事件清单（JSON 数组或用户口述）
2. 本地逐项校验 eventName / displayName
3. 去重：按 eventName 去重
4. 调用 umeng.umini.getEventList 预检并剔除已存在项
5. 向用户列出完整待创建清单，请求二次确认
6. 调用 umeng.umini.batchCreateEvent
7. 失败时建议用户将失败批改为 N=1 逐个试，以定位问题事件（整批失败不自动重试）
8. 等待 3–5 秒
9. 再调 umeng.umini.getEventList 核对每个 eventName 是否存在
```

### W4：创建前重复性预检（避免重复创建）

```text
场景：用户要求"创建 purchase_click 事件"
  → 先调事件列表（App 走 event.list，小程序走 getEventList）
  → 搜索目标 eventName
  → 已存在 → 告知用户"事件已存在，无需创建"
  → 不存在 → 按 W1 / W2 流程继续
```

### W5：跨平台事件清单盘点

```text
1. 调用 umeng-cli-uapp-assets 获取账户下 App + 小程序列表
2. 对 App 类 appkey 调用 umeng.uapp.event.list
3. 对小程序类 dataSourceId 调用 umeng.umini.getEventList
4. 客户端合并 + 去重输出
（注意：两接口响应字段不同，App 用 name，小程序用 eventName，合并时需要映射）
```

## 字段别名与旧参数对照表

| 旧 CLI 参数（`uapp-event-manage`）| 新接口字段 | 说明 |
|---|---|---|
| `--create EVENT_NAME` | `eventName`（`event.create`）/ `eventList[].eventName`（`batchCreateEvent`）| 事件英文名 |
| `--display-name` | `eventDisplayName`（App）/ `eventList[].displayName`（小程序）| 中文显示名 |
| `--event-type true\|false` | `eventType`（仅 App）| 小程序无对应字段 |
| `--batch-create --events '[...]'` | `eventList`（小程序 `batchCreateEvent` 的参数）| 直接传 JSON 数组 |
| `--batch-create --from-file events.json` | 客户端读文件后填入 `eventList` | umeng-cli 无文件读取语法糖 |
| `--list-events` | `event.list` / `getEventList` | 按平台分流 |
| `--verify` | 创建后延迟 3–5 秒再调 `event.list` / `getEventList` 回查 | 不再有单独参数，由 LLM 工作流编排 |
| `--app "应用名"` → 内部解析 `appkey` | `appkey`（App）/ `dataSourceId`（小程序）| 由 LLM 从 `umeng-cli-uapp-assets` 获取 |
| 客户端 urlEncode 中文显示名 | 由 umeng-cli 内部处理 | LLM 只传原始中文 |

## 边界与异常处理

| 情形 | 处理方式 |
|---|---|
| 用户未说应用名 | 先询问，**不要猜测**；必要时调用 `umeng-cli-uapp-assets` 列出候选 |
| App 名找不到 | 提示"可用 `umeng-cli-uapp-assets` 查询全部应用列表" |
| `eventName` 包含禁止字符 | 本地直接拒绝，列出合法正则，要求用户修正 |
| `eventDisplayName` 包含禁止字符 | 本地直接拒绝，要求修正 |
| App 类型用户要求批量创建 | 明确告知"App 类型无批量接口，需逐个创建"，询问是否继续按逐个模式执行 |
| 小程序类型用户只创建 1 个事件 | 直接走 `batchCreateEvent`（`eventList` 长度为 1），向用户说明无单创接口 |
| 创建后立即 `--verify` 返回不存在 | 告知"事件同步需数秒，延迟 3–5 秒后再回查" |
| 创建失败返回 `status != 0` / `success=false` | 透传 `msg`，不自动重试；若需诊断，引导用户检查命名是否冲突或平台是否匹配 |
| 小程序批量写入整体失败 | 建议改为 N=1 逐个创建以定位问题事件，不自动整批重试 |
| 用户要求删除 / 重命名 / 改显示名 | 明确告知"友盟 OpenAPI 不支持事件删除 / 重命名 / 编辑显示名，Skill 无此能力" |
| `eventType` 传成字符串 `"true"` / `"false"` | API 层期望 Boolean，建议传入 JSON 原生 `true` / `false`；若 CLI 客户端要求字符串，按其文档约定 |
| H5 应用 | 归为小程序分类，走 `batchCreateEvent` / `getEventList` |
| App 事件列表分页溢出 | 按 `totalPage` 循环拉取，客户端合并（`perPage` 最大 100）|

## 典型问法与内部意图映射

| 典型问法 | 对应接口 / 工作流 |
|---|---|
| "给 Android_Demo 创建一个叫 purchase_click 的事件，显示名叫购买点击" | `umeng.uapp.event.create`（W1）|
| "创建一个叫 purchase_amount 的数值型事件" | `umeng.uapp.event.create` + `eventType=true` |
| "给小程序『友小盟数据官』批量创建这几个事件：…" | `umeng.umini.batchCreateEvent`（W3）|
| "view_page 这个事件创建好了吗？" | `event.list` 或 `getEventList` 回查（W4）|
| "当前应用有哪些自定义事件？" | 按平台 → `event.list` / `getEventList`（纯只读展示）|
| "把 xxx 事件删掉" | 明确告知不支持 |

## 快速自检清单

调用前自检：

- [ ] 平台类型已确认，走正确命名空间（App→`com.umeng.uapp`，小程序/H5→`com.umeng.umini`）
- [ ] `appkey` / `dataSourceId` 已拿到（必要时先走 `umeng-cli-uapp-assets`）
- [ ] `eventName` 满足 `^[a-zA-Z0-9_]+$`
- [ ] `eventDisplayName` / `displayName` 不含 `? / . \ < >`
- [ ] 写入前已做重复性预检（`event.list` / `getEventList`）
- [ ] 写入前已向用户复述并二次确认
- [ ] 失败时不自动重试写入
- [ ] 写入成功后延迟 3–5 秒再做回查

调用后自检：

- [ ] App：`status == 0` 判成功；小程序：`success == true` 且 `code` 为成功码
- [ ] 已执行回查（`event.list` / `getEventList`）并反馈给用户
- [ ] 用户要求删除 / 重命名时明确告知不支持
