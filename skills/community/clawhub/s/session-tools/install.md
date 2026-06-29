# Install Session ID Hook

Register the `session-id-inject.sh` hook in `settings.json` so that every session automatically receives its ID in context.

## When to Use

- After installing `claude-session` skill via `clawhub install`
- When setting up a new machine/environment
- When session ID is not appearing in context

## Prerequisites

- `session-id-inject.sh` must exist at one of:
  - `~/.claude/skills/claude-session/scripts/session-id-inject.sh` (ClawHub install — preferred)
  - `~/.claude/hooks/session-id-inject.sh` (legacy location)
- `jq` must be available in PATH

## Installation Steps

### 1. Verify Script Exists

```bash
ls ~/.claude/skills/claude-session/scripts/session-id-inject.sh 2>/dev/null \
  || ls ~/.claude/hooks/session-id-inject.sh 2>/dev/null \
  || echo "MISSING — run: clawhub install claude-session"
```

### 2. Register in settings.json

Add to `SessionStart` and `UserPromptSubmit` hooks. The script accepts the event name as first argument.

**SessionStart** (no argument needed — defaults to `SessionStart`):
```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/skills/claude-session/scripts/session-id-inject.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**UserPromptSubmit** (pass `UserPromptSubmit` as argument):
```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/skills/claude-session/scripts/session-id-inject.sh UserPromptSubmit",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

> **Note:** Do NOT register in `Stop` hooks — Stop event rejects `SessionStart` hookEventName, and session ID context is not needed at session end.

### 3. Verify

Start a new session and check for the `Current session ID:` context in the first message.

## Hook Event Name

The script outputs `hookEventName` matching the event it runs under. This is critical — Claude Code rejects hooks that return the wrong event name.

| Event | Command | hookEventName |
|-------|---------|---------------|
| SessionStart | `bash session-id-inject.sh` | `SessionStart` |
| Stop | `bash session-id-inject.sh Stop` | `Stop` |
| UserPromptSubmit | `bash session-id-inject.sh UserPromptSubmit` | `UserPromptSubmit` |

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "Hook returned incorrect event name" | Missing event argument in Stop/other hooks | Add event name as first argument |
| Session ID not appearing | Hook not registered in settings.json | Run this install procedure |
| "jq: command not found" | jq not installed | Install via `scoop install jq` or `brew install jq` |
