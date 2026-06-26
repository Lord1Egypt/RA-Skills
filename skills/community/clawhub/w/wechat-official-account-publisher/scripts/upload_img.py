#!/usr/bin/env python3
"""
Upload a local image to WeChat CDN.
Usage: python3 upload_img.py <image_path>
Output: prints the WeChat CDN URL to stdout (for use in articles)

Note: This uploads as a permanent material image (for article body images).
For the article cover/thumb, a different media_id is used — see upload_thumb.py.
"""

import json, sys, urllib.request, urllib.parse
from pathlib import Path

UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/media/uploadimg"

def get_token():
    import subprocess, os
    result = subprocess.run(
        ["python3", Path(__file__).parent / "get_token.py"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)
    return result.stdout.strip()


def upload_image(img_path: str) -> str:
    path = Path(img_path)
    if not path.exists():
        print(f"ERROR: File not found: {img_path}", file=sys.stderr)
        sys.exit(1)

    token = get_token()
    url = f"{UPLOAD_URL}?access_token={token}"

    # Determine content type
    suffix = path.suffix.lower()
    content_type_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                        ".png": "image/png", ".gif": "image/gif", ".webp": "image/webp"}
    content_type = content_type_map.get(suffix, "image/jpeg")

    # Multipart form upload
    boundary = "----WxPublisherBoundary"
    img_data = path.read_bytes()
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{path.name}"\r\n'
        f"Content-Type: {content_type}\r\n\r\n"
    ).encode() + img_data + f"\r\n--{boundary}--\r\n".encode()

    req = urllib.request.Request(url, data=body,
                                  headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
                                  method="POST")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())

    if "errcode" in data and data["errcode"] != 0:
        print(f"ERROR: WeChat upload error: {data}", file=sys.stderr)
        sys.exit(1)

    wx_url = data.get("url")
    if not wx_url:
        print(f"ERROR: No URL in response: {data}", file=sys.stderr)
        sys.exit(1)

    print(wx_url, end="")
    return wx_url


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 upload_img.py <image_path>", file=sys.stderr)
        sys.exit(1)
    upload_image(sys.argv[1])
