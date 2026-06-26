---
name: reel-digest
description: Download, transcribe, extract frames, and deeply analyze any video or reel from URL (Instagram, YouTube, TikTok, X, direct MP4). Use when user shares a video/reel URL and wants to understand its content, strategy, script, visual elements, or marketing breakdown. Triggers on "analyze this reel", "digest this video", "what's in this video", "break down this clip", or when any video URL is shared with intent to analyze. NOT for downloading videos to watch — only for AI-powered content analysis.
---

# Reel Digest — Full Video Analysis Pipeline

## Quick Start

Give this skill a video URL. It will download, extract frames, transcribe audio, and deliver a complete analysis.

## Step 1: Download & Extract

Run the bash pipeline script (handles Instagram embed extraction, frame extraction, audio, and transcription):

```bash
bash scripts/ig-reel-dl.sh "<URL>" /tmp/reel-digest
```

This produces:
- `video.mp4` — original video
- `audio.wav` — extracted audio (16kHz mono)
- `transcript.txt` — Whisper transcription with timestamps
- `frames/` — key frames (1 per 5 seconds, 640px wide)

For non-Instagram URLs (YouTube, TikTok, etc.), use the Python script:

```bash
python3 scripts/reel-digest.py "<URL>" -o /tmp/reel-digest -f 10
```

## Step 2: Analyze Frames

1. Read `transcript.txt` for the spoken content
2. Copy frames from `/tmp` to workspace directory (required for image tool)
3. Analyze 4-8 key frames using the `image` tool
4. Describe: on-screen text, UI, products, branding, visual style, transitions

## Step 3: Synthesize

Combine transcript + frame analysis into a structured digest:

1. **Hook** — Opening 3 seconds: what grabs attention?
2. **Narrative Arc** — Frame-by-frame story
3. **Key Messages** — Main points communicated
4. **Visual Strategy** — Production quality, text overlays, aesthetic
5. **Engagement Tactics** — What makes this shareable?
6. **Business Intel** — Products, CTAs, pricing, competitive signals
7. **Viral Mechanics** — Why this works for the algorithm

## Step 4: Deliver

Present in clean, scannable format. Quote exact transcript text, describe exact visual elements. No generic advice.

## Requirements

- `curl` — HTTP requests
- `ffmpeg` / `ffprobe` — video processing
- `yt-dlp` — YouTube/TikTok downloads
- `faster-whisper` (Python) — audio transcription

## Troubleshooting

- **Instagram 403**: CDN URLs expire fast. The bash script handles this with single-session extraction via `tr -d '\\'` on embed HTML
- **Vision model timeout**: Resize frames to 360px: `ffmpeg -i frame.jpg -vf scale=360:-1 small.jpg`
- **Image tool path error**: Files must be under workspace directory, not `/tmp`. Copy first.
- **Whisper OOM**: Use `--no-transcript` flag, analyze frames only
- **No audio track**: Some clips are visual-only. Use `--no-audio` flag.
