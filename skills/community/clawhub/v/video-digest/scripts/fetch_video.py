#!/usr/bin/env python3
"""Fetch YouTube subtitles with the pinned yt-dlp Python API."""

import argparse
import json
import os
import re
import stat
import sys
import tempfile
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

PINNED_VERSION = "2026.8.19"
CACHE_ROOT = Path(tempfile.gettempdir()) / f"video-deep-reader-{os.geteuid()}"
VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{6,40}$")
YOUTUBE_HOSTS = ("youtube.com", "youtu.be", "youtube-nocookie.com")
TRANSCRIPT_LINE = re.compile(r"^\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*(.+)$")


class QuietLogger:
    """Suppress upstream CLI guidance; callers receive bounded errors instead."""

    def debug(self, message):
        pass

    def info(self, message):
        pass

    def warning(self, message):
        pass

    def error(self, message):
        pass


def is_youtube_ref(value):
    value = (value or "").strip()
    if not value:
        return False
    if value.lower().startswith(("http://", "https://")):
        host = (urlsplit(value).hostname or "").lower()
        return any(host == item or host.endswith("." + item) for item in YOUTUBE_HOSTS)
    return bool(VIDEO_ID.fullmatch(value))


def load_yt_dlp():
    try:
        import yt_dlp
    except ImportError as exc:
        raise RuntimeError("yt-dlp is missing; run fetch_video.py --doctor") from exc
    actual = yt_dlp.version.__version__
    normalize = lambda value: tuple(int(part) for part in value.split("."))
    if normalize(actual) != normalize(PINNED_VERSION):
        raise RuntimeError(
            f"yt-dlp {PINNED_VERSION} is required; found {actual}. "
            "Run fetch_video.py --doctor"
        )
    return yt_dlp


def dependency_status():
    try:
        import yt_dlp
    except ImportError:
        return {"ok": False, "installed": None, "required": PINNED_VERSION}
    installed = yt_dlp.version.__version__
    normalize = lambda value: tuple(int(part) for part in value.split("."))
    return {
        "ok": normalize(installed) == normalize(PINNED_VERSION),
        "installed": installed,
        "required": PINNED_VERSION,
    }


def network_status(proxy_port=None):
    handlers = []
    if proxy_port:
        proxy = f"http://127.0.0.1:{proxy_port}"
        handlers.append(urllib.request.ProxyHandler({"http": proxy, "https": proxy}))
    opener = urllib.request.build_opener(*handlers)
    try:
        request = urllib.request.Request("https://www.youtube.com", method="HEAD")
        status = opener.open(request, timeout=6).status
        return {"checked": True, "ok": status < 400, "status": status}
    except Exception as exc:
        return {"checked": True, "ok": False, "error": type(exc).__name__}


def format_ts(seconds):
    seconds = max(0, int(seconds or 0))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours else f"{minutes:02d}:{secs:02d}"


def ts_to_seconds(value):
    try:
        parts = [int(item) for item in value.split(":")]
    except ValueError:
        return None
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    return None


def safe_name(value):
    value = re.sub(r"\s+", "_", (value or "channel").strip())
    value = re.sub(r"[^\w\u4e00-\u9fff-]", "_", value).strip("_")
    return value[:60] or "channel"


