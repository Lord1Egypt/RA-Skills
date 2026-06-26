---
name: tomoviee-tail-to-video
description: Generate videos from first and last frame images using Tomoviee First-Last Frame API (`tm_tail2video_b`) via Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`). Requires `app_key` and `app_secret`. Use when users request first-last keyframe interpolation, start-end frame animation, or two-image to 5-second video generation.
---

# Tomoviee AI First-Last Frame to Video

## Overview

Generate a 5-second video from two keyframe images:

- `image`: first frame
- `image_tail`: last frame

API capability: `tm_tail2video_b`

## Provider and Endpoint Provenance

Use this mapping to verify provenance before using production credentials:

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- Runtime API gateway host used by this skill: `https://openapi.wondershare.cc`
- Create endpoint: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_tail2video_b`
- Result endpoint: `https://openapi.wondershare.cc/v1/open/pub/task`

This skill sends runtime API requests only to `openapi.wondershare.cc`.

## Credential Handling

- Sensitive credentials required: `app_key` and `app_secret`.
- Credentials are only used to build `Authorization: Basic <base64(app_key:app_secret)>`.
- Credentials are kept in process memory only and are not written to disk by this skill.
- Do not hardcode credentials in source files or commit them to git.

## Required Inputs

- Credentials: `app_key`, `app_secret`
- Generation inputs: `prompt`, `image`, `image_tail`

## Scope

- This skill only covers `tm_tail2video_b` (first-last frame to video).
- Output duration is fixed to 5 seconds by API design.
- This skill does not implement text-to-video, image-to-video, or video continuation APIs.

## Dependencies

- Runtime dependency: `requests>=2.31.0,<3.0.0`
- Install with: `pip install -r requirements.txt`

## Quick Start

### Install dependencies

```bash
pip install -r requirements.txt
```

### Authentication helper

```bash
python scripts/generate_auth_token.py YOUR_APP_KEY YOUR_APP_SECRET
```

### Python Client

```python
from scripts.tomoviee_firstlast2video_client import TomovieeFirstLast2VideoClient

client = TomovieeFirstLast2VideoClient("app_key", "app_secret")
```

## API Usage

### Basic Example

```python
task_id = client.firstlast_to_video(
    prompt="Scene transitions naturally from first frame to last frame with smooth motion",
    image="https://example.com/first-frame.jpg",
    image_tail="https://example.com/last-frame.jpg",
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

- `prompt` (required): Motion guidance text.
- `image` (required): First frame image URL.
- `image_tail` (required): Last frame image URL.
- `resolution` (optional): `720p` or `1080p`, default `720p`.
- `duration` (optional): only `5` is supported.
- `aspect_ratio` (optional): `16:9`, `9:16`, `4:3`, `3:4`, `1:1`, `original`.
- `camera_move_index` (optional): camera movement type `1-46`.
- `callback` (optional): callback URL.
- `params` (optional): transparent callback parameter.

### Image Constraints

- File size: each image must be `<200M`
- Formats: `JPG`, `JPEG`, `PNG`, `WEBP`
- Recommended resolution: at least 720p source quality

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

- `scripts/tomoviee_firstlast2video_client.py` - main API client
- `scripts/generate_auth_token.py` - auth token helper
- `references/video_apis.md` - API reference and constraints
- `references/camera_movements.md` - camera movement index reference
- `references/prompt_guide.md` - prompt writing guidance

## External Resources

- Developer portal (global): `https://www.tomoviee.ai/developers.html`
- API docs (global): `https://www.tomoviee.ai/doc/ai-video/first-and-last-frame-to-video.html`
- Developer portal (mainland): `https://www.tomoviee.cn/developers.html`
- API docs (mainland): `https://www.tomoviee.cn/doc/ai-video/first-and-last-frame-to-video.html`
