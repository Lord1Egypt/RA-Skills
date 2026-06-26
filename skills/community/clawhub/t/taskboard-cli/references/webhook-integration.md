# Webhook & Discord Integration

The taskboard CLI itself makes no network calls. To add notifications, the agent reads hook output and acts on it.

## Pattern 1: Agent-Driven Notifications

When a task status changes and a hook fires, the CLI prints:
```
🔔 ON_DONE: message:CHANNEL_ID:✅ Task #5 completed
```

The agent parses this and uses its own messaging tools (e.g., OpenClaw `message` tool, `sessions_send`, etc.) to deliver the notification.

## Pattern 2: Discord Webhook (External)

If you want a standalone webhook notifier outside the agent, create a wrapper script:

```python
#!/usr/bin/env python3
"""Wrapper: runs taskboard command, parses hook output, sends Discord webhook."""
import subprocess, json, urllib.request, sys

result = subprocess.run(
    ["python3", "scripts/taskboard.py"] + sys.argv[1:],
    capture_output=True, text=True
)
print(result.stdout, end="")

# Parse hook lines
for line in result.stdout.splitlines():
    if line.startswith("🔔 ON_"):
        hook_type, _, instruction = line.partition(": ")
        # Send to Discord webhook
        # ... your webhook logic here
```

This wrapper lives **outside** the skill directory (not published to ClawHub).

## Pattern 3: OpenClaw Cron Integration

Use OpenClaw cron jobs to periodically check for task changes:

```
Schedule: every 5 minutes
Payload: "Check taskboard for recently completed tasks, notify #task-status channel"
```

## Webhook Config Example

For teams using the webhook pattern, store config in a separate file (not in the skill):

```json
{
  "discord_webhook": "https://discord.com/api/webhooks/...",
  "discord_status_thread": "1482856331923816650",
  "gateway_url": "http://localhost:18789",
  "hooks_token": "your-token",
  "agent_map": {
    "tech-lead": {"agentId": "shannon"},
    "code-engineer": {"agentId": "linus"}
  }
}
```
