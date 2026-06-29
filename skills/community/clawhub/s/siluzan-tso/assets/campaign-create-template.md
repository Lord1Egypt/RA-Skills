# `ad campaign-create` JSON 配置说明

> **Agent 必读（与 JSON 成对加载）**：本文件是字段说明；**结构真相源**是同目录 [`campaign-create-template.json`](campaign-create-template.json)。建系列前**必须先 Read `.json`**，再 Read 本 `.md`。**禁止**只读本文件凭印象手写 JSON。

`siluzan-tso ad campaign-create` **仅**接受 `--config-file` 指向的 JSON 文件

**JSON 字段名保持 PascalCase**，与后端 `Campaign` / `CampaignCreationRecord` 契约一致；`ad campaign-validate` 会**就地自动修复**关键词词面（按 `MatchTypeV2` 补全 `"` / `[]`，兼容 `matchTypeV2` / `keywordText` / `Items[]`），可用 `--write-normalized` 落盘修复后的 JSON。

**`ad campaign-create` 提交前**，CLI 在 JSON 原文之外额外处理（不影响 validate 读到的「元」口径）：

1. 剥除以 `_` 开头的注解键（如 `_meta`、`_comment_budget`、`_comment_finalurl`）；
2. 外层 body：`account` → 数字 `customerId`；补全 `KeywordRecommendationsV2`（按广告组名，`Value` 可为 `[]`）；`googleDataRecordId` 缺省为 `""`（CLI 默认）；
3. `campaign` 金额字段「元」→「分」（×100）；
4. `ExtensionsForBatchJob` 中 SITELINK 的 `Properties` 规范化（见下文「SITELINK」）。

JSON 模板：同目录 [`campaign-create-template.json`](campaign-create-template.json)。

---

## Agent 常见坑（实战）

> 摘自真实创建流水：多次 `--json-out` 误用、validate 通过但 create 因 `Finalurl` 失败、**否词误填正向关键词**。提交前对照本表，避免重复踩坑。

### 正向关键词 vs 否定关键词（勿混放）

| 类型 | JSON 路径 | 说明 |
| ---- | --------- | ---- |
| **正向关键词**（要买的词） | `campaign.AdGroupsForBatchJob[].KeywordsForBatchJob[]` | 按组写入；含 `MatchTypeV2` + `FinalURL` |
| **否定关键词**（要排除的词） | `campaign.NegativeKeywordsForBatchJob[]` | **系列级**；元素 `{ KeywordText: [...], MatchTypeV2: "BROAD", FinalURL: "" }` |

**禁止**：把方案 Markdown「否定词表」里的 `free` / `jobs` / `tutorial` 等抄进 `KeywordsForBatchJob`——那会**主动购买**这些流量。  
**正确**：否词只写 `NegativeKeywordsForBatchJob`；`ad campaign-validate` 会对误填给出 **warnings**（常见否词词根 / 与否词块重复）。

投放方案 Markdown 中 §3.3 关键词矩阵 → `KeywordsForBatchJob`；§3.3 系列级否定词 / §3.4 账户级否定词 → `NegativeKeywordsForBatchJob`（账户级列表仍须在 Google 后台单独应用）。

### CLI 参数（勿混用）

