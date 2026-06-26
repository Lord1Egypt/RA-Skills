---
name: volcengine-stt
description: Transcribe audio to text using Volcano Engine (Volcengine/ARK) speech-to-text APIs. Use when the user wants to replace Whisper/OpenAI STT with Volcengine, transcribe Telegram/Discord voice notes via Volcengine, or build a reusable STT skill for other OpenClaw agents.
---

# Volcengine STT

Use this skill to run speech-to-text through Volcengine.

## Quick start

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg
```

Default behavior:
- Endpoint: `${ARK_BASE_URL:-https://ark.cn-beijing.volces.com/api/v3}/audio/transcriptions`
- Model: `${ARK_STT_MODEL:-doubao-seed-asr-1-0}`
- Auth header: `Authorization: Bearer $ARK_API_KEY`
- Output file: `<input>.txt`

## Required env

- `ARK_API_KEY` (required)

Optional:
- `ARK_BASE_URL` (default: `https://ark.cn-beijing.volces.com/api/v3`)
- `ARK_STT_MODEL` (default: `doubao-seed-asr-1-0`)

## Useful flags

```bash
# Save plain text to custom path
{baseDir}/scripts/transcribe.sh ./voice.ogg --out /tmp/voice.txt

# Force model
{baseDir}/scripts/transcribe.sh ./voice.ogg --model doubao-seed-asr-1-0

# Return raw JSON (for debugging/integration)
{baseDir}/scripts/transcribe.sh ./voice.ogg --json --out /tmp/voice.json

# Hint language/prompt when needed
{baseDir}/scripts/transcribe.sh ./voice.ogg --language zh --prompt "中英混合，保留术语"
```

## Integration notes

- For OpenClaw voice-message handling, call this script instead of Whisper script.
- Keep keys in machine-local config or env, never commit secrets.
- If your Volcengine account uses a different model name, pass `--model` or set `ARK_STT_MODEL`.
