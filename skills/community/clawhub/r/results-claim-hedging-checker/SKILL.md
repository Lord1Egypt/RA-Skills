---
name: results-claim-hedging-checker
description: "Academic writing revision advisor for the Results section of psychology and STEMM research papers. Checks claim-hedging alignment, causal language appropriateness, statistical reporting completeness, and interpretation boundaries. Triggers when the user asks to review, revise, or check a Results section draft, or mentions hedging, claim strength, overclaiming, or causal language in academic writing."
agent_created: true
---

# Results Claim & Hedging Checker

## Purpose

Diagnose and revise the Results section of psychology / STEMM research papers for five recurring problem types: (1) missing or excessive hedging, (2) claim strength mismatched to statistical evidence, (3) causal language inappropriate for the design, (4) theoretical interpretation leaking into Results, and (5) subjective evaluative language. Produce a sentence-level audit with risk ratings and concrete revision suggestions, grounded in 18 curated examples from 8 classic psychology papers.

## When to Use

- User submits a Results section draft (full or partial) and asks for review or revision.
- User mentions "hedging," "claim strength," "overclaiming," "causal language," or "Results section" in the context of academic writing.
- User asks to check whether their Results section is "too strong" or "too speculative."
- User wants to align their writing with conventions observed in published psychology / STEMM papers.

## When NOT to Use

- Reviewing Introduction, Discussion, or Method sections (different conventions apply).
- General proofreading for grammar, spelling, or formatting (use general editing tools instead).
- Checking the validity of the statistical analysis itself (this skill evaluates *reporting*, not *analysis*).
- Non-academic writing tasks (e.g., blog posts, reports, marketing copy).

## Inputs

- **Required**: A Results section draft in English or Chinese (plain text, Markdown, or a file path to .md/.txt/.docx).
- **Optional**: The paper's research design (experimental, correlational, cross-sectional, longitudinal) — improves causal-language diagnosis accuracy.
- **Optional**: Target journal or style guide (e.g., APA 7th) — adjusts formatting expectations for statistical reporting.

## Workflow

### Step 1 — Parse and Segment

1. Read the submitted Results draft.
2. Split the text into individual sentences or minimal clause-level units. Each unit becomes one diagnostic record.
3. Tag each unit with its sequential position (e.g., S1, S2, S3 …) for traceability.

### Step 2 — Classify Each Unit

For every sentence, check against the five diagnostic dimensions. A sentence may trigger more than one dimension.

| Dimension | What to detect | Reference examples |
|---|---|---|
| **D1. Hedging** | Missing hedging where indirect evidence is used; or excessive hedging that undermines clear findings | F-01, F-05, F-07, F-09, F-16 |
| **D2. Claim Strength vs. Evidence** | Overclaims beyond what the statistics support; strong claim words ("strong evidence," "robust finding") used without corresponding evidence; causal leaps from correlational data | F-03, F-10, F-15 |
| **D3. Causal Language** | Strong causal verbs ("caused," "produced," "leads to," "determines") used when design does not support causal inference, or even when it does but Results convention favors neutral phrasing | F-06, F-11, F-13 |
| **D4. Interpretation in Results** | Theoretical mechanisms, "because" explanations, hypothesis restatements, or discussion-level conclusions appearing in Results | F-04, F-08, F-12, F-18 |
| **D5. Subjective / Evaluative Language** | Evaluative adjectives ("instructive," "conspicuous," "remarkable"), subjective hedges ("It is helpful to consider," "Interestingly,"), or absolute expressions ("leave no room for doubt," "prove") | F-02, F-14, F-15, F-17 |

### Step 3 — Score Each Unit

Apply the scoring rubric (below) to assign a **1—5 分** per dimension per sentence（**5 分为最高，1 分为最低**）。如果某个维度没有问题，该维度应得 **5 分**。不得在输出中使用"2 分 / Pass"这种含糊表述——直接给出 1—5 的数字分数。如果某句在所有五个维度上均为 5 分，则该句无需出现在报告中（除非用户要求全文审计）。

### Step 4 — Generate Revision Suggestions

For each flagged sentence:

1. Quote the original text.
2. State the diagnosed problem and the dimension it falls under.
3. Provide a concrete revision suggestion — not just "add hedging" but the actual revised sentence.
4. If available, cite the matching reference example (by Example ID) and the reusable rule extracted from it.

### Step 5 — Compile Output

Assemble all diagnostic results into the output format specified below. **最终输出必须严格使用以下六个标题，不得使用其他自定义标题**（`Dimension Score` / `Key Problems` / `Evidence from Draft` / `Example-based Comparison` / `Revision Suggestions` / `Priority Level`），以便汇总 Skill 统一整合各子 Skill 的诊断结果。不得添加额外的自定义标题或省略任何一个标准标题。

**Dimension Score 部分必须**：
1. 先给出 D1—D5 每个维度的分数（1—5 分，5 分为最高）。
2. 再给出一个**总体分**（1—5 分），综合各维度评分得出。
3. 附一句话总评。
4. 如果用户草稿质量较高（各维度均为 5 分或仅有轻微风格问题），总体分应相应较高（4 分或 5 分）。
5. Summary 中不得出现"2 分 / Pass"的标记——直接使用 1—5 的数字分数。

