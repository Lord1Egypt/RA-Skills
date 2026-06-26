#!/usr/bin/env python3
"""Generate illustration images with OpenAI first and Gemini as fallback.

Usage:
    python generate_image.py --prompt "your prompt" --output image.png
    python generate_image.py --provider openai --prompt "your prompt"
    python generate_image.py --provider gemini --prompt "your prompt"
"""

import argparse
import base64
import json
import math
import os
import sys
from pathlib import Path
from typing import Any

import httpx

DEFAULT_PROVIDER = "auto"
DEFAULT_OPENAI_MODEL = "gpt-image-2"
DEFAULT_GEMINI_MODEL = "gemini-3.1-flash-image-preview"
DEFAULT_ASPECT_RATIO = "3:2"
DEFAULT_IMAGE_SIZE = "1K"
DEFAULT_OPENAI_QUALITY = "high"
DEFAULT_STYLE_PREFIX = (
    "Use a clean, modern color palette with soft tones. "
    "Minimalist flat illustration style with clear visual hierarchy. "
    "Professional and polished look suitable for technical blog articles. "
    "No photorealistic rendering. No excessive gradients or shadows."
)

VALID_PROVIDERS = ["auto", "openai", "gemini"]
VALID_ASPECT_RATIOS = [
    "1:1",
    "1:4",
    "1:8",
    "2:3",
    "3:2",
    "3:4",
    "4:1",
    "4:3",
    "4:5",
    "5:4",
    "8:1",
    "9:16",
    "16:9",
    "21:9",
]
VALID_IMAGE_SIZES = ["512", "1K", "2K", "4K"]
VALID_OPENAI_QUALITIES = ["low", "medium", "high", "auto"]


class GenerationError(RuntimeError):
    """Raised when an image provider cannot complete the request."""


def build_prompt(prompt: str, style_prefix: str) -> str:
    return f"{style_prefix}\n\n{prompt}" if style_prefix else prompt


def ensure_parent(path: str) -> None:
    parent = Path(path).expanduser().parent
    if str(parent) != ".":
        parent.mkdir(parents=True, exist_ok=True)


def parse_aspect_ratio(aspect_ratio: str) -> tuple[int, int]:
    try:
        width, height = aspect_ratio.split(":", 1)
        return int(width), int(height)
    except ValueError as exc:
        raise GenerationError(f"Invalid aspect ratio: {aspect_ratio}") from exc


def round_to_multiple(value: float, multiple: int = 16) -> int:
    return max(multiple, int(round(value / multiple)) * multiple)


def openai_size_from_aspect(aspect_ratio: str, image_size: str) -> str:
    """Map Gemini-style ratio/tiers to valid gpt-image-2 dimensions."""
    ratio_w, ratio_h = parse_aspect_ratio(aspect_ratio)
    long_to_short = max(ratio_w, ratio_h) / min(ratio_w, ratio_h)
    if long_to_short > 3:
        raise GenerationError(
            f"Aspect ratio {aspect_ratio} is not supported by gpt-image-2 because it exceeds 3:1"
        )

    short_edge_by_tier = {
        "512": 768,
        "1K": 1024,
        "2K": 2048,
        "4K": 2160,
    }
    short_edge = short_edge_by_tier[image_size]

    if ratio_w >= ratio_h:
        height = short_edge
        width = short_edge * ratio_w / ratio_h
    else:
        width = short_edge
        height = short_edge * ratio_h / ratio_w

    max_edge = 3840
    max_pixels = 8_294_400
    min_pixels = 655_360

    scale = min(1.0, max_edge / max(width, height))
    if width * height * scale * scale > max_pixels:
        scale = math.sqrt(max_pixels / (width * height))

    width = round_to_multiple(width * scale)
    height = round_to_multiple(height * scale)

    while width * height > max_pixels:
        width = round_to_multiple(width - 16)
        height = round_to_multiple(height - 16)

    if width * height < min_pixels:
        scale = math.sqrt(min_pixels / (width * height))
        width = round_to_multiple(width * scale)
        height = round_to_multiple(height * scale)

    return f"{width}x{height}"


