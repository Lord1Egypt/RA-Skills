---
name: task-supervisor
description: Self-supervising long-running task manager with progress tracking and periodic status reports. Only activate for LARGE tasks — do NOT activate for quick or simple tasks. Activate when ALL of these are true: (1) Task has 5+ distinct steps OR estimated time >20 minutes, AND (2) at least one of: user says "take your time / do this overnight / finish by yourself / keep me posted", task requires sub-agents or cron jobs, task spans multiple tool calls across different domains (e.g. research + write + deploy). Do NOT activate for: single-step requests, quick searches, short code edits, simple Q&A, file reads, summarization of one document.
---

# Task Supervisor

Manage long-running tasks with checkpoints, progress files, and periodic WhatsApp reports.

## Is This a Large Task?

Before doing anything else, mentally check:

| Signal | Large? |
|--------|--------|
| Steps ≥ 5 OR time > 20 min | ✅ Yes |
| User says "take your time / overnight / keep me posted" | ✅ Yes |
| Needs sub-agent + cron + multiple domains | ✅ Yes |
| Single tool call, quick search, short edit, Q&A | ❌ No — skip this skill entirely |
| "Help me write X" (one doc, one sitting) | ❌ No |
| "Search for Y and summarize" (few minutes) | ❌ No |

If not large → respond normally, skip task files and crons entirely.

## On Task Start

When you receive a large task, immediately:

1. **Create a task file** at `.tasks/<TASK-SLUG>.md` (use kebab-case slug)
2. **Decompose** the task into numbered steps
3. **Spawn a reporter cron** to send progress updates
4. **Begin execution**, updating the file after each step

### Task File Format

```markdown
# Task: <Title>

**Started**: <ISO timestamp>
**Status**: in_progress | paused | done | failed
**Estimated Steps**: N
**Last Updated**: <ISO timestamp>

## Steps

- [ ] 1. First step
- [ ] 2. Second step
- [x] 3. Completed step ✓ (2026-03-02T22:05:00+08:00)
- [!] 4. Failed step — <error summary>

## Log

### Step 3 — 2026-03-02T22:05:00+08:00
Result or notes here.

### Error — 2026-03-02T22:07:00+08:00
What failed and how it was handled.

## Result

(Fill when done — final summary for the user)
```

## During Execution

After **every step** (success or failure):
- Update the checkbox in Steps (`[x]` done, `[!]` failed)
- Append a Log entry with timestamp and key findings
- Update `Last Updated` timestamp

On failure:
- Mark step `[!]` with error summary
- Try an alternative approach if obvious
- If truly stuck, set Status to `paused` and note what's needed

## Progress Reporting (Cron)

At task start, spawn a cron reporter using `exec`:

```bash
openclaw cron add "task-report-<SLUG>" \
  --schedule "*/15 * * * *" \
  --message "Read .tasks/<SLUG>.md and send a Feishu message to the user with progress update. Include: completed steps, current step, blockers if any. Keep it under 5 sentences. Remove this cron when Status=done or Status=failed." \
  --once-complete
```

Adjust interval based on task scope:
- Quick task (<30 min): every 10 min
- Medium task (30 min–2 hr): every 15 min  
- Long task (>2 hr): every 30 min

## On Task Completion

1. Fill in `## Result` section with a clear summary
2. Set `Status: done`
3. Send a final Feishu message: task name, what was accomplished, any caveats
4. Remove the progress cron

## On Task Failure / Getting Stuck

1. Set `Status: paused`
2. Document exactly what was tried and what's blocked
3. Send Feishu message alert immediately (don't wait for cron)
4. Do NOT silently stop — always notify

## Resuming a Paused Task

When asked to continue a task:
1. Read `.tasks/<SLUG>.md`
2. Find the last completed step
3. Continue from there
4. Re-spawn reporter cron if needed

## Multi-Task Awareness

If multiple tasks are running, maintain separate files per task. On heartbeat, check `.tasks/` for any `in_progress` tasks and include a brief status in heartbeat responses.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Task assigned | Create file, decompose, spawn cron, start |
| Step done | Update `[x]`, append log |
| Step failed | Mark `[!]`, try alternative, log error |
| Truly stuck | Set `paused`, WhatsApp alert immediately |
| Task complete | Fill Result, set `done`, final message, remove cron |
| Asked for update | Read task file, summarize current state |