| 命令                             | 支持 `--json-out`？ | 推荐用法                                                                                                                                                                                                                                               |
| -------------------------------- | :-----------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ad campaign-validate`           |       **是**        | **推荐** `--json-out ./snap-campaign`（落盘 `ad-campaign-validate-<account>.json`，含 `lengthViolations`）；。人读：`--config-file` 即可；词面规范化：`--write-normalized`。超长勿自动截断，见 `references/google-ads/google-ads-campaign-plan.md` § 超长人工确认 |
| `ad campaign-create`             |       **是**        | 落盘任务响应：`--json-out ./snap-campaign`；                                                                                                                                                                                                           |
| `ad batch get` / `ad batch diff` |       **是**        | 轮询与 diff 结果落盘，见 `references/core/tips.md`                                                                                                                                                                                                     |

**Agent**：校验与 create/batch 共用同一 `--json-out` 目录时，按 stdout 摘要里的 `outlineFile` → 再读对应 JSON（勿把 outline 当数据）。

### RSA 落地页：`Finalurl` 必填

后端 BatchJob **要求**每条 `AdsForBatchJob[]` 带 **`Finalurl`**（小写 url）。仅写 `DestinationUrl` 时：

- `ad campaign-validate` **可能仍显示通过**（校验用 `Finalurl ?? DestinationUrl` 只检查 URL 格式，不强制字段存在）；
- `ad campaign-create` / BatchJob **会失败**（报 `Finalurl` 缺失类错误）。

**正确写法**（两字段同值）：

```json
"DestinationUrl": "https://www.example.com/products",
"Finalurl": "https://www.example.com/products",
"AdTitle": null
```

生成 JSON 后可用脚本批量补全（勿手改几十条）：

```python
# 与实战 fix_campaign_v2.py 同逻辑：缺 Finalurl 则从 DestinationUrl 复制
for ag in camp.get("AdGroupsForBatchJob", []):
    for ad in ag.get("AdsForBatchJob", []):
        if "Finalurl" not in ad:
            ad["Finalurl"] = ad.get("DestinationUrl", "")
        if "AdTitle" not in ad:
            ad["AdTitle"] = None
```

### SITELINK 附加信息

每条 `typeV2: "SITELINK"` 须同时有 **`AssetFieldType": "SITELINK"`**（模板已示例）。缺省时部分账户 BatchJob 会失败。

### 推荐命令顺序（单系列）

```bash
siluzan-tso ad campaign-validate --config-file ./campaign.json
# 用户确认方案后：
siluzan-tso ad campaign-create --config-file ./campaign.json --commit '<campaign create description>'
siluzan-tso ad batch get --id <taskId> --config-file ./campaign.json --json-out ./snap-campaign
siluzan-tso ad batch diff --batch-id <taskId> --config-file ./campaign.json --json-out ./snap-campaign
```

`Creating` 时每 5–10s 轮询 `batch get`，**勿**重复 `campaign-create`。

---

## Agent 编排

流程、双轨入口、`campaign-validate` 门禁与分层规则阅读：**`references/google-ads/google-ads-campaign-plan.md`**（本文件仅字段契约，不重复流水线）。

一个 JSON 对应一个广告系列；多系列使用多个 JSON 文件（可选 `campaign-manifest.json`，见 campaign-plan）。

**提交前自检（代码改 JSON，不手填 Markdown）：**

1. 每条 RSA：`Finalurl` 与 `DestinationUrl` 同值；可选 `AdTitle: null`；
2. 每条 SITELINK：`AssetFieldType` = `SITELINK`；
3. `ad campaign-validate` 通过（**不加** `--json-out`）；
4. 用户确认后再 `campaign-create`。

---

## 外层字段（CampaignCreationRecord）

| 字段                 | 类型           | 必填 | 说明                                                                                                                                                                           |
| -------------------- | -------------- | :--: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `account`            | string         |  ✅  | 媒体账户 ID；提交时转为数字 `customerId`（勿依赖引号字符串）                                                                                                                   |
| `customerName`       | string         |      | 展示/智投用客户名；**可省略**——`campaign-create` / `batch publish` 会按 `account` 调 `list-accounts` 自动填入 `mediaCustomerName`。若填写则须与之一致，否则提交时 CLI 自动更正 |
| `name`               | string         |      | 智投 `campaignName`；缺省取 `campaign.Name`；账户内不得与已有在投/暂停系列重名，否则 BatchJob 系列创建失败                                                                     |
| `url`                | string         |      | 智投展示用 URL；后端只读，用于回显                                                                                                                                             |
| `locations`          | string[]       |      | 展示用地区名（后端只读，可空数组）                                                                                                                                             |
| `productWords`       | string[]       |      | 智投/推荐用产品核心词                                                                                                                                                          |
| `googleDataRecordId` | string \| null |      | 智投记录 ID；省略时提交 `""`（CLI 默认）                                                                                                                                       |
| `draft`              | boolean        |      | `false`（默认）立即发布到 Google；`true` 仅保存草稿，需后续 `ad batch publish`                                                                                                 |
| `campaign`           | object         |  ✅  | 内层 Campaign 对象，见下表                                                                                                                                                     |

