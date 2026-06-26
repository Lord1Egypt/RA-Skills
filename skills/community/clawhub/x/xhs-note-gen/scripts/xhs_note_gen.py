#!/usr/bin/env python3
"""Generate XiaoHongShu (XHS) notes via content-marketing-dashboard API.

Endpoint: POST /content/quick-note/generate
Auth: not required

Exit codes:
- 0: success
- 2: unexpected response format
- 3: HTTP error or backend error
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional


def _http_json(method: str, url: str, headers: Dict[str, str], body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    data = None
    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
        headers = {**headers, "Content-Type": "application/json"}

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except Exception:
            payload = {"raw": raw}
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {payload}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default="https://xiaonian.cc/employee-console/dashboard/v2/api", help="API base url")
    ap.add_argument("--task-description", required=True, help="User requirement / request_desc")
    ap.add_argument("--audience", default="小红书用户", help="Target audience")
    ap.add_argument("--tone", default="友好自然", help="Account tone")
    ap.add_argument("--character", default="专业分享者", help="Persona")
    ap.add_argument("--note-type", default="", help="Note type (optional; empty means auto)")
    ap.add_argument("--generate-num", type=int, default=1, help="How many note variants to generate (repeats the request). Default: 1")

    ap.add_argument("--generate-image", action="store_true", default=True, help="Generate images (default on)")
    ap.add_argument("--no-generate-image", dest="generate_image", action="store_false", help="Do not generate images")
    ap.add_argument("--image-num", type=int, default=1, help="Number of images to generate per note")
    args = ap.parse_args()

    base = args.base_url.rstrip("/")
    url = f"{base}/content/quick-note/generate"

    notes: List[Dict[str, Any]] = []
    raws: List[Any] = []

    for _ in range(max(1, int(args.generate_num))):
        body = {
            "task_description": args.task_description,
            "audience": args.audience,
            "tone": args.tone,
            "character": args.character,
            "note_type": (args.note_type or None),
            "generate_image": bool(args.generate_image),
            "image_num": int(args.image_num),
        }

        try:
            resp = _http_json("POST", url, headers={}, body=body)
        except Exception as e:
            sys.stderr.write(str(e) + "\n")
            return 3

        if isinstance(resp, dict) and resp.get("success") is False:
            sys.stderr.write(f"API error: {resp.get('message', resp)}\n")
            return 3

        title = resp.get("title")
        content = resp.get("content")
        tags = resp.get("tags")
        image_urls = resp.get("image_urls")
        note_type = resp.get("note_type")

        if not title and not content:
            sys.stderr.write(f"Unexpected response: {resp}\n")
            return 2

        notes.append({
            "title": title,
            "content": content,
            "tags": tags or [],
            "image_urls": image_urls or [],
            "note_type": note_type,
        })
        raws.append(resp)

    out = {"state": "SUCCESS", "notes": notes, "raw": raws}
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
