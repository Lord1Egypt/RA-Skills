# Google Ads 账户诊断报告

> 账户诊断报告纲要：配合 `google-analysis` CLI 拉数后填充。  
> 占位符：`{reportDate}` `{companyName}` `{period}` 等。  
> 与 `google-account-diagnosis-report.md`（章节与 CLI 对照）配合使用；**撰写与验收以本节「硬约束」为准**。

---

## 撰写硬约束（产品验收 · 必遵）

### 1. 数值格式（含「每日趋势」）

| 类型                             | 规则                                                                                         | 示例                       |
| -------------------------------- | -------------------------------------------------------------------------------------------- | -------------------------- |
| 金额类（消耗、CPA、CPC、预算等） | **保留 2 位小数**，带货币                                                                    | `￥1,234.56 CNY`           |
| 展示、点击、转化次数             | **整数**，不写长小数                                                                         | `1,280` 而非 `1280.000000` |
| 比率（CTR、CVR、环比%）          | JSON 为 0~1 小数时，展示 `(v×100).toFixed(2)+'%'`                                            | `0.0523` → `5.23%`         |
| **每日趋势 / 转化成本曲线**      | 数据源：`daily-metrics` 或 `conversionCost.items`（`date`、`cost`、`cpa`、`conversions` 等） | 见下                       |

**每日趋势表与图（§3.5 转化成本 / 按日趋势）**：

- 表格中：`cost`、`cpa`、`averageCpc` 等金额 → **`Number(v).toFixed(2)`**（或千分位 + 2 位小数）。
- 表格中：`conversions`、`clicks`、`impressions` → **整数**。
- ECharts：Y 轴与 tooltip 对金额类 **最多 2 位小数**；禁止 `12.3456789` 类展示。
- 脚本示例（Node）：`const money = (n) => Number(n).toFixed(2);` `const int = (n) => Math.round(Number(n));`

### 2. 每个模块必须有「分析」（禁止只贴表）

除「页眉」「导航」外，**每一个业务模块**（对应 `section-*` 或下文章节 §02~§12）在数据表/图之后**必须**包含：

1. **分析**（`### 分析` 或 `insight-title analysis-title`）：≥2 条要点，写清**现象 + 依据字段**（如「CPA 由 85.2 升至 112.40，峰值出现在 3/15」），禁止空泛套话。
2. **建议**（`### 建议` / `### 优化建议`）：≥1 条可执行项，与上文分析对应。

| 模块                    | 数据对象                                                             | 分析字段（优先写入报告）                                                           |
| ----------------------- | -------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| §02 诊断概览            | `diagnosisOverview`                                                  | 优势/不足每条已有描述，可补充 1 句总评                                             |
| §03 核心指标            | `metrics`                                                            | `metrics.analysis`、`metrics.suggestions`；**无则 Agent 根据 JSON 撰写，禁止省略** |
| §03.5 系列/地域/词/按日 | `campaigns`、`geographic`、`keywords`、`conversionCost`              | 各对象的 `analysis`、`suggestions`；**按日趋势**另须结合曲线写 2 条趋势分析        |
| §04 黄金账户            | `goldAccount`                                                        | 未达标项归纳 + 修复优先级                                                          |
| §05 预算竞争力          | `budgetCompetitiveness`                                              | 每项 IS/份额与标准对比后的结论                                                     |
| §06 定向策略            | `fullGeographic`、`fullDevice`、`fullAudience`、`fullCustomAudience` | 各维 `analysis`、`suggestions`（无数据则写「本期无数据」+ 原因，**仍须有建议**）   |
| §07 着陆页              | `landingPageAnalysis`                                                | 未达标项与行动优先级                                                               |
| §08 关键词/搜索词       | `fullKeywords`、`fullSearchTerms`、`broadKeywordsCount`              | 各块 `analysis`、`suggestions`                                                     |
| §09 出价策略            | `biddingStrategy`                                                    | 有问题系列逐条说明                                                                 |
| §10 创意                | `adCreativeOptimization`                                             | `analysis`、`suggestions`                                                          |
| §11 新产品              | `newFeatures`                                                        | 未启用功能的建议                                                                   |
| §12 总结                | `summary`                                                            | `keyIssues`、`optimizationRoadmap`                                                 |

