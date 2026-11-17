---
name: xiaohongshu-imitation-writer
description: >
  Imitation-write viral social content-marketing notes. Analyzes a
  reference viral post's structure, style, and traffic logic, then generates original,
  differentiated content that matches the reference tone while combining your product
  and selling points — bypassing duplicate detection to iterate quality notes fast.
  Use when the user wants to imitate / rewrite a viral social note, do 爆款仿写
  / 对标爆款 / original rewrite, or turn a reference note into a branded product note.
  Trigger keywords: social content, imitation, 仿写, rewrite,
  改写, viral, 爆款, 对标. Requires an API key from wsdsocial.com.
---

# Viral Note Imitation Writer

Analyze a viral social content-marketing note's structure, style, and traffic
logic, then generate original, differentiated content that matches the reference tone
without copying — combining your product and selling points to bypass duplicate detection
and rapidly iterate quality content.

## Setup

1. Get your API key at https://ai.wsdsocial.com/skills
2. Set as environment variable: `WSD_API_KEY`

## Usage

```bash
curl -X POST "https://ai.wsdsocial.com/api/pub/skills/red-note-imitation-writing/_tool_89" \
-H "Content-Type: application/json" \
-H "key: ${WSD_API_KEY}" \
-d '{
"reference": "Paste a viral note here",
"request": "Keep 300-500 words, use emoji, friendly tone",
"product_info": "Your product details",
"selling_points": "Key selling points"
}'
```

## Parameters

| Param | Type | Required | Description |
|------------------|--------|:--------:|-------------|
| `reference` | String | Yes | Original viral note text to use as style reference |
| `request` | String | No | Additional requirements: word count, tone, emoji usage, etc. |
| `product_info` | String | No | Product / service information |
| `selling_points` | String | No | Key benefits and selling points |

## Response

Returns the generated original social content-marketing style note content.
