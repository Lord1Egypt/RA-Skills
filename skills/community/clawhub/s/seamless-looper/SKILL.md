---
name: seamless-looper
description: Create seamless looping video files with smooth crossfade transitions at the loop junction. Use when asked to loop a video, make a seamless loop, create ambient video loops, crossfade video loops, or loop background footage. Output is visual-only (no audio). Trigger phrases: "loop video", "seamless loop", "video loop", "crossfade loop", "ambient video", "background loop", "loop MP4".
---

# Seamless Looper

Create seamless looping versions of ambient/background videos with smooth crossfade transitions at the junction.

**Limitations:** Output is visual-only (no audio). Input must be MP4. Videos under 2 seconds are skipped.

## Quick Start

```bash
cd ~/.openclaw/skills/seamless-looper
bash scripts/loop.sh <source_dir> <output_dir> [crossfade_seconds]
```

**Example:**
```bash
bash scripts/loop.sh ~/Videos/ambient ~/Videos/looped 1
```

- Source dir must contain `.mp4` files
- Output dir created automatically
- Default crossfade: 1 second

## Output

Looped files saved as `<filename>_looped.mp4` in the output directory.

## How It Works

1. Takes each `.mp4` in source dir
2. Doubles the video (original + original via stream_loop)
3. Applies crossfade at the junction point (fade out tail, fade in head)
4. Outputs `<filename>_looped.mp4` — seamless loop of the original duration

## Requirements

- `ffmpeg` (with libx264 and overlay filter support)
- `ffprobe` (for duration detection)

Install on macOS: `brew install ffmpeg`

## Tips

| Use Case | Crossfade |
|----------|-----------|
| Fast cuts, high motion | 0.5s |
| Default ambient | 1s |
| Slow fades, nature footage | 2s |
| Very slow drift | 3s |

## Limitations

- Input must be `.mp4`
- Videos <2s duration are skipped
- No audio looping (visual-only output)
- Output duration = 2x input duration

## File Structure

```
seamless-looper/
├── SKILL.md           ← you are here
├── scripts/
│   └── loop.sh        ← main loop script
└── references/
    └── tips.md        ← use cases + crossfade presets
```
