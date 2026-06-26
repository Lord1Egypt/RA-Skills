---
name: umeng-cli-uapp-mini-channel
description: 友盟小程序推广渠道/活动/场景效果分析技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 5 个只读接口，覆盖获客来源排行、渠道/活动/场景值明细统计与趋势分析。当用户需要了解小程序的获客来源、渠道/活动/场景效果、Top 排行、趋势分析时使用。触发词：获客来源、推广渠道、推广活动、场景分析、渠道排行、活动效果、场景值、渠道趋势、活动趋势。仅适用于小程序 / H5 / 小游戏，不支持 Android/iOS App。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# 友盟小程序推广渠道/活动/场景效果分析技能

> `umeng-cli` 是友盟提供的命令行程序，所有操作通过执行 `umeng-cli call` 命令完成。

分析友盟小程序（U-MiniProgram）的**获客来源与推广效果**，覆盖：

- 获客来源排行（渠道 / 活动 / H5 场景 / 其他场景）
- 指定渠道 / 活动 / 场景值的明细统计与趋势分析
- 推广资产清单查询（取推广链接 URL 或展示用）

共 **5 个接口**（命名空间 `com.umeng.umini`，**全部为只读查询**）：

| # | 接口 | 读/写 | 能力 |
|---|---|---|---|
| 1 | `umeng.umini.getCustomerSourceOverview` | 📖 只读 | **获客来源排行**（按 `sourceType` 分档：渠道/活动/H5场景/其他场景） |
| 2 | `umeng.umini.getChannelOverview` | 📖 只读 | 指定**推广渠道**的明细统计 / 趋势 |
| 3 | `umeng.umini.getCampaignOverview` | 📖 只读 | 指定**推广活动**的明细统计 / 趋势 |
| 4 | `umeng.umini.getSceneOverview` | 📖 只读 | 指定**场景值**的明细统计 / 趋势（H5 不支持） |
| 5 | `umeng.umini.getSceneInfoList` | 📖 只读 | 推广活动/渠道清单（含完整 `url`） |

> ⚠️ **本 Skill 全部接口为只读查询**，无写入风险；推广链接的**创建**由 `umeng-cli-uapp-campaign` 覆盖。

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-mini-channel"}'
> ```
>
> **Appkey 维度打点：** 当本轮任务中出现 Appkey（小程序 `dataSourceId`）的输入操作时，在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-mini-channel", "appkey":"<输入的Appkey>"}'
> ```
> 同一 Appkey 在同一会话中只打一次；若用户切换到新的 Appkey，需对新的 Appkey 再打一次。

## ⚠️ 适用范围限制（强制）

本 Skill **仅适用于小程序 / H5 / 小游戏**类应用：

| 应用类型 | 是否适用 | 说明 |
|---|---|---|
| 微信 / 支付宝 / 字节 / 百度 / QQ 小程序 | ✅ | 完全适用 |
| 微信小游戏（`mini_game_wechat`） | ✅ | 适用 |
| H5（`html_5`） | ⚠️ 部分适用 | `getSceneOverview` 不支持；`launch` / `onceDuration` 字段不支持；需改用 `sourceType=platform`（H5 场景）查询 |
| Android App（`android`） | ❌ | **不适用**，请改用 `umeng-cli-uapp-channel-version`（App 渠道效果） |
| iOS App（`iphone`） | ❌ | 同上 |

当用户对 Android / iOS App 询问"渠道/活动效果"时，应明确告知：「本 Skill 仅限小程序 / H5 / 小游戏；App 渠道请用 `umeng-cli-uapp-channel-version`」。

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

- 「各推广渠道昨天带来了多少用户？」→ 排行
- 「XX 活动最近 7 天的效果趋势」→ 活动趋势
- 「某场景值（如 `wx_1011` 扫码）的数据」→ 场景明细
- 「H5 的场景来源排行」→ `sourceType=platform`
- 关键词：获客来源、推广渠道、推广活动、场景分析、渠道排行、活动效果、场景值、渠道趋势、活动趋势、Top N 渠道

## 鉴权方式

- **authType**: `umeng-aksk`（友盟 OpenAPI AK/SK 签名，HMAC-SHA1）
- **baseUrl**: `https://gateway.open.umeng.com/openapi`
- **endpoint 路径规则**: `param2/1/com.umeng.umini/<接口名>`
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

