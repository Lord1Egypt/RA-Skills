# 🎬 Video Watcher

Download videos, extract transcripts, capture frames. Perfect for analyzing DD videos, tutorials, podcasts.

## Features

- **Download** - YouTube, Vimeo, most video sites (via yt-dlp)
- **Transcribe** - Local speech-to-text (via Whisper)
- **Frames** - Screenshot every N seconds (via ffmpeg)
- **Summarize** - AI-ready transcript for quick summaries

## Requirements

```bash
brew install yt-dlp ffmpeg openai-whisper
```

## Quick Start

```bash
./scripts/analyze.sh "https://youtube.com/watch?v=..."
```

## Output

```
outputs/
├── video.mp4           # Downloaded video
├── audio.mp3           # Extracted audio
├── transcript.txt      # Plain text transcript
├── transcript.srt      # Subtitle format
└── frames/             # Screenshots
    ├── 00_00_00.jpg    # At 0:00
    ├── 00_00_30.jpg    # At 0:30
    └── ...
```

## Configuration

`config.json`:
```json
{
  "whisper_model": "medium",
  "frame_interval": 30,
  "output_dir": "./outputs",
  "languages": ["en", "tr"]
}
```

### Whisper Models
- `tiny` - Fastest, least accurate
- `base` - Fast
- `small` - Balanced
- `medium` - Good accuracy (recommended)
- `large` - Best accuracy, slow

## Usage Examples

### Analyze a YouTube video
```bash
./scripts/analyze.sh "https://youtube.com/watch?v=xyz"
```

### Custom output directory
```bash
./scripts/analyze.sh "URL" ./my-output
```

### Different frame interval (every 60 seconds)
```bash
./scripts/analyze.sh "URL" ./output 60
```

### Use larger Whisper model
```bash
./scripts/analyze.sh "URL" ./output 30 large
```

## Summarize Transcript

After analysis:
```bash
./scripts/summarize.sh ./outputs/transcript.txt
```

Or pipe to your AI:
```bash
cat outputs/transcript.txt | clawdbot ask "Summarize this video"
```

## Use Cases

- DD (Due Diligence) video analysis
- Lecture notes extraction
- Podcast summaries
- Tutorial documentation
- Meeting recordings

## Notes

- First Whisper run downloads the model (~1.5GB for medium)
- Long videos = long transcription time
- Frame extraction is fast, transcription is slow
