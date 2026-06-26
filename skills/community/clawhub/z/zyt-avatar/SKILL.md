---
name: chanjing-avatar
description: use chanjing avatar api to create lip-sync videos by uploading source media, creating avatar tasks, and polling task status. this skill reads app_id and secret_key from ~/.chanjing/credentials.json or $CHANJING_CONFIG_DIR/credentials.json and refreshes access_token for api calls. by default it does not auto-open browser pages; it returns login guidance when credentials are missing or invalid.
metadata:
  openclaw:
    requires:
      env:
        - CHANJING_CONFIG_DIR
        - CHANJING_API_BASE
    homepage: https://open-api.chanjing.cc
---

# Chanjing Avatar

## When to Use This Skill

Use this skill when the user wants to create lip-sync avatar videos with Chanjing Avatar.

Typical uses:

- create text-driven lip-sync videos from a source avatar video
- create audio-driven lip-sync videos from a source avatar video plus uploaded audio
- upload video or audio assets and obtain `file_id`
- create a lip-sync generation task
- poll task status until completion and return the remote video URL

## How to Use This Skill

This skill includes its own local configuration and authentication flow.

### Local Configuration

This skill reads credentials from:

- `~/.chanjing/credentials.json`
- or `$CHANJING_CONFIG_DIR/credentials.json`

The credentials file should contain:

```json
{
  "app_id": "<your_app_id>",
  "secret_key": "<your_secret_key>"
}
```

Supported environment variables:

- `CHANJING_CONFIG_DIR`: custom local config directory
- `CHANJING_API_BASE`: custom API base URL, default is `https://open-api.chanjing.cc`

If credentials are missing or invalid, scripts return login guidance with the official Chanjing login URL (no browser auto-open by default):

- `https://www.chanjing.cc/openapi/login`

Optional behavior:

- set `CHANJING_AUTO_OPEN_LOGIN=1` only when you explicitly want local scripts to try opening the login page in your default browser.

### Standard Workflow

All API calls use JSON and UTF-8.

1. Read local credentials and obtain a valid `access_token`
2. Upload the source avatar video and optional driving audio to obtain `file_id`
3. Create a lip-sync task with either:
   - text-driven TTS input, or
   - uploaded audio input
4. Poll the task status until success or failure
5. On success, return the remote video URL from the API response

By default, return the remote video URL only. Do not auto-download the generated video unless the user explicitly asks to save it locally.

## Covered APIs

This skill currently covers:

- `POST /open/v1/access_token`
- `GET /open/v1/common/create_upload_url`
- `GET /open/v1/common/file_detail`
- `POST /open/v1/video_lip_sync/create`
- `POST /open/v1/video_lip_sync/list`
- `GET /open/v1/video_lip_sync/detail`

## Scripts

Scripts are located in `scripts/`.

| Script | Purpose |
|------|------|
| `chanjing-config` | write or inspect local `app_id` / `secret_key` configuration |
| `chanjing-get-token` | read local credentials and print a valid `access_token` |
| `_auth.py` | read local credentials, fetch or refresh `access_token` |
| `get_upload_url` | request an upload URL and return `sign_url`, `mime_type`, and `file_id` |
| `upload_file` | upload a local file, poll `file_detail` until ready, then print `file_id` |
| `create_task` | create a lip-sync task and print the returned task id |
| `poll_task` | poll task status until completion and print the remote `video_url` |

## Usage Examples

### TTS-driven lip-sync

```bash
# 0. Configure credentials
python scripts/chanjing-config \
  --ak "<your_app_id>" \
  --sk "<your_secret_key>"

# 1. Upload source video and get video_file_id
VIDEO_FILE_ID=$(python scripts/upload_file \
  --service lip_sync_video \
  --file ./my_video.mp4)

# 2. Create a TTS-driven lip-sync task
TASK_ID=$(python scripts/create_task \
  --video-file-id "$VIDEO_FILE_ID" \
  --text "君不见黄河之水天上来" \
  --audio-man-id "C-f2429d07554749839849497589199916")

# 3. Poll until completion and get the remote video URL
python scripts/poll_task --id "$TASK_ID"
```

### Audio-driven lip-sync

```bash
# 1. Upload source video
VIDEO_FILE_ID=$(python scripts/upload_file \
  --service lip_sync_video \
  --file ./my_video.mp4)

# 2. Upload driving audio
AUDIO_FILE_ID=$(python scripts/upload_file \
  --service lip_sync_audio \
  --file ./my_audio.wav)

# 3. Create an audio-driven lip-sync task
TASK_ID=$(python scripts/create_task \
  --video-file-id "$VIDEO_FILE_ID" \
  --audio-file-id "$AUDIO_FILE_ID")

# 4. Poll until completion and get the remote video URL
python scripts/poll_task --id "$TASK_ID"
```

## API Notes

### Access Token

Read `app_id` and `secret_key` from the local credentials file. If there is no valid token, request one from:

