# 账户分析数据拉取与周期报告

> 流程见 `playbooks.md` **P1** / **P4** / **P4-FB**；报告纲要见 `report-templates/*.md`。TSO 平台优化报告见 `reporting.md`。

## Contents

- 数据时效性（实时 vs 每日同步）—— 选命令前必读
- 工作流入口（线性步骤见 playbooks）
- 报告硬约束
- Google 账户分析：`google-analysis` 命令
- Meta / Facebook Ads 账户分析
- TikTok 账户分析
- Bing（BingV2）账户分析（含原始实体只读运营子命令 / `--aggregation` 近实时报表）
- Yandex 账户分析
- 报告模板

---

---

## 数据时效性（实时 vs 每日同步）—— 选命令前必读

涉及"今天/当天/今日消耗""实时消耗排行"等问题时，**必须**先按此表确认接口口径，否则今天消耗会被误判为 0。

| 命令 / 接口                                                                                                                                                                           | 时效性                                                                                                                                                      | 能否查"今天"                      | 典型用途                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | ------------------------------------------------ |
| `google-analysis --sections overview`（Google 网关 `OverviewSectionData`）                                                                                                            | **实时**；请求起止为 **YYYY-MM-DD**（不附加时区）                                                                                                           | ✅ 可查当天                       | 当天/今日消耗、当天高消耗账号排行                |
| `google-analysis --sections campaign-types`（`types-summary`）                                                                                                                        | **实时**                                                                                                                                                    | ✅ 可查当天                       | 当天系列类型分布                                 |
| `google-analysis` 其他 range 维度（`campaigns` / `keywords` / `devices` / `geographic` / `daily-metrics` / …）                                                                        | 实时（受 Google Ads API 同步延迟影响）；网关维传 YYYY-MM-DD；`daily-metrics` 与 `stats` 一样按 UTC+8 起止，落盘行与 `--start`~`--end` 逐日一致            | 可查当天，但当天可能尚未结算      | 周期分析、报告                                   |
| `stats -m Google` / `balance-scan -m Google` / `accounts-digest -m Google` / `list-accounts -m Google` 合并消耗（TSO `account-spend-overview`，2026-05 起）                           | **后端自动分流**：窗口完全在历史 → `database`；含今天 → `googleCombined`。**凡走本接口的请求起止一律东八区墙钟**（`…T00:00:00+08:00` ~ `…T23:59:59+08:00`） | ✅ 可查当天（含今天时切实时聚合） | 历史回溯、巡检、周报 KPI、余额续航估算           |
| `stats` / `balance-scan` / `accounts-digest` / `list-accounts` 的 **TikTok / Yandex / BingV2 / MetaAd** 合并消耗（TSO `accountsoverview`；MetaAd OAuth 户走 `FacebookAds` 段） | **每日同步昨天**                                                                                                                                            | ❌ 查今天会全为 0                 | 历史回溯、巡检、余额续航估算（口径为"截至昨天"） |
| `balance`（`GetMediaAccountInfo`）                                                                                                                                                    | 实时                                                                                                                                                        | —                                 | 仅当前余额，不反映消耗                           |

**选用规则**：

- 「今天/当天/今日消耗」「实时消耗排行」 → 优先 `google-analysis(-batch) --sections overview`，`--start` / `--end` 都设为今天；
  - Google 单账户/批量取数也可直接 `stats -m Google` 把 `--end-date` 设为今天，后端会切到 `googleCombined` 模式给实时消耗（但**不会**返回余额/币种/账户名）。
- 「最近 N 天消耗 / 周报 / 月报 / 余额续航」 → `stats` / `balance-scan` / `accounts-digest`，默认窗口截至昨天即可（Google 此时走 `database`，包含完整字段）。
- **禁止**用 TikTok / Yandex / BingV2 / MetaAd 的 `accountsoverview` 接口判断当天消耗（仍是每日同步）。
- **禁止**给非 Google 媒体的当天高消耗场景加 `--min-spend`：其预筛选来自非实时 `accountsoverview`，会把今天有消耗的账号当成 0 给筛掉。Google 媒体当 `--end-date` 设为今天时，预筛选走的是 `googleCombined` 实时数据，可以使用 `--min-spend`。

---

## 工作流入口（线性步骤见 playbooks）

> 线性步骤见 `playbooks.md`：单户画像 **P1**、Google 周期 **P4**、Meta 周期 **P4-FB**、多账户批处理 **P5**、OKKI **P6**、询盘 **P7**。
> 「使用 okki 周报模板」→ **P6**（勿按默认 10 章追问；终稿 `google-analysis okki-render`，禁止 Agent 手写 xlsx）。Google 周期 Excel（非 OKKI/询盘）→ **P4** + `report-templates/google-period-report-excel.md`。

拉数落盘：`google-analysis … --json-out <dir>`（Google）或 `yandex-analysis` / `bing-analysis` / `facebook-analysis` / `tiktok-analysis`；目录内生成 `<section>-<accountId>.json` + `manifest-<accountId>.json`（Meta/TikTok/Bing/Yandex 为 `report-manifest-<accountId>.json`）。读盘协议、交付自检与报告首行标注统一见 `references/core/agent-conventions.md` §三、§七。

---

## 报告硬约束

报告中「系列状态列」不得来自账户接口（账户状态 ≠ 系列状态，见 `references/core/agent-conventions.md` §四）：系列是否启用**必须**来自 `ad campaigns`（含 `statusDisplay`）或 `google-analysis --sections campaigns` 落盘的系列数据。

**报告脚本禁止自行映射 `campaignStatus` 枚举**：网关值为 PascalCase（`Enabled`/`Paused`/`Removed`），Agent 若写 `STATUS_MAP[s] || '已移除'` 且未归一大小写，会把「投放中」误显示为「已移除」。`campaigns-*.json` 的 `items[]` 已注入 **`campaignStatusDisplay`**（`投放中` / `已暂停` / `已移除` / `—` / `未知`），HTML/Excel 状态列**直接读该字段**。

