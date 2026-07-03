---
name: beeper
description: Send and search messages across WhatsApp, LinkedIn, Instagram, Discord, Telegram, Signal, Messenger, Slack, and other Beeper-connected networks through the Beeper Desktop API. Use when an agent needs operator-approved cross-channel messaging, chat lookup, message search, or local DM history access through Beeper.
---

# Beeper Desktop API Skill

Use this skill when an agent needs to work with the operator's own Beeper-connected chats through Beeper Desktop's local API.

Beeper Desktop must already be installed, logged in, and running on a trusted machine. This skill does not create Beeper accounts, bypass platform permissions, or read messages unless the operator has enabled Beeper Desktop API access.

## What It Covers

- List connected Beeper accounts.
- List recent chats across connected networks.
- Search chats by person, group, or title.
- Search messages across Beeper's indexed local history.
- Read messages from a specific chat ID.
- Send a message to a matched chat after operator approval.
- Use Beeper through a local API endpoint or a local SSH tunnel to another trusted machine.

## Requirements

1. Beeper Desktop installed and running.
2. Beeper Desktop API enabled in Beeper settings under Developers.
3. API key stored in one of:
   - `BEEPER_API_KEY`
   - `$HOME/.config/beeper/api-key`
   - `$HOME/.config/beeper/config.json` with an `api_key` field
4. `curl` and `jq`.
5. Optional: SSH access to the machine running Beeper Desktop if the agent runs elsewhere.

## Configuration

For a local Beeper Desktop API:

```bash
export BEEPER_API_BASE="http://127.0.0.1:23373"
export BEEPER_API_KEY="paste-api-key-here"
```

For a remote Beeper Desktop API reached through SSH, create a local tunnel first:

```bash
ssh -N -L 23373:127.0.0.1:23373 user@beeper-host
export BEEPER_API_BASE="http://127.0.0.1:23373"
```

You can also set `BEEPER_SSH_HOST=user@beeper-host` and let the helper scripts call `curl` through SSH. The tunnel approach is usually cleaner for long-running agents.

## Quick Start

```bash
# Test the API
scripts/beeper.sh test

# List accounts
scripts/beeper.sh accounts

# List recent chats
scripts/beeper.sh chats 20

# Search chats
scripts/search-chats.sh "Kinan"

# Search message history
scripts/beeper.sh search "gbrain"

# Read messages from a chat ID
scripts/beeper.sh messages '!chat-id:beeper.local' 50

# Send a message by recipient/chat title match
scripts/send-message.sh "Kinan" "Following up on this."
```

## API Reference

Default base URL: `http://127.0.0.1:23373`

Authentication: `Authorization: Bearer <api-key>`

Common endpoints:

- `GET /v1/accounts`
- `GET /v1/chats?limit=100`
- `GET /v1/chats/search?query=name`
- `GET /v1/chats/{chatID}/messages?limit=50`
- `GET /v1/messages/search?query=keyword`
- `POST /v1/chats/{chatID}/messages`

Official API docs: `https://developers.beeper.com/desktop-api-reference`

## Messaging Rules

- Do not send messages without explicit operator approval.
- Search and read only the chats needed for the requested task.
- Treat DMs and message exports as private operator data.
- Do not paste API keys into prompts, config pages, or public logs.
- Prefer chat search and message search before bulk crawling.
- Bulk backup/crawl should be an explicit operator request because it can export a large private archive.

## When To Use This Instead Of Platform APIs

Use Beeper when the operator wants one local messaging surface across many networks, especially when Discord DMs, WhatsApp, LinkedIn, Telegram, Instagram, Signal, Messenger, or Slack are all reachable from the same Beeper account.

Use a native platform API when you need workspace-level administration, moderation actions, bot-only behavior, or server/channel operations that Beeper does not expose.