> HTML 报告对齐 `GoogleAdsDiagnosisReport.html` 时：有 `*.analysis` / `*.suggestions` 数组的，**必须渲染**「分析」「建议」区块；禁止只渲染表格/图表。

---

## 页眉信息（报告头）

| 字段                  | 占位 / 说明                                |
| --------------------- | ------------------------------------------ |
| 账户名称              | `{companyName}`                            |
| 诊断周期              | `{period}`（如 `2026-03-01 ~ 2026-03-31`） |
| 核心转化行为          | 如「询盘/转化」                            |
| 账户 ID / 货币 / 网址 | 副栏展示用                                 |

**对应数据对象**：`accountInfo`（`companyId`、`companyName`、`currencyCode`、`period`、`conversionAction`、`website`、`businessModel`）

---

## 01 账户基本信息与目标设定

**区块 ID**：`section-account-info`

| 字段（中英）                          | 内容 |
| ------------------------------------- | ---- |
| 账户名称 (Company)                    |      |
| 网址 (Website)                        |      |
| 账户 ID (ID)                          |      |
| 核心业务模式 (Core Business Model)    |      |
| 诊断时间 (Period)                     |      |
| 核心转化行为 (Core Conversion Action) |      |
| 货币单位 (Currency)                   |      |

---

## 02 账户诊断概览

**区块 ID**：`section-diagnosis-overview`  
**数据**：`diagnosisOverview`

### 优势

对每条优势填写 **标题** + **描述**：

1. **{title}** — {description}
2. …

### 不足

1. **{title}** — {description}
2. …

---

## 03 核心业绩指标快照

**区块 ID**：`section-kpi-snapshot`  
**数据**：`metrics`、`structure`、`conversionGoals`、`campaigns`、`geographic`、`keywords`、`conversionCost`（及转化趋势相关块，若有）

### 3.1 数据概览（漏斗）

按顺序呈现（与页面「数据概览」一致）：

| 步骤 | 指标                   | 数值 | 附注       |
| ---- | ---------------------- | ---- | ---------- |
| 1    | 消耗 (Cost)            |      |            |
| 2    | 展示次数 (Impressions) |      |            |
| 3    | 点击次数 (Clicks)      |      | 点击率 CTR |
| 4    | 转化次数 (Conversions) |      | 转化率 CVR |
| 5    | 每次转化费用 (CPA)     |      |            |

### 3.2 账户结构

| 项目                                  | 数量 |
| ------------------------------------- | ---- |
| 有效广告系列 (Effective Ad Campaigns) |      |
| 有效广告组 (Effective Ad Groups)      |      |
| 有效关键字 (Effective Keywords)       |      |
| 有效广告 (Effective Ads)              |      |
| 附加链接 (Sitelinks)                  |      |
| 否定关键字 (Negative Keywords)        |      |
| 有效国家 (Effective Countries)        |      |

**对应字段**：`structure.campaignCount`、`adGroupCount`、`keywordCount`、`adCount`、`extensionCount`、`negativeKeywordCount`、`countriesWithConversionsCount`

### 3.3 指标检测

将下列指标与「行业/健康标准」对照（页面配置：消耗↔`averageCost`，转化↔`averageConversions`，CPA↔`averageCpa`，CTR↔`averageCtr`，CVR↔`averageCvr`）：

| 指标 (Metric) | 数据 (Data) | 行业/健康标准 |
| ------------- | ----------- | ------------- |
| 消耗          |             |               |
| 转化次数      |             |               |
| 每次转化费用  |             |               |
| 点击率        |             |               |
| 转化率        |             |               |

### 分析 / 建议

- **分析**：`metrics.analysis`（列表）
- **建议**：`metrics.suggestions`（列表）

### 3.4 转化目标

| 事件名称 | 状态       | 转化次数 | 转化价值 |
| -------- | ---------- | -------- | -------- |
|          | 启用/停用… |          |          |

**数据**：`conversionGoals.items`（`name` / `eventName`、`status`、`allConversions`、`allConversionsValue`）

### 3.5 重点项分析

每一子块包含：**对比表** + **分析结论** + **优化建议**。

#### 广告系列分析

