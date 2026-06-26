#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.request
import urllib.error


def to_data_uri(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Call SiliconFlow PaddleOCR-VL-1.5")
    ap.add_argument("--prompt", required=True, help="User prompt")
    ap.add_argument("--image-path", help="Local image path")
    ap.add_argument("--image-url", help="Remote image URL")
    ap.add_argument("--max-tokens", type=int, default=512)
    ap.add_argument("--base-url", default="https://api.siliconflow.cn/v1")
    ap.add_argument("--model", default="PaddlePaddle/PaddleOCR-VL-1.5")
    args = ap.parse_args()

    key = os.getenv("SILICONFLOW_API_KEY", "").strip()
    if not key:
        key_file = os.path.expanduser("~/.openclaw/secrets/siliconflow_api_key")
        if os.path.exists(key_file):
            with open(key_file, "r", encoding="utf-8") as f:
                key = f.read().strip()
    if not key:
        print("ERROR: SILICONFLOW_API_KEY is missing", file=sys.stderr)
        return 2

    content = [{"type": "text", "text": args.prompt}]

    if args.image_path and args.image_url:
        print("ERROR: use only one of --image-path or --image-url", file=sys.stderr)
        return 2

    if args.image_path:
        if not os.path.exists(args.image_path):
            print(f"ERROR: image not found: {args.image_path}", file=sys.stderr)
            return 2
        content.append({"type": "image_url", "image_url": {"url": to_data_uri(args.image_path)}})
    elif args.image_url:
        content.append({"type": "image_url", "image_url": {"url": args.image_url}})

    payload = {
        "model": args.model,
        "messages": [{"role": "user", "content": content if len(content) > 1 else args.prompt}],
        "max_tokens": args.max_tokens,
    }

    url = args.base_url.rstrip("/") + "/chat/completions"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(body)
            return 0
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="replace")
        print(err, file=sys.stderr)
        return 1
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
