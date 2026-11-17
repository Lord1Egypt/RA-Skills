# Google 账户分析报告

> 统计区间：`{startDate}` ~ `{endDate}`  
> 账户：`{mediaCustomerId}`

> **终稿语言**：叙事跟 `meta.lang`（`zh` 或 `en`），表头用该语言。`render` 必须带 `--lang`。
>
> **默认交付物**：一份可打开的、带 ECharts 图表的 **HTML 文件**（`google-period-report.html`）。  
> 用户**未指定格式**时一律走下方 **标准四步流程**；**禁止** Agent 手写/拼接 HTML（语法错误会导致报告无法显示）。  
> **用户明确要求 Excel / xlsx**（且非 OKKI / 询盘话术）时：在拉数步骤不变的前提下，**另 Read 全文** `report-templates/google-period-report-excel.md`，并**先读齐**各维度 `*.outline.txt` 再写脚本；禁止加载宿主第三方 xlsx Skill；**不要**调用 `google-analysis render`。

---

## 标准四步流程（默认 · 交付 HTML）

| 步骤             | 执行者       | 动作                                                                                                                                                                                                               |
| ---------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. 拉数**      | Agent 调 CLI | `google-analysis -a <id> --start <s> --end <e> --json-out ./snap-google --sections <见下方默认维度对应 CLI>`                                                                                                       |
| **2. 分析**      | Agent        | 用 **node/python 脚本**读落盘 JSON（勿用 Read 打开业务 `*.json`），完成筛选、聚合、排序与洞察                                                                                                                      |
| **3. 写 JSON**   | Agent        | 按 `assets/google-period-report.schema.json` 撰写 `google-period-report.json`：只写 `meta` + `narrative`（9 个数据维 + 优化建议）；`kpis`/`charts`/`tables` 留给步骤 4 的 `--snapshot-dir` 合并（合并后缺 KPI 或缺否词表会拒绝出 HTML） |
| **4. 渲染 HTML** | CLI          | `google-analysis render` — **校验 narrative 10 章必含字段**（含受众、否词），缺项报错不生成 HTML；**禁止** Agent 手写/拼接 HTML                                                                                                   |

```bash
# 步骤 1
siluzan-tso google-analysis -a <id> --start <s> --end <e> --json-out ./snap-google \
  --sections overview,daily-metrics,dimension-summary,campaigns,devices,geographic,audience,keywords,negative-keywords

# 步骤 4（步骤 2～3 完成后）
siluzan-tso google-analysis render \
  --data ./google-period-report.json \
  --snapshot-dir ./snap-google \
  --out ./google-period-report.html \
  --lang <zh|en>
```

`google-period-report.json` 顶层结构：

- `meta`：`accountId`（必填）/ `accountName` / `currency` / `startDate` / `endDate`；可省略由 `--snapshot-dir` 从 `overview` + manifest 自动合并。
- `kpis`：账户级 KPI（消耗/展示/点击/转化/CTR/CPC/CPA，含可选 `previousPeriod` 环比；另含 `activeDays` / `averageDailyCost`）；Agent 可省略，但 **render 合并后** `cost`/`impressions`/`clicks` 至少一项须为有效数字，否则拒绝出 HTML（避免执行摘要卡片全「—」）。本期 KPI 由 CLI 优先对 `campaigns` 全系列累加并重算比率；无 campaigns 时回退 `overview.currentPeriod`，再回退 `dimension-summary`。`activeDays` / `averageDailyCost` 来自 `overview.record` 根（**不是** `currentPeriod`）；环比仍来自 `overview.previousPeriod`（上期无活跃天数，不编造）。
- `charts.dailyTrend`：每日趋势（`dates`/`cost`/`conversions`/`cpa`）；可省略由 `daily-metrics` 自动合并。
- `tables.{dimensionSummary,campaigns,devices,geographic,audience,keywords,negativeKeywords}`：对应 §3～§9 表格数据；可省略由同名 `google-analysis` section 自动合并。`negativeKeywords` 合并后必须是数组，**0 条也是 `[]`**。
- `narrative`（**Agent 必填，唯一由 Agent 撰写的内容**）：
  - `executiveSummary[]`：≥1 段执行摘要
  - `sections.{overview,dailyTrend,dimensionSummary,campaigns,devices,geographic,audience,keywords,negativeKeywords}`：每个维度各 `{analysis[]（≥2 条）, suggestions[]（≥1 条）}`，对应报告 §1～§9
  - `recommendations[]`：≥3 条跨维度优化建议，对应报告 §9

