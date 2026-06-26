#!/usr/bin/env python3
"""Gemini Image Generate - CLI for Star Office UI background generation.

Calls Google's Gemini API to generate images, with optional reference image
for style transfer / layout preservation.

Expected interface (called by Star Office UI backend):
  python gemini_image_generate.py \
    --prompt "..." \
    --model <model_name> \
    --out-dir /tmp/xxx \
    --cleanup \
    [--aspect-ratio 16:9] \
    [--reference-image /path/to/ref.webp]

Environment:
  GEMINI_API_KEY  - Google AI API key (required)
  GEMINI_MODEL    - override model name (optional, --model takes precedence)

Output (last line of stdout):
  {"files": ["/tmp/xxx/generated_0.png"]}
"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import tempfile
import shutil
from pathlib import Path

try:
    from google import genai
    from google.genai import types
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


def detect_mime(path: str) -> str:
    mt, _ = mimetypes.guess_type(path)
    if mt:
        return mt
    ext = os.path.splitext(path)[1].lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/png")


def main():
    parser = argparse.ArgumentParser(description="Generate image via Gemini API")
    parser.add_argument("--prompt", required=True, help="Generation prompt")
    parser.add_argument("--model", default="", help="Model name")
    parser.add_argument("--out-dir", required=True, help="Output directory")
    parser.add_argument("--cleanup", action="store_true", help="(ignored, kept for compat)")
    parser.add_argument("--aspect-ratio", default="", help="Aspect ratio hint (e.g. 16:9)")
    parser.add_argument("--reference-image", default="", help="Reference image path")
    args = parser.parse_args()

    # Resolve API key
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        api_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if not api_key:
        print("ERROR: GEMINI_API_KEY or GOOGLE_API_KEY not set", file=sys.stderr)
        sys.exit(1)

    # Resolve model - env var GEMINI_MODEL overrides --model flag
    model = os.environ.get("GEMINI_MODEL", "").strip() or args.model.strip()
    if not model:
        model = "gemini-2.0-flash-exp"

    # Ensure output directory
    out_dir = args.out_dir
    os.makedirs(out_dir, exist_ok=True)

    if not HAS_GENAI:
        print("ERROR: google-genai package not installed", file=sys.stderr)
        sys.exit(1)

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Build prompt parts
    contents = []

    # Add reference image if provided
    if args.reference_image and os.path.exists(args.reference_image):
        ref_path = args.reference_image
        mime = detect_mime(ref_path)
        with open(ref_path, "rb") as f:
            ref_data = f.read()
        contents.append(
            types.Part.from_bytes(data=ref_data, mime_type=mime)
        )

    # Add text prompt
    prompt_text = args.prompt
    if args.aspect_ratio:
        prompt_text += f"\nTarget aspect ratio: {args.aspect_ratio}."
    contents.append(prompt_text)

    # Configure generation
    generate_config = types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_config,
        )
    except Exception as e:
        err_msg = str(e)
        print(f"ERROR: {err_msg}", file=sys.stderr)
        sys.exit(1)

    # Extract generated images
    output_files = []
    idx = 0

    if response.candidates:
        for candidate in response.candidates:
            if not candidate.content or not candidate.content.parts:
                continue
            for part in candidate.content.parts:
                if part.inline_data and part.inline_data.mime_type and part.inline_data.mime_type.startswith("image/"):
                    # Determine extension from mime
                    mime = part.inline_data.mime_type
                    ext_map = {
                        "image/png": ".png",
                        "image/jpeg": ".jpg",
                        "image/webp": ".webp",
                    }
                    ext = ext_map.get(mime, ".png")
                    out_path = os.path.join(out_dir, f"generated_{idx}{ext}")
                    with open(out_path, "wb") as f:
                        f.write(part.inline_data.data)
                    output_files.append(out_path)
                    idx += 1

    if not output_files:
        # Check if there's text response with error info
        text_parts = []
        if response.candidates:
            for candidate in response.candidates:
                if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if part.text:
                            text_parts.append(part.text)
        if text_parts:
            print(f"ERROR: No image generated. Model response: {' '.join(text_parts)[:500]}", file=sys.stderr)
        else:
            print("ERROR: No image generated and no text response", file=sys.stderr)
        sys.exit(1)

    # Output result as JSON (backend reads the last line)
    result = {"files": output_files}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
