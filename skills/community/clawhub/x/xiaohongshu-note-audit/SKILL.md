---
name: xiaohongshu-note-audit
description: >
  Audit social content-marketing note content for policy compliance
  and shadowban / traffic-throttling risk. Scans for banned words, superlative /
  absolute-claim (极限词) violations, and sensitive content, flags the risks, and
  returns actionable, compliant rewrite suggestions to avoid throttling, takedown,
  or account penalties. Use when the user wants to check a social note before
  posting, do 违禁词检测 / 合规审核 / 笔记预审, review social copy for compliance, or assess
  shadowban / 限流 risk. Trigger keywords: social note, content marketing,
  compliance, audit, 审核, 违禁词, 极限词, 限流, shadowban, moderation. Requires an API key
  from wsdsocial.com.
---

# Social Note Compliance Audit

Audit social content-marketing note content for compliance and performance.
Checks for policy violations, banned / superlative words, shadowban (限流) risk, and
provides actionable optimization suggestions to improve visibility and pass review.

## Setup

1. Get your API key at https://ai.wsdsocial.com/skills
2. Set as environment variable: `WSD_API_KEY`

## Usage

```bash
curl -X POST "https://ai.wsdsocial.com/api/pub/skills/red-note-audit/_tool_87" \
-H "Content-Type: application/json" \
-H "key: ${WSD_API_KEY}" \
-d '{
"content": "Your full note content (title + body)"
}'
```

## Parameters

| Param | Type | Required | Description |
|-----------|--------|:--------:|-------------|
| `content` | String | Yes | The full note content including title and body text |

## Response

Returns compliance analysis, shadowban / throttling risk assessment, and optimization tips.
