---
name: work-im-avatar-generate
description: >
  AI-powered professional IM avatar generator. Upload a personal photo and get
  a clean, high-end business-style headshot — no influencer glamour, just
  polished corporate look. Requires API key from wsdsocial.com.
---

# Work IM Avatar Generator

Generate clean, professional IM avatars with AI. Upload a personal photo and
get a business-grade headshot — minimal, polished, no over-the-top styling.

## Setup

1. Get your API key at https://ai.wsdsocial.com/skills
2. Set as environment variable: `WSD_API_KEY`

## Usage

```bash
curl -X POST "https://ai.wsdsocial.com/api/pub/skills/work-im-avatar-generate/_tool_85" \
  -H "Content-Type: application/json" \
  -H "key: ${WSD_API_KEY}" \
  -d '{
    "request": "Classic light gray background, business suit, clean professional look",
    "custom_data": {
      "files": ["https://example.com/photo.jpg"]
    }
  }'
```

## Parameters

| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| `request` | String | Yes | Avatar generation instructions. Supports multi-dimensional styling: background (classic light gray, seamless pure white), outfit (executive suit, black polo, gray T-shirt, minimalist crew neck white). Suitable for office and social scenarios, creating a professional and reliable personal image. |
| `custom_data` | Object | No | Image data for the avatar |
| `custom_data.files` | Array\<String\> | No | List of image URLs or base64-encoded image data |

## Response

Returns the generated avatar image URL in JSON format.
