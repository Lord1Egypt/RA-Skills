#!/usr/bin/env python3
"""
Extract and clean subtitles from a YouTube / Bilibili video URL.
Outputs JSON with deduplicated subtitle entries, each with timestamp and text.

Usage:
    python3 extract_subtitles.py <url> [--output <path>] [--lang <lang>]
                                       [--cookies-from-browser <browser>]
                                       [--cookies <cookie_file>]

Output JSON format:
    [{"t": "mm:ss", "s": <seconds_float>, "text": "<content>"}, ...]

YouTube 注意事项:
  - 若遇到 "Sign in to confirm" 或 "Requested format is not available"，
    需要传入 --cookies-from-browser chrome（或 firefox/safari），
    脚本会自动先导出 cookies 文件，再以 storyboard 格式触发字幕下载。
  - 字幕格式优先尝试 VTT（与 yt-dlp storyboard 下载兼容），失败则回退 SRT。

哔哩哔哩注意事项:
  - 用 --lang zh 或 --lang zh-Hans 提取中文字幕。
  - 部分视频需要登录 cookie，用 --cookies-from-browser chrome。
  - 哔哩哔哩上传字幕（非 AI 生成）用 --write-subs 而非 --write-auto-subs，
    脚本已自动兼容处理。
"""

import sys
import re
import json
import subprocess
import tempfile
import os
import argparse
from collections import defaultdict


def ensure_yt_dlp():
    try:
        import yt_dlp  # noqa
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "yt-dlp", "-q", "--break-system-packages"],
            stderr=subprocess.DEVNULL
        )


def _run_yt_dlp(extra_args: list, url: str, tmpdir: str, lang: str) -> str | None:
    """Run yt-dlp with given args, return raw subtitle text (srt or vtt) or None."""
    out_tmpl = os.path.join(tmpdir, "sub")
    # Try VTT first (more reliable with storyboard download)
    for sub_fmt, convert_args in [
        ("vtt", []),
        ("srt", ["--convert-subs", "srt"]),
    ]:
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--write-auto-subs",
            "--write-subs",          # also pick up manually uploaded subs (Bilibili)
            "--sub-langs", lang,
            "--sub-format", sub_fmt,
            "-o", out_tmpl,
            "--quiet",
            *convert_args,
            *extra_args,
            url,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        for f in os.listdir(tmpdir):
            if f.endswith(f".{sub_fmt}") or f.endswith(".srt"):
                path = os.path.join(tmpdir, f)
                with open(path) as fh:
                    return fh.read(), f.rsplit(".", 1)[-1]
    return None, None


def download_subtitles(url: str, lang: str = "en",
                       cookies_browser: str | None = None,
                       cookies_file: str | None = None) -> tuple[str | None, str]:
    """
    Download subtitles via yt-dlp.
    Returns (raw_content, format) or (None, '').

    Strategy:
    1. Fast path: --skip-download (no video needed)
    2. Fallback: if cookies needed or format unavailable, export cookies then
       download with storyboard format (-f sb3) which is always available on YouTube.
    """
    base_cookie_args = []
    if cookies_file and os.path.exists(cookies_file):
        base_cookie_args = ["--cookies", cookies_file]
    elif cookies_browser:
        base_cookie_args = ["--cookies-from-browser", cookies_browser]

    with tempfile.TemporaryDirectory() as tmpdir:
        # --- Fast path: skip-download ---
        content, fmt = _run_yt_dlp(
            ["--skip-download", *base_cookie_args], url, tmpdir, lang
        )
        if content:
            return content, fmt

    # --- Fallback: storyboard format (always available on YouTube) ---
    # First export cookies to a file so we don't re-authenticate per attempt
    if cookies_browser and not cookies_file:
        cookies_file = "/tmp/yt-cookies-export.txt"
        subprocess.run(
            [sys.executable, "-m", "yt_dlp",
             "--cookies-from-browser", cookies_browser,
             "--cookies", cookies_file,
             "--skip-download", "-o", "/tmp/yt_cookie_export_dummy", "--quiet",
             url],
            capture_output=True
        )

    cookie_args = []
    if cookies_file and os.path.exists(cookies_file):
        cookie_args = ["--cookies", cookies_file]
    elif cookies_browser:
        cookie_args = ["--cookies-from-browser", cookies_browser]

    if not cookie_args:
        print("[extract_subtitles] HINT: If YouTube returns a bot-check error, "
              "retry with: --cookies-from-browser chrome", file=sys.stderr)
        return None, ""

    print("[extract_subtitles] Fast path failed, retrying with storyboard format + cookies...",
          file=sys.stderr)
    with tempfile.TemporaryDirectory() as tmpdir:
        content, fmt = _run_yt_dlp(
            ["-f", "sb3", *cookie_args], url, tmpdir, lang
        )
        if content:
            return content, fmt

    return None, ""


