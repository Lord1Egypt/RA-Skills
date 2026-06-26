---
description: "Check status of shark-exec background jobs"
---

# Shark Status

Check the current state of any shark-exec background jobs.

## Instructions

1. Read the file `$SKILL_DIR/shark-exec/state/pending.json` if it exists
2. If it doesn't exist or has no jobs, report "No active shark-exec jobs."
3. If jobs exist, for each job report:
   - Label
   - Command
   - How long it's been running (compare startedAt to now)
   - Whether it's past maxSeconds (overdue)
4. Also check if `.shark-done` exists in the skill directory and report its contents if so
5. Check if `SHARK_LOG.md` exists and show the last 10 lines if so