### 金额单位

CLI 出口的所有 JSON / 表格金额已统一为**元**，关键字段：

| 命令 / Section                                      | 元字段                                                                                                                                    |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `ad campaigns --json-out ./snap`                    | `budget`（元，与 `--budget` 写参同口径）                                                                                                  |
| `ad groups --json-out ./snap`                       | `maxCPCAmountYuan`、`targetCpaAmountYuan`                                                                                                 |
| `google-analysis campaigns` 落盘 `campaigns-*.json` | `budgetAmountYuan`、`campaignTargetCpaYuan`、`maximizeConversionsTargetCpaYuan`；同行 `spend` / `averageCpc` / `costPerConversion` 也是元 |
| `keyword -k … --json-out ./snap`                    | `averageCpc`、`lowTopOfPageBid`、`highTopOfPageBid`；根级与每条 `bidAmountCurrency`（有 `-a` 为账户币；无 `-a` 为 USD）                   |
| `balance` 等账户余额接口                            | 余额字段为`remainingAccountBudget`（元）                                                                                                  |

旧字段 `budgetAmount`（分）、`maxCPCAmountDisplay`、`*Micros`（微元）**已不再落盘**，下游脚本无需做单位换算。金额保留 2 位小数，带货币代码（如 `￥50.00 CNY`、`$50.00 USD`），`currencyCode` 从响应读取，跨币种账户分表；细则见 `references/accounts/currency.md`。

### 预算建议

基于当前实际预算（如 `ad campaigns --json-out ./snap` 的 `budget`（元）或 `google-analysis campaigns-*.json` 的 `budgetAmountYuan`（元））、历史日均消耗、用户给的预算上限给出建议。数据不足以判断时，在报告里写明「建议区间需用户确认」而非直接给高风险数字。

---

## Google 账户分析：`google-analysis` 命令

> **重要**：`google-analysis` 是统一入口，所有维度都通过 `--sections` 选取。关键词维度用 `--sections keywords`，**不要**用 `ad keywords` 代替。否词名单用 `--sections negative-keywords`，**不要**另跑 `ad keywords --negative`。这份否词是精简列表：`keywordText`、`matchTypeV2`、`negativeLevel`、`campaignId`、`adGroupId`，没有系列名，也不按 `--start` / `--end` 过滤。涉及「今天/当天」消耗的口径见本文顶部「数据时效性」表。

```bash
# 单维度
siluzan-tso google-analysis -a <id> --sections overview --json-out <dir>

# 多维度（周期报告默认 9 个拉数维，含 audience 与 negative-keywords）
siluzan-tso google-analysis -a <id> --start YYYY-MM-DD --end YYYY-MM-DD \
  --sections overview,daily-metrics,dimension-summary,campaigns,devices,geographic,audience,keywords,negative-keywords --json-out <dir>

# 全部维度（省略 --sections）
siluzan-tso google-analysis -a <id> --json-out <dir>

# 排除慢/不需要的维度
siluzan-tso google-analysis -a <id> --exclude materials,gold-account --json-out <dir>
```

### 选项

| 选项                        | 说明                                                                                                                                                                     |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `-a, --account <id>`        | Google `mediaCustomerId`（必填）                                                                                                                                         |
| `--json-out <dir>`          | 必填；每维一个 `<section>-<accountId>.json` + `manifest-<accountId>.json`                                                                                                |
| `--sections <list>`         | 仅执行指定维度（逗号分隔）；省略=全部 25 个                                                                                                                              |
| `--exclude <list>`          | 排除指定维度；与 `--sections` 可叠加                                                                                                                                     |
| `--start` / `--end`         | 统计区间（YYYY-MM-DD，**只传年月日**；默认区间按 UTC+8 日历）。与 `stats -m Google`（会加成 `+08:00`）不同；省略=近 7 天截至昨天；`final-urls`/`campaign-types` 自动忽略 |
| `--concurrency <n>`         | 并发数，默认 5，上限 16                                                                                                                                                  |
| `--limit <n>`               | 透传给 `keywords`/`search-terms`（默认 **0**=不封顶；`orderByCost=true`）                                                                                                |
| `--level <lvl>`             | 透传给 `extensions`（Account/Campaign/Ad Group）                                                                                                                         |
| `--audience-type <type>`    | 透传给 `audience`（SystemDefined/UserDefined）                                                                                                                           |
| `--no-order-by-cost`        | 透传给 `keywords`/`search-terms`                                                                                                                                         |
| `--cost-greater <n>`        | 仅 **`geo-matched` / `campaign-geo` / `campaign-geo-matched`**：网关 `costGreater`（整数，单位以后端为准）                                                               |
| `--click-greater <n>`       | 仅 **`geo-matched` / `campaign-geo` / `campaign-geo-matched`**：网关 `clickGreater`                                                                                      |
| `--conversions-greater <n>` | 仅 **`geo-matched` / `campaign-geo` / `campaign-geo-matched`**：网关 `conversionsGreater`                                                                                |
| `--verbose`                 | 打印详细错误                                                                                                                                                             |

### 维度列表（25 个）

