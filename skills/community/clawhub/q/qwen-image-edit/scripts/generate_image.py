#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///
"""
Generate or edit images using Qwen Image API (Alibaba Cloud DashScope).

Usage:
    # Text-to-image
    python generate_image.py --prompt "your image description" --filename "output.png"

    # Single image editing
    python generate_image.py --images input.png --prompt "add a cat on the sofa" --filename output.png

    # Multi-image fusion
    python generate_image.py --images bg.png style.png --prompt "apply style from second image to first" --filename output.png
"""

import argparse
import base64
import mimetypes
import os
import sys
import json
from pathlib import Path


def get_api_key(provided_key: str | None) -> str | None:
    """Get API key from argument first, then environment."""
    return provided_key or os.getenv("DASHSCOPE_API_KEY")


def encode_image_to_base64(image_path: str) -> str:
    """Read a local image file and return a data URI with Base64 encoding."""
    path = Path(image_path)
    if not path.exists():
        print(f"Error: Image file not found: {image_path}", file=sys.stderr)
        sys.exit(1)
    if path.stat().st_size > 10 * 1024 * 1024:
        print(f"Error: Image file exceeds 10MB limit: {image_path}", file=sys.stderr)
        sys.exit(1)

    mime_type, _ = mimetypes.guess_type(str(path))
    if not mime_type or not mime_type.startswith("image/"):
        print(f"Error: Unsupported image format: {image_path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def resolve_image(image_ref: str) -> str:
    """Return the image as a URL string or Base64 data URI if it's a local file."""
    if image_ref.startswith(("http://", "https://", "oss://", "data:")):
        return image_ref
    return encode_image_to_base64(image_ref)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Qwen Image API"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description / editing instruction"
    )
    parser.add_argument(
        "--images", "-i",
        nargs="+",
        help="Input image(s) for editing: 1-3 local file paths or URLs"
    )
    parser.add_argument(
        "--filename", "-f",
        help="Output filename (optional, if not provided will only return URL)"
    )
    ALL_MODELS = [
        "qwen-image-2.0-pro", "qwen-image-2.0",
        "qwen-image-edit-max", "qwen-image-edit-plus", "qwen-image-edit",
    ]
    parser.add_argument(
        "--model", "-m",
        choices=ALL_MODELS,
        default="qwen-image-2.0-pro",
        help="Model (default: qwen-image-2.0-pro). Edit models: qwen-image-edit-max, qwen-image-edit-plus, qwen-image-edit"
    )
    parser.add_argument(
        "--size", "-s",
        default=None,
        help="Output resolution WxH, e.g. 2048*2048. Omit to auto-match input image ratio"
    )
    parser.add_argument(
        "--negative-prompt", "-n",
        default="低分辨率，低画质，肢体畸形，手指畸形，画面过饱和，蜡像感，人脸无细节，过度光滑，画面具有AI感。构图混乱。文字模糊，扭曲。",
        help="Negative prompt to avoid unwanted elements"
    )
    parser.add_argument(
        "--no-prompt-extend",
        action="store_true",
        help="Disable automatic prompt enhancement"
    )
    parser.add_argument(
        "--watermark",
        action="store_true",
        help="Add watermark to generated image"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed [0, 2147483647] for reproducible results"
    )
    parser.add_argument(
        "--n",
        type=int,
        default=1,
        choices=range(1, 7),
        help="Number of images to generate (1-6, default: 1)"
    )
    parser.add_argument(
        "--region",
        choices=["beijing", "singapore"],
        default="beijing",
        help="API region: beijing (default) or singapore"
    )
    parser.add_argument(
        "--workspace-id",
        help="Workspace ID (required for singapore region)"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="DashScope API key (overrides DASHSCOPE_API_KEY env var)"
    )
    parser.add_argument(
        "--no-verify-ssl",
        action="store_true",
        help="Disable SSL certificate verification (use with caution)"
    )

    args = parser.parse_args()

    # Get API key
    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Provide --api-key argument", file=sys.stderr)
        print("  2. Set DASHSCOPE_API_KEY environment variable", file=sys.stderr)
        sys.exit(1)

    # Import here after checking API key
    import requests

    # Resolve API endpoint based on region
    if args.region == "singapore":
        if not args.workspace_id:
            print("Error: --workspace-id is required for singapore region", file=sys.stderr)
            sys.exit(1)
        api_url = f"https://{args.workspace_id}.ap-southeast-1.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"
    else:
        api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation"

    # Validate images
    if args.images and len(args.images) > 3:
        print("Error: Maximum 3 input images supported", file=sys.stderr)
        sys.exit(1)

    is_edit_mode = args.images is not None

    # Build content array: images first, then text
    content = []
    if is_edit_mode:
        for img_ref in args.images:
            content.append({"image": resolve_image(img_ref)})
    content.append({"text": args.prompt})

    # Build parameters — qwen-image-edit does not support size/prompt_extend
    parameters = {"negative_prompt": args.negative_prompt, "watermark": args.watermark}
    if args.model != "qwen-image-edit":
        parameters["prompt_extend"] = not args.no_prompt_extend
        if args.size:
            parameters["size"] = args.size
    if args.n != 1:
        parameters["n"] = args.n
    if args.seed is not None:
        parameters["seed"] = args.seed

    payload = {
        "model": args.model,
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": content
                }
            ]
        },
        "parameters": parameters
    }

    mode = "Editing" if is_edit_mode else "Generating"
    print(f"{mode} image with {args.model}...")
    if is_edit_mode:
        print(f"Input images: {len(args.images)}")
    if args.size:
        print(f"Size: {args.size}")
    print(f"Prompt: {args.prompt}")

    try:
        # Make API request
        response = requests.post(
            api_url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json=payload,
            timeout=180,
            verify=not args.no_verify_ssl
        )

        response.raise_for_status()
        result = response.json()

        # Check for errors
        if result.get("code"):
            error_msg = result.get("message", "Unknown error")
            print(f"API Error: {error_msg}", file=sys.stderr)
            sys.exit(1)

        # Extract image URLs from response
        output_data = result.get("output", {})
        choices = output_data.get("choices", [])

        if not choices:
            print("Error: No choices in response", file=sys.stderr)
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
            sys.exit(1)

        message = choices[0].get("message", {})
        content = message.get("content", [])

        image_urls = [item["image"] for item in content if item.get("image")]
        if not image_urls:
            print("Error: No image URL in response", file=sys.stderr)
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
            sys.exit(1)

        for url in image_urls:
            print(f"\nImage URL: {url}")

        # Print usage info
        usage = result.get("usage", {})
        if usage:
            print(f"Resolution: {usage.get('width')}*{usage.get('height')}, Count: {usage.get('image_count')}")

        # Download and save images if filename is provided
        if args.filename:
            output_path = Path(args.filename)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            stem = output_path.stem
            suffix = output_path.suffix or ".png"

            for i, url in enumerate(image_urls):
                if len(image_urls) == 1:
                    save_path = output_path
                else:
                    save_path = output_path.parent / f"{stem}_{i + 1}{suffix}"

                print(f"Downloading image {i + 1}/{len(image_urls)}...")
                img_response = requests.get(url, timeout=60, verify=not args.no_verify_ssl)
                img_response.raise_for_status()

                with open(save_path, "wb") as f:
                    f.write(img_response.content)

                full_path = save_path.resolve()
                print(f"Image saved: {full_path}")
                print(f"MEDIA: {full_path}")
        else:
            for url in image_urls:
                print(f"MEDIA_URL: {url}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}", file=sys.stderr)
        try:
            error_detail = response.json()
            print(f"Error details: {json.dumps(error_detail, indent=2, ensure_ascii=False)}", file=sys.stderr)
        except:
            print(f"Response text: {response.text}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error making API request: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
