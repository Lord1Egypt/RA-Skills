---
name: tech-content-review-panel
description: Reviews a tech/AI/industry research or in-depth analysis long-form article before publishing, via a fixed eight-role expert panel (target-reader reps, quality gatekeepers incl. fact+originality check, distribution gatekeeper) in an evaluate-then-optimize loop. Applies to tech/AI/data deep-dives, sector judgment and research pieces — not news, marketing, docs, tutorials, or short opinion posts. Trigger when the user asks to 会审/评审/review a finished deep-analysis draft or wants tech content 接近完美/可发布.
version: "1.2.4"
agent_created: true
read_when:
  - "会审 / 评审 / review this article"
  - "多视角挑刺 / 让内容接近完美 / 可发布质量"
  - "tech/AI/行业深度稿成稿后的质量把关"
slug: tech-content-review-panel
displayName: Tech Content Review Panel
description_zh: "技术内容评审委员会：发布前用固定八角色专家小组（目标读者代表、质量门禁含事实与原创检查、分发门禁）以先评估后优化循环，评审技术/AI/行业研究深度长文。"
not_for:
  - Fact-checking a single claim in isolation (use a claim-audit skill instead)
  - Rewriting or restructuring the article itself (review only; revision guidance is advisory)
  - News, marketing copy, documentation, tutorials, or short opinion posts
  - Reviewing content that has no finished draft yet
---

# Tech Content Review Panel

A tech/AI/industry deep-analysis piece aimed at an industry readership and built to establish a professional personal brand is easy to miss with a single perspective. This skill provides a fixed **eight-role expert panel** that reviews a finished draft from multiple angles, giving blunt per-role feedback to push it toward publish-ready quality.

**Design pattern: Evaluator-Optimizer** — the panel evaluates, you revise per the feedback, then re-check to confirm no new problems before finalizing. It is a generate → evaluate → revise loop.

## When to use

**Applies to**: tech / AI / industry research or in-depth analysis **long-form** articles aimed at an industry readership (industry deep-dives, sector judgments, research pieces).
**Does not apply to**: news, marketing copy, product docs, tutorials, or short opinion posts — different goals and criteria mean this panel would mismatch. When such content triggers, tell the user this skill does not apply.

## Review workflow

### Step 1 [Deterministic] Confirm input and applicability
- Confirm there is a finished deep-analysis draft (file path or full text). If none, stop and ask the user to finish a first draft first.
- Judge whether the content type applies (see above). If not, stop and explain.

### Step 2 [LLM] G1 Fact & originality check (gate first — reject if it fails)
- **Facts**: verify every number / company name / date / policy / event. Foundational facts must be verified online with traceable sources. Distinguish confirmed / to-verify / possibly-stale (watch timeliness — do not present old news as new).
- **Originality**: search (WebSearch) the core argument, framework, and signature phrasing to judge whether it is "independently derived / deepened from public views" (keep, add a clarifying line if needed) or "verbatim-similar and needs rewrite" (plagiarism risk). Every "original / first / exclusive" claim must be verified — never assert originality from memory.

