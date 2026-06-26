---
name: tmpfiles-upload
description: |
  Upload files (images, PDFs, documents) to tmpfiles.org and send download links via messaging platforms.
  Use when: (1) User asks to send screenshots/files via Feishu/other platforms, (2) Direct file upload to messaging platform fails,
  (3) User needs a temporary file sharing solution with auto-expiring links.
---

# tmpfiles.org File Upload

Upload files to tmpfiles.org (temporary file hosting) and get a download link.

## When to Use

- Sending screenshots to Feishu when direct upload fails
- Sharing files temporarily (links expire after ~1 hour)
- Quick file sharing without authentication

## Upload Script

```python
import requests

def upload_to_tmpfiles(file_path):
    """Upload file to tmpfiles.org and return download URL"""
    with open(file_path, 'rb') as f:
        r = requests.post('https://tmpfiles.org/api/v1/upload', files={'file': f})
        data = r.json()
        if data.get('status') == 'success':
            # Replace org/ with org/dl/ for direct download
            return data['data']['url'].replace('org/', 'org/dl/')
        raise Exception(f"Upload failed: {data}")
```

## Usage in OpenClaw

### Step 1: Capture screenshot (if needed)
```bash
/usr/sbin/screencapture -x ~/Desktop/screenshot.png
```

### Step 2: Upload to tmpfiles.org
```bash
python3 -c "
import requests
with open('/path/to/file.png', 'rb') as f:
    r = requests.post('https://tmpfiles.org/api/v1/upload', files={'file': f})
    d = r.json()
    if d.get('status') == 'success':
        print(d['data']['url'].replace('org/', 'org/dl/'))
"
```

### Step 3: Send link via message
```json
{
  "action": "send",
  "channel": "feishu",
  "message": "文件链接：https://tmpfiles.org/dl/xxx",
  "target": "user_id"
}
```

## Notes

- Links expire after ~1 hour
- Max file size: ~100MB
- Files are publicly accessible while active
- Not suitable for sensitive/permanent storage
