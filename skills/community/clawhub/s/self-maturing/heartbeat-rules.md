# Heartbeat Rules

Keeps ~/self-improving/ organized without creating churn or losing data.

## Source of Truth

Workspace HEARTBEAT.md snippet stays minimal. This file is the stable contract.
Mutable run state lives only in ~/self-improving/heartbeat-state.md.

## Every Heartbeat

1. Ensure ~/self-improving/heartbeat-state.md exists
2. Write `last_heartbeat_started_at` immediately (ISO 8601)
3. Read previous `last_reviewed_change_at`
4. Scan ~/self-improving/ for files changed after that moment (exclude heartbeat-state.md)

## If Nothing Changed

- Set `last_heartbeat_result: HEARTBEAT_OK`
- Return HEARTBEAT_OK

## If Something Changed

Conservative organization only:

- Refresh index.md if counts or file references drifted
- Compact oversized files by merging duplicates or summarizing repetition
- Move clearly misplaced notes to the right namespace (only when unambiguous)
- Preserve confirmed rules and explicit corrections exactly
- Check memory.md line count — if >100, demote oldest unconfirmed entries to WARM
- Update `last_reviewed_change_at` only after clean review

## Cold-Boot Recovery (on first heartbeat after restart)

If `last_heartbeat_started_at` is older than the current session start:
1. Read SESSION-STATE.md — verify it's current
2. Read ~/self-improving/memory.md — verify HOT tier is loaded
3. Log recovery in heartbeat-state.md

## Safety Rules

- Most heartbeat runs should do nothing
- Prefer append, summarize, or index fixes over large rewrites
- Never delete data, empty files, or overwrite uncertain text
- Never reorganize files outside ~/self-improving/
- If scope is ambiguous, leave files untouched and record a suggested follow-up

## State Fields

Keep ~/self-improving/heartbeat-state.md simple:

- `last_heartbeat_started_at`
- `last_reviewed_change_at`
- `last_heartbeat_result`
- `last_actions`
