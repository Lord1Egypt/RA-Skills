---
name: reminder
description: Use when user wants to set a reminder, timer, or scheduled notification.
triggers: ["提醒", "remind", "闹钟", "定时", "分钟后", "小时后"]
version: 1.0.0
---

# ⏰ Reminder Skill

> Set reminders and scheduled notifications

## Usage

Use `yuanbao_remind` tool:
```json
{
  "action": "add",
  "content": "Reminder text",
  "time": "5m" | "1h" | "2025-01-01T12:00:00Z",
  "name": "optional-name"
}
```

## Time Formats

| Format | Example | Use Case |
|--------|---------|----------|
| Relative | `5m` | 5 minutes |
| Relative | `1h30m` | 1.5 hours |
| Relative | `2d` | 2 days |
| Cron | `0 9 * * *` | Daily at 9am |
| Absolute | `2025-01-01T12:00:00Z` | Specific time |

## Example Triggers

- "5分钟后提醒我喝水"
- "1小时后提醒我开会"
- "每天早上9点提醒我..."

## Response

After setting:
```
✅ Reminder set: [内容]
⏰ [时间]
```

Check status field - `ok` means success, `PENDING_CRON_CALL` needs cron tool.
