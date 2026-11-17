---
name: results-statistics-convention-checker
description: 用于诊断英文心理学论文 Results（结果）部分的统计报告规范，检查 M、SD、t(df)、F(df1, df2)、p 值、效应量（Cohen's d、partial η²、r 等）、置信区间的报告格式与完整性，以及统计结果与文字描述的一致性，判断是否符合 APA 风格统计报告习惯。当用户提供 Results 草稿并希望检查统计报告格式、补充效应量或置信区间、核对统计量与文字描述是否一致、或需要按 APA 格式改写统计结果陈述时触发本 Skill。仅针对 Results 部分的统计报告写作规范，不替代统计计算本身。
---

# results-statistics-convention-checker

## 1. Name

`results-statistics-convention-checker`

## 2. Description

用于诊断英文心理学论文 Results 部分的统计报告规范性，包括：

- M、SD 的描述统计格式是否一致、完整；
- t(df)、F(df1, df2)、χ²(df)、r、β 等统计量的报告格式是否规范；
- p 值的报告方式是否规范（精确 p 值 vs. 阈值报告、前导零、p = .000 等）；
- 是否报告效应量（Cohen's d、partial η²、r、β 等）；
- 是否需要补充置信区间（95% CI）；
- 统计结果与文字描述是否一致（数据、方向、显著性结论）；
- 是否符合常见 APA 风格统计报告习惯（斜体、空格、小数位、自由度）。

## 3. When to use

- 用户提供 Results 草稿，希望检查统计报告格式是否符合 APA 规范；
- 用户需要确认 t、F、p、χ²、r 等统计量是否报告完整（含自由度）；
- 用户希望判断是否需要补充效应量或置信区间；
- 用户需要核对统计数值与文字描述（如“显著提高”）是否一致；
- 用户需要把不符合规范的统计陈述改写成规范的 APA 格式；
- 用户想了解优秀心理学论文 Results 中的统计报告范例。

## 4. When not to use

- 不用于诊断 Abstract、Introduction、Method、Discussion 部分；
- 不负责统计计算本身（不重新计算 t、F、p，不验证数值正误）；
- 不判断实验设计、统计方法选择是否合理（那是 Method 维度）；
- 不负责时态、语法、词汇、衔接、hedging 等其他维度的诊断（由组内其他 Skill 负责）；
- 不负责整篇论文全文润色或翻译；
- 不处理纯定性研究（无统计报告可检查）。

## 5. Inputs

用户需提供：

- **Results 草稿**（必需）：英文 Results 部分的完整文本或相关段落；
- **研究领域或论文主题**（建议提供）：便于判断统计惯例是否符合领域习惯；
- **研究假设或研究问题**（建议提供）：用于核对统计结果是否回应假设；
- **图表或统计信息**（如有）：用于核对文中统计量与图表数据是否一致；
- **目标格式**（可选）：默认 APA 第 7 版；如目标期刊有特殊要求请说明。

## 6. Workflow

1. **识别输入**：确认用户提供的文本属于 Results 部分；若不属于，提示用户并停止诊断。
2. **提取统计陈述**：逐句找出草稿中所有统计报告句，标记其中的统计元素（M、SD、t、F、p、效应量、CI、χ²、r、β 等）。
3. **读取 examples**：读取 `references/examples/examples_memberB.md`，调取对应统计类型的正例与问题例作为诊断依据。
4. **逐项检查**：按 `references/checklist.md` 的检查清单逐项核对：
   - 描述统计：M、SD 是否成对出现、格式是否一致；
   - 推断统计：t、F、χ² 等是否带自由度，统计量符号是否斜体；
   - p 值：是否报告精确 p 值（或规范的阈值报告），是否存在 p = .000、p < 0.1 当显著等问题；
   - 效应量与置信区间：是否报告，是否解读；
   - 一致性：文中数值与图表、文字结论与统计结果是否一致。
5. **对照评分**：按 `references/rubric.md` 的 1—5 分标准给出本维度评分。
6. **输出报告**：按统一输出格式给出问题定位、原因解释、修改建议，必要时提供 Before / After 示例，并引用 examples 编号作为依据。

## 7. Scoring Rubric

采用 1—5 分制，细则见 `references/rubric.md`：

- **5 分**：统计报告高度规范——描述统计完整、推断统计含自由度、报告精确 p 值与效应量、必要处有置信区间、文表一致；
- **4 分**：整体规范，仅有少量格式问题（如个别空格、斜体缺失）；
- **3 分**：基本可用，但有明显缺项（如部分结果缺效应量、个别统计量缺自由度）；
- **2 分**：问题较多——统计报告缺项多、p 值报告混乱、文表存在不一致；
- **1 分**：严重不符合要求——几乎没有规范的统计报告，无法支撑结论。

## 8. Output Format

```markdown
## Dimension Score
评分：X / 5（统计报告规范维度）

## Key Problems
主要问题：（按严重程度排序，逐条列出）

## Evidence from Draft
原文证据：（摘录草稿中的问题句并标注位置）

## Example-based Comparison
与 examples 的对照：（引用 references/examples/examples_memberB.md 中的 Example ID）

## Revision Suggestions
修改建议：（含 Before / After 示例，给出可直接使用的规范表述）

## Priority Level
修改优先级：高 / 中 / 低（附理由）
```

## 9. Limitations

- 不替代统计计算：不重新计算或验证统计量数值的正确性；
- 不判断实验设计、取样、统计方法选择是否合理；
- 不检查时态、语法、词汇、衔接、hedging 等其他维度；
- 默认以 APA 第 7 版为基准，目标期刊另有规定时从其规定；
- 仅针对 Results 部分提供统计报告写作诊断建议，不直接生成完整论文。

## 10. Bundled Resources

- `references/examples/examples_memberB.md`：从 8 篇心理学论文中提取的统计报告正例、问题例与可复用规则，诊断时按统计类型调取引用；
- `references/rubric.md`：统计报告规范维度的 1—5 分评分细则；
- `references/checklist.md`：逐项检查清单，保证诊断输出稳定、可复现；
- `tests/test_input.md`、`tests/test_output.md`：一组测试输入与对应的标准诊断输出，展示本 Skill 的预期工作方式。
