#!/usr/bin/env python3
"""
Video Metadata Fetcher

Detects the video platform from a URL, invokes the appropriate tool (BBDown for
Bilibili, yt-dlp for YouTube), and emits a unified JSON metadata blob.

Usage:
    python fetch_metadata.py <url> [--bbdown <path>] [--ytdlp <path>] [--ffmpeg-path <path>]

Environment variables (used as fallback when CLI flags are absent):
    BBDOWN_PATH      — full path to BBDown.exe
    YTDLP_PATH       — full path to yt-dlp.exe
    FFMPEG_PATH      — placeholder ffmpeg path for BBDown (any existing exe works)

Output (stdout, JSON):
    {
        "platform": "bilibili" | "youtube",
        "video_id": "BV...",                  # or "dQw4w9WgXcQ"
        "title": "...",
        "uploader": "...",
        "uploader_url": "...",
        "duration_seconds": 908,
        "publish_date": "2026-05-16",         # ISO date if available
        "url": "<canonical URL>"
    }

Exit codes:
    0 — success
    1 — invalid URL / unsupported platform
    2 — required tool missing
    3 — tool ran but metadata could not be parsed
"""

from __future__ import annotations

import argparse
import json
import locale
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Make our own stdout/stderr UTF-8 so JSON output and error messages don't
# get mangled by the host console's legacy code page (cp936 on zh-CN Windows).
for _stream_name in ("stdout", "stderr"):
    _stream = getattr(sys, _stream_name, None)
    if _stream is not None and hasattr(_stream, "reconfigure"):
        try:
            _stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


def _decode_tool_output(raw: bytes) -> str:
    """Decode stdout/stderr bytes from BBDown / yt-dlp.

    These tools write in the host console's code page: UTF-8 on POSIX and
    modern Windows configurations, but cp936 (GBK) on a default zh-CN Windows.
    We try UTF-8 first; if it fails strict-mode, we fall back to the locale's
    preferred encoding (which on Windows is the active console code page).
    Two attempts are enough — no scoring needed.
    """
    if not raw:
        return ""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fallback = locale.getpreferredencoding(False) or "cp936"
        return raw.decode(fallback, errors="replace")


BILIBILI_PATTERNS = [
    re.compile(r"bilibili\.com/video/(BV[0-9A-Za-z]+)", re.I),
    re.compile(r"bilibili\.com/video/(av\d+)", re.I),
    re.compile(r"b23\.tv/([0-9A-Za-z]+)", re.I),
]

YOUTUBE_PATTERNS = [
    re.compile(r"youtube\.com/watch\?v=([0-9A-Za-z_-]{11})"),
    re.compile(r"youtu\.be/([0-9A-Za-z_-]{11})"),
    re.compile(r"youtube\.com/shorts/([0-9A-Za-z_-]{11})"),
]


def detect_platform(url: str) -> tuple[str, str] | None:
    """Return (platform, video_id) tuple or None if unrecognized."""
    for p in BILIBILI_PATTERNS:
        m = p.search(url)
        if m:
            return ("bilibili", m.group(1))
    for p in YOUTUBE_PATTERNS:
        m = p.search(url)
        if m:
            return ("youtube", m.group(1))
    return None


def find_tool(explicit: str | None, env_var: str, candidates: list[str]) -> str | None:
    """Locate an executable via explicit arg → env var → PATH search."""
    if explicit:
        if Path(explicit).is_file():
            return explicit
        return None
    env_val = os.environ.get(env_var)
    if env_val and Path(env_val).is_file():
        return env_val
    for name in candidates:
        found = shutil.which(name)
        if found:
            return found
    return None


# --- Bilibili (BBDown) ----------------------------------------------------------

# Sample BBDown lines we parse:
#   [2026-05-25 21:46:20.504] - 视频标题: 撤离玩法设计迭代观察【游戏提灯#40】
#   [2026-05-25 21:46:20.504] - 发布时间: 2026-05-16 14:35:15 +08:00
#   [2026-05-25 21:46:20.504] - UP主页: https://space.bilibili.com/11212682
#   [2026-05-25 21:46:20.504] - P1: [38372118417] [撤离玩法设计迭代观察【游戏提灯#40】] [15m08s]

BBDOWN_TITLE_RE = re.compile(r"视频标题:\s*(.+?)\s*$", re.M)
BBDOWN_PUBLISH_RE = re.compile(r"发布时间:\s*(\d{4}-\d{2}-\d{2})", re.M)
BBDOWN_UPLOADER_URL_RE = re.compile(r"UP主页:\s*(\S+)", re.M)
BBDOWN_DURATION_RE = re.compile(r"\]\s*\[(\d+)m(\d+)s\]")


def fetch_bilibili(
    url: str, video_id: str, bbdown: str, ffmpeg_placeholder: str
) -> dict:
    cmd = [
        bbdown,
        url,
        "--only-show-info",
        "--ffmpeg-path",
        ffmpeg_placeholder,
    ]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        timeout=60,
    )
    output = _decode_tool_output(proc.stdout) + "\n" + _decode_tool_output(proc.stderr)

    title_m = BBDOWN_TITLE_RE.search(output)
    publish_m = BBDOWN_PUBLISH_RE.search(output)
    uploader_url_m = BBDOWN_UPLOADER_URL_RE.search(output)
    duration_m = BBDOWN_DURATION_RE.search(output)

    if not title_m:
        raise RuntimeError(
            f"BBDown ran but title not found in output. Raw output:\n{output[:1000]}"
        )

    duration_seconds = None
    if duration_m:
        duration_seconds = int(duration_m.group(1)) * 60 + int(duration_m.group(2))

    return {
        "platform": "bilibili",
        "video_id": video_id,
        "title": title_m.group(1).strip(),
        "uploader": None,  # BBDown doesn't print uploader name in --only-show-info
        "uploader_url": uploader_url_m.group(1) if uploader_url_m else None,
        "duration_seconds": duration_seconds,
        "publish_date": publish_m.group(1) if publish_m else None,
        "url": url,
    }


