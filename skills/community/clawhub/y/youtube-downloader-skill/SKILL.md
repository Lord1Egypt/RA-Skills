---
name: youtube-downloader
description: Download YouTube videos by URL in various resolutions using a pay-per-use API with credit-based authentication and no charge on failed downloads. Use when users request to download YouTube videos, extract audio, or specify resolution requirements (360p, 480p, 720p, 1080p, best quality). Triggers on phrases like "download YouTube video", "download from YouTube", "save YouTube video", "extract YouTube audio", "download video in [resolution]".
---

# YouTube Video Downloader Skill

Download any YouTube video in various resolutions with a simple command. Supports 360p, 480p, 720p, 1080p, best quality, and audio-only extraction.

## Quick Install

Just tell OpenClaw:

"Help me install this skill: https://clawhub.ai/jxyyjm/youtube-downloader-skill"

OpenClaw will ask you for an **API Key**. Follow these steps to get one:

- Go to https://skill.lordest.cn and register an account
- Navigate to the **API Keys** page (or visit https://skill.lordest.cn/?page=apikeys)
- Click **Generate** to create your API Key (format: `sk-yt-xxxxx`)
- Copy the key and paste it to OpenClaw when prompted

That's it! You're ready to use the skill.

## Usage

Once installed, just tell OpenClaw what you want. For example:

"Download this YouTube video: https://youtube.com/watch?v=dQw4w9WgXcQ"

"Download this video in 1080p: https://youtube.com/watch?v=xxxxx"

"Extract audio from this video: https://youtube.com/watch?v=xxxxx"

Supported resolutions: 360p, 480p, 720p (default), 1080p, best, audio-only.

## Authentication

All API calls require an API Key in the Authorization header:

```
Authorization: Bearer sk-yt-xxxxx
```

Get your API Key at: https://skill.lordest.cn/?page=apikeys

## Endpoints

### POST /api/v1/download

Download a YouTube video.

**Request:**

```json
{
  "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "resolution": "720"
}
```

**Parameters:**

- `youtube_url` (required): YouTube video URL
- `resolution` (optional): "360", "480", "720", "1080", "best", "audio". Default: "720"

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

### GET /api/v1/balance

Check account status.

**Response:**

```json
{
  "username": "user123"
}
```

### GET /health

Health check (no authentication required).

**Response:**

```json
{
  "status": "healthy",
  "service": "YouTube Video Downloader Service",
  "version": "1.0.0"
}
```

## Error Codes

| Code | Meaning |
|---|---|
| 200 | Success |
| 401 | Invalid or missing API Key |
| 400 | Invalid request (bad URL, etc.) |
| 500 | Server error |

## Example (curl)

```bash
# Download a video
curl -X POST https://skill.lordest.cn/api/v1/download \
  -H "Authorization: Bearer sk-yt-xxxxx" \
  -H "Content-Type: application/json" \
  -d '{"youtube_url": "https://youtube.com/watch?v=dQw4w9WgXcQ", "resolution": "720"}'
```

## Example (Python)

```python
import requests

API_KEY = "sk-yt-xxxxx"
BASE_URL = "https://skill.lordest.cn"

# Download
resp = requests.post(
    f"{BASE_URL}/api/v1/download",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={"youtube_url": "https://youtube.com/watch?v=dQw4w9WgXcQ", "resolution": "720"}
)
data = resp.json()
if data["success"]:
    print(f"Download URL: {data['download_url']}")
```