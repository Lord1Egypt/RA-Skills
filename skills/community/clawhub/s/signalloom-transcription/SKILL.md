---
name: transcription
description: Transcribe audio and video files using the Signal Loom AI API. Supports MP3, WAV, M4A, MP4, MOV, and more. Runs locally on Apple Silicon for speed and privacy.
metadata:
  openclaw:
    emoji: "🎙"
    requires:
      bins: ["transcribe"]
    install:
      - id: skill-install
        kind: skill
        label: "Transcription skill is installed — type /transcribe in any chat"
---

# Transcription — Signal Loom AI

## What It Does

Transcribes media files to structured JSON, SRT, VTT, and plain text — all in a single pass. Local processing on Apple Silicon means audio never leaves your machine.

## When to Use

- Transcribing meeting recordings, podcasts, or videos
- Converting spoken content to searchable text
- Processing audio for AI agent pipelines
- Subtitles and captions for video content

## Syntax

```
/transcribe ./meeting-recording.mp3 --format json
/transcribe ./podcast.mp4 --language en
```

## Free Tier

**100 minutes/month free** with any Signalloom API key.

Get your free key: https://signalloomai.com/signup

## Output Formats

- **JSON**: Timestamped words, confidence scores, speaker diarization
- **SRT/VTT**: Subtitles ready for video players
- **Plain text**: Clean transcript
