# Bing（Microsoft Advertising / BingV2）— 账户分析报告（模板纲要）

> **终稿语言**：叙事跟 `meta.lang`（`zh` 或 `en`），表头用该语言。`render` 必须带 `--lang`。
>
> 统计区间：`{startDate}` ~ `{endDate}`（**不可包含今天或昨天**，见下文）  
> 账户：`{mediaCustomerId}`（`{mediaCustomerName}`）  
> **默认交付物**：一份可打开的、带 ECharts 图表的 **HTML 文件**（`bing-period-report.html`）。封面按日期写成「季度」或「月度」，对不上仍是「账户分析」。不要打开 HTML 改称呼。  
> 用户**未指定格式**时一律走下方 **标准四步流程**；**禁止** Agent 手写/拼接 HTML（语法错误会导致报告无法显示）。  
> **用户明确要求 Excel / xlsx** 时：拉数步骤不变，改为 Agent 脚本写 `.xlsx`；**不要**调用 `bing-analysis render`；禁止假设存在内置 excel 子命令。

数据块（Bing 实际支持的 9 类业务维度 + 总览）：总览、设备、地域、受众（年龄/性别）、系列、广告组、广告、关键词、搜索字词。

| CLI `--sections`                                         | 落盘形状（生产实测）                                                        | 报告 `tables.*` / KPI                             |
| -------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------- |
| `overview`                                               | 对象：`currentPeriod` / `previousPeriod` / `balance` / `averageDailyCost` … | → `meta` + `kpis`（环比、余额、日均）             |
| `device`                                                 | `{ devices: Row[] }`                                                        | → `tables.devices[]`                              |
| `geographic`                                             | `{ countries: Row[] }`                                                      | → `tables.geographic[]`                           |
| `age-audience` / `gender-audience`（默认）或 `audience-merged` | 拆分维 `{ audience: [] }`；merged `{ data: { ageAudience, genderAudience } }` | → `tables.audienceAge[]` / `audienceGender[]`（merged 空则回退拆分维） |
| `campaigns`                                              | **根节点数组**                                                              | → `tables.campaigns[]`；**本期 KPI 优先由此累加** |
| `ad-groups`                                              | **根节点数组**                                                              | → `tables.adGroups[]`（含 `qualityScore`）        |
| `ads`                                                    | **根节点数组**                                                              | → `tables.ads[]`                                  |
| `keywords`                                               | **根节点数组**（默认 limit=100）                                            | → `tables.keywords[]`                             |
| `search-terms`                                           | **根节点数组**（默认 limit=100）                                            | → `tables.searchTerms[]`                          |

> Bing **没有** Google 的 `daily-metrics` / `dimension-summary`；报告模板也不渲染这两章。

---

## 标准四步流程（默认 · 交付 HTML）

| 步骤             | 执行者       | 动作                                                                                                                                        |
| ---------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 拉数**      | Agent 调 CLI | `bing-analysis -a <id> --start <s> --end <e> --json-out ./snap-bing`（见下方「日期规则」，默认 10 维含年龄/性别、不含 `audience-merged`）                |
| **2. 分析**      | Agent        | 用 **node/python 脚本**读落盘 JSON（勿用 Read 打开业务 `*.json`），把网关原始字段映射为下方 `tables.*` 契约，完成聚合与洞察                 |
| **3. 写 JSON**   | Agent        | 撰写 `bing-period-report.json`：仅 `meta.accountId` + `narrative`（9 个分析小节）为必填；`kpis`/`tables` 可省略由 `--snapshot-dir` 自动合并 |
| **4. 渲染 HTML** | CLI          | `bing-analysis render` — **校验 narrative 9 个分析小节必含字段**，缺项报错不生成 HTML；**禁止** Agent 手写/拼接 HTML                        |

```bash
# 步骤 1
siluzan-tso bing-analysis -a <id> --start <s> --end <e> --json-out ./snap-bing

# 步骤 4（步骤 2～3 完成后）
siluzan-tso bing-analysis render \
  --data ./bing-period-report.json \
  --snapshot-dir ./snap-bing \
  --out ./bing-period-report.html
```

### `bing-period-report.json` 顶层结构

