---
name: tg-message-assistant
description: >
  Generate topic briefings from Telegram channels. Use this skill when the user mentions
  "briefing", "newsletter", "digest", "message summary", "channel recap", "generate report",
  "send briefing", "scheduled push", or "channel roundup". Also applies when users want
  to compile messages from multiple Telegram channels into structured summaries and
  deliver them to others.
---

# TG Message Assistant (OpenClaw)

Read `../../core/prompt.md` for the full 5-step workflow and interaction principles.

---

## Choose Your Tool Strategy

Before starting, ask the user which approach they prefer.
Explain the options clearly, then proceed with their choice.

### Option 1 (Recommended): Browser Automation

Use Playwright Scraper or any available browser automation tool to interact with
Telegram Web and Gmail Web directly.

| Pros | Cons |
|------|------|
| Zero setup — no Bot tokens or ClawHub installs | Slower than native channel / API |
| Works immediately if logged into Telegram/Gmail in browser | Requires browser session to remain active |
| No BotFather registration needed | Scrolling long channel histories takes time |

### Option 2: Native Channel + ClawHub Skills (Faster, Needs Setup)

Use OpenClaw's native Telegram channel integration and ClawHub email skills.

| Pros | Cons |
|------|------|
| Fast, reliable first-class channel support | Requires BotFather bot + token |
| Built-in cron for recurring tasks | Bot must be added to all target channels |
| Works in background without browser | Requires `clawhub install agentmail` |

---

## Option 1: Browser Automation

Install the Playwright Scraper skill if not already available:
```bash
clawhub install playwright-scraper
```

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

### Cron / Scheduling

OpenClaw has built-in cron. Use it directly to schedule recurring briefing generation.

---

## Option 2: Native Channel + ClawHub Skills

### Telegram (Native Channel)

OpenClaw supports Telegram as a first-class channel:

1. Create a bot via [@BotFather](https://t.me/BotFather) on Telegram.
2. Add the bot token to your `openclaw.json` channels configuration.
3. Add the bot to all target channels before fetching messages.

Once configured, OpenClaw can natively read from and send to Telegram channels.

### Gmail (AgentMail)

```bash
clawhub install agentmail
```

AgentMail provides send, read, reply, search, and organize capabilities.
First use will trigger OAuth — guide the user through browser authorization.

### Cron / Scheduling

OpenClaw's built-in cron works directly with native channel skills.
