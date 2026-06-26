## Platform Relay API

These scripts call this platform backend, not the upstream provider directly.

Platform routes:
- `POST /api/veo2/custom_video/model/{model}`
- `GET /api/veo2/custom_video/fetch/{task_id}`

Authentication:

Preferred:

```http
X-API-Token: <platform_token>
```

Compatible fallback:

```http
X-API-Key: <platform_api_key>
X-API-Secret: <platform_api_secret>
```

Notes:
- The backend deducts points before forwarding the request upstream.
- The backend injects the admin-configured upstream Bearer token.
- The backend records relay logs with user, request parameters, response parameters, task id, success, points cost, and timestamp.
- The backend submit endpoint returns immediately after task submission. It does not wait internally for completion.
- `scripts/generate_video.py` submits once and, by default, creates an OpenClaw cron watcher in the same run.
- The watcher polls `GET /api/veo2/custom_video/fetch/{task_id}` every 30 seconds.
- When the task reaches a terminal state, the watcher returns the final result and removes its own cron job.
- The polling and cron behavior must stay inside the skill scripts. Do not implement it by modifying OpenClaw core or unrelated platform routes.
- VEO upstream rules from the provider docs:
  - `veo_3_1-fast`: text-to-video or reference-image video with up to 3 images
  - `veo_3_1-fast-fl`: start/end frame mode with 1-2 images
  - VEO JSON `input_reference` expects Base64 image array string, not HTTP URLs
  - VEO multipart file upload uses repeated `input_reference[]` files and may include Base64 fallback `input_reference`

## Request Styles

### JSON

Use JSON when the upstream expects structured JSON payloads:
- VEO text or URL reference requests
- Banana standard requests
- Gemini Banana requests
- Sora text or `image_url` requests

Examples of fields that may appear in JSON:
- `model`
- `prompt`
- `size`
- `style`
- `image_url`
- `input_reference`
- `metadata`
- `contents`
- `generationConfig`

### Multipart form-data

Use multipart form-data when the upstream expects local file upload fields such as `input_reference`.

Typical multipart text fields:
- `model`
- `prompt`
- `style`
- `size`

Typical multipart file fields:
- `input_reference`

Repeat the same file field name when multiple files are needed.
