---
name: streaming-audio-memory
description: Ingest live edge-device audio (car, doorbell, wearable, kiosk) into per-device streaming memory and recall what a device heard. Use when an agent streams audio chunks from devices, monitors ambient audio, or answers questions about a device's audio history. Requires a BlueColumn API key (bc_live_*).
---

# Streaming Audio Memory — BlueColumn Skill

Stream audio chunks from any edge device into persistent, per-device memory.
Each chunk is transcribed (Whisper large-v3), mined for entities and intent,
and indexed under `<namespace>_audio_streaming_<deviceId>` for instant recall.

## Setup
Read `TOOLS.md` or the platform secret store for the BlueColumn API key (`bc_live_*`). Base URL: `https://xkjkwqbfvkswwdmbtndo.supabase.co/functions/v1`

## Ingest a chunk
```bash
curl -X POST .../streaming-audio \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"deviceId": "dashcam-01", "audio": "<base64>", "format": "wav",
       "sampleRate": 16000, "timestamp": 1756000000000,
       "idempotencyKey": "chunk_dashcam-01_1756000000000_a1b2c3d4e5f6"}'
```

Idempotency key format: `chunk_<deviceId>_<epoch-ms>_<6-12 hex>`. Same key +
same body returns the cached response; same key + different body = 409. Retries
never double-process.

## Recall what a device heard
```bash
curl -X POST .../streaming-audio/query \
  -H "Authorization: Bearer <key>" \
  -H "Content-Type: application/json" \
  -d '{"deviceId": "dashcam-01", "query": "what happened near the warehouse?"}'
```

Add `?stream=1` (or `Accept: text/event-stream`) for SSE: `sources` →
`delta` → `done` events.

## Pipeline (per chunk)
1. Transcription — Groq Whisper large-v3
2. Entity extraction — people / locations / events / actions
3. Intent classification — query | command | notification | warning | conversation
4. Persist — indexed segment in the device namespace
5. Session summary — auto-summarized after 30s silence or 5 min of stream

## Workflow
1. Buffer device audio client-side in 5–30s chunks (WAV/Opus/PCM/MP3)
2. POST each chunk with a fresh idempotency key
3. On user/environment questions, hit `/streaming-audio/query` for that device
4. Surface `session_summary` memories for long-horizon context
