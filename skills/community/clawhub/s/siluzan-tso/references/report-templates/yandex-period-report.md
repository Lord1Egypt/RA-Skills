# Yandex Direct — 账户分析报告（模板纲要）

> **终稿语言**：叙事跟 `meta.lang`（`zh` 或 `en`），表头用该语言。`render` 必须带 `--lang`。
>
> 统计区间：`{startDate}` ~ `{endDate}`（**不能晚于今天**；省略默认近 7 天含今天）  
> 账户：`{mediaCustomerId}`（如 `porg-xxx`，与 `list-accounts -m Yandex` 一致）  
> **默认交付物**：一份可打开的 **HTML 文件**（`yandex-period-report.html`，样式对齐开发样例）。封面按日期写成「季度」或「月度」，对不上仍是「账户分析」。不要打开 HTML 改称呼。  
> 用户**未指定格式**时一律走下方 **标准四步流程**；**禁止** Agent 手写/拼接 HTML。  
> **用户明确要求 Excel / xlsx** 时：拉数步骤不变，改为 Agent 脚本写 `.xlsx`；**不要**调用 `yandex-analysis render`；禁止假设存在内置 excel 子命令。见 `yandex-period-report-excel.md`。

数据块（YandexAPI `/yandex-analysis` 8 维 + 本地周聚合）：总览、按日、Search 网络、系列、关键词、搜索词、地域、设备；周报由 CLI 写入 `daily.weekly`（后端无独立 weekly）。**禁止**自行按 `date` 聚周。

| CLI `--sections` | 落盘形状（CI 实测）                                                   | 报告 `tables.*` / KPI                            |
| ---------------- | --------------------------------------------------------------------- | ------------------------------------------------ |
| `overview`       | 对象：`account` / `currency` / `balance` / `totals` …                 | → `meta` + `kpis`（余额、日均、续航天数）        |
| `daily`          | `{ account, startDate, endDate, items: DayRow[], weekly: WeekRow[] }` | → `tables.daily[]` + `tables.weekly[]`（勿重算） |
| `search`         | `{ …, items: SearchRow[] }`                                           | → `tables.search[]`                              |
| `campaigns`      | `{ …, items: CampaignRow[] }`（默认 limit=100）                       | → `tables.campaigns[]`                           |
| `keywords`       | `{ …, items: KeywordRow[] }`                                          | → `tables.keywords[]`                            |
| `search-terms`   | `{ …, items: SearchTermRow[] }`（**仅近 180 天**）                    | → `tables.searchTerms[]`                         |
| `geo`            | `{ …, items: GeoRow[] }`                                              | → `tables.geo[]`                                 |
| `devices`        | `{ …, items: DeviceRow[] }`                                           | → `tables.devices[]`                             |

> 金额已为账户币种小数；`ctr` / `conversionRate` / `roi` 均为**小数比率**。`roi` = **(购买收益-消耗)/消耗**（如 `-0.5998` 表示亏损约 59.98%），写给用户时必须 ×100 加 `%`，禁止把 `-0.6` 写成 `-0.6%`。无购买收益时常为 `-1`（按缺失）。写叙事前先读各维 `*.outline.txt`。

---

## 标准四步流程（默认 · 交付 HTML）

| 步骤             | 执行者       | 动作                                                                                                                                      |
| ---------------- | ------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 拉数**      | Agent 调 CLI | `yandex-analysis -a <porg-xxx> --start <s> --end <e> --json-out ./snap-yandex`（全 8 维或 `--sections` 指定子集）                         |
| **2. 分析**      | Agent        | 用 **node/python 脚本**读落盘 JSON（勿用 Read 打开业务 `*.json`）。周趋势读 `daily-*.json` 的 `weekly[]`，**禁止**自己按 `date` 聚周。    |
| **3. 写 JSON**   | Agent        | 撰写 `yandex-period-report.json`：仅 `meta.accountId` + `narrative`（8 个分析章节）为必填；`kpis`/`tables` 可省略由 `--snapshot-dir` 合并 |
| **4. 渲染 HTML** | CLI          | `yandex-analysis render` — **校验 narrative 8 个分析章节必含字段**，缺项报错不生成 HTML；**禁止** Agent 手写/拼接 HTML                    |

