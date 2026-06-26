---
name: session-cleaner
description: Clean up stale OpenClaw session files. Keep the current main session and all group chat sessions; move everything else to a backup directory. Use when performing periodic maintenance, heartbeat cleanup, or when the user asks to clean up sessions.
---

# Session Cleaner

Clean stale session transcript files from `~/.openclaw/agents/main/sessions/`.

## Rules

- **Always keep**: current main session (the one with `agent:main:main` key that is active)
- **Always keep**: all group chat sessions (target address contains `oc_`)
- **Move to backup**: everything else (old main sessions, completed sub-agents, API sessions, cron/heartbeat transcripts)
- **Never delete**: all moved files go to `sessions/backup/`, recoverable

## Usage

```bash
bash scripts/clean-sessions.sh [--dry-run]
```

- Default: move stale files to backup
- `--dry-run`: only report what would be moved, no changes
