---
name: seamless-restart
description: >-
  Seamless gateway restart with automatic context recovery and post-restart notification.
  Use whenever the agent needs to restart the OpenClaw gateway (config changes, updates,
  manual restarts). Ensures no context is lost and the user is always notified when the
  agent comes back online. Also use when the user mentions "restart", "reboot gateway",
  "apply config", or any action that triggers a gateway restart. This skill prevents the
  common problem of agents going silent after restarts.
metadata:
  openclaw:
    emoji: 🔄
---

# Seamless Restart

Zero-downtime gateway restart protocol with automatic context recovery. Prevents the
common problem where agents lose context and go silent after gateway restarts.

## Why This Exists

Gateway restarts (config changes, updates, manual restarts) cause context loss because
a new API session starts with no conversation history. Without this protocol, the agent
wakes up with no memory of what it was doing and no way to proactively notify the user.

## The Protocol

Every gateway restart MUST follow these three steps in order:

### Step 1: Save State to NOW.md

Before restarting, update `NOW.md` in the workspace root with:

```markdown
# NOW.md - Current State Snapshot

## Last Updated
- **Time**: [current timestamp]
- **Session**: [which channel/chat the user is in]
- **Status**: [what was happening]

## Active Tasks
- [list any in-progress tasks]

## Recent Context
- [key context points the next session needs to know]

## Post-Restart Action
- [specific actions to take after restart, e.g. notify user, continue task]
```

Keep it concise. This file is read on every session start, so avoid bloat.

### Step 2: Notify + Schedule Recovery Cron

Send a pre-restart notification to the user, then schedule a one-shot cron job
that fires ~1 minute after restart to trigger recovery:

**Send notification:**
```
message(action=send, channel=<current_channel>, target=<current_channel_id>,
  message="⚡ Restarting gateway — back in ~1 minute...")
```

**Schedule recovery cron:**
```
cron(action=add, job={
  "name": "restart-recovery",
  "schedule": {"kind": "at", "at": "<1 minute from now in ISO-8601 UTC>"},
  "payload": {
    "kind": "systemEvent",
    "text": "RESTART RECOVERY: You just restarted. Read NOW.md immediately.
      Then notify the user you are back and summarize what you were doing.
      Send the notification to the same channel the user was in before restart."
  },
  "sessionTarget": "main",
  "enabled": true
})
```

The cron job is automatically deleted after it fires (one-shot).

### Step 3: Execute Restart

Now restart the gateway:
```
gateway(action=restart, note="<human-readable reason>")
```

Or for config changes:
```
gateway(action=config.patch, raw=<config>, note="<reason>")
```

Both trigger a SIGUSR1 restart.

### Post-Restart (Automatic)

When the recovery cron fires after restart:

1. **Read NOW.md** to restore context
2. **Send recovery notification** to the user confirming the restart completed
3. **Resume any active tasks** listed in NOW.md
4. **Clear the Post-Restart Action section** of NOW.md (set to "none")

## Channel-Specific Notification

Adapt the notification target based on where the user was chatting:

| Channel | Notification Method |
|---------|-------------------|
| Discord | `message(action=send, channel=discord, target=<channelId>, guildId=<guildId>)` |
| Telegram | `message(action=send, channel=telegram, target=<chatId>)` |
| Other | Use the channel and target from the pre-restart session |

Always include the channel target in the NOW.md so the recovery cron knows where to send.

## Edge Cases

**Multiple restarts in quick succession:**
If another restart is needed before the recovery cron fires, cancel the old cron
and create a new one. Only one recovery cron should exist at a time.

**Restart during sub-agent tasks:**
Note any running sub-agents in NOW.md. After restart, sub-agents that were in progress
will have been terminated. The user should be informed which tasks were interrupted.

**Unexpected restarts (crashes):**
This protocol only covers intentional restarts. For crash recovery, the heartbeat
mechanism is the fallback — if the agent misses heartbeats, it should check NOW.md
on the next activation.

## Integration with AGENTS.md

Add this to your User Rules or Operations section:

```markdown
- **Gateway restart protocol**: Always use the seamless-restart skill for any
  gateway restart. Three steps: (1) update NOW.md, (2) notify + set recovery cron,
  (3) restart. Never restart without steps 1 and 2.
```

## Example: Full Restart Flow

```
1. Agent needs to restart for a config change

2. Agent updates NOW.md:
   "Status: Applying new Gemini API key. Session: Discord #misc.
    Post-Restart: Notify Zihao in Discord #misc that config is applied."

3. Agent sends: "⚡ Applying config change — restarting, back in ~1 min..."

4. Agent creates one-shot cron for T+60s:
   systemEvent → "RESTART RECOVERY: Read NOW.md, notify user, resume."

5. Agent calls: gateway(action=config.patch, raw={...}, note="New API key")

6. Gateway restarts. ~60s later, cron fires.

7. Agent reads NOW.md, sends: "✅ Back online. Config change applied successfully."

8. Agent clears Post-Restart Action in NOW.md.
```
