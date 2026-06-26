---
name: skill-ugc-pipeline
version: 1.2.0
description: >
  End-to-end AI UGC video pipeline. Product info → GPT-4o-mini script → ElevenLabs voiceover
  → Aurora talking head (fal-ai/creatify/aurora) → Kling 2.6 Pro product B-roll →
  Whisper-synced captions → UGC post-processing filter (grain + handheld shake on avatar,
  clean product shot) → final MP4. Full pipeline ~$1.75/video.
requires:
  env:
    - FAL_KEY
    - ELEVENLABS_API_KEY
    - OPENAI_API_KEY
  bins:
    - node
    - ffmpeg
    - uv
---

# skill-ugc-pipeline v1.2.0

Build your own MakeUGC pipeline. Direct API access — no $300/mo enterprise tier.

**Default model: Aurora** (`fal-ai/creatify/aurora`) — locked after A/B test.  
Aurora produces significantly more realistic lip sync and narration vs alternatives.

## What's new in v1.2.0
- **B-roll splicing** — Kling 2.6 Pro image-to-video generates a cinematic product shot, spliced into the avatar video at a configurable timecode
- **UGC filter** — grain + handheld shake applied to avatar segments ONLY; product B-roll stays clean and cinematic
- Continuous audio across splice points (no audio gap)

## Architecture

```
product info → [GPT-4o-mini] → script
                             → [ElevenLabs] → audio.mp3
avatar image + audio         → [fal.ai Aurora] → avatar.mp4
product image                → [Kling 2.6 Pro] → broll.mp4
avatar + broll + ugc-filter  → [ffmpeg] → final.mp4
audio.mp3                    → [OpenAI Whisper] → captions overlay
```

## Full Pipeline (6 steps)

```
1. Script       GPT-4o-mini → spoken script
2. Voice        ElevenLabs → audio.mp3
3. Avatar       fal-ai/creatify/aurora → talking head MP4
4. B-roll       Kling 2.6 Pro image-to-video → product shot
5. Splice       ffmpeg: avatar(hook) + broll + avatar(resume) + continuous audio
6. Captions     Whisper word-level → overlay.py → final MP4
7. UGC filter   grain + handheld shake on avatar ONLY (product shot stays clean)
```

## Quick Start — Full Pipeline

```bash
cd skill-ugc-pipeline
npm install

# Step 1-3: Script + voice + avatar
node scripts/generate.js \
  --product "Rain Cloud Humidifier" \
  --product-desc "USB cool mist humidifier. 300ml tank, LED glow, silent mode." \
  --avatar avatars/my_avatar.png \
  --output output/ad_raincloud.mp4

# Step 4-5: Add B-roll + UGC filter
node scripts/broll.js \
  --avatar-video output/ad_raincloud_aurora.mp4 \
  --audio output/ad_raincloud_audio.mp3 \
  --product-image https://example.com/product.jpg \
  --product-name "Rain Cloud Humidifier" \
  --splice-at 4.5 \
  --broll-duration 5 \
  --ugc-filter \
  --output output/final.mp4

# Step 6: Whisper captions
node scripts/transcribe_captions.js \
  --audio output/ad_raincloud_audio.mp3 \
  --video output/final.mp4 \
  --output output/final_captioned.mp4
```

## Scripts

| Script | Description |
|--------|-------------|
| `generate.js` | Main pipeline: script → voice → Aurora talking head |
| `broll.js` | B-roll splice + optional UGC filter (grain + shake on avatar) |
| `transcribe_captions.js` | Whisper word-level caption overlay |
| `aurora_only.js` | Generate Aurora talking head only (skip script/voice) |
| `batch.js` | Run pipeline for multiple products |
| `product_in_hand.js` | Generate product-in-hand composite image |

## broll.js Options

| Flag | Default | Description |
|------|---------|-------------|
| `--avatar-video` | required | Path to Aurora talking head MP4 |
| `--audio` | required | Original voiceover MP3 (plays continuously) |
| `--product-image` | required | URL or local path to product image |
| `--product-name` | required | Product name (used in Kling prompt) |
| `--splice-at` | `4.5` | Seconds into avatar video where B-roll inserts |
| `--broll-duration` | `5` | B-roll duration: 5 or 10 seconds |
| `--ugc-filter` | off | Add grain + handheld shake to avatar (product stays clean) |
| `--output` | required | Output MP4 path |

## Cost Estimate

| Step | Model | Cost/video |
|------|-------|-----------|
| Script | GPT-4o-mini | ~$0.01 |
| Voice | ElevenLabs | ~$0.05 |
| Avatar | Aurora (fal.ai) | ~$1.00 |
| B-roll | Kling 2.6 Pro (fal.ai) | ~$0.40 |
| Captions | Whisper API | ~$0.01 |
| **Total** | | **~$1.47–1.75** |

## Requirements

- `FAL_KEY` — fal.ai API key (Aurora + Kling)
- `ELEVENLABS_API_KEY` — ElevenLabs API key
- `OPENAI_API_KEY` — OpenAI API key (GPT-4o-mini + Whisper)
- `ffmpeg` — for video splicing and UGC filter
- `uv` — for Python caption overlay (via skill-tiktok-ads-video)

## Avatar Requirements

- Portrait photo, face visible (no heavy makeup or accessories that obscure mouth)
- Resolution: 512×512 minimum, 1024×1024 recommended
- File format: PNG or JPG
