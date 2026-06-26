#!/usr/bin/env python3
"""
Upload a local file to Vidau asset storage. Reads API key from env VIDAU_API_KEY or OpenClaw config.
Prints API JSON to stdout; use data.url as image_url / last_image_url / ref_image_urls in create_task.
Caches assetId by file content hash (env VIDAU_ASSET_CACHE or ~/.vidau_asset_cache.json) so the same file is not re-uploaded.
"""
import argparse
import hashlib
import json
import mimetypes
import os
import sys
import uuid
from typing import Tuple
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import api_client

API_BASE = "https://api.superaiglobal.com/v1"
UPLOAD_URL = f"{API_BASE}/asset/upload"


def _cache_path() -> str:
    return os.environ.get("VIDAU_ASSET_CACHE", os.path.expanduser("~/.vidau_asset_cache.json"))


def _file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def _load_cache() -> dict:
    p = _cache_path()
    if not os.path.isfile(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def _save_cache(cache: dict) -> None:
    p = _cache_path()
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def _build_multipart_body(file_path: str, field_name: str) -> Tuple[bytes, str]:
    """Build multipart/form-data body. Returns (body_bytes, boundary)."""
    boundary = uuid.uuid4().hex
    filename = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        file_data = f.read()
    content_type = mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    part = (
        f'--{boundary}\r\n'
        f'Content-Disposition: form-data; name="{field_name}"; filename="{filename}"\r\n'
        f'Content-Type: {content_type}\r\n\r\n'
    ).encode("utf-8") + file_data + f'\r\n--{boundary}--\r\n'.encode("utf-8")
    return part, boundary


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload a local file to Vidau; get back a URL for use in create_task."
    )
    parser.add_argument(
        "file",
        help="Local file path (image or video)",
    )
    parser.add_argument(
        "--field",
        default="file",
        help="Form field name (default: file)",
    )
    args = parser.parse_args()

    path = os.path.expanduser(args.file)
    if not os.path.isfile(path):
        print(f"Error: not a file: {path}", file=sys.stderr)
        sys.exit(1)

    file_hash = _file_sha256(path)
    cache = _load_cache()
    cached = cache.get(file_hash)
    if cached and cached.get("url") and cached.get("assetId"):
        out = {
            "code": "200",
            "message": "success",
            "data": {"url": cached["url"], "assetId": cached["assetId"]},
        }
        print(json.dumps(out, ensure_ascii=False))
        return

    api_key = api_client.get_api_key()
    if not api_key:
        print(
            "Error: VIDAU_API_KEY is not set. Register at https://www.superaiglobal.com/ "
            "and set apiKey or env.VIDAU_API_KEY in OpenClaw skills.entries.vidau.",
            file=sys.stderr,
        )
        sys.exit(1)

    body, boundary = _build_multipart_body(path, args.field)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
        "Content-Length": str(len(body)),
    }
    try:
        req = Request(UPLOAD_URL, data=body, headers=headers, method="POST")
        with urlopen(req, timeout=120) as resp:
            raw = resp.read()
    except HTTPError as e:
        try:
            err_body = e.read().decode("utf-8", errors="replace")
            msg = json.loads(err_body).get("message", err_body)
        except Exception:
            msg = str(e.reason)
        print(f"Upload failed: {msg}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Upload failed: {e.reason}", file=sys.stderr)
        sys.exit(1)

    raw_str = raw.decode("utf-8")
    print(raw_str)
    try:
        out = json.loads(raw_str)
    except json.JSONDecodeError as e:
        print(f"Response is not valid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    if out.get("code") != "200":
        msg = out.get("message", "Unknown error")
        print(f"API returned non-success: code={out.get('code')}, message={msg}", file=sys.stderr)
        sys.exit(1)

    data = out.get("data") or {}
    url_val = data.get("url")
    asset_id = data.get("assetId")
    if url_val and asset_id:
        cache[file_hash] = {"url": url_val, "assetId": asset_id}
        _save_cache(cache)


if __name__ == "__main__":
    main()
