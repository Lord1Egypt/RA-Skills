#!/usr/bin/env python3
"""
Web Content → Structured Markdown Converter (Unified Entry)

Auto-detects URL type and routes to the appropriate converter:
  - x.com / twitter.com → x-tweet-fetcher + tweet_to_md.py
  - mp.weixin.qq.com    → markitdown (WeChat plugin)
  - xiaohongshu.com     → markitdown (Xiaohongshu plugin)
  - weibo.com           → markitdown (generic)
  - youtube.com         → markitdown (YouTube support)
  - Other URLs          → markitdown (generic HTML)
  - Local files         → markitdown (PDF/DOCX/PPTX/XLSX/Images/Audio/etc.)

Usage:
  python3 web_to_md.py --url <url_or_path> --output <output.md>
  python3 web_to_md.py --url <url_or_path>  (prints to stdout)
  python3 web_to_md.py --url <tweet_url> --replies  (fetch thread replies)
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SKILLS_DIR = os.path.expanduser("~/.aily/workspace/skills")
TWEET_FETCHER = os.path.join(SKILLS_DIR, "x-tweet-fetcher/scripts/fetch_tweet.py")
SCRIPT_DIR = Path(__file__).parent
TWEET_TO_MD = str(SCRIPT_DIR / "tweet_to_md.py")


def _run(cmd, check=True):
    result = subprocess.run(cmd, capture_output=True, text=True, check=check)
    return result.stdout.strip()


def _detect_source(url_or_path: str) -> str:
    lower = url_or_path.lower()

    if "x.com" in lower or "twitter.com" in lower:
        return "twitter"
    if "mp.weixin.qq.com" in lower:
        return "wechat"
    if "weibo.com" in lower:
        return "weibo"
    if "xiaohongshu.com" in lower or "xhslink.com" in lower:
        return "xiaohongshu"
    if "youtube.com" in lower or "youtu.be" in lower:
        return "youtube"
    if lower.startswith("http://") or lower.startswith("https://"):
        return "html"

    ext = Path(lower).suffix
    file_map = {
        ".pdf": "pdf", ".docx": "docx", ".doc": "docx",
        ".pptx": "pptx", ".ppt": "pptx",
        ".xlsx": "xlsx", ".xls": "xlsx",
        ".png": "image", ".jpg": "image", ".jpeg": "image",
        ".gif": "image", ".bmp": "image", ".webp": "image", ".tiff": "image",
        ".mp3": "audio", ".wav": "audio", ".m4a": "audio", ".flac": "audio",
        ".csv": "csv", ".json": "json", ".xml": "xml",
        ".zip": "zip", ".epub": "epub",
        ".md": "markdown", ".txt": "text", ".html": "html_file", ".htm": "html_file",
    }
    return file_map.get(ext, "unknown")


def _convert_twitter(url: str, output_path: str = None, replies: bool = False) -> str:
    fetch_cmd = [sys.executable, TWEET_FETCHER, "--url", url, "--pretty"]
    if replies:
        fetch_cmd.append("--replies")

    try:
        json_str = _run(fetch_cmd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to fetch tweet: {e.stderr}", file=sys.stderr)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
        tmp.write(json_str)
        tmp_json = tmp.name

    convert_cmd = [sys.executable, TWEET_TO_MD, "--input", tmp_json]
    if output_path:
        convert_cmd.extend(["--output", output_path])

    try:
        result = _run(convert_cmd)
    finally:
        if os.path.exists(tmp_json):
            os.unlink(tmp_json)

    if output_path and os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            return f.read()
    return result


def _convert_markitdown(url_or_path: str, output_path: str = None) -> str:
    try:
        from markitdown import MarkItDown
    except ImportError:
        print("❌ markitdown not installed. Run: pip install markitdown", file=sys.stderr)
        sys.exit(1)

    md = MarkItDown()
    result = md.convert(url_or_path)
    content = result.markdown

    if output_path:
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Markdown saved: {out} ({len(content)} chars)", file=sys.stderr)

    return content


def convert(url_or_path: str, output_path: str = None, replies: bool = False) -> str:
    source_type = _detect_source(url_or_path)

    print(f"🔍 Detected source type: {source_type}", file=sys.stderr)

    if source_type == "twitter":
        return _convert_twitter(url_or_path, output_path, replies)
    else:
        return _convert_markitdown(url_or_path, output_path)


def main():
    parser = argparse.ArgumentParser(description="Web Content → Structured Markdown Converter")
    parser.add_argument("--url", required=True, help="URL or local file path to convert")
    parser.add_argument("--output", help="Output Markdown file path (default: stdout)")
    parser.add_argument("--replies", action="store_true", help="Fetch tweet replies (Twitter only)")
    args = parser.parse_args()

    content = convert(args.url, args.output, args.replies)

    if not args.output:
        print(content)


if __name__ == "__main__":
    main()
