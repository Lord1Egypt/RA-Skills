---
name: wechat-voice
description: 专为微信 clawbot 设计的微信语音解析技能 / WeChat voice parsing skill for clawbot. 识别微信 SILK 语音，解码为 WAV，并用本地 Whisper 转写后回复。适用于微信语音、语音转文字、语音附件解析、‘这段语音说了什么’等场景。
---

# WeChat Voice

专为微信 clawbot 设计的微信语音解析技能。识别微信 SILK 语音、解码为 WAV、转写为文字，并基于语音内容回复。

## What this skill does

- Inspect an inbound audio attachment.
- Detect whether it is WeChat SILK (`#!SILK_V3`).
- Decode SILK audio to WAV with Python.
- Transcribe WAV locally with CPU-based Whisper.
- Return a transcript or explicitly report that the clip is blank / too short / unclear.
- Use the transcript as the basis for the user-facing reply.

## Use this workflow

1. Get the local file path for the inbound audio attachment from the current conversation context.
2. Inspect the first bytes of the file before assuming its format.
3. If the file header contains `#!SILK_V3`, treat it as WeChat SILK.
4. Run the bundled script `scripts/transcribe_wechat_voice.py` on the attachment.
5. If the script returns text, answer based on the transcript.
6. If the script returns `NO_SEGMENTS`, tell the user the clip appears blank, too short, too quiet, or unclear.
7. If decoding fails, report the failure and mention whether the issue is format detection, decode failure, or transcription failure.

## Primary command

```bash
python3 /root/.openclaw/workspace/skills/wechat-voice/scripts/transcribe_wechat_voice.py <audio_path>
```

Optional WAV output path:

```bash
python3 /root/.openclaw/workspace/skills/wechat-voice/scripts/transcribe_wechat_voice.py <audio_path> /tmp/wechat-voice.wav
```

## Installation / environment notes

This skill is text-only and ClawHub-friendly, but it expects common local runtimes and Python packages to be available.

### Required runtimes

- `python3`
- `ffmpeg`

### Python packages needed

Install locally with:

```bash
python3 -m pip install --user silk-python faster-whisper
```

Use `silk-python` to decode WeChat SILK audio in Python.
Use `faster-whisper` for local CPU transcription.
Prefer `faster-whisper` over `openai-whisper` in this environment because it avoids a heavy PyTorch/CUDA installation chain and works well on CPU.

## Output expectations

The script prints exactly one of these:

- The recognized text
- `NO_SEGMENTS` if no usable speech is detected

Treat `NO_SEGMENTS` as a valid outcome, not as a crash.

## Good user-facing behavior

- Be brief.
- If transcript succeeds, respond to the content instead of over-explaining the pipeline.
- If the clip is blank, say so plainly.
- If the clip is unclear, ask for a clearer re-recording.
- Only mention technical details when the user asks or when debugging is needed.

## When debugging is needed

Check these in order:

1. Does the file exist and have non-zero size?
2. Do the first bytes include `#!SILK_V3`?
3. Did WAV decode succeed?
4. Did transcription return `NO_SEGMENTS`?
5. Is the clip too short or silent?

For byte inspection, use a quick Python snippet such as:

```bash
python3 - <<'PY'
from pathlib import Path
p = Path('/path/to/audio')
b = p.read_bytes()[:64]
print('size=', p.stat().st_size)
print('hex=', b.hex())
print('ascii=', ''.join(chr(x) if 32 <= x < 127 else '.' for x in b))
PY
```

## Bundled files

- `scripts/transcribe_wechat_voice.py`: Decode/transcribe entry point.
- `references/notes.md`: Environment-specific notes and maintenance hints.
