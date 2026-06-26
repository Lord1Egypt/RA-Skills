#!/usr/bin/env python3
"""
Seedance 2.0 Video Generator – Loova Seedance 2.0 script.
Loads LOOVA_API_KEY from environment or .env file.
Usage: python scripts/run_seedance.py --prompt "prompt" [--model ...] [--duration 5] [--ratio "16:9"] [--files "path1.jpg,path2.jpg"] [--image-urls "https://...,..."] [--video-urls "..."] [--audio-urls "..."]
Sends request as multipart/form-data when uploading files; otherwise sends application/json.
"""
import argparse
import json
import mimetypes
import os
import sys
import time
from typing import Any, List, Optional, Tuple

from dotenv import load_dotenv
import requests

# Load .env from current directory or project root
load_dotenv()

VID_URL = "https://api.loova.ai/api/v1/video/seedance-2"
VIDEO_ITEM_URL = "https://api.loova.ai/api/v1/tasks"
POLL_INTERVAL_SEC = 60  # Poll once per minute
MAX_POLL_COUNT = 180

# Limits per function mode (omni_reference)
OMNI_MAX_IMAGES = 9
OMNI_MAX_VIDEOS = 3
OMNI_MAX_AUDIO = 3
# first_last_frames: at least 1 image
FIRST_LAST_MIN_IMAGES = 1


def _media_type(path: str) -> str:
    """Return 'image', 'video', 'audio', or 'other' from file path (MIME)."""
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        return "other"
    if mime.startswith("image/"):
        return "image"
    if mime.startswith("video/"):
        return "video"
    if mime.startswith("audio/"):
        return "audio"
    return "other"


def _validate_media_counts_by_function_mode(
    *,
    image_count: int,
    video_count: int,
    audio_count: int,
    function_mode: Optional[str],
) -> None:
    """
    Validate media counts by function mode.
    - omni_reference: images <= 9, videos <= 3, audio <= 3.
    - first_last_frames: at least 1 image.
    """
    if function_mode == "first_last_frames":
        if image_count < FIRST_LAST_MIN_IMAGES:
            raise ValueError(
                f"function-mode first_last_frames requires at least {FIRST_LAST_MIN_IMAGES} image file(s), got {image_count}."
            )
        return

    if function_mode == "omni_reference":
        if image_count > OMNI_MAX_IMAGES:
            raise ValueError(
                f"function-mode omni_reference allows at most {OMNI_MAX_IMAGES} image(s), got {image_count}."
            )
        if video_count > OMNI_MAX_VIDEOS:
            raise ValueError(
                f"function-mode omni_reference allows at most {OMNI_MAX_VIDEOS} video(s), got {video_count}."
            )
        if audio_count > OMNI_MAX_AUDIO:
            raise ValueError(
                f"function-mode omni_reference allows at most {OMNI_MAX_AUDIO} audio file(s), got {audio_count}."
            )


def validate_files_by_function_mode(paths: List[str], function_mode: Optional[str]) -> None:
    """
    Validate file counts by function mode.
    - omni_reference: images <= 9, videos <= 3, audio <= 3.
    - first_last_frames: at least 1 image.
    """
    if not paths:
        return
    by_type: dict[str, List[str]] = {"image": [], "video": [], "audio": [], "other": []}
    for p in paths:
        p = p.strip()
        if not p:
            continue
        t = _media_type(p)
        by_type[t].append(p)
    images, videos, audios = by_type["image"], by_type["video"], by_type["audio"]
    _validate_media_counts_by_function_mode(
        image_count=len(images),
        video_count=len(videos),
        audio_count=len(audios),
        function_mode=function_mode,
    )


def validate_prompt_required(prompt: Optional[str]) -> None:
    if not prompt or not prompt.strip():
        raise ValueError("prompt is required (non-empty).")


