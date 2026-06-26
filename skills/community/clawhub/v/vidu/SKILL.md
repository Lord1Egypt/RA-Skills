---
name: vidu
description: "Generate AI videos using Vidu — featuring text-to-video, image-to-video, reference-to-video, and start-end-to-video with up to 1080p resolution, anime style support, audio/BGM generation, and movement amplitude control. Supports Vidu Q3-Pro (latest) and Vidu 2.0 across 6 model variants. Available via Atlas Cloud API at up to 15% off standard pricing. Use this skill whenever the user wants to generate AI videos, create video clips, animate images, produce short films, make video content, or mentions Vidu, Shengshu AI, or video generation. Also trigger when users ask to create product demos, marketing videos, social media reels, animated scenes, cinematic clips, anime videos, start-end frame interpolation, character-consistent videos, or any video content using AI."
source: "https://github.com/AtlasCloudAI/nano-banana-2-skill"
homepage: "https://github.com/AtlasCloudAI/nano-banana-2-skill"
metadata:
  openclaw:
    requires:
      env:
        - ATLASCLOUD_API_KEY
    primaryEnv: ATLASCLOUD_API_KEY
---

# Vidu — AI Video Generation by Shengshu AI

Generate AI videos using Vidu Q3-Pro and Vidu 2.0 — featuring text-to-video, image-to-video, reference-based generation, and start-end frame interpolation with up to 1080p resolution, anime style support, and synchronized audio generation.

Vidu Q3-Pro is the latest flagship model with cinematic motion quality, smooth animation, optional audio/BGM generation, and multiple style modes (general/anime). Vidu 2.0 adds specialized capabilities including reference-to-video (character-consistent generation) and start-end-to-video (keyframe interpolation).

> **Data usage note**: This skill sends text prompts, image URLs, and video data to the Atlas Cloud API (`api.atlascloud.ai`) for video generation. No data is stored locally beyond the downloaded output files. API usage incurs charges per second based on the model selected.

---

## Key Capabilities

- **Text-to-Video** — Generate video clips from text descriptions with audio (Q3-Pro)
- **Image-to-Video** — Animate still images into dynamic video (Q3-Pro / 2.0)
- **Reference-to-Video** — Generate videos with character/prop consistency from 1-3 reference images (2.0 / Q1)
- **Start-End-to-Video** — Interpolate between two keyframes to create smooth transitions (2.0)
- **Audio & BGM** — Optional synchronized sound effects and background music (Q3-Pro)
- **Anime Style** — Native anime style support (Q3-Pro)
- **Movement Control** — Adjustable movement amplitude: auto, small, medium, large
- **Up to 1080p** — Resolutions: 540p, 720p, 1080p (Q3-Pro)
- **Multiple Aspect Ratios** — 16:9, 9:16, 1:1, 4:3, 3:4 (Q3-Pro)

---

## Setup

1. Sign up at https://www.atlascloud.ai
2. Console → API Keys → Create new key
3. Set env: `export ATLASCLOUD_API_KEY="your-key"`

The API key is tied to your Atlas Cloud account and its pay-as-you-go balance. All usage is billed to this account. Atlas Cloud does not currently support scoped keys — the key grants access to all models available on your account.

---

## Script Usage

This skill includes a Python script for video generation. Zero external dependencies required.

### List available video models

```bash
python scripts/generate_video.py list-models
```

### Generate a video (text-to-video)

```bash
python scripts/generate_video.py generate \
  --model "MODEL_ID" \
  --prompt "Your prompt here" \
  --output ./output \
  duration=5 resolution=720p
```

### Generate a video (image-to-video)

```bash
python scripts/generate_video.py generate \
  --model "MODEL_ID" \
  --image "https://example.com/photo.jpg" \
  --prompt "Animate this scene" \
  --output ./output
```

### Upload a local file

```bash
python scripts/generate_video.py upload ./local-file.jpg
```

Run `python scripts/generate_video.py generate --help` for all options. Extra model params can be passed as key=value (e.g. `duration=10 shot_type=multi_camera`).

---

## Pricing

### Vidu Q3-Pro (per second, by resolution)

All prices are per second of video generated. Atlas Cloud pricing varies by resolution.

