---
name: smart-tasks
description: >
  Intelligent task management using workspace markdown files.
  Natural language CRUD via chat, context-aware reminders,
  priority briefings, and weekly reviews.
  Use when: user mentions tasks, deadlines, todos, or things to do;
  user asks "what should I do today/this week";
  user wants to track, complete, or review work items.
  NOT for: calendar events, meeting scheduling, or project management
  with multiple collaborators.
---

# Smart Tasks

Manage tasks as markdown files in `tasks/` with an INDEX.md summary.
Minimize context usage: read INDEX.md first, individual files only when needed.

## Setup

Run the init script once to create the directory structure:

```bash
bash skills/smart-tasks/scripts/init-tasks.sh
```

This creates `tasks/`, `tasks/active/`, `tasks/done/`, `tasks/archive/`,
`tasks/INDEX.md`, and `tasks/.meta.json`. Idempotent — safe to re-run.

After init, apply workspace integration changes from
[workspace-integration.md](references/workspace-integration.md) with user approval.

## File Structure Overview

- `tasks/INDEX.md` — active task summary table (~1-2KB). **Read every session.**
- `tasks/.meta.json` — tracks `nextId` counter and known categories.
- `tasks/active/` — individual task files (one per task).
- `tasks/done/` — completed tasks (kept 30 days).
- `tasks/archive/YYYY-QN/` — long-term storage.

For full format specs see [file-structure.md](references/file-structure.md).

## Core Workflow

### 1. Detect Task Intent

When the user mentions deadlines, todos, or things to do in conversation,
propose creating a task. No special commands needed — use natural language.

Examples of triggers:
- "다음 주 금요일까지 리뷰 완료해야 해"
- "논문 피드백 보내야 하는데"
- "이번 주 할일 뭐 있어?"

### 2. Create a Task

1. Read `tasks/.meta.json` to get `nextId`.
2. Generate ID: `T-{nextId}` zero-padded to 3 digits (e.g., `T-001`).
3. Create slug from title (kebab-case English summary).
4. Write task file to `tasks/active/{ID}_{slug}.md` using the format in
   [task-format.md](references/task-format.md).
5. Fill the **Agent Notes** section with relevant workspace context
   (related files, people, timeline analysis).
6. Increment `nextId` in `.meta.json`. Add new category if not already listed.
7. Update `tasks/INDEX.md` — insert row in the correct section.

### 3. Update a Task

1. Identify the task by ID or title search in INDEX.md.
2. Read the individual task file from `tasks/active/`.
3. Apply changes to both the task file and INDEX.md.
4. Append a timestamped entry to the task's **메모/진행 기록** section.

### 4. Complete a Task

1. Set `status: done` and `completed: {today}` in the task file.
2. Move file from `tasks/active/` to `tasks/done/`.
3. Remove the row from INDEX.md. (Do NOT add to done section in INDEX.)
4. Confirm completion to the user.

### 5. Query Tasks

- **Quick overview**: Read INDEX.md only. Answer from the table.
- **Detail needed**: Read the specific task file(s) from `tasks/active/`.
- **"What should I do?"**: Analyze INDEX.md by deadline × priority × estimated hours.
  Recommend a sequence with reasoning.

### 6. Delete a Task

Only when explicitly requested. Move to `tasks/done/` with `status: cancelled`
rather than deleting the file. Remove from INDEX.md.

## INDEX.md Management

INDEX.md is the single-read entry point for task awareness.

### Structure

```markdown
# Tasks Index

> Last updated: YYYY-MM-DD
> Active: N | Overdue: N | Due this week: N

## 🔴 Overdue
| ID | Title | Due | Priority | Category |
|----|-------|-----|----------|----------|

## 🟡 Due This Week
| ID | Title | Due | Priority | Category |
|----|-------|-----|----------|----------|

## 📋 Later
| ID | Title | Due | Priority | Category |
|----|-------|-----|----------|----------|

## 📊 Summary
```

### Update Rules

- Update INDEX.md on **every** task create / update / complete / delete.
- Recalculate header counters (Active, Overdue, Due this week) each update.
- Keep rows sorted by due date within each section.
- Reclassify rows between sections based on current date.
- Set `Last updated` to today.

### Size Control

| Active tasks | ~Size | Action |
|-------------|-------|--------|
| 1–20 | ~1KB | Keep as-is |
| 20–50 | ~2.5KB | Abbreviate Later section (title + due only) |
| 50+ | ~5KB+ | Split into category indexes (INDEX-{category}.md) |

## Context Strategy

Read [context-strategy.md](references/context-strategy.md) for details on:
- Layered reading pattern (INDEX → active file → done/archive)
- Subagent cost optimization for cron jobs
- When to read vs. skip individual files

**Key rule**: If INDEX.md alone can answer the question, do NOT read individual files.

## Cron Jobs

Set up scheduled briefings and alerts. All cron jobs use Sonnet-class models.
See [cron-templates.md](references/cron-templates.md) for:
- **Daily morning briefing** (08:00) — overdue alerts + today's priorities
- **Deadline check** (12:00, 18:00) — D-0/D-1/overdue only, silent if none
- **Weekly review** (Sunday 20:00) — completion summary, stale task detection,
  archive cleanup (done/ 30+ days → archive/)

## Automatic Cleanup

| Transition | Trigger | Action |
|-----------|---------|--------|
| active → done | User marks complete | Move file, update INDEX |
| done → archive | 30 days elapsed | Weekly review moves to `archive/YYYY-QN/` |
| archive | — | Never in INDEX. Access only via search. |

## Task File Format

Each task is a markdown file with YAML frontmatter.
See [task-format.md](references/task-format.md) for:
- Complete frontmatter schema
- Section template
- 2-3 example tasks

## Workspace Integration

This skill does NOT modify files outside its own directory.
See [workspace-integration.md](references/workspace-integration.md) for
recommended changes to AGENTS.md, SOUL.md, and HEARTBEAT.md (diff format).
Apply these with user approval during setup.

## Integration with Other Skills

- **proactivity**: Record task status in session-state; proactively surface
  relevant tasks during conversation.
- **self-improving**: Log task management mistakes/improvements to domain file.
  Create `self-improving/tasks.md` for task-specific learnings.

## Best Practices

1. Always update INDEX.md and the task file atomically.
2. Fill Agent Notes with cross-references to workspace files at creation time.
3. Use estimated_hours to give realistic scheduling advice.
4. When reminding about tasks, include relevant context — not just the deadline.
5. Categories are user-defined. Never hardcode a fixed set.
6. Keep task titles concise but descriptive for INDEX readability.
