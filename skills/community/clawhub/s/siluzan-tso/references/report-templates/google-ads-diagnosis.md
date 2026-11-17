# Go

> **终稿语言**：叙事跟 `meta.lang`（`zh` 或 `en`），表头用该语言。`render` 必须带 `--lang`。

## Contents

- CLI 工作流（collect → Agent → render）
- 撰写硬约束（产品验收 · 必遵）
- 页眉信息（报告头）
- 01 账户基本信息与目标设定
- 02 账户诊断概览
- 03 核心业绩指标快照
- 04 账户健康度与结构分析
- 05 投放预算与竞争力分析
- 06 目标受众与投放策略
- 07 着陆页分析
- 08 关键词与搜索词洞察
- 09 预算与出价策略
- 10 广告创意与素材优化
- 11 新产品应用
- 12 诊断总结
- 附录：与 CLI 拉数对照（可选）

---

ogle Ads 账户诊断报告

> 账户诊断报告纲要：配合 `google-analysis` CLI 拉数后填充。  
> **HTML 终稿**：Agent 聚合 JSON → `siluzan-tso google-ads-diagnosis render` 注入 **`GoogleAdsDiagnosisReport.html`**（与 MarkAI `useAnalysisAction/adsDiagnosis` 同源模板，保证样式一致）。  
> 占位符：`{reportDate}` `{companyName}` `{period}` 等。  
> 与 `google-account-diagnosis-report.md`（章节与 CLI 对照）配合使用；**撰写与验收以本节「硬约束」为准**。

---

## CLI 工作流（collect → Agent → render）

```bash
# 1) CLI：仅拉数 + 事实聚合（不含 analysis/suggestions）
siluzan-tso google-ads-diagnosis collect \
  -a <mediaCustomerId> --start <YYYY-MM-DD> --end <YYYY-MM-DD> \
  --json-out ./snap-p1

# 产出三个文件：
#   - google-ads-diagnosis-collect.json   事实数据（reportData + agentBrief）
#   - google-ads-diagnosis.json           **终稿骨架**：事实行已填好，叙事字段留空
#   - google-ads-diagnosis-digest.md      各 section 结构、行数、待填字段清单

# 2) Agent：先读 digest（一次就够），再直接在**骨架**上填空：
#    ./snap-p1/google-ads-diagnosis.json

# 3) CLI：注入 HTML 终稿
siluzan-tso google-ads-diagnosis render \
  --data ./snap-p1/google-ads-diagnosis.json \
  --out ./snap-p1/google-ads-diagnosis-report.html
```

| 子命令    | 说明                                                                                                                       |
| --------- | -------------------------------------------------------------------------------------------------------------------------- |
| `collect` | 拉 google-analysis + 对比周期 + 着陆页（TSO Lighthouse，失败自动重试）；输出 collect / 终稿骨架 / digest 三个文件 |
| `render`  | 读取 Agent 填好的 `google-ads-diagnosis.json`，注入 `GoogleAdsDiagnosisReport.html`                                        |

**读盘纪律（影响出片耗时，必须遵守）**：

- 摸结构**只读** `google-ads-diagnosis-digest.md`；看具体数字**只读** `google-ads-diagnosis.json` 骨架。
- **禁止**用 `node -e` / 临时脚本逐段 dump `google-ads-diagnosis-collect.json`。历史上这种做法会产生 20+ 轮 bash、把上下文顶到十几万 token，单次报告因此多花几十分钟。
- **禁止**从零新建 `google-ads-diagnosis.json`：collect 已生成骨架，直接在上面填空。重跑 collect 不会覆盖你已写的内容（检测到叙事字段非空会跳过并告警）。

**collect 选项**：

| 选项                         | 说明                                                                |
| ---------------------------- | ------------------------------------------------------------------- |
| `--no-fetch-previous-period` | 不拉上一周期 campaigns/geographic/keywords 对比数据（环比列将为空） |
| `--skip-landing-page`        | 不拉取着陆页（跳过 TSO Lighthouse）                                 |

**collect 耗时**：实测约 40~55 秒（单账户、未缓存区间）。拉数进度会实时打到 stderr，不要因为「看起来没输出」就中断重跑。超过 15 分钟 CLI 会自行终止并提示重试或用 `--sections` 缩小范围。

**collect 行为约束**：

