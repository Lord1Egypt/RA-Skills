---
name: red-note-content-topic
description: >
  AI-powered Xiaohongshu (RED) topic planner. Generates trending topic ideas
  and title directions based on account positioning and target audience.
  Requires API key from wsdsocial.com.
---

# Red Book Content Topic Planner

Generate trending Xiaohongshu (RED) topic ideas and headline directions.
Based on your account positioning and target audience, AI suggests hot topics
that resonate with your followers.

## Setup

1. Get your API key at https://ai.wsdsocial.com/skills
2. Set as environment variable: `WSD_API_KEY`

## Usage

```bash
curl -X POST "https://ai.wsdsocial.com/api/pub/skills/red-note-content-topic/_tool_88" \
  -H "Content-Type: application/json" \
  -H "key: ${WSD_API_KEY}" \
  -d '{
    "account_direction": "Beauty and skincare, sharing daily routines",
    "target_audience": "Women 25-35, interested in beauty and self-care"
  }'
```

## Parameters

| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| `account_direction` | String | Yes | Account positioning and industry direction |
| `target_audience` | String | No | Target audience description (age, interests, etc.) |

## Response

Returns trending topic suggestions and headline ideas.
