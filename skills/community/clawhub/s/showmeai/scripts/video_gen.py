#!/usr/bin/env python3
"""
Showmeai Video Generation Script
- Generate videos via POST /task/volces/seedance
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path


def get_default_save_dir() -> Path:
    return Path.home() / ".openclaw" / "media"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:50] or "video"


def download_to_temp(url: str) -> Path:
    """Download remote image to a temp file for image-to-video."""
    import tempfile
    suffix = ".jpg" if ".jpg" in url.lower() else ".png"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        with open(tmp.name, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)
    return Path(tmp.name)


def request_video(
    base_url: str,
    api_key: str,
    prompt: str,
    model: str,
    image_path: str = "",
    first_frame_path: str = "",
    last_frame_path: str = "",
    generate_audio: bool = True,
    draft: bool = False,
    resolution: str = "",
    ratio: str = "",
    duration: int = 0,
    watermark: bool = False,
    camera_fixed: bool = False,
    seed: int = 0,
    frames: int = 0,
) -> dict:
    """POST /task/volces/seedance"""
    # Remove /v1 suffix if present for video API
    base = base_url.rstrip('/')
    if base.endswith('/v1'):
        base = base[:-3]
    url = f"{base}/task/volces/seedance"

    # Build content array
    content = [{"type": "text", "text": prompt}]

    # Add reference image (image-to-video)
    if image_path:
        if image_path.startswith("http"):
            content.append({
                "type": "image_url",
                "image_url": {"url": image_path}
            })
        else:
            # Read local image and convert to base64 data URL
            with open(image_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
                img_mime = "image/jpeg" if image_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{img_mime};base64,{img_data}"}
                })

    # Add first frame (first-and-last-frame video)
    if first_frame_path:
        if first_frame_path.startswith("http"):
            content.append({
                "type": "image_url",
                "image_url": {"url": first_frame_path},
                "role": "first_frame"
            })
        else:
            with open(first_frame_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
                img_mime = "image/jpeg" if first_frame_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{img_mime};base64,{img_data}"},
                    "role": "first_frame"
                })

    # Add last frame (first-and-last-frame video)
    if last_frame_path:
        if last_frame_path.startswith("http"):
            content.append({
                "type": "image_url",
                "image_url": {"url": last_frame_path},
                "role": "last_frame"
            })
        else:
            with open(last_frame_path, "rb") as f:
                img_data = base64.b64encode(f.read()).decode("utf-8")
                img_mime = "image/jpeg" if last_frame_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
                content.append({
                    "type": "image_url",
                    "image_url": {"url": f"data:{img_mime};base64,{img_data}"},
                    "role": "last_frame"
                })

    payload = {
        "model": model,
        "content": content,
        "generate_audio": generate_audio,
    }

    # Only add draft parameter for Seedance 1.5 pro
    if "1-5-pro" in model:
        payload["draft"] = draft

    # Add new direct parameters (recommended way)
    if resolution:
        payload["resolution"] = resolution
    if ratio:
        payload["ratio"] = ratio
    if duration > 0:
        payload["duration"] = duration
    if frames > 0:
        payload["frames"] = frames
    if watermark:
        payload["watermark"] = watermark
    if camera_fixed:
        payload["camera_fixed"] = camera_fixed
    if seed > 0:
        payload["seed"] = seed

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=body,
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Showmeai API error ({e.code}): {e.read().decode('utf-8', errors='replace')}") from e


def query_task(base_url: str, api_key: str, task_id: str) -> dict:
    """GET /task/{task_id} - Query task status"""
    # Remove /v1 suffix if present for video API
    base = base_url.rstrip('/')
    if base.endswith('/v1'):
        base = base[:-3]
    url = f"{base}/task/{task_id}"

    req = urllib.request.Request(
        url, method="GET",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Showmeai API error ({e.code}): {e.read().decode('utf-8', errors='replace')}") from e


def process_response(response: dict, out_dir: Path, prompt: str, filename: str) -> None:
    """Process API response and save video if available."""
    # The API returns a task response; actual video may come later via async
    # For now, output the response for the framework to handle
    print(json.dumps(response, ensure_ascii=False))

    # If response contains direct video URL/data, save it
    data = response.get("data", {})
    video_url = data.get("url") if isinstance(data, dict) else None
    video_b64 = data.get("b64_json") if isinstance(data, dict) else None

    if video_url:
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        fn = filename or f"{ts}-{slugify(prompt)}.mp4"
        fp = out_dir / fn
        urllib.request.urlretrieve(video_url, fp)
        print(f"Video saved: {fp.resolve()}", file=sys.stderr)
        print(f"MEDIA:{fp.resolve()}")
    elif video_b64:
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        fn = filename or f"{ts}-{slugify(prompt)}.mp4"
        fp = out_dir / fn
        fp.write_bytes(base64.b64decode(video_b64))
        print(f"Video saved: {fp.resolve()}", file=sys.stderr)
        print(f"MEDIA:{fp.resolve()}")
    else:
        # Task submitted - output task info
        task_id = response.get("id", "")
        if task_id:
            print(f"Task submitted: {task_id}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser(description="Generate videos via Showmeai Seedance API.")
    ap.add_argument("--prompt", default="", help="Video generation prompt.")
    ap.add_argument("--query", default="", help="Query task status by task ID.")
    ap.add_argument("--model", default="doubao-seedance-1-5-pro-251215",
                    help="Model name (default: doubao-seedance-1-5-pro-251215).")
    ap.add_argument("--image", default="", help="Reference image path or URL (image-to-video).")
    ap.add_argument("--first-frame", default="", help="First frame image path or URL.")
    ap.add_argument("--last-frame", default="", help="Last frame image path or URL.")
    ap.add_argument("--no-audio", action="store_true", help="Generate video without audio.")
    ap.add_argument("--draft", action="store_true",
                    help="Enable draft/preview mode (faster, lower quality, only for 1.5 pro).")
    ap.add_argument("--resolution", default="", choices=["480p", "720p", "1080p"],
                    help="Video resolution (default: 720p for 1.5 pro/lite, 1080p for 1.0 pro).")
    ap.add_argument("--ratio", default="",
                    choices=["16:9", "4:3", "1:1", "3:4", "9:16", "21:9", "adaptive"],
                    help="Aspect ratio (default: 16:9 for text-to-video, adaptive for image-to-video).")
    ap.add_argument("--duration", type=int, default=0,
                    help="Video duration in seconds (2-12, default: 5). Use 0 for auto (4-12, 1.5 pro only).")
    ap.add_argument("--frames", type=int, default=0,
                    help="Number of frames (alternative to duration).")
    ap.add_argument("--watermark", action="store_true", help="Add watermark to video.")
    ap.add_argument("--camera-fixed", action="store_true",
                    help="Keep camera fixed (no camera movement).")
    ap.add_argument("--seed", type=int, default=0,
                    help="Random seed for reproducible results.")
    ap.add_argument("--save", action="store_true", help="Save to ~/.openclaw/media/.")
    ap.add_argument("--out-dir", default="", help="Save to custom directory.")
    ap.add_argument("--filename", default="", help="Custom output filename.")
    args = ap.parse_args()

    api_key = os.environ.get("Showmeai_API_KEY", "").strip()
    base_url = os.environ.get("Showmeai_BASE_URL", "https://api.showmeai.art/v1").strip()
    if not api_key:
        print("Error: Showmeai_API_KEY not set.", file=sys.stderr)
        sys.exit(1)
    if not base_url:
        base_url = "https://api.showmeai.art/v1"

    # Query mode
    if args.query:
        try:
            response = query_task(base_url, api_key, args.query)
            print(json.dumps(response, ensure_ascii=False, indent=2))
            return
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Generate mode - validate prompt
    if not args.prompt:
        print("Error: --prompt is required for video generation.", file=sys.stderr)
        sys.exit(1)

    # Validate frame arguments
    if (args.first_frame and not args.last_frame) or (args.last_frame and not args.first_frame):
        print("Error: Both --first-frame and --last-frame are required for first-and-last-frame video.",
              file=sys.stderr)
        sys.exit(1)

    if args.image and (args.first_frame or args.last_frame):
        print("Error: Cannot use --image with --first-frame/--last-frame.", file=sys.stderr)
        sys.exit(1)

    # Validate duration and frames
    if args.duration < 0 or args.duration > 12:
        print("Error: --duration must be between 0 and 12 seconds (0 for auto, 1.5 pro only).", file=sys.stderr)
        sys.exit(1)
    if args.duration > 0 and args.duration < 2:
        print("Error: --duration must be at least 2 seconds when specified.", file=sys.stderr)
        sys.exit(1)
    if args.frames < 0:
        print("Error: --frames must be a positive integer.", file=sys.stderr)
        sys.exit(1)
    if args.duration > 0 and args.frames > 0:
        print("Warning: Both --duration and --frames specified; --frames takes precedence.", file=sys.stderr)

    out_dir = get_default_save_dir()
    if args.save:
        if args.out_dir:
            out_dir = Path(args.out_dir)
        else:
            out_dir = get_default_save_dir()
        out_dir.mkdir(parents=True, exist_ok=True)

    try:
        print(f"Generating video with model={args.model}...", file=sys.stderr)
        response = request_video(
            base_url=base_url,
            api_key=api_key,
            prompt=args.prompt,
            model=args.model,
            image_path=args.image,
            first_frame_path=args.first_frame,
            last_frame_path=args.last_frame,
            generate_audio=not args.no_audio,
            draft=args.draft,
            resolution=args.resolution,
            ratio=args.ratio,
            duration=args.duration,
            watermark=args.watermark,
            camera_fixed=args.camera_fixed,
            seed=args.seed,
            frames=args.frames,
        )

        process_response(response, out_dir, args.prompt, args.filename)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
