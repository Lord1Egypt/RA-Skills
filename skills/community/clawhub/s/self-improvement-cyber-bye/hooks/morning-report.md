---
name: self-improvement-cyber-bye-morning-report
description: Temp cron hook. Fires at 10 AM IST when escalated errors need owner review. Auto-deletes after firing once. Can also be set manually by owner.
type: temp
fire_once: true
auto_delete: true
---

# Morning Report Hook — 10 AM IST (Temp)

## On Fire: Escalation Report

Present at session start:

```
Good morning! Quick self-improvement report:

ESCALATED ERRORS PENDING YOUR REVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[For each escalated error — max 3 lines each:]

1. [slug] — [type] — [severity]
   What went wrong: [one line]
   What I tried:    [one line or "not self-fixable"]
   What you need:   [one line]

PATTERNS (if any)
━━━━━━━━━━━━━━━━
[pattern-id]: [type] — N occurrences — [root cause one-liner]

To resolve: tell me what to fix → I'll promote to improvements.
To skip: "skip <slug>" → I'll archive with a note.
```

---

## Auto-Delete After Fire

1. Move this file to `crons/completed/<cron-id>.md`
2. Update memory index cron status → fired
3. Remove from soul [ACTIVE CRONS]
4. Append soul [SESSION LOG]

---

## Manual Temp Cron Creation

When owner says "remind me at <time>" or "set a cron for <time>":

1. Parse time → convert to IST if needed
2. Create `crons/active/temp-<YYYY-MM-DD-HH-MM>-<purpose-slug>.md`:

```markdown
---
name: <purpose>
type: temp
schedule_ist: <HH:MM IST>
schedule_date: <YYYY-MM-DD>
purpose: <what to do when it fires>
fire_once: true
auto_delete: true
status: active
created: YYYY-MM-DD HH:MM IST
---
# Temp Cron: <purpose>
## Task
[What to do when this fires]
## Context
[Any context needed]
```

3. Confirm: "Temp cron set — fires at <time> IST and auto-deletes."
4. Add to soul [ACTIVE CRONS]

## Cancellation

"cancel that reminder" → move to completed/ with status: cancelled → confirm.