def normalize_url_list(value: Any) -> Optional[List[str]]:
    """
    Normalize URL inputs to a list of strings.
    - None / "" -> None
    - "a,b" -> ["a", "b"]
    - ["a", "b"] / ("a", "b") -> ["a", "b"]
    """
    if value is None:
        return None
    if isinstance(value, str):
        items = [u.strip() for u in value.split(",") if u.strip()]
        return items or None
    if isinstance(value, (list, tuple)):
        items = [str(u).strip() for u in value if str(u).strip()]
        return items or None
    raise ValueError(f"Expected URL(s) as string or list, got {type(value).__name__}")


def validate_media_inputs_by_function_mode(
    *,
    file_paths: List[str],
    image_urls: List[str],
    video_urls: List[str],
    audio_urls: List[str],
    function_mode: Optional[str],
) -> None:
    """
    Validate media counts by function mode.
    If URLs are provided for a media type, they take precedence and the same-type local files are ignored.
    """
    file_images = 0
    file_videos = 0
    file_audios = 0
    for p in file_paths:
        t = _media_type(p)
        if t == "image":
            file_images += 1
        elif t == "video":
            file_videos += 1
        elif t == "audio":
            file_audios += 1

    effective_images = len(image_urls) if image_urls else file_images
    effective_videos = len(video_urls) if video_urls else file_videos
    effective_audios = len(audio_urls) if audio_urls else file_audios

    _validate_media_counts_by_function_mode(
        image_count=effective_images,
        video_count=effective_videos,
        audio_count=effective_audios,
        function_mode=function_mode,
    )


def filter_files_by_url_overrides(
    *,
    file_paths: List[str],
    image_urls: List[str],
    video_urls: List[str],
    audio_urls: List[str],
) -> List[str]:
    """
    If URLs are provided for a media type, drop same-type local files from upload.
    """
    if not file_paths:
        return []
    has_image_urls = bool(image_urls)
    has_video_urls = bool(video_urls)
    has_audio_urls = bool(audio_urls)
    if not (has_image_urls or has_video_urls or has_audio_urls):
        return file_paths

    filtered: List[str] = []
    for p in file_paths:
        t = _media_type(p)
        if t == "image" and has_image_urls:
            continue
        if t == "video" and has_video_urls:
            continue
        if t == "audio" and has_audio_urls:
            continue
        filtered.append(p)
    return filtered


def open_files_for_upload(paths: List[str]) -> List[Tuple[str, Tuple[str, Any, str]]]:
    """Open local files and return list of (form_key, (filename, fileobj, content_type)) for multipart upload."""
    result = []
    for path in paths:
        path = path.strip()
        if not path:
            continue
        if not os.path.isfile(path):
            raise FileNotFoundError(f"File not found: {path}")
        f = open(path, "rb")
        name = os.path.basename(path)
        mime, _ = mimetypes.guess_type(path)
        mime = mime or "application/octet-stream"
        result.append(("files", (name, f, mime)))
    return result


