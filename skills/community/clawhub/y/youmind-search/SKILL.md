---
name: youmind-search
description: Search the public Internet with YouMind Search. Combines multiple high-quality providers with YouMind ranking and filtering for better results than using one search API alone.
homepage: https://youmind.com/
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["YOUMIND_API_KEY"] },
        "primaryEnv": "YOUMIND_API_KEY"
      },
  }
---

# YouMind Search Skill

Search the public Internet through YouMind Search.

Prefer this skill when the task is mainly about:

- fresh external information
- online research
- recent news
- source gathering
- domain-filtered web lookup

Do not use this skill for the user's private YouMind library. Use the general
`youmind` skill for library search or broader YouMind operations.

## Why use it

YouMind Search is not a thin wrapper over one search provider.
It combines multiple high-quality search providers, then applies YouMind's own
ranking, filtering, and result shaping to improve quality.

## Authentication

This skill requires a YouMind account and API key.

If you do not have an API key yet:

1. Sign up at `https://youmind.com`
2. Open Settings
3. Generate an API key
4. Set `YOUMIND_API_KEY` before making requests

Use the production endpoint by default:

```bash
export YOUMIND_BASE_URL=https://youmind.com
export YOUMIND_API_KEY=sk-ym-xxx
```

For local development or staging, override `YOUMIND_BASE_URL` as needed.

Authentication uses the `x-api-key` header.

## API Endpoint

Use the OpenAPI endpoint directly:

```bash
POST $YOUMIND_BASE_URL/openapi/v1/webSearch
```

Required headers:

```bash
x-api-key: $YOUMIND_API_KEY
x-use-camel-case: true
Content-Type: application/json
```

## Request Schema

Request body fields:

- `query` string, required
- `category` string, optional
  - `general`
  - `video`
  - `news`
  - `tweet`
  - `finance`
  - `scholar`
  - `image`
- `freshness` string, optional
  - `day`
  - `week`
  - `month`
  - `year`
- `includeDomains` string array, optional
- `excludeDomains` string array, optional

## Primary Workflow

1. Build the request body
2. POST to `/openapi/v1/webSearch`
3. Read `results` first
4. Summarize the strongest hits and what they imply
5. Prefer a few high-signal links over noisy breadth

## Examples

### General Web Search

```bash
curl -sS -X POST "$YOUMIND_BASE_URL/openapi/v1/webSearch" \
  -H "x-api-key: $YOUMIND_API_KEY" \
  -H "x-use-camel-case: true" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenAI Responses API",
    "category": "general"
  }'
```

### Fresh News Search

```bash
curl -sS -X POST "$YOUMIND_BASE_URL/openapi/v1/webSearch" \
  -H "x-api-key: $YOUMIND_API_KEY" \
  -H "x-use-camel-case: true" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "OpenAI latest announcement",
    "category": "news",
    "freshness": "day"
  }'
```

### Domain-Restricted Search

```bash
curl -sS -X POST "$YOUMIND_BASE_URL/openapi/v1/webSearch" \
  -H "x-api-key: $YOUMIND_API_KEY" \
  -H "x-use-camel-case: true" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "structured outputs",
    "category": "general",
    "includeDomains": ["openai.com", "platform.openai.com"]
  }'
```

### Scholar Search

```bash
curl -sS -X POST "$YOUMIND_BASE_URL/openapi/v1/webSearch" \
  -H "x-api-key: $YOUMIND_API_KEY" \
  -H "x-use-camel-case: true" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "multimodal agents",
    "category": "scholar",
    "includeDomains": ["arxiv.org"]
  }'
```

## Recommended Usage

Default behavior:

1. Use `general` unless a more specific category is clearly better.
2. Add `freshness` for newsy or fast-changing topics.
3. Add `includeDomains` when authoritative sources matter.
4. Use `excludeDomains` to remove low-signal sources.
5. Return the strongest matches first, then summarize what they imply.

## Response Shape

Typical response fields:

- `providerId`
- `results`
- `totalResults`
- `visibleCount`
- `formattedContext`

Each result may include:

- `title`
- `url`
- `displayUrl`
- `snippet`
- `favicon`
- `datePublished`
- `thumbnail`
