---
name: "video-content-pipeline"
description: "Faceless video production for YouTube/TikTok/Shorts: Pixar-style images (free via Pollinations), parallax effects, voiceover (Edge TTS cloud), composer — the full pipeline from script to finished video. DISCLOSURE: scene prompts go to image.pollinations.ai, narration text goes to Microsoft Edge TTS (cloud)."
metadata: {"clawbot":{"requires":{"python3":True,"network":["https://image.pollinations.ai","https://speech.platform.bing.com"],"bins":["ffmpeg"]},"permissions":{"network":["https://image.pollinations.ai","https://speech.platform.bing.com"],"notes":"Free pipeline sends scene prompts to image.pollinations.ai and narration text to Microsoft Edge TTS (speech.platform.bing.com) — third-party cloud services. Ingen API-nøgle."}}}
---

# Video Content Pipeline 🎬✨

Production of faceless videos — from script to finished MP4, without filming.

## What you get

1. **Pixar-style images** — free via Pollinations.ai (Flux, no API key)
2. **2.5D parallax effect** — brings still images to life (PIL/ffmpeg)
3. **Voiceover** — Edge TTS (multiple languages/voices) or Piper (offline)
4. **Composer** — image + text + audio → finished MP4 (ffmpeg)
5. **Batch production** — whole folder → all videos

## Quick start

```bash
# 1) Script → scenes
python3 scripts/scene_plan.py script.txt scenes.json

# 2) Generate images (free)
python3 scripts/generate_images.py scenes.json images/

# 3) Voiceover
python3 scripts/voiceover.py scenes.json audio/

# 4) Assemble video
python3 scripts/compositor.py scenes.json images/ audio/ final.mp4
```

## Files

```
video-content-pipeline/
├── SKILL.md
└── scripts/
    ├── scene_plan.py      # split script → scenes with prompts
    ├── generate_images.py # Pollinations (Flux, free)
    ├── voiceover.py       # Edge TTS / Piper
    └── compositor.py      # ffmpeg: images + text + audio → MP4
```

## Specs (platform)

- YouTube: 1920×1080 · TikTok/Shorts: 1080×1920
- 30-60 sec per video · 3-5 sec per scene
- Voiceover: 150 words/min

## Monetization (niche ideas)

- Islamic content (the FactSage model)
- Stories/facts · DIY · motivational quotes

Generate cinematic scene prompts for your video automatically:

```bash

# 2) Generate scenes (PAID call — costs per call)
python3 scripts/scene_gen.py "Islamic history coffee culture"
```

- ⚠️ Paid call — each run charges your key. The free pipeline above remains free.
- 🔒 **PRIVACY:** your topic is sent to the external API.
---
