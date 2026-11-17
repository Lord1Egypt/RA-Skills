# Results 统计报告规范诊断报告（with_skill：加载 results-statistics-convention-checker）

**稿件**：用户提供片段（绿景/建筑窗景恢复性研究 Results 片段，即 tests/test_input.md）　**检查范围**：用户所给 Results 片段（4 个自然段，P1–P4，共 13 句；用户只提供片段，按所给文本切分）　**日期**：2026-08-22

句子编号（供定位）：
- S1 The results showed that the green view was better than the built view.
- S2 According to the data analysis, most participants felt more relaxed after viewing the green view.
- S3 A paired-sample t test was conducted to compare stress scores before and after viewing.
- S4 The result was significant (t = 3.45, p < 0.05), which means the green view can effectively reduce stress.
- S5 The stress score decreased from 4.82 ± 1.03 to 3.91 ± 1.12.
- S6 A one-way ANOVA was performed to examine the effect of view type on attention restoration.
- S7 There was a significant difference between the three groups (F = 8.76, p = .000).
- S8 Post-hoc tests showed the green view group (M = 5.12) scored higher than the built view group (M = 4.03) and the mixed view group (M = 4.55, p < 0.05).
- S9 For heart rate, the green view group showed lower values (62.3 ± 2.1 bpm) than the built view group (71.5 ± 1.8 bpm), and the difference was 12.9%.
- S10 The correlation between preference and restoration was significant (p < 0.01).
- S11 The regression analysis showed that preference significantly predicted restoration (p < 0.05), proving that H1 was supported.
- S12 For skin conductance, there was no significant difference between groups (n.s.).
- S13 The effect of view type on mood was slightly significant (p < 0.1).

---

## 一、总体评分

| 维度 | 得分 (1–5) | 简评 |
|---|---|---|
| 描述统计完整性（checklist B 组） | 2 | S8 只报 M 无 SD；S5/S9 的 "±" 未界定；S2 无任何数值 |
| 推断统计格式（checklist C 组） | 2 | t、F 均缺自由度（S4、S7）；相关缺 r（S10）；回归缺 β 与 R²（S11） |
| p 值报告规范（checklist D 组） | 1 | p = .000（S7）；p < 0.1 当显著（S13）；前导零混用（0.05 与 .000 并存）；阴性结果只写 n.s.（S12） |
| 效应量与置信区间（checklist E 组） | 1 | 全文无 Cohen's d / partial η² / 95% CI |
| 一致性与断言支撑（checklist F 组） | 2 | "12.9% higher"（S9）与 "most participants felt"（S2）无检验支撑；S1 "better" 无指标对应 |
| **总评（统计报告规范维度）** | **2 / 5** | 符合 rubric.md 2 分锚点："统计报告缺项普遍、只报 p 值无统计量、把 p < .1 当显著、声称差异但无检验支撑" |

评分依据：references/rubric.md 的 1–5 分锚点与"单项问题对评分的影响速查表"（只报 p 值无统计量 → 不高于 2 分；p < .1 当显著 → 不高于 3 分；无检验支撑差异断言 → 不高于 2 分；取最严项定级为 2 分）；checklist 未通过项统计（B 组未通过 3/4 项；C 组未通过 4/6 项；D 组未通过 4/5 项；E 组未通过 3/4 项；F 组未通过 3/5 项）。

---

## 二、逐维诊断

### 描述统计 — 2/5

**问题 1：事后比较只报 M、不报 SD**
- 原文引用（定位：P2，S8）："the green view group (M = 5.12) scored higher than the built view group (M = 4.03) and the mixed view group (M = 4.55, p < 0.05)."
- 问题说明：三组均只给 M 未给 SD，读者无法判断组内离散程度与重叠情况。对应 checklist 第 B1、B2 项不通过。
- 修改建议：各组补报 SD，写成 M = 5.12, SD = X.XX 的形式。
- 示范改写："Post hoc tests showed that the green view group (M = 5.12, SD = X.XX) scored higher than the built view group (M = 4.03, SD = X.XX) and the mixed view group (M = 4.55, SD = X.XX), p < .05."（事后比较报 M 的范式：examples_memberB.md 例 B-13 "urban river (M = 4.51)… higher than urban environments (control group, M = 4.04)"（Luo et al., 2023, Land, 3.3 节））

**问题 2："±" 未界定**
- 原文引用（定位：P1，S5；P3，S9）："decreased from 4.82 ± 1.03 to 3.91 ± 1.12" / "62.3 ± 2.1 bpm … 71.5 ± 1.8 bpm"
- 问题说明：两处 ± 均未说明是 SD 还是 SEM，且两者数量级特征不同（可能一处是 SD、一处是 SEM），不界定则无法比较。对应 checklist 第 B3 项不通过。
- 修改建议：首次出现处界定 ± 的性质，全文统一。
- 示范改写："The stress score decreased from 4.82 ± 1.03 (SD) to 3.91 ± 1.12."（界定范式：例 B-03 "the mean ± standard error of the mean (SEM) deep sleep duration … (144.75 ± 4.94)"（Xu et al., 2024, LRT, 3.2 节）；反面参照：问题例 B-07 中 "(0.23 ± 0.02)" 未界定（Elsadek et al., 2024, B&E, 3.1.1 节））