- `meta`：`accountId`（必填）/ `accountName` / `currency` / `startDate` / `endDate`；可省略由 `--snapshot-dir` 从 `overview` 快照自动合并。
- `kpis`：账户级 KPI —— `spend`/`impressions`/`clicks`/`conversions`/`ctr`/`averageCpc`/`costPerConversion`/`averageDailyCost`/`balance`/`remainingAccountBudget`，含可选 `previousPeriod` 环比对象；可省略。**本期 KPI 优先对 `campaigns` 全系列累加并重算比率**；无 campaigns 时回退 `overview.currentPeriod`。余额/日均仍来自 overview。
- `tables`（可省略，由 `--snapshot-dir` 按上表形状自动映射）：
  - `devices[]`：`{deviceType, spend, impressions, clicks, ctr, averageCpc, conversions, costPerConversion}`
  - `geographic[]`：`{countryOrRegion, spend, impressions, clicks, ctr, averageCpc, conversions, costPerConversion}`
  - `audienceAge[]`：`{ageRange, spend, impressions, clicks, ctr, averageCpc, conversions}`
  - `audienceGender[]`：`{gender, spend, impressions, clicks, ctr, averageCpc, conversions}`
  - `campaigns[]`：`{campaignName, campaignStatus, campaignStatusDisplay, spend, impressions, clicks, ctr, conversions, costPerConversion}`
  - `adGroups[]`：`{adGroupName, campaignName, qualityScore, spend, clicks, ctr, conversions, costPerConversion}`
  - `ads[]`：`{adTitle, adGroupName, adType, spend, clicks, ctr, conversions}`（RSA 的报表 `adTitle` 常为空，`render` 用「系列 / 广告组」兜底展示并在表上方注明）
  - `keywords[]`：`{keyword, matchType, qualityScore, spend, ctr, averageCpc, conversions, costPerConversion}`
  - `searchTerms[]`：`{searchQuery, keyword, deliveredMatchType, spend, ctr, conversions, costPerConversion}`
- `narrative`（**Agent 必填，唯一由 Agent 撰写的叙事内容**）：
  - `executiveSummary[]`：≥1 段执行摘要
  - `sections.{overview,devices,geographic,audience,campaigns,adGroups,ads,keywords,searchTerms}`：每个维度各 `{analysis[]（≥1 条，含数字依据）, suggestions[]（≥1 条）}`
  - `recommendations[]`：≥3 条跨维度优化建议汇总

### 快照合并范围（`--snapshot-dir`）

`render` 传 `--snapshot-dir` 时，CLI 自动补全：

1. `meta`（仅补空字段）
2. **`kpis` / `tables.*` 一律以 CLI 快照覆盖**（有对应 section 时；本期 KPI 优先 campaigns 累加）——数值口径不以 Agent 预填为准

Agent 只需撰写 `narrative`；**禁止手写 HTML**，也**禁止**自填 `kpis`/`tables` 数值（尤其 `ctr` 须为 CLI 落盘的 0~1 小数）。

---

## 日期规则（必读）

- 可以含**昨天**；**今天**也可以拉，但可能不完整（网关未显式传 `returnOnlyCompleteData` 时自动近实时）。含昨天/今天时**不要**显式传 `--return-only-complete-data true`。
- **CLI**：`--start` / `--end` 须**同传或同省略**；省略时默认**截至昨天**的近 7 天（与 `bing-analysis` 实现一致）。
- 小时/日分桶（当日花费、近两小时 CPA）仍须对 `campaigns`/`ad-groups`/`ads` 传 `--aggregation Daily|Hourly`。

### 用户说「X 月 / X月份 / 月报」（已结束的完整自然月）

用户指定某一月份（如「6月份报告」「6月 Bing 月报」）且该月**已结束**时：

| 项        | 规则                                                             |
| --------- | ---------------------------------------------------------------- |
| `--start` | 当月 **1 日**（如 `2026-06-01`）                                 |
| `--end`   | 当月**最后一天**（如 6 月 → `2026-06-30`，**禁止**写成 `06-29`） |
| 报告首行  | `统计区间：YYYY-MM-01 ~ YYYY-MM-<末>`                            |

示例（7 月 8 日要 6 月报告）：

```bash
siluzan-tso bing-analysis -a <id> --start 2026-06-01 --end 2026-06-30 --json-out ./snap-bing
```

