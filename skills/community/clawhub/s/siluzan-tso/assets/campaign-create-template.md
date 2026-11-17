# `ad campaign-create` JSON 配置说明

> **Agent 必读（与 JSON 成对加载）**：本文件是字段说明；**结构真相源**是同目录 [`campaign-create-template.json`](campaign-create-template.json)。建系列前**必须先 Read `.json`**，再 Read 本 `.md`。**禁止**只读本文件凭印象手写 JSON。

`siluzan-tso ad campaign-create` **仅**接受 `--config-file` 指向的 JSON 文件

**JSON 字段名保持 PascalCase**，与后端 `Campaign` / `CampaignCreationRecord` 契约一致；`ad campaign-validate` 会**就地自动修复**关键词词面（按 `MatchTypeV2` 补全 `"` / `[]`，兼容 `matchTypeV2` / `keywordText` / `Items[]`），可用 `--write-normalized` 落盘修复后的 JSON（不带路径时原地覆盖 `--config-file`）。

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

| 类型                         | JSON 路径                                              | 说明                                                                          |
| ---------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **正向关键词**（要买的词）   | `campaign.AdGroupsForBatchJob[].KeywordsForBatchJob[]` | 按组写入；含 `MatchTypeV2` + `FinalURL`                                       |
| **否定关键词**（要排除的词） | `campaign.NegativeKeywordsForBatchJob[]`               | **系列级**；元素 `{ KeywordText: [...], MatchTypeV2: "BROAD", FinalURL: "" }` |

**禁止**：把方案 Markdown「否定词表」里的 `free` / `jobs` / `tutorial` 等抄进 `KeywordsForBatchJob`——那会**主动购买**这些流量。  
**正确**：否词只写 `NegativeKeywordsForBatchJob`；`ad campaign-validate` 会对误填给出 **warnings**（常见否词词根 / 与否词块重复）。

### Excel / 表格方案保真（地域 + 匹配类型）

用户给了投放方案文件时，**必读** `references/google-ads/rules/google-ads-plan-source-fidelity.md`，并遵守：

| 坑                                                        | 正确做法                                                                                     |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| 编造 `targetedLocations[].id` 或对 30 国逐条 `geo search` | **一次** `ad geo resolve --from-file … --json-out`；见 `google-ads-plan-source-fidelity.md`  |
| 对话里手写完整 campaign JSON                              | Agent **写转换脚本** Excel → `campaign.json`（落盘），再 validate                            |
| 方案有 Exact/Phrase，JSON 却一律 `BROAD`                  | 转换脚本按方案列/词面写入 EXACT/PHRASE/BROAD 分块                                            |
| validate 失败后未问用户就改词/消重标题/截断               | **询问**「您自己改还是我帮您改？」；见 `google-ads-plan-source-fidelity.md` § 用户方案不合规 |
| 代改后只说「创建成功」不交代改了啥                        | 创建完成后出报告：创建清单 + **从 xxx→xxx + 原因**（代改时维护变更账本）                     |

**多词短语（与 `keyword-negative-create` 同类误判）**：`KeywordText` 是 **JSON 字符串数组**，**空格多词完全合法**（如 `"how to make"`、`"home cooking"`）。PHRASE 写 `"\"vegan recipe\""` 或裸词 + `MatchTypeV2: "PHRASE"`（validate 会补引号）。**禁止**因「多词」就省略否词或让用户去 Google Ads 后台手补——那是 Agent 误判，不是 `campaign-create` 限制。

投放方案 Markdown 中 §3.3 关键词矩阵 → `KeywordsForBatchJob`；§3.3 系列级否定词 → `NegativeKeywordsForBatchJob`。**§3.4 账户级否定词**：`campaign-create` 批量接口不支持账户级，需在系列创建完成后**另行**执行 `ad keyword-negative-create --level Account`。

### CLI 参数（勿混用）

