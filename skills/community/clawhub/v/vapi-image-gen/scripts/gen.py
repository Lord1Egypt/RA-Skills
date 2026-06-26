#!/usr/bin/env python3
"""
VAPI Image Generation & Editing Script
- Generate: POST /images/generations
- Edit:     POST /images/edits (when --input is provided)
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


def get_oss_dir() -> Path:
    return Path.home() / ".openclaw" / "oss"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return text[:50] or "image"


def download_to_temp(url: str) -> Path:
    """Download remote image to a temp file with chunked read."""
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


def request_generate(
    base_url: str,
    api_key: str,
    prompt: str,
    model: str,
    response_format: str,
    size: str = "",
    aspect_ratio: str = "",
    count: int = 1,
) -> dict:
    """POST /images/generations"""
    url = f"{base_url.rstrip('/')}/images/generations"
    payload = {
        "model": model,
        "prompt": prompt,
        "n": count,
        "response_format": response_format,
    }
    if size:
        payload["size"] = size
    if aspect_ratio:
        payload["aspect_ratio"] = aspect_ratio

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, method="POST",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        data=body,
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"VAPI API error ({e.code}): {e.read().decode('utf-8', errors='replace')}") from e


def request_edit(
    base_url: str,
    api_key: str,
    prompt: str,
    model: str,
    image_path: Path,
    response_format: str,
    size: str = "",
    aspect_ratio: str = "",
    count: int = 1,
) -> dict:
    """POST /images/edits (multipart form data)"""
    url = f"{base_url.rstrip('/')}/images/edits"

    # Build multipart form data manually
    boundary = "----VAPIBoundary" + os.urandom(8).hex()
    parts = []

    def field(name: str, value: str) -> bytes:
        return (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
            f"{value}\r\n"
        ).encode("utf-8")

    parts.append(field("model", model))
    parts.append(field("prompt", prompt))
    parts.append(field("n", str(count)))
    parts.append(field("response_format", response_format))
    if size:
        parts.append(field("size", size))
    if aspect_ratio:
        parts.append(field("aspect_ratio", aspect_ratio))

    # Image file
    img_data = image_path.read_bytes()
    img_mime = "image/jpeg" if image_path.suffix.lower() in (".jpg", ".jpeg") else "image/png"
    parts.append(
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="image"; filename="{image_path.name}"\r\n'
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
        with urllib.request.urlopen(req, timeout=180) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"VAPI API error ({e.code}): {e.read().decode('utf-8', errors='replace')}") from e


def process_response(data: list, response_format: str, should_save: bool,
                      out_dir: Path, prompt: str, count: int, filename: str) -> None:
    for idx, item in enumerate(data):
        image_url = item.get("url")
        image_b64 = item.get("b64_json")

        if response_format == "url" and image_url:
            print(f"MEDIA:{image_url}")
            continue

        # Save mode: decode b64 or fallback to url download
        if not image_b64 and image_url:
            # API returned url even though we asked for b64 — download it
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            fn = filename or f"{ts}-{slugify(prompt)}{f'-{idx+1}' if count > 1 else ''}.png"
            fp = out_dir / fn
            urllib.request.urlretrieve(image_url, fp)
        elif image_b64:
            ts = datetime.now().strftime("%Y%m%d-%H%M%S")
            fn = filename or f"{ts}-{slugify(prompt)}{f'-{idx+1}' if count > 1 else ''}.png"
            fp = out_dir / fn
            fp.write_bytes(base64.b64decode(image_b64))
        else:
            print(f"Warning: no data for image {idx+1}", file=sys.stderr)
            continue

        full_path = fp.resolve()
        print(f"Image saved: {full_path}", file=sys.stderr)
        print(f"MEDIA:{full_path}")


def main():
    ap = argparse.ArgumentParser(description="Generate or edit images via VAPI API.")
    ap.add_argument("--prompt", required=True, help="Image prompt or edit instruction.")
    ap.add_argument("--model", default="nano-banana-pro", help="Model name.")
    ap.add_argument("--input", default="", help="Input image path or URL for editing (enables edit mode).")
    ap.add_argument("--size", default="", help="Image size (e.g. 1024x1024).")
    ap.add_argument("--aspect-ratio", default="", help="Aspect ratio for generation (e.g. 3:4, 16:9).")
    ap.add_argument("--count", type=int, default=1, help="Number of images.")
    ap.add_argument("--save", action="store_true", help="Save to ~/.openclaw/media/.")
    ap.add_argument("--oss", action="store_true", help="Save to ~/.openclaw/oss/.")
    ap.add_argument("--out-dir", default="", help="Save to custom directory.")
    ap.add_argument("--filename", default="", help="Custom output filename.")
    args = ap.parse_args()

    api_key = os.environ.get("VAPI_API_KEY", "").strip()
    base_url = os.environ.get("VAPI_BASE_URL", "https://api.v3.cm/v1").strip()
    if not api_key:
        print("Error: VAPI_API_KEY not set.", file=sys.stderr); sys.exit(1)
    if not base_url:
        base_url = "https://api.v3.cm/v1"

    is_gpt_image = args.model.startswith("gpt-image")
    should_save = args.save or args.oss or is_gpt_image
    response_format = "b64_json" if should_save else "url"

    if should_save:
        if args.out_dir:
            out_dir = Path(args.out_dir)
        elif args.oss:
            out_dir = get_oss_dir()
        else:
            out_dir = get_default_save_dir()
        out_dir.mkdir(parents=True, exist_ok=True)
    else:
        out_dir = get_default_save_dir()  # unused but needed for process_response signature

    try:
        if args.input:
            # Edit mode
            input_path = args.input.strip()
            if input_path.startswith("http"):
                print(f"Downloading input image...", file=sys.stderr)
                local_input = download_to_temp(input_path)
            else:
                local_input = Path(input_path)

            print(f"Editing image with model={args.model} format={response_format}...", file=sys.stderr)
            response = request_edit(
                base_url=base_url, api_key=api_key,
                prompt=args.prompt, model=args.model,
                image_path=local_input, response_format=response_format,
                size=args.size, aspect_ratio=args.aspect_ratio,
                count=args.count,
            )
        else:
            # Generate mode
            print(f"Generating with model={args.model} format={response_format}...", file=sys.stderr)
            response = request_generate(
                base_url=base_url, api_key=api_key,
                prompt=args.prompt, model=args.model,
                response_format=response_format,
                size=args.size, aspect_ratio=args.aspect_ratio,
                count=args.count,
            )

        data = response.get("data", [])
        if not data:
            print("Error: No image data in response.", file=sys.stderr); sys.exit(1)

        process_response(data, response_format, should_save, out_dir,
                         args.prompt, args.count, args.filename)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)


if __name__ == "__main__":
    main()
