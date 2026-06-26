---
name: session-rotate-80
description: Auto-create a new session when OpenClaw context usage reaches 80% without requiring Mem0 or file memory systems. Use when users want default OpenClaw to proactively rotate sessions and avoid context overflow in long chats.
---

# Session Rotate 80

## Overview
Trigger a standard `[NEW_SESSION]` message when context usage reaches 80%.
This skill is memory-system-agnostic and works in plain default OpenClaw setups.

## Workflow
1. Read current context usage from runtime status.
2. Run `scripts/context_guard.py <used_tokens> <max_tokens>`.
3. If threshold reached, output the new-session trigger and handoff hint.
4. Keep old session only for short handoff, then continue in new session.

## Command
```bash
python scripts/context_guard.py <used_tokens> <max_tokens> --threshold 0.8 --channel boss
```

Example:
```bash
python scripts/context_guard.py 220000 272000 --threshold 0.8 --channel boss
```

## Expected Output
At or above threshold:
- `[ROTATE_NEEDED]`
- `[NEW_SESSION] 上下文达到80%（used/max），自动切换新会话`
- `[HANDOFF_HINT] ...`

Below threshold:
- `[ROTATE_NOT_NEEDED] ratio=x.xx < 0.800`

## Integration Hint (Heartbeat)
In heartbeat flow, after reading context usage:
1. Call `context_guard.py`.
2. If `[ROTATE_NEEDED]`, emit `[NEW_SESSION]...` directly.
3. Stop handling new tasks in old session except handoff confirmation.

## scripts/
- `scripts/context_guard.py`: threshold detector and trigger emitter (no memory dependency).