- 维度列：**广告系列**
- 指标列：花费(上期/本期/环比)、点击(上期/本期/环比)、转化率(上期/本期/环比)
- **数据**：`campaigns.items`（`title`、`previousCost`、`currentCost`、`costRateChange`、`previousClicks`、`currentClicks`、`clicksRateChange`、`previousCvr`、`currentCvr`、`cvrRateChange`）
- **分析 / 建议**：`campaigns.analysis`、`campaigns.suggestions`

#### 国家地区分析

- 维度列：**国家/地区**
- **数据**：`geographic.items`（同上结构）

#### 关键词分析

- 维度列：**关键词**
- **数据**：`keywords.items`

#### 转化成本 / 按日趋势（若页面已渲染）

- **数据**：`conversionCost.items` 或 `daily-metrics` 落盘数组（含 `date`、`cost`、`cpa`、`conversions`、`clicks` 等）。
- **表格**：日期 | 消耗（2 位小数）| 转化（整数）| CPA（2 位小数）— 见上文「每日趋势」格式。
- **图表**：折线/双轴图；tooltip 金额 **2 位小数**。
- **分析（必填）**：至少 2 条，例如「周内 CPA 波动区间」「转化高峰日 vs 消耗高峰日是否一致」。
- **建议（必填）**：至少 1 条（调价/预算/排查追踪等）。

---

## 04 账户健康度与结构分析

**区块 ID**：`section-health-structure`  
**数据**：`goldAccount`

### 黄金账户判定规则（分类说明）

- 账户基础设施、广告创意素材、广告附加信息、出价策略、受众群体功能、搜索关键词、展示广告、YouTube 等分类项数（与页面文案一致即可）

### 黄金账户明细表

| 项目名称           | 是否达标    | 优化建议 |
| ------------------ | ----------- | -------- |
| 转化追踪设置       | 达标/未达标 |          |
| G A与广告账户联结  |             |          |
| 文字广告           |             |          |
| 自适应搜索广告     |             |          |
| 自适应展示广告     |             |          |
| 附加结构化信息摘要 |             |          |
| 附加链接           |             |          |
| 附加宣传信息       |             |          |
| 附加电话信息       |             |          |
| 否定词添加         |             |          |
| 受众群体设置       |             |          |
| 出价策略           |             |          |

**得分**：`goldAccountScore`；**未达标项数**：若有 `goldAccountUnqualifiedCount` 可注明。

---

## 05 投放预算与竞争力分析

**区块 ID**：`section-budget-competitiveness`  
**数据**：`budgetCompetitiveness`（数组）

### 核心系列 IS 目标（公式说明）

- **核心系列 IS 目标** = `impressions ÷ (impressions ÷ searchImpressionShare ÷ 100)`
- 说明：理论可获得展示 = `impressions ÷ (searchImpressionShare ÷ 100)`

### 竞争力表

| 指标 (Metric) | 报告值 (Report Value) | 健康标准 (Health Benchmark) | 优化策略 (Optimization Strategy) |
| ------------- | --------------------- | --------------------------- | -------------------------------- |
|               |                       |                             |                                  |

---

## 06 目标受众与投放策略

**区块 ID**：`section-targeting-strategy`  
**数据**：`fullGeographic`、`fullDevice`、`fullAudience`、`fullCustomAudience`（各含 `items`、`analysis`、`suggestions`）

> 某一维度无 `items` 时，整段在 HTML 中不展示；Markdown 可写「本期无数据」。

对每个有数据的维度，结构相同：

### 6.x {维度标题}

- **地理位置** — `fullGeographic`（列：地理位置、消费、展示、点击、转化、CTR、CVR、CPC、CPA）
- **设备类型** — `fullDevice`（列：设备类型、…）
- **受众特征** — `fullAudience`（列：受众特征、…）
- **自定义受众** — `fullCustomAudience`（列：自定义受众、…）

每维度包含：

- （可选）消费分布图 → Markdown 用「见图/附件」占位
- 数据表
- **分析** / **建议**

---

## 07 着陆页分析

**区块 ID**：`section-landing-page`  
**数据**：`landingPageAnalysis`（经页面加工为下列四行）

| 指标 (Metric)            | 报告值 (Report Value) | 健康标准 (Health Benchmark) | 优先级与行动 (Priority & Action) |
| ------------------------ | --------------------- | --------------------------- | -------------------------------- |
| 达标率 (Compliance Rate) |                       | 100%                        |                                  |
| PC 网站打开速度          |                       | ≤ 3 s                       |                                  |
| 移动网站打开速度         |                       | ≤ 3 s                       |                                  |
| 手机性能指数             |                       | ≥ 75                        |                                  |

