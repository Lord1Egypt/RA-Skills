# Setup

## Prerequisites

- OpenClaw with heartbeat configured (recommended: every 30 minutes)
- A workspace directory

## Installation Steps

### 1. Generate TODO.md

If `TODO.md` doesn't exist in your workspace root, copy the template:

```bash
cp TODO-TEMPLATE.md ~/.openclaw/workspace/TODO.md
```

If `TODO.md` already exists, merge your existing tasks into the new format. The five sections are:

- 🔴 有人在等我 (Inbound)
- 🟡 有 deadline (Time-bound)
- 🔵 承诺了要做 (Committed)
- ⚪ 有空就做 (Fill)
- 🔄 定时任务 (Recurring)

### 2. Update HEARTBEAT.md

Replace task-specific checklists with one line:

```markdown
## TODO
- Read TODO.md, execute by priority
```

Remove any items that are now in TODO.md (e.g., "check GitHub notifications", "check 虾信", "scan TODO for overdue items"). Those are all TODO entries now.

### 3. Migrate Existing Tasks

Scan these sources for tasks that should move into TODO.md:

- **Old HEARTBEAT.md** — any checklist items → move to appropriate section
- **Cron jobs** (`~/.openclaw/cron/jobs.json`) — add corresponding entries to 🔄 with `cron: <job-name>` attribute
- **Memory files** — any "TODO" or "need to do" mentions → add if still relevant
- **Old TODO.md** — reformat existing items into the five sections

### 4. Verify

Read your new TODO.md top to bottom. Ask yourself:

- Does every task I know about appear here?
- Are recurring tasks (daily review, notifications check) included?
- Do cron-linked tasks have the `cron:` attribute?
- Is the priority ordering correct?

## Done

You're set. Next heartbeat will pick up TODO.md and start executing by priority.
