# Voice Agent Memory — Architecture Overview

```
                    ┌─────────────────────────────┐
                    │      ☎️ Twilio Phone #       │
                    │     +1 (929) 828-8689        │
                    │   (Inbound & Outbound)       │
                    └──────────┬──────────────────┘
                               │ SIP / Webhook
                               ▼
                    ┌─────────────────────────────┐
                    │   🎤 Voice Engine Provider   │
                    │  ElevenLabs Conversational   │
                    │  or Deepgram Voice Agent     │
                    │  (TTS + STT + Barge-in)     │
                    └──────────┬──────────────────┘
                               │ POST /v1/chat/completions
                               │ (OpenAI-compatible format)
                               │ Bearer Token Auth
                               ▼
              ╔══════════════════════════════════╗
              ║   🖥️ Voice Bridge Server         ║
              ║   FastAPI on port 8013            ║
              ║                                   ║
              ║   1. Extract caller ID from req   ║
              ║   2. 🔄 BlueColumn RECALL (2s)   ║
              ║   3. Build system prompt w/ mem   ║
              ║   4. 🌀 Stream Claude response    ║
              ║   5. 💾 Auto-store transcript     ║
              ╚══════════════════════════════════╝
                      │                   │
          ┌───────────▼───────────┐       ▼
          │   🧠 BlueColumn API   │  📝 Cost Tracking
          │                       │  📁 Memory/calls/
          │  /agent-recall   ←─── │  ├─ costs.jsonl
          │  /agent-remember ────→│  └─ transcripts/
          │  /agent-note     ────→│
          │                       │
          │  Pinecone Vectors     │
          │  Voyage Embeddings    │
          └───────────────────────┘

=== Call Lifecycle ===

INBOUND CALL:
  Ring → ElevenLabs → Bridge → BlueColumn Recall → Claude → TTS → Caller

  1. Phone rings           Twilio routes to ElevenLabs agent
  2. ElevenLabs requests   POST /v1/chat/completions (w/ caller ID)
  3. Bridge extracts       Caller phone number from metadata
  4. BlueColumn recall     Async query: "what do I know about +X?"
  5. System prompt built   With memory context (or "first call" fallback)
  6. Claude responds       Streamed back via SSE → ElevenLabs TTS
  7. Post-call storage     Transcript → BlueColumn /agent-remember

OUTBOUND CALL:
  Agent decides → BlueColumn Recall → Twilio → Bridge → Claude → Caller

  1. Agent triggers        POST /call/outbound {to, purpose}
  2. BlueColumn recall     Pre-fetch memory for target caller
  3. Twilio initiates      SIP call to target number
  4. Bridge connects       Same flow as inbound from step 4

=== Memory States ===

  Zero calls ──► No memory ──► "Hi, how can I help?"
    │
    1st call ───► Stored ─────► "Welcome back! Last time we talked about X..."
    │
    2nd call ───► Rich ───────► "Hey Joe, you asked about pricing last time..."
    │
    Nth call ───► Deep ───────► Full context, preferences, history

=== Files ===

  voice-agent-memory/
  ├── SKILL.md              # Full documentation
  ├── ARCHITECTURE.md       # This file
  ├── .env.example          # Config template
  ├── requirements.txt      # Python dependencies
  ├── contacts.json         # Whitelisted callers
  ├── bridge/
  │   ├── server.py         # FastAPI bridge (port 8013)
  │   ├── prompt_builder.py # System prompt + memory injection
  │   └── memory.py         # BlueColumn recall/store helpers
  └── scripts/
      ├── start.sh          # Start the bridge server
      ├── test-recall.sh    # Test BlueColumn recall
      └── test-call.sh      # Test the bridge directly
```
