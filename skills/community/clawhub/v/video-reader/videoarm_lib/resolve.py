"""Video resolution — transparently handle URLs and local paths.

resolve_video(source) → (local_path, meta_dict)

If source is a URL, downloads via yt-dlp (cached by URL hash).
If source is a local path, validates existence.
Always returns video metadata alongside the path.
"""

import hashlib
import subprocess
from pathlib import Path
from typing import Tuple

from videoarm_lib.config import VIDEO_DATABASE_FOLDER
from videoarm_lib.logger import ToolTracer, log_event
from videoarm_lib.video_meta import get_video_meta

_URL_PREFIXES = ("http://", "https://", "rtmp://", "rtsp://")
_DOWNLOAD_DIR = VIDEO_DATABASE_FOLDER / "temp" / "downloads"
_DOWNLOAD_TIMEOUT = 300  # seconds


def _is_url(source: str) -> bool:
    return any(source.startswith(p) for p in _URL_PREFIXES)


def _download(url: str, tracer=None) -> Path:
    """Download video via yt-dlp with caching."""
    _DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    url_hash = hashlib.md5(url.encode()).hexdigest()[:12]
    out = _DOWNLOAD_DIR / f"{url_hash}.mp4"

    if out.exists():
        if tracer:
            tracer.log("download_cached", path=str(out))
        return out

    if tracer:
        tracer.log("download_start", url=url)

    result = subprocess.run(
        [
            "yt-dlp",
            "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
            "--merge-output-format", "mp4",
            "-o", str(out),
            url,
        ],
        capture_output=True,
        text=True,
        timeout=_DOWNLOAD_TIMEOUT,
    )

    if result.returncode != 0:
        err = result.stderr[:500].strip()
        raise RuntimeError(f"yt-dlp failed: {err}")

    if not out.exists():
        raise RuntimeError(f"yt-dlp returned 0 but output not found: {out}")

    if tracer:
        size_mb = round(out.stat().st_size / 1024 / 1024, 1)
        tracer.log("download_done", path=str(out), size_mb=size_mb)

    return out


def resolve_video(source: str, tracer=None) -> Tuple[Path, dict]:
    """Resolve a video source (URL or path) to a local file + metadata.

    Args:
        source: URL or local file path.
        tracer: Optional ToolTracer for logging.

    Returns:
        (local_path, meta_dict) where meta_dict contains fps, total_frames, duration, has_audio.

    Raises:
        FileNotFoundError: If local path doesn't exist.
        RuntimeError: If download fails.
    """
    if _is_url(source):
        local_path = _download(source, tracer=tracer)
    else:
        local_path = Path(source)
        if not local_path.exists():
            raise FileNotFoundError(f"Video not found: {local_path}")

    meta = get_video_meta(str(local_path))

    if tracer:
        tracer.log("video_resolved", path=str(local_path), **meta)

    return local_path, meta
