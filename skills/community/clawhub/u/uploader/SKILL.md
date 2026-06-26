---
name: uploader
description: "Upload a local file to Astron Claw Bridge and return a public download URL."
---

# uploader

Upload a local file to Astron Claw Bridge Server and return a publicly accessible download URL. Supports images, audio, video, documents and other file types.

## When to Use

✅ **USE this skill when:**

- When the user wants to obtain the file.
- When the user needs a download URL for a local file (image, audio, video, document, etc.).
- When the user wants to generate an external link for embedding in markdown or web pages.

## When NOT to Use

❌ **DON'T use this skill when:**

- When the user only wants to read or view a local file without uploading.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| file | string | Yes | Absolute or relative path to the local file to upload |
| --session-id | string | No | Optional session ID for the upload |

## Commands

### Basic Call

```bash
python3 scripts/upload_media.py '/path/to/file.png'
```

### With Session ID

```bash
python3 scripts/upload_media.py '/path/to/file.png' --session-id 'my-session'
```

## Examples

**"Help me upload this image and get a link."**

```bash
python3 scripts/upload_media.py './screenshot.png'
```

**"Upload this PDF document."**

```bash
python3 scripts/upload_media.py './report.pdf'
```

## Response

Script outputs upload result to stdout:

```
fileName:    screenshot.png
mimeType:    image/png
fileSize:    102400
sessionId:   abc123
downloadUrl: http://.../<path>/<filename>
```

## Notes

- Host and token are auto-read from `/root/.openclaw/openclaw.json`, no need to pass at runtime
- Requires `requests` package: `pip install requests`
