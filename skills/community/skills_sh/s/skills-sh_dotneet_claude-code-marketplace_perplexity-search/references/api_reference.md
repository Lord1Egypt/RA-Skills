# Perplexity API Reference

## Overview

The Perplexity API provides real-time web search and advanced AI reasoning capabilities.

## Authentication

All requests require an `Authorization: Bearer <PERPLEXITY_API_KEY>` header.

## Endpoints

### Chat Completions

**URL**: `https://api.perplexity.ai/chat/completions`
**Method**: POST

#### Request Body

```json
{
  "model": "sonar-pro",
  "messages": [
    {
      "role": "user",
      "content": "Your question"
    }
  ]
}
```

#### Available Models

| Model | Description | Use Case |
|-------|-------------|----------|
| `sonar-pro` | General conversational AI | Everyday questions, quick searches |
| `sonar-deep-research` | Deep research model | Comprehensive reports, detailed analysis |
| `sonar-reasoning-pro` | Reasoning-focused model | Complex problem-solving, logical analysis |

#### Response

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "Response content"
      }
    }
  ],
  "citations": [
    "https://example.com/source1",
    "https://example.com/source2"
  ]
}
```

### Search API

**URL**: `https://api.perplexity.ai/search`
**Method**: POST

#### Request Body

```json
{
  "query": "search query",
  "max_results": 10,
  "max_tokens_per_page": 1024,
  "country": "JP"
}
```

#### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Search query |
| `max_results` | int | No | Maximum number of results (1-20, default: 10) |
| `max_tokens_per_page` | int | No | Maximum tokens per page (256-2048, default: 1024) |
| `country` | string | No | ISO 3166-1 alpha-2 country code |

#### Response

```json
{
  "results": [
    {
      "title": "Page title",
      "url": "https://example.com/page",
      "snippet": "Page excerpt...",
      "date": "2024-01-15"
    }
  ]
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PERPLEXITY_API_KEY` | API key (required) | - |
| `PERPLEXITY_TIMEOUT_MS` | Timeout (milliseconds) | 300000 |
| `PERPLEXITY_PROXY` | Proxy URL | - |
| `HTTPS_PROXY` | HTTPS proxy (alternative) | - |
| `HTTP_PROXY` | HTTP proxy (alternative) | - |

## Error Handling

### HTTP Status Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 400 | Bad Request |
| 401 | Authentication Error (invalid API key) |
| 429 | Rate Limit |
| 500 | Server Error |

### Common Errors

1. **API Key Error**
   - Symptom: 401 error
   - Solution: Verify the `PERPLEXITY_API_KEY` environment variable

2. **Timeout**
   - Symptom: Request does not complete
   - Solution: Increase `PERPLEXITY_TIMEOUT_MS`

3. **Proxy Error**
   - Symptom: Network connection failure
   - Solution: Verify proxy settings (when inside corporate network)

## Rate Limits

The API has rate limits. When making many requests, ensure appropriate intervals between them.

## About Thinking Tokens

The `sonar-deep-research` and `sonar-reasoning-pro` models may output their thinking process in `<think>...</think>` tags before the answer.

To save context tokens, use the `--strip-thinking` option to remove these tags.
