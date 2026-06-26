---
name: vultr-inference
version: 1.0.0
description: Generate images and text using Vultr Inference API. Supports Flux image generation and various LLMs for text. Use when user wants to generate images, artwork, or text completions.
author: Jimmy
tags:
  - vultr
  - inference
  - image-generation
  - ai
  - flux
  - llm
requires:
  files:
    - path: ~/.config/vultr/api_key
      description: Vultr API key (same as Vultr Cloud API key)
---

# vultr-inference

Generate images and text using Vultr's Inference API.

## Setup

Uses the same API key as Vultr Cloud API. Store it at:
```
~/.config/vultr/api_key
```

## Image Generation

### Available Models

| Model | Description |
|-------|-------------|
| `flux.1-dev` | FLUX.1-dev - High quality |
| `flux.1-schnell` | FLUX.1-schnell - Fast generation |
| `stable-diffusion-3.5-medium` | SD 3.5 Medium - Balanced |

### Generate Image

```bash
curl -X POST "https://api.vultrinference.com/v1/images/generations" \
  -H "Authorization: Bearer $VULTR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "flux.1-schnell",
    "prompt": "a hedgehog eating a burger in Amsterdam",
    "n": 1,
    "size": "1024x1024"
  }'
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | `flux.1-dev`, `flux.1-schnell`, `stable-diffusion-3.5-medium` |
| `prompt` | string | Text description of image |
| `n` | int | Number of images (1-4) |
| `size` | string | `256x256`, `512x512`, `1024x1024` |
| `response_format` | string | `url` (default) or `b64_json` |

### Response

```json
{
  "created": 1734567890,
  "data": [
    {
      "url": "https://ewr.vultrobjects.com/vultrinference-images/tmp_xxx.png"
    }
  ]
}
```

## Text Generation (Chat Completions)

### Available Models

- `llama-3.1-405b-instruct` - Meta Llama 3.1 405B
- `llama-3.1-70b-instruct` - Meta Llama 3.1 70B
- `llama-3.1-8b-instruct` - Meta Llama 3.1 8B
- `mixtral-8x7b-32768` - Mixtral 8x7B
- `qwen-2-72b-instruct` - Qwen 2 72B

### Chat Completion

```bash
curl -X POST "https://api.vultrinference.com/v1/chat/completions" \
  -H "Authorization: Bearer $VULTR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.1-70b-instruct",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ],
    "max_tokens": 100
  }'
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID from list above |
| `messages` | array | Chat messages with role and content |
| `max_tokens` | int | Maximum tokens to generate |
| `temperature` | float | Randomness (0-2, default 1) |
| `stream` | bool | Stream response (default false) |

## Python Example

```python
import os
import requests

API_KEY = open(os.path.expanduser("~/.config/vultr/api_key")).read().strip()

# Generate image
response = requests.post(
    "https://api.vultrinference.com/v1/images/generations",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "model": "flux.1-schnell",
        "prompt": "a hedgehog eating a burger",
        "size": "512x512",
        "n": 1
    }
)

result = response.json()
image_url = result["data"][0]["url"]
print(f"Image URL: {image_url}")

# Download image
img_response = requests.get(image_url)
with open("generated_image.png", "wb") as f:
    f.write(img_response.content)
```

## List Available Models

```bash
curl -s "https://api.vultrinference.com/v1/models" \
  -H "Authorization: Bearer $VULTR_API_KEY" | jq
```

## Troubleshooting

**401 Unauthorized**
- Check API key is valid
- Ensure key has inference permissions

**400 Bad Request**
- Check model name is correct
- Check size is valid (256x256, 512x512, 1024x1024)
- Check prompt is not empty

**Rate Limits**
- Default: 60 requests per minute
- Contact support for higher limits
