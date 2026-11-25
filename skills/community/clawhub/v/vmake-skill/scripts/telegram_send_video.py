#!/usr/bin/env python3
"""
Send video messages via Telegram Bot API.

Usage:
    TELEGRAM_BOT_TOKEN=<token> python3 telegram_send_video.py \
        --video /path/to/video.mp4 \
        --to <chat_id> \
        [--cover-url https://...] \
        [--duration 120] \
        [--caption "Video caption"] \
        [--video-url https://...]

This is a wrapper around scripts.notifications.telegram for backward compatibility.
"""

import argparse
import json
import os
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

from notifications import TelegramNotifier
from notifications.base import MissingCredentialsError


def main():
    parser = argparse.ArgumentParser(
        description="Send video via Telegram. Token via TELEGRAM_BOT_TOKEN only."
    )
    parser.add_argument("--video", required=True, help="Local video file path (.mp4)")
    parser.add_argument("--to", required=True, help="Telegram chat_id")
    parser.add_argument("--cover-url", default="", help="Thumbnail image URL (optional)")
    parser.add_argument("--duration", type=int, default=0, help="Duration in seconds (optional)")
    parser.add_argument("--caption", default="", help="Caption (optional)")
    parser.add_argument(
        "--video-url",
        default="",
        help="Result URL: always sends an extra text message with this link",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print(json.dumps({"error": f"Video file not found: {args.video}"}), file=sys.stderr)
        return 1

    try:
        notifier = TelegramNotifier()
        result = notifier.send_video(
            video_path=args.video,
            recipient=args.to,
            video_url=args.video_url,
            cover_url=args.cover_url,
            duration=args.duration,
            caption=args.caption,
        )
    except MissingCredentialsError as error:
        print(json.dumps(error.payload), file=sys.stderr)
        return 1
    print(json.dumps(result))
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
