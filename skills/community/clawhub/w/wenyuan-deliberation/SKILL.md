---
name: wenyuan-deliberation
description: "Three-seat deliberation protocol for complex decisions: exposes assumptions, compares options, and identifies risks."
version: 1.0.2
metadata:
  openclaw:
    requires: {}
    skillKey: wenyuan
    emoji: "🏛️"
    homepage: https://github.com/gordonlu/wenyuan
---

# Wenyuan Deliberation / 文渊阁合议

Use this skill when the user needs structured deliberation for a complex decision.

文渊阁 uses three seats to examine one issue from different angles, challenge each other, revise their positions, and form a final council recommendation.

This is a prompt-only skill. It uses the current agent's own reasoning model and does not require external APIs, credentials, binaries, or tools.

---

## When to Use

Use this skill when the user asks for:

* 文渊阁合议
* 三席合议
* 多方案权衡
* 产品方向判断
* 架构方案判断
* 风险评估
* 战略规划
* 复杂选择
* trade-off analysis
* decision support
* assumption tracking

Use it proactively when the problem has meaningful uncertainty, trade-offs, or long-term consequences.

Do not use it for simple factual questions, direct translation, pure rewriting, trivial choices, or tasks where the user clearly wants a short direct answer.

---

## Core Principle

文渊阁 is not a role-play exercise.

It is a decision protocol.

The goal is to make a decision more:

* balanced
* inspectable
* risk-aware
* assumption-aware
* resistant to premature consensus
* easier to revisit later

Do not force consensus. Useful disagreement should be preserved.

---

## The Three Seats

Use three clearly different perspectives:

| Seat | Focus                                                                | Main Question                                          |
| ---- | -------------------------------------------------------------------- | ------------------------------------------------------ |
| 谋远席  | long-term direction, alternatives, optionality, second-order effects | What path keeps the most valuable future options open? |
| 经世席  | feasibility, resources, execution path, cost, sequencing             | What can actually be done with current constraints?    |
| 持正席  | hidden assumptions, risks, logic gaps, failure modes, boundaries     | What could make this wrong, unsafe, or misleading?     |

Keep the seats distinct:

* 谋远席 should not become a normal practical planner.
* 经世席 should not become a vague strategist.
* 持正席 should not become generic pessimism.

---

## Deliberation Modes

### Quick Mode

Use only when the user asks for a brief answer.

Output:

* three short seat summaries
* one recommendation
* key risk
* next step

Target length: 500-900 characters (Chinese) or 200-400 words (English).

---

### Medium Mode

Default mode.

Use visible four-phase deliberation:

1. 独议
2. 批议
3. 复议
4. 阁议

Target length: 1000-1800 characters (Chinese) or 400-700 words (English).

Medium Mode should feel like a real deliberation, not a shallow three-angle summary.

---

### Deep Mode

Use only when the user explicitly asks for:

* 深度合议
* 完整四阶段
* 完整过程
* 完整 JSON
* 展开三席过程
* full deliberation
* full JSON

For very complex or high-stakes decisions, mention that a dedicated Wenyuan runtime would be better than a prompt-only skill because it can provide staged execution, progress events, validation, persistence, and review history.

---

## Medium Mode Workflow

Use this workflow by default.

### Phase 1: 独议

Each seat gives one main position.

Each position should include:

* core judgment
* reason
* key assumption
* main risk

Seats should not respond to each other in this phase.

---

### Phase 2: 批议

Each seat gives one strongest critique.

Each critique should include:

* what it challenges
* why it matters
* how the proposal should be improved

Avoid weak critiques such as:

* "总体认同"
* "可以参考"
* "需要进一步完善"
* "风险可控"

The critique must make the decision sharper.

---

### Phase 3: 复议

Each seat revises its position after critique.

Each revision should say:

* what changed
* what was preserved
* what uncertainty remains

Revision should not merely repeat 独议.

---

### Phase 4: 阁议

Form the final council recommendation.

Include:

* recommended direction
* majority reasoning
* minority opinion if any
* key assumptions
* main risks
* unresolved questions
* next actions

