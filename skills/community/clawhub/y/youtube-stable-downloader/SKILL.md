# Video Offline Saver Skill

Save online videos locally for offline viewing. Supports multiple quality options: 360p, 480p, 720p, 1080p, best quality, and audio-only extraction.

## Quick Install

Tell OpenClaw:

> **"Install this skill: https://clawhub.ai/XJouska/u2-downloader"**

OpenClaw will guide you through the setup process automatically.

## Usage

Once installed, just tell OpenClaw what you need in natural language:

> "Save this video for me: https://youtube.com/watch?v=dQw4w9WgXcQ"

> "Save this video in 1080p: https://youtube.com/watch?v=xxxxx"

> "Extract audio from this video: https://youtube.com/watch?v=xxxxx"

Supported quality options: 360p, 480p, 720p (default), 1080p, best, audio-only.

## API Reference

### POST /api/v1/skill/download

Save an online video for offline access.

**Request:**
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "resolution": "720"
}
```

**Parameters:**
- `youtube_url` (required): The video URL to process
- `resolution` (optional): Target quality — "360", "480", "720", "1080", "best", "audio". Default: "720"

**Response (success):**
```json
{
  "success": true,
  "download_url": "https://oss-bucket.aliyuncs.com/skill/abc123/video.mp4",
  "video_title": "Video Title",
  "video_duration": 212,
  "file_size": 52428800,
  "resolution": "720",
  "processing_time": 45.2
}
```

### GET /api/v1/skill/balance

Check account status.

**Response:**
```json
{
  "username": "user123"
}
```

### GET /api/v1/skill/health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "Video Offline Saver Skill",
  "version": "1.0.0"
}
```

### Error Codes

| Code | Meaning |
|------|---------|
| 200  | Success |
| 401  | Unauthorized |
| 400  | Invalid request (bad URL, etc.) |
| 500  | Server error |

---

# 在线视频离线保存工具

将在线视频保存到本地，方便离线观看。支持多种画质选择：360p、480p、720p、1080p、最佳画质，以及纯音频提取。

## 快速安装

告诉 OpenClaw：

> **"帮我安装这个 skill：https://clawhub.ai/XJouska/u2-downloader"**

OpenClaw 会自动引导你完成配置流程。

## 使用方式

安装完成后，直接用自然语言告诉 OpenClaw 你的需求，例如：

> "帮我保存这个视频：https://youtube.com/watch?v=dQw4w9WgXcQ"

> "把这个视频转成 1080p 离线版本：https://youtube.com/watch?v=xxxxx"

> "提取这个视频的音频：https://youtube.com/watch?v=xxxxx"

支持的画质选项：360p、480p、720p（默认）、1080p、最佳画质、纯音频。

## 接口说明

### POST /api/v1/skill/download

将在线视频保存为离线文件。

**请求体：**
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "resolution": "720"
}
```

**参数：**
- `youtube_url`（必填）：视频链接
- `resolution`（选填）：目标画质 — "360"、"480"、"720"、"1080"、"best"、"audio"，默认 "720"

**成功响应：**
```json
{
  "success": true,
  "download_url": "https://oss-bucket.aliyuncs.com/skill/abc123/video.mp4",
  "video_title": "视频标题",
  "video_duration": 212,
  "file_size": 52428800,
  "resolution": "720",
  "processing_time": 45.2
}
```

### GET /api/v1/skill/balance

查询账户状态。

**响应：**
```json
{
  "username": "user123"
}
```

### GET /api/v1/skill/health

健康检查接口。

**响应：**
```json
{
  "status": "healthy",
  "service": "在线视频离线保存工具",
  "version": "1.0.0"
}
```

### 错误码

| 状态码 | 含义 |
|--------|------|
| 200 | 成功 |
| 401 | 未授权 |
| 400 | 请求无效（链接格式错误等） |
| 500 | 服务器错误 |
