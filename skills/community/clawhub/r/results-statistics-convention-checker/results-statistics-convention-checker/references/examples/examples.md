# 统计报告 Examples（成员 B：results-statistics-convention-checker）

本文件收录从 8 篇心理学/环境行为论文 Results 部分提取的统计报告 examples，包括正例（Positive Example）与问题例（Problem Example），供诊断时对照引用。

## 8 篇来源论文清单

| 编号 | 论文 | 期刊 | 年份 |
| --- | --- | --- | --- |
| P1 | Xu, Liu, Li & Xia, *Effects of environmental lighting on students' sleep, alertness and mood: A field study in a Chinese boarding school* | Lighting Research & Technology, 56, 185–206 | 2024 |
| P2 | Yoon, Lim, Kim & Joo, *The relationship between perceived restorativeness and place attachment for hikers at Jeju Gotjawal Provincial Park in South Korea* | Frontiers in Psychology, 14, 1201112 | 2023 |
| P3 | Jain, Garg & Goel, *Comparison of Indoor Air Quality for Air-Conditioned and Naturally Ventilated Office Spaces* | Lecture Notes in Civil Engineering (Vol. 60) | 2020 |
| P4 | Song, Xu, Wang, Lu, Gong, Si & Xu, *Is more vegetation always better? Evaluation of restorative benefits and preference for window views* | Building and Environment, 272, 112660 | 2025 |
| P5 | Elsadek, Zhang & Liu, *High-rise window views: Evaluating the physiological and psychological impacts of green, blue, and built environments* | Building and Environment, 262, 111798 | 2024 |
| P6 | Dong, Liu, Qi & Huang, *Research on the Current Situation and Improvement Strategy of Light Environment in College Classroom* | IOP Conf. Series: Earth and Environmental Science, 531, 012045 | 2020 |
| P7 | Luo, Xie, Wang, Wang, Chen, Yang & Furuya, *Natural Dose of Blue Restoration: A Field Experiment on Mental Restoration of Urban Blue Spaces* | Land, 12, 1834 | 2023 |
| P8 | Yao, Lin, Bao & Zeng, *Natural or balanced? The physiological and psychological benefits of window views with different proportions of sky, green space, and buildings* | Sustainable Cities and Society, 104, 105293 | 2024 |

---

## Example ID：B-01
**Source**：Xu et al., 2024, Lighting Research & Technology（P1）
**Dimension**：Statistics
**Type**：Positive Example
**Original Sentence / Paragraph**：
> ANOVAs revealed significant differences in horizontal illuminance (F(1,389) = 715.57, p < 0.001), vertical illuminance (F(1,389) = 99.43, p < 0.001) and EML (F(1,389) = 224.32, p < 0.001) between baseline and intervention during the increased light level hours.

**Why it is useful**：
三个 F 检验均完整报告了自由度 F(df1, df2)、统计量数值和 p 值，格式统一，多个同类检验并列呈现时结构平行，是 ANOVA 结果批量报告的规范范本。

**Reusable Rule**：
报告 F 检验必须包含 F(df1, df2) = 值，p 值；同一句话报告多个同类检验时，保持“(统计量(自由度) = 值, p 值)”的平行结构。

**Possible Application**：
诊断时发现用户写 "F = 5.98, p < .05" 或 "F(208) = 5.98" 等缺自由度的报告，引用本例说明完整格式，并给出 Before / After 改写。

---

## Example ID：B-02
**Source**：Xu et al., 2024, Lighting Research & Technology（P1）
**Dimension**：Statistics
**Type**：Positive Example
**Original Sentence / Paragraph**：
> The mixed two-factor ANOVA revealed a significant main effect of timing on deep sleep duration (F(1,208) = 5.98, p = 0.02) and no significant interaction between timing and lighting condition (F(1,208) = 0.41, p = 0.52).

**Why it is useful**：
显著与不显著的结果都完整报告统计量与精确 p 值（p = 0.52 而非 "p > 0.05" 或 "n.s."），体现了“阴性结果同样需要完整统计信息”的规范意识。