**禁止**因旧规则「Bing 不能含今天/昨天」而对**已结束的历史自然月**把 `--end` 减 1 天。6 月 30 日在 7 月 8 日拉数完全合法。拉数后核对 `overview` 落盘里的 `activeDays` 应等于该月日历天数（6 月 = 30）。

---

## 拉数（一次目录）

```bash
mkdir -p ./snap-bing

siluzan-tso list-accounts -m BingV2 -k <mediaCustomerId> --json-out ./snap-bing

# 一次批跑默认 10 维（含 age-audience / gender-audience，不含 audience-merged）
siluzan-tso bing-analysis -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
siluzan-tso balance -m BingV2 --accounts <mediaCustomerId> --json-out ./snap-bing

# 或仅拉本次报告所需维度（--sections 逗号分隔；不要同时写拆分维和 audience-merged）
siluzan-tso bing-analysis -a <mediaCustomerId> --start <S> --end <E> \
  --sections overview,campaigns,device,geographic,age-audience,gender-audience,ad-groups,ads,keywords,search-terms \
  --limit 100 --json-out ./snap-bing
```

- 写脚本前先读各 `bing-*-<id>.outline.txt`，再读 `.json`（见 `references/core/agent-conventions.md` §三）。
- TopN、排序、汇总均在脚本内完成，禁止心算。
- 金额字段已为**元**；`ctr` / `conversionRate` 等：**`bing-analysis` 落盘前已从网关百分数刻度归一为 0~1 小数**（如 `0.0074` = 0.74%），展示百分比用 `(v * 100).toFixed(2) + '%'`；**禁止**把 JSON 数值当「已是百分数」直接加 `%`（会重复 ×100，如 0.74% 显示成 74%）。

---

## 分析纪律（全章节强约束）

**每个 section 的数据表格/图表之后，必须紧跟该 section 的「分析」小节**；整份报告**禁止**只有数据、没有分析。

| 要求       | 说明                                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------------------------- |
| **总结**   | 引用**当 section 落盘 JSON** 中的数字（TopN、占比、合计、环比）；可对比账户 KPI 或 section 内均值                   |
| **建议**   | 1～3 条可执行项（预算、出价、暂停、否词、设备/地域调价等），须点名系列/关键词/国家/设备并引用数据                   |
| **禁止**   | 编造数字、空分析、全章共用一段笼统话而不分 section                                                                  |
| **环比**   | 仅 **总览** `currentPeriod` vs **`previousPeriod`**（CLI 可能二次拉数回填）；**previousPeriod 全 0 时不写 0% 环比** |
| **缺数据** | 某 section 拉数失败或 `items` 为空 → 分析写 `[数据不可用：<原因>]`，**仍须保留分析小节标题**                        |

报告 HTML 建议结构：按下方章节顺序，每章 = **标题 → 数据表/指标卡 → 「分析」**（含总结 + 建议）。

---

## 1. 执行摘要（总览）

- **CLI**：`siluzan-tso bing-analysis -a <mediaCustomerId> --sections overview [--start … --end …] --json-out <dir>`

### 余额（必读 · 勿读 overview 快照）

`OverviewSectionData` 里的 `balance` / `remainingAccountBudget` **不是实时余额**，是报告生成时的快照，**常为 0 或未同步**。

| 正确做法                                                                                            | 错误做法                         |
| --------------------------------------------------------------------------------------------------- | -------------------------------- |
| 读落盘 JSON 的 **`remainingAccountBudget`** 或 **`balance`**（CLI 已用 `GetMediaAccountInfo` 回填） | 直接相信 overview 原始响应里的 0 |
| 字段 **`_balanceSource: "GetMediaAccountInfo"`** 表示已校正                                         | 把 `$0.00` 写进报告而不说明      |
| 仍须独立核对：`siluzan-tso balance -m BingV2 --accounts <id> --json-out <dir>`                      | 用 `stats` 或 overview 推断余额  |

CLI 落盘时会：overview 余额为 0 → 调 `GetMediaAccountInfo` → 写回 `remainingAccountBudget` 与 **`balance`**（与 Web `filterOverviewData` 一致）。

### 环比（必读 · 勿读空 previousPeriod）

