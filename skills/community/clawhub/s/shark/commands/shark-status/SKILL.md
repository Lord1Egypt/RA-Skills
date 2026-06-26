---
name: shark-status
description: "Check status of shark-exec background jobs, .shark-done, and SHARK_LOG.md"
---

# Shark Status

Check current shark state:

1. Read `$SKILL_DIR/../shark-exec/state/pending.json` — report active background jobs (label, command, elapsed time, whether overdue past maxSeconds)
2. If `.shark-done` exists in the skill base dir, show its contents
3. If `SHARK_LOG.md` exists, show the last 10 lines
4. If nothing exists, report "No active shark jobs."
