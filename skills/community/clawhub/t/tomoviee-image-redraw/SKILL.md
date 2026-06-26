---
name: tomoviee-image-redraw
description: Redraw image content using Tomoviee Image Redrawing API (`tm_redrawing`) through Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`). Use when users request inpainting, localized replacement, object removal, or mask-based image edits.
---

# Tomoviee AI Image Redrawing

## Overview

Redraw image content with optional mask control.

- API capability: `tm_redrawing`
- White mask area: redraw
- Black mask area: keep unchanged

## Provider and Endpoint Provenance

Use this mapping to verify credential and endpoint provenance before production usage:

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- Gateway host used by this skill: `https://openapi.wondershare.cc`
- Redrawing endpoint: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_redrawing`
- Task result endpoint: `https://openapi.wondershare.cc/v1/open/pub/task`

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
from scripts.tomoviee_redrawing_client import TomovieeRedrawingClient

client = TomovieeRedrawingClient("app_key", "app_secret")
```

## API Usage

### Basic Example

```python
task_id = client.image_redrawing(
    prompt="Clear blue sky with fluffy clouds",
    init_image="https://example.com/photo.jpg",
    mask_url="https://example.com/mask.png",
)

result = client.poll_until_complete(task_id)
import json
output = json.loads(result["result"])
print(output["images_path"][0])
```

### Parameters

- `prompt` (required): positive prompt text
- `init_image` (required): source image URL
  - supported format: `jpg/png`
  - width and height: `>512` and `<2048`
  - aspect ratio: `<3`
- `mask_url` (optional): mask image URL
  - should have same resolution as `init_image`
  - supported format: `jpg/png`
  - width and height: `>512` and `<2048`
  - aspect ratio: `<3`
- `callback`: callback URL (optional)
- `params`: transparent passthrough params (optional)

## Async Workflow

1. Create task and get `task_id`
2. Poll task status with `poll_until_complete(task_id)`
3. Parse output image URLs from `result`

Status codes:
- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

## Resources

- `scripts/tomoviee_redrawing_client.py` - main redrawing client
- `scripts/tomoviee_image_redrawing_client.py` - compatibility import shim
- `scripts/generate_auth_token.py` - auth token helper
- `references/image_apis.md` - endpoint and workflow references
- `references/prompt_guide.md` - prompt writing guidance

## External Resources

- Developer portal (global): `https://www.tomoviee.ai/developers.html`
- API docs (global): `https://www.tomoviee.ai/doc/`
- Developer portal (mainland): `https://www.tomoviee.cn/developers.html`
- API docs (mainland): `https://www.tomoviee.cn/doc/`
- Gateway host used by this package: `https://openapi.wondershare.cc`
