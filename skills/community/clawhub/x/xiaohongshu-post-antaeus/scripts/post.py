#!/usr/bin/env python3
"""
Xiaohongshu (小红书) note posting script.

Supports:
- API posting when XIAOHONGSHU_APP_KEY and XIAOHONGSHU_APP_SECRET are set
- Draft-only mode (output content for manual copy-paste) when no credentials
"""

import argparse
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlencode

BASE_URL = "https://open.xiaohongshu.com"
TIMEOUT = 30


def get_proxy():
    """Return proxy dict for requests if env vars set."""
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
    if proxy:
        return {"http": proxy, "https": proxy}
    return None


def http_post(url: str, data: dict | None = None, json_body: dict | None = None, headers: dict | None = None) -> dict:
    """POST request using urllib (no extra deps)."""
    req_headers = {"Content-Type": "application/json", **(headers or {})}
    body = None
    if json_body is not None:
        body = json.dumps(json_body).encode("utf-8")
    elif data:
        body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=req_headers, method="POST")
    proxy = get_proxy()
    if proxy:
        proxy_url = proxy.get("https") or proxy.get("http")
        req.set_proxy(proxy_url.replace("https://", "http://") if proxy_url else "", "https")

    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def http_upload(url: str, file_path: Path, token: str) -> dict:
    """Upload file via multipart/form-data (PUT as per some docs)."""
    import mimetypes

    content_type, _ = mimetypes.guess_type(str(file_path))
    content_type = content_type or "application/octet-stream"
    with open(file_path, "rb") as f:
        file_data = f.read()

    boundary = "----WebKitFormBoundary" + os.urandom(16).hex()
    body_parts = [
        f'--{boundary}\r\n'.encode(),
        b'Content-Disposition: form-data; name="file"; filename="' + file_path.name.encode("utf-8") + b'"\r\n',
        f"Content-Type: {content_type}\r\n\r\n".encode(),
        file_data,
        f"\r\n--{boundary}--\r\n".encode(),
    ]
    body = b"".join(body_parts)

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
        method="PUT",
    )
    proxy = get_proxy()
    if proxy:
        proxy_url = proxy.get("https") or proxy.get("http")
        if proxy_url:
            req.set_proxy(proxy_url.replace("https://", "http://"), "https")

    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_access_token(app_key: str, app_secret: str) -> str:
    """Get OAuth2 access token (client_credentials)."""
    url = f"{BASE_URL}/api/v1/oauth2/access_token"
    payload = {
        "app_key": app_key,
        "app_secret": app_secret,
        "grant_type": "client_credentials",
    }
    # OAuth2 token endpoint often expects form-urlencoded
    body = urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    proxy = get_proxy()
    if proxy:
        proxy_url = proxy.get("https") or proxy.get("http")
        if proxy_url:
            req.set_proxy(proxy_url.replace("https://", "http://"), "https")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
        resp_data = json.loads(resp.read().decode("utf-8"))
    data = resp_data.get("data", resp_data)
    access_token = None
    if isinstance(data, dict):
        access_token = data.get("access_token") or data.get("accessToken")
    if not access_token:
        raise RuntimeError(f"Failed to get access token: {resp_data}")
    return access_token


def upload_image(token: str, image_path: Path) -> str:
    """Upload image and return file_id."""
    url = f"{BASE_URL}/api/media/v1/upload/web/permit"
    resp = http_upload(url, image_path, token)
    data = resp.get("data", resp)
    file_id = data.get("file_id") if isinstance(data, dict) else None
    if not file_id:
        raise RuntimeError(f"Failed to upload image: {resp}")
    return file_id


def post_note(token: str, title: str, content: str, image_ids: list[str]) -> dict:
    """Post note via API."""
    url = f"{BASE_URL}/api/sns/v1/note/post"
    payload = {
        "title": title[:20],
        "content": content,
        "image_ids": image_ids,
    }
    headers = {"Authorization": f"Bearer {token}"}
    return http_post(url, json_body=payload, headers=headers)


def format_draft(title: str, content: str, tags: list[str]) -> str:
    """Format content as draft for manual copy-paste."""
    tag_str = " ".join(f"#{t.strip()}" for t in tags if t.strip())
    lines = [
        "--- 小红书草稿（复制到 APP 发布） ---",
        "",
        f"标题: {title}",
        "",
        "正文:",
        content,
        "",
        f"标签: {tag_str}" if tag_str else "",
        "",
        "---",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Post or draft Xiaohongshu notes")
    parser.add_argument("--title", required=True, help="Note title")
    parser.add_argument("--content", required=True, help="Note content")
    parser.add_argument("--image", nargs="*", default=[], help="Image file path(s)")
    parser.add_argument("--tags", default="", help="Comma-separated hashtags")
    parser.add_argument("--draft-only", action="store_true", help="Only output draft, no API call")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    app_key = os.environ.get("XIAOHONGSHU_APP_KEY")
    app_secret = os.environ.get("XIAOHONGSHU_APP_SECRET")
    # 支持中文和英文逗号
    tags = [t.strip() for t in re.split(r"[,、，]", args.tags) if t.strip()]

    if args.draft_only or (not app_key or not app_secret):
        draft = format_draft(args.title, args.content, tags)
        if args.json:
            print(json.dumps({"mode": "draft", "title": args.title, "content": args.content, "tags": tags}))
        else:
            print(draft)
        return 0

    try:
        token = get_access_token(app_key, app_secret)
    except Exception as e:
        print(f"Error getting token: {e}", file=sys.stderr)
        return 1

    image_ids: list[str] = []
    for p in args.image:
        path = Path(p)
        if not path.exists():
            print(f"Image not found: {p}", file=sys.stderr)
            return 1
        try:
            fid = upload_image(token, path)
            image_ids.append(fid)
        except Exception as e:
            print(f"Error uploading {p}: {e}", file=sys.stderr)
            return 1

    try:
        result = post_note(token, args.title, args.content, image_ids)
    except Exception as e:
        print(f"Error posting note: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        if result.get("code") == 0 or result.get("success"):
            print("Note posted successfully.")
        else:
            print(f"Post result: {result}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
