---
name: tomoviee-reference-to-image
description: Generate images from a reference image using Tomoviee Image-to-Image API (`tm_reference_img2img`) through Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`). Use when users request image-to-image editing, style transfer, or subject-preserving transformations.
---

# Tomoviee AI Reference-to-Image

## Overview

Generate new images from a reference image and prompt.

- API capability: `tm_reference_img2img`
- Create endpoint: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_reference_img2img`
- Result endpoint: `https://openapi.wondershare.cc/v1/open/pub/task`

## Provider and Endpoint Provenance

Use this mapping to verify provider identity and runtime endpoint provenance:

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- Runtime gateway host used by this skill: `https://openapi.wondershare.cc`
- This skill sends runtime API calls only to `openapi.wondershare.cc`

## Credential Handling

- `app_key` and `app_secret` are only used to build `Authorization: Basic <base64(app_key:app_secret)>`.
- Credentials are kept in process memory only and are not written to disk by this skill.
- Do not commit credentials into skill files or repository history.

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
from scripts.tomoviee_img2img_client import TomovieeImg2ImgClient

client = TomovieeImg2ImgClient("app_key", "app_secret")
```

## API Usage

### Basic Example

```python
task_id = client.image_to_image(
    prompt="Keep subject identity and posture, transform scene to modern office, photorealistic lighting",
    reference_image="https://example.com/reference.jpg",
    control_type="2",
    init_image="https://example.com/reference.jpg",
    width=1024,
    height=1024,
    batch_size=1,
    control_intensity=0.5,
)

result = client.poll_until_complete(task_id)
import json
image_url = json.loads(result["result"])["images_path"][0]
print(image_url)
```

### Parameters

- `prompt` (required): Text prompt for preservation and transformation instructions.
- `reference_image` (required): Input reference image URL.
- `control_type` (required): Control mode. Supported values: `"0"`, `"1"`, `"2"`, `"3"`.
- `width` (required): Output width in pixels, range `512-2048`.
- `height` (required): Output height in pixels, range `512-2048`.
- `batch_size` (required): Number of generated images, range `1-4`.
- `control_intensity` (required): Control strength, range `0-1`.
- `init_image` (optional): Required by backend when `control_type="2"`.
- `callback` (optional): Callback URL.
- `params` (optional): Transparent callback passthrough parameter.

## Async Workflow

1. Create task and get `task_id`
2. Poll with `poll_until_complete(task_id)`
3. Parse output image URL(s) from `result`

Status codes:
- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

## Resources

- `scripts/tomoviee_img2img_client.py` - main API client
- `scripts/tomoviee_image_to_image_client.py` - compatibility import shim
- `scripts/generate_auth_token.py` - auth token helper
- `references/image_apis.md` - API reference and constraints
- `references/prompt_guide.md` - prompt writing guidance

## External Resources

- Developer portal (global): `https://www.tomoviee.ai/developers.html`
- API docs (global): `https://www.tomoviee.ai/doc/ai-image/image-to-image.html`
- Developer portal (mainland): `https://www.tomoviee.cn/developers.html`
- API docs (mainland): `https://www.tomoviee.cn/doc/ai-image/image-to-image.html`