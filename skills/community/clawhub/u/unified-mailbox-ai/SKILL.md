---
name: unified-mailbox-ai
description: Unified mailbox AI for both Outlook and Gmail. Checks unread emails, summarizes new mail with AI, detects meeting invitations, checks calendar conflicts on both Outlook and Google Calendar, and sends Telegram notifications. Use when asked to check/monitor email from either or both accounts.
homepage: https://github.com/L1TangDingZhen/email-monitor
license: MIT
allowed-tools: Bash Read Write
metadata: {"openclaw":{"emoji":"📧","requires":{"bins":["python3"],"env":["EMAIL_MONITOR_TELEGRAM_USER"],"optionalBins":["gog"],"optionalEnv":["MS_GRAPH_ACCESS_TOKEN","EMAIL_MONITOR_GMAIL_ACCOUNT"]}}}
---
# Unified Mailbox AI

Unified inbox monitor for **Outlook** and **Gmail** with AI summarization and calendar conflict detection. Either or both providers can be enabled — configure only what you need.

## Accounts
- **Outlook**: requires `MS_GRAPH_ACCESS_TOKEN` (managed by the `outlook-graph` skill). If `~/.openclaw/ms_tokens.json` is missing, Outlook is skipped.
- **Gmail**: requires `EMAIL_MONITOR_GMAIL_ACCOUNT` env var and the `gog` CLI authorized. If unset, Gmail is skipped.
- **Telegram**: `EMAIL_MONITOR_TELEGRAM_USER` is always required (the chat ID that receives notifications).

## When to Use
- User asks to check emails (either account or both)
- Triggered by cron job for automatic monitoring
- User asks about meeting invitations or calendar conflicts

## Credentials
Accounts are pre-configured via environment variables. **Do not ask the user for credentials. Just run the scripts directly.**

---

## Workflow (manual check)

1. Run the check command (returns JSON with new unread from configured accounts)
2. For each new email, summarize sender/subject/content
3. If it's a meeting invitation, check the configured calendar(s) for conflicts:
   - Outlook calendar: use `outlook-graph` skill `calendar-list`
   - Google Calendar: use `gog calendar events primary --from <iso> --to <iso> --json`
4. Report findings: conflict status on the same line as the summary

## Check new emails
```bash
python3 {baseDir}/scripts/unified_mailbox_ai.py check
```

## Mark email as processed (prevents duplicate notifications)
```bash
python3 {baseDir}/scripts/unified_mailbox_ai.py mark --id "EMAIL_ID"
```
> For Gmail threads, prefix the ID with `gmail:` e.g. `gmail:19ceb0fc779a8a42`

## Clear all notified records
```bash
python3 {baseDir}/scripts/unified_mailbox_ai.py clear
```

## Auto-notify (used by cron — checks configured accounts, calls AI only if new emails found)
```bash
python3 {baseDir}/scripts/unified_mailbox_ai.py auto-notify
```

---

## Calendar conflict check

### Outlook calendar
```bash
python3 ~/.openclaw/workspace/skills/outlook-graph/scripts/outlook_graph.py calendar-list --days 7 --top 20
```

### Google Calendar
```bash
GOG_KEYRING_PASSWORD="" GOG_ACCOUNT="$EMAIL_MONITOR_GMAIL_ACCOUNT" gog calendar events primary --from <ISO_START> --to <ISO_END> --json --no-input
```

---

## Output format for each email

```
- [Outlook/Gmail] From: <name> <email> | Subject: <subject> | <brief summary>
  [If meeting invite] Event: <date/time> | Calendar: ⚠️ Conflict with "<event>" OR ✅ No conflict
```