## 为什么必须提供 `dataSourceId`（appkey）

本 Skill **5 个接口都必须传入 `dataSourceId`**（即小程序的 AppKey），因为统计作用域是"单个小程序"而不是"账号"。

若用户未提供 appkey：
1. **优先**引导使用 `umeng-cli-uapp-assets` 查询小程序列表，取得 `dataSourceId`：
   ```bash
   umeng-cli call '{"name":"umeng.umini.getAppList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getAppList","authType":"umeng-aksk"}}' '{"pageIndex":1,"pageSize":100}'
   ```
2. **备选**引导用户从友盟官网 [web.umeng.com](https://web.umeng.com) → U-MiniProgram → 应用列表 → 复制 AppKey 获取。

## 🔴 关键字段告警：`channel` / `campaign` 参数必须用 `getCustomerSourceOverview.id`

调用接口 2（`getChannelOverview`）与接口 3（`getCampaignOverview`）时，必填的 `channel` / `campaign` 参数需要**渠道/活动的内部 ID（26 位）**。获取方式分两档：

| 来源 | 取哪个字段 | 是否可直接用于明细接口 |
|---|---|---|
| 接口 1 `getCustomerSourceOverview` | `data[].id`（26 位 id） | ✅ **可直接使用** |
| 接口 5 `getSceneInfoList` | `data[].code`（25 位活动/渠道代码） | ❌ **不匹配**，不要把 `code` 传给 `channel`/`campaign` 参数 |

> 实战经验：旧脚本曾踩坑——用 `getSceneInfoList.code` 直接喂给 `getChannelOverview.channel` 会导致 0 数据返回。正确做法是**用 `getCustomerSourceOverview` 做"列表+取 id" 的一站式查询**，见 W3 工作流。
>
> `getSceneInfoList` 仅适用于需要**完整推广链接 URL** 的展示场景（其 `url` 字段不可替代）。

## 5 个接口速查表

| 接口 | 必填参数 | H5 支持 | 分页 | 典型用途 |
|---|---|---|---|---|
| `getCustomerSourceOverview` | `dataSourceId` / `sourceType` / `fromDate` / `toDate` / `timeUnit` | ✅（`sourceType=platform`） | ❌ | 获客来源排行 + 取 `id` |
| `getChannelOverview` | `dataSourceId` / `channel` / `fromDate` / `toDate` / `timeUnit` / `indicators` | ⚠️ `launch`/`onceDuration` 不支持 | `pageIndex` / `pageSize` | 渠道明细趋势 |
| `getCampaignOverview` | `dataSourceId` / `campaign` / `fromDate` / `toDate` / `timeUnit` / `indicators` | ⚠️ 同上 | 同上 | 活动明细趋势 |
| `getSceneOverview` | `dataSourceId` / `scene` / `fromDate` / `toDate` / `timeUnit` / `indicators` | ❌ **整体不支持** | 同上 | 场景值明细趋势 |
| `getSceneInfoList` | `dataSourceId` / `sourceType` | ✅ | ❌ | 取推广链接 `url` 或展示清单 |

### 公共枚举（抽到顶部，避免每个接口重复）

- **`sourceType`**（仅接口 1、5）：
  - 接口 1（`getCustomerSourceOverview`）：`campaign`（活动）/ `channel`（渠道）/ `platform`（H5 场景）/ `scene`（其他场景）
  - 接口 5（`getSceneInfoList`）：`campaign` / `channel`
- **`timeUnit`**（接口 1–4）：`5min` / `hour` / `day` / `7day` / `30day`（接口 1 仅支持 `day,7day,30day`）
- **`indicators`**（接口 2–4，逗号分隔）：`newUser` / `activeUser` / `launch`（H5 不支持）/ `visitTimes` / `onceDuration`（H5 不支持）
- **`orderBy`**（接口 1）：`newUser` / `activeUser` / `launch` / `visitTimes` / `onceDuration` / `createDateTime`
- **`direction`**（接口 1）：`asc` / `desc`（默认 `desc`）

---

## 接口 1：`umeng.umini.getCustomerSourceOverview` — 获客来源排行

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |
| `sourceType` | String | 是 | `campaign` / `channel` / `platform` / `scene` |
| `fromDate` | String | 是 | 开始日期 `yyyy-MM-dd` |
| `toDate` | String | 是 | 结束日期 `yyyy-MM-dd` |
| `timeUnit` | String | 是 | `day` / `7day` / `30day` |
| `orderBy` | String | 否 | 默认 `newUser` |
| `direction` | String | 否 | 默认 `desc` |

### 调用示例

```bash
# 渠道排行（默认，昨天）
umeng-cli call '{"name":"umeng.umini.getCustomerSourceOverview","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getCustomerSourceOverview","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","sourceType":"channel","fromDate":"2026-04-27","toDate":"2026-04-27","timeUnit":"day"}'

# 活动排行（按活跃用户降序）
umeng-cli call '{"name":"umeng.umini.getCustomerSourceOverview",...}' '{"dataSourceId":"1dfe...","sourceType":"campaign","fromDate":"2026-04-27","toDate":"2026-04-27","timeUnit":"day","orderBy":"activeUser"}'

# H5 场景排行
umeng-cli call '{"name":"umeng.umini.getCustomerSourceOverview",...}' '{"dataSourceId":"1dfe...","sourceType":"platform","fromDate":"2026-04-27","toDate":"2026-04-27","timeUnit":"day"}'
```

### 返回字段（`data[]` 数组）

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | String | **内部 ID（26 位），可直接作为接口 2/3 的 `channel`/`campaign` 参数** |
| `name` | String | 渠道/活动/场景名称 |
| `url` | String | 推广链接 URL（仅推广活动可用） |
| `newUser` | Long | 新增用户 |
| `activeUser` | Long | 活跃用户 |
| `launch` | Long | 打开次数（H5 不支持） |
| `visitTimes` | Long | 页面访问次数 |
| `onceDuration` | String | 次均停留时长（H5 不支持） |
| `createDateTime` | String | 创建时间（仅推广活动可用） |

---

## 接口 2：`umeng.umini.getChannelOverview` — 指定渠道明细/趋势

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |
| `channel` | String | 是 | **渠道 ID**，从接口 1 `getCustomerSourceOverview.data[].id` 获取（⚠️ 不要用接口 5 的 `code`） |
| `fromDate` | String | 是 | 开始日期 `yyyy-MM-dd` |
| `toDate` | String | 是 | 结束日期 `yyyy-MM-dd` |
| `timeUnit` | String | 是 | `5min` / `hour` / `day` / `7day` / `30day` |
| `indicators` | String | 是 | 逗号分隔，`newUser,activeUser,launch,visitTimes,onceDuration` |
| `pageIndex` | Integer | 否 | 默认 1 |
| `pageSize` | Integer | 否 | 默认 30 |

### 调用示例

```bash
# 某渠道过去 7 天活跃用户趋势
umeng-cli call '{"name":"umeng.umini.getChannelOverview","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getChannelOverview","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","channel":"5e8c6dea978eea071c37c68201","fromDate":"2026-04-21","toDate":"2026-04-27","timeUnit":"day","indicators":"activeUser,newUser,visitTimes"}'
```

### 返回字段（`data.data[]`）

| 字段 | 类型 | 说明 |
|---|---|---|
| `dateTime` | String | 时间 |
| `newUser` | Long | 新增用户 |
| `activeUser` | Long | 活跃用户 |
| `launch` | Long | 打开次数（H5 不支持） |
| `visitTimes` | Long | 页面访问次数 |
| `onceDuration` | String | 次均停留时长（H5 不支持） |

> 数据按 `dateTime` **降序**排列（最新日期在前）。做趋势分析时，`data[-1]` 为初期值、`data[0]` 为末期值。

---

## 接口 3：`umeng.umini.getCampaignOverview` — 指定活动明细/趋势

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |
| `campaign` | String | 是 | **活动 ID**，从接口 1 `getCustomerSourceOverview.data[].id` 获取（⚠️ 不要用接口 5 的 `code`） |
| `fromDate` | String | 是 | 开始日期 |
| `toDate` | String | 是 | 结束日期 |
| `timeUnit` | String | 是 | `5min` / `hour` / `day` / `7day` / `30day` |
| `indicators` | String | 是 | 同接口 2 |
| `pageIndex` / `pageSize` | Integer | 否 | 默认 1 / 30 |

### 调用示例

```bash
# 某活动过去 30 天新增用户趋势
umeng-cli call '{"name":"umeng.umini.getCampaignOverview","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getCampaignOverview","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","campaign":"5e8c6dea978eea071c37c68202","fromDate":"2026-03-29","toDate":"2026-04-27","timeUnit":"day","indicators":"newUser"}'
```

返回字段结构与接口 2 一致（`refererIndicatorDTO[]`）。

---

## 接口 4：`umeng.umini.getSceneOverview` — 指定场景值明细/趋势（⚠️ H5 不支持）

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |
| `scene` | String | 是 | 场景值编码（如 `wx_1011` 扫二维码、`alipay_1090`）；见 [友盟场景值文档](https://developer.umeng.com/docs/147615/detail/175369) |
| `fromDate` | String | 是 | 开始日期 |
| `toDate` | String | 是 | 结束日期 |
| `timeUnit` | String | 是 | `5min` / `hour` / `day` / `7day` / `30day` |
| `indicators` | String | 是 | 同接口 2 |
| `pageIndex` / `pageSize` | Integer | 否 | 默认 1 / 30 |

### 调用示例

```bash
# 微信扫二维码场景过去 7 天数据
umeng-cli call '{"name":"umeng.umini.getSceneOverview","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getSceneOverview","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","scene":"wx_1011","fromDate":"2026-04-21","toDate":"2026-04-27","timeUnit":"day","indicators":"newUser,activeUser,visitTimes"}'
```

> ⚠️ **H5 整体不支持本接口**：若应用是 `html_5` 平台，应改用接口 1 的 `sourceType=platform` 查询 H5 场景来源。

返回字段结构与接口 2 一致。

---

## 接口 5：`umeng.umini.getSceneInfoList` — 推广活动/渠道清单（含 URL）

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |
| `sourceType` | String | 是 | `campaign`（活动） / `channel`（渠道） |

### 调用示例

```bash
# 活动清单（含完整 url）
umeng-cli call '{"name":"umeng.umini.getSceneInfoList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getSceneInfoList","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","sourceType":"campaign"}'
```

### 返回字段（`data[]`）

| 字段 | 类型 | 说明 |
|---|---|---|
| `code` | String | ⚠️ **25 位活动/渠道代码**，**不能**作为接口 2/3 的 `channel`/`campaign` 参数 |
| `name` | String | 活动/渠道中文名 |
| `url` | String | 完整推广链接 URL（**仅活动有**，渠道通常为空） |
| `createDateTime` | String | 创建时间 |

> **本接口的唯一高价值字段是 `url`**（展示推广链接用）；取 ID 请用接口 1。

---

## 典型问法与内部意图映射

| 典型问法 | 接口 | 关键参数 |
|---|---|---|
| 「各推广渠道昨天带来了多少用户？」 | 接口 1 | `sourceType=channel` |
| 「小程序 Top 10 活动效果？」 | 接口 1 | `sourceType=campaign`, `orderBy=activeUser` |
| 「微信扫码场景（`wx_1011`）今天数据？」 | 接口 4 | `scene=wx_1011` |
| 「H5 各场景来源对比」 | 接口 1 | `sourceType=platform`（**H5 专用**） |
| 「某渠道过去 7 天活跃用户趋势」 | 接口 3 | 先接口 1 取 `id`，再接口 2 + `timeUnit=day` |
| 「某活动过去 30 天新增趋势」 | 接口 1 → 接口 3 | 同上 |
| 「给我推广链接 URL 看看」 | 接口 5 | `sourceType=campaign` 取 `url` |

---

## 工作流

### W1：获客来源 Top N 排行（最常用）

**目标**：一次返回「昨天」或「最近 N 天」的渠道/活动/场景排行。

```bash
# 渠道排行昨天 Top 10
umeng-cli call '{"name":"umeng.umini.getCustomerSourceOverview",...}' '{"dataSourceId":"...","sourceType":"channel","fromDate":"2026-04-27","toDate":"2026-04-27","timeUnit":"day","orderBy":"newUser","direction":"desc"}'
```

**输出处理**：按 `data[]` 前 N 个条目展示「名称 / 新增 / 活跃 / 打开次数」，指出 Top 1 的关键数据。

### W2：指定渠道/活动/场景的明细与趋势

**目标**：对已知 ID 的渠道/活动，或已知场景值编码，查看时间序列数据。

```bash
# 示例：某渠道过去 7 天
umeng-cli call '{"name":"umeng.umini.getChannelOverview",...}' '{"dataSourceId":"...","channel":"<从W3取到的id>","fromDate":"2026-04-21","toDate":"2026-04-27","timeUnit":"day","indicators":"newUser,activeUser,visitTimes"}'
```

**趋势解读**：数据降序排列 → `data[0]`=末期值，`data[-1]`=初期值；(末-初)/初 计算涨跌幅。

### W3：先排行取 id，再查明细（必走）

**目标**：用户给出渠道/活动**中文名称**（非 ID）时的标准流程，**避开 `getSceneInfoList.code` 不可用陷阱**。

**步骤**：
1. 调用接口 1 `getCustomerSourceOverview`（`fromDate=toDate=昨天`，`sourceType=channel` 或 `campaign`）。
2. 在返回 `data[]` 中按 `name` 模糊匹配用户提到的名称，取得 `id` 字段。
3. 将该 `id` 作为 `channel` / `campaign` 参数调用接口 2 / 3 做趋势分析。

**反例**（不要这样做）：
```
# ❌ 错误：用接口 5 返回的 code 当作 channel 参数 → 返回空数据
umeng-cli call '{"name":"umeng.umini.getSceneInfoList",...}' → data[].code = "cp_5f8a3b"
umeng-cli call '{"name":"umeng.umini.getChannelOverview",...}' '{"channel":"cp_5f8a3b",...}'  # 0 数据
```

**正例**：
```
# ✅ 正确：用接口 1 返回的 id
umeng-cli call '{"name":"umeng.umini.getCustomerSourceOverview",...}' → data[].id = "5e8c6dea978eea071c37c68201"
umeng-cli call '{"name":"umeng.umini.getChannelOverview",...}' '{"channel":"5e8c6dea978eea071c37c68201",...}'  # ✅ 有数据
```

### W4：H5 场景来源对比（H5 专属）

H5 应用（`html_5`）不能调用接口 4 `getSceneOverview`，改用接口 1 + `sourceType=platform`：

```bash
umeng-cli call '{"name":"umeng.umini.getCustomerSourceOverview",...}' '{"dataSourceId":"...","sourceType":"platform","fromDate":"2026-04-27","toDate":"2026-04-27","timeUnit":"day"}'
```

### W5：取推广链接 URL（接口 5 唯一必要场景）

仅当需要向用户**展示完整推广链接 URL** 时才调用接口 5：

```bash
umeng-cli call '{"name":"umeng.umini.getSceneInfoList",...}' '{"dataSourceId":"...","sourceType":"campaign"}'
# 返回 data[].url 是完整 URL
```

**注意**：接口 5 的 `code` 不可用于接口 2/3（见「关键字段告警」小节）。

### W6：Android/iOS App 退回

- 若用户是 Android/iOS App 询问"渠道/活动效果" → 直接回复"本 Skill 仅限小程序 / H5 / 小游戏；App 渠道请用 `umeng-cli-uapp-channel-version`"。

---

## 字段别名与旧参数对照表

本 Skill 直达友盟 OpenAPI 参数名，旧 `scripts/mini_channel.py` 的 CLI 抽象层参数对应关系如下：

| 旧 CLI 参数 | 新接口参数 | 说明 |
|---|---|---|
| `--app "友小盟小程序"` | `dataSourceId` | 旧脚本按应用名到 `umeng-config.json` 查 appkey；新 Skill 显式传 appkey |
| `--customer-source` | 接口 1（`getCustomerSourceOverview`） | 模式参数 → 接口直调 |
| `--channel <code>` | 接口 2（`getChannelOverview`）+ `channel` 参数 | ⚠️ **新 Skill 要求 `id`（26 位）而非 `code`** |
| `--campaign <code>` | 接口 3（`getCampaignOverview`）+ `campaign` 参数 | ⚠️ 同上 |
| `--scene <code>` | 接口 4（`getSceneOverview`）+ `scene` 参数 | 场景值编码（如 `wx_1011`） |
| `--list` | 接口 1（取 `id`）或接口 5（取 `url`） | 按需选择 |
| `--list --source-type channel` | 接口 1 `sourceType=channel` | 取 `id` 用途；旧脚本实际也是用 `getCustomerSourceOverview` 做列表 |
| `--source-type` | `sourceType` | `channel` / `campaign` / `platform` / `scene` |
| `--order-by newUser` | `orderBy` | 同 |
| `--direction desc` | `direction` | 同 |
| `--indicators "activeUser,visitTimes"` | `indicators` | 同 |
| `--metric activeUser --range last_7_days` | 接口 2/3/4 + `fromDate/toDate/timeUnit=day` | 趋势分析由客户端基于明细接口自行展开 |
| `--top 10` | 客户端取 `data[]` 前 10 条 | 接口本身不支持 Top N 语义 |
| `--json` | — | 接口本身返回 JSON |

---

## 边界与异常处理

| 情形 | 处理方式 |
|---|---|
| App 类型为 Android/iOS | 拒绝执行，提示「本 Skill 仅限小程序 / H5 / 小游戏；App 渠道请用 `umeng-cli-uapp-channel-version`」 |
| 未提供 `dataSourceId` | 引导先用 `umeng-cli-uapp-assets` 查询小程序列表取 `dataSourceId` |
| H5 应用调用接口 4 | 拒绝，引导改用接口 1 + `sourceType=platform` |
| H5 应用 `indicators` 包含 `launch` / `onceDuration` | 标注该字段 H5 不支持，返回值可能为 0 或 null |
| 用户给渠道/活动**中文名**而非 ID | 先走 W3：接口 1 排行取 `id`，再查明细 |
| 混用 `getSceneInfoList.code` → 接口 2/3 | **禁止**，改用接口 1 的 `id`；详见关键字段告警 |
| `scene` 值不确定 | 建议引导用户查阅 [友盟场景值文档](https://developer.umeng.com/docs/147615/detail/175369) |
| 接口返回空数组 | 告知「该日期/类型暂无数据，建议换昨天或近期日期」 |
| 中文参数（不涉及本 Skill） | 本 Skill 参数基本为英文枚举或 ID，无 urlEncode 问题 |

---

## 与其他 Skill 的边界

| Skill | 本 Skill 如何联动 |
|---|---|
| `umeng-cli-uapp-assets` | **前置**：先取 `dataSourceId`（99% 查询前置步骤） |
| `umeng-cli-uapp-campaign` | 推广链接**创建**归该 Skill；本 Skill **只做查询分析**。创建后的效果分析回到本 Skill。 |
| `umeng-cli-uapp-channel-version` | App 类型（Android/iOS）的渠道效果由该 Skill 覆盖；本 Skill 不涉及 App |
| `uapp-umini`（旧版，Python SDK） | 小程序的**应用级**概况 / 留存 / 页面 / 分享等仍由其覆盖；本 Skill 只做推广维度 |
| `uapp-retention`（旧版） | 留存分析归 `uapp-retention`；本 Skill 不涉及留存 |

---

## 历史产物说明

- 旧实现 `skills/uapp-mini-channel/` 目录 + `scripts/mini_channel.py`（Python SDK + `apiKey`/`apiSecurity` 落盘配置）保留兼容，不删除。
- 旧打包 `skills/uapp-mini-channel-1.1.0.zip` 保留兼容。
- 本 Skill 与旧 `uapp-mini-channel` **能力完全等价**（零能力扩展）：覆盖相同的 5 个接口，仅做调用形态（CLI 化）与鉴权（`umeng-aksk`）的升级，并额外提供 `getSceneInfoList.code` 不可用陷阱的显式告警（新收益）。

---

## 快速自检清单（AI 使用本 Skill 前自检）

- [ ] 已确认用户小程序（非 App），已取得 `dataSourceId`
- [ ] 查询指定渠道/活动时，已通过**接口 1**（`getCustomerSourceOverview`）取 `id` 字段，**未混用接口 5 的 `code`**
- [ ] H5 应用未调用接口 4 `getSceneOverview`；已改用接口 1 `sourceType=platform`
- [ ] H5 应用 `indicators` 已避开 `launch` / `onceDuration`（或已明确告知字段 H5 不支持）
- [ ] `sourceType` / `timeUnit` / `indicators` 枚举值全部在白名单内
- [ ] 趋势分析已理解数据按 `dateTime` 降序排列（`data[0]`=末期、`data[-1]`=初期）
