---
name: voice-agent-memory
description: Full-stack voice agent with BlueColumn persistent memory. Make and receive phone calls with real-time transcription, automatic vector memory storage, and cross-call recall. Every call remembers who called, what they said, and what happened last time.
version: 1.0.0
author: BlueColumn Consulting
keywords:
  - voice
  - phone
  - twilio
  - elevenlabs
  - deepgram
  - memory
  - bluecolumn
  - recall
  - audio
  - transcription
  - voice-agent
permissions:
  network:
    - "https://api.twilio.com"
    - "https://api.elevenlabs.io"
    - "https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1"
    - "https://api.anthropic.com"
  files:
    read:
      - "~/.openclaw/workspace/skills/voice-agent-memory/.env"
      - "~/.openclaw/workspace/skills/voice-agent-memory/contacts.json"
      - "~/.openclaw/workspace/memory/voice-calls/"
    write:
      - "~/.openclaw/workspace/memory/voice-calls/"
dependencies:
  required:
    - name: python3
      reason: Runs the voice bridge server
    - name: curl
      reason: API calls to BlueColumn and Twilio
  pip:
    - fastapi
    - uvicorn
    - httpx
    - anthropic
    - python-dotenv
---

# 🎙️ Voice Agent Memory — Cross-Call BlueColumn Recall

**Give your AI agent a phone number and a memory that never forgets.**

This skill connects Twilio telephony → ElevenLabs/Deepgram voice engine → BlueColumn vector memory in one integrated pipeline. Every call is automatically transcribed, stored in BlueColumn, and recalled before the next call from that caller.

## Why This Exists

The existing skills in the ecosystem are **fragmented**:

| Skill | Does Voice Calls? | Has Vector Memory? | Auto-Recall on Answer? |
|---|---|---|---|
| `phone-voice` | ✅ ElevenLabs + Twilio | ❌ Flat files only | ❌ |
| `bluecolumn-memory` | ❌ | ✅ Text/docs/audio | ❌ |
| `meeting-memory` | ❌ | ✅ Meeting transcripts | ❌ |
| `clawvoice` (external) | ✅ Plugin | ❌ Sandbox files only | ❌ |
| **voice-agent-memory** 🆕 | ✅ | ✅ BlueColumn vectors | ✅ |

## Architecture

```
                  ┌─────────────────────────┐
                  │      Twilio Phone #     │
                  │     +1 (929) 828-8689   │
                  └──────────┬──────────────┘
                             │ SIP / Webhook
                             ▼
                  ┌─────────────────────────┐
                  │  ElevenLabs Agent (TTS) │
                  │  or Deepgram Voice Agt  │
                  └──────────┬──────────────┘
                             │ /v1/chat/completions
                             ▼
                  ┌─────────────────────────┐
                  │   Voice Bridge Server   │ ←── port 8013
                  │   (FastAPI + Claude)    │
                  └──┬─────────────────┬────┘
                     │                 │
          ┌──────────▼────┐    ┌───────▼──────────┐
          │  BlueColumn   │    │  Cost Tracking   │
          │  /agent-recall│    │  Transcript Logs │
          │  /agent-store │    │  Call Analytics  │
          └───────────────┘    └──────────────────┘

  CALL FLOW:
  1. Phone rings → Twilio routes to ElevenLabs
  2. ElevenLabs → Voice Bridge (port 8013) with caller ID
  3. Bridge → BlueColumn recall: "what do we know about +12065550123?"
  4. Bridge injects memory into Claude's system prompt
  5. Claude responds → ElevenLabs TTS → Caller hears
  6. After call → Bridge auto-stores transcript → BlueColumn
```

## What Makes This Different

### 1️⃣ Caller-Based Memory Isolation
Each phone number gets its own memory namespace. When `+12065550123` calls:
- BlueColumn recalls every past interaction from that caller
- Agent greets them by name, picks up where they left off
- No cross-contamination between callers

