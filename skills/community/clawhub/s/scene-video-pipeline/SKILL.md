---
name: scene-video-pipeline
version: 1.0.0
description: Produce modular scene-based videos from slide deck source and per-scene narration audio (text manifest + Kokoro). Includes Playwright slide rendering, per-scene clip generation, and final stitch via editable order file for easy reordering/splicing without full rerender.
metadata:
  {
    "openclaw": {
      "emoji": "🎬",
      "requires": {
        "bins": ["ffmpeg", "ffprobe", "node"],
        "env": []
      },
      "primaryEnv": "/Users/loki/.kokoro-venv/bin/python3",
      "network": {
        "outbound": true,
        "reason": "Only needed on first Kokoro run if model weights are not cached. Rendering/stitching is local."
      }
    }
  }
---

# Scene Video Pipeline

Use this skill when you need movie-style modular production:
- per-scene narration
- per-scene rendered clips
- final assembly from an order file

This allows quick cut/splice/reorder/insert changes without regenerating the whole video.

## Directory Contract

```
<module_dir>/
  slides/deck.html
  slides/01.png ...
  tts/
    manifest.csv
    audio/01.mp3 ...
  dist/
    scenes/01.mp4 ...
    scene-order.txt
    module-first-cut.mp4
```

## Commands

### 1) Render slides from deck source (Playwright)
```bash
# project helper wrapper (solana-academy)
projects/solana-academy/content-production/scripts/render-slides.sh <module_dir>
```

### 2) Generate narration audio (Kokoro local)
```bash
scripts/generate_tts_kokoro.sh <module_dir> [voice] [speed]
```

### 3) Build per-scene clips
```bash
scripts/build_scenes.sh <module_dir>
```

### 4) Stitch final from ordered scene list
```bash
scripts/stitch_scenes.sh <module_dir> [order_file]
```

## Workflow
1. Draft deck source (`slides/deck.html`) and scripts.
2. Render slide PNGs via Playwright.
3. Generate audio from manifest.
4. Build scene clips.
5. QA scene-by-scene.
6. Adjust `scene-order.txt` for narrative edits.
7. Stitch final cut.

## Notes
- Keep scene filenames zero-padded (`01.mp4`, `02.mp4`) to preserve stable sorting.
- For reorder-only edits, rerun stitch only.
- For a single content fix, rerender only the affected scene clip and restitch.

## Files
- `scripts/generate_tts_kokoro.sh`
- `scripts/build_scenes.sh`
- `scripts/stitch_scenes.sh`