> 提交时 CLI 另附 `KeywordRecommendationsV2`：`[{ Key: <广告组 Name>, Value: [] }, …]`，由 CLI 自动附加；JSON 文件内无需手写。

---

## 内层字段（`campaign` 对象）

> **金额单位**：JSON 中以「元」填写，CLI 提交前 ×100 转为「分」（与后端 `Budget`、`MaxCPCAmount` 等字段一致）。
> 涉及字段：`Budget`、`TargetSpend_BidCeilingAmount`、`TargetCpa_BidingAmount`、`TargetCpaAmount`、`MaxCPCAmount`、`MaxCpmAmount`、`MaxCPVAmount`、`MaxCPC`。

### 基础

| 字段            | 类型                  | 必填 | 说明                                                              |
| --------------- | --------------------- | :--: | ----------------------------------------------------------------- |
| `Name`          | string                |  ✅  | 广告系列名；须与外层 `name` 一致；账户内唯一（在投/暂停不可重名） |
| `StatusV2`      | "Enabled" \| "Paused" |      | 默认 `Enabled`                                                    |
| `ChannelTypeV2` | string                |      | 搜索系列填 `SEARCH`                                               |

### 预算与出价

| 字段                           | 类型                                                                                                                     | 必填条件           | 说明                          |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ------------------ | ----------------------------- |
| `Budget`                       | number                                                                                                                   | ✅ > 0             | 日预算（元）                  |
| `BudgetShared`                 | boolean                                                                                                                  |                    | 共享预算时为 true             |
| `BudgetId`                     | number / string                                                                                                          |                    | 共享预算 id                   |
| `BudgetBudgetDeliveryMethodV2` | "STANDARD" \| "ACCELERATED" \| "UNSPECIFIED" \| "UNKNOWN"                                                                |                    | 默认 STANDARD                 |
| `BiddingStrategyTypeV2`        | "TARGET_SPEND" \| "MANUAL_CPC" \| "TARGET_CPA" \| "TARGET_ROAS" \| "MAXIMIZE_CONVERSIONS" \| "MAXIMIZE_CONVERSION_VALUE" | ✅                 | 出价策略                      |
| `TargetSpend_BidCeilingAmount` | number                                                                                                                   | TARGET_SPEND 时 ✅ | 每次点击费用上限（元）        |
| `TargetCpa_BidingAmount`       | number                                                                                                                   | TARGET_CPA 时 ✅   | 目标 CPA（元）                |
| `TargetRoas`                   | number                                                                                                                   | TARGET_ROAS 时 ✅  | 目标 ROAS（如 2.5 表示 250%） |
| `ManualCpc_EnhancedCpcEnabled` | boolean                                                                                                                  |                    | 是否增强 CPC                  |

### 网络（后端硬约束）

| 字段                         | 类型    | 说明                                                              |
| ---------------------------- | ------- | ----------------------------------------------------------------- |
| `TargetGoogleSearch`         | boolean | 默认 true；当 `TargetSearchNetwork=true` 时**必须** true          |
| `TargetSearchNetwork`        | boolean | Google 搜索网络合作伙伴；产品默认建议 false                       |
| `TargetContentNetwork`       | boolean | 展示网络；搜索专属方案建议 false                                  |
| `TargetPartnerSearchNetwork` | boolean | **必须 false**（后端拒绝：cannot set TargetPartnerSearchNetwork） |

### 地理 / 语言 / 平台

