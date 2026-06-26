from __future__ import annotations

import os
import shutil
import subprocess
import tarfile
from pathlib import Path
from typing import Iterable
from urllib.parse import urlparse

try:
    import imageio_ffmpeg
    import requests
except ImportError as exc:
    raise SystemExit(
        "Missing Python dependencies. Run `python scripts/bootstrap_env.py` first."
    ) from exc


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

AUDIO_SUFFIXES = {".mp3", ".m4a", ".wav", ".aac", ".flac", ".ogg"}
VIDEO_SUFFIXES = {".mp4", ".mkv", ".webm"}
STREAM_SUFFIXES = {".m3u8", ".mpd"}
MEDIA_SUFFIXES = AUDIO_SUFFIXES | VIDEO_SUFFIXES | STREAM_SUFFIXES
MEDIA_SUFFIX_ORDER = (
    ".mp3",
    ".m4a",
    ".wav",
    ".aac",
    ".flac",
    ".ogg",
    ".mp4",
    ".mkv",
    ".webm",
    ".m3u8",
    ".mpd",
)

M3U8_CONTENT_TYPES = {
    "application/vnd.apple.mpegurl",
    "application/x-mpegurl",
}

KEEP_CAPTURED_HEADERS = {
    "origin": "Origin",
    "referer": "Referer",
}

MODEL_ARCHIVE_NAME = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2"
MODEL_DIR_NAME = "sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17"
MODEL_URL = (
    "https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/"
    f"{MODEL_ARCHIVE_NAME}"
)


def cache_root() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    root = base / "web-video-transcribe-docx"
    root.mkdir(parents=True, exist_ok=True)
    return root


def format_seconds(seconds: float) -> str:
    rounded = max(0, int(round(seconds)))
    hours = rounded // 3600
    minutes = (rounded % 3600) // 60
    secs = rounded % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def ffmpeg_executable() -> str:
    return imageio_ffmpeg.get_ffmpeg_exe()


def run_ffmpeg(args: list[str]) -> None:
    cmd = [ffmpeg_executable(), "-nostdin", "-y", "-v", "error", *args]
    subprocess.run(cmd, check=True)


def guess_suffix_from_url(url: str) -> str:
    lowered_path = urlparse(url).path.lower()
    for suffix in MEDIA_SUFFIX_ORDER:
        if lowered_path.endswith(suffix):
            return suffix
    lowered = url.lower()
    for suffix in MEDIA_SUFFIX_ORDER:
        if suffix in lowered:
            return suffix
    return ".mp4"


def sanitize_captured_headers(headers: dict[str, str] | None) -> dict[str, str]:
    if not headers:
        return {}

    sanitized: dict[str, str] = {}
    for key, value in headers.items():
        if not value:
            continue
        normalized = key.strip().lower()
        target_key = KEEP_CAPTURED_HEADERS.get(normalized)
        if target_key:
            sanitized[target_key] = value.strip()
    return sanitized


def merge_headers(headers: dict[str, str] | None = None) -> dict[str, str]:
    merged = {"User-Agent": USER_AGENT}
    if headers:
        for key, value in headers.items():
            if key and value:
                merged[key] = value
    return merged


def looks_like_streaming_manifest(url: str, content_type: str = "") -> bool:
    lowered = url.lower()
    ctype = content_type.lower()
    return any(suffix in lowered for suffix in STREAM_SUFFIXES) or any(
        token in ctype for token in M3U8_CONTENT_TYPES
    )


def classify_media_url(url: str, content_type: str = "") -> str | None:
    lowered = url.lower()
    ctype = content_type.lower()
    suffix = Path(urlparse(url).path).suffix.lower()

    if (
        suffix in AUDIO_SUFFIXES
        or "media-audio" in lowered
        or "/audio" in lowered
        or "audio/" in ctype
        or "mime_type=audio" in lowered
    ):
        return "audio"

    if (
        suffix in VIDEO_SUFFIXES
        or suffix in STREAM_SUFFIXES
        or "media-video" in lowered
        or ".mp4" in lowered
        or ".m3u8" in lowered
        or ".mpd" in lowered
        or "video/" in ctype
        or "mime_type=video" in lowered
        or any(token in ctype for token in M3U8_CONTENT_TYPES)
    ):
        return "video"

    return None


