---
name: superouter-video-gen
description: Use when the user wants to generate a video through the superouter, especially the `seedance-2.0-v1` omni-reference workflow with ordered assets, async submission, `taskId` polling, and direct download URLs.
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["curl"], "env": ["SUPER_KEY"] }
      }
  }
---

# superouter Video Gen

## Overview

This skill is for the **superouter platform API**, not for talking to Jimeng upstream directly.

Default model: `seedance-2.0-v1`,you can get model list from the server.

Use this skill when the user wants to:
- upload ordered reference assets
- submit an async video generation task
- query status with platform `taskId`
- download the final video from the real URL returned by the platform

The platform currently exposes:
- `POST /v1/video/assets/upload`
- `POST /v1/video/omni-reference/task/submit`
- `GET /v1/video/omni-reference/task/query`
- `GET /v1/video/models`
- `GET /me/balance`
- `GET /me/tasks`


## Preconditions
- `SUPER_KEY` must be a **superouter client API key**
- If the platform returns `401` or `403`, stop and tell the user the client key is invalid or disabled
- Default ratio for short drama generation is `9:16` only when the user did not give a ratio
- Default model is `seedance-2.0-v1`; do not invent other fields that affect generation

## Current Platform Rules

### Prompt

- `prompt` max length: `2000` characters

### File types

- Images: `jpg` `jpeg` `png` `webp` `gif` `bmp`
- Video: `mp4` `mov` `m4v`
- Audio: `mp3` `wav`

### File limits

- Single file max: `30MB`
- Total referenced asset size per task max: `100MB`
- Image shortest side min: `320px`
- Image long/short side ratio max: `3:1`
- Video duration max: `15s`
- Audio duration max: `15s`

### Seedance submit limits

- `aspectRatio`: `1:1` `4:3` `3:4` `16:9` `9:16` `21:9`
- `resolution`: `720p` 
- `duration`: `4` to `15`
- `generatingCount`: currently only `1`

### Pricing

For `seedance-2.0-v1`:
- no video reference: `5 credits / second`
- any video reference present: `10 credits / second`
- if `duration` is omitted, use `4` seconds for estimation

`upload` and `query` currently do not deduct credits.

## Asset selection principles

- Only upload the people or scene references that actually matter for the current shot
- Keep the asset list as small and ordered as possible
- If clothing continuity is critical, add clothing references explicitly instead of assuming them
- Video generation is sensitive to reference order; keep `references[]` in the exact business order

## Workflow

### 1. Check balance before submit

Use platform balance, not upstream quota:

```bash
curl "http://superouter.nesports.top/me/balance" \
  -H "Authorization: Bearer ${SUPER_KEY}"
```

Estimate credits before submit:
- use `duration` if provided, otherwise `4`
- if any reference asset is video, multiply by `10`
- otherwise multiply by `5`

If balance is insufficient, stop before upload/submit and explain the estimated cost.

### 2. Validate local inputs

Before any upload:
- confirm every referenced local file exists
- confirm prompt length is `<= 2000`
- do not invent file order
- keep placeholder names aligned with reference order

If the prompt uses named placeholders such as `<<<Image1>>>`, make sure the corresponding `references[].name` values match exactly.

### 3. Upload assets first

Upload each local file to the platform and collect `fileId`.

```bash
curl --request POST "http://superouter.nesports.top/v1/video/assets/upload" \
  --header "Authorization: Bearer ${SUPER_KEY}" \
  --form "file=@/absolute/path/to/reference-1.png"
```

Response example:

```json
{
  "code": "200",
  "message": "Success",
  "result": {
    "fileId": "asset_xxx",
    "fileName": "reference-1.png",
    "contentType": "image/png",
    "mediaType": "image",
    "sizeBytes": 12345,
    "status": "uploaded"
  }
}
```

Rules:
- always save the returned `fileId`
- same-client duplicate upload may return an existing `fileId`
- do not assume one upload call accepts multiple files unless the user specifically wants to script multiple sequential uploads
- you can save `fileId` for next submit if file is same.

### 4. Submit the task

Submit to the platform, not to Jimeng directly.

```bash
curl --request POST "http://superouter.nesports.top/v1/video/omni-reference/task/submit" \
  --header "Authorization: Bearer ${SUPER_KEY}" \
  --header "Content-Type: application/json" \
  --data '{
    "model": "seedance-2.0-v1",
    "prompt": "让 @1 中的人物根据 @2 的内容说话。",
    "references": [
      { "fileId": "asset_image_1", "name": "Image1" },
      { "fileId": "asset_audio_1", "name": "Audio1" }
    ],
    "aspectRatio": "9:16",
    "resolution": 720,
    "duration": 4,
    "generatingCount": 1
  }'
```

Rules:
- keep `references[]` in the exact intended order
- first reference is the first logical asset, second reference is the second logical asset, and so on
- do not invent `aspectRatio`, `resolution`, `duration`, or `references[].name`
- default to async submit behavior; the platform returns `taskId`
- after success, report `taskId` and the estimated credit cost

Successful response shape:

```json
{
  "code": "200",
  "message": "Success",
  "result": {
    "taskId": "task_xxx",
    "status": "submitted"
  }
}
```

### 5. Query task status

Use platform `taskId`.

```bash
curl --get "http://superouter.nesports.top/v1/video/omni-reference/task/query" \
  --header "Authorization: Bearer ${SUPER_KEY}" \
  --data-urlencode "taskId=task_xxx"
```

Possible status values you should expect:
- `submitted`
- `processing`
- `completed`
- `failed`

Completed response example:

```json
{
  "code": "200",
  "message": "Success",
  "result": {
    "taskId": "task_xxx",
    "status": "completed",
    "errorMessage": null,
    "videos": [
      {
        "url": "https://..."
      }
    ]
  }
}
```

Rules:
- the returned `videos[].url` is the real download URL; give it directly to the user
- do not proxy-download unless the user explicitly asks you to save the file locally
- if status is `processing`, report that clearly and stop unless the user asked you to keep polling
- if status is `failed`, return `errorMessage`; the platform may refund automatically

### 6. Optional task list

If the user wants recent tasks instead of querying a single task:

```bash
curl "http://superouter.nesports.top/me/tasks?limit=50" \
  -H "Authorization: Bearer ${SUPER_KEY}"
```

Use this to inspect recent platform tasks. The platform may refresh incomplete tasks when listing them.

## Prompt / ordering rules

- Keep the reference list in the same order the user intends the model to read it
- Use `@1` placeholders only when the request actually names references
- If the user gives unnamed files only, keep order and do not invent semantic names
- If the user asks for a shot prompt rewrite, keep the asset references consistent with the final `references[]`

## Fixed rules

- Use the superouter platform API only
- Default only the model; ask for missing generation inputs that materially affect output
- Do not claim success before you have a platform `taskId`
- Do not wait for completion by default after submit
- If the service is unreachable, tell the user to check whether the superouter API is running
