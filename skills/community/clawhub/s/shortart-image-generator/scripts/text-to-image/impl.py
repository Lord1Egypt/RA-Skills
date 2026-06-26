"""
Image Creator Skill - Entry Point
"""
import json
import logging
import sys
import os
import time
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent.parent))
from client import ShortArtClient

def calculate_polling_params(model: str, count: int, resolution: str) -> tuple:
    """Calculate polling interval and timeout based on parameters"""
    # Base times from analysis (in seconds)
    model_times = {
        "nano-banana-pro": 40,
        "nano-banana-2": 43,
        "seedream4.5": 74,
    }

    base_time = model_times.get(model, 50)
    estimated_time = base_time + (count - 1) * 18

    if resolution == "2k":
        estimated_time = int(estimated_time * 1.5)

    interval = max(5, min(8, estimated_time * 0.15))
    timeout = max(120, estimated_time * 3)

    return interval, timeout, estimated_time

def execute(
    prompt: str = "",
    model: str = "",
    count: int = 1,
    images: list = None,
    resolution: str = "",
    aspect_ratio: str = "",
    upload: str = None,
    wait: bool = False,
    poll: str = None,
    download: str = None,
    config: Dict[str, Any] = None,
    **kwargs,
) -> str:
    if config is None:
        config = {}

    api_key = os.environ.get("SHORTART_API_KEY")

    if not api_key:
        return json.dumps({
            "status": "error",
            "error": "No API key provided. Set SHORTART_API_KEY env var"
        }, ensure_ascii=False)

    client = ShortArtClient(
        api_key=api_key,
        base_url="https://api.shortart.ai"
    )

    # Download mode
    if download:
        return _download_images(download, api_key)

    # Poll mode
    if poll:
        return _poll_project(client, poll, model, count, resolution)

    # Submit mode
    logger.info(f"[image-creator] prompt={prompt[:60]!r}, model={model}, count={count}")

    oss_images = list(images or [])

    if upload:
        up = client.upload_image(upload)
        if up["status"] != "success":
            return json.dumps(up, ensure_ascii=False)
        oss_images.append(up["path"])
        logger.info(f"[image-creator] uploaded: {up['path']}")

    max_retries = 2
    result = None
    for attempt in range(max_retries + 1):
        result = client.create_project(
            prompt=prompt,
            model=model,
            count=count,
            images=oss_images or None,
            resolution=resolution,
            aspect_ratio=aspect_ratio,
        )

        if result["status"] == "success":
            print(f"✅ Task submitted (project_id: {result['project_id']})", file=sys.stderr)
            break

        if attempt < max_retries:
            logger.warning(f"[image-creator] Attempt {attempt + 1} failed: {result.get('error')}. Retrying...")
            time.sleep(2)
        else:
            logger.error(f"[image-creator] All {max_retries + 1} attempts failed")
            return json.dumps(result, ensure_ascii=False)

    if result["status"] != "success":
        return json.dumps(result, ensure_ascii=False)

    # If wait flag is set, poll immediately
    if wait:
        return _poll_project(client, result["project_id"], model, count, resolution)

    return json.dumps(result, ensure_ascii=False)


def _poll_project(client, project_id: str, model: str, count: int, resolution: str) -> str:
    """Poll project status until completion"""
    interval, timeout, estimated = calculate_polling_params(model, count, resolution)

    print(f"⏳ Polling project {project_id} (estimated: {estimated}s)...", file=sys.stderr)

    elapsed = 0
    while elapsed < timeout:
        status = client.fetch_status(project_id)

        if status["status"] != "success":
            return json.dumps(status, ensure_ascii=False)

        project_status = status["project_status"]

        if project_status == 2:
            detail = client.get_project(project_id)
            if detail["status"] == "success":
                return json.dumps({
                    "status": "success",
                    "project_id": project_id,
                    "images": detail["images"],
                    "domain": detail["domain"],
                    "result": detail["result"]
                }, ensure_ascii=False)
        elif project_status == 3:
            return json.dumps({
                "status": "error",
                "error": status.get("project_error", "Generation failed"),
                "project_id": project_id
            }, ensure_ascii=False)

        time.sleep(interval)
        elapsed += interval

    return json.dumps({
        "status": "timeout",
        "error": f"Timeout after {timeout}s",
        "project_id": project_id
    }, ensure_ascii=False)


def _download_images(result_json: str, api_key: str) -> str:
    """Download images from result JSON"""
    from datetime import datetime

    try:
        import requests
    except ImportError:
        return json.dumps({"status": "error", "error": "requests library required"}, ensure_ascii=False)

    try:
        result = json.loads(result_json)
    except json.JSONDecodeError:
        return json.dumps({"status": "error", "error": "Invalid JSON"}, ensure_ascii=False)

    if result.get("status") != "success" or not result.get("images"):
        return json.dumps({"status": "error", "error": "No images to download"}, ensure_ascii=False)

    domain = result.get("domain", "https://file.shortart.ai/")
    images = result["images"]
    downloaded = []

    download_dir = Path.home() / "Downloads"
    download_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    headers = {}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for idx, img in enumerate(images, 1):
        url = img.get("url") or f"{domain}{img['path']}"
        ext = Path(img["path"]).suffix or ".jpg"
        filename = f"shortart_{timestamp}_{idx}{ext}"
        filepath = download_dir / filename

        try:
            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                f.write(resp.content)
            downloaded.append(str(filepath))
            print(f"✅ Downloaded: {filepath}", file=sys.stderr)
        except Exception as e:
            print(f"❌ Failed to download image {idx}: {e}", file=sys.stderr)

    return json.dumps({
        "status": "success",
        "downloaded": downloaded
    }, ensure_ascii=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate images via ShortArt")
    parser.add_argument("prompt", nargs="?", default="", help="Image description")
    parser.add_argument("--model", default="nano-banana-pro",
                        choices=["seedream4.5", "nano-banana-pro", "nano-banana-2"])
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--resolution", default="2k",
                        choices=["0.5k", "1k", "2k", "4k"])
    parser.add_argument("--aspect-ratio", default="1:1",
                        choices=["1:1", "16:9", "9:16"])
    parser.add_argument("--image", action="append", dest="images",
                        help="OSS relative path (repeat for multiple)")
    parser.add_argument("--upload", help="Local image file to upload first")
    parser.add_argument("--wait", action="store_true",
                        help="Wait for completion immediately")
    parser.add_argument("--poll", help="Poll existing project by ID")
    parser.add_argument("--download", help="Download images from result JSON")
    args = parser.parse_args()

    output = execute(
        prompt=args.prompt,
        model=args.model,
        count=args.count,
        images=args.images,
        resolution=args.resolution,
        aspect_ratio=args.aspect_ratio,
        upload=args.upload,
        wait=args.wait,
        poll=args.poll,
        download=args.download,
    )
    print(output)