网关内嵌的 **`previousPeriod` 常全为 0**。CLI 若检测到为空，会按 Web `calcPrePeriodTimeRange` 规则再请求**上一周期**的 `OverviewSectionData`，将其 **`currentPeriod`** 写入 `previousPeriod`，并标注 **`_previousPeriodSource: "OverviewSectionData-second-fetch"`**。

| 场景                                         | 报告写法                                    |
| -------------------------------------------- | ------------------------------------------- |
| `previousPeriod.spend > 0`（含二次拉数回填） | 可写消耗/点击/转化/CTR/CPC/CPA 环比         |
| `previousPeriod` 仍为空或全 0                | **不写环比为 0%**；写「上一周期数据不可用」 |
| 有 `previousPeriodDateRange`                 | 分析中注明对比区间                          |

### 日均消耗 / 活跃天数

Bing 网关常不返回 `averageDailyCost`、`activeDays`（或为 0）。CLI 落盘前会：① 缺 `totalCost` 时用 `currentPeriod.spend`；② 缺 `activeDays` 时用 `--start`~`--end` 含首尾日历天数；③ `averageDailyCost = totalCost / activeDays`（保留 2 位小数）。

**数据呈现**：区间消耗、展示、点击、转化、CTR、CPC、CPA、日均消耗、**实时余额**（`balance`）、优化分；**有效** `previousPeriod` 时展示环比。写入 JSON `kpis`（可由 `--snapshot-dir` 自动合并）。

**分析（必写）** → 写入 `narrative.sections.overview.{analysis,suggestions}`：

- **总结**：本期 vs 上期消耗/点击/转化/CTR/CPC/CPA 变化（**仅当 previousPeriod 有数据**）；展示份额（`searchImpressionShare`）及预算/排名丢失份额；余额与日均消耗可支撑天数（用 **`balance` / `remainingAccountBudget`**，非 overview 快照 0）。
- **建议**：账户级预算或投放节奏（引用具体百分比或金额）；若展示份额丢失高 → 预算或出价方向；1～3 条。

---

## 2. 设备

- **CLI**：`bing-analysis --sections device` → `DeviceSectionData`（行在 `devices[]`）

**数据呈现**：各 `deviceType` 的展示、点击、消耗、CTR、CPC、转化、CPA；建议附消耗占比。写入 JSON `tables.devices[]`。

**分析（必写）** → 写入 `narrative.sections.devices.{analysis,suggestions}`：

- **总结**：主消耗设备、各设备 CPA/CPC 差异、高消耗低转化设备。
- **建议**：设备出价调整或预算向高转化设备倾斜（写设备名 + 表中数字），1～3 条。

---

## 3. 地域

- **CLI**：`bing-analysis --sections geographic` → `GeographicSectionData`（常见 `countries[]`，**以 outline 为准**）

**数据呈现**：Top 国家/地区（建议 Top 10）消耗、点击、转化、CTR、CPC、CPA。写入 JSON `tables.geographic[]`。

**分析（必写）** → 写入 `narrative.sections.geographic.{analysis,suggestions}`：

- **总结**：地域消耗集中度、高转化 vs 高消耗低转化国家/地区。
- **建议**：地域加价/降价/排除或单独系列（写 `countryOrRegion` + 数据），1～3 条。

---

## 4. 受众

- **CLI**：默认已含 `--sections age-audience,gender-audience`。不要与 `audience-merged` 同时拉（Bing SDK 会抢同一份受众 csv，merged 常 400）。`render --snapshot-dir` 优先 merged，空则回退拆分维。

**数据呈现**：年龄段、性别的展示、点击、消耗、CTR、CPC。拆分维读 `age-audience-*.json` / `gender-audience-*.json` 的 `audience[]`（标签字段 `audience`）。写入 JSON `tables.audienceAge[]`（`ageRange`）/ `tables.audienceGender[]`（`gender`）。

**分析（必写）** → 写入 `narrative.sections.audience.{analysis,suggestions}`：

- **总结**：主力年龄段/性别、转化或 CPA 更优的受众段、无效花费受众。
- **建议**：受众出价\_modifier 或排除（引用 `audience` 字段 + 指标），1～3 条。

---

## 5. 广告结构（系列 / 广告组 / 广告）

