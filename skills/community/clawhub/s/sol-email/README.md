# SolSkills / SolEmail

**Automated email workflow powered by himalaya + SMTP + cron jobs.**

This is the system behind the Sol AI email automation setup. It gives an AI assistant the ability to read, filter, and respond to emails — fully automated, on a schedule, without any human manually checking email.

Built and documented by [Sol AI](https://thesolai.github.io) — see the [full guide on the website](https://thesolai.github.io/guides/email-automation/) for the complete walkthrough.

---

## What this does

```
Email arrives → himalaya downloads it locally → cron job triggers check →
AI reads it → AI decides what to do → AI sends reply / zips files / does nothing →
human is notified only if needed
```

Specifically, this system can:
- **Read emails** from a local Maildir store (synced by himalaya)
- **Send emails** via SMTP with attachments (zip files, documents, anything)
- **Filter emails** by sender, subject, date, or content
- **Trigger actions** based on email content (zip files and email them back, etc.)
- **Run on a schedule** via cron jobs, without any server to maintain

---

## Architecture Overview

```
                    ┌──────────────────┐
                    │   Email Provider │
                    │ (iCloud / Gmail)│
                    └────────┬────────┘
                             │ IMAP (port 993)
                             ▼
               ┌─────────────────────────────┐
               │  himalaya CLI              │
               │  (syncs email locally)      │
               └──────────────┬─────────────┘
                              │ local Maildir
                              ▼
               ┌─────────────────────────────┐
               │  ~/workspace/scripts/       │
               │  agentmail-inbox.py         │
               │  agentmail-send.py          │
               │  find-zip-email.py          │
               └──────────────┬─────────────┘
                              │ cron jobs / heartbeat
                              ▼
               ┌─────────────────────────────┐
               │  OpenClaw AI assistant     │
               │  (your AI agent)           │
               └─────────────────────────────┘
```

---

## Prerequisites

- **Mac or Linux** (terminal required)
- **Python 3.8+**
- **himalaya** CLI (`brew install himalaya`)
- An email account with IMAP access (iCloud, Gmail, Outlook, any provider)
- App-specific passwords from your email provider

---

## Quick Start

### 1. Install himalaya

```bash
# macOS
brew install himalaya

# Linux (Arch)
sudo pacman -S himalaya

# Or build from source: https://github.com/soywod/himalaya#installation
```

### 2. Configure your email account

Copy the config template:
```bash
mkdir -p ~/.config/himalaya
cp SolEmail/config/himalaya/config.toml ~/.config/himalaya/config.toml
nano ~/.config/himalaya/config.toml
# Fill in: host, port, username, app-specific password
```

Test it:
```bash
himalaya envelope
# You should see your recent emails
```

### 3. Copy the scripts

```bash
mkdir -p ~/.openclaw/workspace/scripts
cp SolEmail/scripts/*.py ~/.openclaw/workspace/scripts/
chmod +x ~/.openclaw/workspace/scripts/*.py
```

### 4. Set environment variables

```bash
# Copy the example env file
cp SolEmail/.env.example ~/.openclaw/workspace/.env

# Edit it with your actual credentials
nano ~/.openclaw/workspace/.env
```

### 5. Test sending

```bash
export SMTP_HOST=smtp.mail.me.com
export SMTP_PORT=587
export SMTP_USER=yourname@icloud.com
export SMTP_PASSWORD=your-app-specific-password
export FROM_NAME="Your Name"

python3 ~/.openclaw/workspace/scripts/agentmail-send.py \
    --to "test@example.com" \
    --subject "Test from SolEmail" \
    --body "Hello, this is a test."
```

---

## The Scripts

### agentmail-send.py

Send emails with optional file attachments.

```bash
python3 agentmail-send.py \
    --to "recipient@example.com" \
    --subject "Your files" \
    --body "Please find the files attached." \
    --attachment "/path/to/file1.pdf" \
    --attachment "/path/to/file2.zip"
```

Or import as a Python module:
```python
from agentmail_send import send_email

send_email(
    to="recipient@example.com",
    subject="Hello",
    body="Message here",
    attachments=["/path/to/file.zip"]
)
```

### agentmail-inbox.py

List or read emails from the local himalaya store.

```bash
# List 10 most recent emails
python3 agentmail-inbox.py --limit 10

# Show only unread
python3 agentmail-inbox.py --unread-only

# Read a specific email by ID
python3 agentmail-inbox.py --read 42

# Output as JSON (good for scripting)
python3 agentmail-inbox.py --limit 5 --json
```

### find-zip-email.py

Find files by glob pattern, zip them, and email to a recipient. Useful for "send me all PDFs from Downloads" workflows.

```bash
python3 find-zip-email.py \
    --find "*.pdf" \
    --search-dir ~/Downloads \
    --to "recipient@example.com" \
    --subject "Your PDFs" \
    --body "As requested, all PDFs from Downloads."
```

---

## Email Provider Setup

### iCloud (recommended for most users)

1. Go to [appleid.apple.com](https://appleid.apple.com)
2. Sign in → **Sign In and Security**
3. **App-Specific Passwords** → Generate
4. Name it something like "himalaya" and copy the password
5. Enable IMAP on your iCloud account:
   - Go to **mail.mu.icloud.com** → Settings → **Email** → **Sync email**

Your `config.toml` IMAP/SMTP values:
```toml
host     = "imap.mail.me.com"   # IMAP
host     = "smtp.mail.me.com"   # SMTP
port     = 993                  # IMAP
port     = 587                  # SMTP (STARTTLS)
```

### Gmail

1. Go to [myaccount.google.com](https://myaccount.google.com) → **Security**
2. Enable **2-Step Verification** if not already on
3. **App passwords** → Generate → Mail → Other (custom name: "himalaya")
4. Copy the 16-character app password

Your `config.toml` values:
```toml
host     = "imap.gmail.com"
port     = 993
username = "yourname@gmail.com"
password = "xxxx xxxx xxxx xxxx"
```

### Outlook / Microsoft 365

1. Go to **account.microsoft.com** → **Security**
2. **App passwords** → Generate
3. Use these values:
```toml
host     = "outlook.office365.com"
port     = 993
username = "yourname@outlook.com"
password = "your-app-password"
```

---

## Cron Jobs

Run automated email checks on a schedule. Add to your crontab (`crontab -e`):

```cron
# Check email every 15 minutes, log to file
*/15 * * * * python3 /Users/yourname/.openclaw/workspace/scripts/agentmail-inbox.py >> /Users/yourname/.openclaw/logs/email-check.log 2>&1

# Every morning at 9 AM
0 9 * * * python3 /Users/yourname/.openclaw/workspace/scripts/agentmail-inbox.py --unread-only >> ~/logs/morning-email.log 2>&1

# Every hour during work hours
0 9-18 * * 1-5 python3 /Users/yourname/.openclaw/workspace/scripts/agentmail-inbox.py --limit 5 --json >> ~/logs/hourly-email.json 2>&1
```

Or use OpenClaw's built-in cron scheduler:
```
# In OpenClaw:
/cron add --name "Email check" --schedule "*/15 * * * *" --command "python3 ~/.openclaw/workspace/scripts/agentmail-inbox.py"
```

---

## Security Notes

### App-specific passwords
**Never use your real email password.** Always generate an app-specific password from your email provider. This limits what the script can do if credentials are ever exposed.

### Local storage
himalaya downloads emails to `~/.mail/`. This directory contains your entire email history in plain text. Treat it like you would treat your email account itself.

### Environment variables
Never hardcode credentials in scripts. Use environment variables (as shown in `.env.example`) or a `.env` file that is listed in your `.gitignore`.

### What to do if credentials are exposed:
1. Revoke the app-specific password immediately at your provider
2. Generate a new one
3. Update your config and `.env`
4. Check your sent mail for anything you didn't send

---

## Common Problems

### "Authentication failed" when sending
- App password is wrong or expired (iCloud passwords can expire after password changes)
- App-specific password, not your regular password — they are different

### "No emails found" with himalaya envelope
- Run `himalaya sync` to download emails from the server
- Check that `IMAP.password` in config matches the app-specific password
- Try `himalaya account list` to verify the account is configured

### Emails not showing as unread
- himalaya tracks read/unread status locally in the Maildir
- Use `himalaya envelope --unread` to see only unread

### SMTP timeout
- Try port 465 (SSL) instead of 587 (STARTTLS)
- Some corporate firewalls block port 587
- Check your email provider supports SMTP from third-party apps (iCloud: yes, with app password)

---

## Extending the System

### Adding to OpenClaw as a skill

Create `~/.openclaw/workspace/skills/sol-email/SKILL.md`:
```markdown
---
name: sol-email
description: Send and read emails using the SolEmail system.
---

# Sol Email Skill

## Check unread emails
python3 ~/.openclaw/workspace/scripts/agentmail-inbox.py --unread-only

## Read a specific email
python3 ~/.openclaw/workspace/scripts/agentmail-inbox.py --read <id>

## Send an email
python3 ~/.openclaw/workspace/scripts/agentmail-send.py \
    --to "recipient@example.com" \
    --subject "Subject" \
    --body "Body text"
```

### Using with AgentMail (receive emails)

If you want to receive emails via a webhook (so people can email your AI directly):

1. Sign up at [agentmail.to](https://agentmail.to)
2. Get your API key
3. Set `AGENTMAIL_API_KEY` in your `.env`
4. Configure the webhook URL in the agentmail.to dashboard

Your AI can then both read emails from your personal account (via himalaya) AND receive emails sent to its own address (via AgentMail).

---

## Repository Structure

```
SolEmail/
├── README.md                    # This file
├── report.md                    # In-depth technical report
├── SKILL.md                     # OpenClaw skill definition
├── .env.example                 # Environment variables template
├── scripts/
│   ├── agentmail-send.py        # Send email via SMTP
│   ├── agentmail-inbox.py       # Read emails from himalaya store
│   └── find-zip-email.py         # Find files, zip, email workflow
├── config/
│   └── himalaya/
│       └── config.toml          # himalaya config template
└── examples/
    └── workflow-examples.md     # More workflow ideas
```

---

## Related

- [Sol AI Email Automation Guide](https://thesolai.github.io/guides/email-automation/) — the full guide this repo supports
- [himalaya CLI](https://github.com/soywod/himalaya) — the email client that powers this
- [OpenClaw](https://openclaw.ai) — the AI agent framework this is built on
- [AgentMail](https://agentmail.to) — webhook-based email receiving
