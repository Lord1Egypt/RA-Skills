---
name: file-upload
description: Upload local files to fal.ai CDN to get publicly accessible URLs for use with the Fabric API
metadata:
  tags: upload, cdn, local-file, storage, fal
---

# Uploading Local Files

The Fabric API requires publicly accessible URLs for image and audio inputs. When the user provides a local file path, upload it to fal.ai's CDN first.

## Detecting local files

A local file path is anything that is NOT a URL (does not start with `http://` or `https://`). Examples:
- `./headshot.png` — local
- `/Users/matt/photos/me.jpg` — local
- `headshot.png` — local
- `https://example.com/photo.jpg` — URL, no upload needed

**MUST** check if the file exists before attempting upload. If it does not exist, tell the user:
> File not found: {path}. Please check the path and try again.

## Upload flow

The upload is a two-step process using fal.ai's CDN presigned URL mechanism:

### Step 1: Initiate upload

Request a presigned upload URL:

```bash
CONTENT_TYPE=$(file --mime-type -b "/path/to/local/file.png")
FILE_NAME=$(basename "/path/to/local/file.png")

UPLOAD_RESPONSE=$(curl -s -X POST "https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"content_type\": \"$CONTENT_TYPE\", \"file_name\": \"$FILE_NAME\"}")
```

The response contains:
```json
{
  "file_url": "https://v3.fal.media/files/abc/xyz.png",
  "upload_url": "https://storage.googleapis.com/..."
}
```

### Step 2: Upload file data

PUT the file to the presigned URL:

```bash
FILE_URL=$(echo "$UPLOAD_RESPONSE" | jq -r '.file_url')
UPLOAD_URL=$(echo "$UPLOAD_RESPONSE" | jq -r '.upload_url')

curl -s -X PUT "$UPLOAD_URL" \
  -H "Content-Type: $CONTENT_TYPE" \
  --data-binary @"/path/to/local/file.png"
```

### Step 3: Use the CDN URL

`FILE_URL` (e.g., `https://v3.fal.media/files/abc/xyz.png`) is now publicly accessible and can be used as `image_url` or `audio_url` in API calls.

## Complete example

Upload a local headshot and use it:

```bash
# Upload
CONTENT_TYPE=$(file --mime-type -b "./headshot.png")
FILE_NAME=$(basename "./headshot.png")

UPLOAD_RESPONSE=$(curl -s -X POST "https://rest.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"content_type\": \"$CONTENT_TYPE\", \"file_name\": \"$FILE_NAME\"}")

IMAGE_URL=$(echo "$UPLOAD_RESPONSE" | jq -r '.file_url')
UPLOAD_URL=$(echo "$UPLOAD_RESPONSE" | jq -r '.upload_url')

curl -s -X PUT "$UPLOAD_URL" \
  -H "Content-Type: $CONTENT_TYPE" \
  --data-binary @"./headshot.png"

# Now use IMAGE_URL in the Fabric API call
echo "Uploaded: $IMAGE_URL"
```

## Error handling

- If the initiate request fails (non-200), check `FAL_KEY` is valid and internet is connected
- If the PUT upload fails, retry once — presigned URLs are single-use, so re-initiate if the URL expired
- **MUST NOT** send local file paths directly to the Fabric API — they will fail
