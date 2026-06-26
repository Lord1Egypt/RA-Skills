#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "requests>=2.31.0",
# ]
# ///

"""
Seedream Image Generation Script
Supports: text-to-image, image editing, multi-reference fusion, sequential (group) generation,
          PNG output, prompt optimization, watermark control, model listing.

Based on Volcengine official API docs:
https://www.volcengine.com/docs/82379/1541523
https://www.volcengine.com/docs/82379/1824121
"""

import argparse
import json
import os
import sys
import requests

API_BASE = "https://ark.cn-beijing.volces.com/api/v3"
GENERATE_URL = f"{API_BASE}/images/generations"
MODELS_URL = f"{API_BASE}/models"

# Model capabilities (from official docs: https://www.volcengine.com/docs/82379/1541523)
MODEL_CAPABILITIES = {
    "doubao-seedream-5-0-260128": {
        "aliases": ["doubao-seedream-5-0-lite-260128"],
        "name": "Doubao-Seedream-5.0-lite",
        "sizes": ["2K", "3K", "4K"],
        "output_formats": ["png", "jpeg"],
        "prompt_optimization": ["standard"],
        "stream": True,
        "web_search": True,
    },
    "doubao-seedream-4-5-251128": {
        "name": "Doubao-Seedream-4.5",
        "sizes": ["2K", "4K"],
        "output_formats": ["jpeg"],
        "prompt_optimization": ["standard"],
        "stream": True,
        "web_search": False,
    },
    "doubao-seedream-4-0-250828": {
        "name": "Doubao-Seedream-4.0",
        "sizes": ["1K", "2K", "4K"],
        "output_formats": ["jpeg"],
        "prompt_optimization": ["standard", "fast"],
        "stream": True,
        "web_search": False,
    },
}

# Supported input image formats (5.0-lite/4.5/4.0)
SUPPORTED_IMAGE_FORMATS = ["jpeg", "png", "webp", "bmp", "tiff", "gif", "heic", "heif"]


def list_models(api_key):
    """Query available Seedream models from the API."""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    try:
        resp = requests.get(MODELS_URL, headers=headers, timeout=30)
        resp.raise_for_status()
        result = resp.json()
        models = result.get("data", [])
        seedream_models = [m for m in models if "seedream" in m.get("id", "").lower()]
        if not seedream_models:
            print("No Seedream models found. All available models:")
            for m in models:
                print(f"  - {m.get('id', 'unknown')}")
            return
        print(f"Available Seedream models ({len(seedream_models)}):")
        for m in seedream_models:
            mid = m.get("id", "unknown")
            caps = MODEL_CAPABILITIES.get(mid, {})
            name = caps.get("name", mid)
            sizes = ", ".join(caps.get("sizes", ["unknown"]))
            fmts = ", ".join(caps.get("output_formats", ["unknown"]))
            print(f"  - {mid} ({name})")
            print(f"    Sizes: {sizes} | Output: {fmts}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Failed to list models: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response body: {e.response.text}")
        sys.exit(1)


