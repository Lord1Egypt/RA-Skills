# -*- coding: utf-8 -*-
"""
上传封面图到微信素材库（永久图片）
"""
import json
import os
import sys
import mimetypes
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from get_token import get_access_token

UPLOAD_URL = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image"


def get_mime_type(path):
    mime, _ = mimetypes.guess_type(path)
    return mime or "image/jpeg"


def upload_thumb(image_path):
    token = get_access_token()
    url = UPLOAD_URL.format(token=token)

    if not os.path.exists(image_path):
        print(f"文件不存在: {image_path}", file=sys.stderr)
        sys.exit(1)

    mime_type = get_mime_type(image_path)
    boundary = f"----WechatBoundary{os.urandom(16).hex()}"

    with open(image_path, "rb") as f:
        file_data = f.read()

    filename = os.path.basename(image_path)

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="media"; filename="{filename}"\r\n'
        f"Content-Type: {mime_type}\r\n\r\n"
    ).encode("utf-8") + file_data + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8") if e.fp else str(e)
        print(f"上传失败 HTTP {e.code}: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"网络错误: {e}", file=sys.stderr)
        sys.exit(1)

    if "media_id" in result:
        print(f"{result['media_id']}")
        return result["media_id"]
    else:
        print(f"上传失败: {result}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python upload_thumb.py <图片路径>", file=sys.stderr)
        sys.exit(1)
    upload_thumb(sys.argv[1])
