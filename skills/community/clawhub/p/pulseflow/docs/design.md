# Design

## Goal

Provide a reusable daily work system for OpenClaw-based operations where:

- human work remains readable in one Markdown dashboard
- AI work is captured as append-only logs
- live AI sections are always derived, never hand-maintained
- daily rollover archives history and prepares the next day automatically
- usage visibility stays in the live dashboard while finalized usage history stays monthly

## Design principles

1. Single source of truth for current work
2. Append-only source logs for AI activity
3. Derived views instead of incremental Markdown mutation where possible
4. Low-friction human editing
5. Deterministic rollover at day boundary
6. Recoverable state through simple files
7. Keep current state lightweight and history monthly

## Components

### Dashboard
`todo/NOW.md`

Holds current human task state, the current week's usage table, and today's AI summary.

### AI source logs
`reports/<agent>-ai-log-YYYY-MM-DD.jsonl`

Hold one JSON object per completed work unit.

### History
`todo/history/YYYY-MM.md`

Stores archived daily human completion snapshots, AI daily summaries, daily usage summaries, and weekly usage summaries.

### System state
- `todo/system/config.json`
- `todo/system/sync-state.json`
- `todo/system/rollover-state.json`

### Bootstrap and repair scripts
- `scripts/init_system.js`
- `scripts/repair_system.js`

These scripts make the system recoverable when files are missing or the installation is only partially initialized.

### Validation script
- `scripts/validate_system.js`

This script exercises the JavaScript runtime end-to-end in a temporary installation so release checks do not depend on the live dashboard.

## Why AI logs are append-only

Append-only logs are resilient, easy to inspect, and safer than shared-write dashboards.
They also allow rebuilding the visible AI section after crashes or missed syncs.

## Why the AI sections are derived

If agents wrote directly to the dashboard:

- concurrent writes would conflict
- formatting would drift
- usage totals would become unreliable
- cleanup and repair would be harder

By rebuilding from logs and OpenClaw usage summaries, the dashboard stays stable.

## Why rollover is cron-based

Day-boundary state changes are deterministic and should not depend on heartbeat timing.
A fixed cron at 00:05 is more reliable than hoping the next heartbeat lands after midnight.

## Why monthly history is preferred

PulseFlow keeps the live surface small and the archive surface predictable.
Instead of scattering usage history into extra standalone files, month files become the single history container.
That makes the system easier to browse:

- current work → `NOW.md`
- past work and past usage → `history/YYYY-MM.md`

## Recovery philosophy

This system is designed around file repair rather than hidden internal state.
If runtime files are missing, the operator should be able to rebuild the working surface with simple scripts.

Minimum recovery set:

- recreate dashboard if missing
- recreate sync state if missing
- recreate rollover state if missing
- preserve healthy files when repairing
