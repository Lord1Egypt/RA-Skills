# Unified Mailbox AI

A unified unread-email monitor for **Outlook** and **Gmail**, built as an [OpenClaw](https://openclaw.ai) skill. Detects new mail across both providers, summarizes them with AI, checks calendar conflicts for meeting invitations, and pushes notifications to Telegram.

Either Outlook or Gmail (or both) can be enabled — configure only what you need.

> **clawhub slug**: `unified-mailbox-ai` &nbsp;·&nbsp; **GitHub**: [L1TangDingZhen/email-monitor](https://github.com/L1TangDingZhen/email-monitor)

---

## Features

- **Dual mailbox support** — monitor Outlook (via Microsoft Graph) and Gmail (via the `gog` CLI) from one place
- **Token-efficient** — pure-Python check first; AI is only invoked when new mail is found
- **Calendar conflict detection** — for meeting invitations, automatically checks both Outlook and Google Calendar for conflicts
- **Telegram delivery** — clean, formatted summaries pushed to your chat
- **Cron-friendly** — designed to run every few minutes from a system crontab
- **Deduplication** — tracks notified email IDs so you never get the same notification twice

---

## Requirements

### Required
- Linux or macOS
- Python 3.8+
- [OpenClaw](https://openclaw.ai) installed and a working Telegram bot pairing

### Required for Outlook support
- The [`outlook-graph`](https://clawhub.ai/byungkyu/outlook-graph) skill installed and authorized
- An MSAL token cache file at `~/.openclaw/ms_tokens.json` (the outlook-graph skill creates this)
- Python package: `msal` (`pip install msal`)

### Required for Gmail support
- [`gog` CLI](https://gogcli.sh) installed and authorized for at least Gmail and Calendar scopes
- Google Cloud project with **Gmail API** and **Google Calendar API** enabled
- gog keyring backend set to `file` (run `gog auth keyring file`) so it works in non-interactive contexts

---

## Installation

### Option A: Install from clawhub (recommended)

```bash
clawhub install unified-mailbox-ai
```

This drops the skill into `~/.openclaw/workspace/skills/unified-mailbox-ai/`. After installing, follow steps 2–4 below to configure env vars and (optionally) cron.

### Option B: Install from GitHub

```bash
git clone https://github.com/L1TangDingZhen/email-monitor.git
cd email-monitor
./install.sh
```

The installer copies files into the right place, prompts for your environment variables, writes them to `~/.openclaw/openclaw.json`, and offers to set up a 5-minute cron job.

### 2. Register the skill with your OpenClaw agent

Edit `~/.openclaw/openclaw.json` and add `"unified-mailbox-ai"` to your agent's `skills` list:

```json
"agents": {
  "list": [
    {
      "id": "main",
      "skills": [
        "unified-mailbox-ai",
        ...
      ]
    }
  ]
}
```

### 3. Configure environment variables

The skill reads three environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `EMAIL_MONITOR_TELEGRAM_USER` | **yes** | The Telegram chat ID that should receive notifications |
| `EMAIL_MONITOR_GMAIL_ACCOUNT` | optional | Your Gmail address (e.g. `you@gmail.com`). If unset, Gmail is skipped. |
| `MS_GRAPH_ACCESS_TOKEN` | optional | Microsoft Graph access token (managed by the `outlook-graph` skill). If `~/.openclaw/ms_tokens.json` is missing, Outlook is skipped. |

You need to configure at least one mailbox (Outlook **or** Gmail). If neither is configured, the script will refuse to run.

#### Where to set the env vars

Set them in **all three places** that may invoke the script:

**A. `~/.openclaw/openclaw.json`** (used when the OpenClaw agent runs the script):
```json
"env": {
  "EMAIL_MONITOR_TELEGRAM_USER": "123456789",
  "EMAIL_MONITOR_GMAIL_ACCOUNT": "you@gmail.com"
}
```

**B. `~/.bashrc`** (used when you run the script manually in a terminal):
```bash
export EMAIL_MONITOR_TELEGRAM_USER="123456789"
export EMAIL_MONITOR_GMAIL_ACCOUNT="you@gmail.com"
export GOG_KEYRING_PASSWORD=""
```

**C. crontab line** (used by the auto-monitor; see step 4):
```
*/5 * * * * EMAIL_MONITOR_TELEGRAM_USER="123456789" EMAIL_MONITOR_GMAIL_ACCOUNT="you@gmail.com" ...
```

### 4. Set up automatic monitoring (optional)

To check for new mail every 5 minutes and push to Telegram automatically:

```bash
crontab -e
```

Add:

```
*/5 * * * * PATH=$HOME/.npm-global/bin:/usr/local/bin:/usr/bin:/bin GOG_KEYRING_PASSWORD="" EMAIL_MONITOR_GMAIL_ACCOUNT="you@gmail.com" EMAIL_MONITOR_TELEGRAM_USER="123456789" /usr/bin/python3 $HOME/.openclaw/workspace/skills/unified-mailbox-ai/scripts/unified_mailbox_ai.py auto-notify
```

Notes:
- `GOG_KEYRING_PASSWORD=""` is only needed if you use Gmail (gog uses an encrypted file keyring with empty password by default in this setup)
- `PATH` is set explicitly because cron's default PATH does not include `~/.npm-global/bin`, where `openclaw` is installed via npm

---

## Usage

### Check for new emails (manual)

```bash
python3 ~/.openclaw/workspace/skills/unified-mailbox-ai/scripts/unified_mailbox_ai.py check
```

Outputs JSON with the unread emails from each enabled mailbox.

### Run the full auto-notify flow

```bash
python3 ~/.openclaw/workspace/skills/unified-mailbox-ai/scripts/unified_mailbox_ai.py auto-notify
```

This is the action the cron job runs:
1. Fetches unread mail from configured mailboxes
2. Filters out already-notified IDs
3. If any new mail is found, hands it to the OpenClaw agent for AI summarization and Telegram delivery
4. Marks the new mail as notified

### Mark a specific email as notified

```bash
python3 ~/.openclaw/workspace/skills/unified-mailbox-ai/scripts/unified_mailbox_ai.py mark --id "<EMAIL_ID>"
```

For Gmail thread IDs, prefix with `gmail:` (e.g. `gmail:19cef361ab2acc22`).

### Clear all notification records

```bash
python3 ~/.openclaw/workspace/skills/unified-mailbox-ai/scripts/unified_mailbox_ai.py clear
```

Use this if you want to re-trigger notifications for previously seen emails.

---

## How it works

```
                  ┌─ Outlook (MS Graph) ─┐
cron (every 5min)─┤                       ├─→ filter notified ─→ any new? ─→ AI summarize ─→ Telegram
                  └─ Gmail (gog CLI) ────┘                          │ no
                                                                    └─→ exit (no AI cost)
```

Key design decisions:

- **Two-layer architecture**: pure-Python detection runs first (free); AI is only invoked when there's actually something to report. This keeps token costs near zero on quiet days.
- **Mailbox independence**: Outlook and Gmail are completely independent. Disable either one by leaving its config unset.
- **Idempotent marking**: notified email IDs are persisted to `~/.openclaw/notified_emails.json`. Capped at 1000 entries.
- **Cron-safe**: handles non-interactive environments where GNOME keyring is locked, npm-global PATH is missing, etc.

---

## Troubleshooting

### "Neither Outlook nor Gmail is configured"
You must enable at least one. For Outlook, install the `outlook-graph` skill and complete its OAuth setup. For Gmail, set `EMAIL_MONITOR_GMAIL_ACCOUNT` and run `gog auth add <your-email> --services gmail,calendar`.

### "Missing EMAIL_MONITOR_TELEGRAM_USER"
This is required regardless of which mailbox you use. It tells the script which Telegram chat to push notifications to. Find your chat ID by messaging [@userinfobot](https://t.me/userinfobot) on Telegram.

### Gmail returns "credentials store locked" or "No auth"
Your `gog` keyring is using GNOME keyring (default on Linux), which is locked when running outside a desktop session. Switch to file backend:
```bash
gog auth keyring file
gog auth add <your-email> --services gmail,calendar
```
And ensure `GOG_KEYRING_PASSWORD=""` is set wherever you run the script.

### Gmail Calendar returns 403
You need to enable the **Google Calendar API** in your Google Cloud project (it's separate from the Gmail API). Visit https://console.developers.google.com/apis/api/calendar-json.googleapis.com and click Enable.

### Cron runs but never pushes
Cron's PATH usually doesn't include `~/.npm-global/bin`, so `openclaw` can't be found. Either set `PATH=...` in the crontab line or symlink `openclaw` into `/usr/local/bin`.

---

## License

MIT

---

## Acknowledgements

Built on top of:
- [OpenClaw](https://openclaw.ai) — the agent framework
- [`outlook-graph`](https://clawhub.ai/byungkyu/outlook-graph) — Microsoft Graph integration
- [`gog`](https://gogcli.sh) — Google Workspace CLI
