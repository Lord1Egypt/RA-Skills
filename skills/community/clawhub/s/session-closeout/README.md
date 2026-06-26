# openclaw-session-closeout

A structured end-of-session closeout skill for [OpenClaw](https://github.com/openclaw/openclaw). Catches loose ends before your context resets.

## What It Does

Runs a non-destructive checklist at the end of every work session:

- **Repo hygiene** — Scans for dirty git repos with uncommitted changes. Reports them but never auto-commits.
- **Task hygiene** — Refreshes your `MASTER_TODO.md` from project backlogs (if a builder script exists). Skips gracefully if not.
- **Memory hygiene** — Appends a timestamped closeout block to your daily memory file (`memory/YYYY-MM-DD.md`) with outcomes, blockers, and next-start items.
- **Automation hygiene** — Flags cron/automation health for manual review.
- **Hooks** — Extensible via `scripts/closeout-hooks.sh` for project-specific checks.

## Install

### From ClawHub

```bash
clawhub install session-closeout
```

### Manual

Copy `SKILL.md` and `scripts/` into your OpenClaw workspace `skills/session-closeout/` directory.

## Usage

Once installed, trigger it naturally in any OpenClaw session:

- "Run closeout"
- "Wrap up this session"
- `/closeout` (if configured as a slash command)

The agent reads the skill and runs the closeout script automatically.

### Environment Variable Overrides

Customize the closeout summary with pipe-delimited values:

```bash
CLOSEOUT_OUTCOMES="Shipped auth flow|Fixed login bug" \
CLOSEOUT_BLOCKERS="Waiting on DNS propagation" \
CLOSEOUT_NEXT="Deploy to prod" \
bash scripts/session-closeout.sh
```

## Output

The script prints structured key-value pairs for the agent to summarize:

| Key | Values | Description |
|-----|--------|-------------|
| `CLOSEOUT_STATUS` | `ok`, `warning`, `error` | Overall session health |
| `DIRTY_REPO_COUNT` | `0`+ | Repos with uncommitted changes |
| `MASTER_TODO_REFRESH` | `yes`, `no` | Whether the task list was refreshed |
| `EXCEPTION_COUNT` | `0`+ | Total issues found |

## Configuration

The script auto-detects your workspace. Override with the `OPENCLAW_WORKSPACE` environment variable.

| Item | Default | Override |
|------|---------|----------|
| Workspace root | `$OPENCLAW_WORKSPACE` or cwd | Set env var |
| Daily memory dir | `$ROOT/memory/` | — |
| Master TODO | `$ROOT/MASTER_TODO.md` | — |
| TODO builder | `$ROOT/scripts/build-master-todo.py` | Skip if missing |
| Custom hooks | `$ROOT/scripts/closeout-hooks.sh` | Source if present |

## Design Principles

- **Non-destructive** — Never commits, deletes, or modifies your code. Read-only except for appending to the daily memory file.
- **Graceful degradation** — Missing scripts, missing files, no git repos? It handles all of it without errors.
- **Extensible** — Add a `closeout-hooks.sh` to plug in your own checks (dashboard pushes, status syncs, etc.).

## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw)
- Bash 4+
- Git (for repo hygiene scanning)

## License

MIT
