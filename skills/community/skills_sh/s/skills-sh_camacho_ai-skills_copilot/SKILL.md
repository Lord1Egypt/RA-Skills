---
name: copilot
description: Enter copilot mode — human drives, Claude assists. Relaxes worktree enforcement, allows main commits.
user_invocable: true
---

# Enter Copilot Mode

> **Claude Code enforcement only** — Codex and Cursor default to autonomous unless a future adapter uses this shared controller.
> Alias for setting `mode=copilot` through the shared mode controller.

## Shared Controller

Mode is a setting with explicit values: `autonomous` and `copilot`.

This skill is an alias over the controller currently owned by `/autonomous`; keep behavior in one place unless this repo grows a neutral `/mode` skill later.

## Activate

```bash
REPO_ROOT="$(git rev-parse --show-toplevel)"
"$REPO_ROOT/.agents/skills/autonomous/scripts/set-mode.sh" copilot
```

If the script does not exist, tell the user: "This project doesn't have mode switching scripts. Install the ai-env template or add set-mode.sh manually."
If it fails for another reason, inform the user with the error message and stop.

## Confirmation

After activation, print:

```
Mode: copilot
Relaxed: worktree requirement, main branch protection
Workflow: menu mode — tell me to follow it or just lead
TTL: 4h sliding (renews on each prompt) / 12h absolute ceiling
```

## Behavior

Follow **copilot mode** rules in `.claude/rules/operating-mode.md`.
When the current task or plan completes, revert with `/autonomous`.
