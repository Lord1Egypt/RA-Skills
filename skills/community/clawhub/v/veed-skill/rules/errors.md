---
name: errors
description: Error handling, input validation, and troubleshooting for VEED Fabric video generation
metadata:
  tags: errors, validation, troubleshooting, formats
---

# Error Handling

## Input validation

Run these checks **before** making any API calls:

### FAL_KEY

```bash
if [ -z "$FAL_KEY" ]; then
  echo "FAL_KEY not set"
fi
```

If missing, show setup instructions and stop. See SKILL.md prerequisites.

### Image format

Supported: **JPG, JPEG, PNG, WebP, GIF, AVIF**

Check the file extension (case-insensitive). If unsupported:
> Unsupported image format: {extension}. Supported formats: JPG, JPEG, PNG, WebP, GIF, AVIF

### Audio format (lip-sync path only)

Supported: **MP3, OGG, WAV, M4A, AAC**

If unsupported:
> Unsupported audio format: {extension}. Supported formats: MP3, OGG, WAV, M4A, AAC

### Text length (text-to-video path only)

- Minimum: 1 character
- Maximum: 2000 characters

If empty:
> Please provide a script for the video.

If over 2000:
> Your script is {length} characters ({length - 2000} over the 2000-character limit, roughly 30–45 seconds of speech). Please shorten it or split into multiple videos.

### Local file existence

Before uploading, verify the file exists:
```bash
if [ ! -f "$FILE_PATH" ]; then
  echo "File not found: $FILE_PATH"
fi
```

## API errors

The fal.ai API returns errors as JSON:
```json
{
  "detail": "Error message here"
}
```

Common errors:

| Error | Likely cause | Action |
|---|---|---|
| 401 Unauthorized | Invalid or expired FAL_KEY | Ask user to check their key at https://fal.ai/dashboard/keys |
| 422 Validation Error | Bad input (wrong format, missing field) | Show the error detail, check inputs match spec |
| 429 Rate Limited | Too many requests | Wait and retry, or tell user to try again shortly |
| 500 Server Error | fal.ai issue | Retry once. If it persists, tell user to try again later |

## Upload errors

If file upload initiation fails, check:
1. `FAL_KEY` is valid
2. Internet connection is working
3. The file exists and is readable

If the PUT to presigned URL fails, the URL may have expired. Re-initiate the upload.

## Generation timeout

If polling exceeds 5 minutes without completion, provide the request ID and stop:
> Generation is taking longer than expected. Your request ID is: {request_id}

**MUST NOT** poll indefinitely. **MUST NOT** silently fail.
