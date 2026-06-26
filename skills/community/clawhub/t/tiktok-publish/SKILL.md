---
name: TikTok Publisher
description: >
  Post to TikTok, upload TikTok videos, and publish TikTok video content
  through the MyBrandMetrics API. Use for TikTok posting, uploading TikTok
  videos, publishing TikTok videos, scheduling TikTok posts, or checking TikTok
  publishing status. Supports local video files, remote video
  URLs, post titles, privacy levels, publish status checks, chat-based posting,
  and one-time scheduled posting tasks from a Google Sheet.
---

# TikTok Publisher

Post to TikTok, upload TikTok videos, and publish TikTok video content through
the MyBrandMetrics API from a local file or a remote video URL.

Use this skill to post to TikTok, upload TikTok videos, publish TikTok videos,
schedule TikTok posts, check TikTok publishing status, or create a one-time
scheduled TikTok posting task.

Website: [https://www.clawbus.com/](https://www.clawbus.com/)  
MyBrandMetrics API: [https://mybrandmetrics.com/](https://mybrandmetrics.com/)

## Why This Is Better

This flow is simpler than a typical TikTok API or developer-app setup:

- Sign in to MyBrandMetrics with Google instead of creating a TikTok developer
  app.
- No TikTok client ID, client secret, redirect URI, or callback server to
  manage.
- No manual token storage or refresh flow to build yourself.
- No separate publish backend to run just to queue uploads and check status.
- MyBrandMetrics handles the connection layer, while this skill focuses on
  publishing, polling, and status checks.

## Core Capabilities

| Capability | Details |
| --- | --- |
| Remote URL publishing | Submit a direct `https://` video URL to TikTok through MyBrandMetrics. |
| Local file publishing | Upload a local video file with multipart form data. |
| Post metadata | Set the TikTok post title and privacy level. |
| Chat-based posting | Use natural-language prompts in chat after the skill is installed. |
| One-time scheduled tasks | Create a scheduled publishing task from a Google Sheet containing title, date, time, and video URL rows. |

## Setup Flow

1. Open [https://mybrandmetrics.com/](https://mybrandmetrics.com/) and sign in
   with Google.
2. In MyBrandMetrics, open **Data sources**.
3. Choose `connect tiktok feed`.
4. Complete the TikTok authorization flow if prompted.
5. Get the MyBrandMetrics API key.
6. Add the API key to `/root/.openclaw/workspace/config.json`:

   ```json
   {
     "tiktok": {
       "api_key": "YOUR_API_KEY"
     }
   }
   ```

7. Install the `tiktok-publish` skill.
8. Start publishing or checking TikTok publish status with this skill.

## Positioning Notes

- Use this skill when the user wants TikTok publishing without building their
  own TikTok developer integration.
- Keep the message simple: one Google-based sign-in to MyBrandMetrics, one
  connected TikTok feed, and the publish workflow is ready.
- This is a publishing workflow, not a generic MCP or developer console setup.

## Workflow

Use this workflow to post to TikTok, upload a TikTok video, publish a TikTok
video, schedule TikTok posts, or check a TikTok publishing job.

1. **Confirm the publishing goal.**
   Choose whether to publish from a remote video URL, upload a local video
   file, check an existing publish job, or prepare a scheduled posting
   workflow.

2. **Confirm the TikTok setup.**
   Sign in to MyBrandMetrics with Google, connect TikTok as a data source, and
   get a MyBrandMetrics API key.

3. **Prepare credentials.**
   Add the MyBrandMetrics API key to the workspace config:

   ```json
   {
     "tiktok": {
       "api_key": "YOUR_API_KEY"
     }
   }
   ```

4. **Collect post details.**
   Prepare the TikTok video source, post title, privacy level, and publishing
   preference.

   Useful defaults:

   - choose `SELF_ONLY` for test posts;
   - choose `PUBLIC` when the post is ready to go live;
   - use a concise title or caption;
   - use a remote video URL or local video file that is ready to publish.

5. **Publish the TikTok video.**
   Use the skill to publish from a remote URL or local file. The workflow can
   also wait for the publishing job to finish when needed.

6. **Check publish status.**
   If a publish identifier is returned, use it to check the TikTok publish
   status later. After the job succeeds, confirm the result in the connected
   TikTok account.

### Drafts, Carousels, And Scheduling

The current script supports video publishing from a remote URL or local file.

Known workflow notes:

- Draft-style flows may appear as a TikTok notification that the video is ready
  to edit, rather than as a normal profile draft.
- Image carousel publishing may require phone-friendly image dimensions such as
  1080x1920. Oversized generated images can fail TikTok image checks.
- Scheduled posting should be treated as an automation workflow: confirm the
  sheet columns, publish date, publish time, video URL, title, privacy level,
  and account before creating the task.

### Common Errors

| Error | Likely cause | Fix |
| --- | --- | --- |
| `401 invalid token format` | API key was sent in the wrong auth format or the key is invalid. | Use the MyBrandMetrics API key configuration supported by this skill. Do not use a bearer-token format. |
| `picture_size_check_failed` | Image dimensions do not meet TikTok requirements. | Resize images to a phone-friendly format such as 1080x1920 and retry. |
| `duration_check` | Video is too short. | Use a video that is at least 3 seconds long. |
| `invalid_params` | Title, caption, media, or request parameters are invalid. | Simplify the title, reduce hashtags, and recheck the source URL or local path. |

The chat request should include:

- the video URL or file reference;
- the caption or title;
- whether the post should be a test or public post;
- whether to wait for publish completion.

After the posting flow finishes, check the response and confirm the TikTok
upload succeeded.

## Use The Scripts Directly

Use `scripts/publish_tiktok.py`.

Remote URL:

```bash
python3 scripts/publish_tiktok.py \
  --source "https://example.com/video.mp4" \
  --title "My TikTok Title" \
  --privacy-level "SELF_ONLY"
```

Local file:

```bash
python3 scripts/publish_tiktok.py \
  --source "/path/to/video.mp4" \
  --title "Launch clip" \
  --privacy-level "PUBLIC" \
  --wait-for-published
```

With explicit polling controls:

```bash
python3 scripts/publish_tiktok.py \
  --source "https://example.com/video.mp4" \
  --title "Campaign preview" \
  --privacy-level "SELF_ONLY" \
  --wait-for-published \
  --poll-interval 5000 \
  --poll-timeout 300000
```

## Check Publish Status

Use `scripts/check_status.py` when you already have a `publish_id`.

```bash
python3 scripts/check_status.py --publish-id "PUBLISH_ID"
```

## One-Time Scheduled Posting

ClawBus can also create a one-time scheduled TikTok posting task.

Prepare:

- videos or images uploaded to Google Drive or another reachable location;
- a Google Sheet with post title, publish date, publish time, and video URL;
- sharing access granted only to the trusted account or service that needs to
  read the table.

Example request:

```text
Please help me create a one-time scheduled task. The task involves publishing videos or images to a TikTok account using the tiktok-publish skill, based on the title, date, time, and video URL data found in this table: GOOGLE_SHEET_URL
```

Before scheduling, review every row in the sheet and confirm the account,
publish time, title, and video URL. When the publishing task reports success,
open TikTok and confirm the post is live.

## Parameters

| Parameter | Required | Purpose |
| --- | --- | --- |
| `--source` | Yes | Direct video URL or local video file path. |
| `--title` | Yes | TikTok post title. |
| `--privacy-level` | No | `SELF_ONLY` by default; use `PUBLIC` only when ready to post live. |
| `--wait-for-published` | No | Poll until the publish job completes. |
| `--poll-interval` | No | Polling interval in milliseconds. |
| `--poll-timeout` | No | Polling timeout in milliseconds. |
| `--config` | No | Path to workspace `config.json`. |

Before publishing, confirm the TikTok account, video source, title or caption,
and privacy setting. For test posts, use `SELF_ONLY` first.
