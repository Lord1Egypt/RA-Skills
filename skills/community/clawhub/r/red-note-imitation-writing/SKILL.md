---
name: red-note-imitation-writing
description: >
  AI-powered Xiaohongshu (RED) note imitation writing. Analyzes viral post
  structure, style, and traffic logic, then generates original differentiated
  content matching the reference tone while avoiding plagiarism detection.
  Requires API key from wsdsocial.com.
---

# Red Book Note Imitation Writing

Analyze viral Xiaohongshu (RED) note structure, style, and traffic logic.
Generate original, differentiated content that matches the reference tone
without copying — combining your product and selling points to bypass duplicate
detection and quickly iterate quality content.

## Setup

1. Get your API key at https://ai.wsdsocial.com/skills
2. Set as environment variable: `WSD_API_KEY`

## Usage

```bash
curl -X POST "https://ai.wsdsocial.com/api/pub/skills/red-note-imitation-writing/_tool_89" \
  -H "Content-Type: application/json" \
  -H "key: ${WSD_API_KEY}" \
  -d '{
    "reference": "Paste a viral RED note here",
    "request": "Keep 300-500 words, use emoji, friendly tone",
    "product_info": "Your product details",
    "selling_points": "Key selling points"
  }'
```

## Parameters

| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| `reference` | String | Yes | Original viral note text to use as style reference |
| `request` | String | No | Additional requirements: word count, tone, emoji usage, etc. |
| `product_info` | String | No | Product/service information |
| `selling_points` | String | No | Key benefits and selling points |

## Response

Returns the generated Xiaohongshu-style note content.