- **禁止**使用已移除的 `--skip-fetch`；环比对比数据须由 CLI 向 API 拉取上一周期快照（`campaigns/geographic/keywords` 的 `*_YYYYMMDD-YYYYMMDD.json`），不可仅靠目录内当期快照映射。
- `google-analysis` **部分维度失败**（exit 2，如 `daily-metrics` HTTP 400）时，collect **仍会继续**拉取对比周期并生成 `google-ads-diagnosis-collect.json`；Agent 可基于 collect 继续撰写，缺失维度在报告中注明。
- 若环比列全为 `null`，检查落盘目录是否存在上一周期文件（如 `campaigns-<id>_20260503-20260602.json`）；不存在则**重新执行 collect**（勿用手动拼装或 Python 脚本绕过 CLI）。

- **render 自动合并（默认开启）**：若同目录存在 `google-ads-diagnosis-collect.json`，且 Agent 改坏了 `campaigns` / `geographic` / `keywords` 的 `items`（缺 `title`/`currentCost` 或环比写成字符串）或整体覆盖丢弃了 `landingPageAnalysis.desktop`/`mobile`，CLI **自动从 collect.reportData 恢复**，保留 Agent 的 `analysis`/`suggestions`。可用 `--no-merge-collect` 关闭；`--collect <file>` 指定 collect 路径。
- **render 硬校验**：合并后对比表仍不完整则 **exit 1**（避免 HTML 表体全空）；`campaigns/geographic/keywords.items` 默认同目录 collect **整表覆盖** Agent 改动（Agent 只填 analysis/suggestions）；`summary.keyIssues` / `diagnosisOverview.disadvantages` 与事实字段矛盾，或出现「否词相关 / 着陆页测速缺失」禁写项、预算/创意建议千篇一律、§07 写成关键词洞察时同样 **exit 1**。

- **禁止**在 `collect` 阶段生成或写入 `analysis` / `suggestions` / `diagnosisOverview` / `summary` 等建议性文案。collect 写出的终稿骨架里这些字段一律为空占位，须由 Agent 填写。
- **禁止**跳过 Agent 直接 `render` collect 产物（`render` 会校验全部叙事 / 建议字段；调试可加 `--lenient`）。
- JSON 顶层结构须与 MarkAI `sectionData.js` / `fetchData` 输出一致（见下文各 `section-*` 数据对象）。
- `render` 默认校验（缺任一项则失败，除非 `--lenient`）：
  - 各模块 `*.analysis` 与 `*.suggestions`（含 `metrics`、`campaigns`、`geographic`、`keywords`、`conversionCost`、`fullGeographic`、`fullDevice`、`fullAudience`、`fullCustomAudience`、`fullKeywords`、`fullSearchTerms`、`broadKeywordsCount`、`biddingStrategy`、`adCreativeOptimization`、`newFeatures`、`landingPageAnalysis`——模块存在于 JSON 时均须非空）
  - `diagnosisOverview.advantages` / `disadvantages`（每条须有非空 `title` 与 `description`；纯字符串 render 会按第一个「：」拆开后再注入。拆完仍缺字段则 **exit 1**，避免 HTML 显示「未填写」）、`summary.keyIssues` / `optimizationRoadmap`
  - `accountInfo.businessModel` / `industry`
- 下列单元格由 `render` 按行数据写入，Agent 不要填，写了也会被覆盖：黄金账户达标与建议、`budgetCompetitiveness[].strategy`、`biddingStrategy.items[].recommendationReason`、`newFeatures.items[].optimizerRecommendation`、`adCreativeOptimization.items[].suggestion`
- **禁止**跳过 `render` 直接在对话里贴 HTML/Markdown 当终稿。

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

### 3. 结构类「0 值」结论——禁止仅凭本期数据判定「策略缺失」

- `structure.keywordCount`（或 `campaignCount`/`adGroupCount` 等）为 0 时，**禁止**直接写「关键词策略完全缺失」「从未做关键词投放」等绝对化结论。
- 该字段口径是「本期活跃（未暂停）系列的结构统计」：`resource-counts` 接口即使传全历史区间，也只统计当前未暂停系列，**历史 `Paused` 系列的关键词/广告组不计入**；`keywords` 报表同样只返回本期有消耗（`spend > 0`）的行。
- 遇到 0 值时须额外核实：拉一次覆盖更长历史的 `campaigns`，检查 `items[].channelTypeV2`（如 `SEARCH`）与 `campaignStatus`（如 `Paused`）——若存在历史上投放过、现已暂停的系列，须改写为「关键词策略已被搁置/账户过度依赖 PMax 等其他系列类型」，并点出具体历史系列名称、花费与转化数据，**禁止**笼统写成「策略缺失」。

### 4. 黄金账户（`goldAccount`）结论——逐字段核对，禁止凭印象编造

