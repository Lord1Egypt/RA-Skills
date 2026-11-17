---
name: results-vocabulary-lexis-advisor
description: 用于诊断英文心理学论文 Results 部分的学术词汇与搭配质量，包括口语化表达识别、学术动词准确性、图表邀请语规范性、结果描述词恰当性、术语一致性和搭配自然度。本 Skill 是 Results 写作诊断总 Skill 的第 4 个子 Skill（成员 D），在 results-structure-diagnoser（A）、results-statistics-convention-checker（B）、results-tense-grammar-checker（C）之后执行。
---

# results-vocabulary-lexis-advisor（成员 D）

## 1. Name

`results-vocabulary-lexis-advisor`

## 2. Description

诊断英文心理学论文 Results 部分的学术词汇（vocabulary）与搭配（lexis/collocation）是否准确、规范、自然。覆盖六个子维度：

1. **口语化表达**：是否存在不符合学术语域的口语词、缩略形式、模糊量词等；
2. **学术动词**：结果报告动词（show / reveal / indicate / demonstrate / yield / find / observe 等）的语义强度与证据类型是否匹配；
3. **图表邀请语**：Figure / Table 的引出方式是否符合期刊规范；
4. **结果描述词**：significant / robust / consistent / marginal 等限定词的使用精度；
5. **术语一致性**：核心构念、变量名、缩写是否全文统一；
6. **搭配自然度**：动词-名词、形容词-名词、介词搭配是否符合学术英语习惯（如 main effect of, associated with, interaction between A and B）。

## 3. When to use

- 用户提供 Results 草稿，希望检查用词是否学术化、是否存在口语化表达；
- 用户不确定某个结果动词是否准确（如该用 show 还是 demonstrate / prove）；
- 用户需要检查图表引用句式是否规范（Figure X shows? see Figure X? as can be seen?）；
- 用户希望检查术语是否全文一致（如 executive attention 与 executive control 混用）；
- 用户需要检查搭配是否自然（如 "do a significant difference"、"make an interaction" 等中式搭配）；
- 总 Skill（Results 写作诊断流程）执行到第 4 步时，由本 Skill 接管词汇维度。

## 4. When not to use

- 不用于诊断 Introduction / Method / Discussion（虽然部分规则可迁移，但 examples 库仅针对 Results 语域）；
- 不检查统计符号格式、效应量是否报告（那是成员 B 的职责；本 Skill 只看词汇层面，如 "significant" 一词的使用精度）；
- 不检查时态、主谓一致、句法错误（那是成员 C 的职责）；
- 不判断 claim strength 与证据匹配度、hedging 是否充分（那是成员 F 的职责；本 Skill 只标记动词强度问题并转介）；
- 不检查段落衔接与连贯（成员 E）；
- 不负责全文翻译或整篇润色。

## 5. Inputs

必需：

- **Results 草稿**（英文，纯文本或 docx 粘贴内容）；
- **研究领域或论文主题**（用于判断术语使用是否符合领域惯例）。

建议提供：

- 研究假设 / 研究问题（帮助判断结果描述词与假设的对应）；
- 图表清单或统计结果（帮助核对图表邀请语是否与实际图表对应）；
- 目标期刊或格式要求（默认 APA 第 7 版）；
- 上游 Skill 的诊断结果（A/B/C 的输出，避免重复报告已诊断问题）。

## 6. Workflow

1. **确认输入范围**：确认文本属于 Results 部分；若混入 Discussion 解释性段落，标记并只对结果报告句做词汇诊断。
2. **读取 examples 库**：加载 `references/examples/` 下四个文件（图表邀请语、学术动词、结果描述词、术语一致性），作为正例与可复用表达的比对基准。
3. **按 checklist 逐项扫描**：依据 `references/checklist.md` 的六大子维度逐项检查，对每个命中问题记录：原句 → 问题类型 → 严重程度。
4. **example 调用逻辑**：
   - 发现口语化/不自然表达时，从 examples 中检索同语义场景的正例，给出 Before / After；
   - 发现动词强度不匹配时，引用 examples 中的动词分级规则（见下）；
   - 发现术语不一致时，引用 examples 中"术语锁定"规则并列出全文中所有变体；
   - 没有命中问题的维度，引用 1 条正例确认该维度达标。