完整字段定义见 `assets/google-period-report.schema.json`。

**Excel 分支**（用户明确要 xlsx 时）：

1. 步骤 1～2 与 HTML 流程相同（拉数 → 分析）。
2. 改为 Agent 执行 node/python 脚本按 `google-period-report-excel.md` 写出 `.xlsx`（先读齐 `*.outline.txt`）。核心指标的上期转化价值 / 单转化价值 / ROAS 按该文「转化价值环比」再拉等长上期 `campaigns` 后汇总。
3. **不要**调用 `google-analysis render`（除非用户同时要 HTML + Excel）。
4. **禁止**假设存在 `siluzan-tso … excel` 子命令。

模板源码：`report-templates/google-period-report.html`（结构与样式，ECharts 渲染逻辑已内联）。

`render` 会向输出目录写入 HTML，并注入 `window.__GOOGLE_PERIOD_REPORT__`。封面按 `meta.startDate/endDate` 写成「季度分析」或「月度分析」；不是完整自然季、也不是从 1 号起的同一个月时，仍写「周期分析」。不要打开 HTML 改这几个字。  
传 `--snapshot-dir` 时 CLI 自动从快照合并 KPI、每日趋势图表、周期汇总/系列/设备/地域/受众/关键词表格：**数值一律以 CLI 快照覆盖**（`meta` 仅补空）。本期 KPI 优先 `campaigns` 累加。若 manifest 缺条目但磁盘上仍有对应 `*.json`，CLI 会按文件名自愈补齐。Agent 只写 `narrative`，勿自填 `kpis`/`tables`。

---

## 默认报告维度

生成报告时，**默认包含**以下 10 章（9 个拉数维 + 优化建议）：

| #   | 维度                                                                         | CLI                                                                                           |
| --- | ---------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 1   | 执行摘要（消耗/展示/点击/转化/CTR/CPC/CPA 本期概览）                         | `google-analysis --sections overview`                                                         |
| 2   | 每日投放趋势（按日消耗/点击/转化曲线；金额/CPA **2 位小数**，转化/点击整数） | `google-analysis --sections daily-metrics`                                                    |
| 3   | 月度汇总（全周期汇总数据）                                                   | `google-analysis --sections dimension-summary`                                                |
| 4   | 广告系列表现（预算/出价策略/各系列消耗与效果）                               | `google-analysis --sections campaigns`                                                        |
| 5   | 设备分布（PC/移动/平板 消耗/点击/转化）                                      | `google-analysis --sections devices`                                                          |
| 6   | 地域分布（国家/地区 消耗占比）                                               | `google-analysis --sections geographic`                                                       |
| 7   | 受众分布（意向/兴趣/再营销/客户匹配等列表表现）                              | `google-analysis --sections audience`（默认不传 `--audience-type`，系统+自定义一起拉）       |
| 8   | 关键词表现（词/消耗/CTR/CPC 排行）                                           | `google-analysis --sections keywords`（这个命令获取的关键词数据会来自多个系列，不能合并去重） |
| 9   | 否词（当前账户已有否定关键词：词面 / 匹配 / 级别 / 系列 id / 广告组 id）           | `google-analysis --sections negative-keywords`（精简列表；0 条也要落盘；不按本周期消耗过滤）       |
| 10  | 优化建议（根据以上数据给出可执行改进建议）                                   | 不额外拉数，基于已有数据撰写                                                                  |

**在执行任何数据拉取之前**，先向用户展示以下可选维度，询问是否需要追加：

---

## 平台支持的全部可选维度

| 维度          | CLI                                             | 备注                                                              |
| ------------- | ----------------------------------------------- | ----------------------------------------------------------------- |
| 系列按小时    | `google-analysis --sections campaign-hour`      | 行在 `items[]`，含 `date`/`hour`/消耗与效果                       |
| 搜索词报告    | `google-analysis --sections search-terms`       | 高消耗搜索词；`queryTargetingStatusZh` 列（已添加/已排除/都没有） |
| 广告创意表现  | `google-analysis --sections ads`                | 广告标题/类型/到达网址                                            |
| 附加信息      | `google-analysis --sections extensions`         | 附加链接/电话/宣传信息等状态                                      |
| 图片/视频素材 | `google-analysis --sections materials`          | 图片 + 视频合并视图                                               |
| 账户落地页    | `google-analysis --sections final-urls`         | 主投放域名/落地页（不传日期）                                     |
| 黄金账户评分  | `google-analysis --sections gold-account`       | 健康度评分与各项达标状态                                          |
| 广告质量指标  | `google-analysis --sections ads-index`          | 质量得分汇总                                                      |
| 转化动作配置  | `google-analysis --sections conversion-actions` | 已配置的转化目标列表                                              |
| 账户结构统计  | `google-analysis --sections resource-counts`    | 系列/组/广告/词数量                                               |
| 广告系列类型  | `google-analysis --sections campaign-types`     | 系列类型分布（不传日期）                                          |