| 字段                    | 类型                                     | 必填 | 说明                                                            |
| ----------------------- | ---------------------------------------- | :--: | --------------------------------------------------------------- |
| `targetedLocations`     | `{ id: string, bidModifier?: number }[]` |  ✅  | 至少 1 个；先 `siluzan-tso ad geo search -a <acct> -q <地区名>` |
| `excludedLocations`     | 同上                                     |      | 排除地区                                                        |
| `targetedLanguages`     | `{ id: number }[]`                       |  ✅  | 英语 1000，中文 1017                                            |
| `targetedPlatforms`     | `{ id: number, bidModifier?: number }[]` |      | 30001 桌面 / 30002 平板 / 30000 移动                            |
| `excludedIpAddresses`   | string[]                                 |      | 排除 IP                                                         |
| `PositiveGeoTargetType` | number                                   |      |                                                                 |
| `NegativeGeoTargetType` | number                                   |      |                                                                 |

### 时间与 DSA

| 字段              | 类型       | 说明                                 |
| ----------------- | ---------- | ------------------------------------ |
| `StartTime`       | YYYY-MM-DD | 开始日期                             |
| `EndTime`         | YYYY-MM-DD | 结束日期（必须晚于 StartTime）       |
| `adSchedules`     | object[]   | 投放时段，缺省可填全周全天（见模板） |
| `DSADomainName`   | string     | 动态搜索广告域名                     |
| `DSALanguageCode` | string     | 默认 `en`                            |

### 子结构

| 字段                          | 类型     | 说明                                                                              |
| ----------------------------- | -------- | --------------------------------------------------------------------------------- |
| `AdGroupsForBatchJob`         | object[] | **至少 1 组**；见下                                                               |
| `NegativeKeywordsForBatchJob` | object[] | 系列级否词；元素：`{ KeywordText: string[], MatchTypeV2: "BROAD", FinalURL: "" }` |
| `ExtensionsForBatchJob`       | object[] | 附加信息；`Properties` 须 **string→string**（勿用数组值）。SITELINK 见下表        |

#### SITELINK（`ExtensionsForBatchJob[i]`，`typeV2` / `AssetFieldType` = `SITELINK`）

| 字段                        | 类型   | 说明                                                                                                                     |
| --------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------ |
| `typeV2`                    | string | 必填 `SITELINK`                                                                                                          |
| `AssetFieldType`            | string | **必填** `SITELINK`（与 `typeV2` 一致；缺省会导致部分账户 BatchJob 失败）                                                |
| `level` / `Level`           | string | 系列级填 `Campaign`                                                                                                      |
| `Properties`                | object | 键值均为字符串；见下表                                                                                                   |
| `Properties.Text`           | string | 链接文字（必填）。可写 `LinkText`，提交前会映射为 `Text`                                                                 |
| `Properties.Line2`          | string | 描述行 1，**≤ 25 字符**。可写 `Description1`，提交前映射为 `Line2`                                                       |
| `Properties.Line3`          | string | 描述行 2，**≤ 25 字符**；**不可省略或空字符串**（Google V20 不允许 null，空时 CLI 用 `Line2` 回填）。可写 `Description2` |
| `Properties.DestinationUrl` | string | 落地页 URL（必填）。**勿**写 `FinalUrls` 数组——会导致 TSO 无法反序列化整包 body（`campaign creation record is null`）    |

---

## 广告组（`AdGroupsForBatchJob[i]`）

| 字段                  | 类型                  |      必填      | 说明                                              |
| --------------------- | --------------------- | :------------: | ------------------------------------------------- |
| `Name`                | string                |       ✅       | 组名；用于提交体 `KeywordRecommendationsV2[].Key` |
| `StatusV2`            | "Enabled" \| "Paused" |                | 默认 Enabled                                      |
| `TypeV2`              | string                |                | 搜索系列填 `SEARCH_STANDARD`                      |
| `RotationModeV2`      | string                |                | 一般 `Unspecified`                                |
| `MaxCPCAmount`        | number                | ✅(MANUAL_CPC) | 元；MANUAL_CPC 出价策略必须 > 0                   |
| `KeywordsForBatchJob` | object[]              |                | 见下                                              |
| `AdsForBatchJob`      | object[]              |                | 见下                                              |

### 关键词块（`KeywordsForBatchJob[j]`）

