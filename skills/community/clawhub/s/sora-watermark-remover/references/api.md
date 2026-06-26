# Sora Watermark Removal API Reference

## Prerequisites

Obtain an API key at: https://nanophoto.ai/settings/apikeys

For OpenClaw users, the recommended setup is to configure the skill with:

- `env.NANOPHOTO_API_KEY=YOUR_API_KEY`

## Endpoint

```
POST https://nanophoto.ai/api/sora/remove-watermark
```

## Headers

| Header | Value |
|--------|-------|
| `Content-Type` | `application/json` |
| `Authorization` | `Bearer YOUR_API_KEY` |

## Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `share_link` | string | Yes | Sora 2 video share link (must contain `sora.chatgpt.com/p/`) |

## Example Request

```bash
curl -X POST "https://nanophoto.ai/api/sora/remove-watermark" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  --data-raw '{
    "share_link": "https://sora.chatgpt.com/p/s_68e83bd7eee88191be79d2ba7158516f"
  }'
```

## Success Response

```json
{
  "success": true,
  "status": "completed",
  "url": "https://video.nanophoto.ai/sora/watermark-remover/2f9385085fbbb64f6e826ba904b5ab56.mp4"
}
```

## Error Response

```json
{
  "success": false,
  "error": "Error description",
  "errorCode": "ERROR_CODE"
}
```

## Error Codes

| errorCode | HTTP Status | Description |
|-----------|-------------|-------------|
| `LOGIN_REQUIRED` | 401 | Authentication required |
| `API_KEY_RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded (100 req/hour) |
| `MISSING_SHARE_LINK` | 400 | Missing `share_link` parameter |
| `INVALID_SHARE_LINK` | 400 | Invalid Sora share link format |
| `GENERATION_FAILED` | 500 | Task creation or processing failed |
