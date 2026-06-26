#!/usr/bin/env python3
"""
Image analysis helper for OpenClaw.
Uses vision models (via Ollama) for image understanding, with extended timeout
to support cloud-based models.

Usage:
    python3 analyze_image.py <image_path> [prompt] [model]

Examples:
    python3 analyze_image.py /tmp/screenshot.png
    python3 analyze_image.py /tmp/screen.png "Is this a chess game?"
    python3 analyze_image.py /tmp/test.png "Describe this" kimi-k2.5:cloud

Output: Plain text description from the vision model.
"""

import sys
import json
import base64
import urllib.request
import urllib.error
import os

# Default Ollama API endpoint (override with OLLAMA_API_URL env var)
OLLAMA_API = os.environ.get("OLLAMA_API_URL", "http://localhost:11434/api/chat")

# Default model — local first for privacy (override with VISION_MODEL env var)
DEFAULT_MODEL = os.environ.get("VISION_MODEL", "gemma4:31b")
DEFAULT_PROMPT = "Describe this image in detail, including all visible objects, text, UI elements, and colors."
DEFAULT_TIMEOUT = int(os.environ.get("VISION_TIMEOUT", "180"))  # 3 minutes, override with env var

# File validation constants
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB
ALLOWED_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tiff', '.svg'}


def validate_image_path(image_path: str) -> str:
    """Validate and resolve image path. Returns resolved path or raises ValueError."""
    # Resolve ~ and normalize
    resolved = os.path.abspath(os.path.expanduser(image_path))

    # Check for path traversal
    if '..' in image_path:
        raise ValueError(f"Path traversal not allowed: {image_path}")

    # Check file extension
    _, ext = os.path.splitext(resolved)
    if ext.lower() not in ALLOWED_EXTS:
        raise ValueError(
            f"Unsupported image format: {ext}. "
            f"Allowed: {', '.join(sorted(ALLOWED_EXTS))}"
        )

    # Check file exists
    if not os.path.exists(resolved):
        raise ValueError(f"Image file not found: {image_path}")

    # Check file size
    file_size = os.path.getsize(resolved)
    if file_size > MAX_FILE_SIZE:
        raise ValueError(
            f"Image too large: {file_size / 1024 / 1024:.1f} MB "
            f"(max {MAX_FILE_SIZE / 1024 / 1024:.0f} MB)"
        )

    if file_size == 0:
        raise ValueError("Image file is empty")

    return resolved


def analyze_image(image_path: str, prompt: str = DEFAULT_PROMPT, model: str = DEFAULT_MODEL, timeout: int = DEFAULT_TIMEOUT) -> str:
    try:
        resolved_path = validate_image_path(image_path)
    except ValueError as e:
        return f"Error: {e}"

    # Read and encode image
    try:
        with open(resolved_path, "rb") as f:
            img_data = f.read()
    except OSError as e:
        return f"Error: Failed to read image file"

    b64 = base64.b64encode(img_data).decode()

    # Build Ollama chat request with image
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [b64]
            }
        ],
        "stream": False
    }

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        OLLAMA_API,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        result = json.loads(resp.read().decode())
        content = result.get("message", {}).get("content", "")
        if not content:
            eval_count = result.get("eval_count", 0)
            if eval_count > 0:
                return "(Model returned empty content but ran successfully)"
            return "Error: No content returned from model"
        return content
    except urllib.error.HTTPError as e:
        return "HTTP request failed"
    except urllib.error.URLError:
        return "Connection failed: unable to reach the vision model API"
    except Exception:
        return "Analysis failed: unexpected error"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 analyze_image.py <image_path> [prompt] [model]")
        print("  image_path  Path to image file (supports: png, jpg, jpeg, gif, webp, bmp, tiff, svg)")
        print("  prompt      Optional description prompt (default: general description in English)")
        print("  model       Optional Ollama model name (default: gemma4:31b, env: VISION_MODEL)")
        sys.exit(1)

    img_path = sys.argv[1]
    user_prompt = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_PROMPT
    user_model = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_MODEL

    result = analyze_image(img_path, user_prompt, user_model)
    print(result)