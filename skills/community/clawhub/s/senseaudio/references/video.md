# Video and Storyboard Reference

## Table of Contents

- Endpoint summary
- Upload asset
- Create video task
- Poll video task
- Create storyboard
- Storyboard conversation
- Practical pipeline

## Endpoint Summary

- Create video task: `POST https://api.senseaudio.cn/v1/video/create`
- Query task status: `GET https://api.senseaudio.cn/v1/video/status?id=<task_id>`
- Upload media: `POST https://api.senseaudio.cn/v1/video/upload`
- Create storyboard: `POST https://api.senseaudio.cn/v1/video/storyboard/create`
- Storyboard conversation: `POST https://api.senseaudio.cn/v1/video/storyboard/conversation`

Headers:

- `Authorization: Bearer <API_KEY>`
- `Content-Type: application/json` for JSON APIs
- multipart form for upload

## Upload Asset

Endpoint:

- `POST /v1/video/upload`

Form fields:

- required: `model`, `file`
- optional: `filename`, `media_id`, `provider`

Returns:

- `file_id` and metadata (`url`, size, mime, width/height, duration, etc.)

Use `file_id` in `reference_images` or `reference_videos`.

## Create Video Task

Endpoint:

- `POST /v1/video/create`

Required:

- `model`
- `prompt`
- one of `duration` or `n_frames` (if both provided, doc says `duration` takes effect)

Optional examples:

- `aspect_ratio`, `orientation`, `size`, `style`, `title`
- `reference_images`, `reference_videos`
- `storyboard_id`
- provider-specific fields

Response:

- `task_id`
- initial `status`
- `provider`
- `priority`

## Poll Video Task

Endpoint:

- `GET /v1/video/status?id=<task_id>`

Key response fields:

- `status`: `pending|processing|completed|failed`
- `progress`
- output URLs (`video_url`, `thumbnail_url`, `gif_url`)
- `error_message`

Polling guidance:

- Poll every 5-10 seconds (per doc)
- Stop on `completed` or `failed`

## Create Storyboard

Endpoint:

- `POST /v1/video/storyboard/create`

Required:

- `prompt`
- `duration`
- `orientation`: `landscape|portrait|square`
- `status`: typically `draft`

Response:

- `storyboard_id`
- `summary` with `title` and `shots[]`

## Storyboard Conversation

Endpoint:

- `POST /v1/video/storyboard/conversation`

Required:

- `storyboard_id`
- `prompt`
- `max_frame` (doc mapping: 300->10s, 450->15s, 750->25s)
- `storyboard[]` entries containing at least `shot`, `duration`

Response:

- updated `storyboard_id`
- refreshed `summary.shots`

## Practical Pipeline

For image-to-video style workflows:

1. Upload media -> get `file_id`
2. (Optional) Create storyboard
3. Create video task using `reference_images` and/or `storyboard_id`
4. Poll task status until final
5. On `failed`, inspect `error_message`, revise prompt/params, retry

Validation checklist:

- Ensure model supports requested duration/frame options.
- Send either `duration` or `n_frames` (prefer one explicit field).
- Keep prompt concrete (scene, subject, motion, style).

