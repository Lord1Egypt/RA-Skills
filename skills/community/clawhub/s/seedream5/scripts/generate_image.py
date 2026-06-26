#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.28.0",
#     "pillow>=10.0.0",
# ]
# ///
"""
Generate images using Volcano Engine Seedream 5.0 API (豆包 doubao-seedream-5-0-260128).

API: POST https://ark.cn-beijing.volces.com/api/v3/images/generations

Usage:
    uv run generate_image.py --prompt "your image description" --filename "output.png" [--resolution 2K|3K] [--api-key KEY]

Multi-image editing (up to 14 images):
    uv run generate_image.py --prompt "combine these images" --filename "output.png" -i img1.png -i img2.png -i img3.png
"""

import argparse
import base64
import os
import sys
from io import BytesIO
from pathlib import Path

import requests

API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
MODEL = "doubao-seedream-5-0-260128"

SUPPORTED_ASPECT_RATIOS = [
    "1:1",
    "2:3",
    "3:2",
    "3:4",
    "4:3",
    "4:5",
    "5:4",
    "9:16",
    "16:9",
    "21:9",
]

# doubao-seedream-5.0-lite: 2K/3K resolution, aspect ratio -> pixel size
SIZE_2K = {
    "1:1": "2048x2048",
    "4:3": "2304x1728",
    "3:4": "1728x2304",
    "16:9": "2848x1600",
    "9:16": "1600x2848",
    "3:2": "2496x1664",
    "2:3": "1664x2496",
    "21:9": "3136x1344",
}
SIZE_3K = {
    "1:1": "3072x3072",
    "4:3": "3456x2592",
    "3:4": "2592x3456",
    "16:9": "4096x2304",
    "9:16": "2304x4096",
    "2:3": "2496x3744",
    "3:2": "3744x2496",
    "21:9": "4704x2016",
}


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("VOLC_API_KEY") or os.environ.get("ARK_API_KEY")


def auto_detect_resolution(max_input_dim: int) -> str:
    """Infer output resolution from the largest input image dimension."""
    if max_input_dim >= 2500:
        return "3K"
    return "2K"


def choose_size(
    resolution: str,
    aspect_ratio: str | None,
) -> str:
    """Choose size parameter: 2K/3K or specific pixels."""
    res_map = {"2K": SIZE_2K, "3K": SIZE_3K}
    if aspect_ratio and resolution in res_map and aspect_ratio in res_map[resolution]:
        return res_map[resolution][aspect_ratio]
    return resolution


