---
name: umeng-cli-uapp-campaign
description: 友盟小程序推广链接管理技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 2 个推广接口（1 个写入 + 1 个只读），与旧 uapp-campaign 能力完全等价的 CLI 化。覆盖推广链接创建、活动/渠道清单查询。当用户需要为小程序创建推广链接、查询推广活动列表或推广渠道列表时使用。仅适用于小程序 / H5 / 小游戏，不支持 Android/iOS App。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# 友盟小程序推广链接管理技能

> `umeng-cli` 是友盟提供的命令行程序，所有操作通过执行 `umeng-cli call` 命令完成。

管理友盟小程序（U-MiniProgram）的推广链接资产，覆盖**资产管理**两类核心需求：

- 创建推广活动链接（活动名 + 渠道 + 可选落地页）
- 枚举当前小程序下全部推广活动 / 推广渠道

共 **2 个接口**（命名空间 `com.umeng.umini`，与旧 `uapp-campaign` skill 能力完全等价）：

| # | 接口 | 读/写 | 能力 |
|---|---|---|---|
| 1 | `umeng.umini.createCampaign` | ✏️ **写入** | 创建推广链接（活动 + 渠道 + 可选落地页） |
| 2 | `umeng.umini.getSceneInfoList` | 📖 只读 | 获取当前小程序的推广活动 / 渠道清单 |

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-campaign"}'
> ```
>
> **Appkey 维度打点：** 当本轮任务中出现 Appkey（小程序 `dataSourceId`）的输入操作时，在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-campaign", "appkey":"<输入的Appkey>"}'
> ```
> 同一 Appkey 在同一会话中只打一次；若用户切换到新的 Appkey，需对新的 Appkey 再打一次。

## ⚠️ 适用范围限制（强制）

本 Skill **仅适用于小程序 / H5 / 小游戏**类应用：

| 应用类型 | 是否适用 | 说明 |
|---|---|---|
| 微信 / 支付宝 / 字节 / 百度 / QQ 小程序 | ✅ | 适用 |
| 微信小游戏（`mini_game_wechat`） | ✅ | 适用 |
| H5（`html_5`） | ✅ | 适用 |
| Android App（`android`） | ❌ | **不适用**，请改用 App 端的渠道分析能力（由 `umeng-cli-uapp-channel-version` 覆盖） |
| iOS App（`iphone`） | ❌ | 同上 |

当用户对 Android / iOS App 询问"推广链接"时，应明确告知：「推广链接功能仅限小程序 / H5 / 小游戏；App 类型请改用渠道分析（`umeng-cli-uapp-channel-version`）」。

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

- 用户要求为某小程序创建一条推广链接（活动 + 渠道）
- 用户询问"我有哪些推广活动 / 渠道？"「查看推广链接列表」
- 关键词：推广链接、推广活动、推广渠道、创建推广、推广列表、活动列表、渠道列表

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

与 `umeng-cli-uapp-assets` 资产发现型 Skill 不同，本 Skill **2 个接口都必须传入 `dataSourceId`**（即小程序的 AppKey），因为推广资产作用域是"单个小程序"而不是"账号"。

若用户未提供 appkey：
1. **优先**引导使用 `umeng-cli-uapp-assets` 查询小程序列表，取得 `dataSourceId`：
   ```bash
   umeng-cli call '{"name":"umeng.umini.getAppList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getAppList","authType":"umeng-aksk"}}' '{"pageIndex":1,"pageSize":100}'
   ```
