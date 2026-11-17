---
name: whisper-stt-local-server
description: Ultra-fast local Speech-to-Text bridge (0.2s latency). Optimized for Whisper large-v3-turbo on dedicated GPU infrastructure.
version: 1.0.2
author: Hugo Espuny (@fakehec)
metadata:
  {
    "openclaw":
      {
        "emoji": "🎙️",
        "requires": { "bins": ["curl", "jq"] },
        "tags": ["audio", "stt", "whisper", "local"]
      }
  }
---

# Whisper STT local server

A high-performance bridge to a local Whisper STT server. Designed for real-time conversational AI agents where every millisecond counts.

## Repository
[https://github.com/fakehec/whisper-stt-local-server](https://github.com/fakehec/whisper-stt-local-server)

## Architecture
Redirects all transcription requests to a high-performance local GPU server at `http://localhost:5000`.

## Usage

```bash
{baseDir}/scripts/whisper-bridge.sh /path/to/audio.mp3 large-v3-turbo en
```

## Key Metrics
- **Latency:** ~0.2s for standard voice commands.
- **Accuracy:** High (Whisper large-v3-turbo).
- **Concurrency:** Hybrid thread-managed GPU architecture.