### Step 3 [Deterministic] G2 Style red-line scan (reject if not cleared)
- Grep the full text for red-line phrasing (aligned with the user's long-term writing profile `negative_rules`):
  - Contrast structures are no longer an absolute zero-tolerance gate. Allow natural, low-density contrast at judgment points (roughly <=3 occurrences per 6,500 Chinese characters), but reject formulaic repetition, contrast used as filler, and any sentence with an AI-bridge pattern. If a contrast sentence can be stated more directly without losing meaning, prefer the direct version. Never replace one contrast pattern with another during revision.
  - For English, screen `not X but Y`, `rather than`, `instead of`, and similar forms for density and rhetorical function; do not mechanically delete natural comparative language. Also screen translated-syntax English (Chinese-to-English calques: nominalized predicate chains, stacked passives, literal idiom translations, sentence rhythm that reads like a translation rather than originally-written English). The author is not a reliable judge of EN native-ness — this check must happen in review, never left to author self-assessment.
  - Register scan for Chinese (2026-09-16 calibration, mirrors tech-writing-pipeline section 4 register discipline): reject colloquial scenario/dialogue sentences ("没人帮我们画" / "你的下一个同事" — first/second-person conversational staging; subject should be enterprise/org/buyer), reject English-calque nominal predicates ("组织问题没有供应商" = "X has no vendor" translated literally; rewrite as full subject-predicate clause, e.g. "没有供应商能替买方回答组织问题"), reject entertaining hooks and playful endings. Approved baseline: full subject-predicate + abstract verb (翻译/到来/回答) + precise qualification; short sentences allowed, colloquial words not. Rule applies to titles, section headers, and bolded key lines, not just body text.
  - marketing jargon (empower / closed-loop / end-to-end / powerful / significant / substantial / build)
  - self-aggrandizing / inspirational-influencer tone
  - preacher / instructing tone (you should… / I suggest you… / here's what to do)
  - putting down others' arguments (most analyses… / many articles… / everyone assumes…)
  - writing-process meta-info (one-line wrap-up / follow-up question / this piece will… / conclusion first)
  - explicit commercial intent (researcher posture, no pitching)
- Then read through to confirm no AI tone, no judgment-first, no written deflection.

### Step 4 [LLM] R1–R4 Target-reader representatives
- **R1 Technical decision-maker**: decision layer with a tech background in the industry. Picks on: vague generalities, phenomenon without depth, correct conclusions with no information gain.
- **R2 Cross-domain senior expert**: understands both the local and the reader's market. Picks on: assumed simplifications, inaccurate technical details, arrogant perspective.
- **R3 Investor / strategy analyst**: understands business logic but not details. Picks on: hanging judgments without data, logic jumps, absolute conclusions without boundaries.
- **R4 Blunt veteran critic**: zero tolerance for marketing / AI / influencer tone. Picks on: empty clichés, grandstanding, preacher posture, correct-but-useless platitudes.

### Step 5 [LLM] G3 Structure & professional depth assessment
- Against the six depth moves (see `references/depth-playbook.md`), hit at least 3: ① expose assumed causality ② decompose an overused concept with a layered framework ③ find contradictions within the argued object itself ④ place it in historical context ⑤ give a horizontal reference frame ⑥ expose the boundary of the judgment.
- Check structure: judgment-first, no isomorphic template, has a collectable comparison table / framework.

### Step 6 [LLM] T1 Distribution assessment
- **T1 Tech media editor**: understands platform distribution. Rates title hook (has a hook without losing professionalism), opening retention and search-crawlability, screenshot-shareable memorable points, multi-platform fit (WeChat / LinkedIn / Substack each have their own logic).
- Surface the tension with G2 / R4 (hook vs restraint) explicitly; do not force unification.
- **Mandatory native-speaker language pass (2026-09-16 calibration, not optional)**: after the distribution assessment, re-read the full draft as a native speaker of the writing language (Chinese draft → native Chinese reader; English draft → native English reader). Flag every word, collocation, sentence rhythm, or metaphor that reads translated, calqued, or unnatural; run the pipeline's calque lexicon and back-translation test here as a review-stage filter. Findings route to **must-fix**, never optional — this pass exists because the author is not a reliable judge of native-ness (EN native-ness is an author blind spot; EN→ZH calques are author zero-tolerance but still slip through). Language verdict reported separately from distribution verdict.

### Step 7 [LLM] Consolidate and revise
- Grade feedback: must-fix / suggested / optional / for-author-decision (tension items).
- Handle all must-fix and suggested; list options for tension items for the author to decide.

### Step 8 [Deterministic] Re-check
- After revision, re-run Step 2 and Step 3 (facts and red-lines must not introduce new problems from the changes; re-grep red-lines to confirm cleared). If Step 6's native-speaker pass flagged must-fix items, re-read the revised passages the same way to confirm they are cleared.

### Step R [LLM] Post-draft reader-fit test (separate from the eight-role panel)

Run this after a complete draft exists, preferably after the panel revision and before final release. This is a **reading/comprehension test**, not a ninth review role and not a second eight-role panel.

#### R0. Lock the article positioning before testing

Record five items before collecting reader feedback:

- article type and platform;
- primary reader and intended reading task;
- thesis / research question;
- deliberate scope and exclusions;
- depth, length and technicality target.

Reader feedback cannot silently rewrite these locked decisions. If the positioning is still undecided, resolve it first; do not let reader reactions decide the article's subject by accident.

#### R1. Select representative readers, do not always use all roles

Choose 3–4 roles that match the article. Typical options:

- **Domain specialist**: tests terminology, mechanism and technical credibility;
- **Runtime / infrastructure specialist**: tests component ownership, state flow, recovery and implementation boundaries;
- **Enterprise decision-maker**: tests whether the judgment helps architecture, procurement, governance or prioritization;
- **Cross-domain industry reader**: tests whether a non-specialist can understand the core message without flattening the technical content.

Selection is based on the article's positioning. A research report does not automatically need an investor, media editor or general reader; a highly technical piece may prioritize the first two roles and use the fourth only as a comprehension check.

#### R2. Ask each reader the same five questions

1. What is the article's central message in one or two sentences?
2. What technical distinction or mechanism did you take away?
3. Which paragraph or term could make you infer the wrong scope or conclusion?
4. What is missing for the article's stated reading task, not for a different article?
5. After reading, would you trust the article's positioning and continue to the evidence?

Each reader must separate **misunderstanding**, **missing bridge**, **disagreement**, and **different preference**. Do not treat all negative feedback as a defect.

#### R3. Triage feedback by positioning compatibility

Do not average all reader opinions or adopt every suggestion. Classify each item:

- **Must-fix**: the core thesis is misunderstood; a factual/technical statement is misread; scope or subject is wrongly inferred; a necessary transition blocks comprehension; a term is used inconsistently.
- **Suggested**: at least two relevant readers identify the same comprehension barrier, and the fix strengthens the locked reading task without changing thesis, scope or depth target.
- **Optional**: a single reader's preference, a nice-to-have example, an alternate metaphor or a distribution improvement that does not repair misunderstanding.
- **Reject / park**: feedback that pulls the article toward another genre, adds an unsupported framework, demands a product comparison, turns a research report into a media hook, expands the article into a survey, or materially increases length without new evidence.

Priority order: **factual correctness → positioning integrity → core comprehension → technical depth → elegance → distribution preference**.

#### R4. Resolve conflicts explicitly

When readers disagree, preserve the article's positioning. Record:

- which role raised the issue;
- whether it is a comprehension failure or a preference difference;
- whether the proposed change changes the article's subject;
- the chosen action and why;
- what is intentionally not adopted.

Two readers agreeing is not sufficient if the suggestion violates the locked scope. One specialist's objection is sufficient to fix a factual or technical error even if other readers did not notice it.

#### R5. Limit revision scope

Apply must-fixes and compatible suggested changes in one focused pass. Do not keep adding examples, tables, definitions or sections until every role is satisfied. Re-run only the affected reader test after revision; stop when the core message, intended scope and technical level are understood by the selected roles.

#### Reader-fit output

```text
Positioning lock: article type / primary reader / reading task / thesis / exclusions / depth target
Selected roles: why these roles fit
Role findings: core message / confusion / wrong inference / missing bridge
Consensus barriers: issues raised by 2+ relevant roles
Decision table: keep / fix / optional / reject-or-park + reason
Positioning drift check: pass / fail
Post-fix targeted re-read: pass / remaining issue
```

### Step 9 Finalize

Finalize only after the selected reader-fit test passes its positioning-drift check and all unresolved items are either fixed or explicitly parked.

## Hard Rules

> Cannot be violated.

1. **Panelists critique hard, never self-praise** — finding problems is more valuable than confirming none.
2. **G1 has highest priority** — foundational facts and originality must be verified online; do not rely on existing material or memory alone.
3. **Red-line clearance is a hard gate** — both Step 3 and Step 8 must scan the full text. Marketing jargon, writing-process meta-info, commercial intent, and AI-bridge patterns must be cleared. Contrast structures are reviewed for density and function, not mechanically forced to zero.
4. **Never replace one contrast pattern with another** — when reducing a formulaic contrast sentence, use direct statements or two complete sentences; preserve a natural contrast when it carries the judgment.
5. **Professional-vs-distribution tension is not forced into agreement** — list options for the author to decide. Principle: a hook must not sacrifice professional credibility, but must not be so professional that no one clicks.
6. **Reader-fit feedback cannot override the positioning lock** — the reading test diagnoses misunderstanding; it does not grant every role editorial authority to expand scope, change genre, add unsupported material or flatten technical depth.
7. **Do not average roles or chase unanimity** — fix factual/technical misreadings even if one role reports them; adopt comprehension fixes only when compatible with the intended reading task; park preference conflicts explicitly.
8. **Scope and length are quality constraints** — do not add examples, tables, definitions or sections merely because a reader requested them. Every addition must repair a named comprehension barrier without creating a new center of gravity.
9. **Native-speaker review is a mandatory gate** — T1 must re-read the draft as a native speaker of the writing language and flag translated / calqued / unidiomatic expression; such findings are must-fix. Writing-time discipline (pipeline section 4 register rules) and review-time filtering are two independent defenses, never merged or skipped together.

## Pitfalls

- 把阅读测试当成第二轮八角色会审——它只测目标读者能否正确理解，不重新评判所有事实、深度和传播问题。
- 看到普通读者读不懂就自动降技术密度——先判断是必要术语缺少桥梁，还是文章本来就面向专业读者；不为追求人人读懂而改变文章定位。
- 把四个角色的意见全部采纳——不同角色代表不同阅读任务，意见冲突是正常的；先看是否触及核心误解，再看是否符合定位锁。
- 用“多数人都这样反馈”替代判断——两人重复指出也不代表可以扩篇、加新中心或越过事实证据门槛。
- 为满足阅读测试加入未经研究支撑的案例、市场数据、成本模型或产品横评——这属于定位漂移，应拒绝或停放。
- 阅读测试后不断加表、加例子、加定义，导致文章面面俱到却没有一条线讲透——一次集中修订后只复测受影响段落，达到“核心信息、范围、技术层级可正确理解”即停止。

## Failure Handling

| Scenario | Handling |
|----------|----------|
| No finished draft (only topic/outline) | Stop, ask to finish first draft before review |
| Content type does not apply (news/marketing/docs etc.) | Stop, explain this skill only reviews deep research pieces |
| Foundational fact cannot be verified | Mark "to-verify", reject and ask for evidence or revised judgment; do not pass |
| Core argument collides (plagiarism risk) | Judge independent-derivation vs verbatim-similar; if similar, reject and ask to rewrite that part |
| Revision introduces new red-line phrasing | Step 8 re-check intercepts, revise again |
| Author leaves tension items (professional vs distribution) undecided | Do not finalize; list the options again and require an explicit author decision or an explicit park before Step 9 |

## Output Format

```
【G1 Fact & Originality】Facts: pass/reject + Originality: core-argument search result (original / independently derived / collision-needs-fix)
【G2 Style red-line】pass/reject: specific sentence + line number
【R1】value judgment + what it picked on + pass or not
【R2】【R3】【R4】same as above
【G3 Depth】how many moves hit + what's missing
【T1 Distribution】title hook + opening retention + memorable point + platform fit + tension with G2/R4
【T1 Language】native-speaker pass verdict (must-fix items flagged and cleared on Step 8 re-read), reported separately from distribution
【Summary】must-fix N / suggested N / optional N / for-decision N
```

## Notes

Role profiles can be fine-tuned per the specific project's reader composition and writing norms (e.g., align with the user's long-term writing profile). Detailed role definitions and depth moves are in `references/depth-playbook.md`.

## 中文摘要

本 Skill 提供固定的**八角色专家评审团**，在科技/AI/产业深度长文成稿后做多视角会审，逼近可发布质量。设计模式为 Evaluator-Optimizer（评估→修订→复审）。

- **适用**：面向行业读者、建专业 IP 的科技/AI/产业研究型或深度分析型长文；不适用新闻、营销、文档、教程、短评。
- **流程**：八角色会审负责事实、原创、红线、结构、专业度和传播张力；会审修订后另跑一次 **reader-fit 阅读测试**，再定稿。阅读测试先锁文章定位，按文章需要选择 3–4 个代表角色，不默认全选。
- **阅读测试硬规则**：只诊断核心信息是否被正确理解、范围是否被误读和必要桥梁是否缺失；不把所有角色意见一概采用，不为迎合读者改题、扩篇、降技术密度或加入未经研究支撑的内容。
- **硬规则**：评审挑得狠不自我表扬；G1 优先级最高；红线清零是硬门槛（Step3/Step8 双 grep）；专业 vs 传播张力不强行统一，列选项由作者拍板。
- **母语审核强制门（2026-09-16 增设）**：T1 编辑角色须以写作语言的母语使用者视角重读全文，过滤翻译腔与不地道表达，命中即 must-fix；与写作阶段语域纪律构成两道独立防线。
- **标题锚点门（2026-10-08 增设）**：T1 编辑角色须单独核标题——必须含具体锚点（谁/场景/问题三类至少一类），抽象短标题、文件名式标题、读者导向空泛标题（如"关于 X 的思考"）命中即 must-fix；标题是分发第一入口，不随正文修订自动改善，须单独过一遍。
- 角色画像可按项目读者构成与写作规范微调；详细定义见 `references/depth-playbook.md`。