def save_image_bytes(image_bytes: bytes, output_path: str) -> str:
    ensure_parent(output_path)
    with open(output_path, "wb") as file:
        file.write(image_bytes)
    return output_path


def generate_with_openai(
    prompt: str,
    output_path: str,
    model: str,
    aspect_ratio: str,
    image_size: str,
    quality: str,
) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise GenerationError("OPENAI_API_KEY environment variable is not set.")

    size = openai_size_from_aspect(aspect_ratio, image_size)
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "quality": quality,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    print(f"Provider:     openai")
    print(f"Model:        {model}")
    print(f"Size:         {size}")
    print(f"Quality:      {quality}")
    print(f"Output:       {output_path}")
    print("Generating...")

    response = httpx.post(
        "https://api.openai.com/v1/images/generations",
        headers=headers,
        json=payload,
        timeout=300,
    )
    if response.status_code != 200:
        raise GenerationError(f"OpenAI API error {response.status_code}: {response.text[:500]}")

    data = response.json()
    images = data.get("data", [])
    if not images:
        raise GenerationError(f"No image data returned. Response: {json.dumps(data)[:500]}")

    first = images[0]
    if first.get("b64_json"):
        image_bytes = base64.b64decode(first["b64_json"])
    elif first.get("url"):
        image_response = httpx.get(first["url"], timeout=120)
        image_response.raise_for_status()
        image_bytes = image_response.content
    else:
        raise GenerationError(f"No supported image payload returned. Response: {json.dumps(first)[:500]}")

    save_image_bytes(image_bytes, output_path)
    print(f"Done! Saved {len(image_bytes):,} bytes to {output_path}")
    return output_path


def generate_with_gemini(
    prompt: str,
    output_path: str,
    model: str,
    aspect_ratio: str,
    image_size: str,
) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise GenerationError("GEMINI_API_KEY environment variable is not set.")

    if aspect_ratio not in VALID_ASPECT_RATIOS:
        raise GenerationError(f"Invalid aspect ratio '{aspect_ratio}'. Valid: {VALID_ASPECT_RATIOS}")

    if image_size not in VALID_IMAGE_SIZES:
        raise GenerationError(f"Invalid image size '{image_size}'. Valid: {VALID_IMAGE_SIZES}")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": image_size,
            },
        },
    }

    print(f"Provider:     gemini")
    print(f"Model:        {model}")
    print(f"Aspect ratio: {aspect_ratio}")
    print(f"Image size:   {image_size}")
    print(f"Output:       {output_path}")
    print("Generating...")

    response = httpx.post(url, json=payload, timeout=180)
    if response.status_code != 200:
        raise GenerationError(f"Gemini API error {response.status_code}: {response.text[:500]}")

    data = response.json()
    candidates = data.get("candidates", [])
    if not candidates:
        raise GenerationError(f"No candidates returned. Response: {json.dumps(data)[:500]}")

    parts = candidates[0].get("content", {}).get("parts", [])
    for part in parts:
        if "inlineData" in part:
            image_bytes = base64.b64decode(part["inlineData"]["data"])
            save_image_bytes(image_bytes, output_path)
            print(f"Done! Saved {len(image_bytes):,} bytes to {output_path}")
            return output_path

    text_parts = [part.get("text", "") for part in parts if "text" in part]
    if text_parts:
        print(f"Model text response: {text_parts[0][:300]}", file=sys.stderr)
    raise GenerationError("No image data in response.")