| 维度                   | 说明                                                                                                                                                                                                                                  |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `overview`             | 总览（实时，可查当天；当天高消耗账号排行首选）                                                                                                                                                                                        |
| `keywords`             | 关键词；默认 `costGreater=0`（仅有消耗）、`limit=0`（不封顶）、`orderByCost=true`；可用 `--limit` 限制 Top N                                                                                                                          |
| `search-terms`         | 搜索词；默认 `limit=0`（不封顶）、`orderByCost=true`；落盘前过滤 `spend>0`；含 `queryTargetingStatus` / `queryTargetingStatusZh`（已添加/已排除/都没有）；可用 `--limit` 限制 Top N                                                   |
| `campaigns`            | 广告系列                                                                                                                                                                                                                              |
| `campaign-hour`        | 系列按小时（行在 `items[]`）                                                                                                                                                                                                          |
| `ads`                  | 广告；与 `ad list` 同源                                                                                                                                                                                                               |
| `extensions`           | 附加信息；可选 `--level`                                                                                                                                                                                                              |
| `devices`              | 设备分布（账户级 `DeviceSectionData`）                                                                                                                                                                                                |
| `geographic`           | 地域分布（账户级 `GeographicSectionData`，网关侧常按国家聚合）                                                                                                                                                                        |
| `geo-matched`          | 相符地理位置（Matched locations，`user_location_view`）账户级按国家/地区汇总                                                                                                                                                          |
| `campaign-geo`         | 广告系列维度地理（可选 `--cost-greater` / `--click-greater` / `--conversions-greater` 与网关一致）                                                                                                                                    |
| `campaign-geo-matched` | 相符地理位置（Matched locations）系列级明细（可选同上阈值参数）。日期区间内曾经命中、后来已移除的国家仍会出数 |
| `geo-targeted`         | 当前仍在投放的地理位置（未移除的定位）。OKKI 国家表用这个，不含已删除国家 |
| `campaign-device`      | 广告系列维度设备（行可含系列/组）。`deviceType` 字面量多为 **`Desktop` / `Mobile` / `Tablet`**（Title Case）或中文「计算机 / 移动设备」，**不是** `DESKTOP`/`MOBILE`。出价调整展示用 `bidModifierDisplay`（对齐 Google 后台：未设置=`—`，`0.6`=`-40%`）；`bidModifier` 仍是倍率，禁止自行换成正百分比                                                                 |
| `audience`             | 受众；可选 `--audience-type`                                                                                                                                                                                                          |
| `asset-images`         | 图片素材                                                                                                                                                                                                                              |
| `videos`               | 视频                                                                                                                                                                                                                                  |
| `materials`            | 图片+视频拍平进 `items[]`，每行带 `assetType: 'image' \| 'video'`                                                                                                                                                                     |
| `resource-counts`      | 结构统计                                                                                                                                                                                                                              |
| `conversion-actions`   | 转化动作                                                                                                                                                                                                                              |
| `daily-metrics`        | 按日指标（主平台 `GET …/report/media-account/google/account-daily-reports`，`--json-out` 落盘为按日数组）。**广告诊断报告**中：金额/CPA **保留 2 位小数**，转化/点击/展示为整数；须配趋势**分析**段落（见 `google-ads-diagnosis.md`） |
| `gold-account`         | 黄金账户                                                                                                                                                                                                                              |
| `ads-index`            | 质量指标                                                                                                                                                                                                                              |
| `final-urls`           | 最终到达网址（不传 `--start`/`--end`）                                                                                                                                                                                                |
| `dimension-summary`    | 账户汇总                                                                                                                                                                                                                              |
| `campaign-types`       | 系列类型（实时，可查当天；不传 `--start`/`--end`）                                                                                                                                                                                    |

### 落盘 JSON

| 字段            | 含义                                                                   |
| --------------- | ---------------------------------------------------------------------- |
| `schemaVersion` | 文件内固定 `3`                                                         |
| `section`       | 维度名（与文件名 stem 一致；仅标识，读数据用不到）                     |
| `itemCount`     | `items.length`                                                         |
| `items`         | **所有列表维度的行数据**统一入口（含 `materials`）；汇总维度为 `[]`    |
| `record`        | **汇总维度**的整块对象；列表维度为 `null`                              |
| `meta`          | 仅 `search-terms` / `ads`：网关 `code`/`message`（与数据无关，可忽略） |

**唯一判别规则**：`record` 非 `null` → 读 `record`（汇总维度）；否则 → 读 `items[]`（列表维度）。

`overview` 的 `activeDays` / `averageDailyCost` **只在 `record` 根上**（本期、消耗>0 的自然日；日均=`totalCost/activeDays`）。`currentPeriod` / `previousPeriod` **没有**这两个字段——禁止 `cur.get("activeDays")`（会整行写成「—」）。上期活跃天数接口不返回；要环比另拉上期 `daily-metrics` 数 `spend>0` 的天数，禁止编造。`google-analysis render --snapshot-dir` 会把这两个字段并进 `kpis`。

| 桶       | 维度                                                                                                                                                                                                                                                                       | 读法        |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------- |
| **列表** | `keywords`、`search-terms`、`campaigns`、`campaign-hour`、`ads`、`extensions`、`devices`、`geographic`、`geo-matched`、`campaign-geo`、`campaign-geo-matched`、`geo-targeted`、`campaign-device`、`audience`、`asset-images`、`videos`、`materials`、`daily-metrics`、`conversion-actions` | `d.items[]` |
| **汇总** | `overview`、`resource-counts`、`dimension-summary`、`gold-account`、`ads-index`、`final-urls`、`campaign-types`                                                                                                                                                            | `d.record`  |

脚本示例（Node）—— 所有维度同一套读法：

```javascript
const d = require("./snap/campaigns-9526903813_20260401-20260430.json");
const data = d.record ?? d.items; // record 非空=汇总维度；否则=列表行
```

旧快照（manifest `schemaVersion` 1/2，无 `items`/`record`）须按 `*.outline.txt` 最后一行类型读取。

### stdout 摘要

```json
{
  "kind": "siluzan-tso-google-analysis-snapshot-batch",
  "absoluteSnapshotDir": "/abs/path/to/snap-google",
  "manifestFile": "manifest-9526903813.json",
  "accountId": "9526903813",
  "totalSections": 25,
  "succeeded": 25,
  "failed": 0,
  "concurrency": 5,
  "elapsedMs": 18712,
  "results": [
    { "section": "overview", "ok": true, "elapsedMs": 3380, "file": "overview-9526903813.json" }
  ]
}
```

