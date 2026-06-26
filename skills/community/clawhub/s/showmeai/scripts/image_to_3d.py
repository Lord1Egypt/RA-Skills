#!/usr/bin/env python3
"""
Showmeai Image-to-3D Conversion Script
- Convert 2D images to 3D models via POST /task/gi/image-to-3d
- Query task status via GET /task/{task_id}
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
    return text[:50] or "3d-model"


def request_image_to_3d(
    base_url: str,
    api_key: str,
    image_path: str,
    model: str,
    texture: bool = False,
    num_inference_steps: int = 5,
    octree_resolution: int = 128,
    guidance_scale: float = 5.0,
    file_format: str = "glb",
    seed: int = 1234,
) -> dict:
    """POST /task/gi/image-to-3d with multipart/form-data"""
    # Remove /v1 suffix if present for 3D API
    base = base_url.rstrip('/')
    if base.endswith('/v1'):
        base = base[:-3]
    url = f"{base}/task/gi/image-to-3d"

    # Build multipart form data manually
    boundary = "----Showmeai3DBoundary" + os.urandom(8).hex()
    parts = []

    def field(name: str, value: str) -> bytes:
        return (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n"
        ).encode("utf-8")

    parts.append(field("model", model))
    parts.append(field("texture", str(texture).lower()))
    parts.append(field("num_inference_steps", str(num_inference_steps)))
    parts.append(field("octree_resolution", str(octree_resolution)))
    parts.append(field("guidance_scale", str(guidance_scale)))
    parts.append(field("seed", str(seed)))

    # Format parameter: file_format for most models, type for Hunyuan3D-2
    if "Hunyuan3D-2" in model:
        parts.append(field("type", file_format))
    else:
        parts.append(field("file_format", file_format))

    # Image file
    with open(image_path, "rb") as f:
        img_data = f.read()
    img_mime = "image/png" if image_path.lower().endswith(".png") else "image/jpeg"
    parts.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="image"; filename="{Path(image_path).name}"\r\n'
            f"Content-Type: {img_mime}\r\n\r\n"
        ).encode("utf-8")
        + img_data
        + b"\r\n"
    )

    parts.append(f"--{boundary}--\r\n".encode("utf-8"))
    body = b"".join(parts)

    req = urllib.request.Request(
        url, method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        data=body,
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"Showmeai API error ({e.code}): {e.read().decode('utf-8', errors='replace')}") from e


def query_task(base_url: str, api_key: str, task_id: str) -> dict:
    """GET /task/{task_id} - Query task status"""
    # Remove /v1 suffix if present for 3D API
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


def download_3d_model(url: str, output_path: Path) -> None:
    """Download 3D model file from URL."""
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=300) as resp:
        with open(output_path, "wb") as f:
            while True:
                chunk = resp.read(65536)
                if not chunk:
                    break
                f.write(chunk)


def main():
    ap = argparse.ArgumentParser(description="Convert 2D images to 3D models via Showmeai API.")
    ap.add_argument("--image", required=True, help="Path to input image (PNG with transparent background recommended).")
    ap.add_argument("--model", default="Hunyuan3D-2",
                    choices=["Hunyuan3D-2", "Hi3DGen", "Step1X-3D"],
                    help="3D model to use (default: Hunyuan3D-2).")
    ap.add_argument("--format", default="glb", choices=["glb", "stl"],
                    help="Output format (default: glb).")
    ap.add_argument("--texture", action="store_true", help="Generate texture.")
    ap.add_argument("--steps", type=int, default=5, help="Number of inference steps (2-50, default: 5).")
    ap.add_argument("--resolution", type=int, default=128, help="Octree resolution (16-400, default: 128).")
    ap.add_argument("--guidance", type=float, default=5.0, help="Guidance scale (1-20, default: 5.0).")
    ap.add_argument("--seed", type=int, default=1234, help="Random seed (default: 1234).")
    ap.add_argument("--query", default="", help="Query task status by task ID.")
    ap.add_argument("--save", action="store_true", help="Download and save the 3D model when complete.")
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

            # If save flag is set and task is complete, download the model
            if args.save and response.get("status") == "success":
                file_url = response.get("output", {}).get("file_url")
                if file_url:
                    out_dir = Path(args.out_dir) if args.out_dir else get_default_save_dir()
                    out_dir.mkdir(parents=True, exist_ok=True)
                    filename = args.filename or f"{args.query}.{args.format}"
                    output_path = out_dir / filename
                    print(f"\nDownloading 3D model...", file=sys.stderr)
                    download_3d_model(file_url, output_path)
                    print(f"3D model saved: {output_path.resolve()}", file=sys.stderr)
            elif args.save and response.get("status") not in ["success", "completed"]:
                print(f"\nTask not complete yet. Status: {response.get('status')}", file=sys.stderr)
            return
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

    # Convert mode - validate image path
    if not os.path.exists(args.image):
        print(f"Error: Image file not found: {args.image}", file=sys.stderr)
        sys.exit(1)

    # Validate parameters
    if not 2 <= args.steps <= 50:
        print("Error: --steps must be between 2 and 50.", file=sys.stderr)
        sys.exit(1)
    if not 16 <= args.resolution <= 400:
        print("Error: --resolution must be between 16 and 400.", file=sys.stderr)
        sys.exit(1)
    if not 1.0 <= args.guidance <= 20.0:
        print("Error: --guidance must be between 1 and 20.", file=sys.stderr)
        sys.exit(1)

    try:
        print(f"Converting image to 3D model with {args.model}...", file=sys.stderr)
        print(f"Image: {args.image}", file=sys.stderr)
        print(f"Format: {args.format}, Texture: {args.texture}, Steps: {args.steps}", file=sys.stderr)

        response = request_image_to_3d(
            base_url=base_url,
            api_key=api_key,
            image_path=args.image,
            model=args.model,
            texture=args.texture,
            num_inference_steps=args.steps,
            octree_resolution=args.resolution,
            guidance_scale=args.guidance,
            file_format=args.format,
            seed=args.seed,
        )

        # Output response
        print(json.dumps(response, ensure_ascii=False, indent=2))

        # Show task ID for querying
        task_id = response.get("task_id", "")
        if task_id:
            print(f"\nTask submitted. Query status with:", file=sys.stderr)
            print(f"python3 {sys.argv[0]} --query {task_id}", file=sys.stderr)
            if args.save:
                print(f"\nTo download when complete:", file=sys.stderr)
                print(f"python3 {sys.argv[0]} --query {task_id} --save", file=sys.stderr)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