**Reusable Rule**：
不显著的结果也要报告完整统计量与精确 p 值，不能只写 "no significant difference" 或 "n.s." 了事。

**Possible Application**：
用户草稿中只报告显著结果、对不显著结果一笔带过时，引用本例要求补全统计量与精确 p 值。

---

## Example ID：B-03
**Source**：Xu et al., 2024, Lighting Research & Technology（P1）
**Dimension**：Statistics
**Type**：Positive Example
**Original Sentence / Paragraph**：
> On average, the mean ± standard error of the mean (SEM) deep sleep duration after the morning high light intervention (144.75 ± 4.94) was higher than that after the evening high light intervention (130.02 ± 5.47).

**Why it is useful**：
使用 "mean ± ..." 形式时明确界定了 ± 后面是 SEM（标准误）而非 SD，避免了 ± 报告最常见的歧义。

**Reusable Rule**：
凡使用 "X ± Y" 形式，必须在首次出现处说明 Y 是 SD 还是 SEM；同一篇论文中不可混用而不加说明。

**Possible Application**：
用户草稿出现 "64.42 ± 1.24" 但未说明 ± 含义时，引用本例要求补充界定（对照问题例 B-07）。

---

## Example ID：B-04
**Source**：Xu et al., 2024, Lighting Research & Technology（P1）
**Dimension**：Statistics
**Type**：Positive Example
**Original Sentence / Paragraph**：
> After the intervention, there was a marginally significant difference in the data between the two groups (p = 0.051).

**Why it is useful**：
对处于临界的结果（p = 0.051），论文如实报告精确 p 值并用 "marginally significant" 明确标注其边缘性质，没有把 p = 0.051 写成 "significant"，也没有掩盖数值。

**Reusable Rule**：
0.05 < p < 0.10 的结果应报告精确 p 值，并标注 "marginally significant"（边缘显著）或如实表述为不显著；不得将其当作显著结果陈述。

**Possible Application**：
用户将 p = .06、p = .08 写成 "significantly improved" 时，引用本例（并对照问题例 B-08）要求改为边缘显著的规范表述。

---

## Example ID：B-05
**Source**：Yoon et al., 2023, Frontiers in Psychology（P2）
**Dimension**：Statistics
**Type**：Positive Example
**Original Sentence / Paragraph**：
> For the pooled sample (n = 408), both the measurement model (χ2 = 264.767, df = 51, RMSEA = 0.084, NNFI = 0.971, CFI = 0.977, SRMR = 0.078) and path model (χ2 = 111.361, df = 49, RMSEA = 0.057, NNFI = 0.991, CFI = 0.993, SRMR = 0.032) showed an acceptable fit for the data.

**Why it is useful**：
SEM/路径分析报告了完整的拟合指标组合（χ2、df、RMSEA、NNFI/TLI、CFI、SRMR），而非只报 χ2，是模型拟合报告的国际惯例范本。

**Reusable Rule**：
报告结构方程模型/验证性因子分析时，应同时报告 χ2、df 及至少 2—3 个拟合指数（如 CFI、RMSEA、SRMR），并说明可接受的临界标准。

**Possible Application**：
用户只写 "the model fit was good (χ2 = ..., p < .05)" 时，引用本例要求补齐 df 与多个拟合指数。

---

## Example ID：B-06
**Source**：Yoon et al., 2023, Frontiers in Psychology（P2）
**Dimension**：Statistics
**Type**：Positive Example
**Original Sentence / Paragraph**：
> First, the perceived restorativeness of visitors at Jeju Gotjawal Provincial Park positively influenced place identity (H1; β = 0.618, p < 0.001) and 38.2% of the variance in place identity was explained by perceived restorativeness. Second, visitors' perceived restorativeness had a positive effect on place dependence (H2; β = 0.567, p < 0.001).

**Why it is useful**：
路径系数报告包含标准化 β、显著性，并补充解释方差比例（38.2%），让读者能判断效应的实际大小而非仅知其显著；同时用 H1/H2 标注使统计结果与假设一一对应。

