# PoYo VEO 3 1 API Reference

## Endpoint

- Submit task: `https://api.poyo.ai/api/generate/submit`
- Status query: <https://docs.poyo.ai/api-manual/task-management/status>
- Source docs: <https://docs.poyo.ai/api-manual/video-series/veo-3-1>
- OpenAPI JSON: <https://docs.poyo.ai/api-manual/video-series/veo-3-1.json>

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

- `veo3.1-fast` — general generation with this model variant
- `veo3.1-quality` — general generation with this model variant

## Key input fields

- `model` (string, required) — choose one of the documented model ids
- `callback_url` (string, optional) — Webhook callback URL for result notifications
- `prompt` (string, required) — Generation prompt describing the desired output
- `image_urls` (string[], optional) — Reference image URLs for image-to-video.  - Supports public http/https URLs.  - Maximum 3 images.  - Frame mode: first image is the start frame, second image is the end frame.  - Maximum file size: 10MB.  - Supported formats: .jpeg, .jpg, .png, .webp
- `duration` (integer, optional) — Video duration in seconds (fixed at 8). options: 8
- `aspect_ratio` (string, optional) — Video aspect ratio options: 16:9, 9:16
- `resolution` (string, optional) — Output resolution.  - `720p`: Default.  - `1080p`: Full HD.  - `4k`: Ultra HD. options: 720p, 1080p, 4k
- `generation_type` (string, optional) — Video generation type.  - `frame`: Frame-to-video (two images).  - `reference`: Reference image video (three images).  - If omitted, inferred by `image_urls` count: 2 for `frame`, 3 for `reference`. options: frame, reference

## Submission example

```bash
curl -sS https://api.poyo.ai/api/generate/submit   -H 'Authorization: Bearer YOUR_API_KEY'   -H 'Content-Type: application/json'   -d '{
  "model": "veo3.1-fast",
  "callback_url": "https://your-domain.com/callback",
  "input": {
    "prompt": "Dolphins jumping in a bright blue ocean",
    "duration": 8,
    "aspect_ratio": "16:9"
  }
}'
```

## Polling notes

- PoYo returns a `task_id` after submission.
- If `callback_url` is present, PoYo sends a POST callback when the task reaches `finished` or `failed`.
- Whether or not callbacks are used, the same unified task status docs apply: <https://docs.poyo.ai/api-manual/task-management/status>.

## Practical guidance

- Respect the documented image count limit: `image_urls` allows up to 3 item(s).
- Pick duration deliberately: available values are 8.
- Match aspect ratio to the destination surface: 16:9, 9:16.
- Use a supported `resolution`: 720p, 1080p, 4k.
- Save the returned `task_id` immediately so status polling is straightforward.
