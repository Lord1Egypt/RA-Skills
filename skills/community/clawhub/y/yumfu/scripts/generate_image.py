#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
# YumFu武侠游戏图片生成脚本（无自动发送）
# 基于 Gemini 3 Pro Image API
#
# 特点：
# - 不输出 MEDIA: 标记
# - 由游戏引擎控制发送时机
# - 专为水墨武侠风格设计
#
"""
Generate images using Google's Nano Banana Pro (Gemini 3 Pro Image) API.

Usage:
    uv run generate_image.py --prompt "your image description" --filename "output.png" [--resolution 1K|2K|4K] [--api-key KEY]

Multi-image editing (up to 14 images):
    uv run generate_image.py --prompt "combine these images" --filename "output.png" -i img1.png -i img2.png -i img3.png
"""

import argparse
import os
import sys
from pathlib import Path

LOGO_PATH = Path.home() / 'clawd' / 'skills' / 'yumfu' / 'assets' / 'yumfu-logo.png'

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


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")


def auto_detect_resolution(max_input_dim: int) -> str:
    """Infer output resolution from the largest input image dimension."""
    if max_input_dim >= 3000:
        return "4K"
    if max_input_dim >= 1500:
        return "2K"
    return "1K"


def choose_output_resolution(
    requested_resolution: str | None,
    max_input_dim: int,
    has_input_images: bool,
) -> tuple[str, bool]:
    """Choose final resolution and whether it was auto-detected.

    Auto-detection is only applied when the user did not pass --resolution.
    """
    if requested_resolution is not None:
        return requested_resolution, False

    if has_input_images and max_input_dim > 0:
        return auto_detect_resolution(max_input_dim), True

    return "1K", False


TEXT_AVOIDANCE_SUFFIX = (
    " No text, no words, no letters, no captions, no signs, no speech bubbles, "
    "no book pages, no paragraph blocks, no watermark, no logo, no typographic elements, "
    "image-only illustration."
)


def normalize_prompt(prompt: str) -> str:
    prompt = prompt.strip()
    lower = prompt.lower()
    if "no text" in lower or "no words" in lower or "no letters" in lower:
        return prompt
    return prompt + TEXT_AVOIDANCE_SUFFIX


