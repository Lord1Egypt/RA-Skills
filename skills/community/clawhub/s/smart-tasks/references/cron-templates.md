# Cron Job Templates

All cron jobs should use **Sonnet-class models** for cost efficiency.
Adjust `--channel` to match your messaging surface (telegram, discord, etc.).

## 1. Daily Morning Briefing

**Schedule**: Every day at 08:00  
**Purpose**: Overdue alerts, today's priorities, recommended work order

```bash
openclaw cron add \
  --name "daily-task-briefing" \
  --schedule "0 8 * * *" \
  --channel telegram \
  --model sonnet \
  --prompt "Perform a daily task briefing.

1. Read tasks/INDEX.md for current status.
2. If overdue tasks exist, warn at the top.
3. List today's and this week's deadlines by priority.
4. Read relevant task files from tasks/active/ for context (estimated hours, notes).
5. Suggest a recommended work order with brief reasoning.
6. Check recent memory/ entries for additional context.

Format: Concise message under 500 chars. Use emoji. Include a morning greeting.
If no active tasks, send a brief 'all clear' message."
```

## 2. Deadline Check

**Schedule**: Every day at 12:00 and 18:00  
**Purpose**: Alert only when deadlines are imminent or overdue

```bash
openclaw cron add \
  --name "deadline-check" \
  --schedule "0 12,18 * * *" \
  --channel telegram \
  --model sonnet \
  --prompt "Check for imminent task deadlines.

1. Read tasks/INDEX.md and check today's date.
2. Alert ONLY for tasks matching these conditions:
   - Overdue (due < today)
   - Due today (D-0)
   - Due tomorrow (D-1)
   - High estimated_hours AND due in 2-3 days
3. If NO tasks match → do nothing (HEARTBEAT_OK, no message).
4. If tasks match → send a brief alert with task IDs and deadlines.

Format: Under 200 chars. Only matching tasks. Silent if nothing urgent."
```

## 3. Weekly Review

**Schedule**: Every Sunday at 20:00  
**Purpose**: Full review, cleanup, and planning

```bash
openclaw cron add \
  --name "weekly-task-review" \
  --schedule "0 20 * * 0" \
  --channel telegram \
  --model sonnet \
  --prompt "Perform a weekly task review.

1. Read tasks/INDEX.md and ALL files in tasks/active/.
2. Summarize tasks completed this week (scan tasks/done/).
3. Preview next week's upcoming deadlines.
4. Detect stale tasks: active for 2+ weeks with no progress updates.
   Suggest: close, defer, or break down.
5. Archive cleanup: move tasks in tasks/done/ older than 30 days
   to tasks/archive/YYYY-QN/ (quarter based on completion date).
   Update file status to 'archived'.
6. Refresh INDEX.md: recalculate counters, re-sort sections, update date.
7. Send structured report to chat.

Format: Structured report with sections (Completed, Upcoming, Stale, Archived).
Keep actionable — user should be able to make quick decisions."
```

## Registration Summary

| Name | Schedule | Model | Est. Monthly Cost |
|------|----------|-------|-------------------|
| daily-task-briefing | `0 8 * * *` | sonnet | ~$1.50 |
| deadline-check | `0 12,18 * * *` | sonnet | ~$1.00 |
| weekly-task-review | `0 20 * * 0` | sonnet | ~$0.30 |
| **Total** | | | **~$2.80** |

Cost estimates assume ~5-10 active tasks and INDEX.md under 2KB.

## Customization Notes

- Adjust schedules to match your timezone and routine.
- Add `--channel discord` or `--channel slack` as needed.
- Morning briefing time should match when you typically start work.
- Deadline check can be reduced to once daily if alerts feel excessive.
- Weekly review day/time is flexible — some prefer Friday evening.