```bash
# 步骤 1
siluzan-tso yandex-analysis -a <porg-xxx> --start <s> --end <e> --json-out ./snap-yandex

# 步骤 4（步骤 2～3 完成后）
siluzan-tso yandex-analysis render \
  --data ./yandex-period-report.json \
  --snapshot-dir ./snap-yandex \
  --out ./yandex-period-report.html
```

### `yandex-period-report.json` 顶层结构

- `meta`：`accountId`（必填）/ `accountName` / `currency` / `region` / `startDate` / `endDate` / `platform`；可省略由 `--snapshot-dir` 从 overview 补空。
- `kpis`：`spend` / `impressions` / `clicks` / `conversions` / `ctr` / `averageCpc` / `costPerConversion` / `conversionRate` / `roi` / `balance` / `avgDailySpend` / `activeDays` / `runwayDays` / `balanceAsOf`；可省略。
- `tables`（可省略，由 `--snapshot-dir` 映射）：
  - `daily[]`：`{date, spend, impressions, clicks, ctr, averageCpc, conversions, …}`
  - `weekly[]`：`{weekLabel, isoWeek, startDate, endDate, days, spend, …}`（**只读** CLI 已算好的周；`startDate`/`endDate` 为该 ISO 周周一~周日，`days` 为有数据的天数。禁止自填）
  - `search[]`：`{network, spend, …}`
  - `campaigns[]`：`{campaignId, campaignName, status, state, campaignType, budget, strategy, …metrics}`
  - `keywords[]`：`{keyword, campaignName, criteriaType, network, …metrics}`
  - `searchTerms[]`：`{searchQuery, matchedKeyword, campaignName, …metrics}`
  - `geo[]`：`{locationName, targetingLocationName, network, …metrics}`
  - `devices[]`：`{device, network, …metrics}`
- `narrative`（**Agent 必填**）：
  - `sections.{overview,search,campaigns,keywords,searchTerms,geo,devices,daily}`：每个维度各 `{analysis[]（≥1，含数字依据）, suggestions[]（≥1）}`
  - `recommendations[]`：≥3 条跨维度优化建议（可用 `{priority,text,anchor}`，anchor 对齐样例锚点如 `#keyword` / `#query`）
  - `rowInsights`：有关键词表格行时，**HTML 将展示的 Top N 行必须有中文翻译**；`render` 缺项会拒绝出 HTML。见下方「逐行洞察」。Campaign / 关键词 / 搜索词 / 地域 / 设备列表**不展示**「问题」「建议」列，行级判断写入各维 `sections.*.analysis/suggestions` 即可。

#### 逐行洞察 `narrative.rowInsights`

表格主观列目前只有关键词「中文翻译」，不是原始接口字段，由 Agent 基于已拉取原文翻译：

- **必填（`render` 校验）**：`tables.keywords` 有行时，须为 HTML 将展示的每一行（按消耗降序，最多 40 行）提供匹配的 `rowInsights`，且有非空 `translation`。缺一项即拒绝生成 HTML。
- Campaign「学习期」、搜索词「分类」、各维行级「问题/建议」均不展示。

示例：

```jsonc
"narrative": {
  "rowInsights": {
    // 按 keyword 原文匹配（如同词跨系列，可加 campaignName 消歧）
    "keywords": [
      { "match": { "keyword": "металлопрокатное оборудование" }, "translation": "金属轧制设备" }
    ]
  }
}
```

- `translation` 是 Agent **对已知原文的翻译**，允许生成；不得编造原始接口没有、也无法由现有指标算出的硬事实。
- 每条洞察按原文匹配一行；HTML 将展示的关键词行若缺中文翻译，`render` 会拒绝出 HTML。

### 快照合并范围（`--snapshot-dir`）

