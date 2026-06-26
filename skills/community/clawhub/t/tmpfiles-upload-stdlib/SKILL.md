---
name: tmpfiles-upload-stdlib
description: Upload a local file to tmpfiles.org using Python standard library only, then return a direct download link in strict JSON.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📤"
    os:
      - linux
    homepage: https://tmpfiles.org
---

# Tmpfiles Upload (Standard Library)

Use this skill when the user wants to upload a **local file that already exists in the OpenClaw workspace or container** and receive a **temporary public download link**.

This skill is for:
- uploading a file from a known local path
- returning a temporary download link
- producing machine-friendly output for workflows such as n8n

This skill is **not** for:
- downloading files from remote URLs first
- handling private or sensitive documents
- long-term or secure file storage
- inventing file paths that do not exist

## Safety and scope

Before uploading, always check the following:

1. The file path is explicitly provided by the user or clearly available in context.
2. The file exists locally.
3. The file is not obviously sensitive, unless the user clearly asked to upload it anyway.
4. The user understands the link is temporary and public.

Never upload:
- secrets, credentials, tokens, key files
- private IDs, tax records, contracts, or financial files unless the user explicitly insists
- arbitrary system files outside the task scope

If the file appears sensitive, warn the user briefly before proceeding.

## Required input

You need:
- a local file path, such as `/root/.openclaw/workspace-default/report.pdf`

If no local file path is available, ask for it or explain that the file must already exist locally in the workspace/container.

## Output format

Always return **strict JSON only** with no markdown and no extra commentary.

Success format:
```json
{
  "success": true,
  "file_path": "/root/.openclaw/workspace-default/report.pdf",
  "file_name": "report.pdf",
  "download_url": "https://tmpfiles.org/xxxxxxxx/report.pdf",
  "note": "Temporary public link generated."
}
```

Failure format:
```json
{
  "success": false,
  "file_path": "/root/.openclaw/workspace-default/report.pdf",
  "error": "File not found"
}
```

## Procedure

Follow these steps exactly:

1. Confirm the local file path.
2. Check whether the file exists.
3. Upload the file to tmpfiles.org using Python standard library only.
4. Extract the returned URL.
5. Return strict JSON only.

## Python upload method

Use `python3` and standard library modules only.

Preferred approach:
- `os` for file checks
- `mimetypes` for content type guess if needed
- `urllib.request` and `uuid` for multipart upload
- `json` for parsing response

Use a one-shot Python command or heredoc script.

### Reference implementation

```bash
python3 <<'PY'
import os
import json
import uuid
import mimetypes
import urllib.request

file_path = "/absolute/path/to/file.ext"

if not os.path.isfile(file_path):
    print(json.dumps({
        "success": False,
        "file_path": file_path,
        "error": "File not found"
    }))
    raise SystemExit(0)

file_name = os.path.basename(file_path)
mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
boundary = "----WebKitFormBoundary" + uuid.uuid4().hex

with open(file_path, "rb") as f:
    file_bytes = f.read()

body = []
body.append(f"--{boundary}\r\n".encode())
body.append(
    f'Content-Disposition: form-data; name="file"; filename="{file_name}"\r\n'.encode()
)
body.append(f"Content-Type: {mime_type}\r\n\r\n".encode())
body.append(file_bytes)
body.append(f"\r\n--{boundary}--\r\n".encode())

data = b"".join(body)

req = urllib.request.Request(
    "https://tmpfiles.org/api/v1/upload",
    data=data,
    headers={
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Accept": "application/json"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    parsed = json.loads(raw)

    download_url = None
    if isinstance(parsed, dict):
        data_obj = parsed.get("data", {})
        if isinstance(data_obj, dict):
            download_url = data_obj.get("url")

    if download_url:
        print(json.dumps({
            "success": True,
            "file_path": file_path,
            "file_name": file_name,
            "download_url": download_url,
            "note": "Temporary public link generated."
        }))
    else:
        print(json.dumps({
            "success": False,
            "file_path": file_path,
            "error": "Upload response did not include a download URL",
            "raw_response": parsed
        }))
except Exception as e:
    print(json.dumps({
        "success": False,
        "file_path": file_path,
        "error": str(e)
    }))
PY
```

## Execution rules

- Replace `/absolute/path/to/file.ext` with the real local file path.
- Do not use `requests`.
- Do not return prose before or after the JSON.
- Prefer a single final JSON object.
- If upload fails, return the failure JSON.
- If the file is missing, do not attempt upload.

## When to decline

Decline or warn when:
- the file path is missing
- the file does not exist
- the file is likely sensitive and public upload would be risky
- the user asks for secure/private hosting instead of a public temporary link

In those cases, suggest using private storage such as S3 or Supabase instead.