- 达标 / 未达标**以接口布尔值为准**。广告、附加信息、受众在明细里是否存在，不改变这些布尔值。`render` 不会把 `false` 改成 `true`。
- 表上的建议不是 Agent 写的。未达标默认是「未达到该项黄金账户标准」，不再写「请创建 / 请关联 / 请添加」。
- 同目录快照里已经看得到相关对象、且该项仍是 `false` 时，`render` 只改这一行建议，写明对象已在，**仍然保持未达标**。
- `true` = 已达标，**不可写反**。常见误写：`conversionTrackingQualified: true` 却写「转化跟踪不完整」。
- 明细里已经有对象时，**禁止**在 `summary.keyIssues` / `diagnosisOverview` 写成「请创建文字广告」「没有文字广告」「请关联 GA」「请添加宣传信息 / 结构化信息摘要」「请设置受众」「请使用自适应展示广告」。未达标可以写，但要写标准未达到，不能写成账户里没有。`render` 命中直接 `exit 1`。
- 字段整段缺失时写「该项数据未拉取到」，**禁止**默认当成未达标。

### 5. 写 `summary.keyIssues` / `diagnosisOverview.disadvantages` 前必须逐条自查一致性

- 这两处是**全篇结论的浓缩**，最容易脱离原始事实字段、直接照抄模板套话。写每一条前，必须回头核对同一份 JSON 里已经算好的硬字段，**禁止只看局部模块就下结论**：
  - 结论涉及「关键词/搜索策略缺失」→ 核对 `newFeatures.items[]` 里 `strategy === "KwMatch"` 那一行的 `accountStatus`（`true` 表示账户历史上有过 Search/关键词投放，须按第 3 条改写为「已被搁置」而非「缺失/从未」）。
  - 结论涉及「转化跟踪/GA 关联」→ 以 `gaConfigured` / `conversionTrackingQualified` 为准，不要用「有没有 GA4 转化」代替达标。有启用的 GA4 转化时，禁止写成「未关联 / 请关联」，可写该项未达标。
  - 结论涉及「着陆页测速/性能」→ 先看 `landingPageAnalysis.source`：`api` 才可用 desktop/mobile 的 score/FCP；`none` 写「数据未获取」，**禁止**编造性能指数。
- **禁止写入 keyIssues / disadvantages（render 硬拦截）**：
  - 「否定关键词数量为 0 / 缺少否词过滤」——本报告 **collect 未拉取否词数据**，结构表与黄金账户**不展示否词项**；禁止据此下结论。有搜索词浪费时仅在 §08 按具体搜索词写。
  - 「着陆页性能数据缺失 / 无法评估加载速度」——测速未获取是 Lighthouse API 失败，**不是**投放核心问题；只在 §07 `analysis` 说明即可。
- `render` 会对已知矛盾与上述禁写模式做**硬校验**，命中直接 `exit 1`——须按提示改写，**禁止**删字段绕过。

### 6. `landingPageAnalysis.desktop` / `mobile` 禁止被整体覆盖丢弃

- `collect` 产出的 `landingPageAnalysis` 结构固定为 `{ desktop: {score, firstContentfulPaint, firstMeaningfulPaint, speedIndex}, mobile: {...}, source? }`；Agent 撰写终稿时**只能在这个对象上追加** `analysis`/`suggestions`，**禁止**把整个 `landingPageAnalysis` 替换成仅剩 `{analysis, suggestions}`（否则会丢掉全部 Lighthouse 测速数字）。
- `render` 会在同目录存在 `google-ads-diagnosis-collect.json` 时自动从 collect 恢复缺失/损坏的 `desktop`/`mobile`（保留 Agent 写的 `analysis`/`suggestions`），但**不能依赖这个兜底**——终稿应本就保留完整字段。
- 若 `source` 为 `none`，或 `desktop`/`mobile` 全 0（未测到），`analysis` 须说明数据未获取；**禁止**编造评分，**禁止**把「数据缺失」写进 `keyIssues`。
- **`analysis` / `suggestions` 只能谈着陆页**（测速、HTTPS、表单、追踪、加载体验）。**禁止**在 §07 写关键词花费/CPA/匹配类型等（那些属于 §08）；render 会拦截「只谈关键词、不谈着陆页」的 analysis。

### 6b. 数据列文案由 render 写入

- `budgetCompetitiveness[].strategy`、`adCreativeOptimization.items[].suggestion`、`biddingStrategy.items[].recommendationReason`、`newFeatures.items[].optimizerRecommendation` 都按该行数值生成。Agent 写了也会被覆盖。
- 生成结果若整列变成同一句，render 仍会拦截。每行会带上指标名、广告标题或条数，避免套话。

### 7. 环比对比表 `campaigns/geographic/keywords.items` — Agent 禁止写入