2. **备选**引导用户从友盟官网 [web.umeng.com](https://web.umeng.com) → U-MiniProgram → 应用列表 → 复制 AppKey 获取。

## ⚠️ 写入风险提示（本 Skill 唯一写入接口：`createCampaign`）

`umeng.umini.createCampaign` 是**变更类操作**，会在用户账号下实际创建一条不可撤销的推广链接。调用前**强制**遵循以下规范：

1. **参数完整校验**：`dataSourceId` / `campaignName` / `channelName` 三者必须同时确认（`path` 可选）。
2. **向用户复述并二次确认**：执行前应以自然语言向用户复述"将为 <应用名> 创建活动「<campaignName>」渠道「<channelName>」"，获得明确"确认/继续"后再执行。
3. **活动名不得为空、不得含仅空白字符**：调用前 strip，若为空必须停止并要求补齐。
4. **同名活动可重复创建**：友盟允许同 `campaignName + channelName` 多次创建，返回不同 `code`（活动代码）。不要自动重试相同参数。
5. **失败语义**：返回 `success=false` 或 `code != 0` 时，不要自动重试写入；将 `msg` 原文透传给用户。

## 2 个接口速查表

| 接口 | 必填参数 | 分页 | 典型用途 |
|---|---|---|---|
| `createCampaign` | `dataSourceId` / `campaignName` / `channelName` | — | 创建推广链接 |
| `getSceneInfoList` | `dataSourceId` / `sourceType` | ❌ | 列出全部活动 / 渠道 |

**公共枚举**：

- `sourceType`（仅 `getSceneInfoList`）：`campaign` / `channel`

---

## 接口 1：`umeng.umini.createCampaign` — 创建推广链接（⚠️ 写入）

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |
| `campaignName` | String | 是 | 推广活动名称 |
| `channelName` | String | 是 | 推广渠道名称 |
| `path` | String | 否 | 落地页路径（如 `pages/index/main`） |

### 调用示例

```bash
# 不含落地页路径
umeng-cli call '{"name":"umeng.umini.createCampaign","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.createCampaign","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","campaignName":"春季换新季","channelName":"抖音"}'

# 含落地页路径
umeng-cli call '{"name":"umeng.umini.createCampaign","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.createCampaign","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","campaignName":"春季特卖","channelName":"微信推广","path":"pages/promo/main"}'
```

### 返回

```json
{
  "msg": "success",
  "code": 0,
  "success": true,
  "data": "cp_5f8a3b"
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `data` | String | 新建活动的 **活动代码（code）**；调用 `getSceneInfoList` 可取到完整的 `url` 推广链接 |
| `code` | Long | 业务状态码，0 表示成功 |
| `success` | Boolean | 布尔状态 |
| `msg` | String | 消息文案 |

> 说明：`data` 仅返回活动代码，不返回完整 URL；若需要完整链接，紧接一次 `getSceneInfoList` 查询即可（见 W1 工作流）。

---

## 接口 2：`umeng.umini.getSceneInfoList` — 获取推广活动 / 渠道清单

### 参数

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 小程序 AppKey |
| `sourceType` | String | 是 | `campaign`（活动） / `channel`（渠道） |

### 调用示例

```bash
# 查询所有推广活动
umeng-cli call '{"name":"umeng.umini.getSceneInfoList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getSceneInfoList","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","sourceType":"campaign"}'

# 查询所有推广渠道
umeng-cli call '{"name":"umeng.umini.getSceneInfoList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getSceneInfoList","authType":"umeng-aksk"}}' '{"dataSourceId":"1dfe1b2f3597245664499a91","sourceType":"channel"}'
```

### 返回

```json
{
  "msg": "success",
  "code": 0,
  "success": true,
  "data": [
    {
      "code": "cp_5f8a3b",
      "name": "春季换新季",
      "url": "https://m.umeng.com/...",
      "createDateTime": "2026-04-20 10:12:33"
    }
  ]
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `data[].code` | String | 活动代码（或渠道代码） |
| `data[].name` | String | 活动 / 渠道中文名称 |
| `data[].url` | String | 完整推广链接 URL（仅活动有；渠道通常为空） |
| `data[].createDateTime` | String | 创建时间 `yyyy-MM-dd HH:mm:ss` |

> **本接口不支持分页**：一次性返回当前小程序全部活动 / 渠道；若列表极长可由客户端过滤。

---

## 典型问法与内部意图映射

| 典型问法 | 接口 | 关键参数 |
|---|---|---|
| 「为 X 小程序创建"春季换新季"抖音推广」 | `createCampaign` | `dataSourceId`=X, `campaignName`="春季换新季", `channelName`="抖音" |
| 「列出 X 小程序所有推广活动」 | `getSceneInfoList` | `sourceType`=campaign |
| 「X 小程序有哪些推广渠道」 | `getSceneInfoList` | `sourceType`=channel |

---

## 工作流

### W1：创建推广链接（含二次确认 + 回查 URL）

**目标**：为某小程序创建活动链接并立即返回可分享的完整 URL。

**步骤**：

1. **准备阶段**：向用户复述 `dataSourceId` 对应的小程序名 + `campaignName` + `channelName`（+ 可选 `path`），获得明确"继续/确认"。
2. **执行**：调用 `createCampaign`，取得返回中的 `data`（活动代码）。
3. **回查**：紧接调用 `getSceneInfoList(sourceType=campaign)`，在返回数组中按 `code == 步骤 2 返回的 data` 过滤出刚创建的活动，读取其 `url` 字段作为推广链接交付给用户。

**示例序列**：

```bash
# Step 2
umeng-cli call '{"name":"umeng.umini.createCampaign",...}' '{"dataSourceId":"1dfe...","campaignName":"春季换新季","channelName":"抖音"}'
# 返回 data: "cp_5f8a3b"

# Step 3
umeng-cli call '{"name":"umeng.umini.getSceneInfoList",...}' '{"dataSourceId":"1dfe...","sourceType":"campaign"}' \
  | jq '.data[] | select(.code == "cp_5f8a3b")'
```

### W2：推广资产盘点（活动 + 渠道合并）

**目标**：一次给出小程序所有推广资产的总览。

```bash
# 活动清单
umeng-cli call '{...}' '{"dataSourceId":"...","sourceType":"campaign"}'
# 渠道清单
umeng-cli call '{...}' '{"dataSourceId":"...","sourceType":"channel"}'
```

客户端按 `name` / `createDateTime` 排序合并，输出「共 N 个活动 + M 个渠道」。

### W3：Android/iOS App 退回（异常规避）

- 若用户是 Android/iOS App 询问"推广链接" → 直接回复"推广链接仅限小程序 / H5 / 小游戏；App 渠道分析请使用 `umeng-cli-uapp-channel-version`"。

---

## 字段别名与旧参数对照表

本 Skill 直达友盟 OpenAPI 参数名，旧 `scripts/campaign.py` 的 CLI 抽象层参数对应关系如下：

| 旧 CLI 参数（`scripts/campaign.py`） | 新接口参数（`umeng-cli call`） | 说明 |
|---|---|---|
| `--app "友小盟数据官"` | `dataSourceId` | 旧脚本内部按应用名到 `umeng-config.json` 查 appkey；新 Skill 必须显式传 appkey，可先用 `umeng-cli-uapp-assets` 取得 |
| `--create` | `createCampaign` 接口 | 模式参数 → 接口直调 |
| `--name` | `campaignName` | 活动名称 |
| `--channel` | `channelName` | 渠道名称 |
| `--path` | `path` | 落地页路径 |
| `--list --type campaign` | `getSceneInfoList(sourceType=campaign)` | 活动列表 |
| `--list --type channel` | `getSceneInfoList(sourceType=channel)` | 渠道列表 |
| `--json` | — | 接口本身返回 JSON，无需参数切换 |

---

## 边界与异常处理

| 情形 | 处理方式 |
|---|---|
| App 类型为 Android/iOS | 拒绝执行，提示「推广链接功能仅限小程序 / H5 / 小游戏；App 渠道分析请用 `umeng-cli-uapp-channel-version`」 |
| 未提供 `dataSourceId` | 引导先用 `umeng-cli-uapp-assets` 查询小程序列表取 `dataSourceId` |
| 找不到 appkey 对应的小程序 | 提示 appkey 可能来自非小程序应用或账号错误；让用户在 `umeng-cli whoami` 下确认登录账号 |
| `createCampaign` 活动名为空 / 纯空白 | 调用前 strip 校验，空则停止并要求补齐 |
| `createCampaign` 返回 `success=false` | 原文透传 `msg`，**不自动重试**（可能已经半成功） |
| `getSceneInfoList` 返回空数组 | 告知「当前小程序暂无推广活动/渠道记录」 |
| 中文参数值 `campaignName` / `channelName` | umeng-cli 内部处理 urlEncode，直接传中文即可，**不需要**手工 `encodeURIComponent` |

---

## 与其他 Skill 的边界

| Skill | 本 Skill 如何联动 |
|---|---|
| `umeng-cli-uapp-assets` | **前置**：先取 `dataSourceId`（推荐，99% 的推广操作前置步骤） |
| `umeng-cli-uapp-channel-version` | App 类型（Android/iOS）的渠道分析由该 Skill 承担，本 Skill 不覆盖 App |
| `uapp-umini`（旧版，Python SDK） | 小程序的非推广类数据（概况 / 留存 / 页面 / 分享等）仍由其覆盖；本 Skill 不涉及 |

---

## 历史产物说明

- 旧实现 `skills/uapp-campaign/` 目录 + `scripts/campaign.py`（Python SDK + `apiKey`/`apiSecurity` 落盘配置）保留兼容，不删除。
- 旧打包 `skills/uapp-campaign-1.1.0.zip` 保留兼容。
- 本 Skill 与旧 `uapp-campaign` **能力完全等价**（零能力扩展）：覆盖相同的 2 个接口（`createCampaign` + `getSceneInfoList`），仅做调用形态（CLI 化）与鉴权（`umeng-aksk`）的升级。

---

## 快速自检清单（AI 使用本 Skill 前自检）

- [ ] 已确认用户小程序（非 App），已取得 `dataSourceId`
- [ ] 调用 `createCampaign` 前已向用户复述 `campaignName` + `channelName`，并获得确认
- [ ] `createCampaign` 返回 `success=false` 时，不自动重试，原文透传 `msg`
