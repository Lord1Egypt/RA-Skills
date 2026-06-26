---
name: restart-recovery
description: Make OpenClaw agent workflows restart-safe using checkpoint files, idempotent step tracking, wake/resume handoff, and stale-checkpoint monitoring. Use when users ask to recover from restarts, preserve progress across updates/config restarts, or implement checkpoint → restart → wake → resume patterns.
---

# Restart Recovery

Implement restart-safe execution with this sequence:
1. checkpoint
2. restart
3. wake
4. resume from file

## Use bundled scripts

- Use `scripts/checkpoint_tool.py` for deterministic checkpoint lifecycle:
  - `start`, `update`, `resume`, `complete`, `list`
- Use `scripts/checkpoint_selfcheck.py` for stale unfinished checkpoint alerts without LLM/tool-token usage.

## Required operating rules

- Write checkpoints before any restart-prone operation (config patch/apply, update, service restart, long multi-step jobs).
- Use atomic file writes (`.tmp` then rename).
- Track completed and remaining steps explicitly.
- Include an idempotency key per workflow to avoid duplicate side effects after resume.
- Never write secrets/tokens to checkpoint files.
- Acquire a resume lock before continuing unfinished work.

## Recommended checkpoint location

- Per agent: `memory/checkpoints/*.json`
- Shared/default workspace flows: `memory/checkpoints/*.json` at workspace root

## Startup instruction to add in AGENTS.md

Add this exact section:

```md
## Restart-safe workflow rule
On startup, check `memory/checkpoints/*.json` for unfinished workflows. If found, acquire resume lock, validate checkpoint schema/hash, and continue from the last completed idempotent step.
```

## No-LLM stale checkpoint monitor

Use host scheduler (launchd/systemd/cron), not LLM cron jobs.

- Run every 10 minutes.
- Alert only when unfinished checkpoints are older than threshold.
- Log to local file for audit.

## Suggested execution flow

1. `checkpoint_tool.py start` before risky step.
2. Perform step.
3. `checkpoint_tool.py update --complete <step> --step <next>`.
4. If restart happens, wake session/process.
5. On startup/re-entry, `checkpoint_tool.py resume` and continue.
6. `checkpoint_tool.py complete` when done.

## Validation checklist

- Simulate mid-work restart and verify resume from last completed step.
- Confirm idempotency (no duplicate sends/writes/actions).
- Confirm stale-check script only alerts after threshold.
- Confirm old checkpoint cleanup policy (expiry).
