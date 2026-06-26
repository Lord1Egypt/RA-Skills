# OpenClaw Integration

tts-router exposes a `/v1/audio/speech` endpoint that is fully compatible with the OpenAI TTS API.
OpenClaw supports custom OpenAI-compatible TTS providers via `baseUrl` override.

See OpenClaw TTS configuration docs: https://docs.openclaw.ai/gateway/configuration-reference#tts-text-to-speech

## Setup

1. Start tts-router:
   ```bash
   tts-router pull qwen3-tts
   tts-router serve
   ```

2. Add to `~/.openclaw/openclaw.json`:
   ```json
   {
     "messages": {
       "tts": {
         "provider": "openai",
         "openai": {
           "baseUrl": "http://localhost:8091/v1",
           "model": "qwen3-tts",
           "voice": "Vivian"
         }
       }
     }
   }
   ```
