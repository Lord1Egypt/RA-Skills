# Showmeai

**[English](README.md) | [中文](README.zh-CN.md)**

Generate images and videos with AI via Showmeai's API. Image generation uses OpenAI-compatible Images API. Video generation uses Seedance (Doubao) API. Fast, flexible, works out of the box once configured.

---

## Requirements

- Python 3
- A [Showmeai API Key](https://api.showmeai.art) (`Showmeai_API_KEY`)

---

## Configuration

Set in `.env` or `~/.openclaw/openclaw.json`:
- `Showmeai_API_KEY` — your Showmeai API key **(required)**
- `Showmeai_BASE_URL` — base URL with /v1 suffix **(required)**; defaults to `https://api.showmeai.art/v1` if not set

---

## Example Prompts

Once configured, just tell your AI assistant what you want.

### Image Generation - Basic

| Prompt |
|---|
| Draw a sunset over the ocean |
| Generate a cyberpunk city at night |
| Create a cute cartoon cat illustration |

### Image Generation - Aspect Ratio

| Prompt |
|---|
| Generate a 16:9 wallpaper of a starry sky |
| Draw a 2:3 portrait of a fantasy warrior |
| Create a 1:1 square avatar of a fox in a suit |

### Image Generation - Save to Local

| Prompt |
|---|
| Generate a forest scene and save it |
| Draw 3 variations of a mountain landscape and save |

### Image Generation - High Resolution

| Prompt |
|---|
| Generate a high-res 4K illustration of a dragon |
| Create a 2K detailed city map illustration |

---

## Video Generation

### Text-to-Video

| Prompt |
|---|
| Generate a video of a detective entering a dim room |
| Create a video of a cat playing with a ball of yarn |
| Make a 10 second video of a sunset timelapse |

### Image-to-Video

| Prompt |
|---|
| Animate this image with the girl opening her eyes |
| Create a video from this photo, camera slowly pulling out |

### Video Parameters

| Prompt |
|---|
| Generate a 16:9 widescreen video |
| Create a 5 second video at 720p resolution |
| Generate video without audio to save cost |

---

## Image-to-3D Conversion

Convert 2D images to 3D models (PNG with transparent background recommended).

### Basic Conversion

| Prompt |
|---|
| Convert this character image to 3D model |
| Create a 3D model from this sprite with texture |
| Generate high-quality 3D model with more detail |

### 3D Parameters

| Prompt |
|---|
| Convert to GLB format with texture |
| Generate with higher quality (more steps) |
| Create STL file for 3D printing |

---

## Supported Models

### Image Models

| Model | Quality | Output |
|---|---|---|
| `nano-banana` | Standard | URL |
| `nano-banana-pro` | Better — **Default** | URL |
| `nano-banana-2` | Gen 2 | URL |
| `nano-banana-pro-2k` | High-res 2K | URL |
| `nano-banana-pro-4k` | Ultra 4K | URL |
| `gpt-image-1` | High quality | Saved file |
| `gpt-image-1.5` | Higher quality | Saved file |

### Video Models

| Model | Features |
|---|---|
| `doubao-seedance-1-5-pro-251215` | **Default**. Text-to-video, image-to-video, first-and-last-frame. Supports audio generation, draft mode. 24 FPS, 5s/10s duration, 480P/720P resolution. |

### 3D Models

| Model | Features |
|---|---|
| `Hunyuan3D-2` | **Default**. Fast conversion (seconds). Supports glb/stl output. |
| `Hi3DGen` | Image-to-3D conversion. Supports glb/stl output. |
| `Step1X-3D` | Image-to-3D conversion. Supports glb/stl output. |

---

## Save Behavior

| Flag | Behavior |
|---|---|
| *(default)* | Returns image URL only, no local file |
| `--save` | Saves to `~/.openclaw/media/` |
| `--oss` | Saves to `~/.openclaw/oss/` |
| `gpt-image` models | Always saved (API returns base64 only) |

---

## Links

- Showmeai API: [api.showmeai.art](https://api.showmeai.art)
- OpenClaw: [openclaw.ai](https://openclaw.ai)
- ClawHub: [clawhub.ai](https://clawhub.ai)
