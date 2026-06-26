---
name: skill-supplier-video-ad
version: 1.0.0
description: Build polished 1080×1920 TikTok/Instagram Reels product ads from supplier or CJ Dropshipping source videos. Handles: text-free zone detection, slow-motion cuts, Montserrat Bold text overlays (Pillow-rendered, no ffmpeg drawtext), branded CTA end card, and trending TikTok audio. Use when you have raw supplier/CJ footage and need a ready-to-post short-form ad.
---

# Supplier Video Ad Builder

Turns raw supplier source footage into polished 1080×1920 TikTok/IG Reels ads.

**Pipeline:** detect clean zones → cut + slow-mo → Pillow text overlays → CTA end card → trending audio → final MP4.

## Requirements

- `ffmpeg` + `ffprobe`
- Python 3.10+: `Pillow`
- Montserrat-Bold font (or any TTF — configurable in scripts)
- Your brand logo as PNG (with transparency)
- Source video from supplier/CJ

## File Structure

```
skill-supplier-video-ad/
├── scripts/
│   ├── detect_clean_zones.py   # Step 1: extract 1fps frames for text analysis
│   └── make_product_ad.py      # Step 2: full pipeline from config JSON
├── example/
│   └── product-config.json     # Reference config template
└── SKILL.md
```

## Workflow

### Step 1 — Detect Clean Zones

Run this on each source video to extract frames for visual inspection:

```bash
python3 scripts/detect_clean_zones.py path/to/source.mp4 --output-dir ./frames
```

Then analyze the frames with an image model:
> "For each frame (f_01=t1s, f_02=t2s, ...), is there baked-in text? YES/NO"

Map YES/NO → timestamps → define `clean_zones` in your config.

### Step 2 — Create Product Config

```json
{
  "product_name": "Cool Gadget",
  "price": "29.99 USD",
  "output_name": "cool-gadget-ad-v1.mp4",
  "source_videos": {
    "main": "path/to/source.mp4"
  },
  "clean_zones": [
    { "source": "main", "ss": 2.5, "dur": 2.5, "slowmo": true,  "label": "hero-shot" },
    { "source": "main", "ss": 8.0, "dur": 2.0, "slowmo": false, "label": "lifestyle" },
    { "source": "main", "ss": 14.0,"dur": 3.0, "slowmo": false, "label": "detail" }
  ],
  "text_overlays": [
    { "lines": ["Line 1", "Line 2"],       "start": 0.5, "end": 3.5,  "fontsize": 70, "y_pct": 0.62 },
    { "lines": ["Feature Text"],           "start": 3.8, "end": 6.5,  "fontsize": 70, "y_pct": 0.62 },
    { "lines": ["SHOP NOW"],               "start": 6.8, "end": 9.5,  "fontsize": 92, "y_pct": 0.66 },
    { "lines": ["yourstore.com"],          "start": 6.8, "end": 9.5,  "fontsize": 58, "y_pct": 0.76 }
  ],
  "font_path": "/path/to/Montserrat-Bold.ttf",
  "audio": "path/to/trending-sound.mp3",
  "audio_start_offset": 2,
  "audio_volume": 0.88,
  "cta": {
    "duration": 3,
    "price": "29.99 USD",
    "line1": "Link in bio  🛒",
    "line2": "yourstore.com",
    "bg_color": [8, 8, 14],
    "logo_path": "path/to/logo.png"
  }
}
```

**Config tips:**
- `y_pct`: vertical position as fraction of frame height. `0.62` = product copy, `0.66` = CTA verb, `0.76` = URL.
- `fontsize`: 70–74 for body, 92 for "Shop Now", 58 for URL.
- Lines ≤ 20 chars each for clean wrapping.
- `slowmo: true` → 0.8× speed (PTS=1.25×). Use on hero/dark cinematic shots.
- Total duration: ~10–13s product footage + 3s CTA = 13–16s ideal ad length.

### Step 3 — Run Pipeline

```bash
python3 scripts/make_product_ad.py example/product-config.json
```

Output: `output/cool-gadget-ad-v1.mp4` — ready to post.

## Text Rendering Note

**This skill does NOT use `ffmpeg drawtext`** — it renders text as Pillow PNGs and overlays them via `overlay` filter. This avoids ffmpeg font/emoji compatibility issues and works on any Linux server.

## Output Spec

- Resolution: 1080×1920 (9:16 portrait)
- FPS: 30
- Codec: H.264 + AAC 128k
- Typical size: 8–20 MB

## Proven TikTok Sounds (March 2026)

| Track | Vibe | TikTok Videos |
|-------|------|---------------|
| "Bounce (i just wanna dance)" — фрози & joyful | Upbeat instrumental | 8M+ ✅ |
| "warm nights" — Xori | Lofi/chill lifestyle | Trending |
| "Break Me" — Blake Whiten | Cinematic product demo | Trending |

## CTA Card

The pipeline auto-generates a branded end card with:
- Your logo (PNG with alpha) centered, scaled to 400px wide
- Glowing ambient light effect behind logo
- Price in large bold type
- CTA line + URL in muted gray
- Dark background (configurable `bg_color`)
