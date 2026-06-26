#!/usr/bin/env python3
"""
WiseDiag Report CLI — Interpret medical report images via WiseDiag AI

Sub-commands: N/A (single-step workflow)

Usage:
    export WISEDIAG_API_KEY=your_api_key
    python3 report.py -f "/path/to/report.jpg"
    python3 report.py -f "/path/to/report.jpg" --question "请解读报告中的异常指标"
    python3 report.py -f "/path/to/r1.jpg" -f "/path/to/r2.jpg"
    python3 report.py --image "https://example.com/report.jpg"

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
REQUEST_TIMEOUT    = 180
UPLOAD_TIMEOUT     = 180
MAX_IMAGES         = 5
SUPPORTED_FORMATS  = (".pdf", ".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".webp")
MAX_FILE_SIZE_MB   = 50


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

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
# Core analysis — URL mode
# ---------------------------------------------------------------------------

def _interpret_via_url(
    image_urls: list[str],
    question: str,
    output_dir: str | None,
    name: str | None,
) -> bool:
    """Call WiseDiag photo_read API with image URLs and stream results."""
    key = _get_api_key()
    url = f"{DEFAULT_SERVICE_URL}/v1/medicine/photo_read"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    ts = int(time.time() * 1000)
    payload = {
        "image_list": image_urls,
        "messages": [{"role": "user", "content": question}],
        "topic_id": f"report_{ts}",
        "request_id": str(ts),
        "use_thinking": 1,
        "use_health_record": 0,
    }

    print(f"[*] Images    : {', '.join(image_urls)}")
    print(f"[*] Question  : {question}")
    print()

    return _stream_response(url, headers, payload, None, image_urls, question, output_dir, name)


# ---------------------------------------------------------------------------
# Core analysis — File upload mode
# ---------------------------------------------------------------------------

def _interpret_via_file(
    file_paths: list[str],
    question: str,
    output_dir: str | None,
    name: str | None,
) -> bool:
    """Upload local files via multipart and stream results."""
    key = _get_api_key()
    url = f"{DEFAULT_SERVICE_URL}/api/medicine/photo_read"
    headers = {"Authorization": f"Bearer {key}"}

    ts = int(time.time() * 1000)
    request_data = {
        "image_list": [],
        "messages": [{"role": "user", "content": question}],
        "topic_id": f"report_{ts}",
        "request_id": str(ts),
        "use_thinking": 1,
        "use_health_record": 0,
    }

    print(f"[*] Uploading local files:")
    for fp in file_paths:
        print(f"    - {fp}")
    print(f"[*] Question  : {question}")
    print()

    opened_files = []
    files_list = []
    try:
        for fp in file_paths:
            f = open(fp, "rb")
            opened_files.append(f)
            files_list.append(("files", (os.path.basename(fp), f)))

        request_part = ("request", (None, json.dumps(request_data), "application/json"))

        try:
            resp = requests.post(
                url,
                headers=headers,
                files=[request_part] + files_list,
                stream=True,
                timeout=UPLOAD_TIMEOUT,
            )
        except requests.Timeout:
            print(f"\n[!] Upload timed out after {UPLOAD_TIMEOUT}s.")
            return False
        except requests.ConnectionError as e:
            print(f"\n[!] Connection error: {e}")
            return False

    finally:
        for f in opened_files:
            f.close()

    if resp.status_code == 401:
        print("[!] Authentication failed. Check your API key.")
        return False
    if resp.status_code != 200:
        print(f"[!] Request failed: HTTP {resp.status_code}")
        print(resp.text[:300])
        return False

    return _parse_stream(resp, file_paths, question, output_dir, name, is_file_mode=True)


# ---------------------------------------------------------------------------
# Stream response parsing (shared)
# ---------------------------------------------------------------------------

def _stream_response(url, headers, payload, files_arg, image_sources, question, output_dir, name) -> bool:
    """Send JSON request and parse SSE stream."""
    try:
        with requests.post(
            url, headers=headers, json=payload,
            stream=True, timeout=REQUEST_TIMEOUT,
        ) as resp:
            if resp.status_code == 401:
                print("[!] Authentication failed. Check your API key.")
                return False
            if resp.status_code != 200:
                print(f"[!] Request failed: HTTP {resp.status_code}")
                print(resp.text[:300])
                return False
            return _parse_stream(resp, image_sources, question, output_dir, name, is_file_mode=False)

    except requests.Timeout:
        print(f"\n[!] Request timed out after {REQUEST_TIMEOUT}s.")
        return False
    except requests.ConnectionError as e:
        print(f"\n[!] Connection error: {e}")
        return False


def _parse_stream(resp, image_sources, question, output_dir, name, is_file_mode: bool) -> bool:
    """Parse SSE stream from photo_read response."""
    content_text = ""
    reasoning_text = ""
    vl_result = None
    in_thinking = False

    for line in resp.iter_lines():
        if not line:
            continue
        decoded = line.decode("utf-8")
        raw = decoded.split("data:")[-1].strip()

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

    print()

    # Save result
    if output_dir is None:
        out_dir = Path.cwd()
    else:
        out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    stem = name or f"report_{int(time.time())}"
    out_path = out_dir / f"{stem}.md"
    if out_path.exists():
        counter = 1
        while (out_dir / f"{stem}_{counter}.md").exists():
            counter += 1
        out_path = out_dir / f"{stem}_{counter}.md"
        print(f"[!] Name conflict, saving as: {out_path.name}")

    md = "# Medical Report Interpretation\n\n"
    if is_file_mode:
        for i, fp in enumerate(image_sources, 1):
            md += f"**File {i}:** {fp}\n\n"
    else:
        for i, url_item in enumerate(image_sources, 1):
            md += f"**Image {i}:** {url_item}\n\n"
    md += f"**Question:** {question}\n\n"

    if reasoning_text:
        md += f"## Thinking Process\n\n{reasoning_text}\n\n"

    md += f"## Interpretation\n\n{content_text}\n"

    if vl_result:
        md += (
            f"\n## OCR / Detection Details\n\n"
            f"```json\n{json.dumps(vl_result, ensure_ascii=False, indent=2)}\n```\n"
        )

    md += "\n---\n\n> ⚠️ 本报告由 AI 生成，仅供参考，不构成医疗诊断或治疗建议。如有健康问题请咨询专业医生。\n"

    out_path.write_text(md, encoding="utf-8")
    print(f"\n[+] Result saved: {out_path}")
    return True


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="WiseDiag Report CLI — Interpret medical report images via WiseDiag AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 report.py -f "/path/to/report.jpg"
  python3 report.py -f "/path/to/report.jpg" --question "请解读异常指标"
  python3 report.py -f "/path/to/r1.jpg" -f "/path/to/r2.jpg"
  python3 report.py --image "https://example.com/report.jpg"
  python3 report.py --image "https://example.com/report.jpg" -n "bloodtest_20260324"
        """,
    )

    parser.add_argument(
        "-f", "--file", metavar="PATH", action="append", dest="files",
        help="Local file path to upload (PDF/image, repeat for multiple, max 5). Mutually exclusive with --image.",
    )
    parser.add_argument(
        "--image", metavar="URL", action="append", dest="images",
        help="Public URL of the report image (repeat for multiple, max 5). Mutually exclusive with --file.",
    )
    parser.add_argument(
        "--question", default="请帮我解读这份报告单，重点说明异常指标及建议。",
        help="Question to ask about the report",
    )
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: current working directory)",
    )
    parser.add_argument(
        "-n", "--name",
        help="Output filename stem (without extension)",
    )

    args = parser.parse_args()

    has_files = bool(args.files)
    has_images = bool(args.images)

    if not has_files and not has_images:
        print("[!] Error: must provide --file or --image (mutually exclusive).")
        sys.exit(1)

    if has_files and has_images:
        print("[!] Error: --file and --image are mutually exclusive. Use one or the other.")
        sys.exit(1)

    if has_files:
        if len(args.files) > MAX_IMAGES:
            print(f"[!] Error: maximum {MAX_IMAGES} files per request.")
            sys.exit(1)
        for fp in args.files:
            if not os.path.isfile(fp):
                print(f"[!] File not found: {fp}")
                sys.exit(1)
            ext = os.path.splitext(fp)[1].lower()
            if ext not in SUPPORTED_FORMATS:
                print(f"[!] Unsupported file format: {ext} (file: {fp})")
                print(f"    Supported: {', '.join(SUPPORTED_FORMATS)}")
                sys.exit(1)
            size_mb = os.path.getsize(fp) / (1024 * 1024)
            if size_mb > MAX_FILE_SIZE_MB:
                print(f"[!] File too large: {fp} ({size_mb:.1f} MB, max {MAX_FILE_SIZE_MB} MB)")
                sys.exit(1)
        success = _interpret_via_file(
            file_paths=args.files,
            question=args.question,
            output_dir=args.output,
            name=args.name,
        )
    else:
        if len(args.images) > MAX_IMAGES:
            print(f"[!] Error: maximum {MAX_IMAGES} images per request.")
            sys.exit(1)
        success = _interpret_via_url(
            image_urls=args.images,
            question=args.question,
            output_dir=args.output,
            name=args.name,
        )

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