## Scoring Rubric

每个维度采用 **1—5 分制，5 分为最高（无问题），1 分为最低（严重问题）**。每个维度独立评分后，综合各维度给出一个总体分（1—5 分），并附一句话总评。

| 分值 | 含义 | 行动要求 |
|------|------|---------|
| **5** | 无问题：声称强度与证据匹配，hedging 恰当，因果语言与设计一致，无理论解释渗入，无主观评价词 | 无需修改 |
| **4** | 轻微：风格偏好层面的微小问题，不影响科学准确性 | 可选修改；低优先级 |
| **3** | 中度：声称略超出证据支持，或 hedging 缺失/过度 | 建议修改；说明原因 |
| **2** | 较严重：因果语言与设计不匹配，或相关数据写成因果断言，或 Results 中出现理论解释 | 推荐修改；解释误导风险 |
| **1** | 严重：绝对化断言（prove, definitely），因果跳跃严重，使用强动词且无对应证据 | 必须修改；解释误导风险 |

> **注意**：如果某个维度没有问题，该维度应得 **5 分**，不得使用"Pass""2 分 / Pass"等含糊表述。

### Dimension-Specific Criteria

**D1 — Hedging**
- 5: hedging 使用恰当，既不过度也不缺失。
- 4: hedging 略弱或略强，属风格偏好。
- 3: 间接证据（中介、机制、观察数据）处缺少 hedging。
- 2: 相关数据上直接因果断言且零 hedging。
- 1: 无任何 hedging 的绝对化因果断言。

**D2 — Claim Strength vs. Evidence**
- 5: 所有声称都有充分的统计证据支持，声称强度与证据匹配，无过度声称或因果跳跃。
- 4: 声称强度与证据基本匹配，仅有微小风格问题。
- 3: 部分声称强度略超出证据支持（如使用 "strong evidence" 但未提供效应量或置信区间，或从相关结果推断因果）。
- 2: 声称明显超出证据支持（如使用 "robust finding" 但统计证据薄弱，或相关数据写成因果断言）。
- 1: 大量声称缺乏证据支持，因果跳跃严重，使用 "prove""cause""definitely" 等强动词且无对应证据。

> **职责边界**：本维度不负责统计报告格式的完整性检查（如效应量、置信区间的具体格式）。单纯缺少效应量或置信区间且未使用强声称词时，不作为扣分项。

**D3 — Causal Language**
- 5: 因果语言与设计类型完美匹配，或主动声明不可做因果推断。
- 4: 真实验中使用 "resulted in" 等略强动词，可更中性但非错误。
- 3: 准实验或观察性数据中使用 "leads to""causes" 等因果词。
- 2: 横断面相关数据上使用 "caused""produced""determined" 等强因果词。
- 1: 观察性数据上使用绝对化因果断言且无任何限制声明。

> **行为用法豁免**：当触发词（如 "produced"）用于描述被试行为（如 "participants produced responses"）而非因果推断时，不视为问题，该维度记 **5 分**。

**D4 — Interpretation in Results**
- 5: 纯数据报告，无理论解释渗入；混淆变量处主动声明限制。
- 4: 单句中嵌有一个简短的理论从句，但不影响整体报告性质。
- 3: 完整的 "because X … therefore Y" 解释句出现在 Results 中。
- 2: 段落级别的理论讨论或假设重述出现在 Results 中。
- 1: Results 中出现结论性总结 + 理论解释，完全偏离结果报告。

**D5 — Subjective / Evaluative Language**
- 5: 用词完全客观，无评价性语言或绝对化表达。
- 4: 单个评价性形容词（如 "interesting"）出现在其他客观的句子中。
- 3: 主观引导语（如 "It is instructive to …""It is helpful to consider …"）。
- 2: 评价性形容词与主观框架组合使用。
- 1: 绝对化表达（如 "leave no room for doubt""proved""definitely"）+ 主观框架。

## Output Format

最终输出**必须严格使用以下六个标题**，不得使用其他自定义标题，以便汇总 Skill 统一整合各子 Skill 的诊断结果。

