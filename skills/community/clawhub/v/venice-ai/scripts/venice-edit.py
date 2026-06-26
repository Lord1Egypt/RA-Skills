#!/usr/bin/env python3
"""Edit images via Venice AI Image Edit API."""

import argparse
import base64
import datetime as dt
import io
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Import shared utilities
sys.path.insert(0, str(Path(__file__).parent))
from venice_common import require_api_key, print_media_line, get_mime_type, USER_AGENT, API_BASE


def edit_image_from_file(
    api_key: str,
    image_path: Path,
    prompt: str,
) -> bytes:
    """
    Edit an image via Venice API using multipart file upload.
    Returns raw image bytes.
    """
    url = f"{API_BASE}/image/edit"
    
    # Build multipart form data
    boundary = "----VeniceEditBoundary"
    
    # Read image
    image_data = image_path.read_bytes()
    filename = image_path.name
    mime = get_mime_type(filename)
    
    body = io.BytesIO()
    
    # Add image file
    body.write(f'--{boundary}\r\n'.encode())
    body.write(f'Content-Disposition: form-data; name="image"; filename="{filename}"\r\n'.encode())
    body.write(f'Content-Type: {mime}\r\n\r\n'.encode())
    body.write(image_data)
    body.write(b'\r\n')
    
    # Add prompt
    body.write(f'--{boundary}\r\n'.encode())
    body.write(b'Content-Disposition: form-data; name="prompt"\r\n\r\n')
    body.write(prompt.encode())
    body.write(b'\r\n')
    
    # End boundary
    body.write(f'--{boundary}--\r\n'.encode())
    
    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": USER_AGENT,
        },
        data=body.getvalue(),
    )
    
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Venice API error ({e.code}): {error_body}") from e


def edit_image_from_url(
    api_key: str,
    image_url: str,
    prompt: str,
) -> bytes:
    """
    Edit an image via Venice API using a URL.
    Returns raw image bytes.
    """
    
    url = f"{API_BASE}/image/edit"
    
    payload = {
        "image": image_url,
        "prompt": prompt,
    }
    
    body = json.dumps(payload).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        data=body,
    )
    
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            return resp.read()
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Venice API error ({e.code}): {error_body}") from e