**Reusable Rule**：
报告回归/路径系数时给出标准化 β、p 值，并尽可能补充 R² 或解释方差比例；统计结果应与研究假设编号对应。

**Possible Application**：
用户只写 "perceived restorativeness significantly predicted place attachment (p < .05)" 时，引用本例要求补充 β 与解释方差，并标注对应假设。

---

## Example ID：B-07
**Source**：Elsadek et al., 2024, Building and Environment（P5）
**Dimension**：Statistics
**Type**：Problem Example
**Original Sentence / Paragraph**：
> As depicted in Fig. 5, different window views resulted in significantly different values for alpha relative power at (O1), (F, 64.94, p < 0.05). The alpha relative power was significantly higher when participants viewed scenes featuring a combination of (GW) (0.23 ± 0.02) compared to all other visual stimuli (p < 0.05).

**Why it is useful**：
该句存在两个典型问题：(1) F 检验缺少自由度，写成 "(F, 64.94, p < 0.05)"，读者无法判断检验的具体设计与功效；(2) "(0.23 ± 0.02)" 未说明 ± 是 SD 还是 SEM。这是真实发表论文中仍存在的统计报告缺陷，非常适合作为对照。

**Reusable Rule**：
F 统计量必须附带 (df1, df2)；"X ± Y" 必须界定 Y 的性质（SD 或 SEM）。

**Possible Application**：
用户草稿中出现 "F, 64.94" 式残缺统计量或未界定的 ± 数值时，引用本例定位问题，并用 B-01、B-03 的格式给出 After 改写：*F*(5, 114) = 64.94, *p* = .032（df 与精确 p 需用户据实补全）。

---

## Example ID：B-08
**Source**：Yao et al., 2024, Sustainable Cities and Society（P8）
**Dimension**：Statistics
**Type**：Problem Example
**Original Sentence / Paragraph**：
> Regarding HR, the I-S3B3G3 (p < 0.01), II-S1B4G4 (p < 0.1), III-S4B1G4 (p < 0.1), IV-S4B4G1 (p < 0.05), and VI-S1B1G8 (p < 0.01) groups of window views had varying degrees of significance according to paired-sample t tests comparing pretest and posttest values...
> Most of the experimental groups showed a significant increase in Stroop scores... p values were less than 0.001, 0.001, 0.001, 0.001, 0.05, 0.001, 0.001, and 0.001 for the I-S3B3G3, ... groups, respectively.

**Why it is useful**：
该段集中体现了三类问题：(1) 将 p < 0.1 当作显著性层级报告（"varying degrees of significance"），违背 α = .05 的常规显著性标准，应标注为边缘显著或如实报告精确 p 值；(2) 成串罗列 p 值但未报告 t 统计量与自由度，读者无法复核；(3) 无效应量，无法判断差异的实际意义。

**Reusable Rule**：
只报 p 值不报检验统计量与自由度属于不完整报告；p 在 .05—.10 之间不得表述为 "significant"；成组比较应报告 t(df) 或放入规范表格。

**Possible Application**：
用户草稿出现 "p < 0.1 表明有一定显著性" 或连续罗列 p 值而无 t、df 时，引用本例说明问题，并参照 B-02、B-12 补全统计量、效应量。

---

## Example ID：B-09
**Source**：Dong et al., 2020, IOP Conf. Series: Earth and Environmental Science（P6）
**Dimension**：Statistics
**Type**：Problem Example
**Original Sentence / Paragraph**：
> According to the data analysis, the uniformity of illuminance in the three states is mostly lower than the 300 lx required by the specification, and only the data 32%, 84% and 8% meet the requirements respectively, while the average illuminance is only 8%, 13% and 33% meet the requirements respectively compared with the specification.

**Why it is useful**：
整个 Results 只有百分比和 "according to the data analysis" 这类模糊表述：没有各组的 M 与 SD，没有任何推断统计，"mostly lower" 的程度无法量化。这是“描述统计不完整、推断统计完全缺失”的典型。

**Reusable Rule**：
比较组间差异时必须给出各组 M、SD（或 Mdn），并用适当的推断统计支撑 "lower/higher/significant" 类结论；避免 "data analysis shows" 这类无统计信息支撑的表述。