### 推断统计格式 — 2/5

**问题 1：t、F 缺自由度**
- 原文引用（定位：P1，S4；P2，S7）："(t = 3.45, p < 0.05)" / "(F = 8.76, p = .000)"
- 问题说明：t 检验与方差分析均未报告自由度，读者无法复核检验设计与样本量。对应 checklist 第 C1、C2 项不通过。
- 修改建议：补全为 t(df) 与 F(df1, df2)。
- 示范改写："t(58) = 3.45, p = .001"（df 请据实补全）；"F(2, 117) = 8.76, p < .001"（完整格式范式：例 B-01 "F(1,389) = 715.57, p < 0.001"（Xu et al., 2024, LRT, 3.1 节）；例 B-13 "FPlace = 4.605, p = 0.003"（Luo et al., 2023, Land, 3.3 节））

**问题 2：相关与回归只报 p 值、无统计量**
- 原文引用（定位：P4，S10–S11）："The correlation … was significant (p < 0.01)." / "preference significantly predicted restoration (p < 0.05)"
- 问题说明：相关未报告 r 值与方向，回归未报告标准化 β 与 R²，显著性结论无法复核，效应大小完全未知。对应 checklist 第 C4、C5 项不通过；rubric 速查表"只报 p 值、无统计量 → 不高于 3 分"，多处出现累计至 2 分。
- 修改建议：相关补 r(df)；回归补 β、R²，并与假设编号对应。
- 示范改写："Preference was positively correlated with restoration, r(58) = .XX, p < .01."（范式：例 B-12 "(p < 0.001, r = 0.82)"（Song et al., 2025, B&E, 3.3 节））；"Preference positively predicted restoration, β = .XX, p < .05, explaining XX% of the variance (supporting H1)."（范式：例 B-06 "β = 0.618, p < 0.001) and 38.2% of the variance … was explained"（Yoon et al., 2023, Front. Psychol., 4.2 节））

**问题 3：多个同类检验未考虑表格化呈现**
- 原文引用（定位：P1–P3，S4、S7、S8、S9）：t 检验、ANOVA、事后比较、心率比较各自成句散布。
- 问题说明：检验数量较多时全部堆在正文，既重复又易漏项。对应 checklist 第 E4 项提示。
- 修改建议：将成组检验移入规范表格（含 t/F、df、p、95% CI 列），正文概括并引用表号。
- 示范改写：正文改写为 "Paired-sample t tests revealed significant pre–post changes in stress and heart rate (Table 2)."（"正文概括 + 表格承载"分工范式：例 B-11 表头含 Mean difference、SD、SE、95% CI、t、df、Sig.（Song et al., 2025, B&E, Table 1））

### p 值报告 — 1/5

**问题 1：p = .000 写法违规**
- 原文引用（定位：P2，S7）："(F = 8.76, p = .000)"
- 问题说明：p 值不可能等于 0，"p = .000" 是统计软件输出的直接搬用。对应 checklist 第 D2 项不通过。
- 修改建议：改为 p < .001。
- 示范改写："F(2, 117) = 8.76, p < .001"（规范提示：例 B-14 指出表格中 "Sig. = 0.000" 应改为 p < .001（Luo et al., 2023, Land, Table 5 注））

**问题 2：p < 0.1 被当作显著**
- 原文引用（定位：P4，S13）："The effect of view type on mood was slightly significant (p < 0.1)."
- 问题说明：以 α = .05 为标准，p < .1 不构成显著；"slightly significant" 不是规范术语。对应 checklist 第 D5 项不通过；rubric 速查表"p < .1 当显著 → 不高于 3 分"。
- 修改建议：报告精确 p 值并标注 "marginally significant"，或如实表述为不显著。
- 示范改写："The effect of view type on mood was marginally significant, F(2, 117) = X.XX, p = .08."（边缘显著规范表述范式：例 B-04 "there was a marginally significant difference … (p = 0.051)"（Xu et al., 2024, LRT, 3.2 节）；反面参照：问题例 B-08 将 p < 0.1 作为显著层级（Yao et al., 2024, SCS, 3.1 节））

**问题 3：阴性结果只写 n.s.、前导零混用**
- 原文引用（定位：P4，S12；全文）："there was no significant difference between groups (n.s.)"；"p < 0.05"（S4）与 "p = .000"（S7）前导零并存。
- 问题说明：阴性结果同样需要完整统计量与精确 p 值；APA 惯例中小于 1 的统计量不写前导零（p = .02），全文须统一。对应 checklist 第 D4、D3 项不通过。
- 修改建议：补全统计量与精确 p；统一为 APA 无前导零写法。
- 示范改写："There was no significant group difference in skin conductance, F(2, 117) = 0.XX, p = .XX."（阴性结果完整报告范式：例 B-02 "no significant interaction … (F(1,208) = 0.41, p = 0.52)"（Xu et al., 2024, LRT, 3.2 节））