def clean_caption(value):
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\[[^\]]*\]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def parse_vtt(text):
    """Return timestamped, overlap-reduced transcript blocks."""
    stamp = re.compile(
        r"(\d{1,2}):(\d{2}):(\d{2})\.(\d{3})\s+-->\s*"
        r"(\d{1,2}):(\d{2}):(\d{2})\.(\d{3})"
    )
    lines = text.splitlines()
    raw = []
    index = 0
    while index < len(lines):
        match = stamp.search(lines[index])
        if not match:
            index += 1
            continue
        start = int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3))
        parts = []
        cursor = index + 1
        while cursor < len(lines) and not stamp.search(lines[cursor]):
            item = clean_caption(lines[cursor])
            if item and not item.startswith(("WEBVTT", "Kind:", "Language:")):
                parts.append(item)
            cursor += 1
        if parts:
            raw.append([start, " ".join(parts)])
        index = cursor

    def overlap(left, right):
        for size in range(min(len(left), len(right), 200), 3, -1):
            if left[-size:] == right[:size]:
                return size
        return 0

    merged = []
    for start, value in raw:
        if not merged:
            merged.append([start, value])
            continue
        previous = merged[-1][1]
        if value in previous:
            continue
        size = overlap(previous, value)
        tail = value[size:]
        if size >= 4 and tail and len(previous) + len(tail) <= 320:
            merged[-1][1] = f"{previous} {tail.lstrip()}"
        elif size < 4:
            merged.append([start, value])
        elif tail:
            merged.append([start, tail.lstrip()])
    return merged


def pick_subtitle(info, preferences):
    def score(code):
        base = code.split("-")[0].lower()
        for index, preference in enumerate(preferences):
            if base == preference or base.startswith(preference):
                return index
        return len(preferences)

    choices = []
    for key, automatic in (("subtitles", False), ("automatic_captions", True)):
        for code, formats in (info.get(key) or {}).items():
            track = next((item for item in formats if item.get("ext") == "vtt"), None)
            if track and track.get("url"):
                choices.append((score(code), automatic, code, track["url"]))
    if not choices:
        return None
    _, automatic, code, url = min(choices, key=lambda item: item[:2])
    return code, automatic, url


def secure_directory(path):
    """Create or validate one user-owned, non-symlink 0700 directory."""
    try:
        path.mkdir(mode=0o700)
    except FileExistsError:
        pass
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
        raise RuntimeError("managed cache path is not a real directory")
    if info.st_uid != os.geteuid():
        raise RuntimeError("managed cache path has an unexpected owner")
    if stat.S_IMODE(info.st_mode) != 0o700:
        raise RuntimeError("managed cache directory permissions must be 0700")


def managed_dir(channel, video_id, root=CACHE_ROOT):
    root_parent = root.parent.resolve()
    if root.resolve(strict=False).parent != root_parent:
        raise RuntimeError("managed cache root is invalid")
    secure_directory(root)
    channel_dir = root / safe_name(channel)
    secure_directory(channel_dir)
    target = channel_dir / video_id
    secure_directory(target)
    if root.resolve() not in target.resolve().parents:
        raise RuntimeError("managed cache boundary violation")
    return target


def write_private(path, content):
    """Atomically replace one regular user-owned cache file without following links."""
    parent = path.parent
    secure_directory(parent)
    if path.exists() or path.is_symlink():
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise RuntimeError("cache output path is not a regular file")
        if info.st_uid != os.geteuid():
            raise RuntimeError("cache output file has an unexpected owner")

    descriptor, temporary = tempfile.mkstemp(prefix=".write-", dir=parent)
    temporary_path = Path(temporary)
    try:
        os.fchmod(descriptor, 0o600)
        info = os.fstat(descriptor)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != os.geteuid():
            raise RuntimeError("secure cache file validation failed")
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            descriptor = -1
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary_path.exists():
            temporary_path.unlink()


def find_transcript(video_id, root=CACHE_ROOT):
    """Find exactly one validated transcript for a video ID."""
    if not VIDEO_ID.fullmatch(video_id):
        raise ValueError("invalid video ID")
    secure_directory(root)
    safe = []
    for channel in root.iterdir():
        if channel.is_symlink():
            continue
        try:
            secure_directory(channel)
        except RuntimeError:
            continue
        video_dir = channel / video_id
        if not video_dir.exists() or video_dir.is_symlink():
            continue
        try:
            secure_directory(video_dir)
        except RuntimeError:
            continue
        transcript = video_dir / "transcript.txt"
        if not transcript.exists() or transcript.is_symlink():
            continue
        info = transcript.lstat()
        if stat.S_ISREG(info.st_mode) and info.st_uid == os.geteuid():
            safe.append(transcript)
    if len(safe) != 1:
        raise FileNotFoundError(f"expected one managed transcript, found {len(safe)}")
    return safe[0]