| Resolution | fal.ai | Atlas Cloud | Savings |
|:----------:|:------:|:-----------:|:-------:|
| **540p** | $0.07/s | **$0.06/s** | 14% off |
| **720p** | $0.154/s | **$0.15/s** | 3% off |
| **1080p** | $0.154/s | **$0.16/s** | - |

Applies to both `vidu/q3-pro/text-to-video` and `vidu/q3-pro/image-to-video`.

### Vidu 2.0 / Q1 (per video)

| Model | Atlas Cloud | Type |
|-------|:-----------:|------|
| `vidu/image-to-video-2.0` | **$0.075/video** | Image-to-Video |
| `vidu/start-end-to-video-2.0` | **$0.075/video** | Start-End Interpolation |
| `vidu/reference-to-video-2.0` | **$0.2/video** | Reference-to-Video (character consistent) |
| `vidu/reference-to-video-q1` | **$0.4/video** | Reference-to-Video Q1 (highest quality) |

> fal.ai pricing sourced from [fal.ai/models/fal-ai/vidu/q3-pro/text-to-video](https://fal.ai/models/fal-ai/vidu/q3-pro/text-to-video).

---

## Parameters

### Vidu Q3-Pro — Text-to-Video

| Parameter | Type | Required | Default | Options |
|-----------|------|----------|---------|---------|
| `prompt` | string | Yes | - | Video description (max 1500 chars) |
| `style` | string | No | general | general, anime |
| `resolution` | string | No | 720p | 540p, 720p, 1080p |
| `duration` | number | No | 5 | Duration in seconds |
| `aspect_ratio` | string | No | 4:3 | 16:9, 9:16, 4:3, 3:4, 1:1 |
| `movement_amplitude` | string | No | auto | auto, small, medium, large |
| `generate_audio` | boolean | No | true | Generate synchronized audio |
| `bgm` | boolean | No | true | Generate background music |
| `seed` | integer | No | random | For reproducible results (-1 for random) |

### Vidu Q3-Pro — Image-to-Video

Same as Q3-Pro text-to-video (without `style` and `aspect_ratio`), plus:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `image` | string | Yes | URL of the source image |

### Vidu 2.0 — Image-to-Video

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Video description (max 1500 chars) |
| `image` | string | Yes | - | Start frame image URL (PNG/JPEG/WebP, max 50MB, ratio < 4:1) |
| `duration` | integer | No | 4 | 4 or 8 seconds |
| `movement_amplitude` | string | No | auto | auto, small, medium, large |
| `seed` | integer | No | 0 | For reproducible results |

### Vidu 2.0 — Start-End-to-Video

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Video description (max 1500 chars) |
| `images` | array | Yes | - | Exactly 2 images: [start_frame, end_frame] (similar pixel density, ratio 0.8-1.25) |
| `duration` | integer | No | 4 | 4 or 8 seconds |
| `movement_amplitude` | string | No | auto | auto, small, medium, large |
| `seed` | integer | No | 0 | For reproducible results |

### Vidu 2.0 / Q1 — Reference-to-Video

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | Video description (max 1500 chars) |
| `images` | array | Yes | - | 1-3 reference images (PNG/JPEG/WebP, min 128×128, max 50MB) |
| `aspect_ratio` | string | No | 16:9 | 16:9, 9:16, 1:1 |
| `movement_amplitude` | string | No | auto | auto, small, medium, large |
| `seed` | integer | No | 0 | For reproducible results |

---

## Workflow: Submit → Poll → Download

### Text-to-Video Example (Q3-Pro)

```bash
# Step 1: Submit
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vidu/q3-pro/text-to-video",
    "prompt": "A samurai walks through a bamboo forest at dawn, mist rising from the ground, cinematic lighting",
    "style": "general",
    "resolution": "1080p",
    "duration": 5,
    "aspect_ratio": "16:9",
    "movement_amplitude": "medium",
    "generate_audio": true,
    "bgm": true
  }'
# Returns: { "code": 200, "data": { "id": "prediction-id" } }

# Step 2: Poll (every 5 seconds until completed)
curl -s "https://api.atlascloud.ai/api/v1/model/prediction/{prediction-id}" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY"
# Returns: { "code": 200, "data": { "status": "completed", "outputs": ["https://...video-url..."] } }

# Step 3: Download
curl -o output.mp4 "VIDEO_URL_FROM_OUTPUTS"
```

### Image-to-Video Example (Q3-Pro)

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vidu/q3-pro/image-to-video",
    "image": "https://example.com/landscape.jpg",
    "prompt": "The camera slowly zooms in as clouds drift across the sky and leaves rustle in the wind",
    "resolution": "720p",
    "duration": 5,
    "movement_amplitude": "small",
    "generate_audio": true
  }'
