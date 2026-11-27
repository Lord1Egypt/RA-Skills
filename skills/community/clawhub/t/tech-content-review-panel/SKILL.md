---
name: tech-content-review-panel
description: Reads a finished tech/AI/industry long-form article from several optional reader perspectives and returns observations for the author to adjudicate. Use when the author wants a few more pairs of eyes on a complete draft. Factual and originality verification is the only hard check; perspective findings are feedback, not verdicts, and are not written into standing rules.
version: "1.3.1"
agent_created: true
read_when:
  - "多视角阅读 / 换几个人读一遍 / 读稿反馈"
  - "读完整稿后想知道别人读出了什么"
  - "成稿后的事实与原创性复核"
slug: tech-content-review-panel
displayName: tech-content-review-panel
description_zh: "给成稿换几双眼睛：可选的读者视角报告观察，事实与原创性单独核验；作者按问题性质裁决，意见不自动成为必改项或长期规则。"
not_for:
  - Fact-checking a single claim in isolation (use a claim-audit skill instead)
  - Rewriting or restructuring the article itself (reading is observational; the author decides)
  - News, marketing copy, documentation, tutorials, or short opinion posts
  - Reading a draft that is not finished yet
  - Assigning pass/fail grades or publication-readiness scores to an article
---

# Multi-perspective Reading

A finished long-form article can look correct to its author and still lose a reader. This skill supplies optional reader perspectives and reports what they actually took away. It is a **reading tool, not a review court**: no role carries authority, no finding is automatically a defect, and no feedback becomes a standing rule by itself.

The identifier `tech-content-review-panel` is kept so existing references from other skills do not break. It no longer denotes a fixed panel or an approval gate.

## What stays hard, and what becomes optional

| Layer | Treatment here |
|---|---|
| **A / content baseline** | Facts, numbers, attributions, originality and privacy are verified against sources. A substantiated error is an error, whoever found it. This is the only mandatory check. |
| **B / delivery contract** | Format, size and compliance specs are enforced only when that deliverable exists, by that deliverable's own checker — not by this reading. |
| **C / generative goals** | Whether the piece is worth reading is the author's judgment; this skill does not score it. |
| **D / optional diagnostics** | Red-line patterns, calque lexicons, depth moves, title hooks, distribution preferences and perspective suggestions. Used when a concrete symptom appears. |

## Workflow

### Step 1 — Lock the positioning (record, do not test yet)

Before reading, write down five items: article type and platform; primary reader and reading task; thesis or research question; deliberate scope and exclusions; depth, length and technicality target.

These are the author's decisions. Reader reactions diagnose whether the draft delivers them; they do not reopen the subject, change the genre, flatten technical depth, or add a new centre of gravity.

### Step 2 — Verify facts and originality (the only gate)

- Check every number, company name, date, policy and event against traceable sources. Distinguish confirmed / to-verify / possibly-stale; do not present old material as new.
- Assess whether the core argument and framework are independently derived or verbatim-similar to published work. Verify every "first / original / exclusive" claim rather than asserting it from memory.
- **Before external search**: the draft is often unpublished. Confirm with the user that sending draft-derived text (core argument, framework, signature phrasing) to a third-party search service is authorized. If not, use minimal redacted factual queries, or mark originality "unverified locally" and skip external search. Never transmit the full draft or identifying details.
- A claim that cannot be verified is reported as unverified with the specific gap. The author decides whether to cut it, qualify it, or supply evidence; the reader does not silently rewrite the argument.

### Step 3 — Choose perspectives for this article

Pick 2–4 that match the positioning. Do not use all by default, and do not require two rounds.

- **Domain specialist** — terminology, mechanism, technical credibility.
- **Runtime / infrastructure specialist** — component ownership, state flow, recovery, implementation boundaries.
- **Enterprise decision-maker** — whether the judgment helps architecture, procurement, governance or prioritisation.
- **Cross-domain industry reader** — whether an informed non-specialist can follow the core message.
- **Strategy / investment reader** — business logic and whether conclusions outrun their evidence.
- **Distribution editor** — title entry point, opening retention, shareable lines, platform fit.
- **Language-native reader** — idiomatic rhythm, collocation and translation calques.
- **Blunt general reader** — where attention drops, which sentence feels padded or AI-shaped.

A research report does not automatically need an investor or a media editor. A highly technical piece may use only the first two plus one comprehension check. State why each chosen perspective fits. Simulated perspectives must be labelled **simulated reading** — they are not evidence of real audience response.

### Step 4 — Report observations

Each perspective reports, in plain language:

1. the judgment or mechanism it took away;
2. where it stopped, slid, or had to reread, naming the sentence;
3. what in the text caused that reaction;
4. an optional trial revision, only if one is obvious.

Allow "no new issues". Allow disagreement between perspectives. Do not assign grades, pass/fail, or a required number of findings. A reader does not edit the draft. Findings are separated into **misunderstanding**, **missing bridge**, **disagreement** and **different preference** — these are different things and must not be merged into one defect list.

### Step 5 — Diagnose expression only when a symptom exists

When a specific expression problem is visible, consult the on-demand problem library in `tech-writing-pipeline` §4 and Verification: contrast density, marketing jargon, meta-commentary, calque lexicon, defensive hedging, colloquial fragments, title anchors, AI-bridge patterns. These are diagnostic clues, not a standing clearance gate. A hit is reported with the sentence and the concrete effect; it is not mechanically deleted, and no quota is applied.

Two independent language checks remain because the author's self-assessment is asymmetric:

- **English**: native-speaker read is still required for English drafts. The author has a documented blind spot here. Findings are reported as specific unnatural collocations or rhythm, then adjudicated by the author rather than auto-applied.
- **Chinese**: EN→ZH calques are handled the same way — as concrete findings, not as a whole-draft veto.

Depth moves in `references/depth-playbook.md` are diagnostic options for understanding whether a mechanism is explained. They carry no minimum hit count and never justify adding a history, comparison or boundary section.

### Step 6 — The author adjudicates

Sort findings by their nature, not by the role that raised them or by how many roles agree:

- **Substantiated factual, technical, attribution or spec error** → fix it, then confirm the fix did not flatten the prose. The finding is a clue; evidence or the delivery contract makes it binding.
- **Core thesis misunderstood / necessary bridge missing** → locate the cause in the text and fix it narrowly, provided the fix does not breach the positioning lock.
- **Explanation angle, extra example, tone, title preference** → adopt, adapt, park or decline by net benefit to judgment, clarity and reading momentum. Record a short reason for parked items.
- **Feedback that pulls toward another genre, adds unsupported material, or induces defensive expansion** → decline. No obligation to "cover" every comment with a table, definition or caveat.

One specialist's evidenced factual objection is enough. Two readers agreeing on a preference is not enough to override the locked scope. Unadopted feedback is a record, not an unfinished obligation.

### Step 7 — Targeted reread, then stop

Reread only the affected passages: confirm the factual or spec fix is correct, the core message and scope still read correctly, and no new factual error was introduced. Stop when the core message, intended scope and technical level are understood. Do not loop until every perspective is satisfied.

### Step 8 — No automatic rule-making

A single article's feedback fixes that article. It does not create a standing rule, a new grep, or a new checklist. If the same finding reveals a conflict in an existing rule, amend that rule in place. If the author explicitly states a long-term requirement, register it in the scope the author named. Otherwise, general preferences go to the case library as examples. Perspective findings never become permanent constraints on the strength of a judgment.

## Hard Rules

1. **Evidence makes an error binding, not seniority of a role.** Verify before calling something a factual error.
2. **Perspectives are chosen per article.** No fixed eight, no mandatory second round, no quota of findings.
3. **Observations are not verdicts.** Report what was read; never silently rewrite the draft or grade it.
4. **No invented defects and no credit for volume.** Finding nothing is a valid result. Precision beats count.
5. **Do not average roles or chase unanimity.** Adjudicate by problem nature and the positioning lock.
6. **Expression diagnostics are on-demand.** They do not grant a veto over a draft, and a hit does not force a rewrite.
7. **The positioning lock is not negotiable by feedback.** Reader reactions cannot change the subject, add an unsupported framework, or flatten technical depth.
8. **Feedback does not become a standing rule.** Single-article findings stay with the article; long-term rules change only by explicit author instruction or in-place conflict repair.
9. **Simulated reading is labelled as such.** Never present it as real audience validation.
10. **Diagnostics name the sentence.** Every style, rhythm or calque finding points to an exact sentence and states the reading effect; a pattern match without a location is not reported as a finding.

## Pitfalls

- Turning a reading into a second approval panel with grades, must-fix counts and a re-review loop.
- Treating every perspective's preference as a defect to be cleared, then adding tables, examples and definitions until the piece has no main line left.
- Deleting strong, well-supported judgments because a diagnostic pattern matched.
- Averaging disagreement into a compromise that satisfies no reading task.
- Assuming a general reader's difficulty means the technical density must drop; check whether a term lacks a bridge first.
- Using "most readers said so" to justify an expansion that breaks the locked scope.
- Letting one round of feedback produce a new global prohibition, which is how a rule system grows dry.

## Failure Handling

| Scenario | Handling |
|---|---|
| No finished draft | Stop; ask for a complete draft before reading |
| Content type does not apply | Stop; explain the scope |
| Foundational fact cannot be verified | Report the specific gap as unverified; author decides |
| Core argument collides with published work | Report the overlap as a finding, not a grade |
| A revision introduces a factual error | Catch it in the targeted reread |
| Perspectives disagree | Record the disagreement; author adjudicates |
| Feedback asks for a different article | Decline or park with a reason |

## Output Format

```text
Positioning lock: type / reader / reading task / thesis / exclusions / depth target
Selected perspectives: which ones and why
Fact & originality: verified / to-verify gaps
Observations per perspective: took away / stopped at / sentence / optional trial revision
Separation: misunderstanding / missing bridge / disagreement / preference
Author decisions: fix / adapt / park / decline + short reason
Targeted reread: affected passages only
Simulated reading: yes/no
```

## 中文摘要

本 Skill 给成稿换几双眼睛，**不叫评审、不做通过判定**。

- 事实与原创性核验是唯一的硬检查；其余视角按文章定位选 2–4 个，报告"读出了什么、在哪里停住、哪句造成的、可试的改法"。允许没有新问题，允许意见冲突。
- 观察不等于裁决，不按角色权威或人数采纳。已核实的错误要修；理解障碍定向修；偏好由作者择优或停放。
- 表达红线、纵深六法、标题钩子、语域词表都是按需诊断，命中只是线索，不设配额、不自动改写、不取得对成稿的否决权。
- 英文母语复核保留（作者识别盲区），中文翻译腔同样只报具体发现。模拟角色必须标注，不冒充真实读者。
- **反馈不自动立法**：单篇意见只修单篇；长期规则只在作者明确提出或既有规则冲突时原位修正。
- 标识符 `tech-content-review-panel` 沿用以免破坏其他 Skill 的引用，但它不再代表固定八角色或发布审批门。