- `collect` 已根据当期 + 上一周期快照生成对比行（`title`、`currentCost`/`previousCost`、`costRateChange`、`currentClicks`/`previousClicks`、`clicksRateChange`、`currentCvr`/`previousCvr`、`cvrRateChange`）。Agent 撰写终稿时**只填** `analysis` / `suggestions`，**禁止**写入、清空、删减或「手工重写」`items` 数组
- `agentBrief.comparisonTableItemCounts` 给出 collect 侧行数（如 `keywords: 15`）；终稿 `keywords.items.length` 须与之一致。若 Agent 误改，`render` 会**始终以**同目录 `google-ads-diagnosis-collect.json` **覆盖**上述三个模块的 `items`（保留 Agent 的 narrative）。
- 分析文案须引用对比表中的具体词/系列/国家名与环比数字（如「fitness mat 消耗 $230.60，环比下降 39.6%」），**禁止**在 `items` 有数据时写「关键词对比表为空」类结论。
- `biddingStrategy.items` / `newFeatures.items` 的事实列由 collect 生成。`recommendationReason` / `optimizerRecommendation` 由 render 按行数据重写。Agent 勿篡改 `duration`（须为天数 number）、`biddingStrategyType`、`strategyName`、`accountStatus`。

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

### 优势 / 不足

每条是对象，HTML 只读 `title` 与 `description`：

```json
{
  "title": "转化效率环比明显改善",
  "description": "CPA 由 ￥116.65 降至 ￥75.73（-35.07%）"
}
```

禁止把整句写成字符串。`render` 若收到「标题：说明」，会按第一个「：」拆成上面的对象再注入。

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
| 有效国家 (Effective Countries)        |      |

**对应字段**：`structure.campaignCount`、`adGroupCount`、`keywordCount`、`adCount`、`extensionCount`、`countriesWithConversionsCount`（**不含**否词计数；collect 未拉否词）

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
- **Agent 禁止写入 `items` 行**（只填 `analysis`/`suggestions`）；`render` 会以 collect 为准**自动覆盖** Agent 改动的对比表 items

#### 国家地区分析

- 维度列：**国家/地区**
- **数据**：`geographic.items`（同上结构）
- **Agent 禁止写入 `items` 行**；`render` 自动从 collect 恢复

#### 关键词分析

- 维度列：**关键词**
- **数据**：`keywords.items`（字段同上；行数见 `agentBrief.comparisonTableItemCounts.keywords`）
- **Agent 禁止写入/清空 `items`**；分析须引用表中具体词名与环比，勿写「对比表为空」

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
| 自适应搜索广告     |             |          |
| 自适应展示广告     |             |          |
| 附加结构化信息摘要 |             |          |
| 附加链接           |             |          |
| 附加宣传信息       |             |          |
| 附加电话信息       |             |          |
| 受众群体设置       |             |          |
| 出价策略           |             |          |

> 黄金账户表**不含**「文字广告」（`expandedTextAdQualified`，加大型文字广告已停用）。搜索创意只看「自适应搜索广告」（`responsiveSearchAdQualified`）。
>
> 黄金账户表**不含**「否定词添加」（`adsNegativeQualified`）：collect 未拉取否词数据，render 会剥离该字段。
>
> 达标 / 未达标只看接口布尔值。明细里有 `RESPONSIVE_SEARCH_AD`、宣传信息、GA4 转化或受众，**不**把对应行改成达标。
>
> 未达标时页面写「未达到该项黄金账户标准」。若快照里已经看得到相关对象，建议会补一句「账户里已有……，是否达标不由该对象是否存在决定」，布尔值保持 `false`。
>
> 自适应展示广告只挂在暂停系列上：保持未达标，建议写「已有自适应展示广告，所在展示系列已暂停，本期无消耗」，禁止写「请使用」。

**得分**：页面按 `goldAccountScore` 展示。接口原值仍含已停用的 `expandedTextAdQualified`（3 分）；该项为 `true` 时，页面扣掉这 3 分。**未达标项数**按当前表内项目重算。

---

## 05 投放预算与竞争力分析

**区块 ID**：`section-budget-competitiveness`  
**数据**：`budgetCompetitiveness`（数组）

### 核心系列 IS 目标（公式说明）

- **核心系列 IS 目标** = `impressions ÷ (impressions ÷ searchImpressionShare ÷ 100)`
- 说明：理论可获得展示 = `impressions ÷ (searchImpressionShare ÷ 100)`

### 竞争力表

