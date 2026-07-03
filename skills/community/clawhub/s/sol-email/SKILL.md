---
name: sol-email
description: Read and send emails using the SolEmail automation system. Use when asked to check emails, send files via email, respond to an email, or set up email automation.
---

# Sol Email Skill

Automated email reading and sending via himalaya (local Maildir) and SMTP.

## Scripts Location

All scripts live in `~/.openclaw/workspace/scripts/`:
- `agentmail-send.py` — send emails
- `agentmail-inbox.py` — read emails
- `find-zip-email.py` — find files, zip, email

## Prerequisites

1. **himalaya installed** — `brew install himalaya`
2. **Email account configured** in `~/.config/himalaya/config.toml`
3. **Environment variables** set (see `.env.example` in SolEmail repo):
   - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `FROM_NAME`

## Daily Use

### Check recent emails

```bash
python3 ~/.openclaw/workspace/scripts/agentmail-inbox.py --limit 10
```

### Check unread emails only

```bash
python3 ~/.openclaw/workspace/scripts/agentmail-inbox.py --unread-only
```

### Read a specific email (by ID)

```bash
python3 ~/.openclaw/workspace/scripts/agentmail-inbox.py --read 42
```

### Send an email

```bash
python3 ~/.openclaw/workspace/scripts/agentmail-send.py \
    --to "recipient@example.com" \
    --subject "Subject here" \
    --body "Email body text"
```

### Send with attachments

```bash
python3 ~/.openclaw/workspace/scripts/agentmail-send.py \
    --to "recipient@example.com" \
    --subject "Your files" \
    --body "Please find the files attached." \
    --attachment "/path/to/file1.pdf" \
    --attachment "/path/to/file2.zip"
```

### Find files, zip, and email

```bash
python3 ~/.openclaw/workspace/scripts/find-zip-email.py \
    --find "*.pdf" \
    --search-dir ~/Downloads \
    --to "recipient@example.com" \
    --subject "Your PDFs" \
    --body "As requested."
```

### Sync emails before checking

```bash
himalaya sync && python3 ~/.openclaw/workspace/scripts/agentmail-inbox.py --limit 10
```

## Configuration

### himalaya account (IMAP + SMTP)

`~/.config/himalaya/config.toml`:
```toml
[[accounts]]
name = "icloud"

[accounts.icloud.imap]
host     = "imap.mail.me.com"  # or imap.gmail.com for Gmail
port     = 993
username = "yourname@icloud.com"
password = "xxxx-xxxx-xxxx-xxxx"  # App-specific password, NOT your real password
ssl      = true

[accounts.icloud.smtp]
host     = "smtp.mail.me.com"
port     = 587
username = "yourname@icloud.com"
password = "xxxx-xxxx-xxxx-xxxx"
starttls = true
```

### Environment variables

Set in `~/.openclaw/workspace/.env`:
```
SMTP_HOST=smtp.mail.me.com
SMTP_PORT=587
SMTP_USER=yourname@icloud.com
SMTP_PASSWORD=xxxx-xxxx-xxxx-xxxx
FROM_NAME=Your Name
```

## Troubleshooting

### "Authentication failed" when sending
App password is wrong or expired. Generate a new one at appleid.apple.com.

### "No emails found"
Run `himalaya sync` first to download emails from the server.

### SMTP timeout
Try port 465 (SSL) instead of 587 (STARTTLS).

### himalaya not found
Install: `brew install himalaya`

## Cron / Schedule

Set up automated email checks via OpenClaw cron:
```
name: Email check
schedule: "*/15 * * * *"
command: "himalaya sync && python3 ~/.openclaw/workspace/scripts/agentmail-inbox.py --unread-only"
```

Or add to `HEARTBEAT.md` in the workspace for heartbeat-based checking.

## Related

- **Full guide:** https://thesolai.github.io/guides/email-automation/
- **Repository:** https://github.com/TheSolAI/SolEmail
- **Technical report:** https://github.com/TheSolAI/SolEmail/blob/main/report.md