def multi_edit_images(
    api_key: str,
    images: list[str],
    prompt: str,
    model: str = "flux-2-max-edit",
) -> bytes:
    """
    Edit up to 3 images together using Venice multi-edit endpoint.
    Images can be local paths, HTTP URLs, or data URLs.
    Returns raw image bytes.
    """
    url = f"{API_BASE}/image/multi-edit"

    # Resolve each image to data URL or keep as http URL
    resolved = []
    for src in images[:3]:  # API supports 1-3 images
        if src.startswith(("http://", "https://", "data:")):
            resolved.append(src)
        else:
            fp = Path(src).expanduser()
            if not fp.exists():
                raise FileNotFoundError(f"Image not found: {fp}")
            suffix = fp.suffix.lower().lstrip(".")
            mime_map = {"jpg": "image/jpeg", "jpeg": "image/jpeg",
                        "png": "image/png", "webp": "image/webp"}
            mime = mime_map.get(suffix, "image/jpeg")
            b64 = base64.b64encode(fp.read_bytes()).decode()
            resolved.append(f"data:{mime};base64,{b64}")

    payload = {
        "images": resolved,
        "prompt": prompt,
        "modelId": model,
    }

    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
        data=body,
    )

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            ct = resp.headers.get("Content-Type", "")
            data = resp.read()
            # Response may be raw image bytes or JSON with base64
            if "application/json" in ct:
                result = json.loads(data)
                images_b64 = result.get("images", [])
                if images_b64:
                    import base64 as _b64
                    return _b64.b64decode(images_b64[0])
                raise RuntimeError(f"No images in response: {result}")
            return data
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Venice API error ({e.code}): {error_body}") from e


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Edit images via Venice AI API. The AI interprets your prompt to determine what to modify."
    )
    ap.add_argument("image", nargs="?", help="Path to image file to edit (or use --url)")
    ap.add_argument("--url", help="URL of image to edit (http:// or https://)")
    ap.add_argument("--prompt", "-p", help="Edit instructions (e.g., 'add sunglasses', 'change sky to sunset')")
    ap.add_argument("--out-dir", help="Output directory (default: same as input or current dir for URLs)")
    ap.add_argument("--output", "-o", help="Output filename (default: auto-generated)")
    # Multi-edit options
    ap.add_argument("--multi-edit", nargs="+", metavar="IMAGE",
                    help="Multi-edit mode: 1-3 images to compose/edit together")
    ap.add_argument("--model", default="flux-2-max-edit",
                    help="Model for multi-edit (default: flux-2-max-edit; also: qwen-edit, gpt-image-1-5-edit)")
    args = ap.parse_args()

    api_key = require_api_key()

    # Handle --multi-edit
    if args.multi_edit:
        if not args.prompt:
            print("Error: --prompt is required for multi-edit", file=sys.stderr)
            return 2
        if len(args.multi_edit) > 3:
            print("Warning: multi-edit supports up to 3 images; using first 3", file=sys.stderr)

        print(f"Multi-edit: {len(args.multi_edit)} image(s)")
        for i, img in enumerate(args.multi_edit[:3]):
            print(f"  [{i+1}] {img[:60]}{'...' if len(img) > 60 else ''}")
        print(f"  Model: {args.model}")
        print(f"  Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")

        try:
            result = multi_edit_images(
                api_key=api_key,
                images=args.multi_edit,
                prompt=args.prompt,
                model=args.model,
            )
        except (RuntimeError, FileNotFoundError) as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

        if args.output:
            out_path = Path(args.output).expanduser()
        else:
            out_dir = Path(args.out_dir).expanduser() if args.out_dir else Path.cwd()
            out_dir.mkdir(parents=True, exist_ok=True)
            timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            out_path = out_dir / f"multi-edited-{timestamp}.png"

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(result)
        print(f"\nSaved: {out_path.as_posix()} ({len(result) // 1024}KB)")
        print_media_line(out_path)
        return 0

    # Validate input for single-edit
    if not args.prompt:
        print("Error: --prompt is required", file=sys.stderr)
        return 2
    if not args.image and not args.url:
        print("Error: Either image path or --url is required", file=sys.stderr)
        return 2
    if args.image and args.url:
        print("Error: Provide either image path or --url, not both", file=sys.stderr)
        return 2
    
    # Handle URL input
    if args.url:
        if not args.url.startswith(("http://", "https://")):
            print("Error: URL must start with http:// or https://", file=sys.stderr)
            return 2
        
        # Determine output path for URL input
        if args.output:
            out_path = Path(args.output).expanduser()
        else:
            out_dir = Path(args.out_dir).expanduser() if args.out_dir else Path.cwd()
            out_dir.mkdir(parents=True, exist_ok=True)
            timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            out_path = out_dir / f"edited-{timestamp}.png"
        
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Editing: {args.url[:60]}{'...' if len(args.url) > 60 else ''}")
        print(f"  Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
        
        try:
            result = edit_image_from_url(
                api_key=api_key,
                image_url=args.url,
                prompt=args.prompt,
            )
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    else:
        # Handle file input
        image_path = Path(args.image).expanduser()
        if not image_path.exists():
            print(f"Error: Image not found: {image_path}", file=sys.stderr)
            return 2
        
        # Determine output path
        if args.output:
            out_path = Path(args.output).expanduser()
        else:
            out_dir = Path(args.out_dir).expanduser() if args.out_dir else image_path.parent
            out_dir.mkdir(parents=True, exist_ok=True)
            timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
            suffix = image_path.suffix or ".png"
            out_path = out_dir / f"{image_path.stem}-edited-{timestamp}{suffix}"
        
        out_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"Editing: {image_path.name}")
        print(f"  Prompt: {args.prompt[:80]}{'...' if len(args.prompt) > 80 else ''}")
        
        try:
            result = edit_image_from_file(
                api_key=api_key,
                image_path=image_path,
                prompt=args.prompt,
            )
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
    
    out_path.write_bytes(result)
    print(f"\nSaved: {out_path.as_posix()}")
    print(f"Size: {len(result) / 1024:.1f}KB")
    
    print_media_line(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
