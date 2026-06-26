# -*- coding: utf-8 -*-
"""
腾讯云 VITA 图像/视频理解 CLI

支持：
  - 单图片或多图片 URL / 本地图片理解
  - 单视频 URL 理解
  - 自定义 prompt 指令
  - 流式与非流式输出
"""

import base64
import json
import os
import sys
import argparse

try:
    import openai
except ImportError:
    print(
        json.dumps({
            "error": "DEPENDENCY_MISSING",
            "message": "The 'openai' package is required but not installed.",
            "guide": "Please install it manually: pip install openai",
        }, ensure_ascii=False, indent=2)
    )
    sys.exit(1)


VITA_BASE_URL = "https://api.vita.cloud.tencent.com/v1/video2text"
VITA_MODEL = "youtu-vita"

SUPPORTED_IMAGE_FORMATS = {"jpg", "jpeg", "png", "svg", "webp"}
SUPPORTED_VIDEO_FORMATS = {"mp4", "mov", "avi", "webm"}
IMAGE_MIME_TYPES = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "svg": "image/svg+xml",
    "webp": "image/webp",
}

DEFAULT_PROMPT = "请描述这段媒体内容"
PROMPT_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "prompt", "vita_prompt.txt")


def load_persisted_prompt():
    """Load the user-persisted prompt from <SKILL_DIR>/prompt/vita_prompt.txt.
    Returns None if the file does not exist or is empty."""
    try:
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else None
    except (FileNotFoundError, OSError):
        return None


def resolve_prompt(cli_prompt_raw, cli_prompt_was_set):
    """Resolve prompt by priority: CLI arg > persisted file > default.

    Args:
        cli_prompt_raw: The value of the --prompt argument.
        cli_prompt_was_set: Whether the user explicitly passed --prompt.
    Returns:
        The resolved prompt string.
    """
    # Priority 1: explicit --prompt flag
    if cli_prompt_was_set:
        return cli_prompt_raw

    # Priority 2: persisted prompt file
    persisted = load_persisted_prompt()
    if persisted:
        return persisted

    # Priority 3: default
    return DEFAULT_PROMPT


