#!/usr/bin/env python3
"""
Seedance Video Generation CLI Tool (via SkillBoss API Hub)
Usage:
  python3 seedance.py create --prompt "描述" [options]
  python3 seedance.py create --prompt "描述" --image /path/to/image.png [options]
  python3 seedance.py create --prompt "描述" --image url1 --last-frame url2 [options]
  python3 seedance.py create --prompt "描述" --ref-images url1 url2 [options]
  python3 seedance.py create --draft-task-id <task_id> [options]
  python3 seedance.py status <task_id>
  python3 seedance.py wait <task_id> [--interval 15] [--download ~/Desktop]
  python3 seedance.py list [--status succeeded] [--page 1] [--page-size 10]
  python3 seedance.py delete <task_id>
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path


PILOT_URL = "https://api.heybossai.com/v1/pilot"
DEFAULT_MODEL = "doubao-seedance-1-5-pro-251215"


def get_api_key():
    key = os.environ.get("SKILLBOSS_API_KEY")
    if not key:
        print("Error: SKILLBOSS_API_KEY environment variable is not set.", file=sys.stderr)
        print("Set it with: export SKILLBOSS_API_KEY='your-api-key-here'", file=sys.stderr)
        sys.exit(1)
    return key


def pilot_request(body: dict) -> dict:
    """Call SkillBoss API Hub /v1/pilot and return parsed JSON response."""
    api_key = get_api_key()
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(PILOT_URL, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            resp_body = resp.read().decode("utf-8")
            if resp_body:
                return json.loads(resp_body)
            return {}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("error", {}).get("message", error_body)
        except json.JSONDecodeError:
            error_msg = error_body
        print(f"API Error (HTTP {e.code}): {error_msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def image_to_data_url(image_path):
    """Convert a local image file to a base64 data URL."""
    p = Path(image_path)
    if not p.exists():
        print(f"Error: Image file not found: {image_path}", file=sys.stderr)
        sys.exit(1)

    ext = p.suffix.lower().lstrip(".")
    mime_map = {
        "jpg": "jpeg", "jpeg": "jpeg", "png": "png",
        "webp": "webp", "bmp": "bmp", "tiff": "tiff",
        "tif": "tiff", "gif": "gif", "heic": "heic", "heif": "heif",
    }
    mime_ext = mime_map.get(ext, ext)

    file_size = p.stat().st_size
    if file_size > 30 * 1024 * 1024:
        print(f"Error: Image file too large ({file_size / 1024 / 1024:.1f} MB). Max 30 MB.", file=sys.stderr)
        sys.exit(1)

    with open(p, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")

    return f"data:image/{mime_ext};base64,{b64}"


def resolve_image(image_input):
    """Resolve image input to a URL or data URL. Accepts URL or local file path."""
    if image_input.startswith(("http://", "https://", "data:")):
        return image_input
    return image_to_data_url(image_input)


def cmd_create(args):
    """Create a video generation task via SkillBoss API Hub."""
    inputs = {}

    # Draft task mode
    if args.draft_task_id:
        inputs["draft_task_id"] = args.draft_task_id
    else:
        # Text prompt
        if args.prompt:
            inputs["prompt"] = args.prompt

        # Image inputs
        if args.ref_images:
            # Reference image mode (Lite I2V only)
            inputs["ref_images"] = [resolve_image(img) for img in args.ref_images]
        elif args.image:
            # First frame
            inputs["image"] = resolve_image(args.image)
            # Last frame (optional)
            if args.last_frame:
                inputs["last_frame"] = resolve_image(args.last_frame)

    if not inputs:
        print("Error: Must provide --prompt, --image, or --draft-task-id.", file=sys.stderr)
        sys.exit(1)

    # Optional parameters
    if args.ratio:
        inputs["ratio"] = args.ratio
    if args.duration is not None:
        inputs["duration"] = args.duration
    if args.resolution:
        inputs["resolution"] = args.resolution
    if args.seed is not None:
        inputs["seed"] = args.seed
    if args.camera_fixed is not None:
        inputs["camera_fixed"] = args.camera_fixed
    if args.watermark is not None:
        inputs["watermark"] = args.watermark
    if args.generate_audio is not None:
        inputs["generate_audio"] = args.generate_audio
    if args.draft is not None:
        inputs["draft"] = args.draft
    if args.return_last_frame is not None:
        inputs["return_last_frame"] = args.return_last_frame
    if args.service_tier:
        inputs["service_tier"] = args.service_tier

    body = {
        "type": "video",
        "inputs": inputs,
        "prefer": "balanced",
    }

    result = pilot_request(body)
    video_url = result.get("result", {}).get("video_url", "")
    last_frame_url = result.get("result", {}).get("last_frame_url")

    print(f"\nVideo generation succeeded!")
    print(f"  Video URL: {video_url}")
    if last_frame_url:
        print(f"  Last Frame URL: {last_frame_url}")

    print(json.dumps({"video_url": video_url, "response": result}, indent=2, ensure_ascii=False))

    # Download if requested
    if args.download and video_url:
        _download_video(video_url, args.download, f"result_{int(time.time())}")

    return result


def _download_video(video_url, download_dir, task_id):
    """Download video to local directory."""
    if not download_dir or not video_url:
        return

    download_path = Path(download_dir).expanduser()
    download_path.mkdir(parents=True, exist_ok=True)
    filename = f"seedance_{task_id}.mp4"
    filepath = download_path / filename

    print(f"\nDownloading video to {filepath}...")
    try:
        urllib.request.urlretrieve(video_url, str(filepath))
        print(f"Saved to: {filepath}")

        # Open on macOS
        if sys.platform == "darwin":
            os.system(f'open "{filepath}"')
    except Exception as e:
        print(f"Download failed: {e}", file=sys.stderr)


def cmd_status(args):
    """Query task status. SkillBoss API Hub processes video synchronously; no async task ID is returned."""
    print(f"Note: SkillBoss API Hub /v1/pilot processes video generation directly.", file=sys.stderr)
    print(f"Task ID '{args.task_id}': async task management is not applicable.", file=sys.stderr)
    print(json.dumps({"task_id": args.task_id, "message": "Re-run create to generate a new video."}, indent=2))


def cmd_wait_logic(task_id, interval=15, download_dir=None):
    """No-op: SkillBoss API Hub returns the video URL synchronously in cmd_create."""
    print(f"Note: Video generation completed synchronously. No additional waiting needed.", file=sys.stderr)


def cmd_wait(args):
    """Wait for task completion."""
    return cmd_wait_logic(args.task_id, args.interval, args.download)


def cmd_list(args):
    """List video generation tasks."""
    print("Note: Task listing is not supported via SkillBoss API Hub /v1/pilot.", file=sys.stderr)
    print(json.dumps({"message": "Use SkillBoss API Hub dashboard to manage tasks."}, indent=2))


def cmd_delete(args):
    """Cancel or delete a task."""
    print(f"Note: Task cancellation is not supported via SkillBoss API Hub /v1/pilot.", file=sys.stderr)
    print(f"Task '{args.task_id}': manage via SkillBoss API Hub dashboard.")


def parse_bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ("true", "1", "yes"):
        return True
    if v.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"Boolean expected, got '{v}'")


def main():
    parser = argparse.ArgumentParser(description="Seedance Video Generation CLI (via SkillBoss API Hub)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create
    p_create = subparsers.add_parser("create", help="Create a video generation task")
    p_create.add_argument("--prompt", "-p", help="Text prompt describing the video")
    p_create.add_argument("--image", "-i", help="First frame image (URL or local file path)")
    p_create.add_argument("--last-frame", help="Last frame image (URL or local file path)")
    p_create.add_argument("--ref-images", nargs="+", help="Reference images for Lite I2V (1-4 URLs or paths)")
    p_create.add_argument("--draft-task-id", help="Draft task ID to generate final video from")
    p_create.add_argument("--model", "-m", default=DEFAULT_MODEL, help=f"Model hint (default: {DEFAULT_MODEL})")
    p_create.add_argument("--ratio", choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"], help="Aspect ratio")
    p_create.add_argument("--duration", "-d", type=int, help="Duration in seconds (4-12 for 1.5 Pro)")
    p_create.add_argument("--resolution", "-r", choices=["480p", "720p", "1080p"], help="Resolution")
    p_create.add_argument("--seed", type=int, help="Random seed (-1 for random)")
    p_create.add_argument("--camera-fixed", type=parse_bool, help="Fix camera position (true/false)")
    p_create.add_argument("--watermark", type=parse_bool, help="Add watermark (true/false)")
    p_create.add_argument("--generate-audio", type=parse_bool, help="Generate audio (true/false, 1.5 Pro only)")
    p_create.add_argument("--draft", type=parse_bool, help="Draft/preview mode (true/false, 1.5 Pro only)")
    p_create.add_argument("--return-last-frame", type=parse_bool, help="Return last frame URL (true/false)")
    p_create.add_argument("--service-tier", choices=["default", "flex"], help="Service tier")
    p_create.add_argument("--wait", "-w", action="store_true", help="(No-op) Kept for compatibility; generation is synchronous")
    p_create.add_argument("--interval", type=int, default=15, help="Poll interval in seconds (default: 15, unused)")
    p_create.add_argument("--download", help="Download directory (e.g. ~/Desktop)")

    # status
    p_status = subparsers.add_parser("status", help="Query task status")
    p_status.add_argument("task_id", help="Task ID to query")

    # wait
    p_wait = subparsers.add_parser("wait", help="Wait for task completion")
    p_wait.add_argument("task_id", help="Task ID to wait for")
    p_wait.add_argument("--interval", type=int, default=15, help="Poll interval in seconds (default: 15)")
    p_wait.add_argument("--download", help="Download directory (e.g. ~/Desktop)")

    # list
    p_list = subparsers.add_parser("list", help="List video generation tasks")
    p_list.add_argument("--status", choices=["queued", "running", "cancelled", "succeeded", "failed", "expired"])
    p_list.add_argument("--page", type=int, default=1)
    p_list.add_argument("--page-size", type=int, default=10)

    # delete
    p_delete = subparsers.add_parser("delete", help="Cancel or delete a task")
    p_delete.add_argument("task_id", help="Task ID to cancel/delete")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    commands = {
        "create": cmd_create,
        "status": cmd_status,
        "wait": cmd_wait,
        "list": cmd_list,
        "delete": cmd_delete,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
