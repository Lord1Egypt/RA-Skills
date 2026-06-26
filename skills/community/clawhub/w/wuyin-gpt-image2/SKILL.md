---
name: wuyin-gpt-image2
description: Generate images using the WuyinKeji GPT-Image-2 API (速创科技). Supports text-to-image, reference images, multiple aspect ratios, and async result polling. Use when the user wants to generate images via the WuyinKeji GPT-Image-2 API, especially when they mention the API key "DG97rZEqdfTvNTMGG5iFuHUVvm" or the domain "wuyinkeji.com".
---

# WuyinKeji GPT-Image-2 Image Generation

This skill wraps the WuyinKeji (速创科技) GPT-Image-2 async image generation API.

## API Endpoints

| Action | Method | URL |
|--------|--------|-----|
| Submit task | POST | `https://api.wuyinkeji.com/api/async/image_gpt` |
| Query result | GET | `https://api.wuyinkeji.com/api/async/detail?id=<task_id>&key=<key>` |

## Authentication

- **Header**: `Authorization: <api_key>`
- **Body**: also include `"key": "<api_key>"` in JSON payload

## 1. Submit Generation Task

### Request

```bash
curl -s -X POST "https://api.wuyinkeji.com/api/async/image_gpt" \
  -H "Content-Type: application/json" \
  -H "Authorization: <API_KEY>" \
  -d '{
    "key": "<API_KEY>",
    "prompt": "Your image generation prompt here",
    "size": "16:9",
    "urls": ["http://example.com/ref.jpg"]
  }'
```

### Parameters

| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `key` | Yes | string | API key |
| `prompt` | Yes | string | Generation prompt |
| `size` | No | string | Aspect ratio: `auto`, `16:9`, `9:16`, `1:1`, `3:2`, `2:3` (default: `auto`) |
| `urls` | No | array | Reference image URLs (up to 14 images supported by the model) |

### Response

```json
{
  "code": 200,
  "msg": "成功",
  "data": {
    "id": "image_xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "count": "1"
  }
}
```

Save the `data.id` — this is the async task ID.

## 2. Query Result (Polling)

```bash
curl -s "https://api.wuyinkeji.com/api/async/detail?id=<TASK_ID>&key=<API_KEY>"
```

### Response Fields

| Field | Meaning |
|-------|---------|
| `status: 0` | Task submitted, waiting to start |
| `status: 1` | Generating in progress |
| `status: 2` | Done — check `data.result[0]` for image URL |

### Example (completed)

```json
{
  "code": 200,
  "data": {
    "status": 2,
    "result": ["https://openpt1.wuyinkeji.com/xxxx.png"],
    "created_at": "2026-04-22 13:42:01",
    "updated_at": "2026-04-22 13:43:17"
  }
}
```

## 3. Download Image

```bash
curl -sL "<RESULT_URL>" -o output.png
```

Typical resolution: **1672×941** (the API output is fixed at this resolution regardless of the `size` parameter; use the `size` parameter mainly for aspect ratio hints).

## Model Capabilities

- **Text rendering**: Good Chinese/English text support in images (prompt explicitly for sharp, readable typography)
- **Reference images**: Supports up to 14 reference URLs for style/person consistency
- **Realism**: Improved skin texture, hair, facial details over earlier DALL·E models
- **Color accuracy**: Reduced yellow/orange color cast compared to DALL·E

## Tips for Quality

1. **For sharp text**: Explicitly prompt "sharp, crisp, perfectly legible Chinese typography" and specify font style
2. **For person consistency**: Include a clear reference photo URL in `urls`
3. **For billboard/posters**: Prompt "billboard quality", "high contrast", "professional advertising photography"
4. **Output resolution is fixed** at ~1672×941 — upscaling must be done client-side if 4K is needed

## Helper Script

A Bash helper script is available at `scripts/generate.sh`:

```bash
./scripts/generate.sh \
  -k "<API_KEY>" \
  -p "A beautiful sunset over mountains" \
  -s "16:9" \
  -r "http://example.com/ref.jpg" \
  -o "output.png"
```

The script handles submit → poll → download in one command.
