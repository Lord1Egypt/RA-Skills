#!/usr/bin/env python3
"""
Wuli Platform - Unified AI Image/Video Generation Skill
Uses WULI_API_TOKEN env var for Bearer token authentication via the open platform API.
"""

import argparse
import json
import os
import platform
import struct
import subprocess
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

API_BASE = "https://platform.wuli.art/api/v1/platform"

CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".mp4": "video/mp4",
    ".mov": "video/quicktime",
    ".avi": "video/x-msvideo",
    ".webm": "video/webm",
}

ACTION_DEFAULTS = {
    "image-gen": {
        "media_type": "IMAGE",
        "predict_type": "TXT_2_IMG",
        "model": "Qwen Image 2.0",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "needs_image": False,
    },
    "image-edit": {
        "media_type": "IMAGE",
        "predict_type": "REF_2_IMG",
        "model": "Qwen Image 2.0",
        "aspect_ratio": "1:1",
        "resolution": "2K",
        "needs_image": True,
    },
    "txt2video": {
        "media_type": "VIDEO",
        "predict_type": "TXT_2_VIDEO",
        "model": "通义万相 2.2 Turbo",
        "aspect_ratio": "16:9",
        "resolution": "720P",
        "needs_image": False,
    },
    "image2video": {
        "media_type": "VIDEO",
        "predict_type": "FF_2_VIDEO",
        "model": "通义万相 2.2 Turbo",
        "aspect_ratio": "16:9",
        "resolution": "720P",
        "needs_image": True,
    },
    "flf2video": {
        "media_type": "VIDEO",
        "predict_type": "FLF_2_VIDEO",
        "model": "可灵 3.0",
        "aspect_ratio": "16:9",
        "resolution": "720P",
        "needs_image": True,
    },
    "auto-video": {
        "media_type": "VIDEO",
        "predict_type": "AUTO_VIDEO",
        "model": "通义万相 2.6",
        "aspect_ratio": "16:9",
        "resolution": "720P",
        "needs_image": False,
    },
}


def get_image_size(data):
    """Extract (width, height) from common image formats using stdlib. Returns (None, None) on failure."""
    try:
        # PNG: signature + IHDR chunk
        if data[:8] == b"\x89PNG\r\n\x1a\n":
            w, h = struct.unpack(">II", data[16:24])
            return int(w), int(h)

        # GIF
        if data[:6] in (b"GIF87a", b"GIF89a"):
            w, h = struct.unpack("<HH", data[6:10])
            return int(w), int(h)

        # BMP
        if data[:2] == b"BM":
            w, h = struct.unpack("<ii", data[18:26])
            return int(w), abs(int(h))

        # WebP (RIFF....WEBP)
        if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
            fourcc = data[12:16]
            if fourcc == b"VP8 ":
                # VP8 lossy: width/height at offset 26, 14-bit little-endian
                w = struct.unpack("<H", data[26:28])[0] & 0x3FFF
                h = struct.unpack("<H", data[28:30])[0] & 0x3FFF
                return int(w), int(h)
            if fourcc == b"VP8L":
                b0, b1, b2, b3 = data[21], data[22], data[23], data[24]
                w = 1 + (((b1 & 0x3F) << 8) | b0)
                h = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
                return int(w), int(h)
            if fourcc == b"VP8X":
                w = 1 + (data[24] | (data[25] << 8) | (data[26] << 16))
                h = 1 + (data[27] | (data[28] << 8) | (data[29] << 16))
                return int(w), int(h)

        # JPEG: scan for SOF markers
        if data[:2] == b"\xff\xd8":
            i = 2
            n = len(data)
            while i < n - 9:
                if data[i] != 0xFF:
                    i += 1
                    continue
                while i < n and data[i] == 0xFF:
                    i += 1
                if i >= n:
                    break
                marker = data[i]
                i += 1
                # Standalone markers with no payload
                if marker in (0xD8, 0xD9) or (0xD0 <= marker <= 0xD7):
                    continue
                if i + 2 > n:
                    break
                seg_len = struct.unpack(">H", data[i:i + 2])[0]
                # SOF markers: C0-CF except C4, C8, CC
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    if i + 7 > n:
                        break
                    h = struct.unpack(">H", data[i + 3:i + 5])[0]
                    w = struct.unpack(">H", data[i + 5:i + 7])[0]
                    return int(w), int(h)
                i += seg_len
    except Exception:
        pass
    return None, None