```

### Anime Style Example (Q3-Pro)

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vidu/q3-pro/text-to-video",
    "prompt": "An anime girl with flowing hair runs through a cherry blossom garden, petals swirling around her",
    "style": "anime",
    "resolution": "1080p",
    "duration": 5,
    "aspect_ratio": "16:9"
  }'
```

### Start-End Interpolation Example (2.0)

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vidu/start-end-to-video-2.0",
    "images": ["https://example.com/start-frame.jpg", "https://example.com/end-frame.jpg"],
    "prompt": "Iron Man transforms into a sports car with smooth morphing animation",
    "duration": 4,
    "movement_amplitude": "large"
  }'
```

### Reference-to-Video Example (2.0)

```bash
curl -s -X POST "https://api.atlascloud.ai/api/v1/model/generateVideo" \
  -H "Authorization: Bearer $ATLASCLOUD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vidu/reference-to-video-2.0",
    "images": ["https://example.com/character-ref1.jpg", "https://example.com/character-ref2.jpg"],
    "prompt": "The girl walks from the painting to the room and puts the coffee cup on the table",
    "aspect_ratio": "16:9",
    "movement_amplitude": "auto"
  }'
```

### Polling Logic

- `processing` / `starting` / `running` → wait 5s, retry (typically takes ~60-120s)
- `completed` / `succeeded` → done, get URL from `data.outputs[]`
- `failed` → error, read `data.error`

### Atlas Cloud MCP Tools (if available)

If the Atlas Cloud MCP server is configured, use built-in tools:

```
atlas_generate_video(model="vidu/q3-pro/text-to-video", params={...})
atlas_get_prediction(prediction_id="...")
```

---

## Implementation Guide

1. **Determine task type**:
   - Text-to-video: user describes a scene/action in text → **Q3-Pro T2V**
   - Image-to-video: user provides an image to animate → **Q3-Pro I2V** or **2.0 I2V**
   - Start-end interpolation: user provides two keyframes → **2.0 Start-End**
   - Character-consistent video: user provides reference images → **2.0 / Q1 Reference**
   - Anime content: user wants anime style → **Q3-Pro with style="anime"**

2. **Choose model**:
   - **Q3-Pro** (recommended): Latest generation, best quality, audio/BGM, up to 1080p, anime support
   - **2.0 Image-to-Video**: Budget option at $0.075/video for simple animations
   - **2.0 Start-End**: Unique keyframe interpolation capability
   - **2.0 Reference**: Character-consistent generation from reference images ($0.2/video)
   - **Q1 Reference**: Highest quality reference-to-video ($0.4/video)

3. **Extract parameters**:
   - Prompt: describe scene, action, camera movement
   - Style: general (realistic) or anime
   - Resolution: 540p for drafts, 720p default, 1080p for final output
   - Duration: Q3-Pro supports flexible durations; 2.0 supports 4 or 8 seconds
   - Movement amplitude: small for subtle motion, large for dynamic action
   - Audio: enabled by default on Q3-Pro, set generate_audio=false to disable

4. **Execute**: POST to generateVideo API → poll result → download MP4

5. **Present result**: show file path, offer to play

## Prompt Tips

- **Scene + Action**: "A chef flips a pancake in a busy kitchen, steam rising from the pan"
- **Camera direction**: "Camera slowly pans left...", "Close-up tracking shot of...", "Aerial view..."
- **Anime style**: Use `style: "anime"` + anime-specific prompts: "An anime warrior charges forward, energy aura glowing..."
- **Movement amplitude**: Use `small` for talking heads/subtle scenes, `large` for action/sports
- **Start-End**: Provide visually similar frames for smooth interpolation; dramatic differences work for morphing effects
- **Reference**: Provide clear, well-lit character references from multiple angles for best consistency
