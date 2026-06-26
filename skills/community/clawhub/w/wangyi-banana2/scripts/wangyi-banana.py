#!/usr/bin/env python3
"""
WangYi Banana API client for OpenClaw.

Supports image and video generation via nano-banana and SORA2 APIs.
Uses only Python stdlib and curl.

Modes:
  --check                          Account health check (key + balance)
  --list                           List available tasks
  --info TASK                      Show task details
  --task TASK --prompt "..." ...   Execute a generation task
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# API host（只使用主地址，避免切到你没有权限的备份域名）
DEFAULT_HOST = "https://ai.t8star.cn"
MAX_POLL_SECONDS = 1800  # 30 minutes for video
POLL_INTERVAL = 5

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
CAPABILITIES_PATH = DATA_DIR / "capabilities.json"


# ---------------------------------------------------------------------------
# API key resolution
# ---------------------------------------------------------------------------

def read_key_from_openclaw_config() -> str | None:
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    if not cfg_path.exists():
        return None
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    entry = cfg.get("skills", {}).get("entries", {}).get("wangyi-banana", {})
    api_key = entry.get("apiKey")
    if isinstance(api_key, str) and api_key.strip():
        return api_key.strip()
    env_val = entry.get("env", {}).get("WANGYI_API_KEY")
    if isinstance(env_val, str) and env_val.strip():
        return env_val.strip()
    return None


def resolve_api_key(provided_key: str | None) -> str | None:
    """Resolve API key without exiting. Returns None if not found."""
    if provided_key:
        normalized = provided_key.strip()
        placeholders = {
            "your_api_key_here", "<your_api_key>",
            "YOUR_API_KEY", "WANGYI_API_KEY",
        }
        if normalized and normalized not in placeholders:
            return normalized

    env_key = os.environ.get("WANGYI_API_KEY", "").strip()
    if env_key:
        return env_key

    return read_key_from_openclaw_config()


def require_api_key(provided_key: str | None) -> str:
    key = resolve_api_key(provided_key)
    if key:
        return key
    result = {
        "error": "NO_API_KEY",
        "message": "No API key configured",
        "steps": [
            "1. Get API key from your WangYi Banana service provider",
            "2. Send the key in chat or add to ~/.openclaw/openclaw.json: skills.entries.wangyi-banana.apiKey",
        ],
    }
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(1)


# ---------------------------------------------------------------------------
# HTTP helpers (curl-based, stdlib only)
# ---------------------------------------------------------------------------

def curl_post_json(url: str, payload: dict, headers: dict, timeout: int = 60) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        tmp_path = f.name
    try:
        cmd = ["curl", "-s", "-S", "--fail-with-body", "-X", "POST", url,
               "--max-time", str(timeout), "-d", f"@{tmp_path}"]
        for k, v in headers.items():
            cmd += ["-H", f"{k}: {v}"]
        return subprocess.run(cmd, capture_output=True, text=True)
    finally:
        os.unlink(tmp_path)


def curl_post_form_data(url: str, form_data: dict, headers: dict, timeout: int = 120) -> subprocess.CompletedProcess:
    """Post multipart/form-data using curl.

    支持直接传入 Path / 文件路径，会自动按文件处理：
    - key=Path(...) 或 key=\"C:/path/to/file.png\" => -F key=@C:/path/to/file.png
    """
    cmd = ["curl", "-s", "-S", "--fail-with-body", "-X", "POST", url,
           "--max-time", str(timeout)]
    for k, v in headers.items():
        cmd += ["-H", f"{k}: {v}"]

    for key, value in form_data.items():
        # 多值（暂时不需要文件列表，这里保持简单）
        if isinstance(value, (list, tuple)):
            for item in value:
                if isinstance(item, Path):
                    cmd += ["-F", f"{key}=@{str(item)}"]
                elif isinstance(item, str) and os.path.exists(item):
                    cmd += ["-F", f"{key}=@{item}"]
                else:
                    cmd += ["-F", f"{key}={item}"]
        else:
            # 单值：优先按文件处理
            if isinstance(value, Path):
                cmd += ["-F", f"{key}=@{str(value)}"]
            elif isinstance(value, str) and os.path.exists(value):
                cmd += ["-F", f"{key}=@{value}"]
            else:
                cmd += ["-F", f"{key}={value}"]

    return subprocess.run(cmd, capture_output=True, text=True)


def api_request_with_backup(api_key: str, endpoint_suffix: str, payload: dict,
                            method: str = "POST", timeout: int = 60,
                            is_form_data: bool = False) -> dict:
    """单一主机请求封装（历史上支持多备份，这里只用 DEFAULT_HOST）。

    这样可以避免脚本自动切到你没有权限的其它域名（比如 api.gptbest.vip）。
    """
    url = f"{DEFAULT_HOST}{endpoint_suffix}"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    if not is_form_data:
        headers["Content-Type"] = "application/json"

    max_retries = 3
    last_error: dict | None = None

    for retry in range(max_retries):
        try:
            if is_form_data:
                result = curl_post_form_data(url, payload, headers, timeout)
            else:
                if method == "POST":
                    result = curl_post_json(url, payload, headers, timeout)
                else:  # GET
                    cmd = [
                        "curl", "-s", "-S", "--fail-with-body", "-X", "GET", url,
                        "--max-time", str(timeout),
                    ]
                    for k, v in headers.items():
                        cmd += ["-H", f"{k}: {v}"]
                    result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    print(f"Error: Invalid JSON response from {url}", file=sys.stderr)
                    print(f"Response: {result.stdout[:500]}", file=sys.stderr)
                    sys.exit(1)
            else:
                error_body = result.stdout or result.stderr
                try:
                    err = json.loads(error_body)
                    msg = err.get("msg", error_body)
                except (json.JSONDecodeError, TypeError):
                    msg = error_body

                last_error = {
                    "error": "API_ERROR",
                    "message": f"API request failed: {msg}",
                    "host": DEFAULT_HOST,
                    "url": url,
                }

        except Exception as e:
            last_error = {
                "error": "REQUEST_ERROR",
                "message": str(e),
                "host": DEFAULT_HOST,
            }

        if retry < max_retries - 1:
            wait_time = 1000 * (retry + 1)
            time.sleep(wait_time / 1000)
            continue

    # 所有重试失败
    if last_error:
        print(json.dumps(last_error, ensure_ascii=False), file=sys.stderr)
    else:
        print(json.dumps({
            "error": "ALL_HOSTS_FAILED",
            "message": "Primary host failed to respond"
        }, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# --check: account health check
# ---------------------------------------------------------------------------

def cmd_check(api_key_arg: str | None, host_url: str | None):
    key = resolve_api_key(api_key_arg)
    host = host_url or DEFAULT_HOST
    
    if not key:
        print(json.dumps({
            "status": "no_key",
            "message": "No API key configured",
            "steps": [
                "1. Get API key from your WangYi Banana service provider",
                "2. Send the key in chat or add to ~/.openclaw/openclaw.json: skills.entries.wangyi-banana.apiKey",
            ],
        }, ensure_ascii=False))
        return
    
    key_prefix = key[:4] + "****"
    
    # Try to check API by making a simple request
    try:
        # Use models endpoint as health check
        resp = api_request_with_backup(key, "/v1/models", {}, method="GET", timeout=10)
        print(json.dumps({
            "status": "ready",
            "key_prefix": key_prefix,
            "host": host,
            "message": "API key is valid"
        }, ensure_ascii=False))
    except SystemExit:
        print(json.dumps({
            "status": "invalid_key",
            "key_prefix": key_prefix,
            "host": host,
            "message": "API key verification failed"
        }, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Media handling
# ---------------------------------------------------------------------------

def image_to_data_uri(file_path: str) -> str:
    mime_type = mimetypes.guess_type(file_path)[0] or "image/png"
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:{mime_type};base64,{encoded}"


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

def cmd_generate_image(args):
    """Generate image (text-to-image or image-to-image)."""
    api_key = require_api_key(args.api_key)
    host = args.host_url or DEFAULT_HOST
    
    if not args.prompt:
        print("Error: --prompt is required", file=sys.stderr)
        sys.exit(1)
    
    model = args.model or "nano-banana"
    aspect_ratio = args.aspect_ratio or "4:3"
    
    # Check if it's image-to-image mode
    is_edit = model == "nano-banana-edit" or args.image
    
    if is_edit and not args.image:
        print("Error: --image is required for image-to-image mode", file=sys.stderr)
        sys.exit(1)
    
    # Build request payload
    if is_edit:
        # Image-to-image using /v1/images/edits
        endpoint = "/v1/images/edits"
        form_data = {
            "model": "nano-banana",
            "prompt": args.prompt,
            "response_format": "url"
        }
        
        # Add image file
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: image file not found: {args.image}", file=sys.stderr)
            sys.exit(1)
        
        # For form data, we need to pass file path
        form_data["image"] = image_path
        
        resp = api_request_with_backup(api_key, endpoint, form_data, is_form_data=True, timeout=120)
    elif "gemini" in model.lower():
        # Gemini model uses /v1/chat/completions
        endpoint = "/v1/chat/completions"
        content_array = [{"type": "text", "text": args.prompt}]
        
        if args.image:
            image_path = Path(args.image)
            if not image_path.exists():
                print(f"Error: image file not found: {args.image}", file=sys.stderr)
                sys.exit(1)
            image_data_uri = image_to_data_uri(str(image_path))
            content_array.append({
                "type": "image_url",
                "image_url": {"url": image_data_uri}
            })
        
        payload = {
            "model": model,
            "stream": False,
            "messages": [{"role": "user", "content": content_array}],
            "max_tokens": 4000
        }
        
        resp = api_request_with_backup(api_key, endpoint, payload, timeout=120)
        
        # Extract image URL from response
        image_url = None
        if resp.get("choices") and len(resp["choices"]) > 0:
            content = resp["choices"][0].get("message", {}).get("content", "")
            if isinstance(content, str):
                # Try to extract URL from text
                import re
                url_match = re.search(r'https?://[^\s"\'<>]+', content)
                if url_match:
                    image_url = url_match.group(0)
            elif isinstance(content, list):
                for item in content:
                    if item.get("type") == "image_url":
                        image_url = item.get("image_url", {}).get("url")
                        break
        
        if not image_url:
            print("Error: Could not extract image URL from response", file=sys.stderr)
            print(json.dumps(resp, indent=2, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
        
        # Download image
        output_path = args.output or f"/tmp/openclaw/wangyi-output/image_{int(time.time())}.png"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        cmd = ["curl", "-s", "-S", "-L", "-o", output_path, "--max-time", "300", image_url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Download failed: {result.stderr}", file=sys.stderr)
            sys.exit(1)
        
        print(f"OUTPUT_FILE:{Path(output_path).resolve()}")
        return
    else:
        # Text-to-image using /v1/images/generations
        endpoint = "/v1/images/generations"
        payload = {
            "model": model,
            "prompt": args.prompt,
            "aspect_ratio": aspect_ratio,
            "response_format": "url",
            "n": 1
        }
        
        if args.image:
            image_path = Path(args.image)
            if not image_path.exists():
                print(f"Error: image file not found: {args.image}", file=sys.stderr)
                sys.exit(1)
            image_data_uri = image_to_data_uri(str(image_path))
            payload["image_urls"] = [image_data_uri]
        
        resp = api_request_with_backup(api_key, endpoint, payload, timeout=120)
    
    # Extract image URL from response
    image_url = None
    if resp.get("data") and len(resp["data"]) > 0:
        image_url = resp["data"][0].get("url")
    elif resp.get("url"):
        image_url = resp["url"]
    
    if not image_url:
        print("Error: No image URL in response", file=sys.stderr)
        print(json.dumps(resp, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    
    # Download image
    output_path = args.output or f"/tmp/openclaw/wangyi-output/image_{int(time.time())}.png"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-s", "-S", "-L", "-o", output_path, "--max-time", "300", image_url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Download failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print(f"OUTPUT_FILE:{Path(output_path).resolve()}")


# ---------------------------------------------------------------------------
# Video generation
# ---------------------------------------------------------------------------

def poll_video_task(api_key: str, task_id: str, host: str) -> dict:
    """Poll video generation task until completion."""
    endpoint = f"/v2/videos/generations/{task_id}"
    print(f"Task ID: {task_id}", file=sys.stderr)
    print("Waiting for result", end="", flush=True, file=sys.stderr)
    
    elapsed = 0
    poll_delay = 2  # Start with 2 seconds
    
    while elapsed < MAX_POLL_SECONDS:
        time.sleep(poll_delay)
        elapsed += poll_delay
        
        resp = api_request_with_backup(api_key, endpoint, {}, method="GET", timeout=30)
        
        status = resp.get("status", "UNKNOWN")
        progress = resp.get("progress", "0%")
        
        print(".", end="", flush=True, file=sys.stderr)
        
        if status == "SUCCESS":
            print(f" done ({elapsed}s)", file=sys.stderr)
            return resp
        elif status == "FAILURE":
            fail_reason = resp.get("fail_reason", "Unknown error")
            print(f"\nTask failed: {fail_reason}", file=sys.stderr)
            sys.exit(1)
        elif status in ("NOT_START", "SUBMITTED", "QUEUED", "IN_PROGRESS"):
            # Exponential backoff, max 16 seconds
            poll_delay = min(poll_delay * 2, 16)
        else:
            # Unknown status, continue polling
            poll_delay = min(poll_delay * 2, 16)
    
    print(f"\nTimeout after {MAX_POLL_SECONDS}s", file=sys.stderr)
    sys.exit(1)


def cmd_generate_video(args):
    """Generate video (text-to-video or image-to-video)."""
    api_key = require_api_key(args.api_key)
    host = args.host_url or DEFAULT_HOST
    
    if not args.prompt:
        print("Error: --prompt is required", file=sys.stderr)
        sys.exit(1)
    
    model = args.model or "sora-2"
    duration = args.duration or "10"
    aspect_ratio = args.aspect_ratio or "16:9"
    
    # Validate parameters
    valid_models = ["sora-2", "sora-2-pro"]
    if model not in valid_models:
        model = "sora-2"
        print(f"Warning: Invalid model, using sora-2", file=sys.stderr)
    
    valid_durations = ["10", "15", "25"]
    if duration not in valid_durations:
        duration = "10"
        print(f"Warning: Invalid duration, using 10", file=sys.stderr)
    
    if duration == "25" and model != "sora-2-pro":
        duration = "15"
        print(f"Warning: 25s only supported by sora-2-pro, using 15s", file=sys.stderr)
    
    valid_aspect_ratios = ["16:9", "9:16"]
    if aspect_ratio not in valid_aspect_ratios:
        aspect_ratio = "16:9"
        print(f"Warning: Invalid aspect ratio, using 16:9", file=sys.stderr)
    
    # Build request payload
    payload = {
        "prompt": args.prompt,
        "model": model,
        "aspect_ratio": aspect_ratio,
        "duration": duration,
        "hd": args.hd or False,
        "watermark": args.watermark or False,
        "private": args.private or False
    }
    
    # Add images if provided (image-to-video)
    if args.image:
        images = []
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: image file not found: {args.image}", file=sys.stderr)
            sys.exit(1)
        image_data_uri = image_to_data_uri(str(image_path))
        images.append(image_data_uri)
        payload["images"] = images
    
    # Add character URL if provided
    if args.character_url:
        payload["character_url"] = args.character_url
        payload["character_timestamps"] = args.character_timestamps or "1,3"
    
    # Submit task
    endpoint = "/v2/videos/generations"
    print(f"Submitting video generation task...", file=sys.stderr)
    resp = api_request_with_backup(api_key, endpoint, payload, timeout=30)
    
    task_id = resp.get("task_id")
    if not task_id:
        print("Error: No task_id in response", file=sys.stderr)
        print(json.dumps(resp, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    
    # Poll for result
    final = poll_video_task(api_key, task_id, host)
    
    # Extract video URL
    task_data = final.get("data", {})
    video_url = task_data.get("output") or (task_data.get("outputs", [None])[0] if task_data.get("outputs") else None)
    
    if not video_url:
        print("Error: No video URL in response", file=sys.stderr)
        print(json.dumps(final, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    
    # Download video
    output_path = args.output or f"/tmp/openclaw/wangyi-output/video_{int(time.time())}.mp4"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-s", "-S", "-L", "-o", output_path, "--max-time", "600", video_url]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Download failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    
    print(f"OUTPUT_FILE:{Path(output_path).resolve()}")


# ---------------------------------------------------------------------------
# Character creation
# ---------------------------------------------------------------------------

def cmd_create_character(args):
    """Create character for video cameo feature."""
    api_key = require_api_key(args.api_key)
    host = args.host_url or DEFAULT_HOST
    
    if not args.url or not args.timestamps:
        print("Error: --url and --timestamps are required", file=sys.stderr)
        sys.exit(1)
    
    payload = {
        "url": args.url,
        "timestamps": args.timestamps
    }
    
    endpoint = "/sora/v1/characters"
    resp = api_request_with_backup(api_key, endpoint, payload, timeout=30)
    
    # Save result
    output_path = args.output or f"/tmp/openclaw/wangyi-output/character_{int(time.time())}.json"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resp, f, indent=2, ensure_ascii=False)
    
    print(f"OUTPUT_FILE:{Path(output_path).resolve()}")
    print(json.dumps(resp, indent=2, ensure_ascii=False))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="WangYi Banana API client for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Modes:
  --check                           Check API key
  --list                            List available tasks
  --info TASK                       Show task details
  --task TASK [options]             Execute a generation task

Tasks:
  text-to-image                     Generate image from text
  image-to-image                    Generate image from image
  text-to-video                     Generate video from text
  image-to-video                    Generate video from image
  create-character                  Create character for cameo

Examples:
  python3 wangyi-banana.py --check
  python3 wangyi-banana.py --task text-to-image --prompt "a cute dog" --output /tmp/dog.png
  python3 wangyi-banana.py --task text-to-video --prompt "a cat walking" --model sora-2 --duration 10
""",
    )
    
    # Mode flags
    parser.add_argument("--check", action="store_true", help="Check API key")
    parser.add_argument("--list", action="store_true", help="List available tasks")
    parser.add_argument("--info", metavar="TASK", help="Show details for a task")
    
    # Execution params
    parser.add_argument("--task", "-t", help="Task type")
    parser.add_argument("--prompt", "-p", help="Text prompt")
    parser.add_argument("--image", "-i", help="Input image path")
    parser.add_argument("--model", "-m", help="Model name")
    parser.add_argument("--aspect-ratio", help="Aspect ratio (4:3, 16:9, 9:16, etc.)")
    parser.add_argument("--duration", help="Video duration (10, 15, 25)")
    parser.add_argument("--hd", action="store_true", help="Enable HD mode for video")
    parser.add_argument("--watermark", action="store_true", help="Enable watermark")
    parser.add_argument("--private", action="store_true", help="Private video mode")
    parser.add_argument("--character-url", help="Character URL for cameo")
    parser.add_argument("--character-timestamps", help="Character timestamps (e.g., '1,3')")
    parser.add_argument("--url", help="Video URL for character creation")
    parser.add_argument("--timestamps", help="Timestamps for character creation")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--api-key", "-k", help="API key (optional, resolved from config)")
    parser.add_argument("--host-url", help="API host URL (default: https://ai.t8star.cn)")
    
    args = parser.parse_args()
    
    if args.check:
        cmd_check(args.api_key, args.host_url)
    elif args.list:
        tasks = [
            "text-to-image - Generate image from text",
            "image-to-image - Generate image from image",
            "text-to-video - Generate video from text",
            "image-to-video - Generate video from image",
            "create-character - Create character for cameo feature"
        ]
        print("Available tasks:")
        for task in tasks:
            print(f"  {task}")
    elif args.info:
        print(f"Task info for: {args.info}")
        print("Use --list to see all available tasks")
    elif args.task:
        if args.task == "text-to-image" or args.task == "image-to-image":
            cmd_generate_image(args)
        elif args.task == "text-to-video" or args.task == "image-to-video":
            cmd_generate_video(args)
        elif args.task == "create-character":
            cmd_create_character(args)
        else:
            print(f"Error: Unknown task: {args.task}", file=sys.stderr)
            print("Use --list to see available tasks", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
