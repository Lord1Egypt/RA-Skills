---
name: zyt-tts-test
description: Use Chanjing TTS API to convert text to speech by listing voices, creating synthesis tasks, and polling task status. This skill reads app_id and secret_key from ~/.chanjing/credentials.json or $CHANJING_CONFIG_DIR/credentials.json, refreshes access_token for API calls, and returns login guidance when credentials are missing or invalid.
metadata:
  openclaw:
    requires:
      env:
        - CHANJING_CONFIG_DIR
        - CHANJING_AUTO_OPEN_LOGIN
    homepage: https://open-api.chanjing.cc
---

# Chanjing TTS

## When to Use This Skill

Use this skill when the user wants to convert text into speech audio with Chanjing TTS.

Typical uses:

- generate Chinese or English speech from text
- list available voices and choose a suitable one
- adjust speech speed
- create a TTS task and poll until completion
- return the remote audio URL and subtitle timestamps from the API result

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
- API base is fixed to `https://open-api.chanjing.cc`

If credentials are missing or invalid, scripts return login guidance with the official Chanjing login URL (no browser auto-open by default):

- `https://www.chanjing.cc/openapi/login`

Optional behavior:

- set `CHANJING_AUTO_OPEN_LOGIN=1` only when you explicitly want local scripts to try opening the login page in your default browser.

### Standard Workflow

All API calls use JSON and UTF-8.

1. Read local credentials and obtain a valid `access_token`
2. List available voices and select one
3. Create a speech synthesis task and get `task_id`
4. Poll task status until success or failure
5. On success, return the remote audio URL from the API response

By default, return the remote audio URL only. Do not auto-download the audio file unless the user explicitly asks to save it locally.

## Covered APIs

This skill currently covers:

- `POST /open/v1/access_token`
- `GET /open/v1/list_common_audio`
- `POST /open/v1/create_audio_task`
- `POST /open/v1/audio_task_state`

## Scripts

Scripts are located in `scripts/`.

| Script | Purpose |
|------|------|
| `chanjing-config` | write or inspect local `app_id` / `secret_key` configuration |
| `_auth.py` | read local credentials, fetch or refresh `access_token` |
| `list_voices` | list available public voices, default output is `id/name`, optional `--json` for full data |
| `create_task` | create a TTS task and print `task_id` |
| `poll_task` | poll task status until completion and print the remote audio URL |

## Usage Examples