def get_api_key():
    api_key = os.getenv("TENCENTCLOUD_VITA_API_KEY")
    if not api_key:
        error_msg = {
            "error": "API_KEY_NOT_CONFIGURED",
            "message": (
                "VITA API key not found in environment variables. "
                "Please set TENCENTCLOUD_VITA_API_KEY."
            ),
            "guide": {
                "step1": "登录图像分析与处理控制台: https://console.cloud.tencent.com/",
                "step2": "单击 VITA 图像理解 --> 服务管理，创建 API KEY",
                "step3_linux": 'export TENCENTCLOUD_VITA_API_KEY="your_api_key"',
                "step3_windows": '$env:TENCENTCLOUD_VITA_API_KEY="your_api_key"',
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)
    return api_key


def build_client(api_key):
    return openai.OpenAI(
        api_key=api_key,
        base_url=VITA_BASE_URL,
    )


def is_http_url(value):
    return value.startswith(("http://", "https://"))


def get_file_extension(path):
    lower = path.lower().split("?", 1)[0]
    return lower.rsplit(".", 1)[-1] if "." in lower else ""


def encode_local_image_to_data_url(path):
    resolved_path = os.path.abspath(os.path.expanduser(path))

    if not os.path.isfile(resolved_path):
        print(json.dumps({
            "error": "LOCAL_IMAGE_NOT_FOUND",
            "message": f"Local image file not found: {path}",
            "guide": "Please provide an existing local image path or a public image URL.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    ext = get_file_extension(resolved_path)
    if ext not in SUPPORTED_IMAGE_FORMATS:
        print(json.dumps({
            "error": "UNSUPPORTED_LOCAL_IMAGE_FORMAT",
            "message": (
                f"Unsupported local image format: .{ext or 'unknown'}. "
                "Supported formats: jpg, jpeg, png, svg, webp."
            ),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    try:
        with open(resolved_path, "rb") as f:
            encoded = base64.b64encode(f.read()).decode("ascii")
    except OSError as err:
        print(json.dumps({
            "error": "LOCAL_IMAGE_READ_ERROR",
            "message": f"Failed to read local image file: {err}",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return f"data:{IMAGE_MIME_TYPES[ext]};base64,{encoded}"


def normalize_media_item(item):
    media_type = item.get("type")
    source = item.get("url") or item.get("path")

    if media_type not in {"image", "video"}:
        print(json.dumps({
            "error": "INVALID_MEDIA_TYPE",
            "message": f"Unsupported media type: {media_type}",
            "guide": "Each media item must use type 'image' or 'video'.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if not source:
        print(json.dumps({
            "error": "MISSING_MEDIA_SOURCE",
            "message": "Each media item must provide 'url' or 'path'.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if media_type == "image":
        if is_http_url(source):
            return {"type": "image", "url": source}
        return {"type": "image", "url": encode_local_image_to_data_url(source)}

    if is_http_url(source):
        return {"type": "video", "url": source}

    print(json.dumps({
        "error": "LOCAL_VIDEO_NOT_SUPPORTED",
        "message": "Local video paths are not supported directly by this script.",
        "guide": (
            "Please upload the local video with a separate COS/upload tool first, "
            "then pass the resulting public or pre-signed URL to --video."
        ),
    }, ensure_ascii=False, indent=2))
    sys.exit(1)


def normalize_media_list(media_list):
    return [normalize_media_item(item) for item in media_list]


def guess_media_type(url):
    """Guess media type (image/video) from URL extension."""
    lower = url.lower().split("?")[0]
    ext = lower.rsplit(".", 1)[-1] if "." in lower else ""
    if ext in SUPPORTED_IMAGE_FORMATS:
        return "image"
    if ext in SUPPORTED_VIDEO_FORMATS:
        return "video"
    return None


def build_content(media_inputs, prompt):
    """
    Build the content array for the API request.

    media_inputs: list of dicts, each with keys:
        - "type": "image" or "video"
        - "url": the remote URL or image data URL
    prompt: str, the instruction text
    """
    content = []

    for item in media_inputs:
        media_type = item["type"]
        url = item["url"]
        if media_type == "image":
            content.append({
                "type": "image_url",
                "image_url": {"url": url},
            })
        elif media_type == "video":
            content.append({
                "type": "video_url",
                "video_url": {"url": url},
            })

    content.append({
        "type": "text",
        "text": prompt,
    })

    return content


def call_vita(client, content, stream=False, temperature=None, max_tokens=None):
    """Call the VITA API."""
    kwargs = {
        "model": VITA_MODEL,
        "messages": [
            {
                "role": "user",
                "content": content,
            }
        ],
        "stream": stream,
    }
    if temperature is not None:
        kwargs["temperature"] = temperature
    if max_tokens is not None:
        kwargs["max_tokens"] = max_tokens

    return client.chat.completions.create(**kwargs)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud VITA Image/Video Understanding CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 图片理解
  python main.py --image "https://example.com/image.jpg" --prompt "描述这张图片"

  # 本地图片理解（自动转为 base64 data URL）
  python main.py --image "./image.png" --prompt "描述这张图片"

  # 多图片理解（时序分析）
  python main.py --image "https://example.com/1.jpg" --image "https://example.com/2.jpg" --prompt "分析这些图片的变化"

  # 视频理解
  python main.py --video "https://example.com/video.mp4" --prompt "总结视频内容"

  # 流式输出
  python main.py --video "https://example.com/video.mp4" --prompt "描述视频" --stream

  # 从 stdin 读取 JSON 输入
  echo '{"media":[{"type":"video","url":"https://..."}],"prompt":"..."}' | python main.py --stdin
        """,
    )

    parser.add_argument(
        "--image", dest="images", metavar="URL_OR_PATH", action="append",
        help="Image URL or local image path (can be specified multiple times for multi-image input)",
    )
    parser.add_argument(
        "--video", dest="video", metavar="URL",
        help="Public video URL only (local video paths are not supported directly)",
    )
    parser.add_argument(
        "--prompt", default=None,
        help='Prompt/instruction for analysis (priority: CLI > persisted file > default)',
    )
    parser.add_argument(
        "--stream", action="store_true",
        help="Enable streaming output (SSE)",
    )
    parser.add_argument(
        "--temperature", type=float, default=None,
        help="Sampling temperature (0.0-1.0, higher=more random)",
    )
    parser.add_argument(
        "--max-tokens", type=int, default=None,
        help="Maximum number of output tokens",
    )
    parser.add_argument(
        "--stdin", action="store_true",
        help="Read JSON input from stdin instead of CLI arguments",
    )

    args = parser.parse_args()

    # --- stdin mode ---
    if args.stdin:
        raw = sys.stdin.read().strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            print(json.dumps({
                "error": "INVALID_STDIN_JSON",
                "message": f"Failed to parse stdin as JSON: {e}",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        media_list = data.get("media", [])
        raw_prompt = data.get("prompt")
        prompt = resolve_prompt(raw_prompt, raw_prompt is not None)
        stream = data.get("stream", False)
        temperature = data.get("temperature")
        max_tokens = data.get("max_tokens")

        if not media_list:
            print(json.dumps({
                "error": "NO_MEDIA_INPUT",
                "message": "stdin JSON must contain 'media' field with at least one item.",
                "example": '{"media":[{"type":"image","url":"https://..."}],"prompt":"..."}',
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        media_list = normalize_media_list(media_list)
        return media_list, prompt, stream, temperature, max_tokens

    # --- CLI mode ---
    media_list = []

    if args.images and args.video:
        print(json.dumps({
            "error": "CONFLICTING_INPUT",
            "message": "Cannot specify both --image and --video in the same request.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    if args.images:
        for url in args.images:
            media_list.append({"type": "image", "url": url})
    elif args.video:
        media_list.append({"type": "video", "url": args.video})
    else:
        print(json.dumps({
            "error": "NO_MEDIA_INPUT",
            "message": "Please provide at least one --image URL/path or a --video URL.",
            "usage": {
                "image": 'python main.py --image "https://example.com/image.jpg" --prompt "描述图片"',
                "local_image": 'python main.py --image "./image.png" --prompt "描述图片"',
                "video": 'python main.py --video "https://example.com/video.mp4" --prompt "总结视频"',
                "multi_image": 'python main.py --image "https://.../1.jpg" --image "https://.../2.jpg" --prompt "分析变化"',
                "stdin": 'echo \'{"media":[{"type":"video","url":"https://..."}],"prompt":"..."}\' | python main.py --stdin',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    prompt = resolve_prompt(args.prompt, args.prompt is not None)

    media_list = normalize_media_list(media_list)
    return media_list, prompt, args.stream, args.temperature, args.max_tokens


def handle_stream_response(response):
    """Handle streaming SSE response and print incremental text."""
    full_text = ""
    for chunk in response:
        delta = chunk.choices[0].delta if chunk.choices else None
        if delta and delta.content:
            print(delta.content, end="", flush=True)
            full_text += delta.content
    print()  # newline after stream ends
    return full_text


def main():
    media_list, prompt, stream, temperature, max_tokens = parse_args()
    api_key = get_api_key()
    client = build_client(api_key)

    content = build_content(media_list, prompt)

    try:
        if stream:
            response = call_vita(client, content, stream=True,
                                 temperature=temperature, max_tokens=max_tokens)
            handle_stream_response(response)
        else:
            response = call_vita(client, content, stream=False,
                                 temperature=temperature, max_tokens=max_tokens)
            message = response.choices[0].message.content if response.choices else ""
            usage = response.usage

            result = {
                "result": message,
            }
            if usage:
                result["usage"] = {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens,
                }

            print(json.dumps(result, ensure_ascii=False, indent=2))

    except openai.AuthenticationError as err:
        print(json.dumps({
            "error": "AUTHENTICATION_ERROR",
            "message": f"Invalid API key: {err}",
            "guide": "Please check your TENCENTCLOUD_VITA_API_KEY environment variable.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    except openai.RateLimitError as err:
        print(json.dumps({
            "error": "RATE_LIMIT_ERROR",
            "message": f"Rate limit exceeded (default: 5 concurrent): {err}",
            "guide": "VITA default concurrency is 5. Please retry after a moment.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    except openai.BadRequestError as err:
        print(json.dumps({
            "error": "BAD_REQUEST",
            "message": str(err),
            "guide": "Check media URL accessibility, local image format, and video URL requirements.",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    except openai.APIError as err:
        print(json.dumps({
            "error": "API_ERROR",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    except Exception as err:
        print(json.dumps({
            "error": "UNEXPECTED_ERROR",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
