---
name: second-brain-growth
description: Evaluate the user's second-brain/第二大脑 effective knowledge growth speed and second-brain health, with Hbrain defaults plus Codex interactive use, Hermes cron/reporting, and OpenClaw multi-agent handoff compatibility. Use when the user asks about 知识增长速度, 第二大脑增长, Hbrain growth, knowledge compounding, recall rate, connection density, transformation rate, weekly/monthly second-brain scorecards, OpenClaw/Hermes second-brain automation, or whether notes are becoming usable 人脑 judgment/action/output rather than merely accumulating files.
---

# Second Brain Growth

## Overview

Use this skill to evaluate the user's second-brain growth as a closed loop: structured deposition, connection, 人脑 recall, transformation into action/output, and debt control. Default to Chinese for user-facing summaries.

Core doctrine:

- Growth is not storage. Effective growth means new material becomes connected, recallable, and useful for judgment/action/output.
- Keep knowledge deposition and anchor training separate. Do not create anchor-events, modify `anchor:`, or infer 人脑 training just because a page was written.
- Treat anchor-events as evidence of human-side recall demand, not as a log of AI reading material.
- Use absolute dates in reports.

## Roots

- Hbrain repo: `/Users/jianghaidong/hbrain`
- Wiki root: `/Users/jianghaidong/hbrain/llm-wiki`
- Anchor dashboard: `/Users/jianghaidong/hbrain/llm-wiki/_meta/anchors/index.md`
- Core questions: `/Users/jianghaidong/hbrain/llm-wiki/_meta/my-core-questions.md`
- Anchor events: `/Users/jianghaidong/hbrain/llm-wiki/_meta/anchor-events/YYYY-MM.jsonl`
- Router misses: `/Users/jianghaidong/hbrain/llm-wiki/_meta/anchor-events/router-misses/YYYY-MM.jsonl`

## Ecosystem Roles

Use the same metric model across Codex, Hermes, and OpenClaw, but adapt the delivery contract:

| Runtime | Role | Output expectation |
|---|---|---|
| Codex | interactive evaluator and skill maintainer | concise diagnosis in chat, optional file edits when asked |
| Hermes | daily/weekly scheduled operator | deterministic commands plus Markdown report; no prompt-side derived state edits |
| OpenClaw | multi-agent orchestration layer | task handoff block, machine-readable summary, clear next-agent actions |

Hermes is the daily operation interface. OpenClaw is the experiment/orchestration sandbox. Codex remains the engineering executor for changing this skill, scripts, or wiki automation.

## Runtime Modes

### Codex Interactive

- Use when the user asks a direct question in chat.
- Read local Hbrain sources, compute the five metric groups, and answer in Chinese.
- Avoid persistent writes unless the user asks for a saved report.

### Hermes Cron

- Use when the user asks to schedule, automate, or integrate this check into Hermes.
- Prefer `hermes cron create --skill second-brain-growth --workdir /Users/jianghaidong/hbrain ...`.
- Hermes cron should orchestrate commands, read outputs, and write/append reports only. It must not hand-edit `weight`, `last_active`, `hot`, `review-state`, or anchor lifecycle fields.
- For persistent reports, write under:
  - Daily/weekly automation: `/Users/jianghaidong/hbrain/llm-wiki/_meta/automation-runs/`
  - Growth-specific audits: `/Users/jianghaidong/hbrain/llm-wiki/_meta/anchor-governance/knowledge-growth/`
- Include a stable final section named `## Agent Handoff` so future Hermes/OpenClaw runs can pick up unresolved work.

Hermes cron prompt pattern:

```bash
hermes cron create "0 21 * * 0" \
  --name "第二大脑有效增长周报" \
  --skill second-brain-growth \
  --workdir /Users/jianghaidong/hbrain \
  "Use $second-brain-growth to evaluate Hbrain effective knowledge growth for the last 7 days. Save a Markdown report if safe, and do not modify anchor lifecycle fields."
```

### OpenClaw Orchestration

- Use when the task should be split across main/design/code/coder/test or when OpenClaw is explicitly requested.
- The main/design agent should define the window, risk level, and output path.
- The code/coder agent may add scripts or run deterministic checks.
- The test agent should validate report shape, skill validity, and safety gates.
- Prefer OpenClaw `--json` output for automation, and include this skill name in the message body:

```bash
openclaw agent --agent main --json --message "Use $second-brain-growth to audit Hbrain effective knowledge growth for 2026-06-08..2026-06-14. Return the Markdown report plus Agent Handoff. Do not edit derived anchor fields."
```

If OpenClaw is only used as an orchestrator, do not assume it has permission to mutate Hbrain. Treat edits as proposals unless the initiating prompt explicitly allows low-risk writeback.

## Workflow

1. Establish context.
   - Read the anchor dashboard and core questions before broad recall.
   - If the user gives a specific question, run dry routing only:

```bash
python3 /Users/jianghaidong/.agents/skills/hbrain-cognitive-loop/scripts/hbrain_loop.py route --query "<user question>"
```

   - Do not rerun with `--record` unless the user explicitly asks to count a human-side call, nomination, or miss.

2. Choose the window.
   - Default to the last 7 days for "this week" or an unspecified growth check.
   - Use month-to-date for "this month".
   - State the exact date range in the report.

3. Collect five metric groups.

**A. 沉淀速度**

- Count total Markdown pages.
- Count pages created/updated in the window from frontmatter and, when useful, git history.
- Segment by `concepts/`, `queries/`, `practices/`, `comparisons/`, `entities/`, and `_meta/`.
- Favor structural pages over raw volume.

Useful commands:

