import argparse
import json
import os
import re
import sys
from urllib.parse import urlparse
from pathlib import Path
from typing import Any

import requests
from yt_dlp import YoutubeDL


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
COVERS_DIR = PROJECT_ROOT / "data" / "covers"
STATE_DIR = PROJECT_ROOT / "data" / "state"
ARCHIVE_PATH = STATE_DIR / "archive.txt"
CONFIG_PATH = PROJECT_ROOT / "data" / "channel_rules.json"
VIDEO_META_DIR = STATE_DIR / "video_meta"


def ensure_directories() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    COVERS_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    VIDEO_META_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_PATH.touch(exist_ok=True)


def sanitize_stem(file_path: Path) -> str:
    stem = re.sub(r"[^\w\- ]+", "", file_path.stem, flags=re.UNICODE)
    stem = stem.replace(".", "_")
    stem = re.sub(r"\s+", " ", stem).strip()
    return stem or "video"


def get_ydl_options() -> dict[str, Any]:
    output_template = str(RAW_DIR / "%(title)s.%(ext)s")
    cookies_file = os.getenv("YTDLP_COOKIES_FILE", "").strip()
    cookies_from_browser = os.getenv("YTDLP_COOKIES_FROM_BROWSER", "").strip()
    cookies_option: dict[str, Any] = {}
    if cookies_file:
        cookies_option["cookiefile"] = cookies_file
    elif cookies_from_browser:
        cookies_option["cookiesfrombrowser"] = (cookies_from_browser,)
    return {
        "format": "bestvideo*+bestaudio/best",
        "format_sort": [
            "hasvid",
            "res",
            "fps",
            "hdr:12",
            "vcodec:h264",
            "acodec:m4a",
            "ext:mp4:m4a",
        ],
        "outtmpl": output_template,
        "merge_output_format": "mp4",
        "postprocessors": [
            {
                "key": "FFmpegVideoRemuxer",
                "preferedformat": "mp4",
            }
        ],
        **cookies_option,
        "js_runtimes": {
            "node": {"path": "node"},
        },
        "download_archive": str(ARCHIVE_PATH),
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
    }


def get_info_ydl_options() -> dict[str, Any]:
    options = get_ydl_options().copy()
    options.pop("download_archive", None)
    options["skip_download"] = True
    return options


def build_expected_path(info: dict[str, Any]) -> Path:
    with YoutubeDL(get_info_ydl_options()) as ydl:
        candidate = Path(ydl.prepare_filename(info))

    if candidate.suffix.lower() != ".mp4":
        candidate = candidate.with_suffix(".mp4")

    return candidate.with_name(f"{sanitize_stem(candidate)}.mp4")


