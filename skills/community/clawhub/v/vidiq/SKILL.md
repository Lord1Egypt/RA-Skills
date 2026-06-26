---
name: vidiq
description: "AI-powered video intelligence - download, analyze, clip, GIF from any URL. Supports YouTube, TikTok, Instagram, X. Uses ffmpeg + yt-dlp."
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      bins: ["ffmpeg", "yt-dlp"]
---

# VidIQ - Video Intelligence & Query Tool

Download, understand, and manipulate any video from a URL.

## Commands

```bash
# Video info (duration, resolution, codecs)
{baseDir}/scripts/vidiq.sh <url_or_path> info

# Extract N frames evenly spaced
{baseDir}/scripts/vidiq.sh <url_or_path> frames 10

# Single frame at timestamp
{baseDir}/scripts/vidiq.sh <url_or_path> frame 01:30:00

# Clip between timestamps
{baseDir}/scripts/vidiq.sh <url_or_path> clip 01:01:01 01:20:01 output.mp4

# Create GIF (start time, duration in seconds)
{baseDir}/scripts/vidiq.sh <url_or_path> gif 00:45:00 5

# Extract audio as MP3
{baseDir}/scripts/vidiq.sh <url_or_path> audio

# Detect scene changes
{baseDir}/scripts/vidiq.sh <url_or_path> scenes 0.3

# Visual mosaic (columns, total frames)
{baseDir}/scripts/vidiq.sh <url_or_path> mosaic 4 16
```

## AI Analysis Workflow

1. Extract frames: `vidiq.sh <url> frames 10`
2. Feed frames to vision model for content understanding
3. Answer questions about the video based on frame analysis

## Supported Platforms

YouTube, TikTok, Instagram, X/Twitter, any direct video URL, local files.

## Notes

- Downloaded videos are cached in `/tmp/vidiq/` for reuse
- Frames output to `/tmp/vidiq/frames_*/`
- For long videos, extract more frames for better coverage
- GIFs are optimized with palette generation for small file size
