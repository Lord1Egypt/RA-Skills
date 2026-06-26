---
name: gmail-checker
description: >
  Check Gmail for unread inbox emails, filtered by priority. Use when asked to check emails,
  check inbox, email digest, email summary, or "any new mail". Outputs a brief list sorted
  by priority (HIGH/MEDIUM/LOW). Skips marketing, promotions, social, and update categories.
  Configurable via gmail-config.json.
---

# Gmail Checker 📧

Fetch unread Gmail messages, filter out noise, deliver a prioritized digest.

## Why

Your inbox is full of automated emails, promotions, and updates. This skill surfaces what actually matters — security alerts, personal messages, and anything you've flagged as important.

## When to Use

- "Check my emails"
- "Any new mail?"
- "Give me an email digest"
- "What's in my inbox?"
- "Email summary"

## Setup

First-time users need Google OAuth credentials. If the script exits with a "missing file" error, read [references/setup.md](references/setup.md) and walk the user through the setup flow.

```bash
pip install google-api-python-client google-auth-oauthlib
```

## How to Run

```bash
python3 scripts/check_gmail.py [hours]          # default: last 24h
python3 scripts/check_gmail.py --json [hours]   # structured JSON output
```

**Config:** Copy `config.example.json` to `<DATA_DIR>/gmail-config.json` and customize. The script prints the resolved `<DATA_DIR>` path if credentials are missing.

## Data Directory

Credentials and config resolve to:

```
1. $SKILL_DATA_DIR (set by agent platform)
2. ~/.config/gmail-checker/  (default fallback)
```

Any platform can set `$SKILL_DATA_DIR` to their preferred credential store. If unset, `~/.config/gmail-checker/` is used automatically. Works with OpenClaw, Claude Code, Codex, and any agent that can run Python scripts.

## Priority Rules

```
🔴 HIGH   → Sender domain or subject matches your config
🟡 MEDIUM → Gmail-labeled personal messages
🟢 LOW    → Everything else (still inbox, still unread)
```

```
Filtered out entirely:
• CATEGORY_PROMOTIONS
• CATEGORY_UPDATES
• CATEGORY_FORUMS
• CATEGORY_SOCIAL
```

Customize priorities in `gmail-config.json`:

```
high_priority_domains:   ["stripe.com", "github.com"]
high_priority_keywords:  ["security", "urgent", "billing"]
```

## Output Example

```
Unread Inbox (last 24h)

🔴 HIGH
  Security alert: new sign-in from unknown device
  from: Google <no-reply@google.com>

🟡 MED
  Re: dinner friday?
  from: Sarah <sarah@gmail.com>

🟢 LOW
  Your weekly GitHub digest
  from: GitHub <noreply@github.com>

3 unread emails
```

Adapt formatting for the current channel (bold, bullets, etc.).

## Suggested Integration

```
cron: 0 8 * * * → python3 scripts/check_gmail.py
```
