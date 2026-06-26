#!/usr/bin/env python3
"""
Product to Video Creator

Generate marketing videos from product images using Sora2 AI.
Task type: sora2/product-to-video

Usage:
    python3 product-to-video.py --product-name "<name>" --image <image_path> --aspect-ratio <ratio> --duration <seconds> [options]
"""

import argparse
import json
import os
import sys
import tempfile
import time
import uuid
from typing import Any

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests")
    sys.exit(1)


# Constants
VALID_ASPECT_RATIOS = ["16:9", "9:16"]
VALID_DURATIONS = [12]  # Only 12 seconds supported
MAX_PROMPT_LENGTH = 2000
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# Video status
STATUS_PENDING = 0
STATUS_PROCESSING = 1
STATUS_COMPLETED = 2
STATUS_FAILED = 3

STATUS_NAMES = {
    STATUS_PENDING: "Pending",
    STATUS_PROCESSING: "Processing",
    STATUS_COMPLETED: "Completed",
    STATUS_FAILED: "Failed"
}


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


def is_url(path: str) -> bool:
    """Check if path is a URL."""
    return path and path.startswith(("http://", "https://"))


def is_local_file(path: str) -> bool:
    """Check if path is a local file."""
    if not path:
        return False
    if path.startswith(("http://", "https://", "oss://")):
        return False
    return os.path.isfile(path)


def is_oss_path(path: str) -> bool:
    """Check if path is an OSS path."""
    if not path:
        return False
    if path.startswith("oss://"):
        return True
    # OSS identifiers like d2mm4m9addr0008000a0.png
    if "/" not in path and "." in path:
        return True
    return False


def get_extension_from_url(url: str) -> str:
    """Extract file extension from URL."""
    path = url.split("?")[0]
    ext = os.path.splitext(path)[1].lower()
    valid_exts = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"]
    return ext if ext in valid_exts else ".jpg"


