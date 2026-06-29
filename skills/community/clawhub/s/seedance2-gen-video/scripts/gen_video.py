#!/usr/bin/env python3
"""
Seedance 2.0 Video Generation Script

Usage:
    python3 gen_video.py --prompt "prompt text" [options]

Dependencies:
    pip install 'volcengine-python-sdk[ark]'
"""

import os
import sys
import time
import argparse


def load_dotenv():
    """Load environment variables from .env file (script directory first, then parent directory). Does not override existing environment variables."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(script_dir, ".env"),
        os.path.join(script_dir, "..", ".env"),
    ]
    for path in candidates:
        path = os.path.normpath(path)
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            break


def parse_args():
    parser = argparse.ArgumentParser(description="Seedance 2.0 Video Generation Script")
    parser.add_argument("--prompt", required=True, help="Text prompt")
    parser.add_argument(
        "--model",
        default="doubao-seedance-2-0-260128",
        choices=["doubao-seedance-2-0-260128", "doubao-seedance-2-0-fast-260128"],
        help="Model ID (default: doubao-seedance-2-0-260128)",
    )
    parser.add_argument(
        "--ratio",
        default="16:9",
        choices=["16:9", "9:16", "1:1", "4:3", "3:4", "21:9", "adaptive"],
        help="Output video aspect ratio (default: 16:9)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=5,
        help="Output video duration in seconds (4~15, default: 5)",
    )
    parser.add_argument(
        "--generate-audio",
        action="store_true",
        help="Whether to generate video with audio",
    )
    parser.add_argument(
        "--watermark",
        action="store_true",
        help="Whether to add a watermark",
    )
    parser.add_argument(
        "--images",
        nargs="*",
        default=[],
        help="Reference image URL list (up to 9)",
    )
    parser.add_argument(
        "--image-roles",
        nargs="*",
        default=[],
        help="Image role list, corresponding one-to-one with --images (reference_image / first_frame / last_frame)",
    )
    parser.add_argument(
        "--videos",
        nargs="*",
        default=[],
        help="Reference video URL list (up to 3)",
    )
    parser.add_argument(
        "--audios",
        nargs="*",
        default=[],
        help="Reference audio URL list (up to 3)",
    )
    parser.add_argument(
        "--web-search",
        action="store_true",
        help="Whether to enable web search (only effective for plain text input)",
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=30,
        help="Polling interval in seconds (default: 30)",
    )
    return parser.parse_args()


def validate_args(args):
    if not (4 <= args.duration <= 15):
        print(f"Error: Duration must be between 4~15 seconds, current value: {args.duration}", file=sys.stderr)
        sys.exit(1)

    if len(args.images) > 9:
        print(f"Error: Up to 9 reference images allowed, current: {len(args.images)}", file=sys.stderr)
        sys.exit(1)

    if len(args.videos) > 3:
        print(f"Error: Up to 3 reference videos allowed, current: {len(args.videos)}", file=sys.stderr)
        sys.exit(1)

    if len(args.audios) > 3:
        print(f"Error: Up to 3 reference audio clips allowed, current: {len(args.audios)}", file=sys.stderr)
        sys.exit(1)

    if args.image_roles and len(args.image_roles) != len(args.images):
        print(
            f"Error: --image-roles count ({len(args.image_roles)}) must match --images count ({len(args.images)})",
            file=sys.stderr,
        )
        sys.exit(1)

    valid_roles = {"reference_image", "first_frame", "last_frame"}
    for role in args.image_roles:
        if role not in valid_roles:
            print(f"Error: Invalid image role '{role}', valid values: {valid_roles}", file=sys.stderr)
            sys.exit(1)

    # Check unsupported input combinations
    has_only_audio = len(args.audios) > 0 and len(args.images) == 0 and len(args.videos) == 0
    if has_only_audio:
        print("Error: Audio-only input is not supported, please also provide a text prompt (already included) or images/videos", file=sys.stderr)
        sys.exit(1)


def build_content(args):
    content = [{"type": "text", "text": args.prompt}]

    image_roles = args.image_roles if args.image_roles else ["reference_image"] * len(args.images)
    for url, role in zip(args.images, image_roles):
        content.append({
            "type": "image_url",
            "image_url": {"url": url},
            "role": role,
        })

    for url in args.videos:
        content.append({
            "type": "video_url",
            "video_url": {"url": url},
            "role": "reference_video",
        })

    for url in args.audios:
        content.append({
            "type": "audio_url",
            "audio_url": {"url": url},
            "role": "reference_audio",
        })

    return content


def main():
    load_dotenv()
    args = parse_args()
    validate_args(args)

    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("Error: ARK_API_KEY is not set, please configure it in the .env file or as an environment variable:", file=sys.stderr)
        print("  ARK_API_KEY=your_api_key", file=sys.stderr)
        sys.exit(1)

    try:
        from volcenginesdkarkruntime import Ark
    except ImportError:
        print("Error: volcengine-python-sdk is not installed, please run:", file=sys.stderr)
        print("  pip install 'volcengine-python-sdk[ark]'", file=sys.stderr)
        sys.exit(1)

    client = Ark(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key,
    )

    content = build_content(args)

    create_kwargs = {
        "model": args.model,
        "content": content,
        "ratio": args.ratio,
        "duration": args.duration,
        "watermark": args.watermark,
    }

    if args.generate_audio:
        create_kwargs["generate_audio"] = True

    if args.web_search:
        create_kwargs["tools"] = [{"type": "web_search"}]

    print("----- Creating video generation task -----")
    print(f"Model: {args.model}")
    print(f"Prompt: {args.prompt}")
    print(f"Aspect Ratio: {args.ratio} | Duration: {args.duration}s | Audio: {args.generate_audio}")
    if args.images:
        image_roles = args.image_roles if args.image_roles else ["reference_image"] * len(args.images)
        for i, (url, role) in enumerate(zip(args.images, image_roles), 1):
            print(f"Image {i} ({role}): {url}")
    if args.videos:
        for i, url in enumerate(args.videos, 1):
            print(f"Video {i}: {url}")
    if args.audios:
        for i, url in enumerate(args.audios, 1):
            print(f"Audio {i}: {url}")
    if args.web_search:
        print("Web search enabled")
    print()

    try:
        create_result = client.content_generation.tasks.create(**create_kwargs)
    except Exception as e:
        print(f"Failed to create task: {e}", file=sys.stderr)
        sys.exit(1)

    task_id = create_result.id
    print(f"Task created, ID: {task_id}")
    print()

    print("----- Polling task status -----")
    while True:
        try:
            get_result = client.content_generation.tasks.get(task_id=task_id)
        except Exception as e:
            print(f"Failed to query task status: {e}", file=sys.stderr)
            sys.exit(1)

        status = get_result.status
        if status == "succeeded":
            print("----- Task succeeded -----")
            video_url = get_result.content.video_url if hasattr(get_result, "content") and get_result.content else None
            if video_url:
                print(f"Video URL: {video_url}")
            else:
                print(get_result)
            print()
            print("Note: The video URL is valid for only 24 hours. Please download and save it promptly.")
            break
        elif status == "failed":
            print("----- Task failed -----")
            error_msg = get_result.error if hasattr(get_result, "error") else "Unknown error"
            print(f"Error message: {error_msg}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"Current status: {status}, retrying in {args.poll_interval} seconds...")
            time.sleep(args.poll_interval)


if __name__ == "__main__":
    main()
