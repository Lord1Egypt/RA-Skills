---
name: sts-upload
description: Upload files to Aliyun OSS using STS temporary credentials via the VectCut backend. Use this skill whenever the user wants to upload a file, video, image, or any asset to OSS/cloud storage, mentions STS upload, or needs a public signed URL for an uploaded file. Also trigger when the user says "upload this to the server", "put this file online", "get me a URL for this file", or similar upload-related requests.
---

# STS Upload Skill

Upload files to Aliyun OSS through a three-step STS (Security Token Service) workflow provided by the VectCut backend.

## When to use

- User wants to upload any file (video, image, document, etc.) to cloud storage
- User needs a public signed URL for a local file
- User mentions STS, OSS, or cloud upload in the context of this project

## Workflow

The upload is a three-step process. Execute each step in order using the bundled script.

### Prerequisites

- Python 3 with `requests` library installed
- Check `VECTCUT_API_KEY` before execution; if missing, call `vectcut-login` first and continue only after login succeeds
- Network access to the backend and OSS endpoints

### Execution

Run the upload script with the target file path:

```bash
python <skill-path>/scripts/sts_upload.py "<file_path>"
```

The script only accepts a single argument: the file path. Authentication is handled via the `VECTCUT_API_KEY` environment variable.

### What the script does

1. **Init** — `POST /sts/upload/init` with file name and size. The backend returns temporary STS credentials (`AccessKeyId`, `AccessKeySecret`, `SecurityToken`), a `bucket_name`, and an `object_key`.

2. **Upload to OSS** — Signs a PUT request using HMAC-SHA1 over the STS credentials and uploads the file directly to `https://{bucket_name}.{oss_endpoint}/{object_key}`.

3. **Complete** — `POST /sts/upload/complete` with the `object_key`. The backend finalizes the upload and returns a `public_signed_url`.

### Output

The script prints a JSON object on success:

```json
{
  "base_url": "https://open.vectcut.com",
  "bucket_name": "...",
  "local_file": "/path/to/file",
  "object_key": "...",
  "file_size": 12345,
  "public_signed_url": "https://..."
}
```

The `public_signed_url` is the key result — it's the publicly accessible URL for the uploaded file.

### File management

After uploading, you can visit https://www.vectcut.com/materials to visually manage your uploaded files.

### Error handling

- If `VECTCUT_API_KEY` is not set, call `vectcut-login` first, then rerun this skill
- If the file doesn't exist, the script exits with a `FileNotFoundError`
- If any API call fails, the script exits with an error message indicating which step failed and the HTTP status code
- Common issues: expired API key, network connectivity, file too large

### Configuration

| Parameter | Source | Value |
|-----------|--------|-------|
| API Key | Env var `VECTCUT_API_KEY` | (required) |
| Backend URL | Hardcoded | `https://open.vectcut.com` |
| OSS endpoint | Hardcoded | `oss-cn-hangzhou.aliyuncs.com` |
