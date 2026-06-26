#!/usr/bin/env python3
"""
Upload a cover/thumbnail image as permanent material (required for article thumb_media_id).
Usage: python3 upload_thumb.py <image_path>
Output: prints the media_id to stdout (used as thumb_media_id in draft/add)

WeChat requires the cover image to be uploaded via /cgi-bin/material/add_material (not uploadimg).
Supported formats: jpg/png, max 1MB.
"""

import json, sys, urllib.request
from pathlib import Path

UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material"

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


def upload_thumb(img_path: str) -> str:
    path = Path(img_path)
    if not path.exists():
        print(f"ERROR: File not found: {img_path}", file=sys.stderr)
        sys.exit(1)

    token = get_token()
    url = f"{UPLOAD_URL}?access_token={token}&type=thumb"

    suffix = path.suffix.lower()
    content_type = "image/jpeg" if suffix in (".jpg", ".jpeg") else "image/png"

    boundary = "----WxThumbBoundary"
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

    media_id = data.get("media_id")
    if not media_id:
        print(f"ERROR: No media_id in response: {data}", file=sys.stderr)
        sys.exit(1)

    print(media_id, end="")
    return media_id


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 upload_thumb.py <image_path>", file=sys.stderr)
        sys.exit(1)
    upload_thumb(sys.argv[1])