def overlay_yumfu_logo(image, output_path, pil_image_module):
    if not LOGO_PATH.exists():
        image.save(str(output_path), 'PNG')
        return False

    base = image.convert('RGBA')
    logo = pil_image_module.open(LOGO_PATH).convert('RGBA')

    max_logo_w = max(120, base.width // 5)
    scale = min(1.0, max_logo_w / max(1, logo.width))
    new_size = (max(1, int(logo.width * scale)), max(1, int(logo.height * scale)))
    logo = logo.resize(new_size)

    margin = max(18, base.width // 40)
    x = max(0, base.width - logo.width - margin)
    y = max(0, base.height - logo.height - margin)

    composed = pil_image_module.new('RGBA', base.size, (255, 255, 255, 0))
    composed.alpha_composite(base)
    composed.alpha_composite(logo, (x, y))
    composed.convert('RGB').save(str(output_path), 'PNG')
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Nano Banana Pro (Gemini 3 Pro Image)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., sunset-mountains.png)"
    )
    parser.add_argument(
        "--input-image", "-i",
        action="append",
        dest="input_images",
        metavar="IMAGE",
        help="Input image path(s) for editing/composition. Can be specified multiple times (up to 14 images)."
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default=None,
        help="Output resolution: 1K, 2K, or 4K. If omitted with input images, auto-detect from largest image dimension."
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        choices=SUPPORTED_ASPECT_RATIOS,
        default=None,
        help=f"Output aspect ratio (default: model decides). Options: {', '.join(SUPPORTED_ASPECT_RATIOS)}"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key (overrides GEMINI_API_KEY / GOOGLE_API_KEY env var)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Import here after checking API key to avoid slow import on error
    # IMPORTANT: this script is intended to be run via `uv run .../generate_image.py`
    # so the inline dependencies declared in the script header are available.
    try:
        from google import genai
        from google.genai import types
        from PIL import Image as PILImage
    except ImportError as e:
        print("Error: required image-generation dependencies are not available in this Python runtime.", file=sys.stderr)
        print("Run this script with `uv run ~/clawd/skills/yumfu/scripts/generate_image.py ...` so inline dependencies are installed automatically.", file=sys.stderr)
        print(f"Import detail: {e}", file=sys.stderr)
        sys.exit(1)

    # Initialise client
    client = genai.Client(api_key=api_key)

    # Set up output path
    output_path = Path(args.filename).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input images if provided (up to 14 supported by Nano Banana Pro)
    input_images = []
    max_input_dim = 0
    if args.input_images:
        if len(args.input_images) > 14:
            print(f"Error: Too many input images ({len(args.input_images)}). Maximum is 14.", file=sys.stderr)
            sys.exit(1)

        for img_path in args.input_images:
            try:
                with PILImage.open(img_path) as img:
                    copied = img.copy()
                    width, height = copied.size
                input_images.append(copied)
                print(f"Loaded input image: {img_path}")

                # Track largest dimension for auto-resolution
                max_input_dim = max(max_input_dim, width, height)
            except Exception as e:
                print(f"Error loading input image '{img_path}': {e}", file=sys.stderr)
                sys.exit(1)

    output_resolution, auto_detected = choose_output_resolution(
        requested_resolution=args.resolution,
        max_input_dim=max_input_dim,
        has_input_images=bool(input_images),
    )
    if auto_detected:
        print(
            f"Auto-detected resolution: {output_resolution} "
            f"(from max input dimension {max_input_dim})"
        )

    normalized_prompt = normalize_prompt(args.prompt)

    # Build contents (images first if editing, prompt only if generating)
    if input_images:
        contents = [*input_images, normalized_prompt]
        img_count = len(input_images)
        print(f"Processing {img_count} image{'s' if img_count > 1 else ''} with resolution {output_resolution}...")
    else:
        contents = normalized_prompt
        print(f"Generating image with resolution {output_resolution}...")

    try:
        # Build image config with optional aspect ratio
        image_cfg_kwargs = {"image_size": output_resolution}
        if args.aspect_ratio:
            image_cfg_kwargs["aspect_ratio"] = args.aspect_ratio

        response = client.models.generate_content(
            model="gemini-3-pro-image-preview",
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                image_config=types.ImageConfig(**image_cfg_kwargs)
            )
        )

        # Process response and convert to PNG
        image_saved = False
        for part in response.parts:
            if part.text is not None:
                print(f"Model response: {part.text}")
            elif part.inline_data is not None:
                # Convert inline data to PIL Image and save as PNG
                from io import BytesIO

                # inline_data.data is already bytes, not base64
                image_data = part.inline_data.data
                if isinstance(image_data, str):
                    # If it's a string, it might be base64
                    import base64
                    image_data = base64.b64decode(image_data)

                image = PILImage.open(BytesIO(image_data))

                # Ensure PNG output and apply YumFu logo overlay in the final image corner
                if image.mode not in ('RGBA', 'RGB'):
                    image = image.convert('RGBA')
                logo_applied = overlay_yumfu_logo(image, output_path, PILImage)
                if logo_applied:
                    print(f"Applied YumFu logo overlay: {LOGO_PATH}")
                else:
                    print("YumFu logo overlay skipped: logo asset missing")
                image_saved = True

        if image_saved:
            full_path = output_path.resolve()
            print(f"\nImage saved: {full_path}")
            # YumFu: Do NOT emit MEDIA: token - game engine will handle sending
            # print(f"MEDIA:{full_path}")
        else:
            print("Error: No image was generated in the response.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
