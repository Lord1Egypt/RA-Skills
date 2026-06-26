# wan2.7-i2v API Documentation (Image to Video)

## Overview

Generate video from image(s) with support for:
- **First-frame to Video**: Generate video from a starting image
- **First + Last Frame**: Generate video with controlled start and end frames
- **Video Continuation**: Extend an existing video clip

## API Endpoint

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

## Request Headers

| Header | Required | Description |
| --- | --- | --- |
| Content-Type | Yes | Must be `application/json` |
| Authorization | Yes | `Bearer {API_KEY}` |
| X-DashScope-Async | Yes | Must be `enable` for async processing |

## Request Body

### First Frame to Video

```json
{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "一幅都市奇幻艺术的场景",
    "media": [
      {"type": "first_frame", "url": "https://example.com/first.png"},
      {"type": "driving_audio", "url": "https://example.com/audio.mp3"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 10,
    "prompt_extend": true,
    "watermark": false
  }
}
```

### First + Last Frame to Video

```json
{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "写实风格,一只小黑猫好奇地仰望天空",
    "media": [
      {"type": "first_frame", "url": "https://example.com/first.png"},
      {"type": "last_frame", "url": "https://example.com/last.png"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 10
  }
}
```

### Video Continuation

```json
{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "一只戴着墨镜的狗在街道上滑滑板",
    "media": [
      {"type": "first_clip", "url": "https://example.com/video.mp4"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 15
  }
}
```

### Video Continuation + End Frame Control

```json
{
  "model": "wan2.7-i2v",
  "input": {
    "prompt": "继续之前的场景",
    "media": [
      {"type": "first_clip", "url": "https://example.com/video.mp4"},
      {"type": "last_frame", "url": "https://example.com/end.png"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 10
  }
}
```

## Media Types

| Type | Description | Limits |
| --- | --- | --- |
| first_frame | Starting frame image | JPEG/PNG/BMP/WEBP, 240-8000px, max 20MB |
| last_frame | Ending frame image | Same as first_frame |
| first_clip | Video to continue from | mp4/mov, 2-10s, 240-4096px, max 100MB |
| driving_audio | Audio to drive video | wav/mp3, 2-30s, max 15MB |

## Valid Media Combinations

| Mode | Required Media |
| --- | --- |
| First-frame | `first_frame` |
| First-frame + Audio | `first_frame` + `driving_audio` |
| First + Last Frame | `first_frame` + `last_frame` |
| First + Last + Audio | `first_frame` + `last_frame` + `driving_audio` |
| Video Continuation | `first_clip` |
| Continuation + End Control | `first_clip` + `last_frame` |

## Input Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| prompt | string | No | Text prompt for video. Max 5000 characters. Recommended. |
| negative_prompt | string | No | Content to avoid. Max 500 characters. |
| media | array | Yes | Media array with type and url fields |

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| resolution | string | No | `720P` or `1080P` (default: 1080P) |
| duration | integer | No | Video duration 2-15 seconds (default: 5) |
| prompt_extend | boolean | No | Enable prompt rewriting (default: true) |
| watermark | boolean | No | Add watermark (default: false) |
| seed | integer | No | Random seed for reproducibility |

## Response

### Task Creation

```json
{
  "output": {
    "task_status": "PENDING",
    "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
  },
  "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

### Task Query

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

### Success Response

```json
{
  "request_id": "2ca1c497-f9e0-449d-9a3f-xxxxxx",
  "output": {
    "task_id": "af6efbc0-4bef-4194-8246-xxxxxx",
    "task_status": "SUCCEEDED",
    "video_url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4"
  },
  "usage": {
    "duration": 10,
    "input_video_duration": 0,
    "output_video_duration": 10,
    "video_count": 1,
    "SR": 720
  }
}
```

## Video Continuation Billing

When using `first_clip` for continuation:
- Input video: 3 seconds
- Duration parameter: 15 seconds
- Model generates: 12 seconds (new content)
- Total output: 15 seconds
- **Billed for: 15 seconds**

## Audio Handling

- If `driving_audio` provided: Video syncs to audio (lip-sync, motion beats)
- If not provided: Model auto-generates matching background music/effects
- Audio longer than `duration`: Auto-truncated to duration
- Audio shorter than `duration`: Video continues silently

## Important Notes

- Output aspect ratio follows input image/video ratio
- Task ID validity: 24 hours
- Video URL validity: 24 hours
- Supported formats: Output is MP4 (H.264), 30fps
