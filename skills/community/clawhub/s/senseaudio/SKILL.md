---
name: senseaudio-open-platform
description: Integration guide for SenseAudio Open Platform APIs, including TTS (sync/SSE/WebSocket), ASR (HTTP/WebSocket), realtime Agents, video generation/storyboard, and voice clone usage constraints. Use this whenever the user asks to build, debug, or optimize any SenseAudio API call, event flow, request schema, response parsing, or production error handling.
---

# SenseAudio Open Platform

Use this skill for implementation work around `api.senseaudio.cn` and `wss://api.senseaudio.cn`.

## Quick Routing

- TTS text-to-speech: read `references/tts.md`
- ASR speech recognition and audio analysis: read `references/asr.md`
- Realtime agent session lifecycle: read `references/agent.md`
- Video generation and storyboard APIs: read `references/video.md`
- Voice plan levels and clone constraints: read `references/voice.md`

Load only the relevant reference file(s) for the user task.

## Default Workflow

1. Confirm capability and protocol:
- TTS: HTTP sync, SSE stream, or WebSocket stream.
- ASR: HTTP file transcription or WebSocket realtime stream.
- Agent: REST lifecycle plus external realtime media channel.
- Video: upload/create/poll/storyboard pipeline.

2. Build a minimal valid request first:
- Add `Authorization: Bearer <API_KEY>`.
- Set required fields only.
- Validate model and endpoint compatibility.

3. Add advanced options only when asked:
- Voice tuning, dictionary, translation, diarization, timestamps, storyboard edits.

4. Parse responses safely:
- Check status fields before using payload data.
- For TTS, decode hex audio to bytes before saving or playback.
- For streams, aggregate chunks and finalize on terminal event/status.

5. Add production hardening:
- Timeout and retry strategy for transient failures.
- Explicit handling of auth, quota, parameter, and not-found errors.
- Structured logs with `trace_id` or session identifiers when available.

## Implementation Rules

- Keep API keys in environment variables, never hardcode secrets.
- Prefer curl first for reproducibility, then provide language SDK code.
- For WebSocket flows, enforce event ordering from the reference docs.
- Keep examples copy-paste runnable.
- If user provides invalid parameter combinations, explain the exact fix.

## Output Checklist

When producing implementation output, include:

1. Chosen endpoint and protocol.
2. Minimal request example.
3. One production-ready version (language requested by user).
4. Error handling and response parsing notes.
5. Any model-specific constraints that apply.

