# Test Output：results-statistics-convention-checker 标准诊断输出

> 对应 `tests/test_input.md` 的诊断结果，展示本 Skill 的预期输出格式与诊断深度。

## Dimension Score

评分：**2 / 5**（统计报告规范维度）

评分理由：草稿存在统计量缺自由度、只报 p 值无统计量、p = .000、p < 0.1 当显著、± 未界定、无效应量与置信区间、未经检验的百分比差异断言等多处问题（对照 rubric.md：普遍只报 p 值/缺统计量 → 不高于 2 分）。主要检验尚能看出分析意图，故评 2 分而非 1 分。

## Key Problems

按严重程度排序：

1. **【高】统计量普遍缺自由度**：t 检验写成 "t = 3.45"，ANOVA 写成 "F = 8.76"，均未报告 df，读者无法复核。
2. **【高】p 值报告违规**：出现 "p = .000"（p 不可能为 0）；"slightly significant (p < 0.1)" 把 p < .1 当作显著，违背 α = .05 标准。
3. **【高】只报 p 值、无统计量**：相关分析（"p < 0.01"）与回归分析（"p < 0.05"）均无 r、β 等统计量。
4. **【高】未经检验的差异断言**："the difference was 12.9%" 直接用心率均值差百分比声称差异，无任何检验支撑。
5. **【中】效应量与置信区间完全缺失**：所有显著结果均无 Cohen's d / partial η² / 95% CI。
6. **【中】"±" 未界定**："4.82 ± 1.03"、"62.3 ± 2.1 bpm" 未说明是 SD 还是 SEM。
7. **【中】不显著结果报告不完整**："no significant difference between groups (n.s.)" 未给出统计量与精确 p 值。
8. **【中】描述统计不完整**：ANOVA 事后比较只给 M，未给 SD；心率比较只有 ± 数值。
9. **【低】格式不统一**："p < 0.05"（带前导零）与 "p = .000"（不带前导零）混用；统计符号未斜体；"n.s." 非 APA 推荐写法。
10. **【低】统计结论表述越界**："proving that H1 was supported" 中 prove 属于强度问题（提示转交 results-claim-hedging-checker，本 Skill 不计分）；"According to the data analysis, most participants felt more relaxed" 无任何统计信息支撑。

## Evidence from Draft

- "The result was significant (t = 3.45, p < 0.05)" —— t 缺 df；
- "There was a significant difference between the three groups (F = 8.76, p = .000)" —— F 缺 df，p = .000 违规；
- "The correlation between preference and restoration was significant (p < 0.01)" —— 缺 r；
- "preference significantly predicted restoration (p < 0.05)" —— 缺 β 与 R²；
- "the difference was 12.9%" —— 无检验支撑的差异断言；
- "there was no significant difference between groups (n.s.)" —— 阴性结果无统计量；
- "slightly significant (p < 0.1)" —— p < .1 当显著；
- "4.82 ± 1.03" / "62.3 ± 2.1 bpm" —— ± 未界定。

## Example-based Comparison

- 对照 **B-01**（Xu et al., 2024）：规范的 F 报告为 F(1,389) = 715.57, p < 0.001，草稿的 "F = 8.76" 缺 (df1, df2)；
- 对照 **B-02**（Xu et al., 2024）：阴性结果应写 F(1,208) = 0.41, p = 0.52，草稿只写 "n.s."；
- 对照 **B-03**（Xu et al., 2024）：± 需界定为 SD 或 SEM，草稿未界定（与问题例 **B-07** 中 Elsadek et al., 2024 的缺陷相同）；
- 对照 **B-04**（Xu et al., 2024）：p = .051 标注 "marginally significant" 是规范做法，草稿的 "slightly significant (p < 0.1)" 与问题例 **B-08**（Yao et al., 2024）同类；
- 对照 **B-06**（Yoon et al., 2023）：回归应报告 β = 0.618, p < 0.001 及解释方差 38.2%，草稿只有 p；
- 对照 **B-11**（Song et al., 2025）：多个 t 检验宜用表格承载 t、df、p、95% CI，正文概括并引用表号；
- 对照 **B-12**（Song et al., 2025）：相关应报告 r 数值（如 r = 0.82, p < 0.001）；
- 对照 **B-13**（Luo et al., 2023）：ANOVA 应三件套齐备 F、p、partial η²；
- 对照 **B-14**（Luo et al., 2023）：表格中 "p = 0.000" 应改为 p < .001；
- 对照 **B-10**（Jain et al., 2020）："12.9% higher" 式无检验断言是典型缺陷，与草稿问题 4 相同。

## Revision Suggestions

**Before 1**：The result was significant (t = 3.45, p < 0.05).
**After 1**：Stress scores decreased significantly from pre-test (*M* = 4.82, *SD* = 1.03) to post-test (*M* = 3.91, *SD* = 1.12), *t*(df) = 3.45, *p* = .0XX, *d* = X.XX, 95% CI [X.XX, X.XX].（df、精确 p、效应量与 CI 请据实补全；依据 B-01、B-11）

**Before 2**：There was a significant difference between the three groups (F = 8.76, p = .000).
**After 2**：A one-way ANOVA revealed a significant effect of view type on attention restoration, *F*(2, df) = 8.76, *p* < .001, partial η² = .XX. Post hoc comparisons showed that the green view group (*M* = 5.12, *SD* = X.XX) scored significantly higher than the built view group (*M* = 4.03, *SD* = X.XX) and the mixed view group (*M* = 4.55, *SD* = X.XX), *p* < .05.（依据 B-01、B-13、B-14）

**Before 3**：The correlation between preference and restoration was significant (p < 0.01).
**After 3**：Preference was positively correlated with restoration, *r*(df) = .XX, *p* < .01.（依据 B-12；若为 Spearman 相关则写 *r*s）

**Before 4**：For skin conductance, there was no significant difference between groups (n.s.).
**After 4**：There was no significant group difference in skin conductance, *F*(2, df) = X.XX, *p* = .XX.（依据 B-02）

**Before 5**：The effect of view type on mood was slightly significant (p < 0.1).
**After 5**：The effect of view type on mood was marginally significant, *F*(2, df) = X.XX, *p* = .0X（报告精确 p 值并标注 "marginally significant"；不得表述为 significant；依据 B-04）

**Before 6**：the green view group showed lower values (62.3 ± 2.1 bpm) ... the difference was 12.9%.
**After 6**：The green view group showed lower heart rate (*M* = 62.3, *SD* = 2.1 bpm) than the built view group (*M* = 71.5, *SD* = 1.8 bpm), *t*(df) = X.XX, *p* = .XXX, *d* = X.XX.（先界定 ± 为 SD 或 SEM，再做检验；依据 B-03、B-10）

**Before 7**：According to the data analysis, most participants felt more relaxed after viewing the green view.
**After 7**：删除或补全统计支撑：报告放松评分的 *M*、*SD* 及相应检验结果；无法补统计时不做 "most participants felt" 式断言。（依据 B-09）

## Priority Level

**高**（问题 1—4 须优先修改）：统计量缺自由度与 p 值违规属于硬伤，直接影响结果的可复核性；建议先补全所有 t/F/r/β 的自由度与统计量、修正 p 值写法、为 "12.9%" 断言补充检验，再补效应量与 95% CI（问题 5—6），最后统一格式细节（问题 7—9）。问题 10 的 claim 强度部分建议转交 results-claim-hedging-checker 处理。