### 效应量与置信区间 — 1/5

**问题 1：全文无效应量、无置信区间**
- 原文引用（定位：P1–P4 全部显著结果，S4、S7、S10、S11）。
- 问题说明：四处显著结果均未报告任何效应量（Cohen's d、partial η²、r、β）或 95% CI，显著性无法转化为实际意义判断。对应 checklist 第 E1–E3 项不通过；rubric 速查表"效应量完全缺失 → 不高于 3 分"，与推断统计问题叠加至 1 分锚点（"效应量与 CI 完全缺失"）。
- 修改建议：t 检验补 Cohen's d 与 95% CI；ANOVA 补 partial η²；相关以 r 为效应量并分级解读；回归补 R²。
- 示范改写："t(58) = 3.45, p = .001, d = 0.XX, 95% CI [X.XX, X.XX]"；"F(2, 117) = 8.76, p < .001, partial η² = .XX"（效应量三件套范式：例 B-13 "FPlace = 4.605, p = 0.003, Partial η2 = 0.028"（Luo et al., 2023, Land, 3.3 节）；CI 范式：例 B-11 表格含 "95% confidence interval of the difference"（Song et al., 2025, B&E, Table 1））

### 一致性与断言支撑 — 2/5

**问题 1：无检验支撑的差异断言**
- 原文引用（定位：P3，S9；P1，S2）："the difference was 12.9%" / "most participants felt more relaxed after viewing the green view."
- 问题说明：S9 直接以均值差百分比断言心率差异，无任何检验；S2 的 "most participants felt" 无人数、比例或统计支撑，"according to the data analysis" 属模糊表述。对应 checklist 第 F3、B4 项不通过；rubric 速查表"声称差异但无检验支撑 → 不高于 2 分"。
- 修改建议：心率比较补 t 检验；S2 删除或补具体统计。
- 示范改写："The green view group showed lower heart rate (M = 62.3, SD = 2.1 bpm) than the built view group (M = 71.5, SD = 1.8 bpm), t(58) = X.XX, p = .XXX, d = X.XX."（反面参照：问题例 B-10 "These values are 30–40% higher …" 无检验断言（Jain et al., 2020, LNCE, 3.1 节）；问题例 B-09 "According to the data analysis … only the data 32%, 84% and 8% meet the requirements"（Dong et al., 2020, IOP EES, 3.3 节））

**问题 2：方向性结论与统计表述不对应**
- 原文引用（定位：P1，S1）："The results showed that the green view was better than the built view."
- 问题说明："better" 未对应任何具体指标与统计结果，是随后各检验的提前概括，但未说明概括依据。对应 checklist 第 F2 项部分通过。
- 修改建议：总起句指明指标与方向，或改为引出分析结构的框架句。
- 示范改写："The green view produced better restoration outcomes than the built view across stress, attention, and heart rate measures, as detailed below."（结果先行概括的边界：需随后逐项以统计支撑）

---

## 三、转介提示（不在本技能维度扣分）

以下问题超出本技能范围，建议交由对应技能处理：
- 过度声称/hedging：S4 "which means the green view can effectively reduce stress"、S11 "proving that H1 was supported" 的因果与强度表述 → results-claim-hedging-checker
- 篇章结构：总起句（S1）与各指标结果的呈现顺序、是否按假设组织 → results-structure-diagnoser
- 学术词汇："better""slightly significant" 等口语化/非规范表述 → results-vocabulary-lexis-advisor
- 时态语法：S2 "felt"、S11 "proving" 等时态与分词结构 → results-tense-grammar-checker
- 衔接连贯：段间过渡与信息流 → results-cohesion-flow-checker

---

## 四、修改优先级排序

| 优先级 | 问题 | 位置 | 理由 |
|---|---|---|---|
| 高 | t/F 缺自由度；相关/回归只报 p 无统计量 | S4, S7, S10, S11 | 统计报告硬伤，结果不可复核 |
| 高 | p = .000；p < 0.1 当显著 | S7, S13 | 违背显著性报告基本规范，扭曲结论强度 |
| 高 | "12.9%"、"most participants felt" 无检验断言 | S9, S2 | 结论缺乏证据支撑，须补检验或删除 |
| 中 | 全文补效应量与 95% CI | S4, S7, S10, S11 | APA 与期刊普遍要求，决定效应的实际意义解读 |
| 中 | 阴性结果补完整统计量；"±" 界定；事后比较补 SD | S12, S5, S9, S8 | 信息完整性问题，修复成本低 |
| 低 | 前导零统一、统计符号斜体、检验结果表格化 | 全文 | 格式润色性质，最后处理 |

**优先处理**：先修"高"优先级（补自由度与统计量 → 规范 p 值 → 为无检验断言补统计），再补效应量与 CI，最后统一格式细节。
