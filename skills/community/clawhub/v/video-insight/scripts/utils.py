#!/usr/bin/env python3
"""video-insight utilities: platform detection, URL parsing, cache, temp cleanup, disk check, progress."""

import os
import re
import sys
import json
import atexit
import shutil
import signal
import hashlib
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Tuple
from urllib.parse import urlparse, parse_qs


# ──────────────────────────────────────────────
# Unified error/result structure
# ──────────────────────────────────────────────

def ok_result(data: dict) -> dict:
    """Wrap successful output."""
    return {"ok": True, "data": data, "error": None}


def err_result(error: str, code: str = "UNKNOWN") -> dict:
    """Wrap error output."""
    return {"ok": False, "data": None, "error": {"code": code, "message": error}}


# ──────────────────────────────────────────────
# Progress (stderr only)
# ──────────────────────────────────────────────

_quiet = False


def set_quiet(quiet: bool):
    global _quiet
    _quiet = quiet


def progress(msg: str):
    """Print progress to stderr (suppressed in --quiet mode)."""
    if not _quiet:
        print(msg, file=sys.stderr, flush=True)


# ──────────────────────────────────────────────
# Platform detection & URL parsing
# ──────────────────────────────────────────────

def detect_platform(url: str) -> str:
    """Detect video platform from URL."""
    if "bilibili.com" in url or "b23.tv" in url:
        return "bilibili"
    elif "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    return "unknown"