# --- YouTube (yt-dlp) -----------------------------------------------------------


def fetch_youtube(url: str, video_id: str, ytdlp: str) -> dict:
    """Use yt-dlp --print with a structured template."""
    cmd = [
        ytdlp,
        "--skip-download",
        "--no-warnings",
        "--print",
        "%(.{id,title,uploader,uploader_url,duration,upload_date,webpage_url})j",
        url,
    ]
    proc = subprocess.run(
        cmd,
        capture_output=True,
        timeout=60,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"yt-dlp failed (exit {proc.returncode}):\n"
            f"{_decode_tool_output(proc.stderr)[:1000]}"
        )

    stdout_text = _decode_tool_output(proc.stdout)
    line = stdout_text.strip().splitlines()[0] if stdout_text.strip() else ""
    if not line:
        raise RuntimeError("yt-dlp returned no output")

    data = json.loads(line)
    upload_date = data.get("upload_date")  # YYYYMMDD
    publish_date = None
    if upload_date and len(upload_date) == 8:
        publish_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:8]}"

    return {
        "platform": "youtube",
        "video_id": data.get("id") or video_id,
        "title": data.get("title"),
        "uploader": data.get("uploader"),
        "uploader_url": data.get("uploader_url"),
        "duration_seconds": data.get("duration"),
        "publish_date": publish_date,
        "url": data.get("webpage_url") or url,
    }


# --- main ----------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch unified metadata for a Bilibili or YouTube video URL."
    )
    parser.add_argument("url", help="Video URL")
    parser.add_argument("--bbdown", help="Path to BBDown.exe")
    parser.add_argument("--ytdlp", help="Path to yt-dlp.exe")
    parser.add_argument(
        "--ffmpeg-path",
        help="Placeholder ffmpeg path required by BBDown's startup check",
    )
    args = parser.parse_args()

    detection = detect_platform(args.url)
    if not detection:
        print(
            f"ERROR: URL is neither Bilibili nor YouTube: {args.url}", file=sys.stderr
        )
        return 1
    platform, video_id = detection

    try:
        if platform == "bilibili":
            bbdown = find_tool(args.bbdown, "BBDOWN_PATH", ["BBDown", "BBDown.exe"])
            if not bbdown:
                print(
                    "ERROR: BBDown not found. Pass --bbdown <path> or set BBDOWN_PATH.",
                    file=sys.stderr,
                )
                return 2
            ffmpeg = _resolve_ffmpeg_placeholder(args)
            if not ffmpeg:
                print(
                    "ERROR: BBDown's startup check requires --ffmpeg-path. Pass any "
                    "existing executable path (BBDown does not validate it as ffmpeg "
                    "in subtitle-only mode), or set FFMPEG_PATH.",
                    file=sys.stderr,
                )
                return 2
            metadata = fetch_bilibili(args.url, video_id, bbdown, ffmpeg)

        elif platform == "youtube":
            ytdlp = find_tool(args.ytdlp, "YTDLP_PATH", ["yt-dlp", "yt-dlp.exe"])
            if not ytdlp:
                print(
                    "ERROR: yt-dlp not found. Pass --ytdlp <path> or set YTDLP_PATH.",
                    file=sys.stderr,
                )
                return 2
            metadata = fetch_youtube(args.url, video_id, ytdlp)
        else:
            return 1

    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 3
    except subprocess.TimeoutExpired:
        print("ERROR: tool timed out (60s)", file=sys.stderr)
        return 3

    # Validate critical fields before emitting
    missing = [k for k in ("title",) if not metadata.get(k)]
    if missing:
        print(
            f"ERROR: metadata is missing required fields: {missing}. "
            "The upstream tool's output format may have changed.",
            file=sys.stderr,
        )
        return 3

    print(json.dumps(metadata, ensure_ascii=False, indent=2))
    return 0


def _resolve_ffmpeg_placeholder(args) -> str | None:
    """Resolve a path to use as BBDown's --ffmpeg-path.

    Search order (each must point to an existing file):
      1. Explicit --ffmpeg-path argument
      2. FFMPEG_PATH environment variable
      3. Real ffmpeg on PATH
    Does NOT silently borrow --ytdlp / YTDLP_PATH because that conflates two
    different tool roles. If the user wants to reuse yt-dlp.exe as a placeholder,
    they should pass it explicitly via --ffmpeg-path.
    """
    if args.ffmpeg_path and Path(args.ffmpeg_path).is_file():
        return args.ffmpeg_path
    env_val = os.environ.get("FFMPEG_PATH")
    if env_val and Path(env_val).is_file():
        return env_val
    real = shutil.which("ffmpeg")
    if real:
        return real
    return None


if __name__ == "__main__":
    sys.exit(main())