```bash
# 0. Configure credentials
python scripts/chanjing-config \
  --ak "<your_app_id>" \
  --sk "<your_secret_key>"

# 1. List voices
python scripts/list_voices

# 2. Create a synthesis task
TASK_ID=$(python scripts/create_task \
  --audio-man "f9248f3b1b42447fb9282829321cfcf2" \
  --text "Hello, I am your AI assistant.")

# 3. Poll until completion and get the remote audio URL
python scripts/poll_task --task-id "$TASK_ID"
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

Response example:

```json
{
  "trace_id": "8ff3fcd57b33566048ef28568c6cee96",
  "code": 0,
  "msg": "success",
  "data": {
    "access_token": "1208CuZcV1Vlzj8MxqbO0kd1Wcl4yxwoHl6pYIzvAGoP3DpwmCCa73zmgR5NCrNu",
    "expire_in": 1721289220
  }
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

### List Voices

List available public voices:

```http
GET /open/v1/list_common_audio
access_token: {{access_token}}
```

Use query parameters:

```json
{
  "page": 1,
  "size": 100
}
```

Response example:

```json
{
  "trace_id": "25eb6794ffdaaf3672c25ed9efbe49c6",
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": "f9248f3b1b42447fb9282829321cfcf2",
        "grade": 0,
        "name": "带货小芸",
        "gender": "female",
        "lang": "multilingual",
        "desc": "",
        "speed": 1,
        "pitch": 1,
        "audition": "https://res.chanjing.cc/chanjing/res/upload/ms/2025-06-05/7945e0474b8cb526e884ee7e28e4af8d.wav"
      },
      {
        "id": "f5e69c1bbe414bec860da3294e177625",
        "grade": 0,
        "name": "方言口音老奶奶",
        "gender": "female",
        "lang": "multilingual",
        "desc": "",
        "speed": 1,
        "pitch": 1,
        "audition": "https://res.chanjing.cc/chanjing/res/upload/ms/2025-04-30/1b248ad05953028db5a6bcba9a951164.wav"
      }
    ],
    "page_info": {
      "page": 1,
      "size": 100,
      "total_count": 98,
      "total_page": 1
    }
  }
}
```

Important voice fields:

| Field | Description |
|---|---|
| `id` | voice ID |
| `name` | voice name |
| `gender` | gender |
| `lang` | language |
| `desc` | description |
| `audition` | audition link |
| `grade` | grade |

Common status codes:

| Code | Description |
|---|---|
| `0` | success |
| `10400` | access token verification failed |
| `40000` | parameter error |
| `50000` | system internal error |
| `51000` | system internal error |

### Create Speech Task

Create a TTS task:

```http
POST /open/v1/create_audio_task
access_token: {{access_token}}
Content-Type: application/json
```

Example request body:

```json
{
  "audio_man": "89843d52ccd04e2d854decd28d6143ce",
  "speed": 1,
  "pitch": 1,
  "text": {
    "text": "Hello, I am your AI assistant."
  }
}
```

Important request fields:

| Field | Description |
|---|---|
| `audio_man` | voice ID |
| `speed` | speech speed, range `0.5` to `2` |
| `pitch` | usually keep `1` |
| `text.text` | synthesis text, max 4000 characters |
| `aigc_watermark` | optional visible watermark |

Response example:

```json
{
  "trace_id": "dd09f123a25b43cf2119a2449daea6de",
  "code": 0,
  "msg": "success",
  "data": {
    "task_id": "88f635dd9b8e4a898abb9d4679e0edc8"
  }
}
```

Important response fields:

| Field | Description |
|---|---|
| `code` | response status code |
| `msg` | response message |
| `data.task_id` | task ID for polling |

Common status codes:

| Code | Description |
|---|---|
| `0` | success |
| `400` | invalid parameter format |
| `10400` | access token verification failed |
| `40000` | parameter error |
| `40001` | exceeds QPS limit |
| `40002` | production duration reached limit |
| `50000` | system internal error |

### Poll Task Status

Poll task status until completion:

```http
POST /open/v1/audio_task_state
access_token: {{access_token}}
Content-Type: application/json
```

Example request body:

```json
{
  "task_id": "88f635dd9b8e4a898abb9d4679e0edc8"
}
```

Response example:

```json
{
  "trace_id": "ab18b14574bbcc31df864099d474080e",
  "code": 0,
  "msg": "success",
  "data": {
    "id": "9546a0fb1f0a4ae3b5c7489b77e4a94d",
    "type": "tts",
    "status": 9,
    "text": [
      "猫在跌落时能够在空中调整身体，通常能够四脚着地，这种”猫右自己“反射显示了它们惊人的身体协调能力和灵活性。核磁共振成像技术通过利用人体细胞中氢原子的磁性来生成详细的内部图像，为医学诊断提供了重要工具。"
    ],
    "full": {
      "url": "https://cy-cds-test-innovation.cds8.cn/chanjing/res/upload/tts/2025-04-08/093a59021d85a72d28a491f21820ece4.wav",
      "path": "093a59013d85a72d28a491f21820ece4.wav",
      "duration": 18.81
    },
    "slice": null,
    "errMsg": "",
    "errReason": "",
    "subtitles": [
      {
        "key": "20c53ff8cce9831a8d9c347263a400a54d72be15",
        "start_time": 0,
        "end_time": 2.77,
        "subtitle": "猫在跌落时能够在空中调整身体"
      },
      {
        "key": "e19f481b6cd2219225fa4ff67836448e054b2271",
        "start_time": 2.77,
        "end_time": 4.49,
        "subtitle": "通常能够四脚着地"
      }
    ]
  }
}
```

Important response fields:

| Field | Description |
|---|---|
| `data.status` | `1` means generating, `9` means completed |
| `data.full.url` | remote audio URL |
| `data.full.duration` | audio duration |
| `data.subtitles` | sentence-level timestamps |
| `data.errMsg` | error message |
| `data.errReason` | error reason |

Common status codes:

| Code | Description |
|---|---|
| `0` | success |
| `10400` | access token verification failed |
| `40000` | parameter error |
| `50000` | system internal error |

## Output Convention

Default behavior:

- return the remote audio URL from `data.full.url`
- return subtitles when they are present in the API response
- do not auto-download the file unless the user explicitly asks