---
name: subagent-watchdog
version: 0.1.0
description: Watchdog for OpenClaw subagent runs: enforce a completion marker by deadline and alert if missing.
---

# Subagent Watchdog

A small reliability tool for agentic workflows.

## What it does
- After you spawn a subagent with a **label**, start a watchdog timer.
- The subagent must write a **completion marker** file.
- If the marker is missing when the timer expires, the watchdog alerts (or exits non-zero so the caller can restart).

## Files
- `watch.sh` — watchdog runner
- `SUBAGENT_CONTRACT.md` — what the subagent must do

## Usage

### 1) Enforce the contract in your subagent prompt
Tell the subagent to:
- write full results to the instructed project files
- write a marker file: `subagent-watchdog/state/<label>.done`

### 2) Start the watchdog

```bash
# explicit wait (seconds)
./watch.sh "my-subagent-label" 601

# or omit wait_seconds to read from ~/.openclaw/openclaw.json:
#   caliban.subagentWatchdog.maxRuntimeSeconds (+1 second)
./watch.sh "my-subagent-label"
```

## Notification
By default `watch.sh` prints a failure message and **tries** to notify using OpenClaw messaging if:
- `OPENCLAW_BIN` and `WATCHDOG_CHAT_ID` are set.

Config read (optional):
- Reads `OPENCLAW_CONFIG_PATH` or `~/.openclaw/openclaw.json` for `caliban.subagentWatchdog.maxRuntimeSeconds`.

This keeps the skill portable: you can use it with or without OpenClaw messaging.