def parse_vtt(content: str) -> list[dict]:
    """Parse WebVTT content (with inline timing tags) into subtitle entries."""
    blocks = re.split(r'\n\n+', content)
    entries = []
    seen_texts = set()
    for block in blocks:
        lines = block.strip().split('\n')
        ts_line = next((l for l in lines if '-->' in l), None)
        if not ts_line:
            continue
        # Parse start timestamp (supports HH:MM:SS.mmm and MM:SS.mmm)
        ts_match = re.match(r'(?:(\d+):)?(\d+):(\d+)[.,](\d+)', ts_line)
        if not ts_match:
            continue
        groups = ts_match.groups()
        h = int(groups[0] or 0)
        m, s, ms = int(groups[1]), int(groups[2]), int(groups[3])
        total = h * 3600 + m * 60 + s + ms / 1000.0
        # Extract text lines after timestamp
        ts_idx = lines.index(ts_line)
        raw = ' '.join(lines[ts_idx + 1:])
        # Strip inline timing tags <00:00:00.000><c>...</c>
        clean = re.sub(r'<[^>]+>', '', raw).strip()
        clean = re.sub(r'\s+', ' ', clean).strip()
        if not clean or clean in seen_texts:
            continue
        seen_texts.add(clean)
        t_str = f"{int(total)//60:02d}:{int(total)%60:02d}"
        entries.append({'t': t_str, 's': round(total, 1), 'text': clean})
    return entries


def parse_srt(content: str) -> list[dict]:
    """Parse SRT content into list of {s, t, text} dicts, deduplicated."""
    blocks = re.split(r"\n\n+", content.strip())
    entries = []
    for block in blocks:
        lines = block.strip().split("\n")
        ts_line = next((l for l in lines if re.match(r"\d{2}:\d{2}:\d{2}", l)), None)
        if not ts_line:
            continue
        start = ts_line.split("-->")[0].strip()
        h, m, s = start.replace(",", ".").split(":")
        sec = int(h) * 3600 + int(m) * 60 + float(s)
        ts_idx = lines.index(ts_line)
        text_lines = [re.sub(r"<[^>]+>", "", l) for l in lines[ts_idx + 1:] if l.strip()]
        text = " ".join(text_lines).strip()
        if text:
            entries.append((sec, text))

    # Group into ~4s buckets, keep longest text per bucket
    chunks = defaultdict(list)
    for sec, text in entries:
        chunks[int(sec / 4)].append((sec, text))

    result = []
    last_text = ""
    for key in sorted(chunks):
        sec, text = max(chunks[key], key=lambda x: len(x[1]))
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r">>\s*\[.*?\]\s*>>", "", text).strip()
        if len(text) < 5 or text == last_text:
            continue
        # deduplicate by first 50 chars
        total = int(sec)
        ts_fmt = f"{total // 60:02d}:{total % 60:02d}"
        result.append({"t": ts_fmt, "s": round(sec, 1), "text": text})
        last_text = text

    # Final pass: remove near-duplicates
    seen, final = set(), []
    for e in result:
        key = e["text"][:50]
        if key in seen:
            continue
        seen.add(key)
        final.append(e)

    return final


def main():
    parser = argparse.ArgumentParser(description="Extract YouTube/Bilibili subtitles to JSON")
    parser.add_argument("url", help="Video URL (YouTube or Bilibili)")
    parser.add_argument("--output", "-o", help="Output JSON file path (default: stdout)")
    parser.add_argument("--lang", default="en",
                        help="Subtitle language (default: en; use zh/zh-Hans for Chinese)")
    parser.add_argument("--cookies-from-browser",
                        help="Export cookies from browser for auth (e.g. chrome, firefox, safari)")
    parser.add_argument("--cookies",
                        help="Path to Netscape cookies.txt file")
    args = parser.parse_args()

    ensure_yt_dlp()

    print(f"[extract_subtitles] Downloading subtitles for: {args.url}", file=sys.stderr)
    content, fmt = download_subtitles(
        args.url, args.lang,
        cookies_browser=args.cookies_from_browser,
        cookies_file=args.cookies,
    )
    if not content:
        print("[extract_subtitles] ERROR: No subtitles found. Video may not have auto-generated captions.", file=sys.stderr)
        sys.exit(1)

    if fmt == "vtt":
        entries = parse_vtt(content)
        print(f"[extract_subtitles] Parsed {len(entries)} entries from VTT", file=sys.stderr)
    else:
        entries = parse_srt(content)
        print(f"[extract_subtitles] Parsed {len(entries)} entries from SRT", file=sys.stderr)

    output = json.dumps(entries, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"[extract_subtitles] Saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
