---
name: skulk-email
description: |
  Email via DreamHost — read inbox, send email, search messages. Send works from any VPS (including DigitalOcean) by routing through DreamHost's Roundcube webmail over HTTPS, bypassing SMTP port blocks. Optionally read a shared Gmail inbox via IMAP. Use when: sending email, checking inbox, reading messages, or setting up email for an agent. Dependencies: python3, curl, jq (must be installed on the host). Credentials: DreamHost mailbox email+password stored at ~/.config/skulk-email/credentials.json (user must create this file manually before use; see Setup). No third-party services or API keys needed.
---

# Skulk Email

Read and send email via DreamHost. Optionally read a shared Gmail inbox.

**Key feature:** Sending works from VPS providers that block SMTP (DigitalOcean, etc.) by routing through DreamHost's Roundcube webmail over HTTPS. No third parties. No relay services.

## Requirements

- **python3** — IMAP operations
- **curl** — Roundcube webmail sending
- **jq** — credential file parsing
- **DreamHost mailbox** — email address + password
- **Credential file** — stored locally at `~/.config/skulk-email/credentials.json` (never transmitted beyond DreamHost servers)

## Security

- Credentials are read from a local JSON file with strict permissions (700 dir, 600 file)
- Passwords are only sent over TLS: IMAP SSL (port 993) and HTTPS (port 443)
- No credentials are logged, cached, or sent to any third party
- Cookie files used for Roundcube sessions are per-process and cleaned up on exit

## Setup

### 1. DreamHost mailbox

You need a DreamHost-hosted email address and its password.

### 2. Store credentials

```bash
mkdir -p ~/.config/skulk-email && chmod 700 ~/.config/skulk-email
```

Create `~/.config/skulk-email/credentials.json`:

```json
{
  "skulk_email": "you@yourdomain.com",
  "skulk_password": "your-dreamhost-mailbox-password",
  "gmail_email": "",
  "gmail_app_password": ""
}
```

Gmail fields are optional — leave empty if you don't need shared Gmail access.

```bash
chmod 600 ~/.config/skulk-email/credentials.json
```

### 3. Test

```bash
bash scripts/skulk-email.sh test
```

## Commands

```bash
# Test connection
bash scripts/skulk-email.sh test

# Read inbox
bash scripts/skulk-email.sh inbox [limit]

# Check unread count
bash scripts/skulk-email.sh count

# List unread messages
bash scripts/skulk-email.sh unread [limit]

# Read a specific message by ID
bash scripts/skulk-email.sh read <message-id>

# Send email
bash scripts/skulk-email.sh send <to> <subject> <body>

# Search messages
bash scripts/skulk-email.sh search <query> [limit]

# Read shared Gmail inbox (if configured)
bash scripts/skulk-email.sh gmail-inbox [limit]
bash scripts/skulk-email.sh gmail-unread [limit]
bash scripts/skulk-email.sh gmail-count
bash scripts/skulk-email.sh gmail-read <message-id>
```

## How it works

- **Reading:** Direct IMAP to `imap.dreamhost.com:993` (SSL) and optionally `imap.gmail.com:993`
- **Sending:** Authenticates to DreamHost Roundcube webmail via HTTPS, composes and sends through the web interface
- **Dependencies:** `python3`, `curl`, `jq` (standard on most systems)
- **No SMTP ports required.** Works behind any firewall that allows HTTPS.

## Why not just use SMTP?

Many VPS providers (DigitalOcean, some AWS configs) permanently block outbound SMTP ports 25, 465, and 587 to prevent spam. DreamHost's Roundcube webmail operates over HTTPS (port 443), which is never blocked. This skill automates the webmail login and send flow — same as composing email in a browser, just scripted.

## Notes

- First email from a new address may land in spam. Ask recipients to mark "not spam."
- Be reasonable with send volume — this is webmail automation, not a bulk sender.
- Credentials stay local in `~/.config/skulk-email/` — never commit them.
- Script paths are relative to this skill directory.

## Credits

Built by the Skulk 🦊 — [The Human Pattern Lab](https://thehumanpatternlab.com)
