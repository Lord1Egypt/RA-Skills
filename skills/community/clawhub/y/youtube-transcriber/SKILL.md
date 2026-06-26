---
name: youtube-transcriber
description: One-command YouTube video transcription. Automatically downloads audio and transcribes using OpenAI Whisper API — works even when YouTube subtitles are disabled. Use when asked to "transcribe this video", "get transcript", "what does this video say", or when YouTube captions are unavailable.
---

# YouTube Transcriber

One-command transcription for any YouTube video — even when subtitles are disabled.

**How it works:**
1. Tries to fetch existing YouTube subtitles first (free, instant)
2. If subtitles are disabled/unavailable → downloads audio → transcribes via OpenAI Whisper API

## Prerequisites

- `yt-dlp` — `brew install yt-dlp` or `pip install yt-dlp`
- `ffmpeg` — `brew install ffmpeg`
- `OPENAI_API_KEY` environment variable set

## Usage

```bash
# Basic — auto-detect best method
{baseDir}/scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# Specify language (improves accuracy for non-English)
{baseDir}/scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID" --lang zh

# Custom output path
{baseDir}/scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID" --out /tmp/transcript.txt

# Force Whisper (skip subtitle check)
{baseDir}/scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID" --force-whisper

# Keep downloaded audio file
{baseDir}/scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID" --keep-audio
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang <code>` | Language hint (ISO 639-1: en, zh, ja, ko, etc.) | auto-detect |
| `--out <path>` | Output transcript file path | `/tmp/yt_transcript_<VIDEO_ID>.txt` |
| `--force-whisper` | Skip subtitle check, always use Whisper API | off |
| `--keep-audio` | Keep the downloaded audio file after transcription | off (deletes audio) |
| `--audio-bitrate <kbps>` | Audio compression bitrate | 64 |

## How It Works

```
YouTube URL
    │
    ├─► Try yt-dlp subtitles (free, instant)
    │       │
    │       ├─ Found → Clean & output transcript ✓
    │       │
    │       └─ Not found / disabled
    │               │
    │               ▼
    └─► Download audio (yt-dlp + ffmpeg)
            │
            ├─ Compress to mono, low bitrate (fit 25MB API limit)
            │
            ▼
        OpenAI Whisper API → transcript ✓
```

## Cost

- **With subtitles available**: Free (uses existing captions)
- **Whisper API**: ~$0.006/minute of audio → 23-min video ≈ $0.14

## Supported

- Any YouTube video URL (full URL, youtu.be short link, or video ID)
- All languages supported by Whisper (99+ languages)
- Videos up to ~4 hours (audio compressed to fit 25MB API limit)

## Troubleshooting

- **403 from YouTube**: Update yt-dlp (`pip install -U yt-dlp`)
- **File too large for Whisper**: Lower bitrate with `--audio-bitrate 32`
- **Missing API key**: Set `OPENAI_API_KEY` environment variable