def get_api_key() -> str:
    key = os.environ.get("LOOVA_API_KEY", "").strip() or os.environ.get("LOOAI_API_KEY", "").strip()
    if not key:
        print(
            "Error: Set LOOVA_API_KEY in .env or environment (obtain it after logging in at https://loova.ai/)",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def submit_task(api_key: str, args: argparse.Namespace) -> str:
    image_urls = normalize_url_list(getattr(args, "image_urls", None))
    video_urls = normalize_url_list(getattr(args, "video_urls", None))
    audio_urls = normalize_url_list(getattr(args, "audio_urls", None))

    upload_paths = filter_files_by_url_overrides(
        file_paths=args.files or [],
        image_urls=image_urls or [],
        video_urls=video_urls or [],
        audio_urls=audio_urls or [],
    )
    file_tuples = open_files_for_upload(upload_paths) if upload_paths else []
    try:
        if file_tuples:
            # multipart/form-data (file upload)
            data: List[Tuple[str, str]] = [
                ("model", str(args.model)),
                ("prompt", str(args.prompt)),
                ("ratio", str(args.ratio)),
                ("duration", str(args.duration)),
            ]
            if args.function_mode:
                data.append(("functionMode", str(args.function_mode)))
            for u in image_urls or []:
                data.append(("image_urls", u))
            for u in video_urls or []:
                data.append(("video_urls", u))
            for u in audio_urls or []:
                data.append(("audio_urls", u))
            resp = requests.post(
                VID_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                },
                data=data,
                files=file_tuples,
                timeout=120,
            )
        else:
            # application/json (no file upload)
            payload: dict[str, Any] = {
                "model": args.model,
                "prompt": args.prompt,
                "ratio": args.ratio,
                "duration": args.duration,
            }
            if args.function_mode:
                payload["functionMode"] = args.function_mode
            if image_urls:
                payload["image_urls"] = image_urls
            if video_urls:
                payload["video_urls"] = video_urls
            if audio_urls:
                payload["audio_urls"] = audio_urls
            resp = requests.post(
                VID_URL,
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
                timeout=120,
            )
    finally:
        for _key, (_, f, _) in file_tuples:
            f.close()
    resp.raise_for_status()
    result_data = resp.json()
    task_id = result_data.get("task_id") or (result_data.get("data") or {}).get("task_id") or result_data.get("taskId")
    if not task_id:
        raise RuntimeError("No task_id in response: " + json.dumps(result_data))
    return task_id


def poll_result(api_key: str, task_id: str) -> dict:
    url = f"{VIDEO_ITEM_URL}?task_id={task_id}"
    for i in range(MAX_POLL_COUNT):
        resp = requests.get(
            url,
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status") or (data.get("data") or {}).get("status") or data.get("state")
        if status in ("succeeded", "success", "completed"):
            return data
        if status in ("failed", "error"):
            msg = data.get("message") or data.get("error") or json.dumps(data)
            raise RuntimeError("Task failed: " + str(msg))
        if i == 0:
            print(
                "Task submitted. Video generation may take up to 3 hours; polling until complete...",
                file=sys.stderr,
            )
        time.sleep(POLL_INTERVAL_SEC)
    raise RuntimeError("Polling timed out")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seedance 2.0 Video Generator")
    parser.add_argument("--prompt", required=True, help="Prompt text")
    parser.add_argument("--model", default="seedance_2_0", help="Model name")
    parser.add_argument("--duration", type=int, default=5, help="Duration in seconds (4-15)")
    parser.add_argument("--ratio", default="16:9", help="Aspect ratio")
    parser.add_argument("--function-mode", help="first_last_frames or omni_reference")
    parser.add_argument("--files", help="Comma-separated local file paths (sent as multipart File uploads: images/video/audio)")
    parser.add_argument("--image-urls", help="Comma-separated image URLs (no multipart upload)")
    parser.add_argument("--video-urls", help="Comma-separated video URLs (no multipart upload)")
    parser.add_argument("--audio-urls", help="Comma-separated audio URLs (no multipart upload)")
    args = parser.parse_args()
    args.files = [p.strip() for p in args.files.split(",") if p.strip()] if args.files else None
    args.image_urls = normalize_url_list(args.image_urls)
    args.video_urls = normalize_url_list(args.video_urls)
    args.audio_urls = normalize_url_list(args.audio_urls)

    validate_prompt_required(args.prompt)
    validate_media_inputs_by_function_mode(
        file_paths=args.files or [],
        image_urls=args.image_urls or [],
        video_urls=args.video_urls or [],
        audio_urls=args.audio_urls or [],
        function_mode=args.function_mode,
    )
    api_key = get_api_key()
    task_id = submit_task(api_key, args)
    print("task_id:", task_id, file=sys.stderr)
    result = poll_result(api_key, task_id)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except requests.RequestException as e:
        print("Request error:", e, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)
