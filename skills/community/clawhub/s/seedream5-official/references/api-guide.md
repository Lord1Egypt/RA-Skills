# Seedream5.0 API Guide

## Endpoint

- URL: https://agent.mathmind.cn/minimalist/api/volcengine/ai/fzGenerateImg5
- Method: POST
- Headers:
  - Content-Type: application/json
  - x-api-key: required

## Request Body

- prompt: string, required
  - Supports Chinese and English
  - Recommended length <= 300 Chinese characters
- size: string, optional, default `2048x2048`
- watermark: boolean, optional, default `true`
- image: string[], optional, default `[]`

## cURL Example

```bash
curl --location 'https://agent.mathmind.cn/minimalist/api/volcengine/ai/fzGenerateImg5' \
--header 'Content-Type: application/json' \
--header 'x-api-key: <YOUR_X_API_KEY>' \
--data '{"prompt": "一只猫咪在玩耍", "size": "2048x2048", "watermark": true, "image": []}'
```

## Common Error Hints

- 401/403: invalid or missing x-api-key
- 429: rate limited, retry later
- 5xx: service unavailable, retry later
- timeout/network: request timeout or network issue, check connection and retry
