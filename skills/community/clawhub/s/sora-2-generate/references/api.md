# Sora 2 Video Generation API Reference

## Endpoints

- `POST https://nanophoto.ai/api/sora-2/generate`
- `POST https://nanophoto.ai/api/sora-2/check-status`

## Authentication

```text
Authorization: Bearer YOUR_API_KEY
```

For OpenClaw users, the recommended setup is:

- `env.NANOPHOTO_API_KEY=YOUR_API_KEY`
- Structured skill metadata should declare `requires.env=["NANOPHOTO_API_KEY"]` and `primaryEnv="NANOPHOTO_API_KEY"` for registry transparency

## Modes

- `textToVideo`
- `imageToVideo`

## Generate request fields

| Field | Type | Required | Notes |
|------|------|----------|------|
| `prompt` | string | Yes | Main generation prompt |
| `mode` | string | Yes | `textToVideo` or `imageToVideo` |
| `modelTier` | string | No | `sora2`, `sora2-pro-standard`, `sora2-pro-high` |
| `aspectRatio` | string | No | `portrait` or `landscape` |
| `videoDuration` | string | No | `10` or `15` |
| `imageUrls` | string[] | Conditional | Required for `imageToVideo`; must be public URLs |

## Important limitation

API calls accept only `imageUrls` for image-to-video mode. Base64 image upload is not supported.

## Credits

| Model | Duration | Credits |
|-------|----------|---------|
| `sora2` | 10s | 4 |
| `sora2` | 15s | 8 |
| `sora2-pro-standard` | 10s | 60 |
| `sora2-pro-standard` | 15s | 100 |
| `sora2-pro-high` | 10s | 120 |
| `sora2-pro-high` | 15s | 240 |

## Processing behavior

- Default to `sora2`; avoid pro tiers unless explicitly requested
- Wait 120 seconds before the first status check, then check every 20 seconds
- Emit a progress update on each status check and a final completion update when done
- In practice, generation may take roughly 120-480 seconds depending on queue/load, model tier, and prompt complexity
- For Windows compatibility, prefer the bundled Python script over shell-specific curl snippets

Successful submissions return:

```json
{
  "success": true,
  "status": "processing",
  "taskId": "task_abc123",
  "message": "Video generation in progress"
}
```

Then poll the status endpoint every 5-10 seconds.

## Completed status

```json
{
  "success": true,
  "status": "completed",
  "videoUrl": "https://video.nanophoto.ai/sora/...",
  "taskId": "task_abc123",
  "generationTime": 120,
  "creditsUsed": 4
}
```

## Failed status

```json
{
  "success": false,
  "status": "failed",
  "error": "Video generation failed",
  "errorCode": "GENERATION_FAILED",
  "taskId": "task_abc123"
}
```

## Error codes

| errorCode | Meaning |
|-----------|---------|
| `LOGIN_REQUIRED` | Authentication required |
| `API_KEY_RATE_LIMIT_EXCEEDED` | Rate limit exceeded |
| `INSUFFICIENT_CREDITS` | Not enough credits |
| `PROMPT_REQUIRED` | Missing prompt |
| `IMAGE_REQUIRED` | Image required for image-to-video |
| `IMAGE_URLS_REQUIRED` | API requires public `imageUrls` |
| `GENERATION_FAILED` | Generation failed |
| `TASK_ID_REQUIRED` | Missing task ID |
| `TASK_NOT_FOUND` | Task not found or not owned by user |
| `INTERNAL_ERROR` | Internal server error |
