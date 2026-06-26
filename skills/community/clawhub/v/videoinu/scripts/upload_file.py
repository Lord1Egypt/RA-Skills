#!/usr/bin/env python3
"""
Upload a file and create a CoreNode.

Flow: get presign URL -> upload to TOS -> create CoreNode

Usage:
    python3 upload_file.py /path/to/file.png
    python3 upload_file.py /path/to/video.mp4
    python3 upload_file.py /path/to/script.txt

Output (JSON):
    {
      "core_node_id": "...",
      "file_url": "...",
      "asset_type": "image"
    }
"""

import argparse
import json
import mimetypes
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, api_post, upload_raw

ASSET_TYPE_MAP = {
    "image": ["image/png", "image/jpeg", "image/jpg", "image/webp", "image/gif"],
    "video": ["video/mp4", "video/quicktime", "video/webm", "video/avi"],
    "audio": ["audio/mpeg", "audio/wav", "audio/mp3", "audio/ogg", "audio/flac"],
}

MAX_FILE_SIZE = 200 * 1024 * 1024  # 200 MB


def detect_asset_type(mime: str) -> str:
    for asset_type, mimes in ASSET_TYPE_MAP.items():
        if mime in mimes:
            return asset_type
    if mime and mime.startswith("image/"):
        return "image"
    if mime and mime.startswith("video/"):
        return "video"
    if mime and mime.startswith("audio/"):
        return "audio"
    if mime and mime.startswith("text/"):
        return "text"
    return "file"


def get_format(filename: str) -> str:
    _, ext = os.path.splitext(filename)
    return ext.lstrip(".").lower() or "bin"


def main():
    parser = argparse.ArgumentParser(description="Upload a file and create CoreNode")
    parser.add_argument("file", help="Path to file to upload")
    args = parser.parse_args()

    require_access_key()

    filepath = os.path.expanduser(args.file)
    if not os.path.isfile(filepath):
        print(json.dumps({"error": f"File not found: {filepath}"}))
        sys.exit(1)

    file_size = os.path.getsize(filepath)
    if file_size > MAX_FILE_SIZE:
        print(json.dumps({"error": f"File too large ({file_size} bytes). Max is {MAX_FILE_SIZE} bytes."}))
        sys.exit(1)

    mime, _ = mimetypes.guess_type(filepath)
    mime = mime or "application/octet-stream"
    asset_type = detect_asset_type(mime)
    fmt = get_format(filepath)

    # For text files, read content and create CoreNode directly
    if asset_type == "text":
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        ids = api_post("/core_nodes", body={
            "nodes": [{"asset_type": "text", "content": content}]
        })
        core_node_id = ids[0] if isinstance(ids, list) else ""
        print(json.dumps({
            "core_node_id": core_node_id,
            "asset_type": "text",
            "content_length": len(content),
        }, indent=2))
        return

    # For binary files: presign -> upload -> create CoreNode
    presign = api_post("/core_nodes/upload/presign", body={
        "type": asset_type,
        "format": fmt,
    })
    upload_url = presign["upload_url"]
    file_url = presign["file_url"]

    with open(filepath, "rb") as f:
        file_bytes = f.read()

    upload_raw(upload_url, file_bytes, mime)

    # Create CoreNode
    ids = api_post("/core_nodes", body={
        "nodes": [{"asset_type": asset_type, "url": file_url}]
    })
    core_node_id = ids[0] if isinstance(ids, list) else ""

    print(json.dumps({
        "core_node_id": core_node_id,
        "file_url": file_url,
        "asset_type": asset_type,
    }, indent=2))


if __name__ == "__main__":
    main()
