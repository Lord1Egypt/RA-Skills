# Demand Gen 投放数据分析汇总报告 — Excel

> **终稿语言**：Sheet 名和表头跟 `meta.lang`。英文用下面的英文表名和表头，不要另起结构。
> **适用场景**：用户明确要求 **Demand Gen 汇总报告 + Excel/xlsx**。工作流 **P4-DG**。
> **工作流**：与 `demand-gen-analysis-report.md` 共用拉数和 JSON。交付形态不同。
> **禁止**：调用 `google-analysis demand-gen-render` 代替 xlsx；加载宿主「xlsx / Excel」第三方 Skill；把 HTML 样例里的演示数字写入单元格。

用户没要 Excel 时，只走 HTML 纲要。两样都要时，先写同一份 `demand-gen-analysis-report.json`，再渲染 HTML，并用本文把这份 JSON 写成 xlsx。

样式按 `excel-style-guide.md`，脚本可 `import` 同目录 `excel-style-kit.mjs`。账户 ID、系列 ID、广告组 ID 用文本（`numFmt: '@'`）。

---

## 执行门禁

| # | 门禁 | 动作 |
| --- | --- | --- |
| 1 | Read | `agent-conventions.md`、`demand-gen-analysis-report.md`、本文 |
| 2 | 账户 | `list-accounts -m Google -k <id> --json-out ./snap-dg` |
| 3 | 币种 | `items[].ma.currencyCode` |
| 4 | 拉数 | 与 HTML 纲要相同。Demand Gen 过滤 `channelTypeV2 = DEMAND_GEN`。版位用 `ad demand-gen report` |
| 5 | outline | 每个 `google-analysis` section 先 Read `*.outline.txt` |
| 6 | JSON | 脚本写入 `demand-gen-analysis-report.json`。缺 CRM 的格子写 `未提供` |
| 7 | 写簿 | 脚本只读这份 JSON 和落盘快照。9 张表都要有，空表也保留表头并写 `未提供` |
| 8 | 审阅 | `agent-conventions.md` §七。xlsx 无法 Read 时贴自检表和脚本 stdout |

---

## 9 张表

中文表名固定如下。英文终稿换成括号里的名字。

| 表 | 内容来源 |
| --- | --- |
| `01_管理层总览`（`01_Overview`） | `meta`、`headline`、`summaryParagraph`、`headlineKpis`、`summaryPoints` |
| `02_分析范围`（`02_Scope`） | `scopeRows`、`conversionLevels` |
| `03_漏斗`（`03_Funnel`） | `funnel.stages`、`funnel.rates`、两条建议 |
| `04_核心指标`（`04_KPIs`） | `kpiGroups` |
| `05_趋势异常`（`05_Trend`） | `narrative.trend`。HTML 没有这一章 |
| `06_各维度数据`（`06_Dimensions`） | `dimensions`，每个维度一块，块标题用 `title` |
| `07_线索质量`（`07_Lead_Quality`） | `quality` |
| `08_行动建议`（`08_Actions`） | `actions` |
| `09_测试计划`（`09_Tests`） | `tests` |

### 01_管理层总览

- 第 1 行标题：`Demand Gen 投放数据分析汇总报告`（英文 `Demand Gen performance summary`）。
- 第 2 行：账户名、账户 ID、本期、对比期、币种、时区、业务目标、主转化。
- 第 3 行：可信度说明。
- 接着一块「一句话结论」。
- KPI 表头：`指标 | 本期 | 对比期变化 | 备注`。英文 `Metric | Current | Change | Note`。
- 要点表头：`标签 | 标题 | 说明 | 参见`。英文 `Tag | Title | Detail | See`。

### 02_分析范围

两块，不要合成一张没有表头的说明。

- 范围：`项目 | 内容`（`Item | Definition`），来自 `scopeRows`。
- 转化层级：`层级 | 定义 | 来源 | 报告用途`（`Level | Definition | Source | Use`）。

### 03_漏斗

`阶段 | 数量 | 逐级转化率 | 主要影响因素`（`Stage | Volume | Step rate | Driver`）。

阶段名和数量来自 `stages`，转化率和影响因素来自 `rates`。对不上的行分开写，不要为了对齐而编造。表下两行写 `adsAdvice`、`salesAdvice`。

### 04_核心指标

`层级 | 指标 | 本期 | 对比期变化`（`Layer | Metric | Current | Change`）。`层级` 用 `kpiGroups[].title`。

### 05_趋势异常

日表：`日期 | 花费 | 平台转化 | 平台CPA | 有效线索 | 备注`（`Date | Spend | Platform conversions | Platform CPA | Qualified leads | Note`）。

异常表：`现象 | 证据 | 原因 | 动作`（`What happened | Evidence | Cause | Action`）。

日花费和平台转化来自 `daily-metrics` 里 Demand Gen 能拆出来的部分。拆不出来就用账户日花费，并在备注写「账户合计，含非 Demand Gen」。有效线索没有 CRM 就写 `未提供`。

### 06_各维度数据

每个 `dimensions[]` 一块。表头用该块的 `columns`，不要改成另一套列。建议列（有数据才出现）：

| 块 | 中文列 | 英文列 |
| --- | --- | --- |
| Campaign | 投放组合、花费、有效线索、有效成本、有效率、商机率、状态、修改建议 | Mix, Spend, Qualified leads, Cost per qualified, Qualified rate, Opportunity rate, Status, Change |
| 素材 | 素材角度 + 同上，可无商机率 | Angle |
| 受众 | 受众 + Campaign 列 | Audience |
| 地域 | 地域 + Campaign 列 | Location |
| 设备 | 设备 + Campaign 列 | Device |
| 版位 | 版位 + Campaign 列 | Channel |
| 来源 | 来源 + Campaign 列 | Source |

没有 CRM 时删掉有效线索及之后的业务列，改留「花费、平台转化、平台 CPA、修改建议」，并在块下注明。不要留一列全是 `未提供` 假装算过。

版位块只来自 `ad demand-gen report`。地域、设备、受众若仍是账户合计，块下写明，不要把它们说成 Demand Gen 已对账。

### 07_线索质量

`线索批次 | 表单 | 有效线索 | 商机 | 成交 | 成交收入 | 成熟度 | 建议`（`Cohort | Forms | Qualified | Opportunities | Wins | Revenue | Maturity | Note`）。

没有批次资料时只留一行 `未提供`。表下写 `businessConclusion` 和 `splitFactors`。

### 08_行动建议

`优先级 | 动作 | 证据 | 具体修改 | 验证阈值 | 负责人 | 时限 | 风险`（`Priority | Action | Evidence | Change | Check | Owner | Due | Risk`）。

优先级只用 `P0` / `P1` / `P2`。

### 09_测试计划

`测试项 | 假设 | 对照 / 实验组 | 主指标 | 样本量 | 周期 | 停止规则`（`Test | Hypothesis | Control / variant | Metric | Sample | Window | Stop rule`）。

一个测试只改一个主要变量。样本还没达到时，停止规则写「样本不足则不判胜负」。

---

## 不要做的事

- 不要把 9 张表收成 1 张「汇总」。
- 不要把 Search / PMax 系列写进 Campaign 块。
- 不要用模板演示账户的 29 天、$42,680、286、74、19、ROAS 2.84。
- 对比期没拉时，变化列写 `未拉对比期`，不要写 0% 或 `—` 假装持平。