def parse_transcript(path):
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = TRANSCRIPT_LINE.match(line)
        if not match:
            continue
        seconds = ts_to_seconds(match.group(1))
        if seconds is not None:
            entries.append((seconds, match.group(1), match.group(2)))
    return entries


def retrieve(
    video_id,
    keyword=None,
    at=None,
    window=30,
    list_mode=False,
    root=CACHE_ROOT,
):
    entries = parse_transcript(find_transcript(video_id, root))
    if not entries:
        return {"status": "empty", "results": []}
    if list_mode:
        step = max(1, len(entries) // 40)
        selected = entries[::step]
    elif at:
        center = ts_to_seconds(at)
        if center is None:
            raise ValueError("invalid timestamp")
        selected = [
            item for item in entries
            if center - window <= item[0] <= center + window
        ]
    else:
        lowered = (keyword or "").lower()
        selected = [item for item in entries if lowered in item[2].lower()]
    return {
        "status": "ok" if selected else "no_match",
        "results": [
            {"seconds": seconds, "timestamp": stamp, "text": text}
            for seconds, stamp, text in selected
        ],
    }


def safe_error(error):
    """Return a bounded error without credential or bypass instructions."""
    value = str(error).lower()
    if "sign in" in value or "not a bot" in value or "cookies" in value:
        return (
            "YouTube requested sign-in or bot verification. Browser cookies are "
            "intentionally unsupported; paste or upload a transcript, or try later."
        )
    if "age" in value or "restricted" in value or "private video" in value:
        return (
            "The video is access-restricted. This skill does not bypass access controls; "
            "provide an authorized transcript instead."
        )
    if "unavailable" in value or "not available" in value:
        return "The video is unavailable. Check the link or provide a transcript."
    return "YouTube metadata or subtitle retrieval failed. Try later or provide a transcript."


def fetch_one(reference, languages, proxy_port, yt_dlp, root=CACHE_ROOT):
    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "noplaylist": True,
        "logger": QuietLogger(),
    }
    if proxy_port:
        options["proxy"] = f"http://127.0.0.1:{proxy_port}"

    with yt_dlp.YoutubeDL(options) as downloader:
        info = downloader.extract_info(reference, download=False)
        video_id = info.get("id") or ""
        if not VIDEO_ID.fullmatch(video_id):
            raise RuntimeError("provider returned an invalid video ID")
        directory = managed_dir(
            info.get("channel") or info.get("uploader"), video_id, root
        )
        selected = pick_subtitle(info, languages)
        metadata = {
            "id": video_id,
            "title": info.get("title") or "Untitled",
            "channel": info.get("channel") or info.get("uploader") or "Unknown",
            "duration": info.get("duration") or 0,
            "duration_str": format_ts(info.get("duration") or 0),
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "chapters": [
                {
                    "start": format_ts(item.get("start_time") or 0),
                    "end": format_ts(item.get("end_time") or 0),
                    "title": (item.get("title") or "").strip(),
                }
                for item in (info.get("chapters") or [])
                if (item.get("title") or "").strip()
            ],
            "cache": "temporary",
        }
        if not selected:
            metadata["has_subtitle"] = False
            write_private(
                directory / "meta.json",
                json.dumps(metadata, ensure_ascii=False, indent=2),
            )
            return {"status": "no_subtitle", "dir": str(directory), **metadata}

        language, automatic, subtitle_url = selected
        with downloader.urlopen(subtitle_url) as response:
            blocks = parse_vtt(response.read().decode("utf-8", errors="replace"))
        if not blocks:
            metadata["has_subtitle"] = False
            write_private(
                directory / "meta.json",
                json.dumps(metadata, ensure_ascii=False, indent=2),
            )
            return {"status": "no_subtitle", "dir": str(directory), **metadata}

        transcript = "".join(
            f"[{format_ts(start)}] {value}\n" for start, value in blocks
        )
        metadata.update(
            {
                "has_subtitle": True,
                "subtitle_lang": language,
                "subtitle_manual": not automatic,
                "blocks": len(blocks),
            }
        )
        write_private(
            directory / "meta.json",
            json.dumps(metadata, ensure_ascii=False, indent=2),
        )
        write_private(directory / "transcript.txt", transcript)
        return {"status": "ok", "dir": str(directory), **metadata}