**容错**：单维度失败不中断整批；`failed > 0` 时退出码 2，`results[].error` 给出原因。Agent 据此决定是否重跑失败维度。

### 指标字段对照

| 展示名       | 响应中常见字段名    |
| ------------ | ------------------- |
| 消耗         | `spend`             |
| 展示         | `impressions`       |
| 点击         | `clicks`            |
| 转化次数     | `conversions`       |
| 转化价值     | `conversionsValue`  |
| 点击率       | `ctr`               |
| 转化率       | `conversionRate`    |
| 平均点击成本 | `averageCpc`        |
| 转化成本     | `costPerConversion` |

`conversionsValue` 是账户币种的 Google「转化价值」，和 `conversions`（次数）不是一回事。带 `startDate` / `endDate` 时，`keywords`、`search-terms`、`campaigns`、`ads`，以及 `ad keywords` / `ad search-terms` / `ad campaigns` / `ad groups` / `ad list` 的行上会有这个字段。报告要写转化价值或 ROAS 时用它：`ROAS = conversionsValue / spend`（`spend` 为 0 时该格写「—」）。禁止用消耗、点击、转化次数自己算。行上没有该字段（设备、每日趋势，或当次快照未返回）写「未返回」，禁止把系列价值摊到关键词或搜索字词上。账户级三格仍只汇总 `campaigns` 的 `items[]`。

### CampaignSectionData 关键字段

> `campaigns` 维度的系列行在 `items[]`（`schemaVersion 3` 起统一信封；本节下文的 `campaigns[]` 即指 `items[]`）。

`items[]` 每行额外包含：`conversionsValue`、`conversionsValuePerCost`（`spend ≤ 0` 时为 0）、`campaignTargetCpaYuan`、`maximizeConversionsTargetCpaYuan`、`manualCpcEnhancedCpcEnabled`、`percentCpcEnhancedCpcEnabled`。所有金额字段（`*Yuan` 后缀）已统一为元，可直接展示，无需换算。

账户级转化价值 / 单转化价值 / ROAS：先确认 `campaigns` 行是否带 `conversionsValue`；有才对 `items[]` 汇总（`Σ conversionsValue`、`÷ Σ conversions`、`÷ Σ spend`），禁止对行上 `conversionsValuePerCost` 再平均。整批无该字段 → 写「未返回」，禁止用转化次数×1 等估算。`overview` period 块通常没有此字段。上期另拉等长上一周期 `campaigns` 再同样判断（见 `google-period-report-excel.md`）。

| 字段                                  | 含义                                             |
| ------------------------------------- | ------------------------------------------------ |
| `campaignStatus` / `campaignStatusV2` | 网关原始枚举（`Enabled` / `Paused` / `Removed`） |
| `campaignStatusDisplay`               | CLI 注入的中文状态文案；**报告状态列读此字段**   |

日预算字段为 `budgetAmountYuan`（元），脚本可直接 `row.budgetAmountYuan`；网关原始 `budgetAmount`（分）已不再落盘。

#### 竞争指标 `competitiveMetrics`

`campaigns[]` 每系列可带 `competitiveMetrics`，**值为 0~1 小数**（如 `0.0999` ≈ 9.99%）。常见字段：

| 字段                                                                                             | 含义                      |
| ------------------------------------------------------------------------------------------------ | ------------------------- |
| `searchImpressionShare`                                                                          | 搜索展示份额              |
| `searchTopImpressionShare`                                                                       | 搜索页首展示份额          |
| `searchAbsoluteTopImpressionShare`                                                               | 搜索绝对页首展示份额      |
| `searchBudgetLostImpressionShare`                                                                | 因预算丢失的搜索展示份额  |
| `searchRankLostImpressionShare`                                                                  | 因排名丢失的搜索展示份额  |
| `searchBudgetLostTopImpressionShare` / `searchRankLostTopImpressionShare`                        | 页首维度预算/排名丢失     |
| `searchBudgetLostAbsoluteTopImpressionShare` / `searchRankLostAbsoluteTopImpressionShare`        | 绝对页首维度预算/排名丢失 |
| `searchExactMatchImpressionShare`                                                                | 完全匹配展示份额          |
| `contentImpressionShare` / `contentBudgetLostImpressionShare` / `contentRankLostImpressionShare` | 展示网络份额与丢失        |
| `searchClickShare`                                                                               | 搜索点击份额              |
| `relativeCtr`                                                                                    | 相对点击率                |

无竞争数据时 `competitiveMetrics` 为 `null`（或缺省）。`competitiveMetrics` 中均为 **0~1 小数**。写 Excel「x%」列：`(v * 100).toFixed(2) + '%'`。

#### 行顶 legacy 份额（与 `competitiveMetrics` 同名 3 项）

`campaigns` / `keywords` 维度的 `items[]` 行顶仍保留 `searchImpressionShare`、`searchBudgetLostImpressionShare`、`searchRankLostImpressionShare`。CLI 落盘前已统一为 **0~1 小数**（与 `competitiveMetrics` 同名项一致；有嵌套时以 `competitiveMetrics` 为准）。Top/AbsoluteTop/Content/ClickShare 等扩展项仅存在于 `competitiveMetrics`。展示为百分比：`(v * 100).toFixed(2) + '%'`。

### campaign-hour 字段

`items[]` 每行：`campaignId`、`campaignName`、`date`、`hour`、`spend`、`impressions`、`clicks`、`conversions`（`schemaVersion 3` 起行统一在 `items[]`，不再是裸数组根）。

---

## Meta / Facebook Ads 账户分析

