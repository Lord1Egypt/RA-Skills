---
name: voice-memory-features
description: Give voice agents automatic memory of every conversation using BlueColumn. Seven features: Voice Memory (auto-remember every call), Voice Context (recall before answering), Voice Journal (store spoken thoughts), Voice CRM (remember customer conversations and preferences), Voice Meeting Memory (record/transcribe/summarize meetings), Voice Coaching Memory (track goals and progress), Voice Sales Memory (remember objections, follow-ups, and customer history). Use when a voice/phone agent needs to remember callers, meetings, coaching sessions, sales calls, or journal entries; when wiring voice transcripts into BlueColumn; or when a caller needs continuity across calls.
version: 1.0.0
author: BlueColumn
keywords: [voice, memory, recall, bluecolumn, crm, journal, meeting, coaching, sales, context]
permissions:
  network:
    - "https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1"
---

# 🎙️ Voice Memory — Seven BlueColumn Voice Features

Automatic voice memory for every conversation. Powered by BlueColumn (bluecolumn.ai).

## The 7 Features (from Voice-Memory.txt directive)

| # | Feature | What it does | Module |
|---|---|---|---|
| 1 | **Voice Memory** | Automatically remember every conversation | `features/voice_memory.py` |
| 2 | **Voice Context** | Recall relevant memories before answering | `features/voice_context.py` |
| 3 | **Voice Journal** | Store every spoken thought as searchable memories | `features/voice_journal.py` |
| 4 | **Voice CRM** | Remember customer conversations and preferences | `features/voice_crm.py` |
| 5 | **Voice Meeting Memory** | Record, transcribe, summarize, and remember meetings | `features/voice_meeting.py` |
| 6 | **Voice Coaching Memory** | Track goals and progress across coaching sessions | `features/voice_coaching.py` |
| 7 | **Voice Sales Memory** | Remember objections, follow-ups, and customer history | `features/voice_sales.py` |

## Quick Start

```bash
pip install -r requirements.txt
export BLUECOLUMN_API_KEY=bc_live_YOUR_KEY
python -m pytest tests/ -q   # run the offline tests
```

## Core Engine (`features/voice_memory.py`)

- `await remember(text, title, tags)` → stores a conversation, returns `session_id`
- `await recall(q)` → natural-language recall, returns `answer` + `sources`
- `await note(text, tags)` → quick observation

## Feature Usage Examples

### 1 · Voice Memory — remember every conversation
```python
from features.voice_memory import remember
await remember("Caller said they prefer email follow-up.", title="Voice call - +12065550123")
```

### 2 · Voice Context — recall before answering
```python
from features.voice_context import get_context, build_context_block
ctx = await get_context("pricing question")
system_prompt += build_context_block(ctx["context"])
```

### 3 · Voice Journal — store spoken thoughts
```python
from features.voice_journal import journal_entry
await journal_entry("Idea: build a voice CRM feature.", mood="excited")
```

### 4 · Voice CRM — customer conversations + preferences
```python
from features.voice_crm import log_customer_interaction, customer_profile
await log_customer_interaction("Acme Corp", "discussed renewal, wants proposal")
print(await customer_profile("Acme Corp"))
```

### 5 · Voice Meeting Memory — record/summarize meetings
```python
from features.voice_meeting import record_meeting, action_items
await record_meeting("Standup", transcript)
print(await action_items())
```

### 6 · Voice Coaching Memory — goals + progress
```python
from features.voice_coaching import set_goal, log_checkin
await set_goal("Ship MVP by Sep")
await log_checkin("Ship MVP", "on track, risk: design sign-off")
```

### 7 · Voice Sales Memory — objections + follow-ups
```python
from features.voice_sales import log_call, log_objection, pipeline
await log_call("Jane", "discussed pricing", objection="price", next_step="send discount")
print(await pipeline())
```

## Integration with voice-agent-memory

Drop `features/` next to the existing `voice-agent-memory` skill bridge. In `bridge/server.py`:
```python
from features.voice_context import context_for_caller
recalled = await context_for_caller(caller_number, name)
```
Then store the transcript after the call with `voice_memory.remember(...)`.

## Tests

`tests/test_voice_features.py` runs fully offline with a mocked HTTP client — no API key or network needed.

## Docs

Full API reference: https://bluecolumn.ai/docs — fields are `text`, `q`, `tags`.
