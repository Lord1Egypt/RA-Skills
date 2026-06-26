#!/usr/bin/env python3
"""
Upload images to WeChat Official Account for use in article content.

Usage:
  # Upload image for article body (returns URL to use in <img> tags)
  python3 upload_image.py --token TOKEN --file /path/to/image.png

  # Upload image as permanent material / cover (returns media_id)
  python3 upload_image.py --token TOKEN --file /path/to/cover.png --cover
"""

import argparse
import json
import mimetypes
import sys
import urllib.request
import http.client
import os


def upload_article_image(token: str, filepath: str) -> str:
    """Upload image for article body. Returns URL string."""
    if not os.path.isfile(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    req = urllib.request.Request(url, data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if "url" in result:
                return result["url"]
            else:
                print(f"API Error: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def upload_cover_image(token: str, filepath: str) -> str:
    """Upload image as permanent material. Returns media_id string."""
    if not os.path.isfile(filepath):
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    filename = os.path.basename(filepath)

    with open(filepath, "rb") as f:
        file_data = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: image/png\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"
    req = urllib.request.Request(url, data=body)
    req.add_header("Content-Type", f"multipart/form-data; boundary={boundary}")

    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if "media_id" in result:
                return result["media_id"]
            else:
                print(f"API Error: {json.dumps(result, ensure_ascii=False)}", file=sys.stderr)
                sys.exit(1)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Connection Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Upload image to WeChat MP")
    parser.add_argument("--token", required=True, help="WeChat access token")
    parser.add_argument("--file", required=True, help="Path to image file")
    parser.add_argument("--cover", action="store_true", help="Upload as permanent cover material")
    args = parser.parse_args()

    if args.cover:
        result = upload_cover_image(args.token, args.file)
        print(json.dumps({"media_id": result}, ensure_ascii=False))
    else:
        result = upload_article_image(args.token, args.file)
        print(json.dumps({"url": result}, ensure_ascii=False))


if __name__ == "__main__":
    main()
