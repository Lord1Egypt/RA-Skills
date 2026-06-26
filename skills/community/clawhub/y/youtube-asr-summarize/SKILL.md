---
name: youtube-asr-summarize
description: "Summarize YouTube videos with NO subtitles by doing local ASR (yt-dlp + faster-whisper) and extracting a few screenshot frames via ffmpeg. Use when the user asks to summarize the latest video from a channel and YouTube timedtext/subtitles are empty, or when no API tokens/keys should be used."
---

# YouTube ASR Summarize (local, no tokens)

Use this skill to summarize a YouTube video *even when subtitles are missing* by downloading audio and running local speech-to-text.

## Quick start

1) One-time deps

```bash
brew install yt-dlp ffmpeg
```

2) Create venv + install ASR

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install faster-whisper
```

3) Run

```bash
python3 scripts/youtube_asr_summarize.py \
  --url "https://www.youtube.com/watch?v=<id>" \
  --out "/tmp/youtube-asr/<id>" \
  --model small \
  --lang zh \
  --frames 1 \
  --timeline-every 180
```

Outputs in `--out`:
- `summary.md`（含：链接 + 摘要 + 时间轴）
- `transcript.txt`
- `transcript.srt`
- `frames/frame_01.jpg` … (if `--frames > 0`)

## Notes

- Default model `small` (CPU/int8) is fast; use `--model medium` for better accuracy.
- If you need more control, see `references/workflow.md`.
