#!/usr/bin/env python3
"""AI Video generation from input images using inference.sh API."""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import httpx


def _load_env_file(path: Path) -> None:
    """Load environment variables from .env file."""
    if not path.exists() or not path.is_file():
        return
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        os.environ.setdefault(key, value)


def _load_default_envs(env_file: str) -> None:
    """Load default environment files."""
    if env_file:
        _load_env_file(Path(env_file).expanduser())
        return
    skill_root = Path(__file__).resolve().parent.parent
    _load_env_file(skill_root / ".env")
    _load_env_file(Path.cwd() / ".env")


def _build_parser() -> argparse.ArgumentParser:
    """Build argument parser."""
    parser = argparse.ArgumentParser(
        description="Generate AI video from input image using inference.sh CLI."
    )
    parser.add_argument("--image", required=True, help="Input image path.")
    parser.add_argument("--prompt", required=True, help="Video description in English.")
    parser.add_argument("--model", default="veo-3.1",
                       help="Model name (veo-3.1, veo-3, seedance-1.5-pro, wan-2.5, grok-imagine-video, omnihuman).")
    parser.add_argument("--duration", type=int, default=5, help="Video duration in seconds (default 5).")
    parser.add_argument("--save-dir", default="", help="Directory for saved videos (default: ./outputs/videos).")
    parser.add_argument("--upload-service", default="imgbb", choices=["smms", "imgbb"],
                       help="Image upload service (default imgbb).")
    parser.add_argument("--api-token", default="", help="Optional API token for image upload.")
    parser.add_argument("--timeout", type=int, default=1000, help="Request timeout in seconds.")
    parser.add_argument("--env-file", default="", help="Optional .env file path.")
    parser.add_argument("--dry-run", action="store_true", help="Print request and exit.")
    return parser


def _resolve_save_dir(cli_value: str) -> Path:
    """Resolve output directory."""
    if cli_value.strip():
        return Path(cli_value).expanduser()
    return Path.cwd() / "outputs" / "videos"


def upload_to_smms(image_path: Path, api_token: str = "") -> str:
    """Upload image to SM.MS image hosting service.

    Args:
        image_path: Image file path
        api_token: SM.MS API Token (optional, anonymous upload if not provided)

    Returns:
        Image URL
    """
    url = "https://sm.ms/api/v2/upload"
    headers = {}
    if api_token:
        headers["Authorization"] = api_token

    with image_path.open("rb") as f:
        files = {"smfile": (image_path.name, f, "image/png")}
        response = httpx.post(url, files=files, headers=headers, timeout=30.0)

    response.raise_for_status()
    data = response.json()

    if data.get("success"):
        return data["data"]["url"]
    elif data.get("code") == "image_repeated":
        # Image already exists, return existing URL
        return data["images"]
    else:
        raise RuntimeError(f"Upload failed: {data.get('message', 'Unknown error')}")


def upload_to_imgbb(image_path: Path, api_key: str = None) -> str:
    """Upload image to ImgBB image hosting service.

    Args:
        image_path: Image file path
        api_key: ImgBB API Key (required)

    Returns:
        Image URL
    """
    if not api_key:
        raise ValueError("ImgBB API key is required. Provide it via --api-token or IMGBB_API_KEY environment variable.")

    url = f"https://api.imgbb.com/1/upload?key={api_key}"

    with image_path.open("rb") as f:
        files = {"image": f}
        response = httpx.post(url, files=files, timeout=30.0)

    response.raise_for_status()
    data = response.json()

    if data.get("success"):
        return data["data"]["url"]
    else:
        raise RuntimeError(f"Upload failed: {data.get('error', {}).get('message', 'Unknown error')}")


def generate_video_from_image(image_path: str, prompt: str, model: str = "veo-3.1",
                               duration: int = 5, save_dir: Path = None,
                               upload_service: str = "imgbb", api_token: str = "",
                               timeout: int = 1000, dry_run: bool = False) -> dict:
    """Generate video from input image using inference.sh CLI.

    Args:
        image_path: Input image path
        prompt: Video description in English
        model: Model name
        duration: Video duration in seconds
        save_dir: Output directory
        upload_service: Image upload service (smms/imgbb)
        api_token: API token for upload service
        timeout: Request timeout in seconds
        dry_run: Print request and exit

    Returns:
        Generation result dictionary
    """
    if save_dir is None:
        save_dir = Path.cwd() / "outputs" / "videos"

    save_dir.mkdir(parents=True, exist_ok=True)

    image_path_obj = Path(image_path).resolve()
    if not image_path_obj.exists():
        return {
            "ok": False,
            "error": f"Image file not found: {image_path_obj}"
        }

    if dry_run:
        print(json.dumps({
            "ok": True,
            "dry_run": True,
            "image_path": str(image_path_obj),
            "prompt": prompt,
            "model": model,
            "duration": duration,
            "upload_service": upload_service
        }, ensure_ascii=False, indent=2))
        return {"ok": True, "dry_run": True}

    # Step 1: Upload image to cloud storage
    try:
        if upload_service == "smms":
            image_url = upload_to_smms(image_path_obj, api_token)
        else:
            imgbb_key = api_token or os.environ.get("IMGBB_API_KEY")
            image_url = upload_to_imgbb(image_path_obj, imgbb_key)
    except Exception as e:
        return {
            "ok": False,
            "error": "Image upload failed",
            "detail": str(e)
        }

    # Step 2: Generate video using inference.sh CLI
    cmd = [
        "inference.sh",
        "video",
        "generate",
        "--model", model,
        "--prompt", prompt,
        "--image", image_url,
        "--duration", str(duration),
        "--output", str(save_dir),
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        timeout=timeout
    )

    if result.returncode != 0:
        error_msg = result.stderr or result.stdout or "Unknown error"
        return {
            "ok": False,
            "error": "Video generation failed",
            "detail": error_msg,
            "image_url": image_url
        }

    # Step 3: Parse output to find video file path
    output_lines = result.stdout.strip().split('\n')
    video_file = None

    for line in output_lines:
        line = line.strip()
        if line.endswith('.mp4') and Path(line).exists():
            video_file = Path(line)
            break

    # If no explicit path found, look in save_dir
    if video_file is None:
        video_files = list(save_dir.glob("*.mp4"))
        if video_files:
            # Get the most recently created file
            video_file = max(video_files, key=lambda p: p.stat().st_mtime)

    if video_file:
        return {
            "ok": True,
            "downloaded_files": [str(video_file.resolve())],
            "image_url": image_url
        }
    else:
        return {
            "ok": False,
            "error": "Video generation completed but output file not found",
            "stdout": result.stdout,
            "image_url": image_url
        }


def main() -> int:
    """Main entry point."""
    args = _build_parser().parse_args()
    _load_default_envs(args.env_file)

    save_dir = _resolve_save_dir(args.save_dir)

    result = generate_video_from_image(
        image_path=args.image,
        prompt=args.prompt,
        model=args.model,
        duration=args.duration,
        save_dir=save_dir,
        upload_service=args.upload_service,
        api_token=args.api_token,
        timeout=args.timeout,
        dry_run=args.dry_run
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
