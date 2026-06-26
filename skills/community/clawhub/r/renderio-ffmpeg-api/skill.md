---
name: renderio-api
description: Use the RenderIO FFmpeg-as-a-Service API to process video, audio, and images in the cloud. Covers submitting commands, polling results, uploading files, chained workflows, and webhook delivery. Use this skill whenever the user wants to convert, resize, compress, trim, watermark, extract audio from, or otherwise process media via the RenderIO API.
allowed-tools: Read, Write, Edit, Bash, WebFetch
---

# RenderIO API Skill

RenderIO is an FFmpeg-as-a-Service REST API. You send an FFmpeg command over HTTP; RenderIO runs it in a secure cloud sandbox, stores outputs automatically, and returns signed download URLs.

## Setup

```bash
# Store API key as environment variable
export RENDERIO_API_KEY="ffsk_your_api_key_here"
```

Get a free API key at [renderio.dev/get-api-key](https://renderio.dev/get-api-key).

## The three rules that must never be broken

1. **Double braces for placeholders** — use `{{in_video}}` not `{in_video}`
2. **Key prefixes** — input keys start with `in_`, output keys start with `out_`
3. **Every key used in the command must be declared**, and every declared key must appear in the command

```json
// CORRECT
{
  "ffmpeg_command": "-i {{in_video}} -c:v libx264 {{out_video}}",
  "input_files": { "in_video": "https://example.com/video.mp4" },
  "output_files": { "out_video": "result.mp4" }
}

// WRONG — single braces, missing out_ prefix
{
  "ffmpeg_command": "-i {video} result.mp4",
  "input_files": { "video": "https://example.com/video.mp4" }
}
```

## Core workflow

### 1. Submit a command

```bash
curl -X POST https://renderio.dev/api/v1/run-ffmpeg-command \
  -H "X-API-KEY: $RENDERIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "ffmpeg_command": "-i {{in_video}} -vf scale=1280:720 -c:v libx264 -crf 23 {{out_video}}",
    "input_files": { "in_video": "https://example.com/input.mp4" },
    "output_files": { "out_video": "output-720p.mp4" }
  }'
```

Response: `{ "command_id": "a1b2c3d4-..." }`

### 2. Poll for completion

```bash
curl https://renderio.dev/api/v1/commands/$COMMAND_ID \
  -H "X-API-KEY: $RENDERIO_API_KEY"
```

Status values: `QUEUED` → `PROCESSING` → `SUCCESS` or `FAILED` (always uppercase).

### 3. Get output URL

```
result.output_files.out_video.storage_url
```

## TypeScript implementation

```typescript
const API_KEY = process.env.RENDERIO_API_KEY!;
const BASE = "https://api.renderio.dev";

interface CommandResult {
  command_id: string;
  status: "QUEUED" | "PROCESSING" | "SUCCESS" | "FAILED";
  output_files: Record<string, {
    storage_url: string;
    filename: string;
    size_mbytes: number;
    duration?: number;
    codec?: string;
    width?: number;
    height?: number;
  }>;
  total_processing_seconds?: number;
  error?: string;
}

async function runFFmpeg(
  command: string,
  inputFiles: Record<string, string>,
  outputFiles: Record<string, string>,
): Promise<CommandResult> {
  const submitRes = await fetch(`${BASE}/api/v1/run-ffmpeg-command`, {
    method: "POST",
    headers: { "X-API-KEY": API_KEY, "Content-Type": "application/json" },
    body: JSON.stringify({
      ffmpeg_command: command,
      input_files: inputFiles,
      output_files: outputFiles,
    }),
  });

  if (!submitRes.ok) {
    const err = await submitRes.json();
    throw new Error(`Submit failed: ${err.message}`);
  }

  const { command_id } = await submitRes.json();

  // Poll with 2s interval
  while (true) {
    await new Promise((r) => setTimeout(r, 2000));

    const pollRes = await fetch(`${BASE}/api/v1/commands/${command_id}`, {
      headers: { "X-API-KEY": API_KEY },
    });
    const result: CommandResult = await pollRes.json();

    if (result.status === "SUCCESS") return result;
    if (result.status === "FAILED") {
      throw new Error(`Processing failed: ${result.error ?? "unknown"}`);
    }
  }
}

// Usage
const result = await runFFmpeg(
  "-i {{in_video}} -vf scale=1280:720 -c:v libx264 -crf 23 {{out_video}}",
  { in_video: "https://example.com/input.mp4" },
  { out_video: "output-720p.mp4" },
);

console.log(result.output_files.out_video.storage_url);
```

## Python implementation

```python
import os
import time
import requests
from typing import Any

API_KEY = os.environ["RENDERIO_API_KEY"]
BASE = "https://api.renderio.dev"

def run_ffmpeg(
    command: str,
    input_files: dict[str, str],
    output_files: dict[str, str],
) -> dict[str, Any]:
    res = requests.post(
        f"{BASE}/api/v1/run-ffmpeg-command",
        headers={"X-API-KEY": API_KEY},
        json={
            "ffmpeg_command": command,
            "input_files": input_files,
            "output_files": output_files,
        },
    )
    res.raise_for_status()
    command_id = res.json()["command_id"]

    while True:
        time.sleep(2)
        result = requests.get(
            f"{BASE}/api/v1/commands/{command_id}",
            headers={"X-API-KEY": API_KEY},
        ).json()

        if result["status"] == "SUCCESS":
            return result
        if result["status"] == "FAILED":
            raise RuntimeError(f"Processing failed: {result.get('error', 'unknown')}")

# Usage
result = run_ffmpeg(
    "-i {{in_video}} -vf scale=1280:720 -c:v libx264 -crf 23 {{out_video}}",
    {"in_video": "https://example.com/input.mp4"},
    {"out_video": "output-720p.mp4"},
)
print(result["output_files"]["out_video"]["storage_url"])
```

## Common FFmpeg recipes

Copy-paste ready. Replace URLs and filenames.

### Convert MP4 to WebM
```json
{
  "ffmpeg_command": "-i {{in_video}} -c:v libvpx-vp9 -crf 30 -b:v 0 {{out_video}}",
  "input_files": { "in_video": "https://example.com/input.mp4" },
  "output_files": { "out_video": "output.webm" }
}
```

### Resize video to 720p
```json
{
  "ffmpeg_command": "-i {{in_video}} -vf scale=1280:720 -c:v libx264 -crf 23 {{out_video}}",
  "input_files": { "in_video": "https://example.com/input.mp4" },
  "output_files": { "out_video": "720p.mp4" }
}
```

### Extract audio as MP3
```json
{
  "ffmpeg_command": "-i {{in_video}} -vn -acodec libmp3lame -ab 192k {{out_audio}}",
  "input_files": { "in_video": "https://example.com/input.mp4" },
  "output_files": { "out_audio": "audio.mp3" }
}
```

### Compress video (reduce file size)
```json
{
  "ffmpeg_command": "-i {{in_video}} -c:v libx264 -crf 28 -preset slow {{out_video}}",
  "input_files": { "in_video": "https://example.com/input.mp4" },
  "output_files": { "out_video": "compressed.mp4" }
}
```

### Generate thumbnail at 5 seconds
```json
{
  "ffmpeg_command": "-i {{in_video}} -ss 5 -vframes 1 {{out_thumb}}",
  "input_files": { "in_video": "https://example.com/input.mp4" },
  "output_files": { "out_thumb": "thumbnail.jpg" }
}
```

### Trim video (10s to 30s)
```json
{
  "ffmpeg_command": "-i {{in_video}} -ss 10 -to 30 -c copy {{out_video}}",
  "input_files": { "in_video": "https://example.com/input.mp4" },
  "output_files": { "out_video": "trimmed.mp4" }
}
```

### Add image watermark
```json
{
  "ffmpeg_command": "-i {{in_video}} -i {{in_logo}} -filter_complex \"overlay=10:10\" {{out_video}}",
  "input_files": {
    "in_video": "https://example.com/input.mp4",
    "in_logo": "https://example.com/logo.png"
  },
  "output_files": { "out_video": "watermarked.mp4" }
}
```

### Convert to GIF (480px wide, 12fps)
```json
{
  "ffmpeg_command": "-i {{in_video}} -vf \"fps=12,scale=480:-1:flags=lanczos\" {{out_gif}}",
  "input_files": { "in_video": "https://example.com/input.mp4" },
  "output_files": { "out_gif": "output.gif" }
}
```

### Mute video (remove audio track)
```json
{
  "ffmpeg_command": "-i {{in_video}} -an -c:v copy {{out_video}}",
  "input_files": { "in_video": "https://example.com/input.mp4" },
  "output_files": { "out_video": "muted.mp4" }
}
```

### Stack two videos side by side
```json
{
  "ffmpeg_command": "-i {{in_left}} -i {{in_right}} -filter_complex \"[0:v][1:v]hstack=inputs=2\" {{out_video}}",
  "input_files": {
    "in_left": "https://example.com/left.mp4",
    "in_right": "https://example.com/right.mp4"
  },
  "output_files": { "out_video": "side-by-side.mp4" }
}
```

## Upload a local file first

When the user has a local file (not a URL), upload it first:

```typescript
async function uploadFile(filePath: string): Promise<string> {
  const form = new FormData();
  form.append("file", new Blob([await fs.readFile(filePath)]), path.basename(filePath));

  const res = await fetch("https://renderio.dev/api/v1/files/upload", {
    method: "POST",
    headers: { "X-API-KEY": API_KEY },
    body: form,
  });

  const data = await res.json();
  return data.storage_url; // use this as the input_files value
}
```

## Chained commands (sequential pipeline)

Use the output of one step as the input of the next. Reference previous outputs with `{{out_key}}` in the next step's `input_files`.

```json
POST /api/v1/run-chained-ffmpeg-commands
{
  "commands": [
    {
      "ffmpeg_command": "-i {{in_video}} -vf scale=1280:720 {{out_resized}}",
      "input_files": { "in_video": "https://example.com/input.mp4" },
      "output_files": { "out_resized": "resized.mp4" }
    },
    {
      "ffmpeg_command": "-i {{in_resized}} -c:v libx264 -crf 28 {{out_final}}",
      "input_files": { "in_resized": "{{out_resized}}" },
      "output_files": { "out_final": "final.mp4" }
    }
  ]
}
```

## Parallel commands (multiple independent operations)

```json
POST /api/v1/run-multiple-ffmpeg-commands
{
  "commands": [
    {
      "ffmpeg_command": "-i {{in_video}} -vf scale=1920:1080 {{out_1080p}}",
      "input_files": { "in_video": "https://example.com/input.mp4" },
      "output_files": { "out_1080p": "1080p.mp4" }
    },
    {
      "ffmpeg_command": "-i {{in_video}} -vf scale=1280:720 {{out_720p}}",
      "input_files": { "in_video": "https://example.com/input.mp4" },
      "output_files": { "out_720p": "720p.mp4" }
    }
  ]
}
```

## Webhook setup (alternative to polling)

```bash
# Configure once
curl -X PUT https://renderio.dev/api/v1/webhook-config \
  -H "X-API-KEY: $RENDERIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://your-server.com/renderio-webhook"}'

# Payload your endpoint receives on completion:
# {
#   "data": {
#     "command_id": "...",
#     "status": "SUCCESS",
#     "output_files": { "out_video": { "storage_url": "...", ... } }
#   },
#   "timestamp": 1712345678000
# }
```

## Error reference

| Code | Meaning | Fix |
|---|---|---|
| `400` | Bad request | Check placeholder syntax and key prefixes |
| `401` | Unauthorized | Check `X-API-KEY` header and key validity |
| `429` | Rate limited | Wait `Retry-After` seconds and retry |
| `404` | Not found | Check `command_id` or `file_id` |
| `500` | Server error | Safe to retry after a short delay |

## Checklist when generating code for users

- [ ] `RENDERIO_API_KEY` stored as environment variable, never hardcoded
- [ ] Placeholder syntax uses `{{double_braces}}`
- [ ] Input keys start with `in_`, output keys start with `out_`
- [ ] Poll loop handles `QUEUED`, `PROCESSING`, `SUCCESS`, `FAILED`
- [ ] Output URL accessed via `output_files.out_key.storage_url`
- [ ] Error handling for both HTTP errors and `FAILED` status
- [ ] Domain is `api.renderio.dev` (not any other domain)
