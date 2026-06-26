# wan2.7-t2v API Documentation (Text to Video)

## Overview

Generate videos from text prompts with optional audio. Supports multi-shot narrative and automatic audio generation.

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

```json
{
  "model": "wan2.7-t2v",
  "input": {
    "prompt": "一只小猫在月光下奔跑",
    "negative_prompt": "低分辨率、错误",
    "audio_url": "https://example.com/audio.mp3"
  },
  "parameters": {
    "resolution": "1080P",
    "ratio": "16:9",
    "duration": 5,
    "prompt_extend": true,
    "watermark": false,
    "seed": 12345
  }
}
```

### Input Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| prompt | string | Yes | Text prompt for video generation. Max 5000 characters. |
| negative_prompt | string | No | Content to avoid in video. Max 500 characters. |
| audio_url | string | No | Custom audio URL (wav/mp3, 2-30s, max 15MB). If not provided, model auto-generates matching audio. |

### Parameters

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| resolution | string | No | `720P` or `1080P` (default: 1080P). Affects billing. |
| ratio | string | No | Aspect ratio: `16:9` (default), `9:16`, `1:1`, `4:3`, `3:4` |
| duration | integer | No | Video duration in seconds, 2-15 (default: 5). Affects billing. |
| prompt_extend | boolean | No | Enable intelligent prompt rewriting (default: true) |
| watermark | boolean | No | Add "AI Generated" watermark (default: false) |
| seed | integer | No | Random seed [0, 2147483647] for reproducibility |

## Resolution & Aspect Ratio Table

| Resolution | Ratio | Output Size (W*H) |
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

## Multi-shot Narrative

Control shot structure via natural language in prompt:
- Single shot: Include "生成单镜头视频" in prompt
- Multi-shot: Use timestamps like "第1个镜头[0-3秒] 全景：雨夜的纽约街头"

Note: `shot_type` parameter is deprecated in wan2.7.

## Response

### Task Creation Response

```json
{
  "output": {
    "task_status": "PENDING",
    "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
  },
  "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

### Task Query Endpoint

```
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

### Success Response

```json
{
  "request_id": "caa62a12-8841-41a6-8af2-xxxxxx",
  "output": {
    "task_id": "eff1443c-ccab-4676-aad3-xxxxxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2025-09-29 14:18:52.331",
    "scheduled_time": "2025-09-29 14:18:59.290",
    "end_time": "2025-09-29 14:23:39.407",
    "orig_prompt": "一只小猫在月光下奔跑",
    "video_url": "https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx"
  },
  "usage": {
    "duration": 10,
    "input_video_duration": 0,
    "output_video_duration": 10,
    "video_count": 1,
    "ratio": "16:9",
    "SR": 720
  }
}
```

## Task Status Values

| Status | Description |
| --- | --- |
| PENDING | Task queued |
| RUNNING | Task processing |
| SUCCEEDED | Task completed successfully |
| FAILED | Task execution failed |
| CANCELED | Task canceled |
| UNKNOWN | Task not found or expired |

## Important Notes

- Task ID validity: 24 hours
- Video URL validity: 24 hours (download immediately)
- Billing: resolution (1080P > 720P) × duration (seconds)
- Polling interval: Recommended 15 seconds
