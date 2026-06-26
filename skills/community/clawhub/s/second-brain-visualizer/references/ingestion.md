---
title: "Second Brain Visualizer — Ingestion Guide"
version: 1.0.0
---

# Ingestion Guide

## How ingestion works

The parser reads your atom ledger (`memory/second-brain.md`) and converts it to structured JSON. Your job is to get raw ideas from wherever you drop them into that ledger.

There are two approaches:

**Manual** — You write atoms directly into the markdown file. Good for getting started. Fine long-term if you prefer to stay close to the material.

**Automated** — An OpenClaw agent reads your drop channel on a schedule and appends new atoms to the ledger. Drop an idea into Slack at 2am, wake up to find it already parsed and waiting.

This guide covers the automated path for each major channel.

---

## Atom format (what the parser expects)

Every atom in the ledger looks like this:

```markdown
### ts: 1712034567

- **date:** 2026-04-06T14:00:00 UTC
- **raw:** the idea verbatim
- **type:** thought
- **tags:** [tag1, tag2]
- **signal:** hot
- **actionable:** no
- **nextAction:**
```

Your ingestion script produces this format and appends it to the ledger. The timestamp (`ts`) should be Unix epoch seconds. It's the anchor — don't skip it.

---

## Slack

The most common setup. Create a private channel (e.g. `#sb-inbox`) and drop ideas there throughout the day.

**OpenClaw cron to read and append:**

```javascript
// Weekly or daily — reads new messages from your Slack channel
// and appends them as atoms to memory/second-brain.md

const channelId = 'YOUR_CHANNEL_ID'; // e.g. C0AGZG13NFL
const vaultPath = '/path/to/vault/memory/second-brain.md';

// Step 1: Read messages using the message tool
// action=read, channel=slack, channelId=channelId, limit=50, buttons=[]

// Step 2: For each message since last run:
// - Extract text
// - Determine signal (you can prompt an LLM or default to 'warm')
// - Append as atom to second-brain.md

// Step 3: Update last-read timestamp so you don't re-ingest

const atom = `
### ts: ${Math.floor(Date.now() / 1000)}

- **date:** ${new Date().toISOString().replace('T', ' ').slice(0, 19)} UTC
- **raw:** ${messageText}
- **type:** thought
- **tags:** []
- **signal:** warm
- **actionable:** no
- **nextAction:**
`;
```

**Getting your channel ID:** In Slack, right-click the channel name → View channel details → scroll to the bottom. It starts with `C`.

**Recommended schedule:** Weekly pull via cron. Daily if you're a heavy dropper.

---

## Telegram

If you use a Telegram bot or private channel as your drop point.

**Setup:**
1. Create a Telegram bot via @BotFather
2. Add it to your private channel or send messages directly to the bot
3. Store the bot API key in `~/.openclaw/credentials/telegram-sb.json`

**Reading messages:**

```javascript
// Read recent messages from your Telegram bot
const apiKey = 'YOUR_BOT_API_KEY';
const res = await fetch(`https://api.telegram.org/bot${apiKey}/getUpdates?offset=${lastOffset}`);
const updates = await res.json();

for (const update of updates.result) {
  const text = update.message?.text;
  if (!text) continue;
  // append as atom
}
```

**Tip:** OpenClaw's message tool can read Telegram channels directly if your bot is configured. Use `action=read` with your channel target instead of raw API calls.

---

## WhatsApp

WhatsApp doesn't have an official read API for personal accounts. Two practical paths:

**Path A — WhatsApp to Telegram bridge:** Use a service like ManyChat or a personal bridge to forward your WhatsApp messages to a Telegram bot. Then use the Telegram ingestion above.

**Path B — Manual export:** WhatsApp → Export Chat → import the text file and parse it with a custom script. Less elegant, works fine for weekly batch runs.

```bash
# Parse a WhatsApp export file
node references/parse-whatsapp.js ~/Downloads/WhatsApp\ Chat.txt
```

A sample parser for WhatsApp export format is included as an extension in this reference folder.

---

## Gmail

Gmail ingestion is supported but requires advanced setup (Google Cloud project + Gmail API credentials). See the Gmail API documentation for the authorization flow. Once configured, forward ideas to a dedicated `second-brain` label and ingest unread messages on your cron schedule.

---

## Voice (any channel)

The best ideas often arrive when you can't type. Voice to text works with any channel above — iOS and Android both offer voice keyboard input. The transcription won't be clean. That's fine. The parser handles it.

**One tip:** start voice notes with a signal word so you can filter later:

- "Hot idea:" → signal: hot
- "Note to self:" → signal: warm
- "Weird thought:" → signal: cool

You can write a simple pre-processing step that detects these prefixes and sets the signal field automatically.

---

## Scheduling ingestion

Once your ingestion script is working, wire it as an OpenClaw cron:

```bash
openclaw cron add \
  --name "second-brain-ingest" \
  --cron "0 8 * * *" \
  --message "Run second brain ingestion from [channel]. Read new messages since last run, append as atoms to memory/second-brain.md, update last-read timestamp." \
  --model "maple/gpt-oss-120b"
```

Daily at 8am is a good default. Weekly works if you're a lighter dropper.

---

## After ingestion

Once new atoms are in the ledger, run:

```bash
node references/parser.js   # extract atoms to JSON
node references/cluster.js  # re-cluster with new material
```

Or trigger this from Mission Control's Re-cluster button if you're running the full visualizer.
