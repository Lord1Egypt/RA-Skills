---
name: tomoviee-text-to-video
description: Generate 5-second videos from text prompts using Tomoviee Text-to-Video API (tm_text2video_b) via Wondershare OpenAPI gateway (https://openapi.wondershare.cc). Use when users request text-to-video creation with control over resolution, aspect ratio, and camera movement.
---

# Tomoviee AI Text-to-Video

## Overview

Generate 5-second videos from text descriptions.

- API capability: `tm_text2video_b`
- Supported resolutions: `720p`, `1080p`
- Supported aspect ratios: `16:9`, `9:16`, `4:3`, `3:4`, `1:1`
- Optional camera control: `camera_move_index` (1-46)

## Provider and Endpoints

Use the following provider and endpoint mapping to keep credentials and routing consistent:

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- API gateway host used by this skill: `https://openapi.wondershare.cc`
- Create-task endpoint pattern: `https://openapi.wondershare.cc/v1/open/capacity/application/<capacity_id>`
- Result endpoint: `https://openapi.wondershare.cc/v1/open/pub/task`

This skill sends API requests only to `openapi.wondershare.cc`.

## Quick Start

### Install dependencies

```bash
pip install -r requirements.txt
```

### Authentication

```bash
python scripts/generate_auth_token.py YOUR_APP_KEY YOUR_APP_SECRET
```

### Python Client

```python
from scripts.tomoviee_text2video_client import TomovieeText2VideoClient

client = TomovieeText2VideoClient("app_key", "app_secret")
```

## API Usage

### Basic Example

```python
task_id = client.text_to_video(
    prompt="Golden retriever running through sunlit meadow, slow motion, cinematic",
    resolution="720p",
    aspect_ratio="16:9",
    camera_move_index=5,
)

result = client.poll_until_complete(task_id)
import json
video_url = json.loads(result["result"])["video_path"][0]
print(video_url)
```

### Parameters

- `prompt` (required): Text description (subject + action + scene + camera + lighting)
- `resolution`: `720p` or `1080p` (default: `720p`)
- `duration`: duration in seconds (currently `5`)
- `aspect_ratio`: `16:9`, `9:16`, `4:3`, `3:4`, `1:1`
- `camera_move_index`: camera movement type (`1-46`, optional)
- `callback`: callback URL (optional)
- `params`: transparent passthrough params (optional)

## Async Workflow

1. Create task: call `text_to_video()` and get `task_id`
2. Poll status: call `poll_until_complete(task_id)`
3. Parse result: read video URL from returned JSON

Status codes:
- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

Typical generation time is 1-5 minutes per 5-second video.

## Resources

### scripts/
- `tomoviee_text2video_client.py` - Text-to-Video API client
- `generate_auth_token.py` - auth token generator

### references/
- `video_apis.md` - detailed video API documentation
- `camera_movements.md` - camera movement index reference
- `prompt_guide.md` - prompt writing best practices

## External Resources

- Developer portal (global): `https://www.tomoviee.ai/developers.html`
- API docs (global): `https://www.tomoviee.ai/doc/`
- Developer portal (mainland): `https://www.tomoviee.cn/developers.html`
- API docs (mainland): `https://www.tomoviee.cn/doc/`
- API host used by this skill: `https://openapi.wondershare.cc`
