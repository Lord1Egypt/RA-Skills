"""Quota bookkeeping for reel.py: a trimmed copy of Reel Agent's common.py with only the Gemini usage helpers.
reel.py points GEMINI_USAGE at <folder>/reels/.gemini_usage.json."""
import json
import os
import time
import uuid
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path

GEMINI_USAGE = Path("reels") / ".gemini_usage.json"


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(f"{path.name}.{uuid.uuid4().hex[:6]}.tmp")
    tmp.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    for _ in range(20):
        try:
            tmp.replace(path)
            return
        except PermissionError:  # Windows: reader has it open for a moment
            time.sleep(0.05)
    tmp.unlink(missing_ok=True)


@contextmanager
def file_lock(path, stale_sec=30):
    lock = Path(str(path) + ".lock")
    lock.parent.mkdir(parents=True, exist_ok=True)
    fd = None
    for _ in range(400):
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - lock.stat().st_mtime > stale_sec:
                    lock.unlink(missing_ok=True)
            except FileNotFoundError:
                pass
            time.sleep(0.05)
    try:
        yield
    finally:
        if fd is not None:
            os.close(fd)
            lock.unlink(missing_ok=True)


def quota_day():
    """Gemini free-tier quotas reset at midnight Pacific time."""
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d")
    except Exception:
        from datetime import timedelta, timezone
        return (datetime.now(timezone.utc) - timedelta(hours=8)).strftime("%Y-%m-%d")


def gemini_usage_update(fn):
    """fn(day_record) mutates today's record: {"models": {m: {...}}, "exhausted": [...], "limits": {...}}."""
    with file_lock(GEMINI_USAGE):
        data = read_json(GEMINI_USAGE, {}) or {}
        if data.get("day") != quota_day():
            data = {"day": quota_day(), "models": {}, "exhausted": [], "limits": data.get("limits", {})}
        fn(data)
        write_json(GEMINI_USAGE, data)


def gemini_usage():
    data = read_json(GEMINI_USAGE, {}) or {}
    if data.get("day") != quota_day():
        return {"day": quota_day(), "models": {}, "exhausted": [], "limits": data.get("limits", {})}
    return data