def read_archive_entries() -> set[str]:
    ensure_directories()
    return {
        line.strip()
        for line in ARCHIVE_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def load_channel_rules() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {
            "defaults": {
                "download_cover": False,
                "replace_intro_with_cover": False,
                "intro_seconds": 10,
                "voice_type": "zh_male_m191_uranus_bigtts",
                "use_intro_override": False,
            },
            "channels": [],
        }

    payload = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Invalid channel config: {CONFIG_PATH}")
    payload.setdefault("defaults", {})
    payload.setdefault("channels", [])
    return payload


def resolve_channel_settings(info: dict[str, Any]) -> dict[str, Any]:
    payload = load_channel_rules()
    defaults = payload.get("defaults", {})
    resolved = {
        "download_cover": bool(defaults.get("download_cover", False)),
        "replace_intro_with_cover": bool(defaults.get("replace_intro_with_cover", False)),
        "intro_seconds": int(defaults.get("intro_seconds", 10) or 10),
        "voice_type": str(defaults.get("voice_type", "zh_male_m191_uranus_bigtts")).strip()
        or "zh_male_m191_uranus_bigtts",
        "use_intro_override": bool(defaults.get("use_intro_override", False)),
    }

    channel_id = str(info.get("channel_id", "")).strip()
    uploader_id = str(info.get("uploader_id", "")).strip()
    channel_name = str(info.get("channel", "")).strip()
    uploader_name = str(info.get("uploader", "")).strip()

    for item in payload.get("channels", []):
        if not isinstance(item, dict):
            continue
        matched = False
        if item.get("channel_id") and str(item.get("channel_id")).strip() == channel_id:
            matched = True
        elif item.get("uploader_id") and str(item.get("uploader_id")).strip() == uploader_id:
            matched = True
        elif item.get("channel") and str(item.get("channel")).strip() == channel_name:
            matched = True
        elif item.get("uploader") and str(item.get("uploader")).strip() == uploader_name:
            matched = True

        if matched:
            if "download_cover" in item:
                resolved["download_cover"] = bool(item["download_cover"])
            if "replace_intro_with_cover" in item:
                resolved["replace_intro_with_cover"] = bool(item["replace_intro_with_cover"])
            if "intro_seconds" in item:
                resolved["intro_seconds"] = int(item["intro_seconds"] or resolved["intro_seconds"])
            if "voice_type" in item:
                resolved["voice_type"] = (
                    str(item["voice_type"]).strip() or resolved["voice_type"]
                )
            if "use_intro_override" in item:
                resolved["use_intro_override"] = bool(item["use_intro_override"])
            break

    return resolved


def save_video_metadata(info: dict[str, Any], video_path: Path) -> None:
    settings = resolve_channel_settings(info)
    payload = {
        "id": info.get("id", ""),
        "title": info.get("title", ""),
        "channel": info.get("channel", ""),
        "channel_id": info.get("channel_id", ""),
        "uploader": info.get("uploader", ""),
        "uploader_id": info.get("uploader_id", ""),
        "settings": settings,
    }
    meta_path = VIDEO_META_DIR / f"{video_path.stem}.json"
    meta_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_video_info(url: str) -> dict[str, Any]:
    with YoutubeDL(get_info_ydl_options()) as ydl:
        return ydl.extract_info(url, download=False)


def is_in_archive(info: dict[str, Any]) -> bool:
    extractor = info.get("extractor_key", "youtube")
    video_id = info.get("id")
    if not video_id:
        return False
    archive_key = f"{extractor.lower()} {video_id}"
    return archive_key in read_archive_entries()


def normalize_downloaded_path(file_path: Path) -> Path:
    if file_path.suffix.lower() != ".mp4":
        candidate = file_path.with_suffix(".mp4")
        if candidate.exists():
            file_path = candidate

    if not file_path.exists():
        raise FileNotFoundError(f"Downloaded file not found: {file_path}")

    normalized_path = file_path.with_name(f"{sanitize_stem(file_path)}.mp4")
    if file_path != normalized_path and not normalized_path.exists():
        file_path.rename(normalized_path)
        file_path = normalized_path

    return file_path


def find_newest_mp4(excluded_paths: set[Path]) -> Path | None:
    candidates = [path for path in RAW_DIR.glob("*.mp4") if path not in excluded_paths]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def find_matching_local_file(info: dict[str, Any]) -> Path | None:
    title = str(info.get("title", "")).strip()
    if not title:
        return None

    expected_stem = sanitize_stem(Path(f"{title}.mp4"))
    candidates = sorted(RAW_DIR.glob("*.mp4"), key=lambda path: path.stat().st_mtime, reverse=True)
    for candidate in candidates:
        candidate_stem = sanitize_stem(candidate)
        if candidate_stem == expected_stem:
            return candidate
    return None


def get_best_thumbnail(info: dict[str, Any]) -> dict[str, Any] | None:
    thumbnails = info.get("thumbnails") or []
    if not thumbnails:
        return None

    def score(item: dict[str, Any]) -> tuple[int, int, int]:
        url = str(item.get("url", ""))
        width = int(item.get("width") or 0)
        height = int(item.get("height") or 0)
        preference = int(item.get("preference") or 0)
        bonus = 1 if "maxres" in url else 0
        return (bonus, width * height, preference)

    return max(thumbnails, key=score)


def infer_cover_suffix(thumbnail_url: str, response: requests.Response) -> str:
    path = urlparse(thumbnail_url).path.lower()
    for suffix in [".jpg", ".jpeg", ".png", ".webp"]:
        if path.endswith(suffix):
            return ".jpg" if suffix == ".jpeg" else suffix

    content_type = response.headers.get("Content-Type", "").lower()
    if "png" in content_type:
        return ".png"
    if "webp" in content_type:
        return ".webp"
    return ".jpg"


def download_cover(info: dict[str, Any], video_path: Path) -> Path | None:
    ensure_directories()
    settings = resolve_channel_settings(info)
    if not settings.get("download_cover", True):
        print("[INFO] Skip cover download for this channel by config.")
        return None

    thumbnail = get_best_thumbnail(info)
    if thumbnail is None:
        print("[WARN] No thumbnail information found for this video.")
        return None

    thumbnail_url = str(thumbnail.get("url", "")).strip()
    if not thumbnail_url:
        print("[WARN] Thumbnail URL is empty.")
        return None

    print(f"[INFO] Downloading full-size cover: {thumbnail_url}")
    response = requests.get(thumbnail_url, timeout=120)
    response.raise_for_status()

    suffix = infer_cover_suffix(thumbnail_url, response)
    cover_path = COVERS_DIR / f"{video_path.stem}{suffix}"
    cover_path.write_bytes(response.content)
    print(f"[INFO] Cover saved to: {cover_path.relative_to(PROJECT_ROOT)}")
    return cover_path


def download_video(url: str) -> Path | None:
    ensure_directories()
    info = fetch_video_info(url)
    expected_path = build_expected_path(info)

    if is_in_archive(info):
        print(f"[INFO] Skip archived video: {url}")
        if expected_path.exists():
            save_video_metadata(info, expected_path)
            download_cover(info, expected_path)
            print(f"[INFO] Existing video found: {expected_path.relative_to(PROJECT_ROOT)}")
            return expected_path
        matching_path = find_matching_local_file(info)
        if matching_path is not None:
            matching_path = normalize_downloaded_path(matching_path)
            save_video_metadata(info, matching_path)
            download_cover(info, matching_path)
            print(f"[INFO] Recovered local video: {matching_path.relative_to(PROJECT_ROOT)}")
            return matching_path
        print("[WARN] URL is archived but local MP4 was not found. Skipping download.")
        return None

    print(f"[INFO] Start downloading video: {url}")
    existing_files = set(RAW_DIR.glob("*.mp4"))
    with YoutubeDL(get_ydl_options()) as ydl:
        ydl.extract_info(url, download=True)

    downloaded_path = expected_path if expected_path.exists() else find_newest_mp4(existing_files)
    if downloaded_path is None:
        downloaded_path = find_matching_local_file(info)
        if downloaded_path is None:
            raise FileNotFoundError("No downloaded MP4 file was found in data/raw after yt-dlp completed.")
        downloaded_path = normalize_downloaded_path(downloaded_path)

    downloaded_path = normalize_downloaded_path(downloaded_path)
    save_video_metadata(info, downloaded_path)
    download_cover(info, downloaded_path)
    print(f"[INFO] Video saved to: {downloaded_path.relative_to(PROJECT_ROOT)}")
    return downloaded_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a YouTube video into data/raw.")
    parser.add_argument("url", help="YouTube video URL")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        download_video(args.url)
    except Exception as exc:
        print(f"[ERROR] Failed to download video: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
