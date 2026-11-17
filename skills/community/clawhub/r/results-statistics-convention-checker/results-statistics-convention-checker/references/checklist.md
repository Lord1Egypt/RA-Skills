# Checklist：统计报告规范逐项检查表

诊断时按以下清单逐项核对。每项标注 ✅（通过）/ ⚠️（部分通过）/ ❌（不通过），不通过项必须进入诊断报告的 Key Problems。

## A. 范围确认

- [ ] A1 只诊断 Results 部分？（Introduction/Method/Discussion 中的统计内容不纳入本 Skill 诊断）
- [ ] A2 只检查统计报告的**写作规范**，未越界评价统计方法选择或实验设计？

## B. 描述统计

- [ ] B1 所有组间比较是否都报告了 M 与 SD（或 Mdn）？
- [ ] B2 M、SD 的格式是否全文一致（如统一 "M = 4.51, SD = 0.98"）？
- [ ] B3 使用 "X ± Y" 时是否界定 Y 为 SD 或 SEM？（对照 B-03、B-07）
- [ ] B4 百分比、频数报告是否辅以必要的描述统计，而非孤立出现？（对照 B-09）

## C. 推断统计格式

- [ ] C1 t 检验是否报告 t(df) = 值？（对照 B-11）
- [ ] C2 F 检验是否报告 F(df1, df2) = 值？（对照 B-01、B-07）
- [ ] C3 χ² 是否带 df？SEM 是否报告 χ²、df 及多个拟合指数（CFI、RMSEA、SRMR 等）？（对照 B-05）
- [ ] C4 相关是否报告 r（或 rs/ρ）数值与 p？Spearman 是否与 Pearson 符号区分？（对照 B-12）
- [ ] C5 回归/路径系数是否报告标准化 β、p 及 R²/解释方差？（对照 B-06）
- [ ] C6 统计符号（t、F、p、M、SD、r、d）是否斜体、空格规范（p < .05 而非 p<0.05）？

## D. p 值报告

- [ ] D1 是否报告精确 p 值（p = .02）或规范的阈值报告（p < .001）？
- [ ] D2 是否存在 p = .000 的写法？（应改为 p < .001，对照 B-14）
- [ ] D3 前导零使用是否统一（APA：.05，统计量不可能大于 1 时不加前导零）？
- [ ] D4 不显著结果是否同样报告完整统计量与精确 p？（对照 B-02）
- [ ] D5 0.05 < p < .10 的结果是否标注 "marginally significant" 而非 "significant"？（对照 B-04、B-08）

## E. 效应量与置信区间

- [ ] E1 主要效应是否报告效应量（Cohen's d、partial η²、r、β 等）？（对照 B-13）
- [ ] E2 效应量是否有大小解读（small/medium/large）？
- [ ] E3 关键比较是否报告 95% CI（正文或表格）？（对照 B-11）
- [ ] E4 成组 t 检验表格是否含 t、df、p、95% CI 完整列？（对照 B-11）

## F. 一致性核对

- [ ] F1 文中统计数值与表格/图中数值是否一致？
- [ ] F2 文字结论（significant / higher / improved）与统计结果方向是否一致？
- [ ] F3 "significantly higher" 类断言是否有检验支撑？（对照 B-10）
- [ ] F4 统计结果是否与研究假设对应（如标注 H1/H2）？（对照 B-06）
- [ ] F5 Results 中是否混入原因解释（应移至 Discussion 的内容是否提示用户）？（对照 B-10）

## G. 输出规范

- [ ] G1 是否有明确的问题定位（引用草稿原句）？
- [ ] G2 是否引用了 examples 编号（如 B-01、B-08）作为诊断依据？
- [ ] G3 是否给出 Before / After 示例？
- [ ] G4 是否说明各问题的严重程度与修改优先级？
- [ ] G5 修改建议是否具体可操作（给出可直接使用的规范句式，而非"请规范统计格式"式空泛建议）？
- [ ] G6 是否按 `rubric.md` 完成 1—5 分评分并说明理由？
- [ ] G7 是否按 SKILL.md 第 8 节的结构化格式输出（Dimension Score / Key Problems / Evidence from Draft / Example-based Comparison / Revision Suggestions / Priority Level）？
- [ ] G8 输出是否结构化、可被汇总 Skill（results-summary-report-generator）直接整合？
- [ ] G9 是否避免了重新计算统计量、评价实验设计等越界判断？
