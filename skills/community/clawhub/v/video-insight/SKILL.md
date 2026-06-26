---
name: video-insight
description: Cross-platform video transcript extraction and optional AI summarization for YouTube and Bilibili. GPU auto-detect. Transcript-first with opt-in LLM summary.
---

# video-insight

Cross-platform video transcript extraction and optional AI summarization for YouTube and Bilibili.

## Description

Extract transcripts, metadata, and optional keyframes from YouTube and Bilibili videos. Outputs structured JSON to stdout. By default, **no LLM summarization** is performed — the agent receives the full transcript and does its own summarization with full context window.

Supports: macOS, Linux, WSL, Windows VM.

## Usage

```bash
# Single video — transcript only (default, recommended)
video-insight --url "https://www.youtube.com/watch?v=VIDEO_ID"

# Bilibili video
video-insight --url "https://www.bilibili.com/video/BV1xxxxx"

# With LLM summary (opt-in)
video-insight --url "https://..." --summarize

# Channel scan (recent videos)
video-insight --channel "UC_x5XG1OV2P6uZZ5FSM9Ttw" --hours 24

# Quiet mode (no stderr progress)
video-insight --url "https://..." --quiet

# Force refresh (ignore cache)
video-insight --url "https://..." --no-cache

# Extract keyframes too
video-insight --url "https://..." --frames
```

## Triggers

Summarize video, extract transcript, YouTube summary, Bilibili transcript, video transcript, 视频摘要, 视频总结, B站视频, YouTube视频

## Output Schema

```json
{
  "ok": true,
  "data": {
    "video_id": "dQw4w9WgXcQ",
    "platform": "youtube",
    "title": "Video Title",
    "channel": "Channel Name",
    "duration_seconds": 212,
    "transcript": "Full transcript text without truncation...",
    "transcript_with_timestamps": "[0.0-3.2] First segment\n[3.2-6.5] Second...",
    "frames": [{"file": "/tmp/.../frame_001.jpg", "time_sec": 30}],
    "cached": false
  },
  "error": null
}
```

## Cache

Transcripts are permanently cached at `~/.cache/video-insight/{platform}_{video_id}.json`. The `.json` format stores metadata + transcript together for richer cache hits (title, channel, duration, timestamps). Use `--no-cache` to force re-fetch.

## Agent Integration Guide

1. **Default workflow**: Call `video-insight --url <URL>`, receive JSON with full transcript. Use your own LLM context to summarize — you have 128K+ tokens, no need for the script to truncate.

2. **For keyframes**: Add `--frames` flag. Only needed when the user explicitly asks for a visual/image review.

3. **Long videos (2h+)**: The transcript may be very large. Use map-reduce or chunked summarization.

4. **Bilibili videos** require `ffmpeg` and `faster-whisper` (installed via `setup.sh`). YouTube videos typically have captions and are much faster.

5. **Cron/headless**: Use `--summarize --quiet` for automated pipelines.

## Setup

```bash
cd ~/.openclaw/skills/video-insight && bash setup.sh
```

## Dependencies

**Required**: `yt-dlp`, `youtube-transcript-api`, `innertube`, `ffmpeg` (system)
**Optional**: `faster-whisper` (for Bilibili/captionless videos), `requests` (for --summarize)
