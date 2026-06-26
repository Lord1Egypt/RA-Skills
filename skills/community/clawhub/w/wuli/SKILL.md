---
name: wuli
description: Generate AI images and videos with 25+ active models via Wuli.art open platform API. Use when creating images from text prompts, editing images with one or more references, generating videos from text, animating a first frame, generating first-last-frame videos, or creating auto-video tasks from images and videos. Covers text-to-image, image-to-image, text-to-video, first-frame video, first-last-frame video, auto-video, image quality tiers, prompt optimization, uploads, and no-watermark downloads.
version: 1.0.9
author: sir1st
homepage: https://wuli.art
repository: https://github.com/alibaba-wuli/wuli-skill
requires:
  env:
    - WULI_API_TOKEN
primaryEnv: WULI_API_TOKEN
metadata: {"clawdbot":{"emoji":"🎨","primaryEnv":"WULI_API_TOKEN","requires":{"anyBins":["python3"],"env":["WULI_API_TOKEN"]},"os":["linux","darwin","win32"]}}
tags:
  - ai
  - image-generation
  - video-generation
  - text-to-image
  - text-to-video
  - image-to-video
  - image-editing
  - art
  - creative
  - wuli
triggers:
  - generate image
  - generate video
  - text to image
  - text to video
  - image to video
  - AI art
  - edit image
  - create artwork
  - animate image
  - wuli
---

# Wuli Platform — AI Image & Video Generation

