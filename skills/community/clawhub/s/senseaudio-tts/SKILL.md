---
name: senseaudio-tts
description: Build and debug SenseAudio text-to-speech integrations on `/v1/t2a_v2` and `/ws/v1/t2a_v2`, including sync HTTP, SSE stream, WebSocket event sequencing, hex audio decoding, and voice/audio parameter tuning. Use this whenever user requests TTS generation, low-latency streaming speech, voice selection, or TTS error troubleshooting.
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
compatibility:
  required_credentials:
    - name: SENSEAUDIO_API_KEY
      description: API key from https://senseaudio.cn/platform/api-key
      env_var: SENSEAUDIO_API_KEY
---

# SenseAudio TTS

Use this skill for all SenseAudio speech synthesis tasks.

## Read First

- `references/tts.md`

## Workflow

1. Pick protocol:
- HTTP sync for simple one-shot generation.
- SSE for incremental HTTP audio chunks.
- WebSocket for realtime incremental text-to-audio sessions.

2. Build minimal valid request:
- Auth header, model, text, `voice_setting.voice_id`.
- Add optional tuning only if user asks.

3. Implement output parsing:
- Decode `data.audio` hex to bytes.
- Finalize on terminal status/event.

4. Harden for production:
- Handle auth and parameter errors.
- Add retry/backoff for transient network failures.
- Log session and trace identifiers.

