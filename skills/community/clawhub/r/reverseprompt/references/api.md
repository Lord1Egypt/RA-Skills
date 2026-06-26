# Video Reverse Prompt API Reference

## Endpoint

```
POST https://nanophoto.ai/api/sora-2/reverse-prompt
```

## Authentication

```
Authorization: Bearer YOUR_API_KEY
```

Obtain API key at: https://nanophoto.ai/settings/apikeys

For OpenClaw users, the recommended setup is to configure the skill with:

- `env.NANOPHOTO_API_KEY=YOUR_API_KEY`

## Credits

**1 credit** per analysis (API calls only; web interface is free).

## Request Body

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `videoSource` | string | Yes | Video source type: `youtube`, `url`, or `file` |
| `locale` | string | No | Output language (default: `en`). Supported: `en`, `zh`, `zh-TW`, `ja`, `ko`, `es`, `fr`, `de`, `pt`, `ru`, `ar` |
| `videoUrl` | string | Conditional | YouTube link (when `videoSource` is `youtube`) or direct .mp4 URL (when `videoSource` is `url`) |
| `videoFile` | string | Conditional | Base64-encoded video file (required when `videoSource` is `file`) |
| `videoFileName` | string | No | Original filename for uploaded videos |

## File Upload Notes

- Only `.mp4` format is supported
- Maximum file size: **30 MB** (before Base64 encoding)
- `videoFile` accepts plain Base64 string or Data URL (`data:video/mp4;base64,...`)
- For local files, prefer the bundled `scripts/reverse_prompt_file.py` helper instead of embedding multi-megabyte base64 directly in the shell.

## Response Format

**Streaming text response** (`Content-Type: text/plain; charset=utf-8`)

The AI analysis is streamed as generated, containing a detailed shot breakdown in Markdown table format:

- Shot number, framing/angle, camera movement
- Detailed visual description
- Audio analysis (BGM, sound effects, narration)
- Duration per shot
- Overall summary

## Error Response

```json
{
  "success": false,
  "error": "Error description",
  "errorCode": "ERROR_CODE"
}
```

## Error Codes

| errorCode | HTTP Status | Description |
|-----------|-------------|-------------|
| `LOGIN_REQUIRED` | 401 | Authentication required |
| `API_KEY_RATE_LIMIT_EXCEEDED` | 429 | Rate limit exceeded |
| `INSUFFICIENT_CREDITS` | 402 | Not enough credits |
| `INVALID_INPUT` | 400 | Missing required parameters |
| `INVALID_YOUTUBE_URL` | 400 | Invalid YouTube URL |
| `INVALID_VIDEO_URL` | 400 | Invalid video URL |
| `INVALID_FORMAT` | 400 | Invalid MP4 format |
| `FILE_TOO_LARGE` | 400 | File exceeds 30MB |
| `VIDEO_DOWNLOAD_FAILED` | 400 | Video download failed |
| `VIDEO_PROCESSING_FAILED` | 422 | Video processing failed |
| `AI_SERVICE_ERROR` | 503 | AI service unavailable |
| `SERVICE_UNAVAILABLE` | 503 | Service configuration issue |
| `INTERNAL_ERROR` | 500 | Internal server error |

## Example: TypeScript (File Upload with Streaming)

```ts
import { readFile } from "node:fs/promises";

const videoBuffer = await readFile("your-video.mp4");
const videoBase64 = videoBuffer.toString("base64");

const response = await fetch("https://nanophoto.ai/api/sora-2/reverse-prompt", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: "Bearer YOUR_API_KEY",
  },
  body: JSON.stringify({
    videoSource: "file",
    locale: "en",
    videoFile: videoBase64,
    videoFileName: "your-video.mp4",
  }),
});

const reader = response.body!.getReader();
const decoder = new TextDecoder();

while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  process.stdout.write(decoder.decode(value));
}
```
