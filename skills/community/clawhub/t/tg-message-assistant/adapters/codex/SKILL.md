---
name: tg-message-assistant
description: >
  Generate topic briefings from Telegram channels. Use this skill when the user mentions
  "briefing", "newsletter", "digest", "message summary", "channel recap", "generate report",
  "send briefing", "scheduled push", or "channel roundup". Also applies when users want
  to compile messages from multiple Telegram channels into structured summaries and
  deliver them to others.
---

# TG Message Assistant (Codex CLI)

Read `../../core/prompt.md` for the full 5-step workflow and interaction principles.

---

## Choose Your Tool Strategy

Before starting, ask the user which approach they prefer.
Explain the options clearly, then proceed with their choice.

### Option 1 (Recommended): Browser Automation

Use Playwright or any available browser automation tool to interact with Telegram Web
and Gmail Web directly. The agent controls the browser like a human would.

| Pros | Cons |
|------|------|
| Zero setup — no API keys or MCP config | Slower than API calls |
| Works immediately if logged into Telegram/Gmail in browser | Requires browser session to remain active |
| No third-party service dependencies | Scrolling long channel histories takes time |

### Option 2: MCP Servers (Faster, Needs Setup)

Configure dedicated MCP servers for direct API access to Telegram and Gmail.

| Pros | Cons |
|------|------|
| Fast, reliable API access | Requires `TELEGRAM_API_ID` + `TELEGRAM_API_HASH` |
| 102+ Telegram tools via `mcp-telegram` | Requires OAuth setup for Gmail |
| Better for large channels and recurring tasks | MCP config in `~/.codex/config.toml` |

---

## Option 1: Browser Automation

### Telegram via Web (`web.telegram.org`)

**Fetching messages (Step 2):**

1. Navigate to `https://web.telegram.org/`.
2. If the user is not logged in, pause and ask them to log in, then continue.
3. For each target channel, search in the left sidebar or navigate to `https://web.telegram.org/a/#<channel-username>`.
4. Scroll through the message history to cover the requested time range.
5. Extract from each visible message: timestamp, sender, text content, view count, forward count.

**Sending briefings (Step 4):**

1. Navigate to `https://web.telegram.org/`. Confirm the user is logged in.
2. Open the target chat/group/channel via search.
3. Split the briefing into ≤4096-character segments. Label each "(1/N)", "(2/N)", etc.
4. Paste and send each segment in order.
5. Report back when sending is complete.

### Gmail via Web (`mail.google.com`)

1. Navigate to `https://mail.google.com/`. Confirm the user is logged in.
2. Click "Compose".
3. Fill in:
   - To: recipient email address
   - Subject: `{Channel names} Briefing · {date range}`
   - Body: the full Markdown briefing (renders as plain text in email)
4. Click Send.

---

## Option 2: MCP Servers

### Telegram MCP (`mcp-telegram`)

Add to `~/.codex/config.toml`:

```toml
[mcp_servers.telegram]
command = "npx"
args = ["-y", "mcp-telegram"]
env = { TELEGRAM_API_ID = "your_api_id", TELEGRAM_API_HASH = "your_api_hash" }
enabled = true
```

`mcp-telegram` (`beautyfree/mcp-telegram`) provides 102+ tools: read/search/send messages,
manage channels, transcribe voice, and more via MTProto (real Telegram user account).

Get API credentials at https://my.telegram.org/apps.

### Gmail MCP

Choose one:

**A) Codex Official Gmail Plugin (simplest):**
```bash
/plugins install gmail
```
Built-in OAuth, works across Codex App, CLI, and VS Code.

**B) @kembec/email-mcp (most features):**
```toml
[mcp_servers.email]
command = "npx"
args = ["-y", "@kembec/email-mcp"]
enabled = true
```
Supports Gmail (OAuth2), Outlook, and iCloud.

### Cron / Scheduling

Use CodexClaw cron if available, or system cron + `codex exec` as fallback.
