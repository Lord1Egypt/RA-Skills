---
name: video-summarize
description: "Video summarization. Trigger: 1.User provides a video link (Bilibili/YouTube/Douyin/Twitter/TikTok etc.), 2.Summarize this video"
---

# Video Summarizer

Intelligently fetch video transcripts → Let LLM summarize the content

## Pipeline

```
Video Link → Check Cache → Try downloading subtitles → Has subtitles? → Extract text directly → Summarize
                                                     ↓ No subtitles
                                                      Download audio → Whisper transcribe → Summarize
```

## Features

- **Subtitles first**: Prefer official/manual subtitles, fall back to Whisper transcription only when unavailable
- **Multi-platform**: Bilibili, YouTube, Douyin, Twitter, TikTok and 1000+ more platforms
- **Auto language detection**: Whisper auto-detects video language (Chinese, English, Japanese, etc.)
- **Concurrency safe**: Each video uses its own temp directory, supports multiple videos simultaneously
- **Smart caching**: Same video returns cached result on subsequent requests

## Supported Platforms

Powered by yt-dlp, supports **1000+ platforms**:

| Platform | Example URL |
|----------|-------------|
| **Bilibili** | `https://www.bilibili.com/video/BVxxx` |
| **YouTube** | `https://www.youtube.com/watch?v=xxx` |
| **Douyin** | `https://www.douyin.com/video/xxx` |
| **Twitter/X** | `https://twitter.com/user/status/xxx` |
| **TikTok** | `https://www.tiktok.com/@user/video/xxx` |
| **Instagram** | `https://www.instagram.com/p/xxx` |
| **AcFun** | `https://www.acfun.cn/v/acxxx` |
| **iQiyi/Youku/Tencent** | Various Chinese video platforms |
| **Others** | Any platform supported by yt-dlp |

## Dependency Installation

The script will automatically check and install missing dependencies:
- ffmpeg (audio conversion) → `brew install ffmpeg`
- whisper.cpp (transcription) → `brew install whisper-cpp`
- Python3 (isolated virtual environment) → `brew install python3`

Run:
```bash
scripts/install_dependency.sh
```

Note: First-time installation may take a while depending on your network speed.

## Usage

```bash
# Process a video (first run transcribes, subsequent runs return cached result)
scripts/process.sh "video_url"
```

Pipeline:
1. Check cache (return immediately if exists)
2. Try downloading subtitles (prefer Chinese manual, then auto-generated)
3. Has subtitles → extract plain text; No subtitles → download audio → Whisper transcribe
4. Save to `summarize_result/{title}_transcript_raw.txt`

**Then ask me to summarize and save the result as a markdown file!**

## Input Formats

- Bilibili: `https://www.bilibili.com/video/BV1s8UZBZEa8`
- YouTube: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- Douyin: `https://www.douyin.com/video/7123456789`
- Twitter: `https://twitter.com/user/status/123456789`
- TikTok: `https://www.tiktok.com/@user/video/123456789`
- Any other yt-dlp supported URLs

## Output

Filenames use the video title for clarity, special characters handled automatically:

```
cache/{title}/
└── transcript_raw.txt          # Raw transcript

summarize_result/
└── {title}.md                    # Summary
```

**Filename sanitization:**
- Chinese punctuation `《》【】：？` → `_`
- English symbols `/\:*?"<>|` → `_`
- Spaces → `_`
- Consecutive underscores merged
- Max 50 characters

## Directory Structure

```
video-summarize/
├── cache/                   # Cache directory
│   └── {title}/             # Per-video directory
│       ├── transcript_raw.txt  # Raw transcript (preserved)
│       ├── status.json      # Processing status (cleaned up)
│       ├── subs/            # Subtitle temp dir (cleaned up)
│       ├── audio.m4a        # Audio file (cleaned up)
│       └── audio.wav        # WAV format (cleaned up)
├── summarize_result/        # Summary output directory
│   └── {title}.md           # Summary file
├── whisper-models/
│   └── ggml-base.bin
├── scripts/
│   ├── install_dependency.sh
│   ├── process.sh
│   └── safe_filename.py
└── SKILL.md
```

## Subtitle Support

| Platform | Manual Subtitles | Auto Subtitles |
|----------|-----------------|----------------|
| **YouTube** | ✅ Supported | ✅ Supported |
| **Bilibili** | ✅ Supported | ⚠️ Partial |
| **Others** | Varies | Varies |

Subtitle priority: Chinese manual > English manual > Auto-generated

## Notes

- Only processes public videos (no members-only or paid content)
- Subtitles are generally better than Whisper transcription (preferred)
- Transcription quality depends on audio quality and Whisper base model
- Long videos (>30 min) take longer to transcribe
- Works well with Chinese, English, Japanese and other major languages
- Requires network connection to download video audio/subtitles
