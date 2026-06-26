#!/usr/bin/env python3
"""
Upload an article as a WeChat draft.

Usage:
  python3 upload_draft.py \
    --title "文章标题" \
    --html article.html \
    --thumb-media-id "MEDIA_ID" \
    [--author "作者名"] \
    [--digest "文章摘要（不超过120字）"] \
    [--need-open-comment 1]

  # Or pass HTML content directly:
  python3 upload_draft.py --title "标题" --html-content "<p>...</p>" --thumb-media-id "MEDIA_ID"

Output: prints the media_id of the created draft to stdout
"""

import json, sys, urllib.request
import argparse
from pathlib import Path

DRAFT_URL = "https://api.weixin.qq.com/cgi-bin/draft/add"


def get_token():
    import subprocess
    result = subprocess.run(
        ["python3", Path(__file__).parent / "get_token.py"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def upload_draft(title: str, html_content: str, thumb_media_id: str,
                 author: str = "", digest: str = "",
                 need_open_comment: int = 0) -> str:
    token = get_token()
    url = f"{DRAFT_URL}?access_token={token}"

    article = {
        "title": title,
        "author": author,
        "digest": digest,
        "content": html_content,
        "thumb_media_id": thumb_media_id,
        "need_open_comment": need_open_comment,
        "only_fans_can_comment": 0,
    }

    payload = json.dumps({"articles": [article]}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=payload,
                                  headers={"Content-Type": "application/json; charset=utf-8"},
                                  method="POST")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    if "errcode" in data and data["errcode"] != 0:
        print(f"ERROR: WeChat API error: {data}", file=sys.stderr)
        sys.exit(1)

    media_id = data.get("media_id", "")
    print(media_id, end="")
    return media_id


def main():
    parser = argparse.ArgumentParser(description="Upload article as WeChat draft")
    parser.add_argument("--title", required=True, help="Article title")
    parser.add_argument("--html", help="Path to HTML file")
    parser.add_argument("--html-content", help="HTML content string (alternative to --html)")
    parser.add_argument("--thumb-media-id", required=True, help="Cover image media_id from upload_thumb.py")
    parser.add_argument("--author", default="", help="Author name")
    parser.add_argument("--digest", default="", help="Article summary (max 120 chars)")
    parser.add_argument("--need-open-comment", type=int, default=0, help="Enable comments (0 or 1)")
    args = parser.parse_args()

    if args.html:
        html_content = Path(args.html).read_text(encoding="utf-8")
    elif args.html_content:
        html_content = args.html_content
    else:
        print("ERROR: Either --html or --html-content is required", file=sys.stderr)
        sys.exit(1)

    upload_draft(
        title=args.title,
        html_content=html_content,
        thumb_media_id=args.thumb_media_id,
        author=args.author,
        digest=args.digest,
        need_open_comment=args.need_open_comment,
    )


if __name__ == "__main__":
    main()