def image_to_base64(path: str) -> str:
    """Load image and return data URI."""
    from PIL import Image as PILImage

    with PILImage.open(path) as img:
        # Convert to RGB if necessary
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        buf = BytesIO()
        fmt = "PNG" if img.mode == "RGBA" else "JPEG"
        img.save(buf, format=fmt, quality=95)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    mime = "image/png" if fmt == "PNG" else "image/jpeg"
    return f"data:{mime};base64,{b64}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Volcano Engine Seedream 5.0 lite (豆包)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt (支持中英文)",
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., sunset-mountains.png)",
    )
    parser.add_argument(
        "--input-image", "-i",
        action="append",
        dest="input_images",
        metavar="IMAGE",
        help="Input image: local path or URL (http(s)://). Up to 14 images.",
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["2K", "3K"],
        default="2K",
        help="Output resolution: 2K or 3K (Seedream 5.0 lite). Default: 2K",
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        choices=SUPPORTED_ASPECT_RATIOS,
        default=None,
        help=f"Output aspect ratio. Options: {', '.join(SUPPORTED_ASPECT_RATIOS)}",
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Volcano Engine API key (overrides VOLC_API_KEY/ARK_API_KEY env)",
    )
    parser.add_argument(
        "--no-watermark",
        action="store_true",
        help="Do not add AI watermark to output",
    )
    parser.add_argument(
        "--model", "-m",
        default=MODEL,
        help=f"Model ID or Endpoint ID (default: {MODEL})",
    )
    parser.add_argument(
        "--sequential",
        choices=["disabled", "auto"],
        default="disabled",
        help="Group image mode: disabled=single image, auto=generate multiple related images",
    )
    parser.add_argument(
        "--max-images",
        type=int,
        default=15,
        metavar="N",
        help="Max images when sequential=auto (1-15). Default: 15",
    )
    parser.add_argument(
        "--web-search",
        action="store_true",
        help="Enable web search tool (e.g. for weather, real-time info)",
    )

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set VOLC_API_KEY or ARK_API_KEY environment variable", file=sys.stderr)
        print("  3. Set skills.entries.seedream5.apiKey in openclaw.json", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input images: URL or local file -> URL or base64 (up to 14)
    input_images_data = []
    max_input_dim = 0
    if args.input_images:
        if len(args.input_images) > 14:
            print(f"Error: Too many input images ({len(args.input_images)}). Maximum is 14.", file=sys.stderr)
            sys.exit(1)
        for img_spec in args.input_images:
            try:
                if img_spec.startswith(("http://", "https://")):
                    input_images_data.append(img_spec)
                    print(f"Using image URL: {img_spec}")
                else:
                    from PIL import Image as PILImage

                    with PILImage.open(img_spec) as img:
                        width, height = img.size
                        max_input_dim = max(max_input_dim, width, height)
                    input_images_data.append(image_to_base64(img_spec))
                    print(f"Loaded input image: {img_spec}")
            except Exception as e:
                print(f"Error loading input image '{img_spec}': {e}", file=sys.stderr)
                sys.exit(1)

    # Auto-detect resolution from input if not specified and we have inputs
    resolution = args.resolution
    if args.input_images and max_input_dim >= 2500 and args.resolution == "2K":
        resolution = "3K"
        print(f"Auto-detected resolution: 3K (from max input dimension {max_input_dim})")

    size = choose_size(resolution, args.aspect_ratio)
    img_count = len(input_images_data)
    if img_count > 0:
        print(f"Processing {img_count} image{'s' if img_count > 1 else ''} with size {size}...")
    else:
        print(f"Generating image with size {size}...")

    body = {
        "model": args.model,
        "prompt": args.prompt,
        "size": size,
        "sequential_image_generation": args.sequential,
        "response_format": "b64_json",
        "output_format": "png" if str(output_path).lower().endswith(".png") else "jpeg",
        "watermark": not args.no_watermark,
    }
    if input_images_data:
        body["image"] = input_images_data[0] if len(input_images_data) == 1 else input_images_data
    if args.sequential == "auto":
        body["sequential_image_generation_options"] = {"max_images": min(args.max_images, 15)}
    if args.web_search:
        body["tools"] = [{"type": "web_search"}]

    try:
        resp = requests.post(
            f"{API_BASE}/images/generations",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            json=body,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.exceptions.RequestException as e:
        err_detail = ""
        if hasattr(e, "response") and e.response is not None:
            try:
                err_detail = e.response.json()
            except Exception:
                err_detail = e.response.text[:500]
        print(f"Error calling API: {e}", file=sys.stderr)
        if err_detail:
            print(f"Response: {err_detail}", file=sys.stderr)
        sys.exit(1)

    if "error" in data:
        print(f"API error: {data['error']}", file=sys.stderr)
        sys.exit(1)

    result_data = data.get("data", [])
    if not result_data:
        print("Error: No image in response.", file=sys.stderr)
        sys.exit(1)

    saved_paths = []
    stem = output_path.stem
    suffix = output_path.suffix
    parent = output_path.parent

    for idx, item in enumerate(result_data):
        if "error" in item:
            print(f"Image {idx + 1} failed: {item['error']}", file=sys.stderr)
            continue
        b64_data = item.get("b64_json")
        if not b64_data:
            url = item.get("url")
            if url:
                print(f"Image {idx + 1} URL (not saved): {url}", file=sys.stderr)
            continue
        img_bytes = base64.b64decode(b64_data)
        if len(result_data) == 1:
            out_file = output_path
        else:
            out_file = parent / f"{stem}_{idx + 1}{suffix}"
        out_file.write_bytes(img_bytes)
        full_path = out_file.resolve()
        saved_paths.append(full_path)
        print(f"Image saved: {full_path}")
        print(f"MEDIA:{full_path}")
    if not saved_paths:
        sys.exit(1)


if __name__ == "__main__":
    main()
