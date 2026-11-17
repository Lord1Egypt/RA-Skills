#!/usr/bin/env python3
"""
WeChat Official Account Draft Push Script (Generic Version)

Push an article as a draft to the WeChat MP draft box via the draft/add API.

Usage:
    python3 push_draft.py \
        --env ~/.wechat-mp.env \
        --title "Article Title" \
        --digest "Article summary, max 120 chars" \
        --html /path/to/article.html \
        [--thumb MEDIA_ID] \
        [--cover /path/to/cover.png]

Requirements:
    - curl (for binary-safe JSON upload)
    - A .env file with WECHAT_APPID and WECHAT_SECRET
"""

import json
import subprocess
import sys
import argparse
import os
import tempfile


def load_credentials(env_path):
    """Load WeChat credentials from a .env file."""
    creds = {}
    if not os.path.exists(env_path):
        print(f"ERROR: env file not found: {env_path}")
        sys.exit(1)
    with open(env_path, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                creds[key.strip()] = value.strip()
    for required in ("WECHAT_APPID", "WECHAT_SECRET"):
        if required not in creds:
            print(f"ERROR: {required} not found in {env_path}")
            sys.exit(1)
    return creds


def get_access_token(appid, secret):
    """Get WeChat access_token. Handle IP whitelist error (40164)."""
    result = subprocess.run(
        [
            "curl", "-s",
            f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={appid}&secret={secret}",
        ],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    if "access_token" not in data:
        errcode = data.get("errcode")
        print(f"ERROR getting access_token: {data}")
        if errcode == 40164:
            ip_result = subprocess.run(
                ["curl", "-s", "https://api.ipify.org"],
                capture_output=True,
                text=True,
            )
            server_ip = ip_result.stdout.strip()
            print(f"\n[IP Whitelist Error]")
            print(f"  Server IP: {server_ip}")
            print(f"  Add this IP to: mp.weixin.qq.com -> Development -> Basic Configuration -> IP Whitelist")
        sys.exit(1)
    return data["access_token"]


def upload_cover_image(token, image_path):
    """Upload a cover image to WeChat permanent material library. Returns media_id."""
    if not os.path.exists(image_path):
        print(f"ERROR: cover image not found: {image_path}")
        sys.exit(1)
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
            "-F", f"media=@{image_path}",
        ],
        capture_output=True,
        text=True,
    )
    data = json.loads(result.stdout)
    if "media_id" not in data:
        print(f"ERROR uploading cover image: {data}")
        sys.exit(1)
    return data["media_id"]


def push_draft(token, title, digest, content_html, thumb_media_id, author=""):
    """
    Push a draft to the WeChat MP draft box.

    Uses curl --data-binary to avoid Python requests' unicode escaping
    which garbles Chinese characters.
    """
    draft_data = {
        "articles": [
            {
                "title": title,
                "author": author,  # Leave empty; set manually in editor (8-byte limit)
                "digest": digest,
                "content": content_html,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 1,
                "only_fans_can_comment": 0,
            }
        ]
    }

    # Write JSON with ensure_ascii=False to preserve Chinese characters
    json_path = os.path.join(tempfile.gettempdir(), "wechat_draft.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(draft_data, f, ensure_ascii=False, separators=(",", ":"))

    # Verify encoding: check that Chinese characters survived JSON serialization
    with open(json_path, "r", encoding="utf-8") as f:
        raw = f.read()
    # Simple check: if content has non-ASCII chars, they should appear in the JSON
    has_non_ascii = any(ord(c) > 127 for c in content_html)
    if has_non_ascii and all(ord(c) < 128 for c in raw):
        print("ERROR: JSON encoding failed — Chinese characters lost")
        sys.exit(1)

    # Use curl --data-binary for binary-safe upload (avoids unicode escape issues)
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}",
            "-H", "Content-Type: application/json",
            "--data-binary", f"@{json_path}",
        ],
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser(description="Push a draft to WeChat MP draft box")
    parser.add_argument("--env", required=True, help="Path to .env credential file")
    parser.add_argument("--title", required=True, help="Article title (max 64 bytes)")
    parser.add_argument("--digest", required=True, help="Article summary (max 120 chars)")
    parser.add_argument("--html", required=True, help="Path to article HTML file")
    parser.add_argument("--thumb", default="", help="Cover image media_id (skip to auto-upload from --cover)")
    parser.add_argument("--cover", default="", help="Path to cover image (used if --thumb not provided)")
    parser.add_argument("--author", default="", help="Author name (leave empty to set in editor)")
    args = parser.parse_args()

    # Validate title length
    title_bytes = len(args.title.encode("utf-8"))
    if title_bytes > 64:
        print(f"ERROR: title too long: {title_bytes} bytes (max 64)")
        sys.exit(1)

    # Validate digest length
    if len(args.digest) > 120:
        print(f"ERROR: digest too long: {len(args.digest)} chars (max 120)")
        sys.exit(1)

    # Read HTML content
    if not os.path.exists(args.html):
        print(f"ERROR: HTML file not found: {args.html}")
        sys.exit(1)
    with open(args.html, "r", encoding="utf-8") as f:
        content_html = f.read().strip()

    # Load credentials and get token
    creds = load_credentials(args.env)
    token = get_access_token(creds["WECHAT_APPID"], creds["WECHAT_SECRET"])

    # Resolve thumb_media_id
    thumb_media_id = args.thumb
    if not thumb_media_id and args.cover:
        print("Uploading cover image...")
        thumb_media_id = upload_cover_image(token, args.cover)
        print(f"  Cover uploaded: {thumb_media_id}")

    if not thumb_media_id:
        print("WARNING: no thumb_media_id — draft will have no cover. Set one in the editor.")

    # Push draft
    print("Pushing draft...")
    result = push_draft(token, args.title, args.digest, content_html, thumb_media_id, args.author)

    if "media_id" in result:
        print(f"\n[SUCCESS] Draft pushed!")
        print(f"  media_id: {result['media_id']}")
        print(f"\n[Manual steps in editor]:")
        print(f"  1. Set author name (if left empty)")
        print(f"  2. Verify cover image, title, and summary")
        print(f"  3. Preview before publishing")
    else:
        print(f"\n[FAILED] Push failed: {result}")
        errcode = result.get("errcode")
        if errcode == 45004:
            print("  -> digest exceeds 120 characters")
        elif errcode == 45110:
            print("  -> author name exceeds 8 bytes; leave empty and set in editor")
        elif errcode == 40164:
            print("  -> server IP not whitelisted")
        sys.exit(1)


if __name__ == "__main__":
    main()
