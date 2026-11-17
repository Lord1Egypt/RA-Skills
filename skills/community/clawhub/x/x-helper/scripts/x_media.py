"""
X Helper — Media upload (images, video, GIF).
INIT → APPEND → FINALIZE protocol. Pure stdlib, no dependencies.
"""

import json
import os
import sys
import time
import urllib.request
import urllib.parse
from urllib.error import URLError

MEDIA_UPLOAD_URL = "https://api.x.com/2/media/upload"
FILE_SIZE_LIMIT_SIMPLE = 5 * 1024 * 1024  # 5 MB for simple upload
MAX_RETRIES = 5
POLL_INTERVAL = 2


def _guess_media_category(filename, content_type):
    ext = os.path.splitext(filename)[1].lower()
    if ext in ('.gif',):
        return "TWEET_GIF"
    elif content_type.startswith("video/"):
        return "TWEET_VIDEO"
    else:
        return "TWEET_IMAGE"


def _mime_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    mime_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".mp4": "video/mp4",
        ".mov": "video/quicktime",
        ".avi": "video/x-msvideo",
    }
    return mime_map.get(ext, "application/octet-stream")


def _build_multipart(fields, file_field, filename, file_data, content_type):
    boundary = os.urandom(16).hex()
    body_parts = []
    for key, value in fields.items():
        body_parts.append(f"--{boundary}\r\n")
        body_parts.append(f'Content-Disposition: form-data; name="{key}"\r\n\r\n')
        body_parts.append(f"{value}\r\n")
    body_parts.append(f"--{boundary}\r\n")
    body_parts.append(f'Content-Disposition: form-data; name="{file_field}"; filename="{filename}"\r\n')
    body_parts.append(f"Content-Type: {content_type}\r\n\r\n")
    body = "".join(body_parts).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")
    return body, boundary


def _req(url, data, headers, method="POST"):
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except URLError as e:
        body = b""
        try:
            body = e.read()
        except Exception:
            pass
        try:
            err = json.loads(body.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            err = {"detail": body.decode(errors="replace")}
        err["http_code"] = getattr(e, "code", 0)
        err["error"] = True
        return err


def _req_form(url, fields, token, method="POST"):
    data = urllib.parse.urlencode(fields).encode()
    return _req(url, data, {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    }, method)


def _init_upload(total_bytes, media_category, content_type, token):
    return _req_form(MEDIA_UPLOAD_URL, {
        "command": "INIT",
        "total_bytes": str(total_bytes),
        "media_type": content_type,
        "media_category": media_category,
    }, token)


def _append_upload(media_id, segment_index, file_data, filename, content_type, token):
    fields = {"command": "APPEND", "media_id": media_id, "segment_index": str(segment_index)}
    body, boundary = _build_multipart(fields, "media", filename, file_data, content_type)
    return _req(MEDIA_UPLOAD_URL, body, {
        "Authorization": f"Bearer {token}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    })


def _finalize_upload(media_id, token):
    return _req_form(MEDIA_UPLOAD_URL, {"command": "FINALIZE", "media_id": media_id}, token)


def _status_upload(media_id, token):
    qs = urllib.parse.urlencode({"command": "STATUS", "media_id": media_id})
    return _req(f"{MEDIA_UPLOAD_URL}?{qs}", None, {"Authorization": f"Bearer {token}"}, "GET")


def upload(filepath, token):
    """Upload a media file. Returns media_id string or exits with error.

    ⚠️  Token is passed in memory (not via CLI), safe from process-listing
        exposure. The token is used only for X API authentication. All data
        (file content, token) is transmitted to api.x.com over HTTPS.
    """
    if not os.path.isfile(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    filename = os.path.basename(filepath)
    content_type = _mime_type(filename)
    media_category = _guess_media_category(filename, content_type)

    with open(filepath, "rb") as f:
        file_data = f.read()

    total_bytes = len(file_data)
    is_video = content_type.startswith("video/") or media_category == "TWEET_GIF"
    use_chunked = is_video or total_bytes > FILE_SIZE_LIMIT_SIMPLE

    if use_chunked:
        result = _init_upload(total_bytes, media_category, content_type, token)
        if result.get("error"):
            print(f"Error: INIT failed: {result.get('detail', str(result))}", file=sys.stderr)
            sys.exit(1)
        media_id = result["media_id"]
        result = _append_upload(media_id, 0, file_data, filename, content_type, token)
        if result.get("error"):
            print(f"Error: APPEND failed: {result.get('detail', str(result))}", file=sys.stderr)
            sys.exit(1)
        result = _finalize_upload(media_id, token)
        if result.get("error"):
            print(f"Error: FINALIZE failed: {result.get('detail', str(result))}", file=sys.stderr)
            sys.exit(1)
        # Poll for video processing
        if content_type.startswith("video/"):
            for _ in range(MAX_RETRIES):
                s = _status_upload(media_id, token)
                state = s.get("processing_info", {}).get("state", "")
                pct = s.get("processing_info", {}).get("progress_percent", 0)
                if state == "succeeded":
                    print(f"  Video processed 100%", file=sys.stderr)
                    break
                elif state == "failed":
                    err = s.get("processing_info", {}).get("error", {})
                    print(f"Error: video processing failed: {err}", file=sys.stderr)
                    sys.exit(1)
                print(f"  Video processing: {pct}%", file=sys.stderr)
                time.sleep(POLL_INTERVAL)
    else:
        # Simple upload (single multipart, no INIT/APPEND/FINALIZE)
        fields = {"media_category": media_category}
        body, boundary = _build_multipart(fields, "media", filename, file_data, content_type)
        result = _req(MEDIA_UPLOAD_URL, body, {
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        })
        if result.get("error"):
            print(f"Error: upload failed: {result.get('detail', str(result))}", file=sys.stderr)
            sys.exit(1)
        media_id = result.get("media_id", "")

    return media_id


def main():
    """CLI entry point (kept for backward compat, subprocess callers should migrate to import)."""
    if len(sys.argv) < 2:
        print("Usage: python3 x_media.py <filepath> [token]", file=sys.stderr)
        print("Note: token as CLI arg exposes it in process listings.", file=sys.stderr)
        print("Prefer: from x_media import upload; media_id = upload(path, token)", file=sys.stderr)
        sys.exit(1)
    filepath = sys.argv[1]
    token = ""
    if len(sys.argv) >= 3:
        token = sys.argv[2]
    else:
        # Token comes only from the user-set X_BEARER_TOKEN env var.
        token = os.environ.get("X_BEARER_TOKEN", "").strip()
    media_id = upload(filepath, token)
    print(media_id)


if __name__ == "__main__":
    main()
