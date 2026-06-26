---
name: vision-bot
description: "Describe images, detect objects, extract text, and analyze webpages. Pass any image URL directly in your task. Responds in your language."
version: 1.2.0
acceptLicenseTerms: true
metadata:
  clawdbot:
    emoji: "👁️"
    homepage: https://aiprox.dev
    requires:
      env:
        - AIPROX_SPEND_TOKEN
---

# Vision Bot

Analyze images for detailed descriptions, object detection, and OCR text extraction. Pass any image URL directly in your task string — no separate field needed. Auto-detects the right mode from your task — OCR for text extraction, counting for quantity questions, or full description by default. Responds in the language of your task.

## When to Use

- Describing image contents for accessibility
- Extracting text from screenshots, signs, or photos (OCR)
- Counting objects in images
- Identifying objects in images
- Analyzing charts, diagrams, or visual data
- Analyzing images in any language (Chinese, Spanish, French, etc.)
- Describing webpage screenshots for audits
- Analyzing any image by including the URL directly in your task

## Usage Flow

1. Include an image URL directly in your task string
2. Or provide `image_url` field separately
3. Task language sets response language automatically

## Security Manifest

| Permission | Scope | Reason |
|------------|-------|--------|
| Network | aiprox.dev | API calls to orchestration endpoint |
| Env Read | AIPROX_SPEND_TOKEN | Authentication for paid API |

## Make Request

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "描述这张图片的内容: https://example.com/photo.jpg",
    "rail": "bitcoin-lightning",
    "spend_token": "$AIPROX_SPEND_TOKEN"
  }'
```

```bash
curl -X POST https://aiprox.dev/api/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Describe this image: https://example.com/photo.jpg",
    "rail": "bitcoin-lightning",
    "spend_token": "$AIPROX_SPEND_TOKEN"
  }'
```

### Response

```json
{
  "description": "A modern office workspace with a standing desk and dual monitors.",
  "objects": ["desk", "monitors", "keyboard", "mouse", "plant", "window", "headphones"],
  "text_found": "Visual Studio Code - main.js"
}
```

## Trust Statement

Vision Bot analyzes images via URL or base64 input. Images are processed transiently using Claude's vision capabilities via LightningProx. No images are stored. Your spend token is used for payment only.
