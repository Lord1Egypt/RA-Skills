---
name: youtube-transcribe
description: "Transcribe YouTube videos with smart fallback: extracts captions first (fast, free), falls back to local Whisper transcription when no captions available. Auto-detects best Whisper backend (MLX/faster-whisper/openai-whisper) and model size based on hardware. Use when the user shares a YouTube link and wants to know what it says, get a transcript, summarize, or analyze video content. Keywords: YouTube, transcribe, transcript, subtitles, captions, speech-to-text, whisper, mlx, video to text."
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires":
          {
            "bins": ["python3", "yt-dlp"],
            "optionalBins": ["ffmpeg", "mlx_whisper"],
          },
        "install":
          [
            {
              "id": "yt-dlp",
              "kind": "brew",
              "formula": "yt-dlp",
              "bins": ["yt-dlp"],
              "label": "Install yt-dlp (brew)",
            },
            {
              "id": "ffmpeg",
              "kind": "brew",
              "formula": "ffmpeg",
              "bins": ["ffmpeg"],
              "label": "Install ffmpeg (brew)",
            },
          ],
      },
  }
---

# YouTube Transcribe

Smart YouTube video transcription with automatic fallback:
1. **Captions first** — extracts existing subtitles (manual or auto-generated) via yt-dlp. Fast, free, no compute.
2. **Whisper fallback** — when no captions exist, downloads audio and transcribes locally with the best available Whisper backend.

## When to Use

Use this skill when the user wants to:
- Get a transcript or text version of a YouTube video
- Understand what a YouTube video says without watching it
- Summarize, analyze, or take notes from a YouTube video
- Extract subtitles or captions from a video

## Triggers

- "transcribe this YouTube video"
- "what does this video say"
- "get the transcript of [YouTube URL]"
- "summarize this YouTube video" *(transcribe first, then process)*
- Any YouTube URL shared with a request to understand its content

## Requirements

**Required:**
- `yt-dlp` — for caption extraction and audio download
- `python3`

**For Whisper fallback (when no captions available):**
- `ffmpeg` — for audio processing
- One of these Whisper backends (auto-detected in priority order):
  1. `mlx-whisper` — Apple Silicon native, fastest on Mac (pip install mlx-whisper)
  2. `faster-whisper` — CTranslate2 backend, fast on CUDA/CPU (pip install faster-whisper)
  3. `openai-whisper` — Original Whisper, universal fallback (pip install openai-whisper)

## Usage

### Basic — transcribe a video

```bash
python3 {baseDir}/scripts/transcribe.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Specify language for captions

```bash
python3 {baseDir}/scripts/transcribe.py "URL" --language zh
```

### Force Whisper (skip caption check)

```bash
python3 {baseDir}/scripts/transcribe.py "URL" --force-whisper
```

### JSON output

```bash
python3 {baseDir}/scripts/transcribe.py "URL" --format json
```

### Save to file

```bash
python3 {baseDir}/scripts/transcribe.py "URL" --output transcript.txt
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--language` | auto | Preferred subtitle/transcription language (e.g. `zh`, `en`, `ja`) |
| `--format` | `text` | Output format: `text`, `json`, `srt`, `vtt` |
| `--output` | stdout | Save transcript to file |
| `--force-whisper` | false | Skip caption extraction, go straight to Whisper |
| `--backend` | auto | Whisper backend: `auto`, `mlx`, `faster-whisper`, `whisper` |
| `--model` | auto | Whisper model size: `auto`, `large-v3`, `medium`, `small`, `base`, `tiny` |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `YT_WHISPER_BACKEND` | Override Whisper backend selection |
| `YT_WHISPER_MODEL` | Override Whisper model size |

## Auto-Detection

### Whisper Backend (priority order)
1. **MLX Whisper** — detected via `import mlx_whisper`. Best for Apple Silicon.
2. **faster-whisper** — detected via `import faster_whisper`. Best for CUDA GPU, good on CPU.
3. **OpenAI Whisper** — detected via `import whisper`. Universal fallback.

### Model Size (based on available RAM)
| RAM | Model | VRAM/RAM Usage |
|-----|-------|----------------|
| ≥16GB | `large-v3` | ~6-10GB |
| ≥8GB | `medium` | ~5GB |
| ≥4GB | `small` | ~2.5GB |
| <4GB | `base` | ~1.5GB |

## Caption Language Priority

When `--language` is not specified, captions are searched in this order:
1. Video's original language
2. Chinese variants: `zh-Hant`, `zh-Hans`, `zh-TW`, `zh-CN`, `zh`
3. English: `en`
4. Any available language

## Output Formats

### text (default)
Plain text transcript, one continuous block.

### json
```json
{
  "video_id": "ZSnYlbIYpjs",
  "title": "Video Title",
  "channel": "Channel Name",
  "duration": 708,
  "language": "zh",
  "method": "captions",
  "transcript": [
    {"start": 0.0, "end": 5.2, "text": "..."},
    ...
  ],
  "full_text": "Complete transcript as single string"
}
```

### srt / vtt
Standard subtitle formats with timestamps.
