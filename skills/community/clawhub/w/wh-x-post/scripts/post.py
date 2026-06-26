#!/usr/bin/env python3
"""Send a tweet via twitter-cli.

Usage:
    python post.py "Hello world" --json
    python post.py "With image" --images /path/to/img.jpg --json
    python post.py "Multiple images" --images /path/a.jpg,/path/b.jpg --json
"""
from __future__ import annotations

import argparse
import sys

sys.path.insert(0, str(__file__).rsplit("/", 1)[0])
from common import print_result, run_twitter_cli


def main() -> None:
    parser = argparse.ArgumentParser(description="Send a tweet via twitter-cli")
    parser.add_argument("text", help="Tweet content")
    parser.add_argument(
        "--images",
        type=str,
        default=None,
        help="Comma-separated list of image paths (max 4)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="Output result as JSON",
    )
    args = parser.parse_args()

    # Validate tweet length
    if len(args.text) > 280:
        print_result({
            "ok": False,
            "error": {
                "code": "CONTENT_TOO_LONG",
                "message": f"推文内容过长（{len(args.text)}字符），不超过280字符",
            },
        })
        return

    # Build command
    cmd = ["post", args.text]
    if args.images:
        image_list = [img.strip() for img in args.images.split(",") if img.strip()]
        if len(image_list) > 4:
            print_result({
                "ok": False,
                "error": {
                    "code": "TOO_MANY_IMAGES",
                    "message": "最多只能附带4张图片",
                },
            })
            return
        for img in image_list:
            cmd.extend(["-i", img])

    result = run_twitter_cli(cmd, json_output=args.json_output)

    # If successful, format the result nicely
    if result.get("ok"):
        data = result.get("data", {})
        tweet_id = data.get("id") or data.get("tweet_id", "")
        tweet_url = data.get("url", f"https://x.com/i/status/{tweet_id}")
        print_result({
            "ok": True,
            "data": {
                "tweet_id": str(tweet_id),
                "tweet_url": tweet_url,
            },
        })
    else:
        print_result(result)


if __name__ == "__main__":
    main()
