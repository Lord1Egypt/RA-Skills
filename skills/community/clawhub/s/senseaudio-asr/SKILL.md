---
name: senseaudio-asr
description: Build and troubleshoot SenseAudio speech recognition integrations, including HTTP transcription (`/v1/audio/transcriptions`), realtime WebSocket ASR (`/ws/v1/audio/transcriptions`), audio quality analysis (`/v1/audio/analysis`), and recognition record queries (`/v1/audio/records`). Use this whenever user asks for speech-to-text, diarization, translation, streaming ASR, or ASR model/parameter selection.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - SENSEAUDIO_API_KEY
    primaryEnv: SENSEAUDIO_API_KEY
    homepage: https://senseaudio.cn
---

# SenseAudio ASR

Use this skill for all SenseAudio speech recognition tasks.

Credential source: read the API key from `SENSEAUDIO_API_KEY` and send it only in the `Authorization: Bearer ...` header.
Do not place API keys in query parameters, logs, transcripts, or saved examples.

## Read First

- `references/asr.md`

## Workflow

1. Pick recognition mode:
- HTTP file transcription for offline audio.
- WebSocket for realtime streaming microphone/audio chunks.
- Audio analysis for noise and quality checks before recognition.
- Records query for recent recognition history lookup.

2. Choose model by feature needs:
- Lite for low-cost basic transcription.
- ASR for streaming, translation, diarization, sentiment, and timestamps.
- Pro when diarization plus explicit `max_speakers` control is needed.
- DeepThink for streaming, translation, and intelligent editing; do not send `language`, diarization, sentiment, timestamps, ITN, or punctuation controls.

3. Build minimal request:
- Required auth, file/audio format, model.
- Add optional controls only when needed.
- Keep uploaded files at or below 10MB; split longer audio before sending.

4. Validate compatibility:
- Check model-parameter support before sending.
- Enforce WS `pcm` / `16000Hz` / mono requirements.
- For HTTP `stream=true`, expect SSE text deltas only, not structured verbose fields.

5. Parse robustly:
- Handle JSON/text/verbose/SSE forms.
- Handle WS terminal events and failures.
- Treat returned `audio` URLs, `api_key`, `session_id`, and `trace_id` as sensitive operational data.
