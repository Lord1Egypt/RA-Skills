# Task File Format Reference

## YAML Frontmatter Schema

```yaml
---
id: T-001                    # Required. From .meta.json nextId.
title: "Task title"          # Required. Concise, descriptive.
status: active               # Required. active | done | cancelled | archived
priority: medium             # Required. critical | high | medium | low
category: ""                 # Optional. User-defined string. Free-form.
due: 2026-04-10              # Optional. YYYY-MM-DD. Omit if no deadline.
created: 2026-04-02          # Required. YYYY-MM-DD.
completed:                   # Set when status → done. YYYY-MM-DD.
estimated_hours:             # Optional. Number. Rough effort estimate.
tags: []                     # Optional. String array for filtering.
related: []                  # Optional. Related people, projects, systems.
---
```

### Field Details

| Field | Required | Values | Notes |
|-------|----------|--------|-------|
| id | ✅ | T-NNN | Zero-padded, from .meta.json |
| title | ✅ | string | Keep under ~60 chars for INDEX readability |
| status | ✅ | active/done/cancelled/archived | |
| priority | ✅ | critical/high/medium/low | |
| category | ❌ | string | User-defined. Never hardcode a fixed set. |
| due | ❌ | YYYY-MM-DD | Omit for open-ended tasks |
| created | ✅ | YYYY-MM-DD | Auto-set at creation |
| completed | ❌ | YYYY-MM-DD | Set when marking done |
| estimated_hours | ❌ | number | Helps with scheduling advice |
| tags | ❌ | string[] | For search and grouping |
| related | ❌ | string[] | People, projects, external refs |

### Priority Semantics

- **critical**: Blocking other work or has severe consequences if missed
- **high**: Important deadline, significant impact
- **medium**: Normal work item
- **low**: Nice-to-have, can be deferred

## Section Template

```markdown
---
(frontmatter)
---

# {ID}: {Title}

## 설명

What needs to be done. Be specific and actionable.

## 배경/맥락

Why this task exists. Related history or decisions.

## 관련 자료

- Links, file references, Notion pages, external resources.

## 메모/진행 기록

- YYYY-MM-DD: Timestamped progress entries.

## 에이전트 노트

> Agent-generated context analysis.
> Cross-references to workspace files, timeline observations,
> dependency notes, related tasks.
```

### Section Guidelines

- **설명**: 1-3 sentences. Actionable. Answer "what exactly do I do?"
- **배경/맥락**: Optional but valuable for complex tasks.
- **관련 자료**: Links, file paths, Notion pages. Keep updated.
- **메모/진행 기록**: Append-only log. Agent and user both add entries.
- **에이전트 노트**: Agent fills this at creation time with workspace analysis.
  Update when new context is discovered.

## Example Tasks

### Example 1: Conference Review

```markdown
---
id: T-012
title: "AAAI 2027 Paper Review"
status: active
priority: high
category: Research
due: 2026-04-05
created: 2026-03-25
estimated_hours: 4
tags: [AAAI, peer-review, diffusion]
related: [CMT system]
---

# T-012: AAAI 2027 Paper Review

## 설명

Review 2 papers assigned for AAAI 2027 and submit reviews on CMT.

## 배경/맥락

- Assigned by Area Chair on 3/25
- Paper 1: Diffusion-based time series generation
- Paper 2: LLM-based portfolio optimization
- CMT submission deadline: 4/5

## 관련 자료

- [CMT Review Page](https://cmt3.research.microsoft.com/AAAI2027)
- [AAAI Reviewer Guidelines](https://aaai.org/reviewer-guidelines)

## 메모/진행 기록

- 2026-03-25: 2 papers assigned, PDFs downloaded
- 2026-03-30: Paper 2 first reading done

## 에이전트 노트

> Paper 1 (diffusion-based) may relate to ongoing lab research.
> At 2hrs/paper, recommend completing one per day before deadline.
```

### Example 2: Teaching Task

```markdown
---
id: T-013
title: "AI Intro Midterm Exam Prep"
status: active
priority: high
category: Teaching
due: 2026-04-12
created: 2026-04-01
estimated_hours: 5
tags: [midterm, exam, AI-intro]
related: []
---

# T-013: AI Intro Midterm Exam Prep

## 설명

Prepare midterm exam questions and answer key for Introduction to AI.
Exam date: 4/14 (Mon). Print deadline: 4/12.

## 배경/맥락

- Scope: Weeks 1-7 (search, optimization, probabilistic reasoning, ML basics)
- Can reference last year's exam
- TA review needed before printing

## 관련 자료

- Notion: AI Intro course page

## 메모/진행 기록

- 2026-04-01: Scope confirmed

## 에이전트 노트

> Real deadline is 4/11 (TA review buffer before 4/12 print).
> Recommend draft completion by 4/10 to allow revision cycle.
```

### Example 3: Student Supervision

```markdown
---
id: T-014
title: "Wooseok Paper Draft Feedback"
status: active
priority: medium
category: Research
due: 2026-04-08
created: 2026-04-02
estimated_hours: 2
tags: [paper, feedback, DPO]
related: [Wooseok Kang, KCC 2026]
---

# T-014: Wooseok Paper Draft Feedback

## 설명

Review and provide feedback on Wooseok's KCC 2026 paper draft
(DPO-based financial text generation).

## 배경/맥락

- Wooseok: MS student working on DPO for financial text
- KCC 2026 submission deadline: 4/20
- First draft received 4/2

## 관련 자료

- Student research notes in workspace

## 메모/진행 기록

- 2026-04-02: Draft received

## 에이전트 노트

> KCC deadline 4/20 requires at least 1 revision cycle.
> Ideal flow: feedback by 4/8 → revision by 4/15 → final review 4/18.
```