Do not force consensus. If disagreement remains, preserve it.

---

## Progress Visibility

文渊阁合议 is a multi-phase process. The user should not be left with only a spinner when possible.

If the host supports streaming intermediate assistant messages, emit short visible progress updates:

```text
🏛️ 文渊阁合议开始：正在进行合议。
一、独议完成：三席已分别形成初步判断。
二、批议完成：三席已指出关键弱点。
三、复议完成：立场已根据批议修订。
四、阁议完成：已形成建议、风险与下一步。
```

Progress updates must be short, factual, user-facing, and free of hidden chain-of-thought.

If the host only displays the final response, include a compact progress summary at the top of the final answer.

---

## Default Output Format

For Medium Mode, use this structure:

```markdown
## 🏛️ 文渊阁合议

议题：...

## 合议进度

- 独议：已完成
- 批议：已完成
- 复议：已完成
- 阁议：已完成

---

## 一、独议

### 谋远席

...

### 经世席

...

### 持正席

...

---

## 二、批议

- 谋远席质疑：...
- 经世席质疑：...
- 持正席质疑：...

---

## 三、复议

- 谋远席修订：...
- 经世席修订：...
- 持正席修订：...

---

Present the final result in the user's language. Translate all section headers from the template below to match the user's language.

```markdown
## 🏛️ 文渊阁合议

结论
- 推荐方案：...
- 核心理由：...
- 少数意见：...

关键假设
1. ...
2. ...

主要风险
1. ...
2. ...

仍未验证的问题
1. ...
2. ...

建议下一步
1. ...
2. ...
```
```

Keep each section concise. Do not over-expand.

---

## Quick Mode Output Format

Use only when the user asks for a quick answer.

Output in the user's language, following this structure:

```markdown
## 🏛️ 文渊阁简议
- 推荐判断：...
- 谋远席：...
- 经世席：...
- 持正席：...
- 关键风险：...
- 下一步：...
```

---

## Deep Mode JSON

Only output JSON when the user explicitly requests complete JSON.

Use this compact shape:

```json
{
  "topic": "",
  "context_summary": "",
  "independent": {
    "mouyuan": {
      "position": "",
      "assumption": "",
      "risk": ""
    },
    "jingshi": {
      "position": "",
      "assumption": "",
      "risk": ""
    },
    "chizheng": {
      "position": "",
      "assumption": "",
      "risk": ""
    }
  },
  "critique": {
    "mouyuan": "",
    "jingshi": "",
    "chizheng": ""
  },
  "revision": {
    "mouyuan": "",
    "jingshi": "",
    "chizheng": ""
  },
  "final_council": {
    "recommendation": "",
    "majority_reason": "",
    "minority_opinion": "",
    "key_assumptions": [],
    "main_risks": [],
    "unresolved_issues": [],
    "next_actions": []
  }
}
```

When outputting JSON:

1. Output valid JSON only.
2. Do not include explanatory text outside JSON.
3. Do not omit fields.
4. Use empty strings, empty arrays, `false`, or `null` when information is missing.
5. Do not claim that role-play is true multi-model deliberation.

---

## Honesty Rules

Do not invent facts, numbers, sources, user constraints, tool results, or verification results.

If information is missing, label it as an assumption or unresolved issue.

Do not present the result as certain truth.

Do not describe this skill as true independent multi-model deliberation. It is a single agent using structured perspectives unless an external Wenyuan runtime or multi-model system is explicitly available.

Do not overstate confidence.

Do not hide serious disagreement.

Do not force a majority when evidence does not support one.

---

## Quality Checklist

Before finalizing, check:

* Did the three seats remain meaningfully different?
* Did 批议 challenge real weaknesses?
* Did 复议 actually sharpen the positions?
* Did 阁议 preserve important disagreement?
* Did the final answer identify assumptions and risks?
* Did the answer suggest concrete next actions?
* Did the response avoid becoming either too shallow or too long?

A good 文渊阁 answer should help the user make a decision that can survive scrutiny.

