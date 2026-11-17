# Cron Task Template

> ⚠️ Replace placeholders before use

---

## ⚠️ Important: Replace Placeholders

**Before executing any commands, you MUST replace:**
- `{YOUR_USER_ID}` → Your actual OpenClaw user ID (e.g., `ou_xxxxxxxxxxxxxxxx`)
- `{CHANNEL}` → Your preferred channel (`feishu`, `telegram`, `whatsapp`, etc.)

**Find your user ID**:
```bash
openclaw status
```

---

## One-Time Task

```bash
openclaw cron add \
  --name "{Task Name}" \
  --at "+{N}m" \
  --session isolated \
  --channel {CHANNEL} \
  --to "user:{YOUR_USER_ID}" \
  --message "{Execute this task}" \
  --tz "Asia/Shanghai" \
  --description "{Task description}"
```

**Example** (10 minute reminder):
```bash
openclaw cron add \
  --name "Meeting Reminder" \
  --at "+10m" \
  --session isolated \
  --channel feishu \
  --to "user:ou_xxxxxxxxxxxxxxxx" \
  --message "Reminder: Meeting in 10 minutes" \
  --tz "Asia/Shanghai" \
  --description "Remind meeting in 10 minutes"
```

---

## Periodic Task

```bash
openclaw cron add \
  --name "{Task Name}" \
  --cron "{Cron expression}" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --channel {CHANNEL} \
  --to "user:{YOUR_USER_ID}" \
  --message "{Execute this task}" \
  --description "{Task description}"
```

**Example** (Daily news at 9am):
```bash
openclaw cron add \
  --name "Daily News Push" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --session isolated \
  --channel feishu \
  --to "user:ou_xxxxxxxxxxxxxxxx" \
  --message "Search AI news and create briefing" \
  --description "Daily AI news at 9am"
```

---

## Cron Expression Reference

| Description | Expression |
|-------------|------------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every hour | `0 * * * *` |
| Daily at 9am | `0 9 * * *` |
| Every Monday 9am | `0 9 * * 1` |
| First of month | `0 0 1 * *` |

---

## Management Commands

```bash
# List tasks
openclaw cron list

# Run task (test)
openclaw cron run {task_id}

# Remove task
openclaw cron remove {task_id}
```

---

## ✅ Safety Checklist

Before executing:
- [ ] Replaced `{YOUR_USER_ID}` with actual ID
- [ ] Replaced `{CHANNEL}` with preferred channel
- [ ] Verified timezone
- [ ] Tested with non-destructive task first

---

**Template Version**: 2.0.0  
**Note**: This template uses placeholders for safety. Always replace before use.
