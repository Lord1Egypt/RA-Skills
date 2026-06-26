---
name: tomoviee-text2sfx
description: Generate sound effects from text prompts using Tomoviee Text-to-Sound-Effect API (`tm_text2sfx`) through Wondershare OpenAPI gateway (`https://openapi.wondershare.cc`). Use when users request text_to_sound_effect operations or related tasks.
---

# Tomoviee AI Text-to-Sound-Effect

## Overview

Generate sound effects from text prompts.

- API capability: `tm_text2sfx`
- Task creation endpoint: `https://openapi.wondershare.cc/v1/open/capacity/application/tm_text2sfx`
- Result endpoint: `https://openapi.wondershare.cc/v1/open/pub/task`

## Provider and Endpoint Provenance

Use this mapping to verify provider identity and runtime endpoints:

- Vendor portals: `https://www.tomoviee.ai` and `https://www.tomoviee.cn`
- API gateway host used by this skill: `https://openapi.wondershare.cc`
- This skill sends runtime API calls only to `openapi.wondershare.cc`

## Credential Handling

- `app_key` and `app_secret` are only used to construct `Authorization: Basic <base64(app_key:app_secret)>`.
- Credentials are kept in process memory only and are not written to disk by this skill.
- Do not commit credentials into `SKILL.md`, scripts, or repository files.

## Quick Start

### Install dependencies

```bash
pip install requests
```

### Authentication

```bash
python scripts/generate_auth_token.py YOUR_APP_KEY YOUR_APP_SECRET
```

### Python Client

```python
from scripts.tomoviee_text2sfx_client import TomovieeText2SfxClient

client = TomovieeText2SfxClient("app_key", "app_secret")
```

## API Usage

### Basic Example

```python
task_id = client.text_to_sound_effect(
    prompt="Heavy rain falling on roof with distant thunder",
    duration=30,
    qty=1,
)

result = client.poll_until_complete(task_id)
import json
audio_url = json.loads(result["result"])["audio_path"][0]
print(audio_url)
```

### Parameters

- `prompt` (required): Sound effect description
- `duration` (required): Duration in seconds, range `5-180`
- `qty` (optional): Number of generated results, range `1-4`
- `callback` (optional): Callback URL
- `params` (optional): Transparent callback parameter

## Async Workflow

1. Create task and get `task_id`
2. Poll with `poll_until_complete(task_id)`
3. Parse output URL from `result`

Status codes:
- `1` queued
- `2` processing
- `3` success
- `4` failed
- `5` cancelled
- `6` timeout

## Resources

- `scripts/tomoviee_text2sfx_client.py` - main API client
- `scripts/tomoviee_text_to_sound_effect_client.py` - compatibility import shim
- `scripts/generate_auth_token.py` - auth token helper
- `references/audio_apis.md` - focused API reference for `tm_text2sfx`
- `references/prompt_guide.md` - focused prompt writing guide for sound effects

## External Resources

- Developer portal (global): `https://www.tomoviee.ai/developers.html`
- API docs (global): `https://www.tomoviee.ai/doc/`
- Developer portal (mainland): `https://www.tomoviee.cn/developers.html`
- API docs (mainland): `https://www.tomoviee.cn/doc/`
- API gateway host used by this package: `https://openapi.wondershare.cc`
