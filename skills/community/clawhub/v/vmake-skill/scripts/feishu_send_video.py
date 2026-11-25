#!/usr/bin/env python3
"""
Send video messages via Feishu (Lark).

Usage:
    python3 feishu_send_video.py \
        --video /path/to/video.mp4 \
        --to ou_xxx \
        [--cover /path/to/cover.jpg | --cover-url https://...] \
        [--duration 20875] \
        [--video-url https://...]

This is a wrapper around scripts.notifications.feishu for backward compatibility.
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print(json.dumps({
        "error": "requests package not installed",
        "install_command": "pip install requests",
    }), file=sys.stderr)
    raise SystemExit(1)

# Add parent to path
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from notifications import FeishuNotifier
from notifications.base import MissingCredentialsError


def main():
    parser = argparse.ArgumentParser(description="Send video messages via Feishu")
    parser.add_argument("--video", required=True, help="Video file path")
    parser.add_argument(
        "--to",
        required=True,
        help="Recipient open_id (ou_xxx) or group chat_id (oc_xxx)",
    )
    parser.add_argument("--cover", help="Cover image path or URL")
    parser.add_argument("--cover-url", help="Cover image URL (alias for --cover)")
    parser.add_argument("--duration", type=int, help="Video duration in milliseconds")
    parser.add_argument(
        "--video-url",
        default="",
        help="Result URL: always sends an extra text message with this download link",
    )
    args = parser.parse_args()

    cover = args.cover or args.cover_url

    try:
        notifier = FeishuNotifier()
        result = notifier.send_video(
            video_path=args.video,
            recipient=args.to,
            video_url=args.video_url,
            cover_url=cover,
            duration=args.duration,
        )
    except MissingCredentialsError as error:
        print(json.dumps(error.payload), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