`render` 传 `--snapshot-dir` 时，CLI 自动补全：

1. `meta`（仅补空字段）
2. **`kpis` / `tables.*` 一律以 CLI 快照覆盖**（有对应 section 时）
3. `tables.weekly` 由 CLI 从 `daily.items` 按 ISO 周重算并覆盖（与落盘 `daily.weekly` 同一套函数）

Agent 只需撰写 `narrative`；**禁止手写 HTML**，也**禁止**自填 `kpis`/`tables` 数值，**禁止**自行聚周。

### 周趋势（禁止再出现 NaN）

网关 `daily.items[].date` 可能是 ISO 时间戳（`2026-07-01T00:00:00+00:00`）。CLI 落盘时已截成 `YYYY-MM-DD`，并写好 `weekly[]`。

- 写「周趋势」叙事时：**脚本读 `weekly[]`**（`weekLabel` / `startDate` / `endDate` / `spend` / `conversions` / `days`）。
- **禁止** `new Date(date + 'T00:00:00Z')`：日期已是完整时间戳时再拼接会变成 Invalid Date，年份/月份变成 `NaN`，报告出现 `NaN-NaN-NaN`。
- **禁止**自己算 ISO 周、自己拆周。周末无投放时 `days` 会小于 7，属正常。

---

## 日期规则（必读）

- `--start` / `--end` 须**同传或同省略**；**不能晚于今天**；省略=近 7 天（含今天）。
- **search-terms** 仅支持近 **180 天**；超窗网关/CLI 拒绝——拉长区间时对该维用 `--exclude search-terms` 或缩短区间。
- 用户说「X 月 / 月报」且该月已结束：`--start` 当月 1 日、`--end` 当月最后一天。

---

## 拉数（一次目录）

```bash
mkdir -p ./snap-yandex

siluzan-tso list-accounts -m Yandex -k <porg-xxx> --json-out ./snap-yandex

siluzan-tso yandex-analysis -a <porg-xxx> --start <S> --end <E> --json-out ./snap-yandex
```

- 写脚本前先读各 `yandex-*-<id>.outline.txt`（或 stdout 摘要里的 outline），再脚本读 `.json`。
- `search` / `campaigns` / `keywords` / `geo` / `devices` 在 Direct 侧过滤 `AdNetworkType=SEARCH`。
- 周趋势读 `daily-*.json` 的 `weekly[]`，禁止自行聚周、禁止给 `date` 再拼 `T00:00:00Z`。
- Campaign「学习期」、搜索词「分类」、各维行级「问题/建议」均不展示。关键词中文翻译可由 Agent 通过 `narrative.rowInsights` 提供（见上方「逐行洞察」）。

---

## HTML 章节与锚点（对齐开发样例）

| 锚点        | 章节         | 数据 / 叙事来源                                           |
| ----------- | ------------ | --------------------------------------------------------- |
| `#overview` | 账户总览     | `kpis` + `tables.weekly` + 每日折叠 + `sections.overview` |
| `#next`     | 后续优化动作 | `narrative.recommendations`                               |
| `#search`   | Search 网络  | `tables.search` + `sections.search`                       |
| `#campaign` | Campaign     | `tables.campaigns` + `sections.campaigns`                 |
| `#keyword`  | 关键词       | `tables.keywords` + `sections.keywords`                   |
| `#query`    | 搜索词       | `tables.searchTerms` + `sections.searchTerms`             |
| `#geo`      | 地域         | `tables.geo` + `sections.geo`                             |
| `#device`   | 设备         | `tables.devices` + `sections.devices`                     |
| `#daily`    | 日报表       | `tables.daily` + `sections.daily`                         |
| `#weekly`   | 周报表       | `tables.weekly`（同 daily 叙事）                          |

---

## 相关文档

- `yandex-period-report-excel.md` — 用户要 xlsx 时
- `references/analytics/account-analytics.md` — `yandex-analysis` 命令与日期
- `references/core/agent-conventions.md` — 落盘读盘与交付自检
