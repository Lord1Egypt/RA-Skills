# wan2.7-videoedit API Documentation (Video Editing)

## Overview

Edit existing videos with text instructions and optional reference images. Supports:
- **Instruction-based Editing**: Modify video based on text descriptions
- **Reference Image Editing**: Apply styles/elements from reference images
- **Video Migration**: Transform video with new visual style

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

### Instruction-based Editing

```json
{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "为人物换上酷闪的衣服",
    "media": [
      {"type": "video", "url": "https://example.com/original.mp4"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "audio_setting": "auto",
    "watermark": false
  }
}
```

### Reference Image-based Editing

```json
{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "为人物换上参考图里的帽子",
    "media": [
      {"type": "video", "url": "https://example.com/video.mp4"},
      {"type": "reference_image", "url": "https://example.com/hat.png"}
    ]
  },
  "parameters": {
    "resolution": "720P",
    "watermark": false
  }
}
```

### Video Migration (Style Transfer)

```json
{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "参考视频运镜和动作，用一个卡通小狗形象实现类似效果",
    "media": [
      {"type": "video", "url": "https://example.com/original.mp4"},
      {"type": "reference_image", "url": "https://example.com/cartoon_dog.png"}
    ]
  },
  "parameters": {
    "resolution": "1080P"
  }
}
```

### Multiple Reference Images

```json
{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "将场景变成参考图的夜晚霓虹灯风格",
    "media": [
      {"type": "video", "url": "https://example.com/video.mp4"},
      {"type": "reference_image", "url": "https://example.com/style1.png"},
      {"type": "reference_image", "url": "https://example.com/style2.png"}
    ]
  },
  "parameters": {
    "resolution": "720P"
  }
}
```

## Media Types

| Type | Description | Required | Limits |
| --- | --- | --- | --- |
| video | Input video to edit | Yes (exactly 1) | mp4/mov, 2-10s, 240-4096px, max 100MB |
| reference_image | Style/element reference | No (max 3) | JPEG/PNG/BMP/WEBP, 240-8000px, max 20MB |

## Input Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| prompt | string | No | Editing instruction. Max 5000 characters. Recommended. |
| negative_prompt | string | No | Content to avoid. Max 500 characters. |
| media | array | Yes | Must include exactly one video |

## Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| resolution | string | No | `720P` or `1080P` (default: 1080P) |
| ratio | string | No | Output ratio. If not set, uses input video ratio. Options: `16:9`, `9:16`, `1:1`, `4:3`, `3:4` |
| duration | integer | No | Output duration. Default `0` = same as input. Range: 2-10s |
| audio_setting | string | No | `auto` (default) or `origin` (keep original audio) |
| watermark | boolean | No | Add watermark (default: false) |
| seed | integer | No | Random seed for reproducibility |

## Audio Settings

| Setting | Behavior |
| --- | --- |
| `auto` | Model decides based on prompt. May regenerate audio if prompt describes sounds. |
| `origin` | Always keep original video audio, never regenerate. |

## Duration Behavior

- `duration: 0` (default): Output matches input video length
- `duration: N`: Truncate from beginning, output first N seconds
- Range: 2-10 seconds

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
    "input_video_duration": 5,
    "output_video_duration": 5,
    "video_count": 1,
    "SR": 720,
    "ratio": "16:9"
  }
}
```

## Billing

Total billing = `input_video_duration` + `output_video_duration`

Images are not billed, only video duration.

## Use Cases

### Costume/Appearance Change
```
Prompt: "为人物换上酷闪的衣服"
```

### Scene Transformation
```
Prompt: "将场景变成夜晚，添加霓虹灯效果"
```

### Add Elements from Reference
```
Prompt: "为人物戴上参考图里的帽子"
+ reference_image: hat.png
```

### Style Transfer
```
Prompt: "将视频转换成水彩画风格"
+ reference_image: watercolor_style.png
```

### Motion Transfer
```
Prompt: "参考视频运镜和动作，用卡通角色实现"
+ reference_image: cartoon_character.png
```

## Best Practices

1. **Clear Instructions**: Be specific about what to change
2. **Reference Images**: Use high-quality reference images for style/element transfer
3. **Audio Handling**: Use `origin` if you want to preserve original audio
4. **Duration**: Set explicitly if you need to trim the video
5. **Resolution**: Match or exceed input video quality

## Important Notes

- Task ID validity: 24 hours
- Video URL validity: 24 hours
- Input video max: 10 seconds
- Reference images max: 3
- Output format: MP4 (H.264), 30fps
- Content review: Input and output subject to safety review
