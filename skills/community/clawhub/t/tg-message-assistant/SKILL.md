---
name: tg-message-assistant
description: >
  Generate topic briefings from Telegram channels. Use this skill when the user mentions
  "briefing", "newsletter", "digest", "message summary", "channel recap", "generate report",
  "send briefing", "scheduled push", or "channel roundup". Also applies when users want
  to compile messages from multiple Telegram channels into structured summaries and
  deliver them to others.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: "\U0001F4F0"
    homepage: https://github.com/TelyAgent/telyclaw-skills
---

# TG Message Assistant (Telyclaw)

Read `./core/prompt.md` for the full 5-step workflow and interaction principles.

## Tool Strategy: Native API Tools

Telyclaw has built-in Telegram and Gmail tools. Use them directly.

### Telegram

| Action | Tool | Notes |
|--------|------|-------|
| Fetch messages | `telegram_get_messages` | Supports channel usernames and chat IDs |
| Send messages | `telegram_send_message` | 4096-char limit per message; split with "(1/N)" labels |

### Gmail

| Action | Tool | Notes |
|--------|------|-------|
| Authorize | `gmail_authorize` | Opens browser for Google OAuth |
| Send email | `gmail_message_send` | Requires `confirm: true` |

### Cron

Use the **CronCreate** tool for scheduled recurring generation.

---

## Gmail Setup

**Plugin detection (required on first use):**

1. Scan the available tools list for `gmail_*` prefixed tools.
2. If not found, tell the user:
   > "The Gmail plugin is not installed. Please install the **Gmail** plugin from the
   > telyclaw plugin marketplace, or visit https://github.com/TelyAgent/telyclaw-plugin-gmail
   > for installation instructions. Let me know once it's set up and we'll continue."
3. If tools exist but are unavailable (e.g. expired authorization), proceed to authorization.

**Authorization flow:**
- On receiving an authorization error, use AskUserQuestion to ask the user for permission.
- Call `gmail_authorize` — this will open a browser window for Google OAuth.
- Tell the user: "A Google authorization page has been opened in your browser. Please
  complete the authorization and let me know when you're done."
- Once the user confirms, retry the send.

**Send parameters:**
- `to`: recipient email address
- `subject`: `{Channel names} Briefing · {date range}`
- `text`: the full Markdown briefing
- `confirm`: true (required — the tool will refuse to send without this)