5. **按 rubric 评分**：依据 `references/rubric.md` 给出 1—5 分，并写明评分理由。
6. **输出结构化报告**：按 §8 格式输出，确保成员 G（汇总 Skill）可直接整合。

### 动词强度分级规则（诊断核心依据）

| 强度 | 动词 | 适用证据 |
|---|---|---|
| 强 | demonstrate, establish, confirm | 多研究收敛证据、严格控制的因果设计 |
| 中 | show, reveal, find, yield, indicate | 单个实证研究的直接统计结果 |
| 弱 | suggest, appear to, seem to, be associated with, be related to | 相关设计、边缘结果、机制推测 |
| 禁用 | prove, obviously, clearly（修饰因果时）, certainly | 任何单一研究结果 |

诊断规则：**相关/横断面证据 + 强因果动词 = 问题**；**零结果 + "no effect at all" 类绝对化表达 = 问题**；应替换为 examples 中的对应强度表达。若动词强度问题涉及 claim 与证据匹配，标记后转介成员 F，不在本 Skill 内展开。

## 7. Scoring Rubric

采用 1—5 分制（详细锚点见 `references/rubric.md`）：

- **5 分**：词汇全面学术化，动词强度与证据匹配，图表邀请语规范，术语全文一致，无口语化表达，无中式搭配；
- **4 分**：整体规范，个别动词可升级/降级，或存在 1—2 处轻微搭配不自然；
- **3 分**：基本可读，但有明显问题：如多处 "a lot of / big / get" 类口语词，或术语存在 2 种以上变体，或图表引用句式混乱；
- **2 分**：口语化严重，动词强度频繁失配（如相关研究用 prove/demonstrate），术语漂移影响理解，需大幅修改；
- **1 分**：词汇层面完全不符合学术 Results 要求，需重写。

## 8. Output Format

```markdown
## Dimension Score
评分：X / 5（一句话理由）

## Key Problems
按严重程度排序的问题清单，每条标注子维度（口语化/动词/图表邀请语/描述词/术语/搭配）。

## Evidence from Draft
逐条引用原文句子，标注问题位置。

## Example-based Comparison
每个问题对照 references/examples/ 中的正例（给出 Example ID 与原句）。

## Revision Suggestions
每条问题给出 Before / After 修改示例与可复用规则。

## Priority Level
高（影响学术规范性/引起误解）/ 中（影响表达质量）/ 低（润色级）。

## Handoff Notes
需转介其他成员的问题（如动词强度→成员 F；统计格式→成员 B；时态→成员 C）。
```

## 9. Limitations

- 不替代统计判断：不验证统计量数值正确性；
- 不判断实验设计与因果推断是否合理（只做词汇强度标记并转介成员 F）；
- 不负责全文翻译、不直接生成完整 Results 段落；
- examples 库来自 8 篇心理学经典论文（注意网络、认知评估、环境心理学/恢复性环境方向），对高度专业化的其他子领域（如心理计量建模），搭配惯例可能需要补充领域语料；
- 仅针对 Results 部分提供词汇与搭配诊断建议，最终修改由用户决定。

## 10. Examples 库说明

`references/examples/` 按子维度分四个文件，共 40+ 条从以下 8 篇论文提取的 example：

1. Posner & Petersen (1990), *Annual Review of Neuroscience*
2. Johnson et al. (2021), *Journal of Environmental Psychology*
3. Harvey (2019), *Dialogues in Clinical Neuroscience*
4. Toba et al. (2024), *Neuropsychology Review*
5. Song et al. (2022), *International Journal of Environmental Research and Public Health*
6. Chen et al. (2020), *Journal of Environmental Psychology*
7. Rhee et al. (2023), *Scientific Reports*
8. Wang, Lin & Lin (2025), *Frontiers in Forests and Global Change*

每条 example 含：Example ID / Source / Dimension / Type / Original Sentence / Why it is useful / Reusable Rule / Possible Application。
