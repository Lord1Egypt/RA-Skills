---
name: voice-memory
description: Your voice agent remembers forever. Give voice agents automatic memory of every conversation using BlueColumn. Use when a voice/phone agent must remember callers, meetings, coaching sessions, sales calls, or journal entries; when wiring voice transcripts into BlueColumn; or when a caller needs continuity across calls. Requires a BlueColumn API key (bc_live_*).
---

# Voice Memory — BlueColumn

Your voice agent remembers forever. Powered by BlueColumn (bluecolumn.ai).

This skill is the ClawHub-facing wrapper for the full voice-memory feature suite (Voice Memory, Voice Context, Voice Journal, Voice CRM, Voice Meeting Memory, Voice Coaching Memory, Voice Sales Memory).

## Store a call
```bash
curl -X POST .../agent-remember \
  -H "Authorization: Bearer <key>" -H "Content-Type: application/json" \
  -d '{"text": "Caller +12065550123 asked about pricing, prefers email follow-up.", "title": "Voice call - +12065550123"}'
```

## Recall before answering
```bash
curl -X POST .../agent-recall \
  -H "Authorization: Bearer <key>" -H "Content-Type: application/json" \
  -d '{"q": "What do we know about this caller and past conversations?"}'
```

## Full suite
See `~/.openclaw/workspace/voice-memory-features/` for the 7 feature modules (Python) with offline tests.
