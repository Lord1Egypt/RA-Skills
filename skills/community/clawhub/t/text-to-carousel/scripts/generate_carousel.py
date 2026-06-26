#!/usr/bin/env python3
"""
Text-to-Carousel Generator
Generates Instagram/social media carousel slides using Gemini image generation.

Usage:
    python3 generate_carousel.py --config carousel_config.json --output ~/Desktop

Config JSON format:
{
    "api_key": "YOUR_GEMINI_API_KEY",
    "model": "gemini-3-pro-image-preview",
    "brand": {
        "name": "HKIII",
        "tagline": "Life Bamboo Salt",
        "style": "dark luxury editorial"
    },
    "product_image": "/path/to/product.jpg",
    "slides": [
        {
            "type": "cover",
            "title": "竹盐与甲状腺健康",
            "subtitle": "天然无碘矿物盐的秘密"
        },
        ...
    ]
}
"""

import urllib.request
import json
import base64
import os
import sys
import time
import argparse


def generate_slide(api_key, model, prompt, product_image_b64=None, timeout=180):
    """Generate a single slide image via Gemini API."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    parts = []
    if product_image_b64:
        parts.append({"inlineData": {"mimeType": "image/jpeg", "data": product_image_b64}})
    parts.append({"text": prompt})

    payload = {
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["image", "text"]}
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    resp = urllib.request.urlopen(req, timeout=timeout)
    result = json.loads(resp.read())

    for candidate in result.get("candidates", []):
        for part in candidate.get("content", {}).get("parts", []):
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                mime = part["inlineData"].get("mimeType", "image/png")
                ext = "png" if "png" in mime else "jpg"
                return img_data, ext
    return None, None


def main():
    parser = argparse.ArgumentParser(description="Generate carousel slides with Gemini")
    parser.add_argument("--config", required=True, help="Path to carousel config JSON")
    parser.add_argument("--output", default=os.path.expanduser("~/Desktop"), help="Output directory")
    parser.add_argument("--delay", type=int, default=5, help="Delay between API calls (seconds)")
    args = parser.parse_args()

    with open(args.config, "r") as f:
        config = json.load(f)

    api_key = config["api_key"]
    model = config.get("model", "gemini-3-pro-image-preview")
    slides = config["slides"]
    total = len(slides)

    # Load product image if specified
    product_b64 = None
    if config.get("product_image") and os.path.exists(config["product_image"]):
        with open(config["product_image"], "rb") as f:
            product_b64 = base64.b64encode(f.read()).decode()

    os.makedirs(args.output, exist_ok=True)
    prefix = config.get("file_prefix", "carousel")

    for i, slide in enumerate(slides):
        slide_num = i + 1
        name = slide.get("name", f"{slide_num:02d}")
        print(f"  [{slide_num}/{total}] Generating {name}... ", end="", flush=True)

        prompt = slide["prompt"]

        # Determine if this slide needs product image
        use_product = slide.get("use_product_image", False) and product_b64

        try:
            img_data, ext = generate_slide(
                api_key, model, prompt,
                product_image_b64=product_b64 if use_product else None
            )
            if img_data:
                path = os.path.join(args.output, f"{prefix}_{name}.{ext}")
                with open(path, "wb") as f:
                    f.write(img_data)
                print(f"OK ({len(img_data)//1024}KB)")
            else:
                print("FAIL - no image in response")
        except Exception as e:
            err = ""
            try:
                err = e.read().decode()[:200] if hasattr(e, 'read') else str(e)
            except:
                err = str(e)
            print(f"FAIL: {err}")

        if i < total - 1:
            time.sleep(args.delay)

    print(f"\n  Done! {total} slides saved to {args.output}/")


if __name__ == "__main__":
    main()
