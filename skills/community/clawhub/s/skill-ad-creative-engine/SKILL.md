---
name: skill-ad-creative-engine
version: 1.0.0
description: >
  Generate polished 1080×1920 TikTok/Reels/Shorts video ads from product clips and images.
  Three viral styles: Clean, Meme, UGC. Python + ffmpeg, no cloud required.
requires:
  bins:
    - python3
    - ffmpeg
  pip:
    - moviepy
    - pillow
    - librosa (optional, for beat_sync)
---

# skill-ad-creative-engine v1.0.0

Render polished short-form video ads (TikTok / Reels / Shorts) from product clips and images.  
Three viral styles built-in: Clean, Meme, UGC. Runs locally — no cloud API required.

## Quick Start

```bash
cd skill-ad-creative-engine
pip3 install -r requirements.txt

python3 scripts/render.py --config examples/config_example.json
```

## Styles

| Style | Font | Overlay | Best for |
|---|---|---|---|
| `clean` | Montserrat ExtraBold | White text, drop shadow, upper-center | Product launch, brand ads |
| `meme` | Anton (ALL CAPS) | White + 8px black stroke, top-center | Viral hooks, humor ads |
| `ugc` | — | TikTok username pill only (no hook text) | Authentic creator-style |

## Config Format

```json
{
  "style": "clean",
  "hook_text": "You need this →",
  "username": "@yourstore",
  "scenes": [
    { "path": "clips/product_clip.mp4", "duration": 3.0 },
    { "path": "images/product_hero.jpg", "duration": 2.5 }
  ],
  "transitions": ["cut", "dissolve"],
  "music": "luts/background_track.mp3",
  "beat_sync": false,
  "output": "output/ad_final.mp4"
}
```

See `examples/config_example.json` for full reference.

## Dependencies

```bash
pip3 install -r requirements.txt
```

System requirements:
- `ffmpeg` (install via `brew install ffmpeg` or `apt install ffmpeg`)
- Fonts bundled: `fonts/Anton-Regular.ttf` + `fonts/Montserrat-ExtraBold.ttf`

## Output Spec

- Resolution: 1080×1920 (9:16 vertical)
- FPS: 30
- Codec: H.264 + AAC audio
- Color grade: Warm tone applied automatically

## Beat Sync (optional)

Set `"beat_sync": true` in config + provide a music track. Requires `librosa`:

```bash
pip3 install librosa
```

Cuts will snap to detected beat timestamps for a professional music-video feel.