def generate_image(
    prompt: str,
    output_path: str,
    provider: str = DEFAULT_PROVIDER,
    openai_model: str = DEFAULT_OPENAI_MODEL,
    gemini_model: str = DEFAULT_GEMINI_MODEL,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    image_size: str = DEFAULT_IMAGE_SIZE,
    openai_quality: str = DEFAULT_OPENAI_QUALITY,
    style_prefix: str = DEFAULT_STYLE_PREFIX,
) -> str:
    if provider not in VALID_PROVIDERS:
        raise GenerationError(f"Invalid provider '{provider}'. Valid: {VALID_PROVIDERS}")
    if image_size not in VALID_IMAGE_SIZES:
        raise GenerationError(f"Invalid image size '{image_size}'. Valid: {VALID_IMAGE_SIZES}")
    if openai_quality not in VALID_OPENAI_QUALITIES:
        raise GenerationError(f"Invalid OpenAI quality '{openai_quality}'. Valid: {VALID_OPENAI_QUALITIES}")

    full_prompt = build_prompt(prompt, style_prefix)
    print(f"Prompt:       {prompt[:120]}{'...' if len(prompt) > 120 else ''}")

    if provider == "openai":
        return generate_with_openai(
            prompt=full_prompt,
            output_path=output_path,
            model=openai_model,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
            quality=openai_quality,
        )

    if provider == "gemini":
        return generate_with_gemini(
            prompt=full_prompt,
            output_path=output_path,
            model=gemini_model,
            aspect_ratio=aspect_ratio,
            image_size=image_size,
        )

    errors: list[str] = []
    if os.environ.get("OPENAI_API_KEY"):
        try:
            return generate_with_openai(
                prompt=full_prompt,
                output_path=output_path,
                model=openai_model,
                aspect_ratio=aspect_ratio,
                image_size=image_size,
                quality=openai_quality,
            )
        except Exception as exc:
            errors.append(f"OpenAI failed: {exc}")
            print(f"OpenAI failed; trying Gemini fallback. Reason: {exc}", file=sys.stderr)

    if os.environ.get("GEMINI_API_KEY"):
        try:
            return generate_with_gemini(
                prompt=full_prompt,
                output_path=output_path,
                model=gemini_model,
                aspect_ratio=aspect_ratio,
                image_size=image_size,
            )
        except Exception as exc:
            errors.append(f"Gemini failed: {exc}")

    if errors:
        raise GenerationError("; ".join(errors))
    raise GenerationError("No provider credentials found. Set OPENAI_API_KEY or GEMINI_API_KEY.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate illustration images")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", default="generated_image.png", help="Output file path")
    parser.add_argument("--provider", choices=VALID_PROVIDERS, default=DEFAULT_PROVIDER, help="Provider selection")
    parser.add_argument("--model", default=None, help="Provider model ID. Applies to the selected provider.")
    parser.add_argument("--openai-model", default=DEFAULT_OPENAI_MODEL, help=f"OpenAI model ID (default: {DEFAULT_OPENAI_MODEL})")
    parser.add_argument("--gemini-model", default=DEFAULT_GEMINI_MODEL, help=f"Gemini model ID (default: {DEFAULT_GEMINI_MODEL})")
    parser.add_argument("--aspect-ratio", default=DEFAULT_ASPECT_RATIO, help=f"Aspect ratio (default: {DEFAULT_ASPECT_RATIO})")
    parser.add_argument("--image-size", default=DEFAULT_IMAGE_SIZE, help=f"Image size tier (default: {DEFAULT_IMAGE_SIZE})")
    parser.add_argument("--openai-quality", choices=VALID_OPENAI_QUALITIES, default=DEFAULT_OPENAI_QUALITY)
    parser.add_argument("--style-prefix", default=None, help="Custom style prefix (overrides default)")
    parser.add_argument("--no-style", action="store_true", help="Skip the default style prefix")

    args = parser.parse_args()

    style = ""
    if args.no_style:
        style = ""
    elif args.style_prefix:
        style = args.style_prefix
    else:
        style = DEFAULT_STYLE_PREFIX

    openai_model = args.openai_model
    gemini_model = args.gemini_model
    if args.model:
        if args.provider == "gemini":
            gemini_model = args.model
        else:
            openai_model = args.model

    try:
        generate_image(
            prompt=args.prompt,
            output_path=args.output,
            provider=args.provider,
            openai_model=openai_model,
            gemini_model=gemini_model,
            aspect_ratio=args.aspect_ratio,
            image_size=args.image_size,
            openai_quality=args.openai_quality,
            style_prefix=style,
        )
    except GenerationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