```bash
rg --files /Users/jianghaidong/hbrain/llm-wiki -g '*.md' | wc -l
rg -l '^created: YYYY-MM-' /Users/jianghaidong/hbrain/llm-wiki -g '*.md' | wc -l
rg -l '^updated: YYYY-MM-' /Users/jianghaidong/hbrain/llm-wiki -g '*.md' | wc -l
rg --files /Users/jianghaidong/hbrain/llm-wiki -g '*.md' | sed 's#^/Users/jianghaidong/hbrain/llm-wiki/##' | awk -F/ '{print $1}' | sort | uniq -c | sort -nr
```

**B. 连接速度**

- Count total wiki links.
- Sample newly created structural pages and check whether each has at least two meaningful links to existing pages.
- Check whether new material is mapped to Q1-Q5 through direct links, anchor context, or weekly推进记录.

Useful command:

```bash
rg -o '\[\[[^]]+\]\]' /Users/jianghaidong/hbrain/llm-wiki -g '*.md' | wc -l
```

**C. 召回速度**

- Parse anchor-events for `used` and `recall-check`.
- Count active anchors touched in the window.
- Treat `recall_full`, `recall_partial`, and `recall_diverged` as 人脑 training evidence.
- Include router misses as evidence of unmet recall demand.

Useful commands:

```bash
wc -l /Users/jianghaidong/hbrain/llm-wiki/_meta/anchor-events/YYYY-MM.jsonl
wc -l /Users/jianghaidong/hbrain/llm-wiki/_meta/anchor-events/router-misses/YYYY-MM.jsonl
sed -n '1,120p' /Users/jianghaidong/hbrain/llm-wiki/_meta/anchor-events/YYYY-MM.jsonl
```

**D. 转化速度**

- Look for pages, weekly records, output dashboards, practices, code/project notes, decisions, and action experiments created from recent material.
- Report concrete examples rather than vague "learned a lot" summaries.
- Give special weight to evidence that knowledge changed judgment or behavior.

**E. 负债压力**

- Identify new isolated or underlinked structural pages.
- Note repeated router misses around the same theme.
- Note recall divergence, duplicate-like pages, stale high-priority anchors, and unresolved links only when they affect recall/action.
- Do not treat high orphan counts in the whole monorepo as automatically bad; focus on priority concepts, queries, and canonical anchors.

4. Score the loop.
   - Use the formula:

```text
本周有效增长 =
  新增结构化页
+ 新增关键连接
+ 被调用/召回的锚点
+ 转化成输出或行动的案例
- 新增孤岛/重复/不可召回材料
```

   - Prefer diagnostic labels over false precision:
     - `沉淀过快，召回滞后`
     - `连接健康，转化不足`
     - `召回活跃，沉淀不足`
     - `结构均衡，进入复利`
     - `负债上升，需要治理`

5. Report in this shape:

```md
**结论**
一句话判断增长状态和主要瓶颈。

**指标**
| 维度 | 本期证据 | 判断 |
|---|---:|---|
| 沉淀 | ... | ... |
| 连接 | ... | ... |
| 召回 | ... | ... |
| 转化 | ... | ... |
| 负债 | ... | ... |

**有效增长**
用公式解释本期是材料增长、网络增长、召回增长，还是行动增长。

**下周动作**
给 1-3 个最小可执行动作，优先修复瓶颈。

**Agent Handoff**
status: complete | needs-human | blocked
window: YYYY-MM-DD..YYYY-MM-DD
label: 沉淀过快，召回滞后 | 连接健康，转化不足 | 召回活跃，沉淀不足 | 结构均衡，进入复利 | 负债上升，需要治理
report_path: optional absolute path
safe_next_actions:
- ...
requires_confirmation:
- ...
blocked_by:
- ...
```

For Hermes/OpenClaw automation, also include this fenced machine-readable block at the end:

```yaml
knowledge_growth_result:
  status: complete
  window: "YYYY-MM-DD..YYYY-MM-DD"
  label: "沉淀过快，召回滞后"
  report_path: null
  metrics:
    deposition: null
    connection: null
    recall: null
    transformation: null
    debt: null
  safe_next_actions: []
  requires_confirmation: []
  blocked_by: []
```

## Interpretation Rules

- If new/updated pages are high but anchor events and outputs are low, call it "沉淀速度快，召回/转化滞后".
- If new pages have weak links, prioritize connection repair before adding more material.
- If recall-check divergence rises, recommend compressing anchor capsules or morning recall, not adding more pages.
- If router misses cluster around one theme at least three times, propose a candidate anchor review; do not directly add `anchor:`.
- If output/action evidence appears, name the exact pages or projects and explain the loop it closes.
- If asked for an executive metric, use a 0-10 "有效增长指数" but always show the evidence behind it.

## Compatibility Checks

When upgrading or validating this skill:

- Run `python3 /Users/jianghaidong/.codex/skills/.system/skill-creator/scripts/quick_validate.py <skill-dir>`.
- Keep YAML frontmatter limited to `name` and `description` so Codex, Hermes, and OpenClaw skill readers can parse it.
- Keep `agents/openai.yaml` optional and UI-only; do not put required runtime logic there.
- Verify examples use current CLI shapes when changing ecosystem instructions:
  - `hermes cron create --help`
  - `hermes --help`
  - `openclaw agent --help`
  - `openclaw skills --help`
- Do not require OpenClaw or Hermes to be installed for normal Codex interactive use. Missing runtimes should degrade to a chat report.

## Safety

- Do not hand edit `weight`, `last_active`, `hot`, or derived dashboard values.
- Do not write to `links/`; that layer is retired.
- Do not log anchor usage for AI-only analysis.
- Ask before deleting, renaming, merging, retiring, migrating, or editing raw source material.
- Writing a report under `_meta/anchor-governance/knowledge-growth/` is allowed when the user asks for a persistent report; otherwise answer in chat.
