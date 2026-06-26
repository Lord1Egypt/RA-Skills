# PoYo Z Image API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/image-series/z-image>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/image-series/z-image.json>

## Auth

Send:

```http
Authorization: Bearer YOUR_API_KEY
Content-Type: application/json
```

Get API keys from <https://poyo.ai/dashboard/api-key>.

Recommended skill env var:

- `POYO_API_KEY`

## Models

- `z-image` — general generation with this model variant

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Generation prompt describing the desired output
- `size` (string, required) — Image size ratio options: 1:1, 4:3, 3:4, 16:9, 9:16

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "z-image",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "A serene mountain landscape at sunset with vibrant colors",
    "size": "1:1"
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Use a supported `size`: 1:1, 4:3, 3:4, 16:9, 9:16.
- Save the returned `task_id` immediately so status polling is straightforward.
