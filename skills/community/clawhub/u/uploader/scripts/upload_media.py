#!/usr/bin/env python3
"""
Upload a file to Astron Claw Bridge Server via POST /api/media/upload.
Host and token are auto-read from /root/.openclaw/openclaw.json.

Usage:
    python upload_media.py <file_path> [--session-id <sid>]
"""
import sys
import os
import json
import argparse
from urllib.parse import urlparse
import requests

CONFIG_PATH = "/root/.openclaw/openclaw.json"


def read_openclaw_config(config_path=CONFIG_PATH):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        bridge = config["plugins"]["entries"]["astron-claw"]["config"]["bridge"]
        host = urlparse(bridge["url"]).netloc
        token = bridge["token"]
        return {"host": host, "token": token}
    except FileNotFoundError:
        print(f"Error: config not found at {config_path}")
    except (KeyError, TypeError):
        print("Error: bridge config missing in openclaw.json")
    except json.JSONDecodeError:
        print(f"Error: invalid JSON in {config_path}")
    return None


def upload_media(file_path: str, session_id: str = None) -> dict | None:
    config = read_openclaw_config()
    if not config:
        return None

    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        return None

    url = f"http://{config['host']}/api/media/upload"
    filename = os.path.basename(file_path)

    with open(file_path, "rb") as f:
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {config['token']}"},
            files={"file": (filename, f)},
            data={"sessionId": session_id} if session_id else {},
        )

    if resp.status_code != 200:
        print(f"Upload failed ({resp.status_code}): {resp.text}")
        return None

    result = resp.json()
    print(f"fileName:    {result['fileName']}")
    print(f"mimeType:    {result['mimeType']}")
    print(f"fileSize:    {result['fileSize']}")
    print(f"sessionId:   {result['sessionId']}")
    print(f"downloadUrl: {result['downloadUrl']}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a file to Astron Claw Bridge")
    parser.add_argument("file", help="Path to the file to upload")
    parser.add_argument("--session-id", help="Optional session ID", default=None)
    args = parser.parse_args()

    if not upload_media(args.file, args.session_id):
        sys.exit(1)