```http
POST /open/v1/access_token
Content-Type: application/json
```

Request body:

```json
{
  "app_id": "<from local credentials>",
  "secret_key": "<from local credentials>"
}
```

Important response fields:

| Field | Description |
|---|---|
| `code` | response status code |
| `msg` | response message |
| `data.access_token` | valid token for subsequent calls |
| `data.expire_in` | token expiration timestamp |

Common status codes:

| Code | Description |
|---|---|
| `0` | success |
| `400` | invalid parameter format |
| `40000` | parameter error |
| `50000` | system internal error |

### Upload Media Files

Before creating a lip-sync task, upload the source avatar video and optional driving audio through the File Management API.

#### Get upload URL

```http
GET /open/v1/common/create_upload_url
access_token: {{access_token}}
```

Query parameters:

| Parameter | Description |
|---|---|
| `service` | use `lip_sync_video` for avatar video and `lip_sync_audio` for driving audio |
| `name` | original file name with extension |

The response includes:

- `sign_url`
- `mime_type`
- `file_id`

Use the returned `sign_url` with HTTP `PUT` to upload the file, and set `Content-Type` to the returned `mime_type`.

After upload completes, poll the file detail API until the file is ready:

```http
GET /open/v1/common/file_detail?id={{file_id}}
access_token: {{access_token}}
```

Only use the returned `file_id` for task creation after the file status is ready.

### Create Lip-Sync Task

Create a lip-sync task:

```http
POST /open/v1/video_lip_sync/create
access_token: {{access_token}}
Content-Type: application/json
```

#### TTS-driven example

```json
{
  "video_file_id": "e284db4d95de4220afe78132158156b5",
  "screen_width": 1080,
  "screen_height": 1920,
  "model": 0,
  "audio_type": "tts",
  "tts_config": {
    "text": "君不见黄河之水天上来，奔流到海不复回。",
    "audio_man_id": "C-f2429d07554749839849497589199916",
    "speed": 1,
    "pitch": 1
  }
}
```

#### Audio-driven example

```json
{
  "video_file_id": "e284db4d95de4220afe78132158156b5",
  "screen_width": 1080,
  "screen_height": 1920,
  "model": 0,
  "audio_type": "audio",
  "audio_file_id": "audio_file_id_from_file_management"
}
```

Important request fields:

| Field | Description |
|---|---|
| `video_file_id` | uploaded avatar video `file_id` |
| `screen_width` | output width, default `1080` |
| `screen_height` | output height, default `1920` |
| `model` | `0` basic, `1` high quality |
| `audio_type` | `tts` or `audio` |
| `tts_config.text` | text content for TTS-driven mode |
| `tts_config.audio_man_id` | voice ID for TTS-driven mode |
| `tts_config.speed` | speech speed, range `0.5` to `2` |
| `tts_config.pitch` | pitch, usually keep `1` |
| `audio_file_id` | uploaded driving audio `file_id` for audio-driven mode |
| `callback` | optional callback URL |
| `volume` | optional volume, range `1` to `100` |

Successful response:

```json
{
  "trace_id": "8d10659438827bd4d59eaa2696f9d391",
  "code": 0,
  "msg": "success",
  "data": "9499ed79995c4bdb95f0d66ca84419fd"
}
```

Important response fields:

| Field | Description |
|---|---|
| `code` | response status code |
| `msg` | response message |
| `data` | task id used for polling |

### Query Task List

List lip-sync tasks:

```http
POST /open/v1/video_lip_sync/list
access_token: {{access_token}}
Content-Type: application/json
```

Request body:

```json
{
  "page": 1,
  "page_size": 10
}
```

Important response fields in each task item:

| Field | Description |
|---|---|
| `id` | task id |
| `status` | `0` pending, `10` generating, `20` success, `30` failed |
| `progress` | generation progress |
| `msg` | task message |
| `video_url` | remote generated video URL |
| `preview_url` | preview image URL |
| `duration` | video duration in ms |
| `create_time` | unix timestamp |

### Poll Task Detail

Poll task status until completion:

```http
GET /open/v1/video_lip_sync/detail
access_token: {{access_token}}
```

Query parameter:

| Parameter | Description |
|---|---|
| `id` | task id |

Important response fields:

| Field | Description |
|---|---|
| `data.id` | task id |
| `data.status` | `0` pending, `10` generating, `20` success, `30` failed |
| `data.progress` | progress `0-100` |
| `data.msg` | task message |
| `data.video_url` | remote video URL |
| `data.preview_url` | preview image URL |
| `data.duration` | video duration in ms |
| `data.create_time` | unix timestamp |

### Callback Notification

If a callback URL is provided, the system may send a POST request after task completion with the same task detail payload shape.

## Output Convention

Default behavior:

- return the remote video URL from `data.video_url`
- return task status and progress when polling
- do not auto-download the generated file unless the user explicitly asks