---
name: veo-video-gen
description: >-
  Generate videos using Pixwith API's Veo 3.1 model.
  Supports text-to-video and image-to-video (start/end frames).
  Two tiers: Fast (quick preview) and Pro (HD with audio).
  Use when the user asks to generate videos, create AI video,
  text-to-video, or image-to-video with Veo 3.1.

version: 1.0.1
publisher: Pixwith AI
homepage: https://pixwith.ai

categories:
  - video-generation
  - ai-tools

tags:
  - pixwith
  - veo
  - video-generation
  - text-to-video
  - image-to-video

env:
  PIXWITH_API_KEY:
    required: true
    description: Pixwith API key used to authenticate API requests.

permissions:
  network:
    domains:
      - api.pixwith.ai
      - uploads.pixwith.ai
      - "*.amazonaws.com"

  filesystem:
    access: user-provided
    description: >
      May read image files explicitly provided by the user
      for image-to-video tasks.

  persistence:
    modify_agent_config: false
    write_files: false

capabilities:
  - check_credits
  - text_to_video
  - image_to_video
  - image_upload
  - task_creation
  - task_status_polling
---

# Pixwith Veo 3.1 — AI Video Generation

Generate videos through Pixwith using its Veo 3.1 integration.
Supports text-to-video and image-to-video with start and end frames.

## ⚠️ CRITICAL — Do NOT Alter API Response Values

**ALL values returned by the API (`task_id`, `result_urls`, `image_url`, `upload_url`, `fields`) are opaque tokens. Use them EXACTLY as returned — do NOT add, remove, or change even a single character.** Store each value in a shell variable and reuse it directly. A single wrong character in `task_id` or `result_urls` will cause errors or broken links.

## Setup

This skill requires a `PIXWITH_API_KEY` environment variable.

**If the variable is not set**, guide the user through these steps:

1. Go to https://pixwith.ai/api and sign up / log in.
2. Click "Add" to create a new API key and copy it.
3. This skill requires a `PIXWITH_API_KEY` provided by the runtime environment
or the hosting platform's secret manager

If the API key is missing or invalid, instruct the user to create or verify a
Pixwith API key from the Pixwith dashboard and provide it through the runtime's
standard secret or environment-variable mechanism.

**Verify** by running:

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get_credits \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY"
```

A successful response looks like `{"code":1,"data":{"credits":500}}`.

## Pricing

| Tier | Model ID | Credits per video | Description                    |
|------|----------|-------------------|--------------------------------|
| Fast | `2-11`   | 50                | Quick generation, good quality |
| Pro  | `2-12`   | 200               | HD quality with audio          |

Always inform the user of the cost before creating a task.
Default to **Fast** unless the user explicitly requests higher quality or audio.

## Model Parameters

- **model_id**: `2-11` (Fast) or `2-12` (Pro)
- **prompt** (required): Describe the video to generate.
- **image_urls** (optional): 1–2 publicly accessible image URLs.
  - 1 image → used as the start frame.
  - 2 images → first is the start frame, second is the end frame.
- **options.prompt_optimization** (boolean, default `true`): Auto-translate prompt to English.
- **options.aspect_ratio** (required): `16:9` or `9:16`.

## Workflow A — Text-to-Video

Use when the user provides only a text prompt and no images.

### Step 1: Check credits

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get_credits \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY"
```

Verify `data.credits` >= 50 (Fast) or >= 200 (Pro).

### Step 2: Create task

```bash
curl -s -X POST https://api.pixwith.ai/api/task/create \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{
    "prompt": "<user_prompt>",
    "model_id": "2-11",
    "options": {
      "prompt_optimization": true,
      "aspect_ratio": "16:9"
    }
  }'
```

Use `"model_id": "2-12"` for Pro tier.

Response contains `data.task_id` and `data.estimated_time` (seconds).

### Step 3: Poll for results

Wait for `estimated_time` seconds, then poll:

```bash
curl -s -X POST https://api.pixwith.ai/api/task/get \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{"task_id": "<task_id>"}'
```

