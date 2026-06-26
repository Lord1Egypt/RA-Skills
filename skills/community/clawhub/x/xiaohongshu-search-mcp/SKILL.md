---
name: xiaohongshu-search-mcp
description: Search XiaoHongShu / RED notes through the hosted whatson.red MCP endpoint when users need structured RED search results, note details, or a draft blog payload.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - WHATSON_RED_API_KEY
    primaryEnv: WHATSON_RED_API_KEY
    envVars:
      - name: WHATSON_RED_API_KEY
        required: true
        description: whatson.red Agent API key used as the Bearer token for MCP requests.
    homepage: https://www.whatson.red/agents
---

# XiaoHongShu Search MCP

Use this skill when the user wants to search XiaoHongShu / RED / RedNote and receive structured JSON results through the hosted whatson.red MCP endpoint.

## Requirements

- The user needs a whatson.red account with an Agent API key from https://www.whatson.red/agents.
- Read the API key from `WHATSON_RED_API_KEY`.
- Send the key as `Authorization: Bearer ${WHATSON_RED_API_KEY}`.
- MCP requests use account-based whatson.red billing and credits.

## MCP Endpoint

Use the Streamable HTTP endpoint:

```text
https://www.whatson.red/api/agent/mcp
```

Primary tool:

```text
search_xiaohongshu_notes
```

## Tool Arguments

- `query` string, required: Search query in English, Chinese, or pinyin.
- `limit` number, optional: 1-100, default 60. Values above 20 fetch additional search pages.
- `include_note_details` boolean, optional: Default true. Includes note detail payloads when available.
- `include_blog` boolean, optional: Default false. Returns a draft blog/article payload without publishing it.

Use `limit` values such as 40, 60, 80, or 100 when the user needs more than one page of notes. Note details are best-effort for the returned real notes.

## Expected Response

The tool returns structured content with:

- `query`
- `translatedQuery`
- `searchQuery`
- `notes`
- `noteDetails`
- `blog`
- `blogError`
- `usage`

`usage` includes charged credits, remaining credits, and whether the request was already charged through idempotency.

## REST Alternative

For non-MCP callers, whatson.red also exposes:

```text
POST https://www.whatson.red/api/agent/search
```

REST supports API-key billing and accountless x402 payment. x402 is REST-only; do not use x402 for MCP. REST x402 searches cost $0.05 USDC per raw search on supported USDC networks, and `includeBlog=true` is not available through x402.

## Safety Notes

- Do not ask the user for Browserless, proxy, cookie, or deployment secrets; this skill only uses the hosted whatson.red MCP endpoint.
- Do not attempt to scrape XiaoHongShu directly from this skill.
- Do not publish posts when `include_blog` is true; the returned blog payload is only a draft.
