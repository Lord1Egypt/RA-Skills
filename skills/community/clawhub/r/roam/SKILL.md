---
name: roam
description: >
  Interact with Roam HQ via REST API. Search meetings, get transcripts,
  prompt transcripts with AI, send messages, and manage groups. Use when
  the user asks about meetings, call notes, transcripts, or wants to send
  messages in Roam.
metadata:
  {
    "openclaw":
      {
        "emoji": "🏢",
        "requires": { "env": ["ROAM_API_KEY"] },
        "primaryEnv": "ROAM_API_KEY",
      },
  }
---

# Roam HQ

API docs: https://developer.ro.am — fetch endpoint details from there as needed.

## Auth

`ROAM_API_KEY` env var (Personal Access Token from Roam Settings → Developer).

All requests: `Authorization: Bearer $ROAM_API_KEY`

Base URL: `https://api.ro.am`

## Key Endpoints

- `GET /v0/transcript.list` — list meetings (supports `after`, `before`, `limit`)
- `GET /v0/transcript.info?id=<id>` — transcript details + summary
- `POST /v0/transcript.prompt` `{ "id": "...", "prompt": "..." }` — AI analysis of a transcript
- `POST /v0/chat.post` `{ "groupId": "...", "text": "..." }` — send a message
- `GET /v0/chat.history?groupId=<id>` — message history
- `GET /v1/groups.list` — list groups

## Rate Limits

10 burst, 1 req/sec sustained. Respect `Retry-After` on 429s.

## Common Patterns

1. **Summarize recent meetings:** `transcript.list` → `transcript.prompt` for each
2. **Find discussions about a topic/person:** `transcript.list` → filter by participants → `transcript.prompt`
3. **Post follow-up:** Get transcript → prompt for action items → `chat.post` to a group
