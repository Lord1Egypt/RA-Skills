# YouTube Transcriber

One-command YouTube video transcription for [Claude Code](https://claude.com/claude-code). Works even when YouTube subtitles are disabled.

## How It Works

1. **Fast path**: Tries to fetch existing YouTube subtitles (free, instant)
2. **Fallback**: Downloads audio → compresses → transcribes via OpenAI Whisper API

```
YouTube URL → [subtitles available?] → YES → clean transcript ✓
                                     → NO  → download audio → Whisper API → transcript ✓
```

## Install

```bash
npx clawhub install youtube-transcriber
```

Or install directly from GitHub:

```bash
# Clone to your Claude Code skills directory
git clone https://github.com/EdisonChenAI/youtube-transcriber.git ~/.claude/skills/youtube-transcriber
```

## Prerequisites

- **yt-dlp**: `brew install yt-dlp` or `pip install yt-dlp`
- **ffmpeg**: `brew install ffmpeg`
- **OPENAI_API_KEY**: Required only when subtitles are unavailable

## Usage

```bash
# Basic usage
./scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# Chinese video
./scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID" --lang zh

# Custom output path
./scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID" --out ./transcript.txt

# Force Whisper API (skip subtitle check)
./scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID" --force-whisper

# Keep the downloaded audio file
./scripts/transcribe.sh "https://www.youtube.com/watch?v=VIDEO_ID" --keep-audio
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lang <code>` | Language hint (en, zh, ja, ko, etc.) | auto-detect |
| `--out <path>` | Output transcript file path | `/tmp/yt_transcript_<ID>.txt` |
| `--force-whisper` | Always use Whisper API | off |
| `--keep-audio` | Keep downloaded audio | off |
| `--audio-bitrate <kbps>` | Compression bitrate | 64 |

## Cost

| Method | Cost | Speed |
|--------|------|-------|
| Subtitles available | Free | Instant |
| Whisper API | ~$0.006/min | ~30s for 20min video |

A typical 20-minute video costs about **$0.12** via Whisper API.

## Why This Exists

YouTube lets creators disable subtitles/captions. When that happens, tools that rely on YouTube's transcript API simply fail. This skill solves that by downloading the audio and running it through OpenAI's Whisper speech-to-text model.

Built with [Claude Code](https://claude.com/claude-code) via vibe coding.

## License

MIT