- `data.status == 1` → still processing, wait 10 seconds and poll again.
- `data.status == 2` → done, `data.result_urls` contains the video URL(s).
- `data.status == 3` → failed, inform the user.

Video generation typically takes 60–180 seconds. Present the EXACT `result_urls` to the user.

## Workflow B — Image-to-Video

Use when the user provides one or two reference images (start frame, optional end frame).

### Step 1: Upload local images (if needed)

If the user provides a local file path (not a public URL), upload it first.

**Upload constraints:**

- Allowed formats: `.jpg`, `.jpeg`, `.png` only
- Maximum file size: **10 MB**
- `content_type` must match the file: `image/jpeg` for .jpg/.jpeg, `image/png` for .png
- The presigned upload URL expires in **10 minutes**

**1a. Get a presigned upload URL:**

```bash
curl -s -X POST https://api.pixwith.ai/api/task/pre_url \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{"image_name": "frame.jpg", "content_type": "image/jpeg"}'
```

Set `content_type` based on the file extension:
- `.jpg` / `.jpeg` → `"image/jpeg"`
- `.png` → `"image/png"`

Response:
- `data.upload_url` — presigned POST data (`url` + `fields`)
- `data.image_url` — the final CDN URL to use in `image_urls`

**1b. Upload the file using the presigned data:**

```bash
curl -s -X POST "<upload_url.url>" \
  -F "key=<upload_url.fields.key>" \
  -F "Content-Type=<upload_url.fields.Content-Type>" \
  -F "x-amz-credential=<upload_url.fields.x-amz-credential>" \
  -F "x-amz-algorithm=<upload_url.fields.x-amz-algorithm>" \
  -F "x-amz-date=<upload_url.fields.x-amz-date>" \
  -F "x-amz-signature=<upload_url.fields.x-amz-signature>" \
  -F "policy=<upload_url.fields.policy>" \
  -F "file=@/path/to/local/image.jpg"
```

Fill every field from the `upload_url.fields` object into the form.
After upload, use `data.image_url` from step 1a as the image URL.

Repeat for a second image if the user wants to specify an end frame.
If the user already has public image URLs (start with `http`), skip this step.

### Step 2: Check credits

Same as Workflow A, Step 1.

### Step 3: Create task with images

```bash
curl -s -X POST https://api.pixwith.ai/api/task/create \
  -H "Content-Type: application/json" \
  -H "Api-Key: $PIXWITH_API_KEY" \
  -d '{
    "prompt": "<video_description>",
    "image_urls": ["<start_frame_url>", "<end_frame_url>"],
    "model_id": "2-11",
    "options": {
      "prompt_optimization": true,
      "aspect_ratio": "16:9"
    }
  }'
```

- Pass 1 URL for start-frame-only mode.
- Pass 2 URLs for start + end frame mode.

### Step 4: Poll for results

Same as Workflow A, Step 3.

## Choosing Between Fast and Pro

| Aspect        | Fast (`2-11`)         | Pro (`2-12`)                |
|---------------|-----------------------|-----------------------------|
| Cost          | 50 credits            | 200 credits                 |
| Quality       | Good                  | HD                          |
| Audio         | No                    | Yes, generated audio        |
| Speed         | ~60 seconds           | ~120 seconds                |
| Best for      | Previews, prototyping | Final output, presentations |

Default to **Fast** unless the user requests:
- "high quality", "HD", "professional" → use Pro
- "with audio", "with sound" → use Pro
- "quick", "fast", "preview", "draft" → use Fast

## Error Handling

All API responses follow `{"code": 1, "message": "success", "data": {...}}`.
When `code` is `0`, `message` contains the error. Common errors:

- `Invalid API KEY` — key is missing, wrong, or disabled.
- `Credits not enough` — user needs to purchase more credits at https://pixwith.ai/pricing.
- `Invalid image format` — only jpg, png, jpeg are supported.
- `Invalid image url` — the URL is not publicly accessible.

## Defaults

When the user does not specify preferences, use these defaults:

- model_id: `2-11` (Fast)
- aspect_ratio: `16:9`
- prompt_optimization: `true`
