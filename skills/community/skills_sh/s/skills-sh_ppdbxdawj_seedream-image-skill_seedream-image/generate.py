#!/usr/bin/env python3
"""
Seedream 4.0 (jimeng_t2i_v40) Image Generation Script

Usage:
    python generate.py --prompt "一只猫在花园里玩耍，水彩风格"
    python generate.py --prompt "将背景换成海边" --image-urls "https://example.com/photo.jpg"
    python generate.py --prompt "生成一组盲盒" --width 2048 --height 2048

Credentials (either):
    - Environment variables: VOLC_ACCESSKEY, VOLC_SECRETKEY
    - Or a .env file in the script directory or current directory, with:
        VOLC_ACCESSKEY=your_access_key
        VOLC_SECRETKEY=your_secret_key
"""

import argparse
import json
import os
import sys
import time
import base64
from pathlib import Path

try:
    from volcengine.visual.VisualService import VisualService
except ImportError:
    print("Error: volcengine SDK not found. Install it with:")
    print("  pip install volcengine")
    sys.exit(1)

REQ_KEY = "jimeng_t2i_v40"
DEFAULT_POLL_INTERVAL = 3
DEFAULT_MAX_WAIT = 300
TERMINAL_STATUSES = {"done", "not_found", "expired"}


def _load_dotenv() -> None:
    """Load VOLC_ACCESSKEY / VOLC_SECRETKEY from .env if not already in os.environ."""
    if os.environ.get("VOLC_ACCESSKEY") and os.environ.get("VOLC_SECRETKEY"):
        return
    for base in (Path(__file__).resolve().parent, Path.cwd()):
        env_file = base / ".env"
        if not env_file.is_file():
            continue
        for line in env_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key, value = key.strip(), value.strip().strip("'\"").strip()
                if key and key not in os.environ:
                    os.environ[key] = value
        break


def create_service() -> VisualService:
    _load_dotenv()
    ak = os.environ.get("VOLC_ACCESSKEY")
    sk = os.environ.get("VOLC_SECRETKEY")
    if not ak or not sk:
        print("Error: VOLC_ACCESSKEY and VOLC_SECRETKEY are required.")
        print("Set them via: 1) environment variables, or 2) a .env file in this directory.")
        print("Get credentials: https://console.volcengine.com/iam/keymanage/")
        sys.exit(1)

    service = VisualService()
    service.set_ak(ak)
    service.set_sk(sk)
    service.set_scheme("https")
    return service


def submit_task(
    service: VisualService,
    prompt: str,
    image_urls: list[str] | None = None,
    size: int | None = None,
    width: int | None = None,
    height: int | None = None,
    scale: float | None = None,
    force_single: bool = False,
    min_ratio: float | None = None,
    max_ratio: float | None = None,
) -> dict:
    body = {
        "req_key": REQ_KEY,
        "prompt": prompt,
    }

    if image_urls:
        body["image_urls"] = image_urls
    if size is not None:
        body["size"] = size
    if width is not None and height is not None:
        body["width"] = width
        body["height"] = height
    if scale is not None:
        body["scale"] = scale
    if force_single:
        body["force_single"] = True
    if min_ratio is not None:
        body["min_ratio"] = min_ratio
    if max_ratio is not None:
        body["max_ratio"] = max_ratio

    print(f"Submitting task...")
    print(f"  prompt: {prompt}")
    if image_urls:
        print(f"  image_urls: {len(image_urls)} image(s)")

    try:
        resp = service.cv_sync2async_submit_task(body)
    except Exception as e:
        print(f"Submit request failed: {e}")
        sys.exit(1)

    if resp.get("code") != 10000:
        print(f"Submit failed (code={resp.get('code')}): {resp.get('message')}")
        print(f"  request_id: {resp.get('request_id')}")
        sys.exit(1)

    task_id = resp["data"]["task_id"]
    print(f"  task_id: {task_id}")
    print(f"  time_elapsed: {resp.get('time_elapsed', 'N/A')}")
    return resp


def query_task(
    service: VisualService,
    task_id: str,
    return_url: bool = True,
    add_logo: bool = False,
) -> dict:
    body = {
        "req_key": REQ_KEY,
        "task_id": task_id,
    }

    req_json_obj: dict = {"return_url": return_url}
    if add_logo:
        req_json_obj["logo_info"] = {
            "add_logo": True,
            "position": 0,
            "language": 0,
            "opacity": 1,
        }
    body["req_json"] = json.dumps(req_json_obj)

    return service.cv_sync2async_get_result(body)