def main():
    parser = argparse.ArgumentParser(
        description="Check readiness or fetch YouTube subtitles to a private cache."
    )
    parser.add_argument("references", nargs="*", help="YouTube URLs or video IDs")
    parser.add_argument("--langs", default="en,zh", help="Subtitle preference, e.g. en,zh")
    parser.add_argument("--proxy-port", type=int, choices=range(1, 65536))
    parser.add_argument("--doctor", action="store_true", help="Run a read-only dependency check")
    parser.add_argument("--network", action="store_true", help="With --doctor, test YouTube access")
    parser.add_argument("--retrieve-video", help="Retrieve one managed transcript by video ID")
    parser.add_argument("--keyword")
    parser.add_argument("--at")
    parser.add_argument("--window", type=int, default=30)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.retrieve_video:
        if args.references or args.doctor or args.network:
            parser.error("retrieval cannot be combined with fetch or doctor mode")
        if sum((bool(args.keyword), bool(args.at), bool(args.list))) != 1:
            parser.error("choose exactly one of --keyword, --at, or --list")
        try:
            result = retrieve(
                args.retrieve_video,
                keyword=args.keyword,
                at=args.at,
                window=args.window,
                list_mode=args.list,
            )
        except (ValueError, FileNotFoundError) as exc:
            print(json.dumps({"status": "error", "error": str(exc)}))
            return 2
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "ok" else 1

    if args.doctor:
        if args.references:
            parser.error("--doctor does not accept video references")
        result = {
            "python": {
                "ok": sys.version_info >= (3, 9),
                "version": ".".join(map(str, sys.version_info[:3])),
                "required": ">=3.9",
            },
            "yt_dlp": dependency_status(),
            "network": {"checked": False},
        }
        if args.network:
            result["network"] = network_status(args.proxy_port)
            result["network"]["disclosure"] = (
                "One bounded request was sent to YouTube."
            )
        result["ready"] = (
            result["python"]["ok"]
            and result["yt_dlp"]["ok"]
            and (not args.network or result["network"]["ok"])
        )
        if not result["yt_dlp"]["ok"]:
            result["repair"] = (
                "python3 -m venv .venv && "
                ".venv/bin/python -m pip install --require-hashes -r requirements.lock"
            )
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["ready"] else 2

    if not args.references:
        parser.error("provide at least one YouTube reference or use --doctor")
    if args.network:
        parser.error("--network is only valid with --doctor")
    if not all(is_youtube_ref(item) for item in args.references):
        print(json.dumps({"error": "invalid_youtube_reference"}), file=sys.stderr)
        return 2
    try:
        yt_dlp = load_yt_dlp()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    languages = [item.strip().lower() for item in args.langs.split(",") if item.strip()]
    results = []
    for reference in args.references:
        try:
            results.append(fetch_one(reference, languages, args.proxy_port, yt_dlp))
        except Exception as exc:
            results.append(
                {"status": "error", "reference": reference, "error": safe_error(exc)}
            )
    print(json.dumps({
        "network_disclosure": (
            "Supplied video references were sent to YouTube to retrieve public "
            "metadata and captions."
        ),
        "results": results,
    }, ensure_ascii=False, indent=2))
    if any(item["status"] == "error" for item in results):
        return 3
    if any(item["status"] == "no_subtitle" for item in results):
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
