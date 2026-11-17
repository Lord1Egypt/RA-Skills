# video-to-markdown

An OpenClaw / clawhub skill that analyzes YouTube, Facebook, and Instagram videos by combining AI vision analysis of extracted frames with full transcription — generating a comprehensive Markdown reference document from any video.

## The problem it solves

Standard transcription tools capture what a narrator *says*, but miss everything on screen. In trading videos, technical tutorials, and educational content, the charts, diagrams, slides, and visual demonstrations often carry as much information as the narration — sometimes more. The transcript alone leaves a significant gap.

This skill closes that gap by extracting key frames at scene-change points, pairing them with the full transcript, and using Claude's vision API to synthesize a structured Markdown document that captures everything — what was said *and* what was shown.

## What you get

A `.md` file containing:

- **Overview** — what the video is about and what you learn
- **Visual Content Summary** — everything that appeared on screen (charts, diagrams, slides, data)
- **Section Breakdown** — each major topic with both the narration and the visuals described
- **Key Visuals Explained** — detailed breakdown of every significant chart or diagram
- **Key Takeaways** — main lessons and actionable points
- **Terms & Concepts** — domain-specific terms introduced
- **Visual–Narration Gaps** — things shown on screen that weren't explained verbally

## Requirements

**System:**
- Python 3.9+
- `ffmpeg` — frame extraction
- `yt-dlp` — video and caption download

**Python packages:**
- `anthropic` — Claude API client
- `Pillow` — frame resizing
- `faster-whisper` *(optional)* — Whisper transcription fallback

**Environment:**
- `ANTHROPIC_API_KEY` must be set

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/video-to-markdown
cd video-to-markdown
bash scripts/setup.sh
export ANTHROPIC_API_KEY=your_key_here
```

## Usage

```bash
# Basic — YouTube with auto-captions
python scripts/video_analyzer.py "https://youtu.be/VIDEO_ID"

# Trading / chart-heavy — more frames, Whisper transcription
python scripts/video_analyzer.py "https://youtu.be/VIDEO_ID" \
  --max-frames 80 --whisper --output ./notes

# Facebook or Instagram (cookies required)
python scripts/video_analyzer.py "https://fb.watch/..." \
  --cookies cookies.txt --output ./notes

# Maximum quality
python scripts/video_analyzer.py "https://youtu.be/VIDEO_ID" \
  --model claude-opus-4-8 \
  --whisper --whisper-model large-v3 \
  --max-frames 80
```

## Options

| Flag | Default | Description |
|---|---|---|
| `--output` | `.` | Output directory for the Markdown file |
| `--max-frames` | `50` | Max frames to extract (lower for talking-head, higher for charts) |
| `--whisper` | off | Force Whisper transcription instead of platform captions |
| `--whisper-model` | `base` | Whisper model size (`tiny` / `base` / `small` / `medium` / `large-v3`) |
| `--cookies` | none | Path to cookies.txt (required for Facebook/Instagram) |
| `--model` | `claude-sonnet-4-6` | Claude model to use for analysis |

## Platform support

| Platform | Auth needed | Notes |
|---|---|---|
| YouTube | Usually no | Cookies needed on cloud IPs or age-restricted content |
| Instagram | Yes (cookies) | Firefox cookies; intermittent even with valid session |
| Facebook | Yes (cookies + impersonation) | Auto-handled; requires `curl_cffi` installed |

For cookie setup, see [`references/platforms.md`](references/platforms.md).

## Cost estimate (claude-sonnet-4-6)

| Video length | Frames | Approx. cost |
|---|---|---|
| 10 min | ~20 | ~$0.08 |
| 30 min | ~50 | ~$0.20 |
| 60 min | ~80 | ~$0.35 |

Switch to `claude-haiku-4-5` for ~5× lower cost.

## How it works

1. **Platform detection** — identifies YouTube, Facebook, or Instagram and selects appropriate download flags
2. **Transcript** — pulls platform captions first (fast, free); falls back to Whisper if not available
3. **Frame extraction** — uses ffmpeg scene-change detection with a 2s minimum interval guard; falls back to fixed 1-per-15s sampling if scene detection yields fewer than 5 frames; caps to `--max-frames`
4. **Frame preprocessing** — resizes to ≤1,092px long edge, JPEG q85 to stay within Claude Sonnet's vision token ceiling (~1,568 tokens/image)
5. **Claude vision** — sends all frames + transcript in a single request with a structured analysis prompt
6. **Output** — writes a timestamped `.md` file with YAML frontmatter and the full analysis

## License

MIT
