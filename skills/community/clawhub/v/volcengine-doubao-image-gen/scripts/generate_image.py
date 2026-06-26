#!/usr/bin/env python3
"""
Doubao Image Generation - 豆包图片生成

使用火山引擎豆包 API 生成图片。
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
SUPPORTED_MODELS = {
    "doubao-seedream-4-5-251128": "Seedream 4.5，稳定的文生图/图生图模型",
    "doubao-seedream-5-0-260128": "Seedream 5.0，新版文生图/图生图模型",
    "doubao-seedance-1-5-pro-251215": "Seedance 1.5 Pro，按账户能力透传调用（可能需要不同后端能力）",
}
MODEL_ALIASES = {
    "seedream-4.5": "doubao-seedream-4-5-251128",
    "seedream4.5": "doubao-seedream-4-5-251128",
    "seedream-5.0": "doubao-seedream-5-0-260128",
    "seedream5": "doubao-seedream-5-0-260128",
    "seedream5.0": "doubao-seedream-5-0-260128",
    "seedance-1.5-pro": "doubao-seedance-1-5-pro-251215",
    "seedance15pro": "doubao-seedance-1-5-pro-251215",
}
DEFAULT_MODEL = os.environ.get("DOUBAO_MODEL", "doubao-seedream-5-0-260128")


def resolve_model(model: str | None) -> str:
    selected = (model or DEFAULT_MODEL).strip()
    selected = MODEL_ALIASES.get(selected, selected)
    return selected


def generate_image(
    prompt: str,
    api_key: str,
    size: str = "2K",
    watermark: bool = True,
    model: str = DEFAULT_MODEL,
    image=None,
    sequential: str = "disabled",
    max_images: int = None,
    stream: bool = False,
) -> dict:
    model = resolve_model(model)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    payload = {
        "model": model,
        "prompt": prompt,
        "sequential_image_generation": sequential,
        "response_format": "url",
        "size": size,
        "stream": stream,
        "watermark": watermark,
    }

    if image:
        payload["image"] = image if isinstance(image, list) else image

    if sequential == "auto" and max_images:
        payload["sequential_image_generation_options"] = {
            "max_images": max_images
        }

    data = json.dumps(payload).encode("utf-8")
    request = Request(API_URL, data=data, headers=headers, method="POST")

    try:
        with urlopen(request, timeout=120) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "Unknown error"
        raise Exception(f"API Error {e.code}: {error_body}")
    except URLError as e:
        raise Exception(f"Network Error: {e.reason}")


def sanitize_filename(name: str, default_stem: str = "image") -> str:
    base = os.path.basename(name or "")
    stem, ext = os.path.splitext(base)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-._")
    stem = stem[:80] or default_stem
    ext = ext.lower() if ext.lower() in {".png", ".jpg", ".jpeg", ".webp"} else ".png"
    return f"{stem}{ext}"


def ensure_safe_output_path(filepath: str) -> str:
    normalized = os.path.normpath(filepath)
    if os.path.isabs(normalized):
        return normalized
    if normalized.startswith("..") or "/../" in normalized:
        raise ValueError("Unsafe output path: parent traversal is not allowed")
    return normalized


def validate_download_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError(f"Unsupported image URL scheme: {parsed.scheme or 'empty'}")
    if not parsed.netloc:
        raise ValueError("Image URL is missing host")
    return url


def download_image(url: str, filepath: str) -> None:
    safe_url = validate_download_url(url)
    safe_path = ensure_safe_output_path(filepath)
    request = Request(safe_url, headers={"User-Agent": "OpenClaw-DoubaoImageGen/1.0"})
    with urlopen(request, timeout=60) as response:
        content_type = (response.headers.get("Content-Type") or "").lower()
        if not content_type.startswith("image/"):
            raise ValueError(f"Downloaded content is not an image: {content_type or 'unknown'}")
        with open(safe_path, "wb") as f:
            f.write(response.read())
    print(f"✓ Image saved to: {safe_path}")


def generate_filename(prompt: str, index: int = None) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    words = prompt.split()[:5]
    raw_name = "-".join(words).replace(",", "").replace("，", "")[:60]
    safe_name = sanitize_filename(raw_name, default_stem="image")
    stem, ext = os.path.splitext(safe_name)
    if index:
        return f"{timestamp}-{stem}-{index}{ext}"
    return f"{timestamp}-{stem}{ext}"


def main():
    parser = argparse.ArgumentParser(description="豆包图片生成 - 使用火山引擎 API 生成图片")
    parser.add_argument("--prompt", "-p", required=True, help="图片描述/提示词")
    parser.add_argument("--filename", "-f", help="输出文件名 (默认自动生成)")
    parser.add_argument("--size", "-s", choices=["1K", "2K", "4K"], default="2K", help="图片尺寸")
    parser.add_argument("--no-watermark", action="store_true", help="不添加水印")
    parser.add_argument(
        "--model",
        "-m",
        default=DEFAULT_MODEL,
        help=(
            f"模型名称 (默认：{DEFAULT_MODEL})。支持："
            + ", ".join(sorted(SUPPORTED_MODELS.keys()))
        ),
    )
    parser.add_argument("--image", "-i", action="append", help="参考图 URL（可多次指定）")
    parser.add_argument("--sequential", choices=["disabled", "auto"], default="disabled", help="是否生成组图")
    parser.add_argument("--max-images", type=int, default=None, help="组图最大数量")
    parser.add_argument("--stream", action="store_true", help="流式输出")
    args = parser.parse_args()

    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("Error: No API key provided.")
        print("Please set ARK_API_KEY environment variable:")
        print("  export ARK_API_KEY='your-api-key'")
        sys.exit(1)

    image = None
    if args.image:
        image = args.image[0] if len(args.image) == 1 else args.image

    resolved_model = resolve_model(args.model)
    filename = ensure_safe_output_path(args.filename) if args.filename else generate_filename(args.prompt)

    print("Generating image...")
    print(f"  Prompt: {args.prompt[:50]}...")
    print(f"  Size: {args.size}")
    print(f"  Model: {resolved_model}")

    if resolved_model not in SUPPORTED_MODELS:
        print("Warning: model is not in the local supported-model list.")
        print("The request will still be sent through to Volcengine as-is.")

    try:
        result = generate_image(
            prompt=args.prompt,
            api_key=api_key,
            size=args.size,
            watermark=not args.no_watermark,
            model=resolved_model,
            image=image,
            sequential=args.sequential,
            max_images=args.max_images,
            stream=args.stream,
        )

        if "data" in result and len(result["data"]) > 0:
            for idx, item in enumerate(result["data"]):
                image_url = item.get("url")
                if image_url:
                    if len(result["data"]) > 1 and not args.filename:
                        output_file = generate_filename(args.prompt, idx + 1)
                    elif len(result["data"]) > 1 and args.filename:
                        root, ext = os.path.splitext(filename)
                        safe_root = ensure_safe_output_path(root)
                        output_file = f"{safe_root}-{idx + 1}{ext or '.png'}"
                    else:
                        output_file = filename
                    download_image(image_url, output_file)
                else:
                    print(f"Error: No image URL in response {idx + 1}")
            print(f"\n✅ Generated {len(result['data'])} image(s)")
        else:
            print("Error: No image URL in response")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