**Possible Application**：
用户草稿仅有百分比或均值、无任何 SD 与检验时，引用本例定位“统计报告严重缺失”，按 rubric 评 1—2 分，并要求补全描述统计与推断统计。

---

## Example ID：B-10
**Source**：Jain, Garg & Goel, 2020, Lecture Notes in Civil Engineering（P3）
**Dimension**：Statistics
**Type**：Problem Example
**Original Sentence / Paragraph**：
> The particle mass concentration was observed to be higher inside the premises of naturally ventilated Office (O-2)... were found to be 600.53 ± 132.61 µg/m3 and 255.22 ± 79.81 µg/m3 for PM10 and PM1, respectively. These values are 30–40% higher than values recorded in the air-conditioned office O-1... The reason for large particle mass concentration in Office 2 is its ventilation condition.

**Why it is useful**：
该段的问题：(1) 用 "30–40% higher" 直接断言差异，却没有进行任何统计检验（无 t、F、p），差异是否具有统计意义未知；(2) ± 未界定是 SD 还是 SEM；(3) 在 Results 中直接给出因果解释（"The reason ... is its ventilation condition"），统计结果与解释混杂。

**Reusable Rule**：
声称组间差异（higher/lower）必须有统计检验支撑；± 需界定；Results 中只陈述统计事实，原因解释归入 Discussion。

**Possible Application**：
用户草稿出现未检验的 "X% higher" 断言或结果与原因解释混写时，引用本例说明需补充检验并拆分结果与解释。

---

## Example ID：B-11
**Source**：Song et al., 2025, Building and Environment（P4）
**Dimension**：Statistics
**Type**：Positive Example
**Original Sentence / Paragraph**：
> Table 1. Paired-sample t tests of restorative benefits on psychological and physiological indicators (pretest vs. post 1st-test).
> （表头：Variable | Paired differences: Mean, Std. deviation, Std. error of the mean, 95% confidence interval of the difference (Lower, Upper) | t | df | Sig. (2-tailed)）
> 表注：* p < 0.05; ** p < 0.01; *** p < 0.001.
> 正文示例：Compared with the pre-test and the first post-test, there were no significant differences in ROS dimensions and the total score (Table 1). However, when comparing the pre-test with the last post-test, both clearing one's mind (p < 0.05) and the ROS total score (p < 0.05) showed significant improvement (Table 2).

**Why it is useful**：
成对样本 t 检验以规范表格承载完整信息（均值差、SD、SE、95% CI、t、df、Sig.），正文只做概括性陈述并指向表格（Table 1/Table 2），是“正文概括 + 表格承载完整统计”的标准分工模式，且表格报告了差值的 95% 置信区间。

**Reusable Rule**：
多个同类检验放入表格，表格需含 t、df、p（或 Sig.）与 95% CI；正文用一句话概括并引用表号，不重复罗列全部数字。

**Possible Application**：
用户正文堆叠大量 t 检验数字时，引用本例建议改为表格呈现 + 正文概括；若表格缺 CI 列，提醒补充 95% CI。

---

## Example ID：B-12
**Source**：Song et al., 2025, Building and Environment（P4）
**Dimension**：Statistics
**Type**：Positive Example（含提示）
**Original Sentence / Paragraph**：
> Regarding window view preference, vegetation proportion was moderately to strongly correlated to preference score (p < 0.001, r = 0.82), complexity (p < 0.001, r = 0.55), coherence (p < 0.001, r = 0.36), and mystery (p < 0.001, r = 0.67).

**Why it is useful**：
相关分析同时报告了 r 值与显著性，并用 "moderately to strongly" 对效应大小做了口头解读，符合“相关本身就是效应量”的报告习惯。提示：该研究实际使用的是 Spearman 相关，规范写法宜标注 rs（或 ρ）并与 Pearson 的 r 区分，诊断时可提醒用户注意这一区分。

**Reusable Rule**：
报告相关必须给出 r（或 rs/ρ）数值与 p 值；宜对效应大小分级解读（small/medium/large）；Spearman 相关写作 rs，不与 Pearson r 混用。