def download_image_from_url(url: str, timeout: int = 30) -> dict[str, Any]:
    """Download image from URL to a temporary file."""
    try:
        print(f"  Downloading from URL: {url}")
        response = requests.get(url, timeout=timeout, stream=True)
        response.raise_for_status()

        # Check file size
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_FILE_SIZE:
            return {"status": "error", "error": f"Image too large: {content_length} bytes (max: {MAX_FILE_SIZE})"}

        # Get extension
        ext = get_extension_from_url(url)

        # Create temp file
        temp_dir = tempfile.gettempdir()
        filename = f"shortvideo_{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join(temp_dir, filename)

        # Download to temp file
        downloaded_size = 0
        with open(temp_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
                    if downloaded_size > MAX_FILE_SIZE:
                        os.remove(temp_path)
                        return {"status": "error", "error": f"Image too large (max: {MAX_FILE_SIZE} bytes)"}

        print(f"  -> Downloaded to: {temp_path} ({downloaded_size} bytes)")
        return {"status": "success", "temp_path": temp_path, "size": downloaded_size}

    except requests.exceptions.Timeout:
        return {"status": "error", "error": "Download timed out"}
    except requests.exceptions.HTTPError as e:
        return {"status": "error", "error": f"HTTP error: {e}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "error": f"Download failed: {e}"}
    except Exception as e:
        return {"status": "error", "error": f"Download error: {e}"}


def upload_file(filepath: str, upload_type: str = "image") -> dict[str, Any]:
    """Upload a local file to OSS."""
    base_url, api_key = get_config()

    if not os.path.isfile(filepath):
        return {"status": "error", "error": f"File not found: {filepath}"}

    file_size = os.path.getsize(filepath)
    if file_size > MAX_FILE_SIZE:
        return {"status": "error", "error": f"File too large: {file_size} bytes (max: {MAX_FILE_SIZE})"}

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


def create_task(args: dict[str, Any]) -> dict[str, Any]:
    """Create a video generation task."""
    base_url, api_key = get_config()

    url = f"{base_url}/api/task/create"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "user_id": "",
        "type": "sora2/product-to-video",
        "args": args
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        result = response.json()

        code = result.get("code", -1)
        if code != 0:
            error_msg = result.get("message", result.get("info", f"Task creation failed with code {code}"))
            return {"status": "error", "error": error_msg, "code": code}

        data = result.get("data", result)
        return {
            "status": "success",
            "task_id": data.get("task_id", ""),
            "video_ids": data.get("video_ids", []),
            "asset_ids": data.get("asset_ids", []),
            "consumed_credit": data.get("consumed_credit", 0),
            "credit": data.get("credit", 0),
            "sub_credit": data.get("sub_credit", 0)
        }
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


def poll_video_results(video_ids: list[str], max_attempts: int = 60, interval: int = 10) -> dict[str, Any]:
    """Poll for video results until completed or max attempts reached."""
    print(f"Starting to poll for {len(video_ids)} video(s)...")
    print(f"Max attempts: {max_attempts}, Interval: {interval}s")
    print("Video generation typically takes 10-15 minutes. Please wait...")

    videos = []
    domain = ""

    for attempt in range(1, max_attempts + 1):
        result = fetch_videos(video_ids)

        if result.get("status") != "success":
            print(f"Attempt {attempt}/{max_attempts}: Failed to fetch - {result.get('error')}")
            time.sleep(interval)
            continue

        videos = result.get("videos", [])
        domain = result.get("domain", "")
        if not videos:
            print(f"Attempt {attempt}/{max_attempts}: No videos returned")
            time.sleep(interval)
            continue

        all_completed = True
        any_failed = False
        status_summary = []

        for video in videos:
            video_id = video.get("id", "unknown")
            status = video.get("status", STATUS_PENDING)
            status_name = STATUS_NAMES.get(status, f"Unknown({status})")
            status_summary.append(f"{video_id}: {status_name}")

            if status == STATUS_FAILED:
                any_failed = True
            elif status != STATUS_COMPLETED:
                all_completed = False

        print(f"Attempt {attempt}/{max_attempts}: [{', '.join(status_summary)}]")

        if all_completed:
            print("\nAll videos completed!")
            return {"status": "success", "message": "All videos completed", "videos": videos, "domain": domain, "attempts": attempt}

        if any_failed:
            failed_videos = [v for v in videos if v.get("status") == STATUS_FAILED]
            print(f"\nSome videos failed: {len(failed_videos)}")
            return {"status": "partial", "message": f"{len(failed_videos)} video(s) failed", "videos": videos, "domain": domain, "failed_videos": failed_videos, "attempts": attempt}

        time.sleep(interval)

    print(f"\nMax polling attempts ({max_attempts}) reached.")
    return {"status": "timeout", "message": f"Polling timed out after {max_attempts} attempts", "videos": videos, "domain": domain, "attempts": max_attempts}


def print_video_results(videos: list[dict], domain: str = ""):
    """Pretty print video results with full URLs."""
    print("\n" + "=" * 60)
    print("VIDEO RESULTS")
    print("=" * 60)

    for video in videos:
        video_id = video.get("id", "unknown")
        status = video.get("status", STATUS_PENDING)
        status_name = STATUS_NAMES.get(status, f"Unknown({status})")

        print(f"\nVideo ID: {video_id}")
        print(f"  Status: {status_name}")

        if status == STATUS_COMPLETED:
            duration = video.get("duration", 0)
            width = video.get("width", 0)
            height = video.get("height", 0)
            print(f"  Duration: {duration}s")
            print(f"  Resolution: {width}x{height}")

            specs = video.get("specs", {})
            if specs:
                print("  Files:")
                for quality, spec in specs.items():
                    video_path = spec.get("video", "")
                    cover_path = spec.get("cover", "")
                    size = spec.get("size", 0)
                    size_mb = size / (1024 * 1024) if size else 0

                    # Build full URLs
                    video_url = f"{domain}{video_path}" if domain and video_path else video_path
                    cover_url = f"{domain}{cover_path}" if domain and cover_path else cover_path

                    print(f"    [{quality}]")
                    print(f"      Video: {video_url}")
                    print(f"      Cover: {cover_url}")
                    if size:
                        print(f"      Size: {size_mb:.2f} MB")


def validate_args(product_name: str, image: str, aspect_ratio: str, duration: int) -> list[str]:
    """Validate arguments."""
    errors = []

    # Validate product_name
    if not product_name:
        errors.append("product_name is required")

    # Validate image
    if not image:
        errors.append("image is required")

    # Validate aspect ratio
    if aspect_ratio not in VALID_ASPECT_RATIOS:
        errors.append(f"aspect_ratio must be one of {VALID_ASPECT_RATIOS}, got {aspect_ratio}")

    # Validate duration
    if duration not in VALID_DURATIONS:
        errors.append(f"duration must be one of {VALID_DURATIONS}, got {duration}")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Create product-to-video task",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # With local image
  python3 product-to-video.py --product-name "Premium Headphones" --image /path/to/product.jpg --aspect-ratio 16:9 --duration 12

  # With URL image
  python3 product-to-video.py --product-name "Smart Watch" --image https://example.com/product.jpg --aspect-ratio 9:16 --duration 12

  # With product info
  python3 product-to-video.py --product-name "Headphones" --product-info "Wireless noise-canceling" --image product.jpg --aspect-ratio 16:9 --duration 12

  # Without polling
  python3 product-to-video.py --product-name "Product" --image product.jpg --aspect-ratio 16:9 --duration 12 --no-poll
        """
    )

    parser.add_argument("--product-name", required=True,
                        help="Name of the product")
    parser.add_argument("--product-info", default=None,
                        help="Product description/details (optional)")
    parser.add_argument("--image", required=True,
                        help="Product image path (local, OSS, or URL)")
    parser.add_argument("--aspect-ratio", required=True, choices=VALID_ASPECT_RATIOS,
                        help=f"Video ratio: {VALID_ASPECT_RATIOS}")
    parser.add_argument("--duration", type=int, required=True,
                        help=f"Video duration: {VALID_DURATIONS} seconds")
    parser.add_argument("--no-poll", action="store_true",
                        help="Disable automatic polling for video results")
    parser.add_argument("--max-attempts", type=int, default=60,
                        help="Max polling attempts (default: 60)")
    parser.add_argument("--interval", type=int, default=10,
                        help="Polling interval in seconds (default: 10)")

    args = parser.parse_args()

    # Validate
    errors = validate_args(args.product_name, args.image, args.aspect_ratio, args.duration)
    if errors:
        print(json.dumps({"status": "error", "error": "; ".join(errors)}, indent=2))
        sys.exit(1)

    # Track temp files for cleanup
    temp_files = []

    # Process image
    print(f"Processing image: {args.image}")
    image_path = None

    if is_url(args.image):
        # URL: download first, then upload
        download_result = download_image_from_url(args.image)
        if download_result.get("status") != "success":
            print(json.dumps({"status": "error", "error": f"Failed to download {args.image}: {download_result.get('error')}"}, indent=2))
            sys.exit(1)

        temp_path = download_result["temp_path"]
        temp_files.append(temp_path)

        # Upload the downloaded file
        upload_result = upload_file(temp_path, "image")
        if upload_result.get("status") == "success":
            image_path = upload_result["path"]
            print(f"  -> Uploaded to: {image_path}")
        else:
            print(json.dumps({"status": "error", "error": f"Failed to upload {args.image}: {upload_result.get('error')}"}, indent=2))
            sys.exit(1)

    elif is_local_file(args.image):
        # Local file: upload directly
        upload_result = upload_file(args.image, "image")
        if upload_result.get("status") == "success":
            image_path = upload_result["path"]
            print(f"  -> Uploaded to: {image_path}")
        else:
            print(json.dumps({"status": "error", "error": f"Failed to upload {args.image}: {upload_result.get('error')}"}, indent=2))
            sys.exit(1)

    elif is_oss_path(args.image):
        # OSS path: use directly
        image_path = args.image
        print(f"  Using OSS path: {image_path}")

    else:
        # Unknown path type: try to use as-is
        image_path = args.image
        print(f"  Using path as-is: {image_path}")

    # Build task args
    task_args = {
        "product_name": args.product_name,
        "image": image_path,
        "aspect_ratio": args.aspect_ratio,
        "duration": args.duration
    }

    if args.product_info:
        task_args["product_info"] = args.product_info

    # Create task
    print("\nCreating task...")
    result = create_task(task_args)

    if result.get("status") != "success":
        print(json.dumps(result, indent=2))
        sys.exit(1)

    print(f"Task created successfully!")
    print(f"  Task ID: {result.get('task_id')}")
    print(f"  Video IDs: {result.get('video_ids')}")
    print(f"  Credits consumed: {result.get('consumed_credit')}")

    # Poll for results
    if not args.no_poll:
        video_ids = result.get("video_ids", [])
        if video_ids:
            print()
            poll_result = poll_video_results(video_ids, args.max_attempts, args.interval)
            result["poll_result"] = poll_result

            # Print video results with full URLs
            if poll_result.get("status") == "success" and poll_result.get("videos"):
                print_video_results(poll_result.get("videos", []), poll_result.get("domain", ""))

    # Clean up temp files
    for temp_file in temp_files:
        try:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        except Exception:
            pass

    print("\n" + json.dumps(result, indent=2))


if __name__ == "__main__":
    main()