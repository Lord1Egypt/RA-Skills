---
name: results-cohesion-flow-checker
description: >-
  Diagnose and score cohesion & flow writing quality in the Results section of
  English psychology/neuroscience papers. Use when checking or reviewing a
  Results section for: (1) connectives and transitions, (2) sentence-to-sentence
  cohesion (reference chains, lexical recurrence), (3) paragraph coherence
  (topic sentences, paragraph progression, closing sentences), and
  (4) information flow (given→new, topic continuity). Produces a per-dimension
  1–5 score report with quoted problem sentences, revision advice, and model
  rewrites drawn from real published examples.
---

# Results Cohesion & Flow Checker

检查英文心理学/神经科学论文 Results 部分的**衔接与连贯（cohesion & flow）**写作质量。
输出四维评分 + 问题定位 + 修改建议 + 基于真实文献例句的示范改写。

## Scope（技能边界）

**本技能检查（四维）：**
1. **连接词与过渡语**（connectives & transitions）：追加/对比/顺承/总结类过渡语的恰当使用
2. **句间衔接**（sentence-to-sentence cohesion）：指代链（this/these/such + 名词）、词汇复现与同义复现
3. **段落连贯**（paragraph coherence）：主题句、段落推进逻辑、段末收束句
4. **信息流**（information flow）：given→new 排序、话题延续（topic continuity）

**本技能不检查**（发现时在报告末尾以一句话「转介」，不扣分）：
- 篇章结构/小节组织 → `results-structure-diagnoser`
- 统计报告与 APA 格式 → `results-statistics-convention-checker`
- 时态与语法 → `results-tense-grammar-checker`
- 学术词汇与搭配 → `results-vocabulary-lexis-advisor`
- Hedging 与过度声称 → `results-claim-hedging-checker`

## Workflow

### Step 1 — 定位并切分 Results 部分
- 在稿件中定位 Results（含 "Results and discussion" 融合节）的起止。
- 按小节标题（subsection headings）→ 段落 → 句子三级切分，给每个段落编号（P1, P2, …）便于报告定位。
- 若用户只提供片段，则按所给文本切分并在报告中注明范围。

### Step 2 — 逐段做四维诊断
对每个段落，按以下四个维度检查（判定依据与 1/3/5 分锚点详见 `references/rubric.md`）：

**D1 连接词与过渡语**
- 段内/段间是否有显式逻辑标记（Additionally, In contrast, However, Nevertheless, Thus, Taken together…）？
- 过渡语逻辑关系是否与实际一致（警惕 however/therefore 误用）？
- 是否堆砌过渡语或全段无任何过渡标记？
- 对照锚点：rubric.md §D1。

**D2 句间衔接**
- this/these/such 是否带名词（"these scores"、"such effects"）且指代对象明确？
- 关键词是否跨句复现（lexical chain），还是每句换术语造成断裂？
- 缩写是否先定义后使用，关系从句（which…）指代是否清晰？
- 对照锚点：rubric.md §D2。

**D3 段落连贯**
- 每段首句是否为主题句，明示本段分析目的（"To test whether…, we conducted…" / "Next, we examined…"）？
- 段内句子是否服务于该目的（总→分、总体关联→分解检验）？
- 段末是否有收束句（"Taken together…" / "These results support our hypothesis that…"）？
- 对照锚点：rubric.md §D3。

**D4 信息流**
- 句首是否优先放旧信息（given），新信息置于句尾（new）？
- 相邻句是否保持话题延续（同题链），新话题开启时是否有过渡标记？
- 是否存在"新信息出现在句首"造成的话题断裂？
- 对照锚点：rubric.md §D4。

### Step 3 — 对照清单逐项打勾
加载 `references/checklist.md`，对全文逐项核对（每项可判定为 通过/不通过/不适用），
统计各维度未通过项，作为 Step 4 评分的依据之一。

### Step 4 — 输出诊断报告
按 `assets/report_template.md` 输出：
- 总体评分表（四维各 1–5 分；评分对照 `references/rubric.md` 锚点）
- 逐维诊断：问题列表按「原文引用 → 问题说明 → 修改建议 → 示范改写」呈现
- 示范改写优先从 `references/examples.md` 选取**最接近的正例**作为范式（保留其溯源标注），
  也可参照 examples.md 中的「问题句 → 修改后」constructed 对照
- 报告末尾：转介提示（属于其他技能的问题）+ 修改优先级排序（高/中/低）

## When to load reference files

| 文件 | 加载时机 |
|---|---|
| `references/rubric.md` | Step 2 诊断打分前必读；需要 1/3/5 分锚点描述和扣分项清单 |
| `references/checklist.md` | Step 3 逐项核对时加载 |
| `references/examples.md` | Step 4 撰写示范改写时按需检索对应维度的正例 |
| `assets/report_template.md` | Step 4 输出报告时加载，严格按模板结构填写 |

## Notes（中文提示）
- 所有示范改写的正例必须来自 `references/examples.md`（例句逐字取自 8 篇真实论文 Results，含溯源标注），禁止编造。
- 构造的问题句仅用于对照教学，报告中引用时须标注 "constructed example"。
- 评分锚点：5 = 优秀范例水平（接近 notes 中例句），3 = 合格，1 = 严重问题。