### 2️⃣ Auto-Transcribe + Auto-Store
Every call transcript is automatically:
1. Truncated/summarized to key info
2. Pushed to BlueColumn `/agent-remember` with caller phone as title
3. Tagged with `voice-call`, caller number, and date
4. Available for recall on the NEXT call before the agent says a word

### 3️⃣ Pre-Call Context Injection
On inbound call, before the agent speaks:
1. Bridge reads caller ID from ElevenLabs metadata
2. Queries BlueColumn: "what do I know about [caller]?"
3. Injects answer into Claude's system prompt
4. Agent starts the call already informed

### 4️⃣ Real-Time Streaming Recall (Optional)
Mid-call recall queries:
- Agent can ask "what did we discuss about pricing last time?"
- Bridge streams recall results into the conversation context
- Sub-100ms recall means no awkward pauses

---

## Setup

### Prerequisites
- OpenClaw running (gateway on port 18789)
- Twilio account + phone number (already configured: +1 (929) 828-8689)
- BlueColumn API key (already configured: bc_live_*)
- ElevenLabs account + API key
- Anthropic API key (already configured)
- Cloudflare tunnel or ngrok (for exposing bridge to ElevenLabs)

### Step 1: Configure Environment

```bash
# Copy template
cp .env.example .env
# Edit with your keys
```

### Step 2: Install Dependencies

```bash
cd ~/.openclaw/workspace/skills/voice-agent-memory
pip install -r requirements.txt
# Or individually:
pip install fastapi uvicorn httpx anthropic python-dotenv
```

### Step 3: Start the Bridge Server

```bash
python3 bridge/server.py
# Starts on port 8013
# Endpoint: POST /v1/chat/completions
```

### Step 4: Expose with Cloudflare Tunnel

```bash
# If using existing tunnel:
cloudflared tunnel --url http://localhost:8013

# Or configure a permanent tunnel in Cloudflare dashboard
# Point a subdomain to localhost:8013
```

### Step 5: Configure ElevenLabs Agent

In ElevenLabs dashboard:
1. Create a Conversational AI Agent
2. Set Custom LLM URL to: `https://your-tunnel.ngrok.dev/v1/chat/completions`
3. Add auth header: `Authorization: Bearer <your-bridge-token>`
4. Set your Twilio number as the agent's phone number

### Step 6: Connect Twilio

In ElevenLabs agent settings → Phone section:
1. Enter Twilio Account SID and Auth Token
2. Select your Twilio phone number
3. Save — your number is now live with BlueColumn memory

---

## How It Works (Detailed)

### BlueColumn Integration

The bridge uses three BlueColumn API endpoints:

```
Base URL: https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1
```

#### Pre-Call Recall (on inbound ring)
```python
# Before agent speaks, query memory for this caller
POST /agent-recall
{
  "q": "What do I know about caller +12065550123?"
}
# Response:
{
  "answer": "Joe Pagano set up BlueColumn... prefers bullet points...",
  "sources": [...]  # With relevance scores
}
```

#### Post-Call Storage (after call ends)
```python
# Store the conversation summary
POST /agent-remember
{
  "text": "Full transcript or summary of the call...",
  "title": "Voice call - +12065550123 - 2026-06-08"
}
# Response:
{
  "session_id": "sess_...",
  "summary": "Discussed pricing plans...",
  "action_items": ["Send proposal by Friday"]
}
```

#### Mid-Call Quick Note (during call)
```python
# Agent saves an observation mid-conversation
POST /agent-note
{
  "text": "Caller prefers email over phone for follow-up",
  "tags": ["voice-call", "+12065550123", "preference"]
}
```

### Memory Prompts (Zero→First→Nth Call)

| Call # | Memory State | Experience |
|--------|-------------|------------|
| **1st call** | No memory | "Hi, this is Leon from BlueColumn. How can I help you today?" |
| **2nd call** | Recalls 1st call | "Welcome back, Joe! Last time we discussed your pricing concerns. Did you have a chance to review the plans?" |
| **3rd call+** | Rich history | "Hey Joe, good to hear from you again. I see you asked about the Developer plan last time — want to pick up where we left off?" |

