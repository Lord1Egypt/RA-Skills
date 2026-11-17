# Timer Skill — Build Monitor

A minimal timer skill for one-shot async checks (build monitoring, long-running tasks).
Wraps `sessions_spawn` with named timer tracking and status reporting.

## Usage

```bash
# Set a timer
$timer "check eas build in 20 minutes" --name eas-build-v018

# Check active timers
$timer list

# Cancel a timer
$timer cancel eas-build-v018
```

## Architecture

```
User sets timer → Parse intent → Spawn subagent (isolated, timeout) 
  → Subagent sleeps → Checks status → Reports back via message
  → If success: update state, notify user
  → If timeout: update state, notify user "timer expired"
```

## Files

- `SKILL.md` — This file. Usage + workflow.
- `scripts/timer.sh` — CLI wrapper. Parses `$timer` commands, spawns subagents.
- `scripts/state.sh` — CRUD timer state (JSON file in `~/.openclaw/timers/`).

## Why BYO Instead of NervTimer

| NervTimer | This Skill |
|-----------|------------|
| General purpose (any reminder) | Specialized for build monitoring |
| Nagging every 5 min (annoying) | Single check + report back |
| Requires cron tool + state files | Subagent spawn (already works) |
| Needs intent parsing/validation | Simple: "check build in N min" |
| Escalation logic | No escalation needed |

**Trade-off:** Subagent pattern is simpler but doesn't survive session restarts. For persistent timers across restarts, use OpenClaw native `cron` tool or install NervTimer.

## Why BYO Instead of NervTimer

| NervTimer | This Skill |
|-----------|------------|
| General purpose (any reminder) | Specialized for build monitoring |
| Nagging every 5 min (annoying) | Single check + report back |
| Requires cron tool + state files | Subagent spawn (already works) |
| Needs intent parsing/validation | Simple: "check build in N min" |
| Escalation logic | No escalation needed |

**Trade-off:** Subagent pattern is simpler but doesn't survive session restarts. For persistent timers across restarts, use OpenClaw native `cron` tool or install NervTimer.

## State Format

```json
{
  "timers": {
    "eas-build-v018": {
      "id": "eas-build-v018",
      "status": "running",
      "createdAt": "2026-05-18T04:35:00Z",
      "expiresAt": "2026-05-18T04:55:00Z",
      "task": "check eas build status",
      "sessionKey": "agent:main:subagent:xxx",
      "result": null
    }
  }
}
```

## Commands

### `$timer <description>`
Spawn a subagent to execute the described task after the implied delay.
If no delay is stated, ask the user for clarification.

### `$timer list`
Show all active timers with status and time remaining.

### `$timer cancel <name>`
Kill the subagent session and mark timer as cancelled.

## Implementation Notes

- Uses `sessions_spawn` with `mode="run"` and `runTimeoutSeconds`
- Subagent receives the full task description + current context
- Subagent reports back via `sessions_send` or completion event
- No cron dependency — pure subagent-based
- State file is human-readable JSON for debugging
