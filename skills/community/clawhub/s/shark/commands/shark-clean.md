---
description: "Clean up shark state files (.shark-done, SHARK_LOG.md, pending.json)"
allowed-tools: ["Bash(rm -f:*)"]
---

# Shark Clean

Clean up all shark state files from previous runs.

## Instructions

Remove these files if they exist in `$SKILL_DIR`:
- `.shark-done`
- `SHARK_LOG.md`
- `shark-exec/state/pending.json`

Report what was cleaned up.
