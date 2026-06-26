# OpenClaw 2026.2.21+ Integration Guide

Configuration recommendations for running strudel-music as an OpenClaw skill with full Discord integration.

## Thread-Bound Subagent Sessions

Each `/strudel` compose invocation can spawn a sub-agent in its own Discord thread.
Users get a dedicated thread for render progress, iteration ("make it darker"), and playback.

### Config (`openclaw.json`)

```json5
{
  "session": {
    "threadBindings": {
      "enabled": true,
      "ttlHours": 24
    }
  },
  "channels": {
    "discord": {
      "threadBindings": {
        "enabled": true,
        "spawnSubagentSessions": true
      }
    }
  }
}
```

### Agent Usage

When handling `/strudel <prompt>`, the skill should spawn with `thread: true`:

```javascript
// In the agent's dispatch logic:
sessions_spawn({
  task: `Compose a Strudel pattern for: "${prompt}". Use the skill at ${skillPath}.`,
  mode: "run",
  thread: true,
  label: `strudel-compose-${Date.now()}`
})
```

The sub-agent gets its own Discord thread where it can post render progress and the final audio.

## Lifecycle Status Reactions

Use ack reactions to show render phases:

| Phase | Emoji | Meaning |
|-------|-------|---------|
| Received | 🎵 | Pattern received, queuing |
| Rendering | 🔧 | Offline render in progress |
| Done | ✅ | Audio ready |
| Error | ❌ | Render failed |

### Implementation

The agent adds reactions at each phase:

```
1. User sends `/strudel dark ambient`
2. Agent reacts 🎵 (received)
3. Agent starts render → reacts 🔧 (removes 🎵)
4. Render completes → reacts ✅ (removes 🔧)
5. Posts MP3 attachment
```

This is done via the agent's normal message tool:
```
message(action=send, channel=discord, target=<channel>, emoji=🎵, messageId=<trigger-msg>)
```

## Streaming Preview (Partial Updates)

Live-updating draft messages during render. Config:

```json5
{
  "channels": {
    "discord": {
      "streaming": "partial"  // enables draft message updates
    }
  }
}
```

The agent can post progress updates during rendering:
```
🎵 Rendering dark-ambient-001...
├ Pattern evaluated: 47 haps
├ Scheduled: 23/47 (48%)
├ Duration estimate: 12.3s
└ ██████░░░░ 48%
```

## Ephemeral Responses

Keep `/strudel` responses ephemeral by default (only invoker sees them) to reduce channel clutter during iteration:

```json5
{
  "channels": {
    "discord": {
      "ephemeral": true  // slash command responses default to ephemeral
    }
  }
}
```

## Recommended Full Config

```json5
{
  "session": {
    "threadBindings": { "enabled": true, "ttlHours": 24 }
  },
  "channels": {
    "discord": {
      "threadBindings": {
        "enabled": true,
        "spawnSubagentSessions": true
      },
      "streaming": "partial"
    }
  },
  "messages": {
    "ackReaction": "🎵"  // or "" to disable
  }
}
```

## Notes

- Thread-bound sessions require OpenClaw 2026.2.21+
- `spawnSubagentSessions` is opt-in (default: false)
- Lifecycle reactions are agent-driven (no special config needed, just emoji reactions)
- Streaming preview depends on the Discord provider supporting partial message updates
- All features work with the existing `user-invocable: true` SKILL.md setting
