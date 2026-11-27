---
slug: tcms-planner
displayName: Tcms Planner
name: tcms-planner
version: "1.1.11"
not_for:
  - Content creation or drafting (brief output only)
  - Portfolio-level topic evaluation with scoring gates (use a portfolio skill)
  - Editing or approving the content calendar (advisory briefs only)
  - Trend reporting without a topic-selection decision
description: |
  Content topic-planning agent. Generates structured topic briefs from knowledge-base updates, competitor signals, the content calendar, and performance data.
  Does topic judgment and brief output only — not content creation.
description_zh: "内容选题规划器：从知识库更新、竞品信号、内容日历与绩效数据生成结构化选题简报，只做选题判断与简报输出，不做内容创作。"

read_when:
  - "生成选题简报或选题建议"
  - "规划本周/本月内容选题"
  - "从知识库更新或竞品动态里找选题"
  - "review content calendar for topic gaps"
  - "generate a topic brief from knowledge-base updates"
allowed-tools:
  - read_file
  - write_to_file
  - replace_in_file
  - search_content
  - list_dir
metadata:
  openclaw:
    tags:
      - content-marketing
      - content-strategy
      - planning
      - editorial-calendar
      - topic-research
      - tech-product
      - b2b
disable: false
---

# Content Planner

Generates structured topic briefs from multiple signal sources. Does no content creation — only topic judgment and brief output.

## Operating mode: routing

Routes to different topic-selection logic by signal source:

```
signal input
   ↓
[routing decision]
   ├── knowledge base has new/updated entries → new-content topic
   ├── competitor has a major move            → differentiation-response topic
   ├── content calendar due                   → schedule-driven topic
   └── user explicitly requests               → topic by specified direction
```

## Workflow

### Step 1: [deterministic] Confirm the topic trigger

**A. User explicitly requests** → user specified direction/type → go straight to Step 3

**B. Periodic check** → read the following signal sources:
1. Knowledge-base recent updates — check file modification times, identify recently updated product sections
2. Content calendar — read the current month's schedule, find content due this/next week
3. Published-content index — check which topics already have drafts and which are still missing
4. Competitor signals — check recent competitor moves (launch / pricing / funding) for a differentiation-response topic (routing branch above)

> The paths above must be configured per the actual project directory.

### Step 2: [deterministic] Read context

- **Must read**: the content calendar for the current month
- **Must read**: product-line / product-center mapping (configure per actual org structure)
- **As needed**: the knowledge-base section for the relevant product (use `search_content` to locate, don't read in full)
- **As needed**: existing-content inventory (judge whether there is stock content worth re-promoting)

### Step 3: [LLM] Generate topic suggestions

Based on signal sources and context, generate 1-3 topic suggestions. Each outputs a structured brief:

```markdown
## Topic Brief

**Topic title**: [working title, not the final published title]
**Article type**: tech blog / customer case / product update
**Target product**: [product name, use the official site name]
**Target reader**: [specific persona]
**Core message**: [one sentence summarizing the core message]
**Purpose**: [what the article should achieve]
**Material guide**:
  - knowledge-base entry: [which section to point to]
  - internal case: [📋 if any, mark customer name + redaction requirement]
  - published article: [if any reference exists]
**Target channel**: [first channel + syndication channel]
**Approval level**: L1 / L2 / L3
**Priority**: high / medium / low
**Suggested publish time**: [specific date or time window]
```

### Step 4: [LLM] Topic sanity check

- [ ] Is the product within the current priority scope?
- [ ] Does it duplicate any of the last 12 published or planned items?
- [ ] Is material sufficient (a corresponding knowledge-base entry exists)?
- [ ] Is the channel reasonable?

### Step 5: [deterministic] Output

Save the brief to `content-calendar/briefs/YYYY-MM-DD-brief.md`

Output an execution summary:
```
## Execution summary
- Trigger source: [user request / calendar schedule / knowledge-base update]
- Read: [list files read]
- Topics produced: [N]
- Requires human confirmation before entering content-writer
```

## ⚠️ Human-in-the-loop

After a topic brief is produced it **must be confirmed by a human** before entering `content-writer`. Do not auto-trigger downstream skills.

## Hard rules

1. **No content creation.** Output only the topic brief; don't write article body.
2. **No auto-trigger of downstream.** The brief must be human-confirmed.
3. **Don't recommend when material is insufficient.** If the corresponding knowledge-base entry is too thin, mark "insufficient material, suggest supplementing the knowledge base first".
4. **Internal cases default to redaction requirement.** Briefs involving internal-source customers must mark 📋.

5. **Dedupe before recommending.** Check the topic against the last 12 published or planned items; a duplicate or near-duplicate is flagged, not recommended.
6. **The comparison window is fixed.** Dedupe uses the same 12-item window for every suggestion in a run and names that window in the output, so two suggestions are not checked against different histories.

## Failure handling

| Failure scenario | Handling |
|------------------|----------|
| Content calendar file missing | prompt "content schedule not found, please create first" |
| Knowledge-base file missing | prompt "product knowledge base not found, please confirm path" |
| All scheduled content already has drafts | report "this week's scheduled content already has drafts, no new topic needed" |
| Product requested by user not in knowledge base | prompt "[product name] has no corresponding entry in the knowledge base, suggest supplementing first" |

---

## 中文摘要

Content Planner 是基于多信号源（知识库更新、竞品动作、内容日历、效果数据）生成结构化选题 Brief 的 Agent，只做选题判断与 Brief 输出、不写正文。产出后须经人工确认才能进入 content-writer，不自动触发下游。硬性规则：素材不足不推荐、内部客户案例默认标注脱敏要求。
