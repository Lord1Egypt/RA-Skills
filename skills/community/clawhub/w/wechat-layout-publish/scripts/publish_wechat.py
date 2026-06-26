#!/usr/bin/env python3
import argparse
import base64
import html
import json
import mimetypes
import os
import re
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Dict, Optional, Tuple


USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)


def read_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def strip_tags(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def infer_title(html_text: str, fallback: str = "未命名文章") -> str:
    for pattern in [
        r"<h1[^>]*>(.*?)</h1>",
        r"<title[^>]*>(.*?)</title>",
    ]:
        match = re.search(pattern, html_text, re.I | re.S)
        if match:
            title = strip_tags(match.group(1))
            if title:
                return title
    return fallback


def infer_digest(html_text: str, limit: int = 120) -> str:
    plain = strip_tags(html_text)
    return plain[:limit]


def first_image_src(html_text: str) -> Optional[str]:
    match = re.search(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", html_text, re.I)
    if match:
        return match.group(1).strip()
    return None


def build_api_url(proxy_origin: Optional[str], path: str, access_token: Optional[str] = None) -> str:
    base = proxy_origin.rstrip("/") if proxy_origin else "https://api.weixin.qq.com"
    url = f"{base}{path}"
    if access_token:
        joiner = "&" if "?" in url else "?"
        url = f"{url}{joiner}access_token={urllib.parse.quote(access_token)}"
    return url


def request_json(url: str, method: str = "GET", body: Optional[bytes] = None, headers: Optional[Dict[str, str]] = None) -> Dict:
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("User-Agent", USER_AGENT)
    if headers:
        for key, value in headers.items():
            req.add_header(key, value)
    with urllib.request.urlopen(req, timeout=30) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        payload = resp.read().decode(charset, errors="replace")
    data = json.loads(payload)
    errcode = data.get("errcode", 0)
    if errcode not in (0, None):
        raise RuntimeError(json.dumps(data, ensure_ascii=False))
    return data


def post_json(url: str, payload: Dict) -> Dict:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return request_json(url, method="POST", body=body, headers={"Content-Type": "application/json"})


def detect_content_type(path_or_name: str, fallback: str = "application/octet-stream") -> str:
    guessed, _ = mimetypes.guess_type(path_or_name)
    return guessed or fallback


def build_multipart(field_name: str, filename: str, content_type: str, payload: bytes) -> Tuple[bytes, str]:
    boundary = f"----OpenClaw{uuid.uuid4().hex}"
    lines = [
        f"--{boundary}",
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"',
        f"Content-Type: {content_type}",
        "",
    ]
    body = "\r\n".join(lines).encode("utf-8") + b"\r\n" + payload + b"\r\n" + f"--{boundary}--\r\n".encode("utf-8")
    return body, f"multipart/form-data; boundary={boundary}"


def read_binary_source(source: str) -> Tuple[bytes, str, str]:
    if source.startswith("data:"):
        header, encoded = source.split(",", 1)
        mime_match = re.match(r"data:([^;]+);base64", header, re.I)
        mime_type = mime_match.group(1) if mime_match else "application/octet-stream"
        suffix = mimetypes.guess_extension(mime_type) or ".bin"
        return base64.b64decode(encoded), f"inline{suffix}", mime_type
    if re.match(r"^https?://", source, re.I):
        req = urllib.request.Request(source, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = resp.read()
            content_type = resp.headers.get_content_type()
        parsed = urllib.parse.urlparse(source)
        filename = Path(parsed.path).name or f"remote{mimetypes.guess_extension(content_type) or '.bin'}"
        return payload, filename, content_type or detect_content_type(filename)
    path = Path(source)
    payload = path.read_bytes()
    return payload, path.name, detect_content_type(path.name)


def get_access_token(app_id: str, app_secret: str, proxy_origin: Optional[str]) -> str:
    url = build_api_url(proxy_origin, "/cgi-bin/stable_token")
    payload = {
        "grant_type": "client_credential",
        "appid": app_id,
        "secret": app_secret,
    }
    data = post_json(url, payload)
    token = data.get("access_token")
    if not token:
        raise RuntimeError(f"Failed to obtain access token: {json.dumps(data, ensure_ascii=False)}")
    return token


def upload_material(access_token: str, source: str, proxy_origin: Optional[str]) -> Dict:
    payload, filename, content_type = read_binary_source(source)
    body, multipart_content_type = build_multipart("media", filename, content_type, payload)
    url = build_api_url(proxy_origin, "/cgi-bin/material/add_material?type=image", access_token)
    return request_json(url, method="POST", body=body, headers={"Content-Type": multipart_content_type})


def upload_inline_image(access_token: str, source: str, proxy_origin: Optional[str]) -> str:
    payload, filename, content_type = read_binary_source(source)
    body, multipart_content_type = build_multipart("media", filename, content_type, payload)
    url = build_api_url(proxy_origin, "/cgi-bin/media/uploadimg", access_token)
    data = request_json(url, method="POST", body=body, headers={"Content-Type": multipart_content_type})
    image_url = data.get("url")
    if not image_url:
        raise RuntimeError(f"Image upload succeeded without url: {json.dumps(data, ensure_ascii=False)}")
    if image_url.startswith("http://"):
        image_url = "https://" + image_url[len("http://") :]
    return image_url


def replace_body_images(access_token: str, html_text: str, proxy_origin: Optional[str], dry_run: bool) -> str:
    cache: Dict[str, str] = {}

    def repl(match: re.Match) -> str:
        original = match.group(1).strip()
        if original in cache:
            replacement = cache[original]
        elif dry_run:
            replacement = original
            cache[original] = replacement
        else:
            replacement = upload_inline_image(access_token, original, proxy_origin)
            cache[original] = replacement
        return match.group(0).replace(original, replacement, 1)

    return re.sub(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"']", repl, html_text, flags=re.I)


def build_draft_payload(title: str, html_text: str, thumb_media_id: str, author: str, digest: str, source_url: str, open_comment: bool, fans_comment_only: bool) -> Dict:
    article = {
        "article_type": "news",
        "title": title,
        "content": html_text,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": 1 if open_comment else 0,
        "only_fans_can_comment": 1 if fans_comment_only else 0,
    }
    if author:
        article["author"] = author
    if digest:
        article["digest"] = digest
    if source_url:
        article["content_source_url"] = source_url
    return {"articles": [article]}


def add_draft(access_token: str, payload: Dict, proxy_origin: Optional[str]) -> Dict:
    url = build_api_url(proxy_origin, "/cgi-bin/draft/add", access_token)
    return post_json(url, payload)


def get_draft_detail(access_token: str, media_id: str, proxy_origin: Optional[str]) -> Dict:
    url = build_api_url(proxy_origin, "/cgi-bin/draft/get", access_token)
    return post_json(url, {"media_id": media_id})


def freepublish_submit(access_token: str, media_id: str, proxy_origin: Optional[str]) -> Dict:
    url = build_api_url(proxy_origin, "/cgi-bin/freepublish/submit", access_token)
    return post_json(url, {"media_id": media_id})


def freepublish_get(access_token: str, publish_id: str, proxy_origin: Optional[str]) -> Dict:
    url = build_api_url(proxy_origin, "/cgi-bin/freepublish/get", access_token)
    return post_json(url, {"publish_id": publish_id})


def poll_publish(access_token: str, publish_id: str, proxy_origin: Optional[str], poll_interval: int, poll_timeout: int) -> Dict:
    started = time.time()
    while time.time() - started < poll_timeout:
        data = freepublish_get(access_token, publish_id, proxy_origin)
        status = data.get("publish_status")
        if status == 1:
            time.sleep(poll_interval)
            continue
        if status == 0:
            return data
        raise RuntimeError(f"Publish failed: {json.dumps(data, ensure_ascii=False)}")
    raise RuntimeError("Publish timed out while polling freepublish/get")


def load_config(args: argparse.Namespace) -> Dict[str, str]:
    config: Dict[str, str] = {}
    if args.config:
        config = json.loads(read_text(args.config))
    merged = {
        "appId": args.app_id or config.get("appId") or os.getenv("WECHAT_APP_ID", ""),
        "appSecret": args.app_secret or config.get("appSecret") or os.getenv("WECHAT_APP_SECRET", ""),
        "proxyOrigin": args.proxy_origin or config.get("proxyOrigin") or os.getenv("WECHAT_PROXY_ORIGIN", ""),
        "author": args.author or config.get("author") or os.getenv("WECHAT_AUTHOR", ""),
    }
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Publish standalone rendered HTML to WeChat Official Accounts."
    )
    parser.add_argument("--html", required=True, help="The themed WeChat-compatible HTML file to publish.")
    parser.add_argument("--config", help="Optional JSON config containing appId/appSecret/proxyOrigin/author.")
    parser.add_argument("--app-id", help="WeChat Official Accounts appId.")
    parser.add_argument("--app-secret", help="WeChat Official Accounts appSecret.")
    parser.add_argument("--proxy-origin", help="Optional reverse proxy origin for WeChat API requests.")
    parser.add_argument("--title", help="Article title. Inferred from HTML when omitted.")
    parser.add_argument("--author", help="Article author. Falls back to config/env.")
    parser.add_argument("--digest", help="Article digest. Auto-generated when omitted.")
    parser.add_argument("--source-url", default="", help="Original article URL to keep as content_source_url.")
    parser.add_argument("--cover", help="Cover image path, URL, or data URI. Defaults to the first body image.")
    parser.add_argument("--mode", choices=["draft", "formal"], default="draft", help="Publish mode.")
    parser.add_argument("--open-comment", action="store_true", help="Enable comments if the account supports it.")
    parser.add_argument("--fans-comment-only", action="store_true", help="Only allow followers to comment.")
    parser.add_argument("--poll-interval", type=int, default=2, help="Polling interval in seconds for formal publish.")
    parser.add_argument("--poll-timeout", type=int, default=60, help="Total polling timeout in seconds for formal publish.")
    parser.add_argument("--dry-run", action="store_true", help="Build and print the publish payload without calling WeChat APIs.")
    args = parser.parse_args()

    config = load_config(args)
    html_text = read_text(args.html)
    title = args.title or infer_title(html_text, fallback=Path(args.html).stem)
    digest = args.digest or infer_digest(html_text)
    author = config["author"]
    cover = args.cover or first_image_src(html_text)

    if not cover and not args.dry_run:
        raise SystemExit("No cover image provided and no body image found for fallback cover upload.")

    if args.dry_run:
        payload = build_draft_payload(
            title=title,
            html_text=html_text,
            thumb_media_id="DRY_RUN_THUMB_MEDIA_ID",
            author=author,
            digest=digest,
            source_url=args.source_url,
            open_comment=args.open_comment,
            fans_comment_only=args.fans_comment_only,
        )
        print(json.dumps({
            "mode": args.mode,
            "title": title,
            "author": author,
            "digest": digest,
            "cover": cover,
            "payload": payload,
        }, ensure_ascii=False, indent=2))
        return

    if not config["appId"] or not config["appSecret"]:
        raise SystemExit("Missing WeChat appId/appSecret. Provide them via --config, --app-id/--app-secret, or env.")

    access_token = get_access_token(config["appId"], config["appSecret"], config["proxyOrigin"] or None)
    cover_res = upload_material(access_token, cover, config["proxyOrigin"] or None)
    thumb_media_id = cover_res.get("media_id")
    if not thumb_media_id:
        raise RuntimeError(f"Cover upload did not return media_id: {json.dumps(cover_res, ensure_ascii=False)}")

    final_html = replace_body_images(access_token, html_text, config["proxyOrigin"] or None, dry_run=False)
    draft_payload = build_draft_payload(
        title=title,
        html_text=final_html,
        thumb_media_id=thumb_media_id,
        author=author,
        digest=digest,
        source_url=args.source_url,
        open_comment=args.open_comment,
        fans_comment_only=args.fans_comment_only,
    )
    draft_res = add_draft(access_token, draft_payload, config["proxyOrigin"] or None)
    draft_media_id = draft_res.get("media_id")
    if not draft_media_id:
        raise RuntimeError(f"Draft creation failed: {json.dumps(draft_res, ensure_ascii=False)}")

    if args.mode == "draft":
        detail = get_draft_detail(access_token, draft_media_id, config["proxyOrigin"] or None)
        preview_url = ""
        items = detail.get("news_item")
        if isinstance(items, list) and items:
            preview_url = items[0].get("url", "")
        print(json.dumps({
            "status": "draft_created",
            "media_id": draft_media_id,
            "preview_url": preview_url,
        }, ensure_ascii=False, indent=2))
        return

    submit_res = freepublish_submit(access_token, draft_media_id, config["proxyOrigin"] or None)
    publish_id = submit_res.get("publish_id")
    if publish_id is None or str(publish_id).strip() == "":
        raise RuntimeError(f"Formal publish submit failed: {json.dumps(submit_res, ensure_ascii=False)}")
    publish_detail = poll_publish(
        access_token,
        str(publish_id),
        config["proxyOrigin"] or None,
        poll_interval=args.poll_interval,
        poll_timeout=args.poll_timeout,
    )
    article_urls = []
    article_detail = publish_detail.get("article_detail", {})
    items = article_detail.get("item") if isinstance(article_detail, dict) else None
    if isinstance(items, list):
        for item in items:
            url = item.get("article_url")
            if isinstance(url, str) and url:
                article_urls.append(url)
    print(json.dumps({
        "status": "published",
        "media_id": draft_media_id,
        "publish_id": str(publish_id),
        "article_urls": article_urls,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