def poll_until_done(
    service: VisualService,
    task_id: str,
    poll_interval: int = DEFAULT_POLL_INTERVAL,
    max_wait: int = DEFAULT_MAX_WAIT,
    return_url: bool = True,
    add_logo: bool = False,
) -> dict:
    start = time.time()
    attempt = 0

    while True:
        elapsed = time.time() - start
        if elapsed > max_wait:
            print(f"\nTimeout: task not completed after {max_wait}s")
            sys.exit(1)

        attempt += 1
        resp = query_task(service, task_id, return_url=return_url, add_logo=add_logo)

        code = resp.get("code")
        data = resp.get("data")

        if code != 10000:
            if data is None:
                print(f"\nQuery failed (code={code}): {resp.get('message')}")
                print(f"  request_id: {resp.get('request_id')}")
                sys.exit(1)

        status = data.get("status", "unknown") if data else "unknown"

        if status == "done":
            print(f"\nTask completed! (attempt #{attempt}, {elapsed:.1f}s)")
            return resp

        if status in ("not_found", "expired"):
            print(f"\nTask {status}. It may have expired (12h limit) or the ID is invalid.")
            sys.exit(1)

        # in_queue / generating
        print(f"  [{elapsed:.0f}s] status: {status}", end="\r", flush=True)
        time.sleep(poll_interval)


def download_image(url: str, filepath: Path, timeout: int = 60) -> bool:
    import requests as _req

    try:
        resp = _req.get(url, timeout=timeout)
        resp.raise_for_status()
        filepath.write_bytes(resp.content)
        return True
    except Exception as e:
        print(f"  Download failed: {e}")
        return False


def save_images(resp: dict, output_dir: str) -> list[str]:
    data = resp.get("data", {})
    image_urls = data.get("image_urls") or []
    base64_list = data.get("binary_data_base64") or []

    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    saved = []
    ts = int(time.time())

    if image_urls:
        print(f"\nGenerated {len(image_urls)} image(s), downloading to {output_dir}/...")
        for i, url in enumerate(image_urls):
            filepath = out / f"seedream_{ts}_{i+1}.png"
            if download_image(url, filepath):
                size_kb = filepath.stat().st_size / 1024
                print(f"  [{i+1}] {filepath} ({size_kb:.0f} KB)")
                saved.append(str(filepath))
            else:
                print(f"  [{i+1}] URL: {url}")
                saved.append(url)

    if base64_list:
        print(f"\nSaving {len(base64_list)} base64 image(s) to {output_dir}/...")
        for i, b64 in enumerate(base64_list):
            if not b64:
                continue
            filepath = out / f"seedream_{ts}_b64_{i+1}.png"
            filepath.write_bytes(base64.b64decode(b64))
            size_kb = filepath.stat().st_size / 1024
            print(f"  [{i+1}] {filepath} ({size_kb:.0f} KB)")
            saved.append(str(filepath))

    return saved


def main():
    parser = argparse.ArgumentParser(description="Seedream 4.0 Image Generation")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--image-urls", nargs="*", default=None, help="Input image URLs (up to 10)")
    parser.add_argument("--size", type=int, default=None, help="Output area in pixels (e.g. 4194304 = 2048*2048)")
    parser.add_argument("--width", type=int, default=None, help="Output width (use with --height)")
    parser.add_argument("--height", type=int, default=None, help="Output height (use with --width)")
    parser.add_argument("--scale", type=float, default=None, help="Text influence scale 0~1 (default 0.5)")
    parser.add_argument("--no-force-single", dest="force_single", action="store_false", default=True, help="Allow multiple images (group generation); default is 1 image")
    parser.add_argument("--force-single", dest="force_single", action="store_true", help="Generate only 1 image (default)")
    parser.add_argument("--min-ratio", type=float, default=None, help="Min width/height ratio")
    parser.add_argument("--max-ratio", type=float, default=None, help="Max width/height ratio")
    parser.add_argument("--output-dir", default="output", help="Directory to save base64 images")
    parser.add_argument("--poll-interval", type=int, default=DEFAULT_POLL_INTERVAL, help="Seconds between polls")
    parser.add_argument("--max-wait", type=int, default=DEFAULT_MAX_WAIT, help="Max seconds to wait")
    parser.add_argument("--no-url", action="store_true", help="Don't request URL format (use base64)")
    parser.add_argument("--watermark", action="store_true", help="Add AI watermark to output")

    args = parser.parse_args()

    service = create_service()

    # Submit
    submit_resp = submit_task(
        service,
        prompt=args.prompt,
        image_urls=args.image_urls,
        size=args.size,
        width=args.width,
        height=args.height,
        scale=args.scale,
        force_single=args.force_single,
        min_ratio=args.min_ratio,
        max_ratio=args.max_ratio,
    )

    task_id = submit_resp["data"]["task_id"]

    # Poll
    print("Waiting for generation...")
    result = poll_until_done(
        service,
        task_id,
        poll_interval=args.poll_interval,
        max_wait=args.max_wait,
        return_url=not args.no_url,
        add_logo=args.watermark,
    )

    # Save / display results
    saved = save_images(result, args.output_dir)

    if not saved:
        print("\nNo images returned. Full response:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        sys.exit(1)

    print(f"\nDone! {len(saved)} image(s) generated.")


if __name__ == "__main__":
    main()
