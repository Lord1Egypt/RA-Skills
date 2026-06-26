# PoYo Seedance 1 5 Pro API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/seedance-1-5-pro>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/video-series/seedance-1-5-pro.json>

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

- `seedance-1.5-pro` — higher-quality or premium jobs

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Enter video description
- `image_urls` (string[], optional) — Reference image URLs for video generation (1st image as the first frame, 2nd image as the last frame). File URL after upload, not file content; Accepted types: image/jpeg, image/png, image/webp; Max size: 10.0MB
- `duration` (integer, required) — Video duration in seconds options: 4, 8, 12
- `aspect_ratio` (string, required) — Select the frame dimensions. options: 1:1, 21:9, 4:3, 3:4, 16:9, 9:16
- `resolution` (string, optional) — Standard (480p) / High (720p) / Ultra (1080p) options: 480p, 720p, 1080p
- `fixed_lens` (boolean, optional) — Whether to keep the camera lens fixed
- `generate_audio` (boolean, optional) — Whether to generate an audio track

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "seedance-1.5-pro",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "slow zoom, sunset glow",
    "image_urls": [
      "https://example.com/image.jpg"
    ],
    "aspect_ratio": "16:9",
    "resolution": "720p",
    "duration": 4,
    "fixed_lens": false,
    "generate_audio": true
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Respect the documented image count limit: `image_urls` allows up to 2 item(s).
- Pick duration deliberately: available values are 4, 8, 12.
- Match aspect ratio to the destination surface: 1:1, 21:9, 4:3, 3:4, 16:9, 9:16.
- Use a supported `resolution`: 480p, 720p, 1080p.
- Save the returned `task_id` immediately so status polling is straightforward.
