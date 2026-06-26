---
name: agent-memory
description: Long-term Telegram memory for AI agents — search conversations, get digests, extract decisions. Connects to any Telegram channel via user's own account.
version: 0.2.0
metadata:
  openclaw:
    requires:
      env:
        - AGENT_MEMORY_API_KEY
      bins:
        - curl
    primaryEnv: AGENT_MEMORY_API_KEY
---

# Agent Memory — Telegram Memory for AI Agents

Gives you persistent long-term memory across Telegram channels and groups. Search conversations, generate digests, extract decisions and action items.

## First Run (if AGENT_MEMORY_API_KEY is not set)

When the user asks anything related to Telegram memory, channels, or this skill, and `AGENT_MEMORY_API_KEY` is not configured, walk them through setup:

1. Tell the user: "To use Telegram memory, you need an API key. Open @AgentMemoryBot in Telegram: https://t.me/AgentMemoryBot"
2. In the bot: press /start → 📱 Connect Telegram (share contact, enter reversed code) → 🔑 API Keys → ➕ Create Key
3. Ask the user to paste the key (starts with `amk_`)
4. Once they give you the key, save it to the OpenClaw config:

```bash
# Add to openclaw.json skills config
cat ~/.openclaw/openclaw.json | jq '.skills.entries["agent-memory"] = {"env": {"AGENT_MEMORY_API_KEY": "USER_KEY_HERE"}}' > /tmp/oc.json && mv /tmp/oc.json ~/.openclaw/openclaw.json
```

Or if openclaw.json doesn't exist or has no skills section, create it. Then tell the user to restart the OpenClaw session.

## How to Use

All API calls use: `Authorization: Bearer $AGENT_MEMORY_API_KEY`
Base URL: `https://agent.ai-vfx.com`

### Search Memory
Find information across synced Telegram channels. Use for any question about channel content.

```bash
curl -s -X POST https://agent.ai-vfx.com/api/v1/memory/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_MEMORY_API_KEY" \
  -d '{"query": "what was discussed about topic X", "scope": "@channel", "limit": 10}'
```

- `scope`: optional — `@username` for one channel, `folder:Name` for a folder, omit for all
- Response: `{"answer": "...", "sources": [{"url": "https://t.me/...", "channel": "..."}]}`

### List Sources
See which channels are connected.

```bash
curl -s https://agent.ai-vfx.com/api/v1/sources \
  -H "Authorization: Bearer $AGENT_MEMORY_API_KEY"
```

### Add Source
Connect a new Telegram channel. User must have connected their Telegram in the bot first.

```bash
curl -s -X POST https://agent.ai-vfx.com/api/v1/sources/add \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_MEMORY_API_KEY" \
  -d '{"handle": "@channel_username", "sync_range": "1m"}'
```

sync_range options: 1w, 1m, 3m, 6m, 1y

### Get Digest
Summarize conversations for a period.

```bash
curl -s -X POST https://agent.ai-vfx.com/api/v1/digest \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_MEMORY_API_KEY" \
  -d '{"scope": "@channel", "period": "7d"}'
```

period options: 1d, 3d, 7d, 30d

### Extract Decisions
Get decisions, action items, and open questions.

```bash
curl -s -X POST https://agent.ai-vfx.com/api/v1/decisions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGENT_MEMORY_API_KEY" \
  -d '{"scope": "@channel", "topic": "optional filter"}'
```

### Sync Status
Check if channels are still syncing after add_source.

```bash
curl -s https://agent.ai-vfx.com/api/v1/sync-status \
  -H "Authorization: Bearer $AGENT_MEMORY_API_KEY"
```

### Balance
Check remaining points.

```bash
curl -s https://agent.ai-vfx.com/api/v1/account/balance \
  -H "Authorization: Bearer $AGENT_MEMORY_API_KEY"
```

## When to Use Which Operation

- "What did they discuss about X?" → **search** with the topic as query
- "What happened this week in @channel?" → **digest** with period=7d
- "What decisions were made?" → **decisions**
- "Connect @newchannel" → **add_source**, then wait and check **sync_status**
- "What channels do I have?" → **list_sources**
- "How many points left?" → **balance**

## Costs

1 point ≈ $0.01. Search: 3 pts, Digest: 25 pts, Decisions: 12 pts. Top up via TON in @AgentMemoryBot.
