---
name: autonomous
description: Exit copilot mode — return to autonomous mode with full worktree enforcement.
user_invocable: true
---

# Return to Autonomous Mode

> **Claude Code enforcement only** — Codex and Cursor default to autonomous unless a future adapter uses this shared controller.
> Shared mode controller: `.agents/skills/autonomous/scripts/`.

## Shared Controller

Mode is a setting with explicit values: `autonomous` and `copilot`.

For now, this skill owns the shared mode controller because `autonomous` is the default and safe fallback value. `/copilot` is an alias that sets `mode=copilot`; it should not own separate mode logic.

- `.agents/skills/autonomous/scripts/mode.sh` is the sourceable mode facade for all agents and hooks.
- `.agents/skills/autonomous/scripts/set-mode.sh` sets `mode=autonomous` or `mode=copilot`.
- `scripts/lib/session-state.sh` remains project infrastructure because status, detection, bootstrap, and hook code all use it.

## Activate

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
"$REPO_ROOT/.agents/skills/autonomous/scripts/set-mode.sh" autonomous
```

If the script does not exist, tell the user: "This project doesn't have mode switching scripts. You are already in autonomous mode by default."

## Confirmation

After activation, print:

```
Mode: autonomous
Worktree enforcement active. Full workflow pipeline.
```

## Behavior

Follow **autonomous mode** rules in `.claude/rules/operating-mode.md`.
Agents and hooks that need live mode state should source the shared helper or call `scripts/session-state get mode`; do not read raw mode-state files directly.
