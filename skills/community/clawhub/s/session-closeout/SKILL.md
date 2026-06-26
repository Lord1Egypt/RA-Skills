---
name: session-closeout
description: Run a structured end-of-session closeout that checks repo hygiene, refreshes a master task list, appends a closeout block to daily memory, and verifies automation health. Use when the user asks to end a session, run closeout, wrap up, or requests /closeout. Also useful as a periodic hygiene check between work blocks.
---

# Session Closeout

Non-destructive end-of-session checklist. Catches loose ends before context resets.

## Quick Start

Run the closeout script from the workspace root:

```bash
bash "$(dirname "$0")/../scripts/session-closeout.sh"
```

Or with overrides (pipe-delimited):

```bash
CLOSEOUT_OUTCOMES="Shipped feature X|Fixed bug Y" \
CLOSEOUT_BLOCKERS="Waiting on API key" \
bash scripts/session-closeout.sh
```

## What It Checks

1. **Repo hygiene** — Scans for dirty git repos (uncommitted changes). Reports but never auto-commits.
2. **Task hygiene** — Refreshes `MASTER_TODO.md` from project backlogs if `scripts/build-master-todo.py` exists. Skipped gracefully if not.
3. **Memory hygiene** — Appends a timestamped closeout block to `memory/YYYY-MM-DD.md` with outcomes, blockers, and next-start items.
4. **Automation hygiene** — Flags that cron/automation health should be manually verified.

## Configuration

The script auto-detects the workspace root (defaults to `$OPENCLAW_WORKSPACE` or the current working directory). Key paths:

| Item | Default | Override |
|------|---------|----------|
| Workspace root | `$OPENCLAW_WORKSPACE` or cwd | Set env var |
| Daily memory dir | `$ROOT/memory/` | — |
| Master TODO | `$ROOT/MASTER_TODO.md` | — |
| TODO builder | `$ROOT/scripts/build-master-todo.py` | Skip if missing |

## Output

The script prints structured key=value pairs. Report a concise summary to the user:

- **CLOSEOUT_STATUS** — `ok`, `warning`, or `error`
- **DIRTY_REPO_COUNT** — number of repos with uncommitted changes
- **MASTER_TODO_REFRESH** — whether the task list was refreshed
- **EXCEPTION_COUNT** — total issues found

If dirty repos are found, list them but do **not** auto-commit or discard. Let the user decide.

## Customization

- To add project-specific checks (e.g., pushing status to a dashboard), extend the script or add a `scripts/closeout-hooks.sh` that the main script sources if present.
- Override closeout bullets via environment variables: `CLOSEOUT_OUTCOMES`, `CLOSEOUT_BLOCKERS`, `CLOSEOUT_NEXT` (pipe-delimited).
