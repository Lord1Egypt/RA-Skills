#!/usr/bin/env python3
"""Push article HTML to WeChat Official Account draft box.

Usage:
    python push_draft.py <html_file> <title> <digest> <author> <cover_image> [--config <config_json>]

The script:
1. Obtains WeChat access_token (from WECHAT_APP_ID/WECHAT_APP_SECRET env vars or config file)
2. Deletes all existing drafts (prevent pile-up)
3. Uploads cover image as thumb_media
4. Pushes the HTML article to draft box
"""
import sys, os, json, io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import argparse
import requests

SKILL_DIR = os.path.expanduser("~/.AI 助手平台/skills/wechat-gzh/scripts")
if os.path.isdir(SKILL_DIR):
    sys.path.insert(0, SKILL_DIR)

try:
    from wechat_gzh import WeChatGZH, WeChatConfig
    HAS_WECHAT_GZH = True
except ImportError:
    HAS_WECHAT_GZH = False


def get_credentials(config_path=None):
    """Get WeChat credentials from env vars or config file."""
    app_id = os.environ.get("WECHAT_APP_ID") or os.environ.get("WECHAT_APPID")
    app_secret = os.environ.get("WECHAT_APP_SECRET") or os.environ.get("WECHAT_SECRET")

    if not app_id or not app_secret:
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                cfg = json.load(f)
            app_id = cfg.get("appid") or cfg.get("app_id")
            app_secret = cfg.get("secret") or cfg.get("app_secret")

    if not app_id or not app_secret:
        # Try Windows env vars
        import subprocess
        try:
            ps = subprocess.run(
                ['powershell', '-Command',
                 '[Environment]::GetEnvironmentVariable("WECHAT_APP_SECRET","User")'],
                capture_output=True, text=True, timeout=10
            )
            app_secret = ps.stdout.strip() if ps.stdout.strip() else None
            if not app_id:
                ps2 = subprocess.run(
                    ['powershell', '-Command',
                     '[Environment]::GetEnvironmentVariable("WECHAT_APP_ID","User")'],
                    capture_output=True, text=True, timeout=10
                )
                app_id = ps2.stdout.strip() if ps2.stdout.strip() else None
        except Exception:
            pass

    return app_id, app_secret


def get_access_token(app_id, app_secret):
    """Get stable access token."""
    r = requests.post(
        "https://api.weixin.qq.com/cgi-bin/stable_token",
        json={"grant_type": "client_credential", "appid": app_id, "secret": app_secret},
        timeout=30
    )
    data = r.json()
    token = data.get("access_token", "")
    if not token:
        print(f"[ERROR] Failed to get access token: {data}", file=sys.stderr)
        sys.exit(1)
    return token


def delete_all_drafts(token):
    """Delete all existing drafts."""
    r = requests.post(
        "https://api.weixin.qq.com/cgi-bin/draft/batchget",
        json={"offset": 0, "count": 20, "no_content": 1},
        params={"access_token": token},
        timeout=30
    )
    data = r.json()
    items = data.get("item", [])
    print(f"[INFO] Existing drafts: {len(items)}")

    for item in items:
        mid = item["media_id"]
        title = ""
        try:
            title = item["content"]["news_item"][0]["title"]
        except Exception:
            pass
        try:
            requests.post(
                f"https://api.weixin.qq.com/cgi-bin/draft/delete",
                json={"media_id": mid},
                params={"access_token": token},
                timeout=30
            )
            print(f"  [DELETED] {mid} ({title})")
        except Exception as e:
            print(f"  [SKIP] {mid}: {e}")


def upload_cover(token, cover_path):
    """Upload cover image and return thumb_media_id."""
    cover_path = os.path.normpath(cover_path)
    fname = os.path.basename(cover_path)

    if not os.path.exists(cover_path):
        print(f"[ERROR] Cover image not found: {cover_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[INFO] Cover: {cover_path} ({os.path.getsize(cover_path)} bytes)")

    with open(cover_path, 'rb') as f:
        r = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
            files={'media': (fname, f, 'image/png')},
            timeout=120
        )
    result = r.json()

    if 'media_id' not in result:
        print(f"[ERROR] Cover upload failed: {result}", file=sys.stderr)
        sys.exit(1)

    return result["media_id"], result.get("url", "")


def push_draft(token, thumb_media_id, title, content, digest, author):
    """Push article to draft box."""
    articles = [{
        "title": title,
        "content": content,
        "thumb_media_id": thumb_media_id,
        "author": author,
        "digest": digest,
        "need_open_comment": 1,
        "only_fans_can_comment": 0,
    }]

    r = requests.post(
        "https://api.weixin.qq.com/cgi-bin/draft/add",
        json={"articles": articles},
        params={"access_token": token},
        timeout=60
    )
    result = r.json()

    if 'media_id' not in result:
        print(f"[ERROR] Draft push failed: {result}", file=sys.stderr)
        sys.exit(1)

    return result["media_id"]


def main():
    parser = argparse.ArgumentParser(description="Push article to WeChat draft box")
    parser.add_argument("html_file", help="Path to HTML article file")
    parser.add_argument("title", help="Article title (<=8 Chinese chars)")
    parser.add_argument("digest", help="Article digest/summary")
    parser.add_argument("author", help="Author name")
    parser.add_argument("cover_image", help="Path to cover image (16:9 PNG)")
    parser.add_argument("--config", help="Path to JSON config file with appid/secret", default=None)
    args = parser.parse_args()

    # Validate inputs
    if not os.path.exists(args.html_file):
        print(f"[ERROR] HTML file not found: {args.html_file}", file=sys.stderr)
        sys.exit(1)

    with open(args.html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"[OK] HTML loaded: {len(content)} chars")

    if len(args.title.encode('utf-8')) > 24:
        print(f"[WARN] Title may be too long: {len(args.title)} chars ({len(args.title.encode('utf-8'))} bytes)")

    # Get credentials
    app_id, app_secret = get_credentials(args.config)
    if not app_id or not app_secret:
        print("[ERROR] WECHAT_APP_ID or WECHAT_APP_SECRET not found", file=sys.stderr)
        print("  Set env vars or provide --config path", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] AppID: {app_id}, Secret: {app_secret[:4]}...")

    # Get token
    token = get_access_token(app_id, app_secret)
    print(f"[OK] Token: {token[:16]}...")

    # Delete old drafts
    delete_all_drafts(token)

    # Upload cover
    thumb_id, cover_url = upload_cover(token, args.cover_image)
    print(f"[OK] Cover: media_id={thumb_id}")

    # Push draft
    media_id = push_draft(token, thumb_id, args.title, content, args.digest, args.author)

    print(f"\n{'='*60}")
    print(f"[SUCCESS] Draft pushed to WeChat!")
    print(f"  Title: {args.title}")
    print(f"  media_id: {media_id}")
    print(f"  cover_media_id: {thumb_id}")
    print(f"  cover_url: {cover_url}")
    print(f"")
    print(f"  Preview: 公众号后台 -> 草稿箱 -> '{args.title}' -> 预览 -> <示例昵称>")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
