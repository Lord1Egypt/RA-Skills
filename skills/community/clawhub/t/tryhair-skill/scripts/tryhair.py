#!/usr/bin/env python3
"""
tryhair OpenClaw Skill script - supports hairstyle try-on and face shape analysis
Supports:
- Local file
- Base64 image
- Image URL
"""

import os
import sys
import json
import base64
import argparse
import requests
import datetime
import io
import time

TRYHAIR_API = os.environ.get('OPENCLAW_TRYHAIR_API', 'https://tryhair.ai/api/tryhair')
FACESHAPE_API = os.environ.get('OPENCLAW_FACESHAPE_API', 'https://tryhair.ai/api/facial_analysis')


# =============================
# 🔥 NEW: unified image loader
# =============================
def load_image_input(args):
    # 1️⃣ Base64
    if args.image_base64:
        try:
            base64_str = args.image_base64

            if base64_str.startswith("data:image"):
                base64_str = base64_str.split(",")[1]

            image_data = base64.b64decode(base64_str)
            return io.BytesIO(image_data)

        except Exception as e:
            _error_exit(f'Invalid base64 image: {str(e)}')

    # 2️⃣ URL
    if args.image_url:
        try:
            response = requests.get(args.image_url, timeout=30)
            response.raise_for_status()
            return io.BytesIO(response.content)

        except Exception as e:
            _error_exit(f'Failed to download image: {str(e)}')

    # 3️⃣ local file
    if args.image:
        if not os.path.isfile(args.image):
            _error_exit(f'Image file does not exist: {args.image}')
        return open(args.image, 'rb')

    _error_exit('No image input provided')


def main():
    parser = argparse.ArgumentParser(description='AI Hairstyle & FaceShape Tool for OpenClaw')

    parser.add_argument('--action', default='tryhair', choices=['tryhair', 'faceshape'])

    parser.add_argument('--image', help='Path to image file')
    parser.add_argument('--image_base64', help='Base64 encoded image')
    parser.add_argument('--image_url', help='Image URL')

    parser.add_argument('--style', help='Hairstyle description (required for tryhair)')
    parser.add_argument('--uid', required=True)

    args = parser.parse_args()

    print("DEBUG INPUT:", args.image_base64 is not None, args.image_url is not None, file=sys.stderr)

    if args.action == 'tryhair':
        if not args.style:
            _error_exit('Missing --style parameter for tryhair action')
        _handle_tryhair(args)

    elif args.action == 'faceshape':
        _handle_faceshape(args)


last_request = {}

def is_duplicate(uid, style, window=30):
    key = f"{uid}:{style}"
    now = time.time()

    expired = [k for k, t in last_request.items() if now - t > window]
    for k in expired:
        del last_request[k]

    if key in last_request:
        return True

    last_request[key] = now
    return False


# =============================
# TryHair
# =============================
def _handle_tryhair(args):
    if is_duplicate(args.uid, args.style):
        print(json.dumps({
            'success': False,
            'error': 'Duplicate request ignored'
        }))
        sys.exit(0)

    image_file = load_image_input(args)

    files = {
        'facefile': ('image.jpg', image_file, 'image/jpeg')
    }

    data = {
        'hairstyle': args.style,
        'uid': args.uid
    }

    try:
        response = requests.post(
            TRYHAIR_API,
            files=files,
            data=data,
            timeout=180
        )

        result = response.json()
        _process_tryhair_response(result)

    except Exception as e:
        _error_exit(f'Request error: {str(e)}')

    finally:
        if hasattr(image_file, "close"):
            image_file.close()


# =============================
# FaceShape
# =============================
def _handle_faceshape(args):
    image_file = load_image_input(args)

    files = {
        'facefile': ('image.jpg', image_file, 'image/jpeg')
    }

    data = {'uid': args.uid}

    try:
        response = requests.post(
            FACESHAPE_API,
            files=files,
            data=data,
            timeout=120
        )

        result = response.json()
        _process_faceshape_response(result)

    except Exception as e:
        _error_exit(f'Request error: {str(e)}')

    finally:
        if hasattr(image_file, "close"):
            image_file.close()


def _process_tryhair_response(result):

    if result.get('status') == 'need_purchase':
        print(json.dumps({
            'success': False,
            'need_purchase': True,
            'message': result.get('message'),
            'redirect_url': result.get('redirect_url')
        }))
        sys.exit(0)

    if result.get('status') == 'error':
        _error_exit(result.get('message', 'Unknown error'))

    if result.get('status') == 'success':
        data = result['data']

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_style = data['hairstyle'].replace(" ", "_")

        os.makedirs("output", exist_ok=True)
        filepath = f"output/output_{safe_style}_{timestamp}.jpg"

        with open(filepath, 'wb') as f:
            f.write(base64.b64decode(data['image_base64']))

        style = data['hairstyle']
        credits = data['remaining_credits']

        message = "\n".join([
            f"✨ Your {style} hairstyle is ready!",
            "",
            "💇 Take a look above 👆",
            "",
            f"Credits remaining: {credits}",
            "",
            "Want to try another style?",
            f'👉 "try a shorter {style}"',
            '👉 "try a textured version"',
            '👉 "try something completely different"',
        ])

        print(json.dumps({
            'success': True,
            'image_path': filepath,
            'message': message,
            'style': style,
            'remaining_credits': credits
        }))

        sys.exit(0)

    _error_exit('Unexpected response format')

def _process_faceshape_response(result):
    analysis = result.get("analysis", {})
    ai = result.get("ai_recommendation", {})

    face_shape = analysis.get("Face Shape") or "N/A"
    face_ratio = analysis.get("Face Width : Cheek Width : Jaw Width : Face Length") or "N/A"
    five_eye = analysis.get("Right Eye Width : Inner Eye Width : Left Eye Width") or "N/A"
    three_court = analysis.get("Upper Face : Middle Face : Lower Face") or "N/A"

    output_lines = [
        "✨ Your Face Analysis",
        "",
        "Face Shape",
        face_shape,
        "",
        "Proportions",
        f"• Face Ratio: {face_ratio}",
        f"• Eye Balance: {five_eye}",
        f"• Vertical Balance: {three_court}",
    ]

    if isinstance(ai, dict):
        design = ai.get("design", "")
        hairstyles = ai.get("hairstyles", [])

        if isinstance(design, str) and design.strip():
            output_lines += [
                "",
                "💡 Design Strategy",
                design
            ]

        if isinstance(hairstyles, list) and hairstyles:
            output_lines += [
                "",
                "🔥 Recommended Hairstyles"
            ]
            for i, h in enumerate(hairstyles, 1):
                name = h.get("name", "")
                desc = h.get("description", "")

                if name:
                    output_lines.append(f"{i:02d}. {name}")
                    if desc:
                        output_lines.append(f"   {desc}")
                    output_lines.append(f"   🔄 Try this look → {name}")
                    output_lines.append("")

    formatted_text = "\n".join(output_lines)

    print(json.dumps({
        'success': True,
        'final': True,
        'formatted': formatted_text,
        'data': result
    }))

    sys.exit(0)


def _error_exit(error_msg, code=None):
    out = {'success': False, 'error': error_msg}
    if code:
        out['code'] = code
    print(json.dumps(out))
    sys.exit(1)


if __name__ == '__main__':
    main()
