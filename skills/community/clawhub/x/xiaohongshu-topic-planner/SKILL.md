---
name: xiaohongshu-topic-planner
description: >
  Plan trending social content-marketing topics and headline
  directions. Based on account positioning and target audience, generates hot topic
  ideas, viral title angles, and content frameworks to solve topic burnout, sameness,
  and low-traffic problems. Use when the user wants social content topic ideas, does
  选题 / 选题策划 / 爆款标题, plans a content calendar, or needs headline directions
  for a niche account. Trigger keywords: social content, topic,
  选题, 选题策划, headline, 标题, content planning, 爆款, trending. Requires an API key from
  wsdsocial.com.
---

# Social Content Topic Planner

Generate trending social content-marketing topic ideas and headline directions.
Based on your account positioning and target audience, the AI suggests hot topics,
viral title angles, and content frameworks that resonate with your followers.

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
|---------------------|--------|:--------:|-------------|
| `account_direction` | String | Yes | Account positioning and industry direction |
| `target_audience` | String | No | Target audience description (age, interests, etc.) |

## Response

Returns trending topic suggestions, headline ideas, and content frameworks.
