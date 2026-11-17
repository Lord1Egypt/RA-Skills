# openclaw-session-closeout

A read-only end-of-session audit skill for [OpenClaw](https://github.com/openclaw/openclaw).
It catches loose ends before your context resets, and it writes nothing at all.

## What it does

- **Task hygiene.** Reports whether `MASTER_TODO.md` is fresh, stale, or missing. Never rebuilds it.
- **Repo hygiene.** Lists git repos with uncommitted changes. Never commits or discards. Reads status with the scanned repo's fsmonitor and hooks pinned off, so auditing a repo cannot run that repo's code.
- **Project-doc hygiene** (optional). With `CLOSEOUT_PROJECTS="alpha|beta"`, warns when a project's `STATUS.md`, `DECISIONS.md`, `PROJECT.md`, or `BACKLOG.md` was not updated today. Slugs are validated as plain directory names.
- **Automation hygiene.** Reports `not_verified` so you check cron health by hand.

Recording the closeout is the caller's job. The script hands you the findings; you decide what to write down.

## 1.1.1: read-only audit

- **Removed every write.** No daily-memory append, no `mkdir`, no file creation. Earlier versions appended a closeout block to `memory/YYYY-MM-DD.md`; that recording step now belongs to whoever runs the audit.
- **Removed the environment-controlled paths.** `OPENCLAW_WORKSPACE` and `CLOSEOUT_PROJECTS_DIR` no longer steer the script. The workspace root is the current directory, and projects live under `projects/`.
- **Validated project slugs.** Separators, `..`, and absolute paths are rejected and reported instead of being looked up.
- **Hardened the repo scan.** `core.fsmonitor` and `core.hooksPath` are pinned off and optional locks are left alone.
- **Validated the stale threshold.** `CLOSEOUT_TODO_STALE_HOURS` must be digits; anything else falls back to 24.

## 1.1.0: security-first refresh

- Removed automatic execution of `scripts/build-master-todo.py` and sourcing of `scripts/closeout-hooks.sh`. The script no longer discovers and runs anything in your workspace.
- Fixed the status bug: memory used to record `Status: ok` before checks were evaluated.
- Trigger narrowed to explicit closeout requests.
- Portable `stat` (GNU and BSD).

## Install

```bash
clawhub install session-closeout
```

Or copy `SKILL.md` and `scripts/` into `skills/session-closeout/` in your workspace.

## Usage

```bash
CLOSEOUT_PROJECTS="alpha|beta" \
bash skills/session-closeout/scripts/session-closeout.sh
```

Output is `key=value` lines (`CLOSEOUT_STATUS`, `WORKSPACE_ROOT`, `MASTER_TODO_STATUS`, `DIRTY_REPO_COUNT`, `PROJECT_DOC_WARNINGS`, `REJECTED_SLUG_COUNT`, `EXCEPTION_n`). See `SKILL.md` for the full table.

## Configuration

| Item | Value |
|---|---|
| Workspace root | the current directory, not configurable |
| Master TODO | `./MASTER_TODO.md` |
| Projects dir | `./projects` |
| Stale threshold | 24 hours, or `CLOSEOUT_TODO_STALE_HOURS` if it is digits |

## Requirements

Bash 4+ and git.

## License

MIT