---

## 拉数顺序（默认 9 个维度）

**首选：用 `google-analysis --sections` 一次拉齐**（单进程复用 keep-alive，比逐个 spawn 快 3-7×；详见 `references/analytics/account-analytics.md` 的 `all` 子命令说明）：

```bash
mkdir -p ./snap-google
siluzan-tso google-analysis -a <id> --start <s> --end <e> --json-out ./snap-google \
  --sections overview,daily-metrics,dimension-summary,campaigns,devices,geographic,audience,keywords,negative-keywords
```

如果用户**追加**了维度（按上文「可选追加」表），把它们加入 `--sections` 即可；要全部维度则省略 `--sections`。

> 仅在调试单个维度或需要传 `all` 暂未透传的特殊参数时，才回落到逐条 `siluzan-tso google-analysis <子命令> -a <id> …` 调用。

---

## 广告系列状态列（必读）

`campaigns-*.json` → `items[]` 每行含 CLI 注入的 **`campaignStatusDisplay`**（`投放中` / `已暂停` / `已移除`）。

| 正确                                                                              | 错误                                                                                      |
| --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 直接展示 `row.campaignStatusDisplay`                                              | 读 `campaignStatus` 后自行 `MAP[s] \|\| '已移除'`（`Enabled` 未命中键时会全变「已移除」） |
| 需要英文枚举时读 `campaignStatus` 或 `campaignStatusV2`，展示前 `.upper()` 再映射 | 用 `stats` / `list-accounts` 的账户 `status` 充当系列状态                                 |

原始枚举为 PascalCase（`Enabled`），与 `ad campaigns` 的 `statusDisplay`（如 `Enabled·有效` / `Enabled·投放期已结束`）口径不同；周期报告「状态」列统一用 **`campaignStatusDisplay`**。

---

## 受众分析（必写）

`audience-*.json` → `items[]`。标签字段优先 `audienceName`，否则 `audience`。这是广告组受众列表表现（In-market / Affinity / 再营销 / Customer Match 等），**不是** Meta/Bing 那种年龄×性别交叉。

- **呈现**：`tables.audience[]`（`audience` / `audienceType` / `campaignName` / 消耗/点击/转化/CPA）。默认不传 `--audience-type`；用户只要系统或自定义列表时再加 `SystemDefined` / `UserDefined`。
- **分析** → `narrative.sections.audience.{analysis,suggestions}`（≥2 / ≥1）：
  - 写清高消耗、高转化、空耗（高花费低转化或零转化）的受众名称 + 数字。
  - 区分系统意向/兴趣 vs 再营销/客户匹配；空耗列表建议缩小或排除，高效列表建议观察后再加码。
  - 无行时写「本期间无受众行 / 未挂受众列表」，**禁止**编造年龄段或兴趣饼。
  - 未确认前不要写自动改出价/排除命令。

---

## 否词（必写）

`negative-keywords-*.json` → `items[]`，合并后是 `tables.negativeKeywords[]`。这是**当前账户已经存在的否定关键词**（系列 / 广告组 / 账户三级），来自精简列表，不是本周期的消耗或搜索词。

- **呈现**：词面、匹配方式、级别（`levelZh`：账户 / 系列 / 广告组）、`campaignId`、`adGroupId`。精简列表没有系列名和广告组名。账户级没有 `campaignId`，只有广告组级才有 `adGroupId`。旧快照若还有 `campaignName` / `adGroupName` 可以照用。0 条时表格写「当前账户否词 0 条」。
- **分析** → `narrative.sections.negativeKeywords.{analysis,suggestions}`（≥2 / ≥1）：
  - 先写总条数，再按级别拆开。有词就点名几条；0 条就写「当前否词 0 条」。
  - 其他章节如果建议加否词、出否词清单，必须引用这张表的条数。禁止在没拉到名单时写「账户没有否词」或只在建议里提否词。
  - 这张表不说明该否哪些搜索词。要谈浪费搜索词，须另拉 `search-terms`，并对照本表里已有的否词。
  - 未确认前不要执行 `ad keyword-negative-create`。
