---
name: verbatik-tts-assistant
version: 1.0.0
title: Text-to-Speech & Voice Cloning Assistant (via Verbatik)
description: Turn your AI assistant into a TTS and voice cloning powerhouse using the Verbatik API. Use when generating speech from text, cloning voices, managing cloned voices, browsing 2700+ pre-trained voices, or checking account balance. Covers standard TTS, cloned voice TTS with emotion/speed/pitch controls, voice cloning from audio, and prepaid billing.
license: MIT
author: Verbatik
homepage: https://api.verbatik.com
keywords: tts, text-to-speech, voice-cloning, speech-synthesis, audio, verbatik, voices, ai-voice
metadata:
  openclaw:
    requires:
      env:
        - VERBATIK_API_KEY
    primaryEnv: VERBATIK_API_KEY
---

# Text-to-Speech & Voice Cloning Assistant (via Verbatik)

Autonomously generate speech, clone voices, and manage audio via the [Verbatik](https://api.verbatik.com) API.

## Setup

1. Create a Verbatik account at [api.verbatik.com](https://api.verbatik.com)
2. Top up your prepaid balance (Settings → Billing)
3. Generate an API key (Settings → API Keys)
4. Store your API key:
   ```
   VERBATIK_API_KEY=vbt_your_api_key_here
   ```

## Auth

All requests use Bearer token:
```
Authorization: Bearer <VERBATIK_API_KEY>
```

Base URL: `https://api.verbatik.com`

## MCP (Model Context Protocol)

Verbatik also exposes an MCP server for direct AI assistant integration. Endpoint:
```
https://api.verbatik.com/api/mcp/mcp
```
Supports OAuth 2.1 (one-click connect in Claude Desktop) and API key auth via `mcp-remote` bridge.

## Core Workflow

### 1. List Available Voices
```
GET /api/v1/voices
```
Query params:
- `language` — filter by language code (e.g. `en-US`, `fr-FR`)
- `gender` — `Male`, `Female`, or `Neutral`
- `search` — search by voice name

Returns array of voices with `id` (slug), `name`, `gender`, `language_code`, `language_name`, `is_neural`, `sample_url`, `styles`.

### 2. Text-to-Speech (Pre-trained Voices)
```
POST /api/v1/tts
Content-Type: text/plain
Authorization: Bearer <key>
X-Voice-ID: jenny-en-us
X-Store-Audio: true

Hello, this is a test of the Verbatik text-to-speech API.
```

Headers:
- `Content-Type` — `text/plain` or `application/ssml+xml` for SSML
- `X-Voice-ID` — voice slug (e.g. `jenny-en-us`). Defaults to Jenny if omitted
- `X-Store-Audio` — `true` to get a stored URL back, `false` for binary audio stream

Max text length: 50,000 characters. Large texts are automatically chunked.

Cost: **$0.002 per 1,000 characters**

Response (when `X-Store-Audio: true`):
```json
{
  "success": true,
  "audio_url": "https://...",
  "characters_processed": 52,
  "chunks_processed": 1,
  "response_time_ms": 1200,
  "cost_cents": 1
}
```

Response (when `X-Store-Audio: false`): Binary audio with metadata in response headers (`X-Characters-Processed`, `X-Cost-Cents`, `X-Balance-Cents`).

### 3. Clone a Voice
```
POST /api/v1/voice-training
Content-Type: application/json
Authorization: Bearer <key>

{
  "audio_url": "https://example.com/sample.mp3",
  "name": "My Voice",
  "noise_reduction": true,
  "volume_normalization": true,
  "preview_text": "Hello, this is a preview of my cloned voice!"
}
```

Requirements:
- Audio must be at least 10 seconds of speech
- Supported formats: `.mp3`, `.wav` (max 20MB)
- Cost: **$3.00 per clone**

Response:
```json
{
  "success": true,
  "voice_id": "uuid-here",
  "name": "My Voice",
  "fal_voice_id": "...",
  "preview_url": "https://...",
  "cost_cents": 300
}
```

### 4. Generate Speech with Cloned Voice
```
POST /api/v1/voice-cloning
Content-Type: text/plain
Authorization: Bearer <key>
X-Voice-ID: <cloned_voice_uuid>
X-Store-Audio: true

Hello from my cloned voice!
```

Optional headers for voice control:
- `X-Speed` — `0.5` to `2.0` (default: 1)
- `X-Volume` — `0` to `10` (default: 1)
- `X-Pitch` — `-12` to `12` (default: 0)
- `X-Emotion` — `happy`, `sad`, `angry`, `fearful`, `disgusted`, `surprised`, `neutral`
- `X-Format` — `mp3`, `pcm`, `flac` (default: mp3)
- `X-Language-Boost` — language to enhance (e.g. `English`, `French`, `Japanese`)
- `X-Sample-Rate` — `8000`, `16000`, `22050`, `24000`, `32000`, `44100`
- `X-Bitrate` — `32000`, `64000`, `128000`, `256000`

Voice modification (Speech 2.8 Turbo):
- `X-Voice-Modify-Pitch` — `-100` to `100`
- `X-Voice-Modify-Intensity` — `-100` to `100`
- `X-Voice-Modify-Timbre` — `-100` to `100`

Supports interjection tags in text: `(laughs)`, `(sighs)`, `(coughs)`, `(clears throat)`, `(gasps)`, `(sniffs)`, `(groans)`, `(yawns)`

Supports pause markers: `<#x#>` where x = 0.01–99.99 seconds

Max text length: 5,000 characters. Cost: **$0.10 per 1,000 characters**

### 5. Manage Cloned Voices

**List all cloned voices:**
```
GET /api/v1/my-voices
```
Optional query param: `status` — `pending`, `ready`, or `failed`

**Get a specific voice:**
```
GET /api/v1/my-voices/<voice_id>
```

**Delete a voice:**
```
DELETE /api/v1/my-voices/<voice_id>
```

### 6. Preview a Pre-trained Voice
```
GET /api/v1/preview/<voice_slug>
```
Returns binary audio preview. No auth required. Cached for 24 hours.

## Pricing

| Action | Cost |
|--------|------|
| Standard TTS (pre-trained voices) | $0.002 / 1,000 chars |
| Cloned Voice TTS | $0.10 / 1,000 chars |
| Voice Cloning | $3.00 / clone |
| List voices, check balance, estimate cost | Free |

All usage is deducted from your prepaid balance. Auto top-up is available.

## Error Handling

| Status | Meaning |
|--------|---------|
| 401 | Invalid or missing API key |
| 402 | Insufficient balance — top up required |
| 400 | Bad request (invalid params, text too long, voice not found) |
| 404 | Voice not found or doesn't belong to your workspace |
| 429 | Rate limit exceeded — check `Retry-After` header |
| 500 | Server error |

## Tips

- Always use `X-Store-Audio: true` when you need a shareable URL — binary mode is for streaming
- Use voice slugs (e.g. `jenny-en-us`) not internal IDs for pre-trained voices
- Use UUIDs from `voice-training` or `my-voices` for cloned voices
- Clone voices with clean audio (minimal background noise) for best results
- Use `noise_reduction: true` when cloning from imperfect audio
- Cloned voices expire after 7 days of inactivity — Verbatik auto-refreshes them via cron
- Estimate costs before large batches with the `estimate_cost` MCP tool
- Check your balance before bulk operations to avoid 402 errors
- Use emotion and speed controls on cloned voices for more natural output
- SSML is supported for pre-trained voices — use `Content-Type: application/ssml+xml`
