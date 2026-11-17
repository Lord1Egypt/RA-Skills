---
name: video-object-remover
description: Remove an unwanted person, object, logo, or distraction from a video with Video Object Remover.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - VIDEO_OBJECT_REMOVER_API_KEY
      bins:
        - curl
    primaryEnv: VIDEO_OBJECT_REMOVER_API_KEY
    homepage: https://videoobjectremover.com/blog/remove-objects-from-video-with-openclaw
    emoji: "🎬"
---

# Video Object Remover

Use this skill when the user wants to remove one unwanted visual element from a video they own or are authorized to edit.

## Workflow

1. Confirm the local video path and one precise target description. Include position, color, or clothing when useful. Do not process videos the user is not allowed to edit.
2. Create a job with `POST https://videoobjectremover.com/api/v1/jobs`, multipart fields `video` and `prompt`, and `Authorization: Bearer $VIDEO_OBJECT_REMOVER_API_KEY`.
3. Poll `GET /api/v1/jobs/<jobId>` every few seconds. When the status is `MASK_READY`, show the `maskUrl` to the user and ask for explicit confirmation. Never erase automatically.
4. If the user confirms, `POST /api/v1/jobs/<jobId>` with `{"action":"erase"}`. If they want a different target, send `{"action":"reselect","prompt":"..."}` instead.
5. Continue polling until `COMPLETED`, then give the user `videoUrl`. For a free preview, explain that it is watermarked and cannot be downloaded.

## Limits and failures

- Accept MP4, MOV, and WebM files up to 100 MB.
- A new account receives one 5-second watermarked preview. Full videos are limited to 60 seconds and require 10 paid credits.
- Report API errors directly in plain language. Do not retry a failed create request automatically because it may have reserved credits.
- Keep the API key secret: never print it, write it into a command log, or include it in a URL.