def extract_youtube_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats.
    Supports: watch, shorts, embed, youtu.be, live, v/ paths.
    """
    parsed = urlparse(url)

    # youtu.be/VIDEO_ID
    if parsed.hostname and "youtu.be" in parsed.hostname:
        vid = parsed.path.lstrip("/").split("/")[0].split("?")[0]
        return vid if vid else None

    # youtube.com/watch?v=VIDEO_ID
    if parsed.hostname and "youtube.com" in parsed.hostname:
        qs = parse_qs(parsed.query)
        if "v" in qs:
            return qs["v"][0]

        # /shorts/VIDEO_ID, /embed/VIDEO_ID, /live/VIDEO_ID, /v/VIDEO_ID
        path_parts = parsed.path.strip("/").split("/")
        if len(path_parts) >= 2 and path_parts[0] in ("shorts", "embed", "live", "v"):
            return path_parts[1]

    return None


def extract_bilibili_id(url: str) -> str:
    """Extract BV number from Bilibili URL (follows b23.tv short links).
    Uses urllib.parse for proper URL parsing.
    """
    if "b23.tv" in url:
        try:
            import requests
            r = requests.head(url, allow_redirects=True, timeout=10)
            url = r.url
        except Exception:
            pass

    parsed = urlparse(url)
    # Extract BV id from path segments, e.g. /video/BV1xx411c7mD or /video/BV1xx411c7mD/
    path_parts = [p for p in parsed.path.split("/") if p]
    for part in path_parts:
        if part.startswith("BV") and len(part) >= 10:
            return part
    return "unknown"


# ──────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────

def load_settings() -> dict:
    """Load settings from config/settings.json relative to skill root."""
    skill_root = Path(__file__).resolve().parent.parent
    config_path = skill_root / "config" / "settings.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def get_setting(key: str, default=None, env_key: str = None, settings: dict = None):
    """Get a setting with priority: env > settings.json > default."""
    if env_key:
        val = os.environ.get(env_key)
        if val is not None:
            return val
    if settings and key in settings:
        return settings[key]
    return default


# ──────────────────────────────────────────────
# Disk space check
# ──────────────────────────────────────────────

def check_disk_space(path: str = "/tmp", threshold_gb: float = 5.0) -> Tuple[bool, float]:
    """Check if disk has enough free space. Returns (ok, free_gb)."""
    try:
        usage = shutil.disk_usage(path)
        free_gb = usage.free / (1024 ** 3)
        return free_gb >= threshold_gb, free_gb
    except Exception:
        return True, -1  # Can't check, proceed anyway


# ──────────────────────────────────────────────
# Temporary file manager
# ──────────────────────────────────────────────

class TempManager:
    """Process-level temporary file management with auto-cleanup."""

    def __init__(self, base_dir: str = "/tmp", prefix: str = "vi-"):
        self.base_dir = base_dir
        self.work_dir = tempfile.mkdtemp(prefix=prefix, dir=base_dir)
        self._registered = []
        self._cleaned = False

        atexit.register(self.cleanup)
        # Handle SIGTERM gracefully
        try:
            signal.signal(signal.SIGTERM, self._handle_signal)
        except (OSError, ValueError):
            pass  # Can't set signal handler in some contexts

    def get_path(self, filename: str) -> str:
        """Get a path within the work directory."""
        return os.path.join(self.work_dir, filename)

    def register(self, path: str):
        """Register an external file for cleanup."""
        self._registered.append(path)

    def remove_early(self, path: str):
        """Remove a file immediately (e.g., video after audio extraction)."""
        try:
            if os.path.isfile(path):
                os.remove(path)
                progress(f"  🗑️  Cleaned: {os.path.basename(path)}")
        except OSError:
            pass

    def cleanup(self):
        """Clean up all temporary files."""
        if self._cleaned:
            return
        self._cleaned = True
        # Clean registered external files
        for path in self._registered:
            try:
                if os.path.isfile(path):
                    os.remove(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)
            except OSError:
                pass
        # Clean work directory
        try:
            shutil.rmtree(self.work_dir, ignore_errors=True)
        except OSError:
            pass

    def _handle_signal(self, sig, frame):
        self.cleanup()
        sys.exit(128 + sig)

    @staticmethod
    def cleanup_orphans(base_dir: str = "/tmp", prefix: str = "vi-", max_age_hours: int = 24):
        """Clean up orphaned temp directories from crashed runs."""
        import time
        now = time.time()
        cutoff = now - (max_age_hours * 3600)
        try:
            for entry in os.listdir(base_dir):
                if entry.startswith(prefix):
                    full = os.path.join(base_dir, entry)
                    if os.path.isdir(full):
                        try:
                            mtime = os.path.getmtime(full)
                            if mtime < cutoff:
                                shutil.rmtree(full, ignore_errors=True)
                        except OSError:
                            pass
        except OSError:
            pass


# ──────────────────────────────────────────────
# Cache
# ──────────────────────────────────────────────

class Cache:
    """File-based transcript cache at ~/.cache/video-insight/"""

    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/video-insight")
        self.cache_dir = cache_dir
        os.makedirs(self.cache_dir, exist_ok=True)

    def _key(self, platform: str, video_id: str) -> str:
        return f"{platform}_{video_id}"

    def _path(self, key: str) -> str:
        return os.path.join(self.cache_dir, f"{key}.json")

    def get(self, platform: str, video_id: str) -> Optional[dict]:
        """Get cached transcript data. Returns None if not cached."""
        path = self._path(self._key(platform, video_id))
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                data["cached"] = True
                return data
            except (json.JSONDecodeError, OSError):
                return None
        return None

    def put(self, platform: str, video_id: str, data: dict):
        """Cache transcript data (permanent)."""
        key = self._key(platform, video_id)
        path = self._path(key)
        cache_data = {
            "video_id": data.get("video_id", video_id),
            "platform": data.get("platform", platform),
            "title": data.get("title", ""),
            "channel": data.get("channel", ""),
            "duration_seconds": data.get("duration_seconds", 0),
            "transcript": data.get("transcript", ""),
            "transcript_with_timestamps": data.get("transcript_with_timestamps", ""),
            "cached_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            progress(f"  ⚠️  Cache write failed: {e}")

    def has(self, platform: str, video_id: str) -> bool:
        return os.path.exists(self._path(self._key(platform, video_id)))
