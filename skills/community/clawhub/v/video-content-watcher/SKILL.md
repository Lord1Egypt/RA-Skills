---
name: video-content-watcher
description: Extract core content and generate structured analysis reports from YouTube, Bilibili, or local video files. Triggers when user asks to summarize, analyze, extract key points from a video, or assess video value. Supports Chinese/English video content analysis with MiniMax LLM.
---

# Video Content Watcher

Extract audio → transcribe → analyze → generate structured Markdown report.

## Quick Start

```bash
cd /home/ykl/.openclaw/workspace-code-dev/video-reader
export MINIMAX_API_KEY="your-key"
export WHISPER_MODE="local"   # or "api"
python3 << 'EOF'
import sys; sys.path.insert(0, 'src')
from video_reader_mcp import VideoReaderMCP
mcp = VideoReaderMCP()
result = mcp.process_url('VIDEO_URL')
print(result['report'])
EOF
```

Or use the CLI script:
```bash
python3 /home/ykl/.openclaw/workspace/skills/video-content-watcher/scripts/video_reader.py "VIDEO_URL"
```

## Workflow

1. **Audio extraction**: Uses `yt-dlp` for online videos / `ffmpeg` for local files
2. **Transcription**: Whisper (local `openai-whisper` or API mode)
3. **Analysis**: MiniMax LLM analyzes transcript → structured report

## Configuration (env vars)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `MINIMAX_API_KEY` | Yes | — | MiniMax API key |
| `WHISPER_MODE` | No | `api` | `api` or `local` |
| `WHISPER_API_KEY` | If mode=api | — | OpenAI API key for Whisper |
| `LLM_BASE_URL` | No | `https://api.minimaxi.com/v1` | MiniMax endpoint |
| `LLM_MODEL` | No | `MiniMax-M2.7` | Model name |

## Supported Sources

- **YouTube**: `https://www.youtube.com/watch?v=xxx`
- **Bilibili**: `https://www.bilibili.com/video/BVxxx`
- **Local files**: `/path/to/video.mp4`

## Output

Returns a Markdown report with:
- Basic info (source, transcript length)
- Core content summary
- Key takeaways
- Main viewpoints
- Pros / cons
- Target audience

## Scripts

- `scripts/video_reader.py` — CLI entry point
- `scripts/analyze_text.py` — Analyze raw text directly (skip video processing)
