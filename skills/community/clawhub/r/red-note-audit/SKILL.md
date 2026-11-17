---
name: red-note-audit
description: >
  AI-powered Xiaohongshu (RED) note compliance auditor. Reviews note content
  for policy compliance, shadowban risk, and provides optimization suggestions.
  Requires API key from wsdsocial.com.
---

# Red Book Note Audit

Audit Xiaohongshu (RED) note content for compliance and performance.
Checks for policy violations, shadowban risk, and provides actionable
optimization suggestions to improve visibility.

## Setup

1. Get your API key at https://ai.wsdsocial.com/skills
2. Set as environment variable: `WSD_API_KEY`

## Usage

```bash
curl -X POST "https://ai.wsdsocial.com/api/pub/skills/red-note-audit/_tool_87" \
  -H "Content-Type: application/json" \
  -H "key: ${WSD_API_KEY}" \
  -d '{
    "content": "Your full RED note content (title + body)"
  }'
```

## Parameters

| Param | Type | Required | Description |
|-------|------|:--------:|-------------|
| `content` | String | Yes | The full RED note content including title and body text |

## Response

Returns compliance analysis, shadowban risk assessment, and optimization tips.