> 周期/诊断报告：**`facebook-analysis`**（`FacebookAds` 路径，10 Section，含 daily / campaigns / device）。  
> 撰写与 Google 对照表：**`references/analytics/facebook-analysis-guide.md`**（必读）。  
> `report meta-overview` 仅为遗留单维总览：按 `list-accounts` 的 `mediaAccountType` 自动选路径——**FacebookAds**（OAuth 授权）→ `FacebookAds/act_<id>`；**MetaAd**（丝路赞开户）→ `MetaAd/<id>`。多维度请用 `facebook-analysis`。  
> **自动化巡检步骤**（封禁 / 拒审 / 落地页 / 当日超预算 / 空耗预警，只读告警）：`references/operations/hosted-automation-facebook.md`。不要用 `run` 冒充当天/小时。

### 周期报告（默认 6 维，等同 Google 周期报告主流程）

```bash
mkdir -p ./snap-fb
siluzan-tso facebook-analysis -a <mediaCustomerId> --start YYYY-MM-DD --end YYYY-MM-DD --json-out ./snap-fb \
  --sections overview,daily,country,campaigns,audience
```

| 选项                       | 说明                                                                                                                                                                                                |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-a, --account`            | 数字 `mediaCustomerId` 或 `act_<数字>`                                                                                                                                                              |
| `--json-out`               | 必填；`report-manifest-<id>.json` + `<section>-<id>.json`                                                                                                                                           |
| `--sections` / `--exclude` | `overview` `daily` `campaigns` `ad-sets` `platform` `country` `device` `audience` `creative` `material`；**别名**：`daily-metrics`→`daily`，`campaign`→`campaigns`，`geographic`→`country`，`devices`→`platform`，`ads`→`creative`，`materials`→`material` |
| `platform` 响应字段        | `networks[]` 含 `publisherPlatform`（投放平台）+ `platformPosition`（版位）；`network` 与 `platformPosition` 同值，详见 `facebook-analysis-guide.md`                                                |
| `--limit`                  | 仅 `country`：按 spend 降序前 N 条                                                                                                                                                                  |
| `--start` / `--end`        | 同传或同省略；省略=近 7 天截至昨天                                                                                                                                                                  |
| `--concurrency`            | 默认 5，上限 16                                                                                                                                                                                     |

```bash
# 全量（含 device / creative / material）
siluzan-tso facebook-analysis -a <id> --json-out ./snap-fb

# 国家 Top 10
siluzan-tso facebook-analysis -a <id> --sections country --limit 10 --json-out ./snap-fb
```

### 报告模板与交付流程

| 场景               | 模板                                                | 默认终稿                                                                               |
| ------------------ | --------------------------------------------------- | -------------------------------------------------------------------------------------- |
| 周期 / 月报 / 周报 | `report-templates/meta-period-report.md`            | **HTML**（四步：拉数 → 分析 → `meta-period-report.json` → `facebook-analysis render`） |
| 用户指定 Excel     | `report-templates/meta-period-report-excel.md`      | `facebook-analysis render --format xlsx`                                               |
| 深度诊断           | `report-templates/meta-account-diagnosis-report.md` | 按该模板（通常 HTML）                                                                  |

遗留总览：`siluzan-tso report meta-overview -a <id> [--start … --end …] --json-out <dir>`。

### 相对 Google 无法拉取的维度

无 `keywords`、`search-terms`、`extensions`、`final-urls`、`gold-account`、`ads-index`、`conversion-actions`、`resource-counts`、`campaign-types`、`campaign-hour` — 报告中须标注「接口未提供」，禁止编造。按日用 `daily`，系列用 `campaigns`。

---

## TikTok 账户分析

与 `google-analysis` / `facebook-analysis` 同架构：`tiktok-analysis -a … --json-out …`（省略子命令名默认执行 `run`，批量拉取全部维度或 `--sections` 指定子集）。

| 选项                       | 说明                                                                                                                                                                                                                                                                               |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--sections` / `--exclude` | `overview` `campaigns` `ad-groups` `ads` `videos` `audience-gender` `audience-age` `audience-interest-category` `audience-country-code` `audience-platform` `audience-language` `audience-merged`（12 个）；**别名**：`audience`→`audience-merged`，`ad-groups-report`→`ad-groups` |
| `--take`                   | 消耗/条数上限，默认 100（`overview` 不适用）                                                                                                                                                                                                                                       |
| `--start` / `--end`        | 同传或同省略；省略=近 7 天截至昨天                                                                                                                                                                                                                                                 |
| `--concurrency`            | 默认 5，上限 16                                                                                                                                                                                                                                                                    |

```bash
mkdir -p ./snap-tt

# 全 12 维
siluzan-tso tiktok-analysis -a 1234567890 --json-out ./snap-tt

# 仅拉总览 + 系列 + 受众合并
siluzan-tso tiktok-analysis -a 1234567890 --start 2026-03-01 --end 2026-03-31 \
  --sections overview,campaigns,audience-merged --json-out ./snap-tt
```

辅助查询（不接受 `--sections`，非账户投放维度）：

| 子命令                                  | 说明                                     |
| --------------------------------------- | ---------------------------------------- |
| `tiktok-analysis areacode`              | 区域代码枚举（主平台，无需 `--account`） |
| `tiktok-analysis interest-list -a <id>` | 兴趣类目树（需配置 `tiktokApiUrl`）      |

`--start`/`--end` 同传同省略，省略默认近 7 天（截至昨天）。报告模板：`report-templates/tiktok-period-report.md`。

> **自动化巡检步骤**（封禁 / 拒审 / 落地页 / 当日超预算 / 空耗预警，只读告警）：`references/operations/hosted-automation-tiktok.md`。

### TikTok 只读运营（`tiktok-analysis` 子命令，TikTokAPI）

> 与上面 `run` 的 TSO 看板周期报表不同。账户状态/余额、系列预算、组出价、广告落地页/拒审、**可含今天与小时**的官方报表走以下子命令。花费指标名是 `spend`（不要 `stat_cost`）。`PageSize` 由 CLI 显式传入并自动翻页。

