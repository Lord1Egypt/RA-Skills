---
name: red-note-generator
description: >
  AI-powered Xiaohongshu (RED) note content generator. Creates complete RED
  style notes from topic and style requirements. Requires API key from
  wsdsocial.com.
---

# Red Book Note Generator

Generate complete Xiaohongshu (RED) style notes from a topic. Provide a topic
and optional style requirements, and AI creates a fully-formatted note ready
to publish.

## Setup

1. Get your API key at https://ai.wsdsocial.com/skills
2. Set as environment variable: `WSD_API_KEY`

## Usage

```bash
curl -X POST "https://ai.wsdsocial.com/api/pub/skills/red-note-generator/_tool_86" \
  -H "Content-Type: application/json" \
  -H "key: ${WSD_API_KEY}" \
  -d '{
    "topic": "Top 5 skincare products for summer 2024",
    "request": "Friendly tone, use emoji, include bullet points, 400-600 words"
  }'
```

## Parameters

| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| `topic` | String | Yes | The note topic/subject |
| `request` | String | No | Style, word count, format requirements |

## Response

Returns the generated complete RED note content.