```markdown
# Results Claim & Hedging Audit

## Dimension Score

评分：1—5 分（**5 分为最高，1 分为最低**）。先给出 D1—D5 每个维度的分数，再给出一个总体分，并附一句话总评。不得使用"2 分 / Pass"等含糊表述。

> 示例（高质量草稿，各维度均无问题）：
> - D1 Hedging: 5 分 — hedging 使用恰当，无过度或缺失。
> - D2 Claim Strength vs. Evidence: 5 分 — 声称强度与证据匹配，无过度声称。
> - D3 Causal Language: 5 分 — 因果语言与设计类型匹配，无问题。
> - D4 Interpretation: 5 分 — 纯数据报告，无理论解释渗入。
> - D5 Subjective Language: 5 分 — 用词客观，无评价性语言。
> - **总体分: 5 分** — 草稿质量较高，声称强度与证据匹配，无过度声称或因果跳跃。

> 示例（存在问题的草稿）：
> - D1 Hedging: 3 分 — 间接证据处缺少 hedging。
> - D2 Claim Strength vs. Evidence: 2 分 — 使用 "strong evidence" 但未提供对应统计证据。
> - D3 Causal Language: 4 分 — 因果语言基本匹配，个别动词可更中性。
> - D4 Interpretation: 5 分 — 无理论解释渗入。
> - D5 Subjective Language: 3 分 — 出现 "instructive" 等评价性形容词。
> - **总体分: 3 分** — 存在多处声称-证据不匹配和 hedging 缺失，建议逐句修改。

## Key Problems

主要问题：逐条列出。

> 示例：
> 1. S4 使用 "strong evidence" 但未提供效应量或置信区间支撑。
> 2. S6 的 "produced" 虽在结构启动文献中属惯用行为动词，但匹配 D3 触发词清单。

## Evidence from Draft

原文证据：摘录相关句子。

> 示例：
> - **S4**: "It showed a strong main effect of prime type (Estimate = .56, SE = .16, z = 3.60, p < .001)."
> - **S6**: "Pair-wise comparisons indicated that participants produced fewer DO responses following PO-An primes."

## Example-based Comparison

与 examples 的对照：引用具体 Example ID 并说明对应关系。

> 示例：
> - **S4 vs. F-07**（Elkin et al., 1989）：F-07 使用 "there was evidence of significant superiority" 进行适度 hedging，而 S4 直接使用 "strong"，声称强度超出证据支持。
> - **S6 vs. F-01**（Milgram, 1963）：F-01 使用 "showed signs of" 描述被试行为，是规范的行为描述；S6 的 "produced" 同样用于描述被试行为，属行为用法豁免。

## Revision Suggestions

修改建议：逐句给出可操作的替换方案。

> 示例：
> - **S4 修改前**: "It showed a strong main effect of prime type (Estimate = .56, SE = .16, z = 3.60, p < .001)."
>   **S4 修改后**: "It showed a main effect of prime type (Estimate = .56, SE = .16, z = 3.60, p < .001)."
> - **S6 修改前**: "participants produced fewer DO responses following PO-An primes"
>   **S6 修改后**: "participants gave fewer DO responses following PO-An primes"

## Priority Level

修改优先级：按高、中、低排列。

> 示例：
> - **高**: S4 — 强声称词 "strong" 缺乏证据支撑，可能误导读者高估效应大小。需删除 "strong" 或补充效应量。
> - **中**: S6 — "produced" 触发 D3 但属行为用法豁免，替换为 "gave" 可消除歧义，非必须。
> - **低**: 全文风格统一性检查，建议后续通读确认所有声称词与证据匹配。
```

## Reference Files

- `references/examples/examples_memberF.md` — 18 curated examples (F-01 ~ F-18) from 8 classic psychology papers. Load this file before generating revision suggestions to match user sentences against canonical patterns.
- `references/rubric.md` — (Placeholder) Extended scoring rubric with domain-specific rules.
- `references/checklist.md` — (Placeholder) Pre-submission checklist for authors.

## Limitations

1. **Domain scope**: Examples are drawn from classic psychology papers (social, clinical, developmental, cognitive). Conventions in other STEMM fields (e.g., genomics, neuroscience) may differ; apply judgment.
2. **Language scope**: Optimized for English academic writing. Chinese-language Results sections follow related but distinct conventions; use with caution.
3. **Statistical analysis validity**: This skill evaluates *how results are reported*, not *whether the analysis is correct*. It cannot detect p-hacking, violations of assumptions, or inappropriate tests.
4. **Design inference**: If the user does not provide the research design, causal-language diagnosis (D3) defaults to conservative — flagging any strong causal verb. Provide design information for more accurate scoring.
5. **False positives**: Sentences that legitimately summarize results at the end of a Results subsection may be flagged for D4 (Interpretation). Use human judgment to distinguish concluding summaries from theoretical discussion.
6. **Example coverage**: The 18 examples cover five dimensions but do not exhaust all possible Results-section issues (e.g., table/figure referencing, negative-result reporting, replication language). Expand the example set as needed.
7. **Statistical reporting format is out of scope**: 本 Skill 不负责统计报告格式检查，包括效应量、置信区间的具体报告格式和完整性。这些由 `results-statistics-convention-checker` 负责。
8. **D2 仅在强声称与证据不匹配时触发**: 本 Skill 仅在作者使用强声称词（如 "strong effect""clear evidence""robust finding""definitely"）却未提供相应统计证据时，从 claim strength 与证据匹配的角度进行提示。如果结果本身未使用强声称，单纯缺少效应量或置信区间**不应**作为本 Skill 的扣分项。
9. **D3 触发词的行为用法不扣分**: 当触发词（如 "produced"）用于描述被试行为（如 "participants produced responses"）而非因果推断（如 "the prime produced the effect"）时，不应视为问题。判定关键在于主语是否为实验操纵变量及其是否暗示因果关系。
