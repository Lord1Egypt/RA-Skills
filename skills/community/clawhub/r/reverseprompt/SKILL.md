---
name: video-reverse-prompt
description: "Analyze videos to extract reverse prompts, shot-by-shot breakdowns, and AI-ready visual descriptions via the NanoPhoto.AI Video Reverse Prompt API. Use when: (1) User wants reverse prompt, prompt extraction, or video-to-prompt analysis, (2) User provides a YouTube link, direct MP4 URL, or local MP4 file and wants a shot list / storyboard-style breakdown, (3) User mentions video analysis, shot breakdown, extract prompt from video, NanoPhoto, or reverse engineer a video prompt. Supports YouTube links, direct .mp4 URLs, and local file upload. Prerequisite: Obtain an API key at https://nanophoto.ai/settings/apikeys and configure env.NANOPHOTO_API_KEY."
homepage: https://nanophoto.ai
metadata: {"openclaw":{"homepage":"https://nanophoto.ai","requires":{"env":["NANOPHOTO_API_KEY"]},"primaryEnv":"NANOPHOTO_API_KEY"}}
---

# Video Reverse Prompt

Analyze videos to extract detailed shot breakdowns and AI-ready prompts via the NanoPhoto.AI API.

Use the bundled script for local file uploads instead of inlining large base64 payloads directly in the shell; it is more reliable for multi-megabyte videos.

## Prerequisites

1. Obtain an API key at: https://nanophoto.ai/settings/apikeys
2. Configure `NANOPHOTO_API_KEY` before using the skill.

Preferred OpenClaw setup:

- Open the skill settings for this skill
- Add an environment variable named `NANOPHOTO_API_KEY`
- Paste the API key as its value

Equivalent config shape:

```json
{
  "skills": {
    "entries": {
      "video-reverse-prompt": {
        "enabled": true,
        "env": {
          "NANOPHOTO_API_KEY": "your_api_key_here"
        }
      }
    }
  }
}
```

Other valid ways to provide the key:

- **Shell**: `export NANOPHOTO_API_KEY="your_api_key_here"`
- **Tool-specific env config**: any runtime that injects `NANOPHOTO_API_KEY`

Credential declaration summary:

- Required env var: `NANOPHOTO_API_KEY`
- Primary credential: `NANOPHOTO_API_KEY`
- No unrelated credentials are required

If the env var is not set, ask the user to configure it before proceeding.

## Workflow

1. Collect the video source from the user (YouTube link, direct .mp4 URL, or local file path)
2. Determine `videoSource` type: `youtube`, `url`, or `file`
3. Confirm the user is authorized to upload or process the content
4. If local file: read and base64-encode it (must be .mp4, max 30 MB)
5. Call the API (streaming response)
6. Return the shot breakdown and prompts to the user

## API Call

### YouTube Video

```bash
curl -X POST "https://nanophoto.ai/api/sora-2/reverse-prompt" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{
    "videoSource": "youtube",
    "locale": "en",
    "videoUrl": "https://www.youtube.com/watch?v=XXXXXXXXXXX"
  }'
```

### Direct Video URL

```bash
curl -X POST "https://nanophoto.ai/api/sora-2/reverse-prompt" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw '{
    "videoSource": "url",
    "locale": "en",
    "videoUrl": "https://example.com/video.mp4"
  }'
```

### Local File (Preferred: bundled script)

```bash
python3 scripts/reverse_prompt_file.py your-video.mp4 --locale en
```

The script reads `NANOPHOTO_API_KEY` from the environment, validates the file size/format, base64-encodes the MP4, and prints the streaming text response.

### Local File (Manual Base64 request)

```bash
VIDEO_BASE64=$(base64 < your-video.mp4)

curl -X POST "https://nanophoto.ai/api/sora-2/reverse-prompt" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NANOPHOTO_API_KEY" \
  --data-raw "{
    \"videoSource\": \"file\",
    \"locale\": \"en\",
    \"videoFile\": \"$VIDEO_BASE64\",
    \"videoFileName\": \"your-video.mp4\"
  }"
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `videoSource` | string | Yes | `youtube`, `url`, or `file` |
| `locale` | string | No | Output language (default: `en`). Supported: `en`, `zh`, `zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `ar` |
| `videoUrl` | string | Conditional | YouTube link or direct .mp4 URL |
| `videoFile` | string | Conditional | Base64-encoded video (when `videoSource` is `file`) |
| `videoFileName` | string | No | Original filename for uploaded videos |

### Constraints

- Only `.mp4` format supported
- Max file size: **30 MB** (before base64 encoding)
- `videoFile` accepts plain base64 or Data URL (`data:video/mp4;base64,...`)
- Costs **1 credit** per API call

## Response

The API returns a **streaming text response** (`Content-Type: text/plain; charset=utf-8`) containing a Markdown table with:

- Shot number, framing/angle, camera movement
- Detailed visual description
- Audio analysis (BGM, sound effects, narration)
- Duration per shot
- Overall summary

## Error Handling

| errorCode | HTTP | Cause | Action |
|-----------|------|-------|--------|
| `LOGIN_REQUIRED` | 401 | Invalid or missing API key | Verify key at https://nanophoto.ai/settings/apikeys |
| `API_KEY_RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded | Wait and retry |
| `INSUFFICIENT_CREDITS` | 402 | Not enough credits | Top up credits |
| `INVALID_INPUT` | 400 | Missing required parameters | Check `videoSource` and corresponding fields |
| `INVALID_YOUTUBE_URL` | 400 | Invalid YouTube URL | Ask user for a valid YouTube link |
| `INVALID_VIDEO_URL` | 400 | Invalid video URL | Ask user for a valid .mp4 URL |
| `INVALID_FORMAT` | 400 | Not MP4 format | Only .mp4 is supported |
| `FILE_TOO_LARGE` | 400 | File exceeds 30 MB | Ask user for a smaller file |
| `VIDEO_DOWNLOAD_FAILED` | 400 | Cannot download video | Check URL accessibility |
| `VIDEO_PROCESSING_FAILED` | 422 | Processing error | Retry or try a different video |
| `AI_SERVICE_ERROR` | 503 | AI service unavailable | Retry later |

## Bundled script

- `scripts/reverse_prompt_file.py`: Reliable local-file uploader for `.mp4` inputs. Use it when the user provides a local video path.

## Full API Reference

See [references/api.md](references/api.md) for complete endpoint documentation.
