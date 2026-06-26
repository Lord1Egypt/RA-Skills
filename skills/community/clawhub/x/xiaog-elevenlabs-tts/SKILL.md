---
name: elevenlabs-tts
description: Set up, test, benchmark, and use ElevenLabs text-to-speech as an independent TTS skill, including HTTP streaming, WebSocket streaming guidance, voice listing, model/output-format selection, latency tuning, and safe ELEVENLABS_API_KEY handling.
---

# ElevenLabs TTS

Use this skill for ELE / ElevenLabs voice generation, low-latency streaming TTS, voice IDs, voice listing, output formats, or TTS benchmark work.

## Non-negotiables

- Keep this skill independent from Xiaomi MiMo TTS. Do not mix API keys, endpoint shapes, voice IDs, or scripts.
- Treat `ELEVENLABS_API_KEY` as a secret. Never echo it, write it into skill files, commit it, or expose it in logs/screenshots.
- Prefer environment variable injection for tests: `ELEVENLABS_API_KEY=... python3 ...`.
- If the key is missing, verify scripts and docs locally, then report that live API synthesis is blocked by missing credentials.

## Standard workflow

1. Verify API key availability without printing it.
2. List voices with `scripts/list_voices.py`; choose a requested voice by ID/name or use the first available voice for smoke tests.
3. Generate a short HTTP streaming sample with `scripts/tts_stream_http.py`.
4. Capture evidence: output path, bytes, chunks, `ttfb_seconds`, elapsed time, model, output format.
5. If audio validation tools exist (`ffprobe`, `afinfo`, or `file`), inspect the generated file before claiming success.

## Recommended defaults

- Model: `eleven_flash_v2_5` for lowest latency; `eleven_turbo_v2_5` for higher quality with low latency; `eleven_multilingual_v2` for broad multilingual quality.
- Endpoint: `POST /v1/text-to-speech/{voice_id}/stream` when the full text is available.
- Output: `mp3_44100_128` for shareable files; `pcm_16000`/`pcm_24000` for realtime playback pipelines.
- Latency: `optimize_streaming_latency=2` or `3`; avoid `4` unless the user accepts possible number/date mispronunciation.
- Voice settings: keep `use_speaker_boost=false` for low latency.

## Quick commands

List voices:

```bash
ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY" python3 skills/elevenlabs-tts/scripts/list_voices.py
```

HTTP streaming TTS benchmark:

```bash
ELEVENLABS_API_KEY="$ELEVENLABS_API_KEY" python3 skills/elevenlabs-tts/scripts/tts_stream_http.py \
  --text '野哥，ElevenLabs 流式语音测试成功。' \
  --voice-name Rachel \
  --model eleven_flash_v2_5 \
  --output-format mp3_44100_128 \
  --optimize-streaming-latency 2 \
  --out /tmp/elevenlabs-skill-test.mp3
```

If `--voice-name` is omitted, the script uses the first voice returned by `/v1/voices`.

## When to read more

- API contract, request/response details, WebSocket notes, and troubleshooting: `references/elevenlabs-api.md`.
- Deterministic scripts:
  - `scripts/list_voices.py`
  - `scripts/tts_stream_http.py`