def is_probable_media_url(url: str, content_type: str = "") -> bool:
    if classify_media_url(url, content_type):
        return True

    lowered = url.lower()
    return any(
        token in lowered
        for token in ("playurl", "playlist", "stream", "manifest", "media", "audio", "video")
    )


def download_file(url: str, destination: Path, headers: dict[str, str] | None = None) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    merged_headers = merge_headers(headers)

    with requests.get(url, headers=merged_headers, stream=True, timeout=60) as response:
        response.raise_for_status()
        with destination.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
    return destination


def _safe_extract_tar(archive: Path, destination: Path) -> None:
    destination = destination.resolve()
    with tarfile.open(archive, "r:*") as tar:
        members = tar.getmembers()
        for member in members:
            target = (destination / member.name).resolve()
            if not str(target).startswith(str(destination)):
                raise RuntimeError(f"Unsafe tar member path: {member.name}")
        tar.extractall(destination)


def ensure_sensevoice_model(target_root: Path | None = None) -> Path:
    root = target_root or cache_root()
    root.mkdir(parents=True, exist_ok=True)
    model_dir = root / MODEL_DIR_NAME
    model_file = model_dir / "model.int8.onnx"
    tokens_file = model_dir / "tokens.txt"
    if model_file.is_file() and tokens_file.is_file():
        return model_dir

    archive_path = root / MODEL_ARCHIVE_NAME
    if not archive_path.is_file():
        download_file(MODEL_URL, archive_path)
    _safe_extract_tar(archive_path, root)
    if not model_file.is_file() or not tokens_file.is_file():
        raise RuntimeError("SenseVoice model download completed, but required files are missing.")
    return model_dir


def download_media_url(
    url: str,
    destination: Path,
    *,
    headers: dict[str, str] | None = None,
    content_type: str = "",
) -> Path:
    if not looks_like_streaming_manifest(url, content_type=content_type):
        return download_file(url, destination, headers=headers)

    destination.parent.mkdir(parents=True, exist_ok=True)
    merged_headers = merge_headers(headers)
    ffmpeg_args = ["-user_agent", merged_headers["User-Agent"]]

    referer = merged_headers.get("Referer")
    if referer:
        ffmpeg_args.extend(["-referer", referer])

    extra_headers = {
        key: value
        for key, value in merged_headers.items()
        if key not in {"User-Agent", "Referer"}
    }
    if extra_headers:
        header_blob = "".join(f"{key}: {value}\r\n" for key, value in extra_headers.items())
        ffmpeg_args.extend(["-headers", header_blob])

    ffmpeg_args.extend(["-i", url, "-map", "0", "-c", "copy", str(destination)])
    run_ffmpeg(ffmpeg_args)
    return destination


def segment_media(input_path: Path, output_dir: Path, segment_seconds: int = 600) -> list[Path]:
    if output_dir.exists():
        for old in output_dir.glob("part_*.wav"):
            old.unlink()
    output_dir.mkdir(parents=True, exist_ok=True)
    pattern = output_dir / "part_%03d.wav"
    run_ffmpeg(
        [
            "-i",
            str(input_path),
            "-ar",
            "16000",
            "-ac",
            "1",
            "-f",
            "segment",
            "-segment_time",
            str(segment_seconds),
            "-reset_timestamps",
            "1",
            str(pattern),
        ]
    )
    return sorted(output_dir.glob("part_*.wav"))


def find_browser_executable() -> str:
    candidates: Iterable[str | None] = (
        shutil.which("chrome"),
        shutil.which("msedge"),
        shutil.which("chromium"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/usr/bin/google-chrome",
        "/usr/bin/microsoft-edge",
        "/usr/bin/chromium",
        "/snap/bin/chromium",
    )
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise RuntimeError(
        "No supported Chrome/Edge browser executable was found. "
        "Install Chrome or Edge, or extend `find_browser_executable()`."
    )
