---
name: secretary-skill
description: "Full lifecycle goal management: from vague vision to filed, tracked, and automated long-term plan. 5-stage pipeline: de-ambiguation -> vertical splitting -> persistent storage -> cron automation -> ongoing review."
version: 2.0.0
tags: latest, productivity, planning, goal-tracking, goal-storage, lifecycle
---

# Secretary Skill

A specialized procedural tool that prevents long-term plans from failing by combating the three main killers of long-term goals: **ambiguity** (not knowing how to start), **overwhelm** (large goals feeling impossible), and **oblivion** (forgetting or losing motivation over time).

Now extended with **persistent storage and lifecycle management** — every goal gets filed to disk, tracked, and retrievable across sessions.

## The 5-Stage Pipeline

```
[Vague/Profound Goal]
       │
       ▼
 1. De-ambiguation    ──► 一次一问，锁定 Original Goal
       │
       ▼
 2. Vertical Splitting ──► 里程碑 → 2小时可执行原子任务
       │
       ▼
 3. Persistent Storage ──► 写入 ~/.hermes/goals/<slug>.md + memory 指针
       │
       ▼
 4. Cron Automation   ──► 设置定时提醒 / 复盘任务
       │
       ▼
 5. Tracking & Review ──► 更新进度、追加复盘日志、状态流转
```

---

## Stage 1: De-ambiguation — One Question at a Time

**NEVER ask multiple questions at once.** The de-ambiguation phase must follow this protocol:

1. The user states a vague vision.
2. You ask **ONE** thoughtful question from the conversational bank.
3. Wait for the user's full answer.
4. Briefly acknowledge the answer (1 sentence max).
5. Ask: **"现在清晰了吗？"** — if yes and core topics (meaning, scope, timeline) are covered, lock the goal and move on.
6. If not clear yet, ask the **next single question**.
7. Repeat until the user says it's clear.

**Question style guidelines:**
- Each question must reference the user's own words where possible.
- Questions should feel like a curious coach, not a form.
- Topics to explore (in order): meaning → scope → measurement → timeline → stakeholders → risk
- If the user volunteers enough context, skip the topic.
- The goal is not to ask every question — it's to get the user to say "清楚了".

## Stage 2: Vertical Splitting

Once the Original Goal is locked, break it down hierarchically:

| Depth | Output | Time per item |
|-------|--------|---------------|
| 1 | 3-5 major milestones | weeks to months |
| 2 | 10-20 sub-tasks per milestone | days |
| 3 | Atomic executable items | ~2 hours |

The `/split --depth [1-3]` command controls this.

## Stage 3: Persistent Storage

Every locked + split goal gets persisted to disk so it survives across sessions.

### Storage Convention

```
~/.hermes/goals/
└── <slug>.md          # One file per goal
```

### File Format (YAML Frontmatter + Markdown Body)

```markdown
---
title: "<goal title>"
slug: <unique-slug>
status: active          # active | paused | completed | archived
created_at: YYYY-MM-DD
target_date: YYYY-MM-DD
category: finance       # finance | health | career | learning | project | other
tags: [tag1, tag2]
metrics:
  - name: <metric name>
    target: <number>
    current: <number>
    unit: <unit string>
last_reviewed: YYYY-MM-DD
---

# <Goal Title>

## 原始目标
(什么)

## 背景
(为什么、怎么样、关键参数)

## 计划详情
(倒推过程和结构化计划)

## 关键纪律
(要遵守的规则)

## 复盘记录

### YYYY-MM-DD
(每次复盘加一条记录)
```

### Storage Workflow

When the user says "存下这个目标" or the goal is locked and split:
1. Generate a unique slug from the title (lowercase, hyphens)
2. Build the full markdown file with frontmatter + body
3. Write to `~/.hermes/goals/<slug>.md`
4. Save to **memory** a brief pointer: "Goal '<title>' (slug) — ~/.hermes/goals/<slug>.md — status: active — target: <target> — progress: <current>"
5. Confirm to the user the goal has been filed

## Stage 4: Cron Automation

Maps tasks onto a timeline and schedules automated reminders.

### Cron Bridge Payload

```json
{
  "skill_target": "Secretary Skill",
  "cron_expression": "0 9 * * 1-5",
  "action_type": "active_reminder",
  "payload": {
    "original_goal_snapshot": "[Locked Goal]",
    "current_task": "[Task X]",
    "trigger_prompt": "Re-anchor the user to the grand vision, verify if [Task X] is ready for today, and listen for a `/align` call if scheduling conflicts exist."
  }
}
```

Use the `cronjob` tool to set up recurring reminders:
- **Monthly budget review**: `0 9 1 * *` (1st of every month)
- **Weekly progress check**: `0 10 * * 1` (Mondays 10am)
- **Daily task reminder**: `0 9 * * 1-5` (weekdays)

## Stage 5: Tracking & Review

### Cross-Session Recall

The **memory pointer** is the key to cross-session recall. When the user mentions a goal:
1. Check memory for the pointer
2. Read `~/.hermes/goals/<slug>.md`
3. Present current status + progress

### Operations

| User says | Action |
|-----------|--------|
| "我有哪些目标" / "列出目标" | Read all `.md` from `~/.hermes/goals/`, parse frontmatter, present summary table (title, status, category, target_date, progress) |
| "看看 <目标>" / "show <slug>" | Read and display the full goal file |
| "更新进度" / "update <slug>" | Update metrics (current values), append a review log entry, write back, update memory |
| "这个目标完成了" / "archive <slug>" | Set status to `completed` or `archived`, write back, update memory |
| "暂停这个目标" / "pause <slug>" | Set status to `paused`, write back, update memory |

### Review Log Convention

Each review entry in the body:
```
### YYYY-MM-DD
- Status: active → active (or → paused)
- Metrics: current=N (change: +X)
- Notes: (brief reflection on progress, issues, adjustments)
```

---

## Slash Commands (Agent Protocol)

| Command | Stage | Description |
|---------|-------|-------------|
| `/init_goal [text]` | 1 | Activates de-ambiguation, one question at a time |
| `/split --depth [1-3]` | 2 | Breaks locked goal into milestones → atomic tasks |
| `/save` | 3 | Persists current goal to `~/.hermes/goals/` |
| `/schedule --freq [daily/weekly/monthly]` | 4 | Creates cron job for reminders |
| `/align` | 5 | Recalibrates when plans change or friction occurs |
| `/status --report [slug]` | 5 | Shows current progress toward the goal |
| `/goal list` | 5 | Lists all stored goals |
| `/goal show <slug>` | 5 | Shows a specific goal's full content |
| `/goal update <slug>` | 5 | Updates metrics and appends review log |
| `/goal archive <slug>` | 5 | Marks goal as completed/archived |

---

## Domain References

The skill comes with domain-specific reference files that provide background knowledge for common financial planning scenarios:

- **Shenzhen Financial Planning (中国)** (`references/shenzhen-financial-planning.md`) — covers social insurance ratios, tax brackets, housing fund rules, and sample goal breakdowns for users in Shenzhen. Load this reference when the user's goal involves Chinese social insurance, tax, or housing fund calculations.

## Domain-Specific Calculation Skills

When a goal involves structured quantitative analysis (financial planning, budgets, timelines), the Agent should perform the full calculation in-session as part of Stages 1-2, then persist the results in Stage 3. The secretary-skill itself does not offload calculations to sub-skills — the analysis is the core value the user is paying attention to during the de-ambiguation and splitting phases.