def generate_image(prompt, model, size, api_key, image_input=None,
                   sequential=False, max_images=1, response_format="url",
                   output_format=None, watermark=True,
                   prompt_optimization=None, stream=False, web_search=False):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "response_format": response_format,
        "watermark": watermark,
    }

    if output_format:
        payload["output_format"] = output_format

    if image_input:
        payload["image"] = image_input

    if sequential:
        payload["sequential_image_generation"] = "auto"
        payload["sequential_image_generation_options"] = {"max_images": max_images}
    else:
        payload["sequential_image_generation"] = "disabled"

    if prompt_optimization:
        payload["optimize_prompt_options"] = {"mode": prompt_optimization}

    if stream:
        payload["stream"] = True

    if web_search:
        payload["tools"] = [{"type": "web_search"}]

    try:
        response = requests.post(GENERATE_URL, headers=headers, json=payload, timeout=300)
        response.raise_for_status()
        result = response.json()

        if "data" in result and len(result["data"]) > 0:
            for i, item in enumerate(result["data"]):
                if "url" in item:
                    print(f"MEDIA_URL: {item['url']}")
                elif "b64_json" in item:
                    print(f"MEDIA_B64: {item['b64_json']}")
                else:
                    print(f"INFO: Unrecognized item payload: {json.dumps(item, ensure_ascii=False)}")
        else:
            print(f"ERROR: No image data in response. Full response: {json.dumps(result)}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: API request failed: {e}")
        if hasattr(e, "response") and e.response is not None:
            print(f"Response body: {e.response.text}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Volcengine Seedream API.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to image
  %(prog)s --prompt "一只赛博朋克风格的猫" --size 2K --no-watermark

  # Image editing (single reference)
  %(prog)s --prompt "将其变为水墨画风格" --image "https://example.com/photo.jpg"

  # Multi-reference fusion
  %(prog)s --prompt "融合两张图的风格" --image "https://a.jpg" --image "https://b.jpg"

  # Sequential/group generation
  %(prog)s --prompt "四格漫画" --sequential --max-images 4

  # PNG output with prompt optimization
  %(prog)s --prompt "高清风景" --output-format png --prompt-optimization standard

  # List available models
  %(prog)s --list-models

  # Web search enabled (5.0-lite only)
  %(prog)s --prompt "今天上海天气预报图" --web-search

  # Stream output
  %(prog)s --prompt "风景画" --stream

  # Custom pixel size
  %(prog)s --prompt "宽屏壁纸" --size 3840x2160

Model capabilities (Volcengine API, updated 2026-05-16):
  Seedream 5.0-lite: 2K/3K/4K, png/jpeg, standard optimization, stream, web_search (only model)
  Seedream 4.5:      2K/4K, jpeg,     standard optimization, stream
  Seedream 4.0:      1K/2K/4K, jpeg,  standard+fast optimization, stream
""",
    )
    parser.add_argument("--prompt", help="Text prompt for image generation")
    parser.add_argument("--model", default="doubao-seedream-5-0-260128",
                        help="Model ID (default: doubao-seedream-5-0-260128)")
    parser.add_argument("--size", default="2K",
                        help="Image size: 1K/2K/3K/4K or pixel format WIDTHxHEIGHT (default: 2K)")
    parser.add_argument("--api-key", help="Volcengine API Key (or set VOLC_API_KEY env)")
    parser.add_argument("--image", action="append",
                        help="Reference image URL/base64. Repeat for multiple images (max 14). "
                             "Formats: jpeg/png/webp/bmp/tiff/gif/heic/heif")
    parser.add_argument("--response-format", default="url", choices=["url", "b64_json"],
                        help="Response format (default: url)")
    parser.add_argument("--output-format", choices=["jpeg", "png"],
                        help="Output image format (only 5.0-lite supports png)")
    parser.add_argument("--watermark", dest="watermark", action="store_true", default=True,
                        help="Enable watermark (default)")
    parser.add_argument("--no-watermark", dest="watermark", action="store_false",
                        help="Disable watermark")
    parser.add_argument("--sequential", action="store_true",
                        help="Enable sequential/group image generation")
    parser.add_argument("--max-images", type=int, default=1,
                        help="Max images for sequential generation (1-15, default: 1)")
    parser.add_argument("--prompt-optimization", choices=["standard", "fast"],
                        help="Prompt optimization mode (4.0 supports both, 5.0-lite/4.5 standard only)")
    parser.add_argument("--stream", action="store_true",
                        help="Enable streaming output (all models)")
    parser.add_argument("--web-search", action="store_true",
                        help="Enable web search for real-time info (5.0-lite only)")
    parser.add_argument("--list-models", action="store_true",
                        help="List available Seedream models and their capabilities")

    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("VOLC_API_KEY")
    if not api_key:
        print("ERROR: API key required. Use --api-key or set VOLC_API_KEY env var.")
        sys.exit(1)

    if args.list_models:
        list_models(api_key)
        return

    if not args.prompt:
        print("ERROR: --prompt is required (unless using --list-models).")
        sys.exit(1)

    # Validate model + size combination
    caps = MODEL_CAPABILITIES.get(args.model, {})
    if caps:
        # Check if size is a preset (1K/2K/3K/4K) or pixel format (WIDTHxHEIGHT)
        is_pixel_size = "x" in args.size
        if not is_pixel_size:
            supported_sizes = caps.get("sizes", [])
            if args.size not in supported_sizes:
                print(f"WARNING: {args.model} may not support size '{args.size}'. "
                      f"Supported presets: {', '.join(supported_sizes)} (or use pixel format WIDTHxHEIGHT)")
        if args.output_format:
            supported_fmts = caps.get("output_formats", [])
            if args.output_format not in supported_fmts:
                print(f"WARNING: {args.model} may not support output format '{args.output_format}'. "
                      f"Supported: {', '.join(supported_fmts)}")
        if args.prompt_optimization:
            supported_opts = caps.get("prompt_optimization", [])
            if args.prompt_optimization not in supported_opts:
                print(f"WARNING: {args.model} may not support prompt optimization '{args.prompt_optimization}'. "
                      f"Supported: {', '.join(supported_opts)}")
        # Note: fast mode only available on 4.0 per official docs
        if args.prompt_optimization == "fast" and args.model != "doubao-seedream-4-0-250828":
            print(f"WARNING: 'fast' prompt optimization is only supported by doubao-seedream-4-0-250828. "
                  f"Current model: {args.model}")
        if args.stream and not caps.get("stream"):
            print(f"WARNING: {args.model} may not support stream output.")
        if args.web_search and not caps.get("web_search"):
            print(f"WARNING: {args.model} may not support web search.")

    image_input = None
    if args.image:
        if len(args.image) == 1:
            image_input = args.image[0]
        else:
            if len(args.image) > 14:
                print("ERROR: Maximum 14 reference images allowed.")
                sys.exit(1)
            image_input = args.image

    generate_image(
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        api_key=api_key,
        image_input=image_input,
        sequential=args.sequential,
        max_images=args.max_images,
        response_format=args.response_format,
        output_format=args.output_format,
        watermark=args.watermark,
        prompt_optimization=args.prompt_optimization,
        stream=args.stream,
        web_search=args.web_search,
    )


if __name__ == "__main__":
    main()
