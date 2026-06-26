#!/usr/bin/env python3
"""
ZenMux Image Generation Script
Supports aspectRatio and imageSize parameters via imageConfig
Usage: python generate_image.py "<prompt>" [output_path] [options]
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
import socket
from pathlib import Path

# Constants
API_TIMEOUT = 300  # seconds (5 minutes)
MAX_IMAGE_SIZE_MB = 20


def parse_args():
    parser = argparse.ArgumentParser(description='Generate images using ZenMux REST API')
    parser.add_argument('prompt', help='Image generation prompt')
    parser.add_argument('output', nargs='?', default='generated_image.png', help='Output file path')
    parser.add_argument('--api-key', default=os.environ.get('ZENMUX_API_KEY'), help='ZenMux API key')
    parser.add_argument('--model', default='google/gemini-3.1-flash-image-preview',
                       help='Model (default: google/gemini-3.1-flash-image-preview)')
    parser.add_argument('--input-image', help='Input image for image-to-image generation')
    parser.add_argument('--temperature', type=float, default=1.0, help='Randomness (0.0-2.0)')
    parser.add_argument('--max-tokens', type=int, help='Max output tokens')
    parser.add_argument('--aspect-ratio', choices=['1:1', '2:3', '3:2', '3:4', '4:3', '9:16', '16:9', '21:9'],
                       help='Image aspect ratio')
    parser.add_argument('--image-size', choices=['1K', '2K', '4K'], help='Image size (default: 1K)')
    return parser.parse_args()


def validate_api_key(api_key):
    if not api_key:
        print("Error: API key required. Set ZENMUX_API_KEY environment variable or use --api-key")
        print("\nTo set up:")
        print("  export ZENMUX_API_KEY=\"sk-...\"")
        sys.exit(1)

    if not api_key.startswith(('sk-', 'zenmux-')):
        print(f"Warning: API key format looks unusual. Expected to start with 'sk-' or 'zenmux-'")


def validate_input_image(input_image_path):
    if not os.path.exists(input_image_path):
        print(f"Error: Input image not found: {input_image_path}")
        sys.exit(1)

    file_size_mb = os.path.getsize(input_image_path) / (1024 * 1024)
    if file_size_mb > MAX_IMAGE_SIZE_MB:
        print(f"Error: Input image too large ({file_size_mb:.1f} MB). Maximum size is {MAX_IMAGE_SIZE_MB} MB.")
        sys.exit(1)

    valid_extensions = {'.jpg', '.jpeg', '.png', '.webp', '.gif'}
    ext = Path(input_image_path).suffix.lower()
    if ext not in valid_extensions:
        print(f"Error: Unsupported image format '{ext}'. Supported: {', '.join(valid_extensions)}")
        sys.exit(1)


def encode_image(input_image_path):
    validate_input_image(input_image_path)

    try:
        with open(input_image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()
    except (IOError, OSError) as e:
        print(f"Error: Failed to read input image: {e}")
        sys.exit(1)

    ext = input_image_path.split('.')[-1].lower()
    mime_type = {'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'png': 'image/png',
                 'webp': 'image/webp', 'gif': 'image/gif'}.get(ext, 'image/png')

    return {"inlineData": {"mimeType": mime_type, "data": image_data}}


def ensure_output_dir(output_path):
    output_dir = os.path.dirname(os.path.abspath(output_path))
    if output_dir and not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
            print(f"Created output directory: {output_dir}")
        except OSError as e:
            print(f"Error: Failed to create output directory '{output_dir}': {e}")
            sys.exit(1)


def get_unique_output_path(output_path):
    """Generate a unique output path if file already exists."""
    if not os.path.exists(output_path):
        return output_path

    # Split path into base name and extension
    path = Path(output_path)
    base_name = path.stem
    suffix = path.suffix
    parent_dir = path.parent

    # Find next available number
    counter = 1
    while True:
        new_name = f"{base_name}_{counter}{suffix}"
        new_path = parent_dir / new_name
        if not new_path.exists():
            print(f"Note: '{output_path}' already exists, saving to '{new_name}' instead")
            return str(new_path)
        counter += 1
        # Safety limit
        if counter > 1000:
            print(f"Warning: Too many files with similar names, using '{new_name}'")
            return str(new_path)


def build_request_body(args):
    parts = [{"text": args.prompt}]
    if args.input_image:
        parts.append(encode_image(args.input_image))

    generation_config = {
        "responseModalities": ["TEXT", "IMAGE"],
        "temperature": args.temperature
    }
    if args.max_tokens:
        generation_config["maxOutputTokens"] = args.max_tokens

    if args.aspect_ratio or args.image_size:
        generation_config["imageConfig"] = {}
        if args.aspect_ratio:
            generation_config["imageConfig"]["aspectRatio"] = args.aspect_ratio
        if args.image_size:
            generation_config["imageConfig"]["imageSize"] = args.image_size

    return {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": generation_config
    }


def parse_error_response(error_body, status_code):
    """Parse API error response and return user-friendly message."""
    try:
        error_data = json.loads(error_body)
        if 'error' in error_data:
            error_info = error_data['error']
            if 'message' in error_info:
                return f"API Error ({status_code}): {error_info['message']}"
            if 'code' in error_info:
                return f"API Error ({status_code}): {error_info['code']}"
    except json.JSONDecodeError:
        pass

    # Common HTTP status codes
    status_messages = {
        400: "Bad Request - Invalid parameters or malformed request",
        401: "Unauthorized - Invalid or expired API key",
        403: "Forbidden - Insufficient permissions",
        429: "Rate Limited - Too many requests, please wait and retry",
        500: "Internal Server Error - API service issue",
        502: "Bad Gateway - API service temporarily unavailable",
        503: "Service Unavailable - API service is down for maintenance"
    }

    return f"HTTP Error {status_code}: {status_messages.get(status_code, error_body[:200])}"


def make_api_request(url, request_body, api_key):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(request_body).encode('utf-8'),
        headers=headers,
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=API_TIMEOUT) as response:
            return json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(parse_error_response(error_body, e.code))
        sys.exit(1)
    except urllib.error.URLError as e:
        if isinstance(e.reason, socket.timeout):
            print(f"Error: Request timed out after {API_TIMEOUT} seconds. The API may be slow or unavailable.")
        elif isinstance(e.reason, socket.gaierror):
            print("Error: Network error - Could not resolve API host. Check your internet connection.")
        else:
            print(f"Error: Network error - {e.reason}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Failed to parse API response as JSON: {e}")
        sys.exit(1)
    except socket.timeout:
        print(f"Error: Request timed out after {API_TIMEOUT} seconds.")
        sys.exit(1)


def extract_and_save_image(result, output_path):
    if 'candidates' not in result or not result['candidates']:
        print("Warning: No candidates in response")
        if 'promptFeedback' in result:
            print(f"Prompt feedback: {result['promptFeedback']}")
        return False

    candidate = result['candidates'][0]

    if 'content' not in candidate or 'parts' not in candidate['content']:
        print("Warning: No content parts in response")
        return False

    image_found = False
    for part in candidate['content']['parts']:
        if 'text' in part:
            print(f"\nModel response: {part['text'][:200]}...")
        if 'inlineData' in part:
            try:
                image_bytes = base64.b64decode(part['inlineData']['data'])
                with open(output_path, 'wb') as f:
                    f.write(image_bytes)
                print(f"\nImage saved: {output_path}")
                print(f"File size: {len(image_bytes) / 1024:.2f} KB")
                image_found = True
            except Exception as e:
                print(f"Error: Failed to save image: {e}")
                return False

    return image_found


def main():
    args = parse_args()

    validate_api_key(args.api_key)

    ensure_output_dir(args.output)

    # Ensure unique output path to avoid overwriting
    args.output = get_unique_output_path(args.output)

    request_body = build_request_body(args)

    # Parse model to get provider and model name
    model_parts = args.model.split('/', 1)
    if len(model_parts) == 2:
        provider, model_name = model_parts
    else:
        provider = "google"
        model_name = args.model

    url = f"https://zenmux.ai/api/vertex-ai/v1/publishers/{provider}/models/{model_name}:generateContent"

    print(f"Generating image...")
    print(f"Prompt: {args.prompt}")
    print(f"Model: {args.model}")
    if args.input_image:
        print(f"Input image: {args.input_image}")
    if args.aspect_ratio:
        print(f"Aspect ratio: {args.aspect_ratio}")
    if args.image_size:
        print(f"Image size: {args.image_size}")
    print()

    result = make_api_request(url, request_body, args.api_key)

    if not extract_and_save_image(result, args.output):
        print("Warning: No image data in response")
        print(f"Response: {json.dumps(result, indent=2)[:500]}")
        sys.exit(1)


if __name__ == "__main__":
    main()
