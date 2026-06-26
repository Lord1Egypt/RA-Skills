# Portability Notes

## Primary runtime contract

The JavaScript runtime is intended to be reusable across workspaces and repository layouts.

Preferred invocation style:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/sync_ai_done.js
```

This avoids relying on workspace-specific current directories.

## Supported environment overrides

- `AI_WORKLOG_CONFIG` — absolute path to `todo/system/config.json`
- `AI_WORKLOG_ROOT` — dashboard root containing `NOW.md`, `history/`, and `system/`
- `AI_WORKLOG_TIMEZONE` — default timezone used for date boundaries
- `AI_WORKLOG_MAIN_REPORTS` — default reports dir used by `init_system.js`
- `AI_WORKLOG_CORTEX_REPORTS` — default reports dir used by `init_system.js`
- `AI_WORKLOG_TRADING_REPORTS` — default reports dir used by `init_system.js`
- `AI_WORKLOG_ROLLOVER_STATE` — optional explicit rollover state path override

## Default behavior

If `AI_WORKLOG_CONFIG` is not set, the runtime resolves the install root from:

1. `AI_WORKLOG_ROOT`, if provided
2. otherwise `./todo` relative to the current working directory

For reusable installations, prefer `AI_WORKLOG_CONFIG` so the runtime does not depend on the caller's working directory.

## Optional summary-cron installation

PulseFlow can optionally install two template-driven notification cron jobs:

- a 15:30 midday summary
- a 00:05 previous-day report (before rollover)

These jobs are intentionally **not** created by `init_system.js`.
They supplement the normal PulseFlow rollover schedule and should not replace it.
If you install the previous-day report cron, schedule the actual rollover later (recommended: 00:15).
They depend on deployment-specific choices:

- delivery channel and target
- account id
- timezone
- which agent should own the jobs
- where archives should be written

Configure those values under `notifications.summaryCrons` in `config.json`, then run:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_summary_crons.js
```

Use `--dry-run` first when reviewing changes:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_summary_crons.js --dry-run
```

## Privacy and publishability

The primary JS runtime avoids embedding personal machine paths.
Installation-specific paths belong in:

- `todo/system/config.json`
- local heartbeat/cron commands
- local operator docs outside the reusable skill bundle

Do not publish runtime instance data with reusable skill bundles.
