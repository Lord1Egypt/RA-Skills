---
name: whisper-tailnet-api
description: Consume the shared Whisper speech-to-text API over Tailnet at http://100.92.116.99:8765 using OpenAI-compatible audio transcription endpoint (/v1/audio/transcriptions). Use when an agent needs remote transcription checks, request examples, language hints, timing tests, or troubleshooting response/output.
---

# Whisper STT API over Tailnet (OpenAI-compatible)

Use this guide to call the shared Whisper server.

## Endpoint

- **Base URL:** `http://100.92.116.99:8765`
- **Health:** `GET /health`
- **Transcribe:** `POST /v1/audio/transcriptions` (raw binary body)

## Quick health check

```bash
curl -sS http://100.92.116.99:8765/health
```

## Transcribe audio (recommended)

```bash
curl -sS -X POST \
  --data-binary @/path/to/audio.wav \
  "http://100.92.116.99:8765/v1/audio/transcriptions?ext=.wav"
```

## Time the request

```bash
time curl -sS -X POST \
  --data-binary @/path/to/audio.wav \
  "http://100.92.116.99:8765/v1/audio/transcriptions?ext=.wav"
```

## Notes

- Prefer this OpenAI-compatible route over `/transcribe` on this host.
- Pass file type via `ext` query (example: `.wav`, `.mp3`, `.m4a`).
- Use `language` query when known to improve accuracy.

## Expected response shape

```json
{
  "text": "transcribed text...",
  "model": "turbo"
}
```
