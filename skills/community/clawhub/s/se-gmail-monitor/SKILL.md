---
name: se-gmail-monitor
description: Monitor and manage Gmail accounts for Your Agency Name. Use when checking emails, sending emails, scanning for urgent messages, or performing email triage. Supports dual accounts (info@ and agent@) via IMAP/SMTP with app passwords. Use during heartbeats for periodic inbox checks.
version: 1.0.0
---

# Email Monitor

Gmail monitoring and management for Your Agency Name accounts.

## Accounts

| Account | Email | Type |
|---------|-------|------|
| Primary | YourName@yourdomain.com | Main business |
| Admin | info@yourdomain.com | Admin/general |
| Agent | agent@yourdomain.com | AI operator |

Config: `~/.openclaw/workspace/.gmail-config.json`

## Commands

```bash
# List recent emails (default: info@ account)
python3 scripts/gmail-monitor.py list

# List from specific account
python3 scripts/gmail-monitor.py list --account boris

# Read specific email
python3 scripts/gmail-monitor.py read <message_id>

# Send email (CONFIRM WITH the user FIRST)
python3 scripts/gmail-monitor.py send --to recipient@email.com --subject "Subject" --body "Body text" --account boris

# Search emails
python3 scripts/gmail-monitor.py search "query"
```

## Heartbeat Routine

During periodic checks, scan for:
1. Emails from known contacts (team, clients, partners)
2. Urgent keywords: "urgent", "ASAP", "deadline", "payment", "invoice"
3. Security alerts from Google, banks, or services
4. Client responses or new leads

## Rules

- **NEVER send emails as YourName** without explicit permission
- **Boris account** can send operational/internal emails freely
- **Flag urgent emails** to the user immediately
- **Do not auto-reply** to external contacts without approval
