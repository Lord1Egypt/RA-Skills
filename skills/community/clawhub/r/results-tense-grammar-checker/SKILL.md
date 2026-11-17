# SKILL.md — results-tense-grammar-checker


---

## 2.1 Name

name: results-tense-grammar-checker

---

## 2.2 Description

description: 用于诊断英文心理学论文 Results 部分的时态（tense）、语法（grammar）和句法（syntax）问题，包括一般过去时与一般现在时的使用是否合理、主谓一致、冠词、句子片段、run-on sentence 与平行结构，并基于 8 篇权威期刊实证论文的 examples 提供诊断依据与修改建议。

---

## 2.3 When to use

- 用户需要检查 Results 部分的时态使用是否合理（如描述本研究结果是否误用一般现在时）；
- 用户提供 Results 草稿，希望诊断语法、句法问题（主谓一致、冠词、句子片段、run-on、平行结构）；
- 用户需要判断图表引用句的时态（Figure X shows…）与结果报告句的时态（过去时）是否规范；
- 用户希望对照权威期刊论文的规范写法，获得可执行的修改建议；
- 用户需要按统一格式输出诊断报告，供汇总 Skill（results-summary-report-generator）整合。

---

## 2.4 When not to use

- 不用于诊断 Introduction、Method、Discussion 等其他论文模块；
- 不负责统计计算本身（p 值、效应量是否正确不属于本 Skill 职责）；
- 不检查统计报告格式是否符合 APA（如 M、SD、t、F 的格式，属于 results-statistics-convention-checker）；
- 不负责学术词汇、搭配选择（属于 results-vocabulary-lexis-advisor）；
- 不负责全文润色或全文翻译；
- 不直接生成完整论文；
- 不判断实验设计是否合理。

---

## 2.5 Inputs

- Results 草稿（必填）；
- 研究领域或论文主题（选填，用于判断领域共识类现在时陈述）；
- 研究类型（实验 / 问卷 / 纵向 / 元分析，选填，影响时态判断场景）；
- 图表或统计信息（选填，用于核对图表引用句）；
- 目标格式（如 APA 风格，默认 APA）。

---

## 2.6 Workflow

1. **识别输入**：确认用户输入是否属于 Results 部分；若为其他模块，提示不在本 Skill 范围。
2. **读取 examples**：按诊断维度读取 references/examples/examples_memberC.md 中的对应例句（时态→C-T 系列，主谓一致→C-S 系列，冠词→C-A 系列，平行结构→C-P 系列，句子片段→C-F 系列，run-on→C-R 系列）。
3. **逐项检查**：按 references/checklist.md 顺序检查：
   a. 时态（描述本研究结果是否用过去时；图表引用是否用现在时；领域共识是否用现在时；句内时态是否一致）；
   b. 主谓一致（data、复数主语、a series of 等结构）；
   c. 冠词（特指/泛指/首提回指、a + 复数等）；
   d. 句子片段（正文中是否存在无主谓结构的独立句；标题位置除外）；
   e. run-on sentence（两个独立句是否仅以逗号连接；长句连接词是否明确）；
   f. 平行结构（neither…nor…、比较结构、并列列举是否对称）。
4. **对照 examples**：将待测稿中的句子与同维度 examples 对照，判断属于规范用法、可优化用法还是错误。
5. **按 rubric 评分**：依据 references/rubric.md 给出 1–5 分。
6. **输出诊断报告**：按 Output Format 输出，包含问题定位、原因解释、修改建议。
7. **提供 Before / After**：对每个问题给出修改前、修改后示例（必要时引用 examples 中的规范句）。

---

## 2.7 Scoring Rubric

采用 1–5 分制（细则见 references/rubric.md）：

- **5 分**：高度符合 Results 写作规范，时态使用一致且场景正确，无语法、句法错误，几乎无需修改。
- **4 分**：整体规范，仅有少量表达或时态细节问题（如个别句时态不够稳定、冠词小误）。
- **3 分**：基本可用，但有明显问题（如描述本研究结果时混用现在时、存在 run-on 或主谓一致错误）。
- **2 分**：问题较多，影响可读性和学术规范性（时态混乱、多处语法错误、句子结构破碎）。
- **1 分**：严重不符合 Results 写作要求，需要大幅重写（时态全程混乱、语法错误频发、无法形成有效诊断）。

评分时按维度加权参考：时态权重最高（Results 时态规范是本 Skill 核心），其次主谓一致与 run-on（影响可读性），再次冠词、平行结构、句子片段。

---

## 2.8 Output Format

诊断输出统一采用以下结构：

```
## Dimension Score
评分（1–5）：[分数]
分维度说明：Tense（x/5）｜Subject-Verb Agreement（x/5）｜Articles（x/5）｜Parallel Structure（x/5）｜Sentence Fragment（x/5）｜Run-on（x/5）

## Key Problems
主要问题：[按严重程度列出 2–5 项]

## Evidence from Draft
原文证据：[从用户草稿中引用问题句，标注位置]

## Example-based Comparison
与 examples 的对照：[引用 examples_memberC.md 中对应例句（如 C-T01）及规范写法]

## Revision Suggestions
修改建议：[针对每个问题给出具体修改，含 Before / After]

## Priority Level
修改优先级：[高 / 中 / 低，说明理由]
```

---

## 2.9 Limitations

- 本 Skill 仅针对 Results 部分的写作语言提供诊断建议，不替代统计计算、不判断实验设计是否合理；
- 不负责整篇论文的翻译与润色；
- examples 中的问题例（Problem Example）来自权威期刊原文的真实疏漏，不代表该论文整体质量，仅用于说明"期刊发表 ≠ 语言完美"；
- 时态判断依赖研究类型与上下文，若用户未提供研究类型，诊断按通用 APA 规范执行；
- 本 Skill 默认目标为英文论文 Results；中文论文的时态/语法问题不在本版范围内；
- 输出供 results-summary-report-generator 整合，不直接生成最终论文。
