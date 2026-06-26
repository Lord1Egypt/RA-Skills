# wan2.7-r2v API Documentation (Reference to Video)

## Overview

Generate video using reference images and videos as character/scene sources. Supports:
- Multi-character interactions
- Single character performance
- Voice cloning from reference
- First frame control

## API Endpoint

```
POST https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis
```

## Request Headers

| Header | Required | Description |
| --- | --- | --- |
| Content-Type | Yes | Must be `application/json` |
| Authorization | Yes | `Bearer {API_KEY}` |
| X-DashScope-Async | Yes | Must be `enable` |

## Request Body

### Multi-Character with Images and Videos

```json
{
  "model": "wan2.7-r2v",
  "input": {
    "prompt": "视频1在沙发上看电影，图片1在旁边唱歌",
    "media": [
      {"type": "reference_video", "url": "https://example.com/person.mp4"},
      {"type": "reference_image", "url": "https://example.com/singer.png"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "ratio": "16:9",
    "duration": 10,
    "watermark": false
  }
}
```

### With Voice Reference

```json
{
  "model": "wan2.7-r2v",
  "input": {
    "prompt": "视频1对视频2说：听起来不错",
    "media": [
      {
        "type": "reference_video",
        "url": "https://example.com/role1.mp4",
        "reference_voice": "https://example.com/voice.mp3"
      },
      {"type": "reference_video", "url": "https://example.com/role2.mp4"}
    ]
  },
  "parameters": {
    "resolution": "1080P",
    "ratio": "16:9",
    "duration": 10
  }
}
```

### With First Frame Control

```json
{
  "model": "wan2.7-r2v",
  "input": {
    "prompt": "图片1在海边散步",
    "media": [
      {"type": "reference_image", "url": "https://example.com/person.png"},
      {"type": "first_frame", "url": "https://example.com/beach.png"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "duration": 5
  }
}
```

## Character Reference System

Reference characters in prompt using:
- `视频1`, `视频2`, `视频3` - Reference videos in order
- `图片1`, `图片2`, `图片3` - Reference images in order

The numbering follows the order in the `media` array:
- First `reference_video` → `视频1`
- Second `reference_video` → `视频2`
- First `reference_image` → `图片1`
- etc.

## Media Types

| Type | Description | Limits |
| --- | --- | --- |
| reference_image | Character/scene image | JPEG/PNG/BMP/WEBP, 240-8000px, max 20MB |
| reference_video | Character/scene video | mp4/mov, 1-30s, 240-4096px, max 100MB |
| first_frame | Starting frame | Same as reference_image |

### Media Limits

- Reference images: 0-5
- Reference videos: 0-3
- Total references: ≤ 5
- First frame: max 1 (optional)
- Each reference should contain only ONE character

## Voice Reference

Add `reference_voice` field to a media object:

```json
{
  "type": "reference_video",
  "url": "https://example.com/video.mp4",
  "reference_voice": "https://example.com/voice.mp3"
}
```

Voice limits:
- Format: wav, mp3
- Duration: 1-10 seconds
- Size: max 15MB

Voice priority:
- If `reference_voice` provided → Use this voice
- If video has audio but no `reference_voice` → Use video's original voice
- If image reference → Must provide `reference_voice` for voice

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| resolution | string | No | `720P` or `1080P` (default: 1080P) |
| ratio | string | No | `16:9`, `9:16`, `1:1`, `4:3`, `3:4` (default: 16:9). Ignored if first_frame provided. |
| duration | integer | No | 2-10 seconds (default: 5) |
| watermark | boolean | No | Add watermark (default: false) |
| seed | integer | No | Random seed for reproducibility |

## Resolution & Ratio Table

| Resolution | Ratio | Output Size |
| --- | --- | --- |
| 720P | 16:9 | 1280*720 |
| 720P | 9:16 | 720*1280 |
| 720P | 1:1 | 960*960 |
| 720P | 4:3 | 1104*832 |
| 720P | 3:4 | 832*1104 |
| 1080P | 16:9 | 1920*1080 |
| 1080P | 9:16 | 1080*1920 |
| 1080P | 1:1 | 1440*1440 |
| 1080P | 4:3 | 1648*1248 |
| 1080P | 3:4 | 1248*1648 |

## Response

### Task Creation

```json
{
  "output": {
    "task_status": "PENDING",
    "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
  }
}
```

### Task Query

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

### Success Response

```json
{
  "output": {
    "task_id": "eff1443c-ccab-4676-aad3-xxxxxx",
    "task_status": "SUCCEEDED",
    "video_url": "https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4"
  },
  "usage": {
    "duration": 10.0,
    "input_video_duration": 5,
    "output_video_duration": 5,
    "video_count": 1,
    "SR": 720
  }
}
```

## Billing

Total billing = `input_video_duration` + `output_video_duration`

This means reference videos are also counted toward billing.

## Best Practices

1. **Character References**: Each reference should contain only one character for best results
2. **Background Videos**: Avoid empty/background-only videos as references
3. **Voice Matching**: For dialogue, provide voice reference for each speaking character
4. **Ratio Control**: Use `first_frame` to control exact output ratio
5. **Prompt Clarity**: Clearly describe which character does what using `视频N` or `图片N`

## Important Notes

- Task ID validity: 24 hours
- Video URL validity: 24 hours
- Supported output: MP4 (H.264), 30fps
- Content review: Input and output are subject to safety review