def api_request(method, url, token, data=None, content_type="application/json"):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
    }
    extra_cookie = os.environ.get("WULI_EXTRA_COOKIE")
    if extra_cookie:
        headers["Cookie"] = extra_cookie
    body = None
    if data is not None:
        if content_type == "application/json":
            body = json.dumps(data).encode("utf-8")
            headers["Content-Type"] = "application/json"
        else:
            body = data
            headers["Content-Type"] = content_type

    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"Error: HTTP {e.code} - {err_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def upload_file(file_path, token):
    path = Path(file_path)
    if not path.is_file():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    filename = path.name
    print(f"Uploading file: {filename} ...")

    encoded_filename = urllib.parse.quote(filename)
    resp = api_request("GET", f"{API_BASE}/image/getUploadUrl?filename={encoded_filename}", token)
    if not resp.get("success"):
        print(f"Error: Failed to get upload URL: {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    upload_url = resp["data"]["uploadUrl"]
    # Build public URL from upload_url (strip query params)
    parsed = urllib.parse.urlparse(upload_url)
    public_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    file_data = path.read_bytes()
    put_req = urllib.request.Request(upload_url, data=file_data, method="PUT")
    put_req.add_header("Content-Type", "application/octet-stream")
    with urllib.request.urlopen(put_req, timeout=120) as _:
        pass

    width, height = get_image_size(file_data)
    print(f"Upload complete: {public_url}")
    return public_url, width, height


def upload_url_media(media_url, token):
    """Download a remote media file and re-upload it to OSS."""
    print(f"Downloading remote media: {media_url} ...")
    req = urllib.request.Request(media_url)
    with urllib.request.urlopen(req, timeout=60) as resp:
        media_data = resp.read()
        ct = resp.headers.get("Content-Type", "")

    ext = ".jpg"
    for suffix, mime in CONTENT_TYPES.items():
        if mime in ct:
            ext = suffix
            break

    url_path = urllib.parse.urlparse(media_url).path
    if "." in url_path.split("/")[-1]:
        ext = "." + url_path.split("/")[-1].rsplit(".", 1)[-1].lower()

    filename = f"upload{ext}"
    encoded_filename = urllib.parse.quote(filename)
    print(f"Re-uploading to OSS as {filename} ...")

    resp = api_request("GET", f"{API_BASE}/image/getUploadUrl?filename={encoded_filename}", token)
    if not resp.get("success"):
        print(f"Error: Failed to get upload URL: {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    upload_url = resp["data"]["uploadUrl"]

    # Build public URL from upload_url (strip query params)
    parsed = urllib.parse.urlparse(upload_url)
    public_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    put_req = urllib.request.Request(upload_url, data=media_data, method="PUT")
    put_req.add_header("Content-Type", "application/octet-stream")
    with urllib.request.urlopen(put_req, timeout=120) as _:
        pass

    width, height = get_image_size(media_data)
    print(f"Upload complete: {public_url}")
    return public_url, width, height


def parse_list_arg(value):
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def upload_inputs(file_paths, remote_urls, token):
    uploaded = []
    for file_path in file_paths:
        uploaded.append(upload_file(file_path, token))
    for remote_url in remote_urls:
        uploaded.append(upload_url_media(remote_url, token))
    return uploaded


def get_no_watermark_urls(task_ids, token):
    """Fetch no-watermark URLs for given task IDs."""
    urls = {}
    for task_id in task_ids:
        try:
            resp = api_request("POST", f"{API_BASE}/predict/noWatermarkImage", token,
                               data={"taskId": task_id})
            if resp.get("success") and resp.get("data", {}).get("url"):
                urls[task_id] = resp["data"]["url"]
        except Exception:
            pass
    return urls


def download_file(url, filename):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=120) as resp:
        Path(filename).write_bytes(resp.read())


def open_file(filepath):
    """Open a local file with the OS default viewer after download."""
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", filepath])
        elif system == "Windows":
            os.startfile(filepath)
        elif system == "Linux":
            subprocess.Popen(["xdg-open", filepath])
    except Exception:
        pass


def main():
    parser = argparse.ArgumentParser(description="Wuli Platform - AI Image/Video Generation")
    parser.add_argument("--action", required=True, choices=ACTION_DEFAULTS.keys(),
                        help="Action: image-gen, image-edit, txt2video, image2video, flf2video, auto-video")
    parser.add_argument("--prompt", required=True, help="Generation prompt (max 2000 chars)")
    parser.add_argument("--model", default=None, help="Model name")
    parser.add_argument("--aspect_ratio", default=None, help="Aspect ratio (e.g. 1:1, 16:9)")
    parser.add_argument("--resolution", default=None, help="Resolution (e.g. 2K, 4K, 720P, 1080P)")
    parser.add_argument("--n", type=int, default=1, help="Number of images (1-4, image only)")
    parser.add_argument("--image_url", default=None,
                        help="Reference image URL(s), comma-separated for multiple images")
    parser.add_argument("--image_path", default=None,
                        help="Local image path(s), comma-separated for multiple files")
    parser.add_argument("--end_image_url", default=None,
                        help="End-frame image URL for flf2video")
    parser.add_argument("--end_image_path", default=None,
                        help="End-frame local image path for flf2video")
    parser.add_argument("--video_url", default=None,
                        help="Reference video URL(s), comma-separated for auto-video")
    parser.add_argument("--video_path", default=None,
                        help="Local video path(s), comma-separated for auto-video")
    parser.add_argument("--duration", type=int, default=None, help="Video duration in seconds")
    parser.add_argument("--negative_prompt", default=None, help="Negative prompt")
    parser.add_argument("--quality", default=None,
                        help="Image quality for supported models: low/medium/high or 低画质/标准画质/高画质")
    parser.set_defaults(optimize=True)
    parser.add_argument("--optimize", action="store_true", dest="optimize",
                        help="Enable prompt optimization (default)")
    parser.add_argument("--no-optimize", action="store_false", dest="optimize",
                        help="Disable prompt optimization")
    parser.set_defaults(sound=None)
    parser.add_argument("--sound", action="store_true", dest="sound",
                        help="Enable sound for supported video models")
    parser.add_argument("--no-sound", action="store_false", dest="sound",
                        help="Disable sound for video output")
    args = parser.parse_args()

    token = os.environ.get("WULI_API_TOKEN")
    if not token:
        print("Error: WULI_API_TOKEN environment variable is not set\n"
              "Get your API token from https://wuli.art (左下角 -> API 开放平台)\n"
              "Then set it:\n"
              '  export WULI_API_TOKEN="wuli-your-token-here"', file=sys.stderr)
        sys.exit(1)

    cfg = ACTION_DEFAULTS[args.action]
    model = args.model or cfg["model"]
    aspect_ratio = args.aspect_ratio or cfg["aspect_ratio"]
    resolution = args.resolution or cfg["resolution"]
    media_type = cfg["media_type"]
    predict_type = cfg["predict_type"]

    image_paths = parse_list_arg(args.image_path)
    image_urls = parse_list_arg(args.image_url)
    end_image_paths = parse_list_arg(args.end_image_path)
    end_image_urls = parse_list_arg(args.end_image_url)
    video_paths = parse_list_arg(args.video_path)
    video_urls = parse_list_arg(args.video_url)

    if cfg["needs_image"] and not (image_paths or image_urls or end_image_paths or end_image_urls):
        print(f"Error: image input is required for {args.action}", file=sys.stderr)
        sys.exit(1)

    # Handle media inputs: always upload to OSS (local file or remote URL)
    uploaded_images = upload_inputs(image_paths, image_urls, token)
    uploaded_end_images = upload_inputs(end_image_paths, end_image_urls, token)
    uploaded_videos = upload_inputs(video_paths, video_urls, token)

    input_images = uploaded_images + uploaded_end_images
    input_videos = uploaded_videos

    if args.action == "image-edit":
        if not input_images:
            print("Error: image-edit requires at least one reference image", file=sys.stderr)
            sys.exit(1)
        if input_videos:
            print("Error: image-edit does not accept video input", file=sys.stderr)
            sys.exit(1)
    elif args.action == "image2video":
        if len(input_images) != 1:
            print("Error: image2video requires exactly one reference image", file=sys.stderr)
            sys.exit(1)
        if input_videos:
            print("Error: image2video does not accept video input", file=sys.stderr)
            sys.exit(1)
    elif args.action == "flf2video":
        if len(input_images) != 2:
            print("Error: flf2video requires exactly two reference images (start and end frame)", file=sys.stderr)
            sys.exit(1)
        if input_videos:
            print("Error: flf2video does not accept video input", file=sys.stderr)
            sys.exit(1)
    elif args.action == "auto-video":
        if not input_images and not input_videos:
            print("Error: auto-video requires at least one reference image or video", file=sys.stderr)
            sys.exit(1)

    def _image_item(entry):
        url, w, h = entry
        item = {"imageUrl": url}
        if w is not None and h is not None:
            item["width"] = w
            item["height"] = h
        return item

    input_image_list = [_image_item(entry) for entry in input_images]
    input_video_list = [{"imageUrl": url} for url, _, _ in input_videos]

    # Warn loudly if we couldn't extract image dimensions — backend validators
    # for Wan 2.6/2.7, Seedream, Hailuo, etc. dereference width/height directly
    # and will NPE (HTTP 500) without them.
    missing_dims = [item["imageUrl"] for item in input_image_list if "width" not in item]
    if missing_dims:
        print("Warning: could not extract width/height for: "
              + ", ".join(missing_dims)
              + " (some models' validators require these and will fail).",
              file=sys.stderr)

    # Build request
    body = {
        "modelName": model,
        "mediaType": media_type,
        "predictType": predict_type,
        "prompt": args.prompt,
        "aspectRatio": aspect_ratio,
        "resolution": resolution,
        "n": args.n if media_type == "IMAGE" else 1,
        "optimizePrompt": args.optimize,
        "inputImageList": input_image_list,
        "inputVideoList": input_video_list,
    }

    duration = args.duration
    if media_type == "VIDEO":
        body["videoTotalSeconds"] = duration if duration else 5
        if args.sound is not None:
            body["sound"] = args.sound
    if args.quality:
        body["quality"] = args.quality
    if args.negative_prompt:
        body["negativePrompt"] = args.negative_prompt

    print(f"\n=== Wuli Platform: {args.action} ===")
    print(f"Model:  {model}")
    print(f"Prompt: {args.prompt}")
    print(f"Optimize Prompt: {body['optimizePrompt']}")
    if media_type == "VIDEO":
        print(f"Duration: {body.get('videoTotalSeconds', 5)}s")
        if args.sound is None:
            print("Sound: auto (backend default)")
        else:
            print(f"Sound: {args.sound}")
    print(f"Aspect: {aspect_ratio}  Resolution: {resolution}")
    if args.quality:
        print(f"Quality: {args.quality}")
    if input_image_list:
        print(f"Image refs: {len(input_image_list)}")
    if input_video_list:
        print(f"Video refs: {len(input_video_list)}")
    print("\nSubmitting request...")

    # Submit
    resp = api_request("POST", f"{API_BASE}/predict/submit", token, data=body)
    if not resp.get("success"):
        print(f"Error: Submit failed - {json.dumps(resp, ensure_ascii=False)}", file=sys.stderr)
        sys.exit(1)

    record_id = resp["data"]["recordId"]
    print(f"Record ID: {record_id}")
    print("Waiting for generation...")

    # Poll
    poll_interval = 10 if media_type == "VIDEO" else 5
    max_attempts = 120 if media_type == "VIDEO" else 60

    for attempt in range(1, max_attempts + 1):
        time.sleep(poll_interval)

        query_resp = api_request("GET", f"{API_BASE}/predict/query?recordId={record_id}", token)
        status = query_resp.get("data", {}).get("recordStatus", "UNKNOWN")

        if status == "SUCCEED":
            print("Generation completed!\n")
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            results = query_resp["data"].get("results", [])

            # Fetch no-watermark URLs
            task_ids = [item["taskId"] for item in results if item.get("taskId")]
            print("Fetching no-watermark URLs...")
            nw_urls = get_no_watermark_urls(task_ids, token)

            if media_type == "IMAGE":
                downloaded = []
                for i, item in enumerate(results, 1):
                    task_id = item.get("taskId")
                    url = nw_urls.get(task_id) or item.get("imageUrl")
                    if url:
                        filename = f"wuli_image_{timestamp}_{i}.png"
                        src = "no-watermark" if task_id in nw_urls else "watermarked"
                        print(f"Downloading ({src}): {filename}")
                        download_file(url, filename)
                        downloaded.append(filename)
                print(f"\nDownloaded {len(downloaded)} image(s) to current directory")
                for f in downloaded:
                    open_file(f)
            else:
                task_id = results[0].get("taskId") if results else None
                url = nw_urls.get(task_id) or (results[0].get("imageUrl") if results else None)
                if url:
                    filename = f"wuli_video_{timestamp}.mp4"
                    src = "no-watermark" if task_id in nw_urls else "watermarked"
                    print(f"Downloading ({src}): {filename}")
                    download_file(url, filename)
                    print("Video downloaded to current directory")
                    open_file(filename)
            return

        if status in ("FAILED", "REVIEW_FAILED", "TIMEOUT", "CANCELLED"):
            print(f"Generation {status}")
            for item in query_resp.get("data", {}).get("results", []):
                err = item.get("errorMsg")
                if err:
                    print(f"  Task {item.get('taskId')}: {err}")
            sys.exit(1)

        elapsed = attempt * poll_interval
        print(f"Status: {status} ({elapsed}s elapsed)")

    print(f"Timeout: Generation took too long (>{max_attempts * poll_interval}s)")
    sys.exit(1)


if __name__ == "__main__":
    main()