---

## 08 关键词与搜索词洞察

**区块 ID**：`section-keyword-insights`  
**数据**：`fullKeywords`、`fullSearchTerms`、`broadKeywordsCount`、`metrics`（用于占比等）

### 8.1 关键词洞察

**表 1（综合）** 列：关键词、点击成本、匹配类型、展示、点击、点击率、转化、转化率、每次转化费用、**花费占比**、**转化占比**

**表 2（转化向，与表 1 列相同）**

- **数据分析** / **优化建议**：`fullKeywords.analysis`、`fullKeywords.suggestions`

### 8.2 广泛匹配关键词洞察

| 统计项             | 数值         |
| ------------------ | ------------ |
| 广泛匹配关键词数量 | `broadTotal` |
| 总关键词数量       | `total`      |
| 广泛匹配占比       | %            |

- **数据分析** / **优化建议**：`broadKeywordsCount.analysis`、`suggestions`

### 8.3 搜索词洞察

列：搜索词、**已添加/已排除**（`queryTargetingStatusZh`）、展示、点击、点击率、转化、转化率、每次转化费用

- **数据分析** / **优化建议**：`fullSearchTerms.analysis`、`fullSearchTerms.suggestions`

---

## 09 预算与出价策略

**区块 ID**：`section-bidding-strategy`  
**数据**：`biddingStrategy.items`（仅「有问题」的系列进入表格；无数据时页面为「出价策略配置良好」）

| 广告系列 | 投放时长 | 当前出价策略 | 推荐出价策略 | 状态 |
| -------- | -------- | ------------ | ------------ | ---- |
|          |          |              |              |      |

---

## 10 广告创意与素材优化

**区块 ID**：`section-ad-creative`  
**数据**：`adCreativeOptimization`

### 搜索广告 — 检测规则

- **Headlines**：推荐大于 2 个，最多 4 个
- **Descriptions**：推荐 8–10 个，最多 15 个；含 1–2 个关键字相关 + 3 个不含关键字的通用标题

### 创意表

| 广告 | Headlines | Descriptions | 优化建议 |
| ---- | --------- | ------------ | -------- |
|      |           |              |          |

- **分析** / **优化建议**：`adCreativeOptimization.analysis`、`suggestions`

---

## 11 新产品应用

**区块 ID**：`section-new-features`  
**数据**：`newFeatures.items`

| 策略/功能 (Strategy/Feature) | 账户状态 (Account Status) | 优化师建议 (Senior Optimizer Recommendation) |
| ---------------------------- | ------------------------- | -------------------------------------------- |
|                              |                           |                                              |

---

## 12 诊断总结

**区块 ID**：`section-summary`（页面标题为「总结」，导航为「诊断总结」）  
**数据**：`summary`

### 12.1 核心问题总结

- `summary.keyIssues`：逐条列出（或写「暂无核心问题」）

### 12.2 优先级优化路线图

| 优先级 | 优化重点 | 关键行动 | 预期效果 |
| ------ | -------- | -------- | -------- |
|        |          |          |          |

**数据**：`summary.optimizationRoadmap`

---

## 附录：与 CLI 拉数对照（可选）

| 报告块                                             | 可参考的 `siluzan-tso google-analysis` 子命令                                           |
| -------------------------------------------------- | --------------------------------------------------------------------------------------- |
| 账户结构 / 转化 / 黄金账户 / 系列类型 / 落地页主域 | `resource-counts`、`conversion-actions`、`gold-account`、`campaign-types`、`final-urls` |
| 概览与维度汇总                                     | `overview`、`dimension-summary`                                                         |
| 重点项对比（系列/地域/词）                         | `campaigns`、`geographic`、`keywords`（本期/上期各拉一次后在文外对比）                  |
| 定向全表                                           | `geographic`、`devices`、`audience`（SystemDefined / UserDefined 各一次）               |
| 搜索词与广告                                       | `search-terms`、`ads`                                                                   |
| 按日 CPA                                           | `daily-metrics`                                                                         |
| 预算竞争力（展示份额等）                           | `dimension-summary` + `campaigns` 等组合计算                                            |

详见 `references/analytics/account-analytics.md`。
