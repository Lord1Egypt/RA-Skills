"""
Template to Image Skill - Entry Point
"""
import json
import sys
import os
import time
from pathlib import Path
from typing import Dict, Any, List

sys.path.insert(0, str(Path(__file__).parent.parent))
from client import ShortArtClient as TemplateClient


def calculate_polling_params(count: int) -> tuple:
    """Calculate polling interval and timeout"""
    base_time = 50
    estimated_time = base_time + (count - 1) * 18
    interval = max(5, min(8, estimated_time * 0.15))
    timeout = max(120, estimated_time * 3)
    return interval, timeout, estimated_time


def execute(
    template_id: str = "",
    args: List[Dict] = None,
    images: List[str] = None,
    uploads: List[str] = None,
    wait: bool = False,
    poll: str = None,
    download: str = None,
    list_templates: List[str] = None,
    get_template: str = None,
    upload_image: str = None,
    count: int = 6,
    **kwargs,
) -> str:
    api_key = os.environ.get("SHORTART_API_KEY")
    if not api_key:
        return json.dumps({
            "status": "error",
            "error": "No API key provided. Set SHORTART_API_KEY env var"
        }, ensure_ascii=False)

    client = TemplateClient(
        api_key=api_key,
        base_url="https://api.shortart.ai"
    )

    # List templates mode
    if list_templates:
        result = client.list_templates(keywords=list_templates, count=count)
        return json.dumps(result, ensure_ascii=False)

    # Get template mode
    if get_template:
        result = client.get_template(slug=get_template)
        return json.dumps(result, ensure_ascii=False)

    # Upload image mode
    if upload_image:
        result = client.upload_image(upload_image)
        return json.dumps(result, ensure_ascii=False)

    # Download mode
    if download:
        return _download_images(download, api_key)

    # Poll mode
    if poll:
        count = 1
        if args:
            for arg in args:
                if arg.get("id") == "count":
                    try:
                        count = int(arg.get("default", 1))
                    except:
                        count = 1
        return _poll_project(client, poll, count)

    # Submit mode
    oss_images = list(images or [])

    if uploads:
        for upload_path in uploads:
            up = client.upload_image(upload_path)
            if up["status"] != "success":
                return json.dumps(up, ensure_ascii=False)
            oss_images.append(up["path"])

    max_retries = 2
    result = None
    for attempt in range(max_retries + 1):
        result = client.create_from_template(
            template_id=template_id,
            args=args or [],
            images=oss_images,
        )

        if result["status"] == "success":
            print(f"✅ Task submitted (project_id: {result['project_id']})", file=sys.stderr)
            break

        if attempt < max_retries:
            time.sleep(2)
        else:
            return json.dumps(result, ensure_ascii=False)

    if result["status"] != "success":
        return json.dumps(result, ensure_ascii=False)

    # If wait flag is set, poll immediately
    if wait:
        count = 1
        if args:
            for arg in args:
                if arg.get("id") == "count":
                    try:
                        count = int(arg.get("default", 1))
                    except:
                        count = 1
        return _poll_project(client, result["project_id"], count)

    return json.dumps(result, ensure_ascii=False)


def _poll_project(client, project_id: str, count: int) -> str:
    """Poll project status until completion"""
    interval, timeout, estimated = calculate_polling_params(count)

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
        filename = f"shortart_template_{timestamp}_{idx}{ext}"
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

    parser = argparse.ArgumentParser(description="Generate images from template")
    parser.add_argument("--list-templates", nargs="+", help="List templates by keywords")
    parser.add_argument("--get-template", help="Get template by slug")
    parser.add_argument("--upload-image", help="Upload image to OSS")
    parser.add_argument("--count", type=int, default=6, help="Number of templates to return")
    parser.add_argument("--template-id", help="Template ID")
    parser.add_argument("--args", help="JSON string of args")
    parser.add_argument("--image", action="append", dest="images", help="OSS image paths")
    parser.add_argument("--uploads", action="append", help="Local images to upload")
    parser.add_argument("--wait", action="store_true", help="Wait for completion immediately")
    parser.add_argument("--poll", help="Poll existing project by ID")
    parser.add_argument("--download", help="Download images from result JSON")

    parsed = parser.parse_args()

    # List templates mode
    if parsed.list_templates:
        output = execute(list_templates=parsed.list_templates, count=parsed.count)
        print(output)
        sys.exit(0)

    # Get template mode
    if parsed.get_template:
        output = execute(get_template=parsed.get_template)
        print(output)
        sys.exit(0)

    # Upload image mode
    if parsed.upload_image:
        output = execute(upload_image=parsed.upload_image)
        print(output)
        sys.exit(0)

    # Handle different modes
    if parsed.download:
        output = execute(download=parsed.download)
        print(output)
        sys.exit(0)

    if parsed.poll:
        args_list = []
        if parsed.args:
            try:
                args_list = json.loads(parsed.args)
            except json.JSONDecodeError:
                print(json.dumps({"status": "error", "error": "Invalid JSON in --args"}))
                sys.exit(1)
        output = execute(poll=parsed.poll, args=args_list)
        print(output)
        sys.exit(0)

    # Submit mode requires template-id and args
    if not parsed.template_id or not parsed.args:
        parser.error("--template-id and --args are required for submit mode")

    try:
        args_list = json.loads(parsed.args)
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "error": "Invalid JSON in --args"}))
        sys.exit(1)

    output = execute(
        template_id=parsed.template_id,
        args=args_list,
        images=parsed.images,
        uploads=parsed.uploads,
        wait=parsed.wait,
    )
    print(output)