| 命令                             | 支持 `--json-out`？ | 推荐用法                                                                                                                                                                                                                                                          |
| -------------------------------- | :-----------------: | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ad campaign-validate`           |       **是**        | **推荐** `--json-out ./snap-campaign`（落盘 `ad-campaign-validate-<account>.json`，含 `lengthViolations`）；。人读：`--config-file` 即可；词面规范化：`--write-normalized`。超长勿自动截断，见 `references/google-ads/google-ads-campaign-plan.md` § 超长人工确认 |
| `ad campaign-create`             |       **是**        | 落盘任务响应：`--json-out ./snap-campaign`；                                                                                                                                                                                                                      |
| `ad batch get` / `ad batch diff` |       **是**        | 轮询与 diff 结果落盘，见 `references/core/tips.md`                                                                                                                                                                                                                |

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
# 读落盘 agentWorkflow.nextCommand（Creating 继续轮询；成功/部分成功 → batch diff）
siluzan-tso ad batch diff --batch-id <taskId> --config-file ./campaign.json --json-out ./snap-campaign
# 读 ok / missing（含 layer=location 投放国家）；有缺失 exit 2，执行 remediateCommand 后复 diff
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

| 字段                 | 类型           | 必填 | 说明                                                                                                                                                                                                                               |
| -------------------- | -------------- | :--: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `account`            | string         |  ✅  | 媒体账户 ID；提交时转为数字 `customerId`（勿依赖引号字符串）。**仅出方案**（未确认创建、无账户）可填 `"[PENDING_ACCOUNT]"` 或 `""`，见 `google-ads-campaign-plan.md` §仅出方案；**create/validate 前**须换成真实 `mediaCustomerId` |
| `customerName`       | string         |      | 展示/智投用客户名；**可省略**——`campaign-create` / `batch publish` 会按 `account` 调 `list-accounts` 自动填入 `mediaCustomerName`。若填写则须与之一致，否则提交时 CLI 自动更正                                                     |
| `name`               | string         |      | 智投 `campaignName`；缺省取 `campaign.Name`；账户内不得与已有在投/暂停系列重名，否则 BatchJob 系列创建失败                                                                                                                         |
| `url`                | string         |      | 智投展示用 URL；后端只读，用于回显                                                                                                                                                                                                 |
| `locations`          | string[]       |      | 展示用地区名（后端只读，可空数组）；**若填写非空**则长度须与 `campaign.targetedLocations` 一致（validate 硬校验）                                                                                                                  |
| `productWords`       | string[]       |      | 智投/推荐用产品核心词                                                                                                                                                                                                              |
| `googleDataRecordId` | string \| null |      | 智投记录 ID；省略时提交 `""`（CLI 默认）                                                                                                                                                                                           |
| `draft`              | boolean        |      | `false`（默认）立即发布到 Google；`true` 仅保存草稿，需后续 `ad batch publish`                                                                                                                                                     |
| `campaign`           | object         |  ✅  | 内层 Campaign 对象，见下表                                                                                                                                                                                                         |

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

| 字段                           | 类型                                                                                                                     | 必填条件           | 说明                                                                     |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ------------------ | ------------------------------------------------------------------------ |
| `Budget`                       | number                                                                                                                   | ✅ > 0             | 日预算（元）                                                             |
| `BudgetShared`                 | boolean                                                                                                                  |                    | 共享预算时为 true                                                        |
| `BudgetId`                     | number / string                                                                                                          |                    | 共享预算 id                                                              |
| `BudgetBudgetDeliveryMethodV2` | "STANDARD" \| "ACCELERATED" \| "UNSPECIFIED" \| "UNKNOWN"                                                                |                    | 默认 **STANDARD**；`ACCELERATED` 多数账户会被 Google 拒（validate 警告） |
| `BiddingStrategyTypeV2`        | "TARGET_SPEND" \| "MANUAL_CPC" \| "TARGET_CPA" \| "TARGET_ROAS" \| "MAXIMIZE_CONVERSIONS" \| "MAXIMIZE_CONVERSION_VALUE" | ✅                 | 出价策略                                                                 |
| `TargetSpend_BidCeilingAmount` | number                                                                                                                   | TARGET_SPEND 时 ✅ | 每次点击费用上限（元）                                                   |
| `TargetCpa_BidingAmount`       | number                                                                                                                   | TARGET_CPA 时 ✅   | 目标 CPA（元）                                                           |
| `TargetRoas`                   | number                                                                                                                   | TARGET_ROAS 时 ✅  | 目标 ROAS（如 2.5 表示 250%）                                            |

### 网络（后端硬约束）

| 字段                         | 类型    | 说明                                                              |
| ---------------------------- | ------- | ----------------------------------------------------------------- |
| `TargetGoogleSearch`         | boolean | 默认 true；当 `TargetSearchNetwork=true` 时**必须** true          |
| `TargetSearchNetwork`        | boolean | Google 搜索网络合作伙伴；产品默认建议 false                       |
| `TargetContentNetwork`       | boolean | 展示网络；搜索专属方案建议 false                                  |
| `TargetPartnerSearchNetwork` | boolean | **必须 false**（后端拒绝：cannot set TargetPartnerSearchNetwork） |

### 地理 / 语言 / 平台

| 字段                    | 类型                                     | 必填 | 说明                                                                                     |
| ----------------------- | ---------------------------------------- | :--: | ---------------------------------------------------------------------------------------- |
| `targetedLocations`     | `{ id: string, bidModifier?: number }[]` |  ✅  | 至少 1 个；**id 必须来自** `siluzan-tso ad geo search -a <acct> -q <地区名>`（禁止编造） |
| `excludedLocations`     | 同上                                     |      | 排除地区；**不得与 `targetedLocations` 有相同 id**（validate 报错；「刚果」等歧义地名 resolve 后须核对） |
| `targetedPlatforms`     | `{ id: number, bidModifier?: number }[]` |      | **30000 桌面 / 30001 移动 / 30002 平板**；`bidModifier` 为**百分比整数**（见下）         |
| `excludedIpAddresses`   | string[]                                 |      | 排除 IP                                                                                  |
| `PositiveGeoTargetType` | number                                   |      |                                                                                          |
| `NegativeGeoTargetType` | number                                   |      |                                                                                          |

**`targetedPlatforms.bidModifier`（创建时，百分比整数，范围 -100～900）**：

- `0` = 不调整；`-40` = 降 40%；`20` = 提高 20%；**`-100` = 排除该设备**（如方案写「平板 -100%」就写 `{ "id": 30002, "bidModifier": -100 }`）。
- 不要写倍率（`0.6`、`1.2`）。倍率只出现在 `device-bid list` 的读回结果里。
- 省略某个设备 ≠ 排除，该设备按不调整投放。方案要求排除时必须显式写 `-100`；validate 对缺项、越界、疑似倍率会给 warning 或 error。
- 创建后再改设备出价用 `ad device-bid set`（倍率口径，`0` = 排除），见 `google-ads-write.md`。

### 时间与 DSA

| 字段              | 类型       | 说明                                 |
| ----------------- | ---------- | ------------------------------------ |
| `StartTime`       | YYYY-MM-DD | 开始日期                             |
| `EndTime`         | YYYY-MM-DD | 结束日期（必须晚于 StartTime）       |
| `adSchedules`     | object[]   | 投放时段，缺省可填全周全天（见模板） |
| `DSADomainName`   | string     | 动态搜索广告域名                     |
| `DSALanguageCode` | string     | 默认 `en`                            |

### 子结构

| 字段                          | 类型     | 说明                                                                                                                                             |
| ----------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `AdGroupsForBatchJob`         | object[] | **至少 1 组**；见下                                                                                                                              |
| `NegativeKeywordsForBatchJob` | object[] | 系列级否词；元素：`{ KeywordText: string[], MatchTypeV2: "BROAD"\|"PHRASE"\|"EXACT", FinalURL: "" }`；**KeywordText 可含空格多词**（见模板示例） |
| `ExtensionsForBatchJob`       | object[] | 附加信息；`Properties` 须 **string→string**（勿用数组值）。SITELINK / STRUCTURED_SNIPPET 见下                                                    |

#### STRUCTURED_SNIPPET（`typeV2` / `AssetFieldType` = `STRUCTURED_SNIPPET`）

| 字段                                            | 说明                                                                                                                          |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `Properties.StructuredSnippetHeaderValue.Key`   | **须为合法英文标头**（`ad extension snippet-headers`）。非法值如 `Features` 会被 `campaign-validate` 拦截（建议 `Amenities`） |
| `Properties.StructuredSnippetHeaderValue.Value` | 非空字符串数组（各条目有长度上限）                                                                                            |

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
| `MaxCPCAmount`        | number                |       ✅       | 元；**任何出价策略都必须 > 0**（后端恒写 `cpc_bid_micros`，缺省/0 → Google「Too low」，整组及其词/广告全部失败）；方案无值先问用户 |
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

文案按 `references/google-ads/rules/google-ads-creative-optimization.md` **1.2 / 1.3**：先定 B2B/B2C，写满 15 标题 + 4 描述；禁止空话与无活动促销。`campaign-validate` 还拦：组内标题重复、**不同广告组共用同一标题**。

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

| 规则                    | 说明                                                                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 基础                    | `customerName` / `campaign` 非空；`Budget > 0`；地理/语言至少 1 项                                                             |
| 地域一致性              | 外层 `locations` 非空时，长度须等于 `targetedLocations`；每个 location `id` 须为数字字符串                                     |
| 网络                    | `TargetPartnerSearchNetwork` 须 false；不可同时关闭 Google 搜索与搜索网络                                                      |
| RSA / 关键词 / 附加信息 | 标题 **15** 条、描述 **4** 条（须写满）；字符上限、词面非空；RSA `Path1`/`Path2` 必填；SITELINK 行长度限制                     |
| 否词误填                | `KeywordsForBatchJob` 含常见否词词根或与 `NegativeKeywordsForBatchJob` 重复 → **warnings**（不阻断，须 Agent 修正后再 create） |
| 实务                    | 日期格式与先后、出价策略与配套字段一致                                                                                         |
| 否词屏蔽正向词          | 某条否词（按 BROAD / PHRASE / EXACT 规则）会屏蔽正向关键词 → **warning**，列出被屏蔽的词和所在组；方案自相矛盾，须问用户删否词还是删关键词 |
| CPC 上限 ≥ 日预算       | `TargetSpend_BidCeilingAmount` 或组 `MaxCPCAmount` ≥ `Budget` → **warning**；等于没设上限，创建前须向用户确认                  |
| 设备                    | `targetedPlatforms` id 非法/重复、`bidModifier` 越界 → error；疑似倍率、缺少桌面/移动/平板之一 → warning（省略 ≠ 排除）        |
| 政策风险词面            | 关键词或 RSA 含高拒审词（guaranteed、cure、replica、casino、CBD 等）→ **warning**，按风险类型汇总                              |
| 裸词补符号              | 块级 `MatchTypeV2` 为 PHRASE / EXACT 时裸词补引号或 `[ ]` 属预期修复，每块只汇总一条 warning，不逐词列出                       |

**政策预检的限制**：网关不提供 Google Ads `validate_only` 或政策预检接口，`PolicyViolation`（包括与投放地域相关的 `LEGAL_REQUIREMENTS`）只有提交后在 `ad batch get` 的 `failedOperations` 里才能看到。上表的「政策风险词面」只能覆盖跨行业高拒审词，无法预判地域相关政策。投放国家多（几十个以上）且属于纺织、家居、保健等可能涉及各国标签/准入法规的品类时，在审查稿里提示用户「部分关键词可能被地域相关政策拒绝，需创建后才能确认」。

`ad campaign-validate` 通过不保证 BatchJob 成功（例如仅写 `DestinationUrl` 未写 `Finalurl` 时 validate 仍可能 ✅）。异步结果用 `ad batch get` 轮询；`HasFailed` / 部分失败时用 `ad batch diff` 对照 JSON 补缺，系列级失败时改 JSON 重提，勿在半成品上反复整包创建。**附加信息（Sitelink 等）batch 漏建时**：`batch diff` 后 **自动** `ad extension *` 补挂，勿仅询问用户（见 `references/google-ads/google-ads-campaign-plan.md` § batch diff 后自动补建）。写操作须 `--commit`，见 `references/google-ads/google-ads-write.md` § ad campaign-create。