| 子命令 | 说明 |
| --- | --- |
| `account-status` | `GetAdvertiserInfo/Tiktok`：`status`/`balance`/`timezone`；须**拥有**；`STATUS_ENABLE` 为正常 |
| `campaign-entities` | 系列 `budget`/`budget_mode`/`budget_optimize_on`/`operation_status`（无 `status` 字段） |
| `adgroup-entities` | 组 `bid_type` 与对应出价、组预算；CBO 时组预算为 0 |
| `ad-entities` | 落地页；拒审加 `--secondary-status AD_STATUS_AUDIT_DENY`；黄条不能当过滤 |
| `official-report` | `query/report/Tiktok/search`：必填 `--data-level`/`--dimensions`/`--metrics`/`--start`/`--end` |

```bash
siluzan-tso tiktok-analysis account-status -a <mediaCustomerId> --json-out ./snap-tt
siluzan-tso tiktok-analysis campaign-entities -a <mediaCustomerId> --json-out ./snap-tt
siluzan-tso tiktok-analysis ad-entities -a <mediaCustomerId> \
  --secondary-status AD_STATUS_AUDIT_DENY --json-out ./snap-tt
siluzan-tso tiktok-analysis official-report -a <mediaCustomerId> --json-out ./snap-tt \
  --start 2026-08-17 --end 2026-08-17 \
  --data-level AUCTION_CAMPAIGN --dimensions campaign_id --metrics spend
```

