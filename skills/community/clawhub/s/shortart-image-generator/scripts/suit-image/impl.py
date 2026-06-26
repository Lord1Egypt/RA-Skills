"""
Suit Image Creator Skill - Entry Point
"""
import json
import logging
import sys
import os
import time
import requests
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).parent.parent))
from client import ShortArtClient

def execute(
    prompt: str = "",
    image: str = None,
    upload: str = None,
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
        base_url="https://api.shortart.ai"  # For testing, replace with actual API URL in production
    )

    # Download mode
    if download:
        return _download_images(download, api_key)

    # Poll mode
    if poll:
        return _poll_project(client, poll)

    # Submit mode
    logger.info(f"[suit-image-creator] prompt={prompt[:60]!r}")

    oss_image = image

    if upload:
        up = client.upload_image(upload)
        if up["status"] != "success":
            return json.dumps(up, ensure_ascii=False)
        oss_image = up["path"]
        logger.info(f"[suit-image-creator] uploaded: {up['path']}")

    if not oss_image:
        return json.dumps({
            "status": "error",
            "error": "Must provide either --image or --upload parameter"
        }, ensure_ascii=False)

    result = client.create_suit_image(prompt=prompt, image=oss_image)

    if result["status"] == "success":
        print(f"✅ Task submitted (project_id: {result['project_id']})", file=sys.stderr)

    return json.dumps(result, ensure_ascii=False, indent=2)

def _poll_project(client: ShortArtClient, project_id: str) -> str:
    """Poll project until completion"""
    interval = 6
    timeout = 300
    start_time = time.time()

    print(f"⏳ Polling project {project_id}...", file=sys.stderr)

    while time.time() - start_time < timeout:
        result = client.get_project(project_id)

        if result["status"] == "error":
            return json.dumps(result, ensure_ascii=False, indent=2)

        project_status = result.get("project_status")
        if project_status == "completed":
            print(f"✅ Generation completed!", file=sys.stderr)
            return json.dumps({**result, "status": "completed"}, ensure_ascii=False, indent=2)
        elif project_status == "failed":
            print(f"❌ Generation failed", file=sys.stderr)
            return json.dumps({**result, "status": "failed"}, ensure_ascii=False, indent=2)

        time.sleep(interval)

    return json.dumps({"status": "timeout", "error": "Polling timeout"}, ensure_ascii=False)

def _download_images(result_json: str, api_key: str) -> str:
    """Download images to local directory"""
    try:
        result = json.loads(result_json)
        if result.get("status") != "completed":
            return json.dumps({"status": "error", "error": "Result is not completed"}, ensure_ascii=False)

        download_dir = Path.home() / "Downloads"
        download_dir.mkdir(exist_ok=True)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        downloaded = []

        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        for idx, img in enumerate(result.get("images", []), 1):
            url = img["url"]
            ext = Path(img["path"]).suffix or ".jpg"
            filename = f"shortart_suit_{timestamp}_{idx}{ext}"
            filepath = download_dir / filename

            resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()

            with open(filepath, "wb") as f:
                f.write(resp.content)

            downloaded.append(str(filepath))
            print(f"✅ Downloaded: {filepath}", file=sys.stderr)

        return json.dumps({"status": "success", "files": downloaded}, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", nargs="?", default="")
    parser.add_argument("--image", help="OSS image path")
    parser.add_argument("--upload", help="Local image path to upload")
    parser.add_argument("--poll", help="Poll project by ID")
    parser.add_argument("--download", help="Download images from result JSON")
    args = parser.parse_args()

    result = execute(
        prompt=args.prompt,
        image=args.image,
        upload=args.upload,
        poll=args.poll,
        download=args.download,
    )
    print(result)
