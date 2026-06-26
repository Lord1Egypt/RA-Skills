#!/usr/bin/env python3
"""
Create and optionally publish WeChat Official Account (公众号) articles.

Usage:
  python3 publish.py --title "标题" --content "正文" [--cover cover.jpg] [--publish]
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import urllib.request
import urllib.error

BASE_URL = "https://api.weixin.qq.com"


def get_proxies() -> dict | None:
    """Read HTTP/HTTPS proxy from env."""
    http = os.environ.get("HTTP_PROXY") or os.environ.get("http_proxy")
    https = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if https or http:
        return {"http": http or https, "https": https or http}
    return None


def http_post(url: str, data: bytes, content_type: str = "application/json") -> dict:
    """POST JSON or form data and return parsed JSON."""
    req = urllib.request.Request(
        url,
        data=data,
        method="POST",
        headers={"Content-Type": content_type},
    )
    opener = urllib.request.build_opener()
    if get_proxies():
        opener.add_handler(urllib.request.ProxyHandler(get_proxies()))
    with opener.open(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def http_post_file(url: str, file_path: Path, field_name: str) -> dict:
    """POST multipart form with file (media field for WeChat add_material)."""
    import mimetypes

    content_type, _ = mimetypes.guess_type(str(file_path)) or ("image/jpeg", None)
    with open(file_path, "rb") as f:
        body = f.read()

    boundary = b"----WebKitFormBoundary" + os.urandom(16).hex().encode()
    disp = (
        f'Content-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"'
    ).encode()
    ctype = f"Content-Type: {content_type}".encode()
    parts = [
        b"--" + boundary,
        disp,
        ctype,
        b"",
        body,
        b"--" + boundary + b"--",
    ]
    req = urllib.request.Request(
        url,
        data=b"\r\n".join(parts),
        method="POST",
        headers={"Content-Type": f"multipart/form-data; boundary={boundary.decode()}"},
    )
    opener = urllib.request.build_opener()
    if get_proxies():
        opener.add_handler(urllib.request.ProxyHandler(get_proxies()))
    with opener.open(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def get_access_token(appid: str, secret: str) -> str:
    """Fetch access_token from WeChat API."""
    url = f"{BASE_URL}/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}"
    req = urllib.request.Request(url, method="GET")
    opener = urllib.request.build_opener()
    if get_proxies():
        opener.add_handler(urllib.request.ProxyHandler(get_proxies()))
    with opener.open(req, timeout=15) as resp:
        out = json.loads(resp.read().decode())
    if "access_token" not in out:
        raise RuntimeError(f"Failed to get access_token: {out}")
    return out["access_token"]


def upload_cover(token: str, file_path: Path) -> str:
    """Upload cover image as permanent material, return media_id."""
    url = f"{BASE_URL}/cgi-bin/material/add_material?access_token={token}&type=image"
    out = http_post_file(url, file_path, "media")
    if "media_id" not in out:
        raise RuntimeError(f"Failed to upload cover: {out}")
    return out["media_id"]


def md_to_html(text: str) -> str:
    """Simple markdown to HTML conversion for WeChat content."""
    # WeChat content: basic tags only
    html = text
    # Bold
    html = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html)
    html = re.sub(r"__(.+?)__", r"<b>\1</b>", html)
    # Italic
    html = re.sub(r"\*(.+?)\*", r"<i>\1</i>", html)
    html = re.sub(r"_(.+?)_", r"<i>\1</i>", html)
    # Line breaks
    html = html.replace("\n", "<br>")
    return html


def add_draft(
    token: str,
    *,
    title: str,
    content: str,
    thumb_media_id: str,
    author: str = "",
    digest: str = "",
    content_source_url: str = "",
) -> str:
    """Create draft and return media_id."""
    url = f"{BASE_URL}/cgi-bin/draft/add?access_token={token}"
    # Content length limit ~20k chars
    if len(content) > 19000:
        content = content[:19000] + "<br>...[内容已截断]"
    body = {
        "articles": [
            {
                "title": title[:32],
                "author": author[:16] if author else "",
                "digest": digest[:128] if digest else "",
                "content": content,
                "content_source_url": content_source_url[:1024] if content_source_url else "",
                "thumb_media_id": thumb_media_id,
            }
        ]
    }
    out = http_post(url, json.dumps(body, ensure_ascii=False).encode())
    if "media_id" not in out:
        raise RuntimeError(f"Failed to add draft: {out}")
    return out["media_id"]


def publish_draft(token: str, media_id: str) -> dict:
    """Submit draft for publishing. Returns publish_id; actual publish is async."""
    url = f"{BASE_URL}/cgi-bin/freepublish/submit?access_token={token}"
    out = http_post(url, json.dumps({"media_id": media_id}).encode())
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Create/publish WeChat Official Account article")
    parser.add_argument("--title", required=True, help="Article title (≤32 chars)")
    parser.add_argument("--content", help="Article body (Markdown or HTML)")
    parser.add_argument("--content-file", help="Read content from file instead of --content")
    parser.add_argument("--author", default="", help="Author name (≤16 chars)")
    parser.add_argument("--digest", default="", help="Summary (≤128 chars, single-article only)")
    parser.add_argument("--cover", help="Cover image path (jpg/png)")
    parser.add_argument("--source-url", default="", help="Original article URL")
    parser.add_argument("--publish", action="store_true", help="Submit for publishing after draft")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()

    appid = os.environ.get("WECHAT_APPID")
    secret = os.environ.get("WECHAT_SECRET")
    if not appid or not secret:
        print("Error: WECHAT_APPID and WECHAT_SECRET must be set", file=sys.stderr)
        return 1

    content = args.content
    if args.content_file:
        p = Path(args.content_file)
        if not p.exists():
            print(f"Error: file not found: {p}", file=sys.stderr)
            return 1
        content = p.read_text(encoding="utf-8")
    if not content:
        print("Error: --content or --content-file required", file=sys.stderr)
        return 1

    # Simple HTML detection: if starts with <, assume HTML
    if not content.strip().startswith("<"):
        content = md_to_html(content)

    try:
        token = get_access_token(appid, secret)
    except Exception as e:
        print(f"Error getting token: {e}", file=sys.stderr)
        return 1

    # Cover: required for article. Use placeholder or user-provided.
    if args.cover:
        cover_path = Path(args.cover)
        if not cover_path.exists():
            print(f"Error: cover not found: {cover_path}", file=sys.stderr)
            return 1
        try:
            thumb_media_id = upload_cover(token, cover_path)
        except Exception as e:
            print(f"Error uploading cover: {e}", file=sys.stderr)
            return 1
    else:
        # WeChat requires thumb_media_id. Without cover, user must provide one.
        print(
            "Error: --cover required (WeChat requires a cover image for articles)",
            file=sys.stderr,
        )
        return 1

    try:
        media_id = add_draft(
            token,
            title=args.title,
            content=content,
            thumb_media_id=thumb_media_id,
            author=args.author,
            digest=args.digest,
            content_source_url=args.source_url,
        )
    except Exception as e:
        print(f"Error adding draft: {e}", file=sys.stderr)
        return 1

    result = {"media_id": media_id, "draft_created": True}

    if args.publish:
        try:
            pub = publish_draft(token, media_id)
            if pub.get("errcode", -1) != 0:
                print(f"Error publishing: {pub}", file=sys.stderr)
                return 1
            result["publish_id"] = pub.get("publish_id", "")
            result["published"] = True
        except Exception as e:
            print(f"Error publishing: {e}", file=sys.stderr)
            return 1

    if args.json:
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(f"Draft created: media_id={media_id}")
        if args.publish:
            print(f"Publish submitted: publish_id={result.get('publish_id', '')}")
        print("You can edit/publish in WeChat Official Account admin.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