| 指标 (Metric) | 报告值 (Report Value) | 健康标准 (Health Benchmark) | 优化策略 (Optimization Strategy)        |
| ------------- | --------------------- | --------------------------- | --------------------------------------- |
|               |                       |                             | **按行填写 `strategy`，禁止整列同一句** |

示例差异化方向（须代入本账户数字，勿照抄）：

| metric                            | 策略侧重点                                    |
| --------------------------------- | --------------------------------------------- |
| `budgetUtilizationRate`           | 日预算是否打满、是否需调日预算/排期           |
| `searchImpressionShare`           | 份额偏低时优先查预算丢失 vs 排名丢失占比      |
| `searchBudgetLostImpressionShare` | 预算丢失高 → 加预算/拆核心系列预算            |
| `searchRankLostImpressionShare`   | 排名丢失高 → 出价/质量分/落地页，而非只加预算 |
| 核心系列 IS 目标                  | 对照公式与目标差距，列可执行的系列级动作      |

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
**数据**：`landingPageAnalysis`（`source`: `api` | `none`）

- **`api`**：TSO Lighthouse 成功 → 下表四行（达标率 / PC·移动打开速度 / 手机性能指数）。
- **`none`**：API 重试仍失败 → 写「数据未获取」；**禁止**编造 FCP / 性能指数。
- 测速全 0 / 未测到时，HTML 显示「未测到」，**不会**标 P1；Agent 也勿把「性能缺失」写入 §12 核心问题。
- **`analysis` / `suggestions`**：只写着陆页；关键词洞察写到 §08。

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

**items 行字段**：`campaignName`、`duration`（**天数 number**）、`biddingStrategyType`、`recommendedStrategy`、`isCorrect` 为事实。`recommendationReason` 由 render 按当前策略与建议策略写成一句，Agent 不要填。

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

| 广告              | Headlines                            | Descriptions                               | 优化建议                                                  |
| ----------------- | ------------------------------------ | ------------------------------------------ | --------------------------------------------------------- |
| `items[].adTitle` | `headlinesCount` / `headlinesStatus` | `descriptionsCount` / `descriptionsStatus` | `items[].suggestion`（render 按条数与状态写入） |

- **模块级**分析 / 建议：`adCreativeOptimization.analysis`、`adCreativeOptimization.suggestions`（主观分析，Agent 填写）
- **逐条创意建议**：render 写入，Agent 不要填

---

## 11 新产品应用

**区块 ID**：`section-new-features`  
**数据**：`newFeatures.items`（collect 来自 campaign-types；过滤 `strategy === "AiMax"` 的行）

**items 行字段**：

- collect 事实（勿改）：`strategy`（如 `PerformanceMax`）、`strategyName`（如 `效果最大化`）、`accountStatus`（**boolean**，`true`=已启用）
- `optimizerRecommendation` 由 render 按 `accountStatus` 写成「已启用」或「本期未检测到对应系列」
- **禁止**用 `feature` 替代 `strategyName`

| 策略/功能 (Strategy/Feature) | 账户状态 (Account Status) | 优化师建议 (Senior Optimizer Recommendation) |
| ---------------------------- | ------------------------- | -------------------------------------------- |
|                              |                           |                                              |

---

## 12 诊断总结

**区块 ID**：`section-summary`（页面标题为「总结」，导航为「诊断总结」）  
**数据**：`summary`

### 12.1 核心问题总结

- `summary.keyIssues`：逐条列出（或写「暂无核心问题」）
- **不要写**：否词数量/缺少否词（本报告无否词数据）；着陆页测速数据缺失（见撰写硬约束第 5 条）

### 12.2 优先级优化路线图

| 优先级 | 优化重点 | 关键行动 | 预期效果 |
| ------ | -------- | -------- | -------- |
|        |          |          |          |

**数据**：`summary.optimizationRoadmap` — **对象数组**（与 HTML 表格四列对齐；禁止只写字符串）

```json
{
  "priority": "P0（立即）",
  "focusArea": "恢复投放与账户结构",
  "actionItems": ["恢复核心 Search 系列", "补全 RSA 与附加信息"],
  "expectedOutcome": "恢复有效曝光，rank lost IS 开始下降"
}
```

| 字段              | 说明                                 |
| ----------------- | ------------------------------------ |
| `priority`        | P0/P1/P2… 或「P0（立即）」等可读标签 |
| `focusArea`       | 优化重点（表格「优化重点」列）       |
| `actionItems`     | 字符串数组，关键行动列表             |
| `expectedOutcome` | 预期效果                             |

> 若 Agent 暂写 `"第 1 周：…"` 字符串，render 会尽力拆成 focusArea + actionItems，但**仍须补全 `expectedOutcome` 对象格式**以获得完整表格。

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