---

## Voice Bridge Server

The bridge server (`bridge/server.py`) handles:

- **HTTP Method**: POST
- **Endpoint**: `/v1/chat/completions` (OpenAI-compatible)
- **Auth**: Bearer token in `Authorization` header
- **Streaming**: SSE-based streaming (ElevenLabs expects this)
- **Model routing**: Claude Sonnet 4 (via Anthropic API) or OpenClaw gateway

### Key Features in the Bridge

1. **Parallel recall**: Starts BlueColumn recall in a background task while initializing the Claude stream — if recall finishes in <2s, it's injected; if slow, the call proceeds without it
2. **Fire-and-forget memory**: After each call exchange, the conversation is auto-stored to BlueColumn asynchronously
3. **Cost tracking**: Logs per-call costs (Twilio + ElevenLabs + Anthropic) to JSONL for analytics
4. **Caller identification**: Extracts caller ID from ElevenLabs metadata for memory namespacing

---

## BlueColumn Audio API (Direct Audio Ingestion)

BlueColumn also accepts audio files directly — useful for uploading call recordings post-hoc:

```bash
# Upload a recorded call for memory storage
curl -X POST https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1/agent-remember \
  -H "Authorization: Bearer bc_live_YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "audio_url": "https://your-storage/call-recording-2026-06-08.mp3",
    "title": "Voice call recording - +12065550123 - 2026-06-08"
  }'

# Or upload via file URL (PDFs also supported)
curl -X POST .../agent-remember \
  -d '{
    "file_url": "https://your-storage/transcript.pdf",
    "title": "Call transcript - +12065550123"
  }'
```

---

## Outbound Calling

In addition to inbound, the bridge supports outbound calls:

```bash
# Trigger an outbound call from the agent
curl -X POST http://localhost:8013/call/outbound \
  -H "Authorization: Bearer <bridge-token>" \
  -d '{
    "to": "+12065550123",
    "purpose": "Follow up on pricing page deadline",
    "pre_call_recall": true
  }'
```

The bridge will:
1. Query BlueColumn for context about this caller
2. Initiate the call via Twilio
3. Inject memory into the agent's prompt before the call connects
4. Auto-store the transcript after the call

---

## Costs

Estimated per-minute:
| Component | Cost |
|-----------|------|
| Twilio (inbound) | ~$0.01/min |
| ElevenLabs TTS | ~$0.05/min (varies by voice) |
| Anthropic Claude | ~$0.01/min (varies by tokens) |
| BlueColumn API | ~$0.002/recall + $0.003/remember |
| **Total** | **~$0.07–0.08/min** |

---

## Files

```
voice-agent-memory/
├── SKILL.md              ← This file
├── .env.example          ← Config template
├── requirements.txt      ← Python dependencies
├── bridge/
│   ├── server.py         ← FastAPI bridge (port 8013)
│   ├── prompt_builder.py ← System prompt + memory injection
│   └── memory.py         ← BlueColumn recall/store helpers
├── scripts/
│   ├── start.sh          ← Start the bridge server
│   ├── test-recall.sh    ← Test BlueColumn recall for a caller
│   └── test-call.sh      ← Test making an outbound call
└── contacts.json         ← Whitelisted callers
```

---

## Testing

```bash
# Test BlueColumn recall for a specific caller
./scripts/test-recall.sh +12065550123

# Test the bridge directly (simulate ElevenLabs)
curl -X POST http://localhost:8013/v1/chat/completions \
  -H "Authorization: Bearer <bridge-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4",
    "messages": [
      {"role": "user", "content": "Hello, this is Joe calling again"}
    ],
    "stream": false
  }'

# Check call logs
tail -f ~/.openclaw/workspace/memory/voice-calls/costs.jsonl
```

---

## License

MIT — built on BlueColumn.ai and OpenClaw.