**ROAS 口径**（对齐 [网页事件](https://ads.tiktok.com/help/article/page-events?lang=zh) / [应用内事件](https://ads.tiktok.com/help/article/in-app-events?lang=zh)）：`--metrics` 含完付或 ROAS 时 CLI 自动附带 `total_purchase_value,complete_payment_roas,total_active_pay_roas`。落盘行有 `revenue` / `revenueSource` / `roas` / `roasSource`，多行汇总在 `totals`（先加总 spend/revenue 再除）。`complete_payment` 是网页支付完成**次数**；金额用 `total_purchase_value`（总付费价值）。ROAS 优先官方列 `complete_payment_roas` / `total_active_pay_roas`。**禁止** `complete_payment/spend`，**禁止**把完付=0 判成「像素没回传」，**禁止**对各组 `roas` 取平均。不确定时先 `adgroup-entities` 看 `optimization_event`。

---

## Bing（BingV2）账户分析

> **日期**：可含昨天（及今天，数据可能不完整）。网关未显式传 `returnOnlyCompleteData` 时，区间碰到今天/昨天会自动改为近实时。省略时 CLI 默认截至昨天的近 7 天。用户要**已结束的完整自然月**（如「6月份」）→ `--start` 当月 1 日、`--end` 当月最后一天（6 月 = `06-30`，**禁止**减 1 天），见 `report-templates/bing-period-report.md` §日期规则。
>
> **自动化巡检步骤**（封禁 / 拒审 / 落地页 / 当日超预算 / 空耗预警，只读告警）：`references/operations/hosted-automation-bing.md`。

与 `google-analysis` / `facebook-analysis` 同架构：`bing-analysis -a … --json-out …`（省略子命令名默认执行 `run`，批量拉取全部维度或 `--sections` 指定子集）。

| 选项                       | 说明                                                                                                                                                                                                                                    |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--sections` / `--exclude` | 可选 11 个：`overview` `device` `geographic` `age-audience` `gender-audience` `audience-merged` `campaigns` `ad-groups` `ads` `keywords` `search-terms`；**默认 10 个**（不含 `audience-merged`，勿与年龄/性别维同时拉）；**别名**：`devices`→`device`，`geo`→`geographic`，`search-queries`→`search-terms` |
| `--limit`                  | 仅 `keywords` / `search-terms`：条数上限，默认 100                                                                                                                                                                                      |
| `--start` / `--end`        | 同传或同省略；可含昨天/今天（可能不完整）；省略=截至昨天的近 7 天                                                                                                                                                                      |
| `--concurrency`            | 默认 5，上限 16                                                                                                                                                                                                                         |

```bash
mkdir -p ./snap-bing

# 默认 10 维（含年龄/性别受众，不含 audience-merged）
siluzan-tso bing-analysis -a <mediaCustomerId> --json-out ./snap-bing

# 仅拉总览 + 关键词（limit 50）
siluzan-tso bing-analysis -a <mediaCustomerId> --start 2026-03-01 --end 2026-03-20 \
  --sections overview,keywords --limit 50 --json-out ./snap-bing
```

报告模板：`report-templates/bing-period-report.md`（**每个 section 须写「分析」**；**余额**：`overview` section 落盘 JSON 常自动校正 0 快照，读 `balance`/`remainingAccountBudget` 或 `balance` 命令；**环比**：网关 `previousPeriod` 常空，CLI 二次拉上一周期回填）。

### 点击率 / 转化率口径（必读）

Bing 的 `ctr` / `conversionRate` 为 0~1 小数\*\*（`0.007434` = 0.74%），与 Google `schemaVersion ≥ 2` 一致。

| 场景           | 正确写法                                               | 错误写法                                        |
| -------------- | ------------------------------------------------------ | ----------------------------------------------- |
| 报告 HTML 展示 | `(ctr * 100).toFixed(2) + '%'`                         | `ctr.toFixed(2) + '%'`（会显示 74% 而非 0.74%） |
| Excel 0~1 列   | 直接写 JSON 数值                                       | 再 ÷100                                         |
| 脚本校验       | `clicks / impressions` 与 `ctr` 应一致（允许四舍五入） | 心算或凭印象                                    |

各 `overview-*.outline.txt` 等文件头部含 `//` 硬提示，Agent **须先读 outline** 再写报告。

### Bing 只读运营子命令（原始实体，供自动化监控/优化使用）

> 以下均为 `bing-analysis` 的子命令（与 `run`/`render` 平级），专供「账户封禁」「拒审巡检」
> 「余额续航」等场景的**原始实体**接口（非报表数值），不带日期区间参数。系列/广告组/广告的
> **花费/点击/转化**等报表数值走 `run --sections campaigns/ad-groups/ads`（见下方「近实时报表」），
> 与本节的 `campaign-entities`/`ad-entities` 不是同一份数据，不要混用。
> 本批（2026-08）**仅只读**：暂停 / 改价 / 改预算暂无接口。

| 子命令               | 用途                                                                                          |
| -------------------- | --------------------------------------------------------------------------------------------- |
| `account-status`     | 账户生命周期状态（`status=Active` 为正常投放），封禁监控用                                    |
| `campaign-entities`  | 系列原始实体：`dailyBudget`/`isSharedBudget`/`status`/`biddingScheme`（非报表数值）           |
| `ad-entities`        | 单系列广告列表（**必须**带 `--campaign-id`，否则 400）：落地页 `finalUrls`、`editorialStatus` |
| `bulk-ads`           | 全账户 Bulk 广告下载：拒审巡检首选，避免按系列遍历；回传 `syncTimeUtc` 可做增量               |
| `insertion-orders`   | 插入订单（IO）列表：额度看 `budgetRemaining`/`spendCapAmount`；无预付余额字段                 |
| `monthly-spend`      | 官方月消耗（非预付余额）；`--year`/`--month` 须成对传入或都省略查北京当月                     |

```bash
# 系列原始实体（预算/出价策略），配合 run --sections campaigns 的花费数值一起判断能否改价/超预算
siluzan-tso bing-analysis campaign-entities -a <mediaCustomerId>

# 账户封禁监控
siluzan-tso bing-analysis account-status -a <mediaCustomerId>

# 全账户拒审巡检（首次全量；下次把上次响应的 syncTimeUtc 回传做增量，最早回溯 30 天）
siluzan-tso bing-analysis bulk-ads -a <mediaCustomerId> --editorial-status Disapproved
siluzan-tso bing-analysis bulk-ads -a <mediaCustomerId> --editorial-status Disapproved --last-sync-time-utc 2026-08-16T03:12:00Z

# 余额续航：IO 额度 + 官方月消耗（无 IO 时没有额度上限，只看 monthly-spend）
siluzan-tso bing-analysis insertion-orders -a <mediaCustomerId>
siluzan-tso bing-analysis monthly-spend -a <mediaCustomerId>
```

**要点**：

- `ad-entities` 单系列查必须带 `--campaign-id`；查全账户拒审/落地页用 `bulk-ads`，不要按系列遍历 `ad-entities`。
- `bulk-ads` 底层为官方异步下载任务，网关等文件就绪才返回，大账户可能要几分钟，不适合放在页面同步加载场景，适合定时巡检。

### Bing 近实时报表（`bing-analysis --aggregation`，按日/小时分桶）

> `--aggregation` / `--return-only-complete-data` 仅 `campaigns`/`ad-groups`/`ads` 三个 section 支持
> （分别对应网关 `CampaignReport`/`AdGroupReport`/`AdReport`）。省略这两个参数时，含昨天/今天的区间
> 同样可以拉（网关自动近实时）；`--aggregation` 用来拿 Daily/Hourly 分桶。省略日期且传了 `--aggregation` 时默认今天当天。

```bash
# 单日花费与日预算（同一 campaignId 算 spend / dailyBudget；isSharedBudget=true 时 dailyBudget 是共享总额）
siluzan-tso bing-analysis run -a <mediaCustomerId> --json-out ./snap --sections campaigns \
  --start 2026-08-17 --end 2026-08-17 --aggregation Daily

# 近两小时 CPA（按 adGroupId 取最近两个整点 spend/conversions 相加再算 CPA）
siluzan-tso bing-analysis run -a <mediaCustomerId> --json-out ./snap --sections ad-groups \
  --start 2026-08-16 --end 2026-08-17 --aggregation Hourly
```

**要点**：

- `--aggregation` 透传官方 `ReportAggregation`（`Summary` 默认 / `Daily` / `Hourly` / `Weekly` 等），无法识别网关返回 400；非 `Summary` 时行内 `timePeriod` 为**太平洋时区**分桶（如 `"2026-08-16"` / `"2026-08-16|14"`），与北京日期可能错一天。
- `--return-only-complete-data <true|false>` 省略即可：网关按区间是否含今天/昨天自动判断；**拉今天数据不要显式传 `true`**。
- `campaigns`/`ad-groups`/`ads` 三个 section 的 `ctr`/`conversionRate` 已归一为 **0~1 小数**，与周期报告口径一致。

---

## Yandex 账户分析

> **自动化巡检步骤**（归档 / 拒审 / 落地页 / 当日超预算 / 空耗预警，只读告警）：`references/operations/hosted-automation-yandex.md`。
>
> **网关**：直打 YandexAPI `{yandexApiUrl}/yandex-analysis/*`（从 TSO `apiBaseUrl` 推导：`tso-api-ci` → `yandexapi-ci.mysiluzan.com`；可用 `SILUZAN_YANDEX_API` 覆盖）。
>
> **日期**：`start`/`end` 不能晚于今天；省略默认近 7 天（含今天）。**search-terms** 仅支持近 **180 天**（Direct 限制），超窗网关/CLI 均会拒绝。
>
> **账户 ID**：Yandex Client-Login / mediaCustomerId（如 `porg-xxx`，与 `list-accounts -m Yandex` 一致），**不是**纯数字。
>
> **金额**：已从 micros 转为账户币种小数（`/1e6`）。`ctr` / `conversionRate` / `roi` 均为**小数比率**（先读 outline）。`roi` = (购买收益-消耗)/消耗，例如 `-0.5998` 展示为 **−59.98%**，禁止把 `-0.6` 写成 `-0.6%`。

与 `bing-analysis` 同架构：`yandex-analysis -a … --json-out …`（省略子命令名默认执行 `run`）；周期报告默认 **HTML**：`yandex-analysis render`（见 `report-templates/yandex-period-report.md`）。用户要 Excel → `yandex-period-report-excel.md`（Agent 脚本，无 excel 子命令）。

| 选项                       | 说明                                                                                                                                                                     |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `--sections` / `--exclude` | `overview` `daily` `search` `campaigns` `keywords` `search-terms` `geo` `devices`（8 个）；别名：`geographic`→`geo`，`device`→`devices`，`search-queries`→`search-terms` |
| `--limit`                  | 仅 `campaigns` / `keywords` / `search-terms` / `geo`：默认 100，最大 10000                                                                                               |
| `--start` / `--end`        | 同传或同省略；不能晚于今天；省略=近 7 天（含今天）                                                                                                                       |
| `--concurrency`            | 默认 5，上限 16                                                                                                                                                          |

```bash
mkdir -p ./snap-yandex

# 全 8 维
siluzan-tso yandex-analysis -a <porg-xxx> --json-out ./snap-yandex

# 总览 + 系列 + 关键词
siluzan-tso yandex-analysis -a <porg-xxx> --start 2026-07-01 --end 2026-07-31 \
  --sections overview,campaigns,keywords --limit 50 --json-out ./snap-yandex

# 周期报告 HTML（Agent 写完 narrative JSON 后）
siluzan-tso yandex-analysis render \
  --data ./yandex-period-report.json \
  --snapshot-dir ./snap-yandex \
  --out ./yandex-period-report.html
```

`search` / `campaigns` / `keywords` / `geo` / `devices` 在 Direct 侧过滤 `AdNetworkType=SEARCH`。无 Metrica / 写操作。报告模板：`report-templates/yandex-period-report.md`（8 个分析章节必写总结+建议；周趋势读落盘 `daily.weekly[]`，**禁止**自行按 `date` 聚周）。

### Yandex 只读运营（`yandex-analysis` 子命令，YandexAPI）

> 与上面 `run` 的周期报表不同。归档/余额、当日全网花费、组级 CPA、拒审、落地页、按日环比走以下子命令。省略 `--start/--end` 默认当天。金额已是账户币种小数。本批**不能**暂停 / 改价 / 改预算。

| 子命令 | 说明 |
| --- | --- |
| `account-status` | `GET /overview`：`archived` / `balance` / `currency`；官方无封户原因 |
| `campaign-entities` | `GET /campaigns`：`spend` / `weeklyBudget` / `budget` / `strategy` / `targetCpa`；全网加 `--network ALL`；按日加 `--time-increment 1` |
| `adgroup-entities` | `GET /adgroups`：组绩效 + `campaignTargetCpa` / `campaignWeeklyBudget`；默认全网 |
| `ad-entities` | `GET /ads`：落地页 `landingUrls`；拒审 `--status REJECTED`（与 `--time-increment` 互斥） |
| `insights` | `--level daily\|geo\|devices\|keywords\|campaigns\|adgroups\|ads`；geo/devices 全网须 `--network ALL` |

```bash
siluzan-tso yandex-analysis account-status -a <porg-xxx> --json-out ./snap-yandex
siluzan-tso yandex-analysis campaign-entities -a <porg-xxx> --json-out ./snap-yandex \
  --start 2026-08-27 --end 2026-08-27 --time-increment 1 --network ALL
siluzan-tso yandex-analysis ad-entities -a <porg-xxx> --json-out ./snap-yandex \
  --status REJECTED --start 2026-08-27 --end 2026-08-27
siluzan-tso yandex-analysis insights -a <porg-xxx> --json-out ./snap-yandex \
  --level daily --start 2026-08-25 --end 2026-08-27
```

**要点**：Direct 无小时维度。默认报表只出现有消耗对象。`budget` 是系列日预算（自动策略常空），对照 `weeklyBudget`。`campaignTargetCpa` 只取 Search。`roi` 按成交额算。

---

## 报告模板

报告产物可以是 HTML、Excel、PDF、PPT、Markdown 等，数据口径须与快照 JSON 一致。章节与数据块参考 `report-templates/`：
下面这些报告默认都输出HTML,禁止仅输出markdown

| 模板                                 | 用途                                                                                                            |
| ------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `google-period-report.md`            | Google 周期汇总报告章节                                                                                         |
| `demand-gen-analysis-report.md`      | Demand Gen 投放数据分析汇总报告（P4-DG，`google-analysis demand-gen-render`）                                |
| `demand-gen-analysis-report-excel.md`| Demand Gen 汇总报告 Excel（9 Sheet，Agent 脚本）                                                            |
| `google-quarterly-report.md`         | Google 季度经营报告（`google-quarterly collect`+`render`，P10）                                                 |
| `google-quarterly-plan.md`           | P10 下期规划规则（写 `narrative.plan` 前必读）                                                                  |
| `google-account-diagnosis-report.md` | Google 诊断报告纲要                                                                                             |
| `google-ads-diagnosis.md`            | Google Ads 诊断报告完整骨架                                                                                     |
| `meta-period-report.md`              | Meta（Facebook）周期报告                                                                                        |
| `tiktok-period-report.md`            | TikTok 周期报告                                                                                                 |
| `bing-period-report.md`              | Bing 周期报告                                                                                                   |
| `yandex-period-report.md`            | Yandex 周期报告（HTML：`yandex-analysis render`）                                                               |
| `yandex-period-report-excel.md`      | Yandex 周期报告 Excel（Agent 脚本）                                                                             |
| `website-diagnosis-report.md`        | 网站/落地页诊断（`website-diagnosis`，见 P8）；**默认交付 HTML**（`website-diagnosis render`，禁止仅 Markdown） |
| `README.md`                          | 索引与规则                                                                                                      |

`.html` 文件（`report-template.html`、`report-template-academic.html` 等）为 HTML 路线的样式参考。选其他格式时仍以各 `*.md` 纲要为章节清单。
