---
name: roblox-clip-transformer
version: 1.0.0
description: Transform raw Roblox gameplay footage into platform-ready promotional content (TikTok, YouTube Shorts, Reels). Auto-edit with smart trimming, aspect ratio conversion, music sync, captions, and brand overlays. Use when creating game trailers, promotional clips, or social media content from Roblox recordings. Ideal for game developers, content creators, and marketing teams.
---

# Roblox Clip Transformer

Transform raw Roblox gameplay into polished, platform-ready promotional clips in minutes.

## What This Skill Does

Takes raw Roblox screen recordings and produces edited vertical/horizontal videos optimized for TikTok, YouTube Shorts, and Instagram Reels.

**Core Capabilities:**
- Aspect ratio conversion (16:9 → 9:16)
- Smart action detection and trimming
- Beat-synced transitions
- Auto-generated captions
- Brand overlay support

## Quick Start

```bash
# Basic usage - horizontal to vertical
roblox-transform input.mp4 --output output.mp4 --platform tiktok

# With captions
roblox-transform input.mp4 --output output.mp4 --platform shorts --captions

# Full trailer mode
roblox-transform input.mp4 --output output.mp4 --platform tiktok --trailer --title "My Game" --cta "Play Now!"
```

## Workflow

### 1. Analyze Footage

The skill automatically detects:
- Action moments (movement, transitions, key events)
- Dead time (menus, loading screens)
- Audio peaks (for caption timing)

```bash
python scripts/analyze-footage.py input.mp4 --output analysis.json
```

### 2. Configure Platform

Each platform has specific requirements:

| Platform | Aspect Ratio | Duration | FPS |
|----------|--------------|----------|-----|
| TikTok | 9:16 | 15-60s | 30 |
| YouTube Shorts | 9:16 | <60s | 30 |
| Instagram Reels | 9:16 | 15-90s | 30 |
| YouTube Horizontal | 16:9 | Any | 30 |

See [references/platform-specs.md](references/platform-specs.md) for full details.

### 3. Generate Output

```bash
python scripts/platform-render.py input.mp4 \
  --analysis analysis.json \
  --platform tiktok \
  --output final.mp4
```

## Features

### Smart Trimming

Automatically removes:
- Menu screens
- Loading screens
- AFK/idle moments
- Repetitive sequences

### Aspect Ratio Conversion

Converts horizontal gameplay to vertical while:
- Centering key action
- Adding blurred background fill
- Preserving important elements

### Music Sync

Beat-synchronized transitions using:
- Royalty-free tracks in `assets/music/`
- Custom audio with `--music path/to/track.mp3`

### Auto Captions

Generates timed subtitles:
- Extracts audio with Whisper
- Syncs to video timeline
- Styles for readability

```bash
python scripts/caption-sync.py input.mp4 --output captions.srt
```

### Brand Overlays

Add:
- Game logo (PNG with transparency)
- Watermark
- Call-to-action text
- Title cards

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `analyze-footage.py` | Detect action moments, remove dead time |
| `platform-render.py` | FFmpeg wrapper for platform-specific output |
| `caption-sync.py` | Whisper-based caption generation |
| `music-sync.py` | Beat detection and transition timing |

## Requirements

**System Dependencies:**
- FFmpeg (for video processing)
- Python 3.10+
- Whisper (for captions, optional)

**Python Packages:**
- ffmpeg-python
- librosa (for beat detection)
- openai-whisper (for captions)

Install with:
```bash
pip install ffmpeg-python librosa openai-whisper
```

## Examples

### Example 1: Basic Vertical Clip

```bash
roblox-transform gameplay.mp4 --output tiktok.mp4 --platform tiktok
```

### Example 2: Vertical with Captions

```bash
roblox-transform gameplay.mp4 --output shorts.mp4 --platform shorts --captions --language en
```

### Example 3: Game Trailer Mode

```bash
roblox-transform gameplay.mp4 \
  --output trailer.mp4 \
  --platform tiktok \
  --trailer \
  --title "Escape the Castle" \
  --logo assets/logo.png \
  --cta "Play Now!"
```

### Example 4: Multi-Platform Export

```bash
# Generate for all platforms
roblox-transform gameplay.mp4 --output-dir ./exports --platform all
```

## Output Structure

```
exports/
├── tiktok_916_30fps.mp4
├── shorts_916_30fps.mp4
├── reels_916_30fps.mp4
└── youtube_169_30fps.mp4
```

## Limitations

- Best results with gameplay 30+ seconds
- Caption accuracy depends on audio clarity
- Beat sync works best with music-heavy sections

## Troubleshooting

**"FFmpeg not found"**
- Install FFmpeg: `apt install ffmpeg` or `brew install ffmpeg`

**"Whisper failed"**
- Captions optional - skip with `--no-captions`
- Or install: `pip install openai-whisper`

**"Output too long"**
- Use `--max-duration 60` to limit length
- Smart trim will prioritize best moments

## Next Steps

1. Place raw gameplay in your working directory
2. Run basic transformation: `roblox-transform input.mp4 -o output.mp4 -p tiktok`
3. Review output and adjust settings
4. Add brand elements for polished trailer

For advanced usage, see [references/brand-templates.md](references/brand-templates.md).