Generate AI images and videos via the [Wuli.art](https://wuli.art) open platform API. Supports text-to-image, multi-reference image editing, text-to-video, first-frame image-to-video, first-last-frame video, auto-video, and sound control on supported video models across 25+ active models including Qwen Image, Seedream, GPT Image 2, Gemini image models, 通义万相, Happy Horse, 可灵, Seedance, and MiniMax Hailuo, with automatic uploads and no-watermark downloads when available.

## When to Use

- User wants to generate images from a text description
- User wants to edit or transform one or more existing images with AI
- User wants to create video from a text prompt
- User wants to animate a static image into a video
- User wants to generate a video from a first frame and last frame
- User wants to generate a video from reference images and/or a reference video
- User needs high-resolution (up to 4K) AI artwork
- User wants batch image generation
- User needs to choose between multiple AI models for best results

## Setup

```bash
export WULI_API_TOKEN="wuli-your-token-here"
```

Get your token: log in to [wuli.art](https://wuli.art), click the **API entry** at the bottom-left corner.

No additional dependencies — uses only Python 3 standard library.

## Quick Start

```bash
# Generate an image (simplest usage)
python3 skill.py --action image-gen --prompt "a serene mountain lake at sunrise"

# Generate a video
python3 skill.py --action txt2video --prompt "waves crashing on a golden beach at sunset"

# First-last-frame video
python3 skill.py --action flf2video --prompt "camera pushes through the scene"   --image_path ./start.jpg --end_image_path ./end.jpg

# Auto-video from a reference video
python3 skill.py --action auto-video --prompt "preserve the motion, make it cinematic"   --video_path ./input.mp4 --model "通义万相 2.6"
```

## Complete Command Reference

```bash
python3 skill.py --action <action> --prompt "description" [options]
```

### Actions

| Action | Description | Reference Inputs |
|---|---|---|
| `image-gen` | Text to image | None |
| `image-edit` | Edit or transform one or more reference images | `--image_url` or `--image_path` |
| `txt2video` | Text to video | None |
| `image2video` | Animate one image into a video | Exactly one `--image_*` |
| `flf2video` | First-last-frame video generation | Start frame via `--image_*`, end frame via `--end_image_*` |
| `auto-video` | Auto-video from reference images and/or videos | `--image_*`, `--video_*`, or both |

### Parameters

| Parameter | Default | Description |
|---|---|---|
| `--prompt` | *(required)* | Generation prompt, max 2000 chars |
| `--model` | auto-selected | Model name (see Model Selection Guide) |
| `--aspect_ratio` | 1:1 (image) / 16:9 (video) | Aspect ratio |
| `--resolution` | 2K (image) / 720P (video) | Output resolution. Model-dependent values include `2K`, `3K`, `4K`, `480P`, `720P`, `768P`, `1080P` |
| `--quality` | backend default | Image quality for supported models. Values include `low`, `medium`, `high`, `低画质`, `标准画质`, `高画质` |
| `--n` | 1 | Number of images to generate (1-4, image-gen only) |
| `--image_url` | — | Reference image URL(s). Supports comma-separated multiple URLs |
| `--image_path` | — | Local reference image path(s). Supports comma-separated multiple files |
| `--end_image_url` | — | End-frame image URL for `flf2video` |
| `--end_image_path` | — | End-frame local image path for `flf2video` |
| `--video_url` | — | Reference video URL(s) for `auto-video`, comma-separated |
| `--video_path` | — | Local reference video path(s) for `auto-video`, comma-separated |
| `--duration` | 5 | Video length in seconds |
| `--negative_prompt` | — | Exclude unwanted elements |
| `--sound` | backend default | Enable sound for supported video models. If omitted, backend default behavior is used |
| `--no-sound` | — | Disable sound for supported video models |
| `--optimize` | true | Prompt optimization is enabled by default and recommended for most prompts |
| `--no-optimize` | — | Disable prompt optimization when you need fully raw prompt behavior |

### Inline References in Prompt (`@imageN` / `@videoN`)

The open platform API accepts inline placeholders inside the prompt to bind a phrase to a specific reference asset:

- `@image1`, `@image2`, ... refer to the 1st, 2nd, ... entry of `--image_path` / `--image_url` (in the order given)
- `@video1`, `@video2`, ... refer to the 1st, 2nd, ... entry of `--video_path` / `--video_url`
- **No space allowed** between `@` and the type, or between the type and the index: `@image1` ✅,  `@image 1` ✗,  `@ image1` ✗
- Case-insensitive: `@Image1` / `@IMAGE1` also work
- **Index out of range** (e.g. `@image5` when only 2 images are passed) → backend rejects with HTTP 400
- Placeholder is rewritten into the canonical `<<<image_N:url>>>` form before reaching any model:
  - **可灵 series** (O1 / V3 Omni / V3 / V2.6 / V2.5 Turbo) — natively understands `<<<image_N>>>` as the Nth entry of `image_list`
  - **通义万相 2.6 R2V / Happy Horse 1.0 R2V** — replaced with the model's internal `characterN` role token
  - **Other models** (Qwen Image / Seedream / Hailuo / Seedance) — the tag is stripped down to plain text `image_N` and embedded inline; no semantic binding, but human readable

Example:
```bash
python3 skill.py --action auto-video   --prompt "把 @image1 中的人物放进 @video1 的场景,保留 @image1 的服装"   --image_path ./hero.jpg --video_path ./scene.mp4   --model "通义万相 2.6"
```

### Input Rules

- `image-edit` accepts one or more reference images
- `image2video` requires exactly one reference image
- `flf2video` requires exactly two images: start frame + end frame
- `auto-video` accepts reference images, reference videos, or both
- `--sound` / `--no-sound` only affect video tasks, and only take effect on models that support sound control
- Local files and remote URLs are auto-uploaded to Wuli OSS before submission

### Aspect Ratios

| Ratio | Use Case |
|---|---|
| `1:1` | Square — social media posts, avatars, icons |
| `16:9` | Widescreen — videos, desktop wallpapers, presentations |
| `9:16` | Vertical — phone wallpapers, stories, reels |
| `4:3` | Classic — photos, prints |
| `3:2` | Photography — DSLR-style landscape shots |
| `2:1` / `1:2` | Wide or tall image crops on supported image models |
| `5:4` / `4:5` | Print and portrait image crops on supported image models |
| `21:9` | Ultra-wide — cinematic banners (image only on supported models) |
| `4:1` / `1:4` | Extreme panorama or vertical crops on supported Gemini image models |

## Model Selection Guide

### Image Models — Which to Choose

| Model | Best For | Resolution | Ref Images | Cost |
|---|---|---|---|---|
| 智能IMAGE 2 | Highest-control image generation/editing with quality tiers | 1K, 2K, 4K | 4 | quality-based |
| 全能图片 2 | Gemini Flash image generation/editing | 1K, 2K, 4K | 4 | 9-20 credits |
| 全能图片 Pro | Gemini Pro image generation/editing | 1K, 2K, 4K | 4 | 4-5 credits |
| 通义万相 2.7 | Newest Wan image model, up to 9 ref images | 2K, 4K | 9 | 1 credit (2K) / 3 credits (4K) |
| **Qwen Image 2.0** *(default)* | General purpose, fast, versatile | 2K, 4K | 4 | 1 credit |
| Qwen Image Turbo | Quick drafts, iterations | 2K, 4K | 4 | 1 credit |
| Seedream 5.0 Lite | Higher detail at lower cost than premium Seedream | 2K, 3K | 8 | 4 credits |
| Seedream 4.5 | Photorealism, high-fidelity detail | 2K, 4K | 8 | 4 credits |
| Seedream 4.0 | Photorealism with broad API-side support | 2K, 4K | 8 | 4 credits |

**Recommendations:**
- **Fastest & cheapest**: Qwen Image Turbo
- **Best all-rounder**: Qwen Image 2.0
- **Best quality control**: 智能IMAGE 2 with `--quality low|medium|high`
- **Best new image models**: 智能IMAGE 2, 全能图片 2, 全能图片 Pro
- **Best detail at mid tier**: Seedream 5.0 Lite
- **Best quality for photos**: Seedream 4.5
- **Most ref images (up to 9)**: 通义万相 2.7
- **Need 4K**: 通义万相 2.7, Qwen Image 2.0, Qwen Image Turbo, or Seedream 4.5

### Video Models — Which to Choose

| Model | Best For | Resolution | Duration | Key Modes |
|---|---|---|---|---|
| **通义万相 2.2 Turbo** *(default)* | Quick videos, low cost | 720P | 5s | TXT, FF |
| 通义万相 2.7 | Newest Wan video model with stronger narrative | 720P-1080P | 5-15s (AUTO 5-10) | TXT, FF, FLF, AUTO |
| 通义万相 2.6 Flash | Fast image-to-video | 720P-1080P | 5-15s | FF |
| 通义万相 2.6 | Best all-rounder with auto-video | 720P-1080P | 5-15s | TXT, FF, AUTO |
| Happy Horse 1.1 | Newest Happy Horse video model, lower 1080P cost | 720P-1080P | 5-15s | TXT, FF, AUTO |
| Happy Horse 1.0 | Long-duration TXT/FF/AUTO video with video-reference edit | 720P-1080P | 3-15s | TXT, FF, AUTO |
| 可灵 3.0 Omni | Richest multi-input video workflow | 720P-1080P | 5-15s | TXT, FF, FLF, AUTO |
| 可灵 O1 | Premium omni video quality | 720P-1080P | 5-10s | TXT, FF, FLF, AUTO |
| 可灵 3.0 | High-quality first-last-frame video | 720P-1080P | 5-15s | TXT, FF, FLF |
| 可灵 2.6 | 1080P-focused Kling generation | 1080P | 5-10s | TXT, FF, FLF |
| 可灵 2.5 Turbo | Lower-cost Kling first-last-frame workflows | 1080P | 5-10s | TXT, FF, FLF |
| Seedance 1.5 Pro | Motion-heavy videos, up to 12s | 480P-720P | 5-12s | TXT, FF, FLF |
| Seedance 1.0 Pro | Broad resolution coverage | 480P-1080P | 5-10s | TXT, FF, FLF |
| MiniMax Hailuo 2.3 | Cinematic text/video generation | 768P-1080P | 6-10s | TXT, FF |
| MiniMax Hailuo 2.3 Fast | Faster image-to-video | 768P-1080P | 6-10s | FF |

**Recommendations:**
- **Fastest & cheapest**: 通义万相 2.2 Turbo
- **Best all-rounder**: 通义万相 2.7 or 通义万相 2.6
- **Best multi-input / auto-video**: 可灵 3.0 Omni or 通义万相 2.7
- **Best Happy Horse model**: Happy Horse 1.1 for image references, Happy Horse 1.0 when you need video-reference auto-video
- **Best premium quality**: Happy Horse 1.1, 可灵 O1, or 可灵 3.0
- **Best for first-last-frame**: 通义万相 2.7, 可灵 3.0, 可灵 2.6, or Seedance 1.5 Pro
- **Best for 1080P-only workflows**: 可灵 2.6 or 可灵 2.5 Turbo

## Examples

### Text to Image

```bash
# Simple generation
python3 skill.py --action image-gen --prompt "anime girl with blue hair in a garden"

# Batch generate 4 images to pick the best
python3 skill.py --action image-gen --prompt "cyberpunk cityscape at night" --n 4

# Photorealistic with premium model
python3 skill.py --action image-gen --prompt "photorealistic mountain landscape, golden hour"   --model "Seedream 4.5" --resolution 4K --aspect_ratio 16:9

# Higher-detail model
python3 skill.py --action image-gen --prompt "luxury product photography, studio lighting"   --model "Seedream 5.0 Lite" --resolution 3K

# New quality-tier image model
python3 skill.py --action image-gen --prompt "editorial product shot, crisp reflective studio lighting"   --model "智能IMAGE 2" --resolution 2K --quality high

# Prompt optimization is enabled by default
python3 skill.py --action image-gen --prompt "a cat"

# Disable optimization only when you need exact raw prompting
python3 skill.py --action image-gen --prompt "a cat" --no-optimize
```

### Image Editing

```bash
# Edit a local image
python3 skill.py --action image-edit --prompt "add sunglasses and a hat"   --image_path ./photo.jpg

# Edit with multiple reference images
python3 skill.py --action image-edit --prompt "merge these references into one unified brand illustration"   --image_path "./ref1.jpg,./ref2.jpg"

# Edit a remote image
python3 skill.py --action image-edit --prompt "change background to sunset beach"   --image_url "https://example.com/photo.jpg"

# Style transfer
python3 skill.py --action image-edit --prompt "convert to oil painting style"   --image_path ./landscape.jpg --model "Seedream 4.5"
```

### Text to Video

```bash
# Simple video
python3 skill.py --action txt2video --prompt "waves crashing on a golden beach at sunset"

# Longer duration with higher quality
python3 skill.py --action txt2video --prompt "a cat playing piano in a jazz club"   --model "通义万相 2.6" --duration 10 --resolution 1080P

# Explicitly enable sound on a supported model
python3 skill.py --action txt2video --prompt "a singer performing on a neon stage"   --model "通义万相 2.6" --duration 10 --sound

# Cinematic quality
python3 skill.py --action txt2video --prompt "slow-motion rain drops on a window"   --model "可灵 O1" --resolution 1080P --aspect_ratio 16:9

# Disable sound when you want silent output or a lower-credit tier on some models
python3 skill.py --action txt2video --prompt "slow aerial shot over a mountain lake"   --model "可灵 3.0 Omni" --duration 10 --no-sound
```

### Image to Video (Animate)

```bash
# Animate a landscape photo
python3 skill.py --action image2video --prompt "slow zoom in with gentle wind blowing"   --image_path ./landscape.jpg --duration 5

# Animate from URL with premium model
python3 skill.py --action image2video --prompt "character turns head and smiles"   --image_url "https://example.com/portrait.jpg" --model "可灵 O1"
```

### First-Last-Frame Video

```bash
# Use start and end frame to control motion
python3 skill.py --action flf2video --prompt "a smooth cinematic transition between these two shots"   --image_path ./start.jpg --end_image_path ./end.jpg --model "可灵 3.0"

# Mix local and remote references
python3 skill.py --action flf2video --prompt "the flower blooms naturally from frame one to frame two"   --image_path ./flower_closed.jpg   --end_image_url "https://example.com/flower_open.jpg"
```

### Auto-Video

```bash
# Auto-video from a reference video
python3 skill.py --action auto-video --prompt "keep the action, upgrade it to a cinematic sci-fi look"   --video_path ./input.mp4 --model "通义万相 2.6" --duration 10 --sound

# Auto-video from multiple reference images
python3 skill.py --action auto-video --prompt "turn these keyframes into a coherent product reveal video"   --image_path "./frame1.jpg,./frame2.jpg,./frame3.jpg"   --model "可灵 3.0 Omni" --resolution 1080P

# Auto-video with both images and video
python3 skill.py --action auto-video --prompt "preserve the motion, but restyle everything as an anime sequence"   --image_url "https://example.com/style_ref.jpg"   --video_url "https://example.com/source.mp4"   --model "可灵 O1"
```

## Workflow

```
1. (Optional) Upload reference images/videos
   --image_path ./photo.jpg             → auto-uploaded to cloud storage
   --image_url https://...              → auto-downloaded and re-uploaded
   --video_path ./clip.mp4              → auto-uploaded to cloud storage
   --image_path "./a.jpg,./b.jpg"       → uploads multiple image refs

2. Submit generation task
   → Returns recordId for tracking

3. Auto-poll for completion
   → Images: polls every 5s (up to 5 min)
   → Videos: polls every 10s (up to 20 min)

4. Auto-download results
   → Fetches no-watermark version when available
   → Saves to current directory
   → Auto-opens on macOS/Linux/Windows
```

## Troubleshooting

- **"WULI_API_TOKEN not set"**: Run `export WULI_API_TOKEN="wuli-your-token"`. Get your token from [wuli.art](https://wuli.art) bottom-left corner → API. The token is sent as `Authorization: Bearer <token>`.
- **"HTTP 401"**: Token is invalid or expired. Regenerate it on the wuli.art platform.
- **"HTTP 429"**: Rate limited. Wait a few seconds and retry.
- **"Error code 2001"**: Insufficient credits. Top up at [wuli.art](https://wuli.art).
- **"REVIEW_FAILED"**: Content moderation rejected the prompt. Rephrase to avoid sensitive content.
- **"TIMEOUT"**: Generation took too long. Try a faster model or shorter duration.
- **"image2video requires exactly one reference image"**: Use only one `--image_*` input for `image2video`.
- **"flf2video requires exactly two reference images"**: Pass a start frame with `--image_*` and an end frame with `--end_image_*`, or provide exactly two image references total.
- **"auto-video requires at least one reference image or video"**: Provide `--image_*`, `--video_*`, or both.
- **Media upload fails**: Supported image formats are `jpg`, `jpeg`, `png`, `webp`. Supported video formats are `mp4`, `mov`, `avi`, `webm`.
- **Sound flag seems ignored**: `--sound` / `--no-sound` only affect video models that expose sound control. Some models or modes may keep backend default behavior.

## Tips

- Prompt optimization is enabled by default and is recommended for most prompts, especially short or vague ones.
- Use `--no-optimize` only when you need the model to follow your raw prompt as directly as possible.
- Start with the default models (Qwen Image 2.0 / 通义万相 2.2 Turbo) when you want the cheapest and simplest path.
- Generate multiple images with `--n 4` and pick the best.
- Use `--negative_prompt` to exclude unwanted elements, e.g. `--negative_prompt "blurry, low quality, watermark"`.
- For video, start with 5-second duration to preview, then re-generate at longer duration once you're happy with the style.
- If a video model supports sound control, `--no-sound` can be useful for silent exports and may reduce credits on some models.
- For `flf2video`, keep the start and end frames visually consistent for smoother motion.
- For `auto-video`, start with one video or 2-3 images before scaling up to more references.
- All results are auto-downloaded without watermarks when available.

For complete API documentation including current model tables and upload flow, see [references/【呜哩Wuli】开放平台 API 文档.md](references/%E3%80%90%E5%91%9C%E5%93%A9Wuli%E3%80%91%E5%BC%80%E6%94%BE%E5%B9%B3%E5%8F%B0%20API%20%E6%96%87%E6%A1%A3.md).