每个块描述一组**同匹配类型**的关键词。若同一块内混用裸词 / `"词组"` / `[完全]`（或与块级 `MatchTypeV2` 冲突的符号），`campaign-validate` 会**自动拆成多个块**（顺序：BROAD → PHRASE → EXACT），再按块级类型修复词面。

| 字段          | 类型                           | 说明                                                                                                                             |
| ------------- | ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `KeywordText` | string[]                       | 关键词词面数组；PHRASE 应写 `"keyword"`，EXACT 应写 `[keyword]`（裸词亦可，`campaign-validate` 会按 `MatchTypeV2` **自动修复**） |
| `MatchTypeV2` | "BROAD" \| "PHRASE" \| "EXACT" | 与词面格式对应；Google 网关以词面符号为准，CLI 校验时会改写 `KeywordText` 与之对齐                                               |
| `FinalURL`    | string                         | 关键词级落地页                                                                                                                   |

### 创意块（`AdsForBatchJob[j]`，RSA）

| 字段                               | 类型           | 必填 | 说明                                                                                                                            |
| ---------------------------------- | -------------- | :--: | ------------------------------------------------------------------------------------------------------------------------------- |
| `TypeV2`                           | string         |      | RSA 填 `RESPONSIVE_SEARCH_AD`                                                                                                   |
| `DestinationUrl`                   | string         |  ✅  | 展示/编辑用落地页 URL                                                                                                           |
| `Finalurl`                         | string         |  ✅  | **后端 BatchJob 必填**；与 `DestinationUrl` 填**相同** URL。勿只写前者——validate 可能仍通过，create 会失败                      |
| `AdTitle`                          | null \| string |      | 可选；无标题时写 `null`（CLI 默认）                                                                                             |
| `Path1` / `Path2`                  | string         |  ✅  | 显示路径（**必填**，缺/null 会导致后端 BatchJob `ArgumentNullException`）；**≤ 15 字符**（CJK 按 2 计）；小写 a-z、数字、连字符 |
| `headlinePart1/2/3`                | string         |  ✅  | 前 3 条标题；**每条 ≤ 30 字符**（CJK 按 2 计）                                                                                  |
| `AddtionalHeadlines`               | string[]       |  ✅  | 第 4–15 条标题；与前三条合计须 **15 条**（写满）                                                                                |
| `adDescription` / `adDescription2` | string         |  ✅  | 前 2 条描述；**每条 ≤ 90 字符**                                                                                                 |
| `AddtionalAdDescriptions`          | string[]       |  ✅  | 第 3–4 条描述；与前两条合计须 **4 条**（写满）                                                                                  |

---

## 校验规则（`ad campaign-validate`）

| 规则                    | 说明                                                                                                       |
| ----------------------- | ---------------------------------------------------------------------------------------------------------- |
| 基础                    | `customerName` / `campaign` 非空；`Budget > 0`；地理/语言至少 1 项                                         |
| 网络                    | `TargetPartnerSearchNetwork` 须 false；不可同时关闭 Google 搜索与搜索网络                                  |
| RSA / 关键词 / 附加信息 | 标题 **15** 条、描述 **4** 条（须写满）；字符上限、词面非空；RSA `Path1`/`Path2` 必填；SITELINK 行长度限制 |
| 否词误填 | `KeywordsForBatchJob` 含常见否词词根或与 `NegativeKeywordsForBatchJob` 重复 → **warnings**（不阻断，须 Agent 修正后再 create） |
| 实务 | 日期格式与先后、出价策略与配套字段一致 |

`ad campaign-validate` 通过不保证 BatchJob 成功（例如仅写 `DestinationUrl` 未写 `Finalurl` 时 validate 仍可能 ✅）。异步结果用 `ad batch get` 轮询；`HasFailed` / 部分失败时用 `ad batch diff` 对照 JSON 补缺，系列级失败时改 JSON 重提，勿在半成品上反复整包创建。写操作须 `--commit`，见 `references/google-ads/google-ads.md` § ad campaign-create。
