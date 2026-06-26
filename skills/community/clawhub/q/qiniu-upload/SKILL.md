---
name: qiniu-upload
description: Upload local files to Qiniu Cloud and return a publicly accessible URL (or signed private URL). Use when the user wants to upload a local file path to Qiniu, obtain a CDN/public URL, prepare files for downstream cloud processing, or convert local audio/video/documents into externally accessible URLs for other skills such as speech transcription.
homepage: https://www.qiniu.com/
metadata: {"clawdbot":{"emoji":"☁️","requires":{"env":["QINIU_ACCESS_KEY","QINIU_SECRET_KEY","QINIU_BUCKET","QINIU_DOMAIN"]},"tags":["cloud","storage","cdn","upload"]}}
---

# Qiniu Upload

Use this skill when a task needs a local file turned into a Qiniu-hosted URL.

## Required environment variables

- `QINIU_ACCESS_KEY`
- `QINIU_SECRET_KEY`
- `QINIU_BUCKET`
- `QINIU_DOMAIN`

Optional:

- `QINIU_ZONE` - one of `z0`, `z1`, `z2`, `na0`, `as0`
- `QINIU_PRIVATE_BUCKET` - `true` to emit signed private URLs by default
- `QINIU_PRIVATE_EXPIRE_SECONDS` - default expiry for private URLs

## Safety rules

- Never hardcode Qiniu credentials.
- Fail fast if any required environment variable is missing.
- Prefer returning both `key` and final `url`.
- For local files, verify the path exists before upload.

## Primary command

Run the Node script:

```powershell
node scripts/upload.js --file-path "E:\\audio\\sample.mp3" --prefix audio
```

Optional flags:

- `--private` - return a signed private URL
- `--expire-seconds 3600` - private URL expiry
- `--prefix audio` - object key prefix
- `--key my/custom/name.mp3` - explicit object key
- `--json` - machine-friendly JSON only

## Output contract

The script returns JSON like:

```json
{
  "success": true,
  "bucket": "example-bucket",
  "key": "audio/uuid.mp3",
  "url": "https://cdn.example.com/audio/uuid.mp3",
  "isPrivate": false,
  "size": 12345,
  "mimeType": "audio/mpeg",
  "sourcePath": "E:\\audio\\sample.mp3"
}
```

## Domain and access caveat

Some Qiniu domains may sit behind auth or anti-leeching. Upload success does not automatically guarantee anonymous public fetch success. If downstream services need to fetch the object, verify the returned URL is externally accessible, or use private signed URLs / a proper public CDN domain.

## Chaining to other skills

After upload succeeds, pass the returned `url` into downstream skills such as an Aliyun speech transcription workflow.
