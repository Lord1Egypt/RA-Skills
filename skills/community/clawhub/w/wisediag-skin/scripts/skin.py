#!/usr/bin/env python3
"""
WiseDiag Skin CLI — Skin Disease Analysis from a local image file (powered by WiseDiag)

Usage:
    export WISEDIAG_API_KEY=your_api_key
    python3 skin.py -f skin.jpg
    python3 skin.py -f skin.jpg --question "这个皮疹是什么原因？"
    python3 skin.py -f rash.png -n "skin_20260324"

Get API key: https://console.wisediag.com/apiKeyManage
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

import requests


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_SERVICE_URL = "https://openapi.wisediag.com"
REQUEST_TIMEOUT     = 120   # seconds
MAX_FILE_SIZE_MB    = 50
DEFAULT_QUESTION    = "请分析这张皮肤图片，判断可能是什么皮肤问题，并给出建议。"

IMAGE_EXTENSIONS = {
    "jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff", "tif",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mime(filename: str) -> str:
    ext = Path(filename).suffix.lstrip(".").lower()
    if ext in ("jpg", "jpeg"):
        return "image/jpeg"
    return f"image/{ext}"


def _get_api_key() -> str:
    key = os.environ.get("WISEDIAG_API_KEY", "")
    if not key:
        print("""
[!] Error: WISEDIAG_API_KEY is not set.

    export WISEDIAG_API_KEY=your_api_key

Get a key at: https://console.wisediag.com/apiKeyManage
""")
        raise SystemExit(1)
    return key


# ---------------------------------------------------------------------------
# Core analysis
# ---------------------------------------------------------------------------

def analyze_skin(
    image_path: str,
    question:   str        = DEFAULT_QUESTION,
    output_dir: str | None = None,
    name:       str | None = None,
) -> bool:
    """Call WiseDiag skin API with file upload and stream results to stdout."""

    p = Path(image_path)

    if not p.exists():
        print(f"[!] File not found: {p}")
        return False

    ext = p.suffix.lstrip(".").lower()
    if ext not in IMAGE_EXTENSIONS:
        print(f"[!] Unsupported format: {p}  (supported: {', '.join(sorted(IMAGE_EXTENSIONS))})")
        return False

    size_mb = p.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        print(f"[!] File too large: {p.name} ({size_mb:.1f} MB, limit {MAX_FILE_SIZE_MB} MB)")
        return False

    key = _get_api_key()

    url     = f"{DEFAULT_SERVICE_URL}/api/medicine/chat"
    headers = {
        "Authorization": f"Bearer {key}",
    }

    ts = int(time.time() * 1000)
    request_data = {
        "model": "zzkj-chat",
        "task_name": "skin",
        "image_list": [],
        "messages": [{"role": "user", "content": question}],
        "topic_id": f"skin_{ts}",
        "request_id": str(ts),
        "user_id": "",
        "member_id": "sample_1",
        "query_understand": 0,
        "local_DB": 0,
        "use_ch_medicine": 0,
        "expert_DB": 0,
        "web_engine": 0,
        "use_health_record": 0,
        "product_open": 1,
        "language": "zh",
    }

    print(f"[*] Analyzing : {p.name}")
    print(f"[*] Question  : {question}")
    print()

    content_text = ""
    reasoning_text = ""
    vl_result    = None
    in_thinking  = False

    try:
        with open(p, "rb") as fh:
            request_part = ("request", (None, json.dumps(request_data, ensure_ascii=False), "application/json"))
            file_part = ("files", (p.name, fh, _mime(p.name)))

            with requests.post(
                url, headers=headers, files=[request_part, file_part],
                stream=True, timeout=REQUEST_TIMEOUT,
            ) as resp:

                if resp.status_code == 401:
                    print("[!] Authentication failed. Check your API key.")
                    return False

                if resp.status_code != 200:
                    print(f"[!] Request failed: HTTP {resp.status_code}")
                    print(resp.text[:300])
                    return False

                for line in resp.iter_lines():
                    if not line:
                        continue
                    decoded = line.decode("utf-8")
                    raw     = decoded.split("data:")[-1].strip()

                    if raw == "[DONE]":
                        break

                    try:
                        data = json.loads(raw)
                    except json.JSONDecodeError:
                        continue

                    t = data.get("type", "")

                    if t == "reasoning_content":
                        chunk = data.get("content") or ""
                        if chunk:
                            if not in_thinking:
                                print("[Thinking] ", end="", flush=True)
                                in_thinking = True
                            print(chunk, end="", flush=True)
                            reasoning_text += chunk

                    elif t == "content":
                        if in_thinking:
                            print()
                            print()
                            in_thinking = False
                        chunk = data.get("content") or ""
                        print(chunk, end="", flush=True)
                        content_text += chunk

                    elif t == "vl_complete":
                        vl_result = data.get("data")

    except requests.Timeout:
        print("\n[!] Request timed out.")
        return False

    except requests.ConnectionError as e:
        print(f"\n[!] Connection error: {e}")
        return False

    print()  # newline after streaming output

    # -----------------------------------------------------------------------
    # Save result to Markdown
    # -----------------------------------------------------------------------
    if output_dir is None:
        out_dir = Path.home() / ".openclaw" / "workspace" / "WiseDiag-Skin"
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    stem     = name or f"skin_{int(time.time())}"
    out_path = out_dir / f"{stem}.md"
    if out_path.exists():
        counter = 1
        while (out_dir / f"{stem}_{counter}.md").exists():
            counter += 1
        out_path = out_dir / f"{stem}_{counter}.md"
        print(f"[!] Name conflict, saving as: {out_path.name}")

    md  = f"# WiseDiag Skin Analysis\n\n"
    md += f"**Image:** {p.name}\n\n"
    md += f"**Question:** {question}\n\n"

    if reasoning_text:
        md += f"## Thinking Process\n\n{reasoning_text}\n\n"

    md += f"## Result\n\n{content_text}\n"

    if vl_result:
        md += (
            f"\n## Detection Details\n\n"
            f"```json\n{json.dumps(vl_result, ensure_ascii=False, indent=2)}\n```\n"
        )

    md += "\n---\n\n> ⚠️ For reference only. Not a medical diagnosis.\n"

    out_path.write_text(md, encoding="utf-8")
    print(f"\n[+] Result saved: {out_path}")
    return True


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="WiseDiag Skin CLI — AI skin disease analysis from a local image file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 skin.py -f skin.jpg
  python3 skin.py -f skin.jpg --question "这个皮疹是什么原因？"
  python3 skin.py -f rash.png -n "skin_20260324"
        """,
    )

    parser.add_argument(
        "-f", "--file", required=True, metavar="FILE",
        help="Input image file: jpg/png/webp/gif/bmp/tiff (required)",
    )
    parser.add_argument(
        "--question", default=DEFAULT_QUESTION,
        help="Question about the skin image",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: ~/.openclaw/workspace/WiseDiag-Skin)",
    )
    parser.add_argument(
        "-n", "--name",
        help="Output filename stem",
    )

    args = parser.parse_args()

    success = analyze_skin(
        image_path = args.file,
        question   = args.question,
        output_dir = args.output,
        name       = args.name,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
