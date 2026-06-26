# Cron Task Template (v2.2 Enhanced)

> ⚠️ Replace placeholders before use

---

## ⚠️ Important: Replace Placeholders

**Before executing any command, MUST replace:**
- `{YOUR_USER_ID}` → Your actual OpenClaw user ID (e.g., `ou_xxxxxxxxxxxxxxxx`)
- `{CHANNEL}` → Your preferred channel (`feishu`, `telegram`, `whatsapp`, etc)
- `{AGENT_ID}` → Agent ID that executes the task (e.g., `kk`)
- `{ACCOUNT_ID}` → Feishu account that sends the message (e.g., `kk-feishu`)

**Find Your User ID**:
```bash
openclaw status
```

**Find Agent's Account ID**:
```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
for b in d.get('bindings', []):
    print(f\"Agent {b['agentId']}: {b['match']['accountId']}\")
"
```

---

## Standard Configuration (Recommended) ⭐

```bash
openclaw cron add \
  --agentId "{AGENT_ID}" \
  --session "{AGENT_ID}" \
  --name "{Task Name}" \
  --cron "{Cron Expression}" \
  --tz "Asia/Shanghai" \
  --channel {CHANNEL} \
  --to "user:{YOUR_USER_ID}" \
  --accountId "{ACCOUNT_ID}" \
  --message "{Execute Content}" \
  --description "{Task Description}"
```

**Parameter Description**:
| Parameter | Description | Required |
|------|------|------|
| `--agentId` | Specify which agent executes the task | ✅ Required |
| `--session` | Use agent's dedicated session (inherits channel binding) | ✅ Required |
| `--accountId` | Specify which Feishu account sends the message | ✅ Required |

---

## One-time Task

```bash
openclaw cron add \
  --agentId "{AGENT_ID}" \
  --session "{AGENT_ID}" \
  --name "{Task Name}" \
  --at "+{N}m" \
  --session "{AGENT_ID}" \
  --channel {CHANNEL} \
  --to "user:{YOUR_USER_ID}" \
  --accountId "{ACCOUNT_ID}" \
  --message "{Execute this task}" \
  --tz "Asia/Shanghai" \
  --description "{Task Description}"
```

**Example** (Reminder in 10 minutes):
```bash
openclaw cron add \
  --agentId "main" \
  --session "main" \
  --name "Meeting Reminder" \
  --at "+10m" \
  --session "main" \
  --channel feishu \
  --to "user:ou_xxxxxxxxxxxxxxxx" \
  --accountId "default" \
  --message "Reminder: Meeting in 10 minutes" \
  --tz "Asia/Shanghai" \
  --description "Remind about meeting in 10 minutes"
```

---

## Recurring Task

```bash
openclaw cron add \
  --agentId "{AGENT_ID}" \
  --session "{AGENT_ID}" \
  --name "{Task Name}" \
  --cron "{Cron Expression}" \
  --tz "Asia/Shanghai" \
  --channel {CHANNEL} \
  --to "user:{YOUR_USER_ID}" \
  --accountId "{ACCOUNT_ID}" \
  --message "{Execute this task}" \
  --description "{Task Description}"
```

**Example** (Daily news push at 9am):
```bash
openclaw cron add \
  --agentId "main" \
  --session "main" \
  --name "Daily News Push" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --channel feishu \
  --to "user:ou_xxxxxxxxxxxxxxxx" \
  --accountId "default" \
  --message "Search AI news and compile into briefing" \
  --description "Push AI news every day at 9am"
```

**Example** (KK Heartbeat - Every 10 minutes):
```bash
openclaw cron add \
  --agentId "kk" \
  --session "kk" \
  --name "KK Heartbeat 10min" \
  --cron "*/10 * * * *" \
  --tz "Asia/Shanghai" \
  --channel feishu \
  --to "user:ou_642f1cb74d63462d1037375caac5ea2d" \
  --accountId "kk-feishu" \
  --message "Execute heartbeat check" \
  --description "Execute heartbeat check every 10 minutes"
```

---

## Cron Expression Reference

| Description | Expression |
|------|--------|
| Every minute | `* * * * *` |
| Every 5 minutes | `*/5 * * * *` |
| Every hour | `0 * * * *` |
| Every day at 9am | `0 9 * * *` |
| Every Monday at 9am | `0 9 * * 1` |
| 1st of every month | `0 0 1 * *` |

---

## Management Commands

```bash
# View task list
openclaw cron list

# Run task (test)
openclaw cron run {task_id}

# Remove task
openclaw cron remove {task_id}
```

---

## ✅ Security Checklist

Before execution:
- [ ] Replaced `{YOUR_USER_ID}` with actual ID
- [ ] Replaced `{CHANNEL}` with preferred channel
- [ ] Replaced `{AGENT_ID}` with executing agent
- [ ] Replaced `{ACCOUNT_ID}` with sending account
- [ ] Verified timezone settings
- [ ] Tested with non-destructive task

---

**Template Version**: 2.2.0  
**Note**: This template uses placeholders for security. Must replace before use.