**Possible Application**：
用户写 "the two variables were significantly correlated" 而无 r 值时，引用本例要求补 r 与 p；发现 Spearman 误标为 r 时提醒统一符号。

---

## Example ID：B-13
**Source**：Luo et al., 2023, Land（P7）
**Dimension**：Statistics
**Type**：Positive Example
**Original Sentence / Paragraph**：
> For SVS, there was a significant main effect of experimental sites on the scores of subjective vitalities, FPlace = 4.605, p = 0.003, Partial η2 = 0.028 (Table 5). Paired comparison results indicated that urban river (M = 4.51), urban canal (M = 4.36), and urban lake (M = 4.30) were equal in measure and higher than urban environments (control group, M = 4.04)... Furthermore, the insignificant interaction effect (FPlace×Time = 0.995, p = 0.428, Partial η2 = 0.012, Figure 7a) indicates that no significant differences were shown...

**Why it is useful**：
这是本组 8 篇中最完整的推断统计报告范本：F 值、精确 p 值、partial η² 效应量三件套齐备；不显著结果同样完整报告；事后比较给出各组 M 支撑方向性结论。

**Reusable Rule**：
方差分析报告应包含 F（含 df，可在表格中承载）、精确 p、效应量（partial η²）；事后比较应报告各组 M（与 SD）以支撑方向性结论。

**Possible Application**：
作为“5 分标准”的锚定 example：用户 ANOVA 报告只给 F 与 p 时，引用本例要求补效应量与事后比较的 M。

---

## Example ID：B-14
**Source**：Luo et al., 2023, Land（P7）
**Dimension**：Statistics
**Type**：Positive Example（含提示）
**Original Sentence / Paragraph**：
> Cronbach's α values were good for all scales, ranging from 0.73 to 0.96, with only one data point having a lower but acceptable reliability score (SVS (T2, CG) = 0.60).

**Why it is useful**：
信度报告给出 α 的范围并如实披露个别低于常规阈值（0.70）的数值（0.60），同时说明其可接受性，体现了透明报告原则。提示：表格中出现 "p = 0.000" 的写法（如 Table 5 中 Sig. = 0.000）不规范，p 不可能为 0，应写 p < .001——诊断时可用此细节提醒用户检查表格。

**Reusable Rule**：
量表信度在 Results（或 Method）中报告 Cronbach's α 的具体数值或范围，低于 .70 的需说明；p 值永不为 0，"p = .000" 应改为 "p < .001"。

**Possible Application**：
用户表格中出现 "Sig. = .000" 或只写 "the scale was reliable" 而无 α 数值时，引用本例给出规范改法。

---

## 可复用统计报告模板（从以上 examples 提炼）

1. **t 检验**：`t(df) = X.XX, p = .XXX, Cohen's d = X.XX, 95% CI [lower, upper]`
   例：*t*(59) = 7.10, *p* < .001, 95% CI [2.25, 4.02]
2. **F 检验（ANOVA）**：`F(df1, df2) = X.XX, p = .XXX, partial η² = .XXX`
   例：*F*(1, 208) = 5.98, *p* = .02（对照 B-01、B-13）
3. **相关**：`r(df) = .XX, p = .XXX`（Spearman 用 rs）
   例：*r* = .82, *p* < .001（对照 B-12）
4. **回归/路径系数**：`β = .XX, p < .XXX`，并报告 R² 或解释方差（对照 B-06）
5. **χ² / SEM 拟合**：`χ²(df) = X.XX, p = .XXX, CFI = .XXX, RMSEA = .XXX, SRMR = .XXX`（对照 B-05）
6. **描述统计**：`M = X.XX, SD = X.XX`；"X ± Y" 首次出现处界定 Y 为 SD 或 SEM（对照 B-03）
7. **不显著结果**：完整报告统计量与精确 p，例：*F*(1, 208) = 0.41, *p* = .52（对照 B-02）
8. **边缘显著**：`p = .051` 标注 "marginally significant"，不得写为 significant（对照 B-04）
