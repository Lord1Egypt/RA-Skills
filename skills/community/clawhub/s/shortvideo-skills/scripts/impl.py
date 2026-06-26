#!/usr/bin/env python3
"""
ShortVideo API Client - General Utilities

Upload files and create video generation tasks via ShortVideo API.

For specific task types, use dedicated scripts:
- image-to-ad-video.py: Create image-to-ad-video tasks
- poll-videos.py: Poll for video results
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


# Task type constants
TASK_TYPES = {
    "product-to-video": "sora2/product-to-video",
    "image-to-ad-video-v2": "vidu/image-to-ad-video-v2",
    "replicate-video": "vidu/replicate-video",
}

# Required fields for each task type
REQUIRED_FIELDS = {
    "sora2/product-to-video": ["product_name", "image", "aspect_ratio", "duration"],
    "vidu/image-to-ad-video-v2": ["images", "aspect_ratio", "duration", "language"],
    "vidu/replicate-video": ["video", "aspect_ratio", "resolution"],
}

# File type mappings
FILE_TYPE_MAPPING = {
    ".jpg": "image", ".jpeg": "image", ".png": "image", ".gif": "image", ".webp": "image", ".bmp": "image",
    ".mp4": "video", ".mov": "video", ".avi": "video", ".mkv": "video", ".webm": "video",
    ".mp3": "video", ".wav": "video", ".aac": "video", ".m4a": "video", ".ogg": "video",
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


def get_config() -> tuple[str, str]:
    """Get base_url and api_key from environment variables."""
    base_url = os.environ.get("SHORTVIDEO_BASE_URL", "")
    api_key = os.environ.get("SHORTVIDEO_API_KEY", "")

    if not base_url:
        print("Error: SHORTVIDEO_BASE_URL environment variable not set")
        print("Set it with: export SHORTVIDEO_BASE_URL='https://api.shortvideo.ai'")
        sys.exit(1)

    if not api_key:
        print("Error: SHORTVIDEO_API_KEY environment variable not set")
        print("Please visit https://shortvideo.ai to get your API key")
        print("Set it with: export SHORTVIDEO_API_KEY='your-api-key'")
        sys.exit(1)

    return base_url.rstrip("/"), api_key


def get_file_type(filepath: str) -> str:
    """Determine upload type based on file extension."""
    ext = Path(filepath).suffix.lower()
    return FILE_TYPE_MAPPING.get(ext, "video")


def is_local_file(path: str) -> bool:
    """Check if path is a local file."""
    if not path:
        return False
    if path.startswith(("http://", "https://", "oss://")):
        return False
    return os.path.isfile(path)


def upload_file(filepath: str, upload_type: str = None) -> dict[str, Any]:
    """Upload a local file to OSS."""
    base_url, api_key = get_config()

    if not os.path.isfile(filepath):
        return {"status": "error", "error": f"File not found: {filepath}"}

    file_size = os.path.getsize(filepath)
    if file_size > MAX_FILE_SIZE:
        return {"status": "error", "error": f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE})"}

    if not upload_type:
        upload_type = get_file_type(filepath)

    url = f"{base_url}/api/oss/upload"
    headers = {"Authorization": f"Bearer {api_key}"}
    filename = os.path.basename(filepath)

    try:
        with open(filepath, "rb") as f:
            files = {"file": (filename, f)}
            data = {"type": upload_type}
            response = requests.post(url, files=files, data=data, headers=headers, timeout=60)
            response.raise_for_status()
            result = response.json()

            code = result.get("code", -1)
            if code != 0:
                error_msg = result.get("message", result.get("info", f"Upload failed with code {code}"))
                return {"status": "error", "error": error_msg, "code": code}

            data = result.get("data", {})
            return {
                "status": "success",
                "path": data.get("path", ""),
                "domain": data.get("domain", ""),
                "url": f"{data.get('domain', '')}{data.get('path', '')}",
                "filename": filename,
                "size": file_size
            }
    except requests.exceptions.Timeout:
        return {"status": "error", "error": "Upload request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error": f"HTTP error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": f"Upload failed: {e}"}
    except json.JSONDecodeError:
        return {"status": "error", "error": "Invalid JSON response"}


def upload_multiple_files(filepaths: list[str], upload_type: str = None) -> dict[str, Any]:
    """Upload multiple files to OSS."""
    paths, urls, errors = [], [], []

    for filepath in filepaths:
        result = upload_file(filepath, upload_type)
        if result.get("status") == "success":
            paths.append(result["path"])
            urls.append(result["url"])
        else:
            errors.append(f"{filepath}: {result.get('error', 'Unknown error')}")

    if errors:
        return {"status": "error", "error": f"Some files failed: {'; '.join(errors)}", "uploaded": paths}

    return {"status": "success", "paths": paths, "urls": urls}


def process_args_for_upload(args: dict[str, Any]) -> tuple[dict[str, Any], list]:
    """Process task arguments, uploading any local file paths."""
    processed_args = args.copy()
    upload_results = []

    single_file_fields = ["image", "video"]
    array_file_fields = ["images", "product_images", "model_images"]

    for field in single_file_fields:
        if field in processed_args and is_local_file(processed_args[field]):
            print(f"Uploading {field}: {processed_args[field]}")
            result = upload_file(processed_args[field])
            if result.get("status") == "success":
                processed_args[field] = result["path"]
                upload_results.append({"field": field, **result})
            else:
                print(f"Warning: Failed to upload {field}: {result.get('error')}")

    for field in array_file_fields:
        if field in processed_args and isinstance(processed_args[field], list):
            new_paths = []
            for i, path in enumerate(processed_args[field]):
                if is_local_file(path):
                    print(f"Uploading {field}[{i}]: {path}")
                    result = upload_file(path)
                    if result.get("status") == "success":
                        new_paths.append(result["path"])
                        upload_results.append({"field": f"{field}[{i}]", **result})
                    else:
                        print(f"Warning: Failed to upload {field}[{i}]: {result.get('error')}")
                else:
                    new_paths.append(path)
            processed_args[field] = new_paths

    return processed_args, upload_results


def validate_args(task_type: str, args: dict[str, Any]) -> list[str]:
    """Validate required fields for task type."""
    required = REQUIRED_FIELDS.get(task_type, [])
    missing = []

    for field in required:
        if field not in args or args[field] is None or args[field] == "":
            missing.append(field)
        elif isinstance(args[field], list) and len(args[field]) == 0:
            missing.append(field)

    return missing


def create_task(task_type: str, args: dict[str, Any], user_id: str = "", auto_upload: bool = True) -> dict[str, Any]:
    """Create a ShortVideo task."""
    base_url, api_key = get_config()

    upload_results = []
    if auto_upload:
        args, upload_results = process_args_for_upload(args)

    missing = validate_args(task_type, args)
    if missing:
        return {"status": "error", "error": f"Missing required fields: {', '.join(missing)}"}

    url = f"{base_url}/api/task/create"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    payload = {"user_id": user_id, "type": task_type, "args": args}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        code = result.get("code", -1)
        if code != 0:
            error_msg = result.get("message", result.get("info", f"Task creation failed with code {code}"))
            return {"status": "error", "error": error_msg, "code": code}

        data = result.get("data", result)
        response_data = {
            "status": "success",
            "task_id": data.get("task_id", ""),
            "video_ids": data.get("video_ids", []),
            "asset_ids": data.get("asset_ids", []),
            "consumed_credit": data.get("consumed_credit", 0),
            "credit": data.get("credit", 0),
            "sub_credit": data.get("sub_credit", 0)
        }

        if upload_results:
            response_data["uploads"] = upload_results

        return response_data
    except requests.exceptions.Timeout:
        return {"status": "error", "error": "Request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error": f"HTTP error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": f"Request failed: {e}"}
    except json.JSONDecodeError:
        return {"status": "error", "error": "Invalid JSON response"}


def fetch_videos(video_ids: list[str]) -> dict[str, Any]:
    """Fetch video information by video IDs."""
    base_url, api_key = get_config()

    url = f"{base_url}/api/video/fetch?ids={','.join(video_ids)}"
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        code = result.get("code", -1)
        if code != 0:
            error_msg = result.get("message", result.get("info", f"Fetch failed with code {code}"))
            return {"status": "error", "error": error_msg, "code": code}

        data = result.get("data", result)
        return {"status": "success", "videos": data.get("videos", []), "domain": data.get("domain", "")}
    except requests.exceptions.Timeout:
        return {"status": "error", "error": "Request timed out"}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error": f"HTTP error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": f"Request failed: {e}"}
    except json.JSONDecodeError:
        return {"status": "error", "error": "Invalid JSON response"}


def main():
    parser = argparse.ArgumentParser(
        description="ShortVideo API Client - Upload files and create video tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  upload   Upload local files to OSS
  create   Create a video generation task (JSON args)
  fetch    Fetch video information by IDs

For dedicated task scripts, use:
  python3 product-to-video.py    # Product to video
  python3 image-to-ad-video.py   # Image to ad video
  python3 replicate-video.py     # Replicate video
  python3 poll-videos.py         # Poll for results

Task Types (for create command):
  product-to-video      Product image to video (sora2)
  image-to-ad-video-v2  Images to ad video (vidu)
  replicate-video       Video replication (vidu)

Examples:
  python3 impl.py upload --file /path/to/image.jpg
  python3 impl.py create "sora2/product-to-video" --args '{"product_name":"Product","image":"path.jpg","aspect_ratio":"16:9","duration":12}'
  python3 impl.py fetch --video-ids video_id1 video_id2
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Upload command
    upload_parser = subparsers.add_parser("upload", help="Upload files to OSS")
    upload_parser.add_argument("--file", "-f", help="Single file to upload")
    upload_parser.add_argument("--files", nargs="+", help="Multiple files to upload")
    upload_parser.add_argument("--type", "-t", choices=["image", "video", "blog"],
                               help="Upload type (auto-detected if not specified)")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a video generation task")
    create_parser.add_argument("task_type", help="Task type")
    create_parser.add_argument("--args", required=True, help="JSON string of task arguments")
    create_parser.add_argument("--user-id", default="", help="User ID (optional)")
    create_parser.add_argument("--no-auto-upload", action="store_true",
                               help="Disable automatic upload of local files")

    # Fetch command
    fetch_parser = subparsers.add_parser("fetch", help="Fetch video information by IDs")
    fetch_parser.add_argument("--video-ids", nargs="+", required=True, help="Video IDs to fetch")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "upload":
        if args.file:
            result = upload_file(args.file, args.type)
        elif args.files:
            result = upload_multiple_files(args.files, args.type)
        else:
            print("Error: Please specify --file or --files")
            sys.exit(1)
        print(json.dumps(result, indent=2))
        if result.get("status") != "success":
            sys.exit(1)

    elif args.command == "create":
        task_type = TASK_TYPES.get(args.task_type, args.task_type)
        try:
            task_args = json.loads(args.args)
        except json.JSONDecodeError as e:
            print(json.dumps({"status": "error", "error": f"Invalid JSON args: {e}"}))
            sys.exit(1)

        result = create_task(task_type, task_args, args.user_id, auto_upload=not args.no_auto_upload)
        print(json.dumps(result, indent=2))
        if result.get("status") != "success":
            sys.exit(1)

    elif args.command == "fetch":
        result = fetch_videos(args.video_ids)
        print(json.dumps(result, indent=2))
        if result.get("status") != "success":
            sys.exit(1)


if __name__ == "__main__":
    main()