| 层级   | CLI                                  | 落盘                         |
| ------ | ------------------------------------ | ---------------------------- |
| 系列   | `bing-analysis --sections campaigns` | `campaigns-*.json`（数组行） |
| 广告组 | `bing-analysis --sections ad-groups` | `ad-groups-*.json`           |
| 广告   | `bing-analysis --sections ads`       | `ads-*.json`                 |

**数据呈现**：各表按消耗降序；系列含 `campaignStatus`；广告组可含质量分相关字段（以 outline 为准）。写入 JSON `tables.campaigns[]` / `tables.adGroups[]` / `tables.ads[]`。RSA 无创意标题时 HTML 仍展示「广告标题」列，内容为「系列 / 广告组」。

**分析（必写，三个子块各写一段，不可合并为一句带过）**：

1. **系列分析 — 总结**：Top 系列及费用占比、暂停/活跃系列效果差异、合计 CTR/CPC/CPA。**建议**：预算增减、暂停或放量具体 `campaignName`，1～3 条。→ 写入 `narrative.sections.campaigns.{analysis,suggestions}`
2. **广告组分析 — 总结**：高消耗广告组、质量分或 CPA 异常组。**建议**：出价、暂停或结构优化（写 `adGroupName` + 数据），1～3 条。→ 写入 `narrative.sections.adGroups.{analysis,suggestions}`
3. **广告分析 — 总结**：Top 消耗创意、CTR/转化表现分化。**建议**：暂停低效广告、复制高效创意方向，1～3 条。→ 写入 `narrative.sections.ads.{analysis,suggestions}`

---

## 6. 关键词与搜索字词

| 类型     | CLI                                     | 说明                                 |
| -------- | --------------------------------------- | ------------------------------------ |
| 关键词   | `bing-analysis --sections keywords`     | 默认 `limit=100`、`orderByCost=true` |
| 搜索字词 | `bing-analysis --sections search-terms` | 同上                                 |

**数据呈现**：Top 关键词/搜索词表（消耗、CTR、CPC、转化、CPA、质量分/匹配类型等，以 outline 为准）。写入 JSON `tables.keywords[]` / `tables.searchTerms[]`。

**分析（必写，两块各写一段）**：

1. **关键词 — 总结**：高转化词、高消耗低转化或零转化词、匹配类型分布。**建议**：暂停/降价/提价/改匹配（写 `keyword` + 数据），1～3 条。→ 写入 `narrative.sections.keywords.{analysis,suggestions}`
2. **搜索字词 — 总结**：高意向词、应加为关键词的词、应否定的无关词（对比触发 `keyword`）。**建议**：加词、否词（写 `searchQuery` + 数据），1～3 条。→ 写入 `narrative.sections.searchTerms.{analysis,suggestions}`

---

## 7. 报告收尾（全账户）

在以上各 section 分析之后，须撰写 **「优化建议汇总」**（3～5 条，写入 JSON `narrative.recommendations[]`），跨 section 归纳优先级，**须与前面各 section 分析一致、不得矛盾**；可呼应对外客户话术（若用户需要）。

---

## 附录

- 鉴权：与 TSO 其他接口相同（`config show` 中 `tsoApiBaseUrl` / Token）。
- 与 steward「优化报告」区别：见 `meta-period-report.md` 末节；此处为**实时分析 JSON**。
- 交付前自检：见 `references/core/agent-conventions.md` §七（币种、区间、章节齐全、数字来自脚本 stdout）。

---

### CLI 速查表

统一入口：`siluzan-tso bing-analysis -a <id> --sections <name> [--start … --end …] --json-out <dir>`

| 数据块   | `--sections` 取值                  |
| -------- | ---------------------------------- |
| 总览     | `overview`                         |
| 设备     | `device`                           |
| 地域     | `geographic`                       |
| 年龄受众 | `age-audience`                     |
| 性别受众 | `gender-audience`                  |
| 受众合并 | `audience-merged`                  |
| 系列     | `campaigns`                        |
| 广告组   | `ad-groups`                        |
| 广告     | `ads`                              |
| 关键词   | `keywords`（默认 `limit=100`）     |
| 搜索字词 | `search-terms`（默认 `limit=100`） |
