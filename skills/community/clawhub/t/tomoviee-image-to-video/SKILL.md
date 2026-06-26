---
name: tomoviee-image-to-video
description: Generate videos from image + text prompts using Tomoviee Image-to-Video API (`tm_img2video_b`) through Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`). Use when users request animating a still image with motion and camera guidance.
---

# Tomoviee AI Image-to-Video

## Overview

Generate a 5-second video from a still image and prompt.

- API capability: `tm_img2video_b`
- Create endpoint: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_img2video_b`
- Result endpoint: `https://openapi.wondershare.cc/v1/open/pub/task`

## Provider and Endpoint Provenance

Use this mapping to verify provider identity and endpoint provenance:

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- Runtime gateway host used by this skill: `https://openapi.wondershare.cc`
- Compatible gateway alias: `https://open-api.wondershare.cc`

This skill sends runtime API calls only to `openapi.wondershare.cc`.

## Credential Handling

- Sensitive credentials required: `app_key` and `app_secret`.
- Credentials are only used to build `Authorization: Basic <base64(app_key:app_secret)>`.
- Credentials are kept in process memory and are not written to disk by this skill.
- Do not hardcode credentials in source files or commit them to git.

## Dependencies

- Runtime dependency: `requests>=2.31.0,<3.0.0`
- Install with: `pip install -r requirements.txt`

## Quick Start

### Authentication helper

```bash
python scripts/generate_auth_token.py YOUR_APP_KEY YOUR_APP_SECRET
```

### Python Client

```python
from scripts.tomoviee_img2video_client import TomovieeImg2VideoClient

client = TomovieeImg2VideoClient("app_key", "app_secret")
```

## API Usage

### Basic Example

```python
task_id = client.image_to_video(
    prompt="Camera slowly pushes in, gentle motion in the scene, cinematic lighting",
    image="https://example.com/landscape.jpg",
    resolution="720p",
    duration=5,
    aspect_ratio="original",
)

result = client.poll_until_complete(task_id)
import json
video_url = json.loads(result["result"])["video_path"][0]
print(video_url)
```

### Parameters

- `prompt` (required): motion and scene guidance text.
- `image` (required): source image URL (`JPG/JPEG/PNG/WEBP`, `<200M`).
- `resolution` (optional): `720p` or `1080p`, default `720p`.
- `duration` (optional): only `5` supported.
- `aspect_ratio` (optional): `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `original`.
- `camera_move_index` (optional): camera movement type `1-46`.
- `callback` (optional): callback URL.
- `params` (optional): transparent callback parameter.

## Async Workflow

1. Create task and get `task_id`
2. Poll with `poll_until_complete(task_id)`
3. Parse video URL from `result`

Status codes:
- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

## Resources

- `scripts/tomoviee_img2video_client.py` - main API client
- `scripts/tomoviee_image_to_video_client.py` - compatibility import shim
- `scripts/generate_auth_token.py` - auth token helper
- `references/video_apis.md` - API reference and constraints
- `references/camera_movements.md` - camera movement index reference
- `references/prompt_guide.md` - prompt writing guidance

## External Resources

- Developer portal (global): `https://www.tomoviee.ai/developers.html`
- API docs (global): `https://www.tomoviee.ai/doc/ai-video/image-to-video.html`
- Developer portal (mainland): `https://www.tomoviee.cn/developers.html`
- API docs (mainland): `https://www.tomoviee.cn/doc/ai-video/image-to-video.html`