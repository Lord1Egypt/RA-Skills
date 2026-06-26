#!/usr/bin/env python3
"""
Doubao / Seedance Video Generation - 豆包视频生成

使用火山方舟 content_generation.tasks 接口生成视频，并在成功后下载 mp4 到本地。
"""

import argparse
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

from volcenginesdkarkruntime import Ark

SUPPORTED_MODELS = {
    "doubao-seedance-1-5-pro-251215": "Seedance 1.5 Pro 视频生成",
}
MODEL_ALIASES = {
    "seedance-1.5-pro": "doubao-seedance-1-5-pro-251215",
    "seedance15pro": "doubao-seedance-1-5-pro-251215",
}
DEFAULT_MODEL = os.environ.get("DOUBAO_VIDEO_MODEL", "doubao-seedance-1-5-pro-251215")


def load_env_file(path: str) -> None:
    env_path = Path(path)
    if not env_path.exists():
        return
    for line in env_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


def resolve_model(model: str | None) -> str:
    selected = (model or DEFAULT_MODEL).strip()
    return MODEL_ALIASES.get(selected, selected)


def sanitize_filename(name: str, default_stem: str = "video") -> str:
    base = os.path.basename(name or "")
    stem, ext = os.path.splitext(base)
    stem = re.sub(r"[^A-Za-z0-9._-]+", "-", stem).strip("-._")
    stem = stem[:80] or default_stem
    ext = ext.lower() if ext.lower() in {".mp4", ".mov", ".webm"} else ".mp4"
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
        raise ValueError(f"Unsupported video URL scheme: {parsed.scheme or 'empty'}")
    if not parsed.netloc:
        raise ValueError("Video URL is missing host")
    return url


def generate_filename(prompt: str) -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    words = prompt.split()[:5]
    raw_name = "-".join(words).replace(",", "").replace("，", "")[:60]
    safe_name = sanitize_filename(raw_name, default_stem="video")
    stem, ext = os.path.splitext(safe_name)
    return f"{timestamp}-{stem}{ext}"


def download_video(url: str, filepath: str) -> None:
    safe_url = validate_download_url(url)
    safe_path = ensure_safe_output_path(filepath)
    request = Request(safe_url, headers={"User-Agent": "OpenClaw-SeedanceVideo/1.0"})
    with urlopen(request, timeout=180) as response:
        content_type = (response.headers.get("Content-Type") or "").lower()
        if not content_type.startswith("video/"):
            raise ValueError(f"Downloaded content is not a video: {content_type or 'unknown'}")
        Path(safe_path).write_bytes(response.read())
    print(f"✓ Video saved to: {safe_path}")


def main() -> None:
    load_env_file("/root/.openclaw/workspace/.env")

    parser = argparse.ArgumentParser(description="豆包视频生成 - 使用火山方舟 Seedance 生成视频")
    parser.add_argument("--prompt", "-p", required=True, help="视频描述/提示词")
    parser.add_argument("--filename", "-f", help="输出文件名 (默认自动生成)")
    parser.add_argument("--model", "-m", default=DEFAULT_MODEL, help="视频模型名称")
    parser.add_argument("--duration", type=int, default=5, help="视频时长（秒）")
    parser.add_argument("--resolution", default="720p", help="分辨率，例如 480p/720p/1080p")
    parser.add_argument("--ratio", default="16:9", help="画幅比例，例如 16:9 / 9:16 / 1:1")
    parser.add_argument("--camera-fixed", action="store_true", help="固定机位")
    parser.add_argument("--no-audio", action="store_true", help="不生成音频")
    parser.add_argument("--watermark", action="store_true", help="添加水印")
    parser.add_argument("--poll-interval", type=int, default=5, help="轮询间隔秒数")
    parser.add_argument("--timeout", type=int, default=300, help="最长等待秒数")
    args = parser.parse_args()

    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        print("Error: No API key provided. Please set ARK_API_KEY in environment or .env")
        sys.exit(1)

    model = resolve_model(args.model)
    if model not in SUPPORTED_MODELS:
        print("Warning: model is not in the local supported-video list; sending as-is.")

    output_file = ensure_safe_output_path(args.filename) if args.filename else generate_filename(args.prompt)

    print("Creating video task...")
    print(f"  Prompt: {args.prompt[:80]}...")
    print(f"  Model: {model}")
    print(f"  Duration: {args.duration}s")
    print(f"  Resolution: {args.resolution}")
    print(f"  Ratio: {args.ratio}")

    client = Ark(api_key=api_key)
    task = client.content_generation.tasks.create(
        model=model,
        content=[{"type": "text", "text": args.prompt}],
        duration=args.duration,
        resolution=args.resolution,
        ratio=args.ratio,
        camera_fixed=args.camera_fixed,
        generate_audio=not args.no_audio,
        watermark=args.watermark,
    )

    task_id = task.id
    print(f"✓ Task created: {task_id}")

    start = time.time()
    while True:
        current = client.content_generation.tasks.get(task_id=task_id)
        print(f"  Status: {current.status}")

        if current.status == "succeeded":
            video_url = current.content.video_url if current.content else None
            if not video_url:
                print("Error: task succeeded but no video_url returned")
                sys.exit(1)
            download_video(video_url, output_file)
            print("\n✅ Video generation completed")
            print(f"Task ID: {task_id}")
            print(f"Duration: {current.duration}s")
            print(f"Resolution: {current.resolution}")
            print(f"Ratio: {current.ratio}")
            break

        if current.status in {"failed", "cancelled"}:
            print(f"Error: task {current.status}")
            if current.error:
                print(current.error)
            sys.exit(1)

        if time.time() - start > args.timeout:
            print("Error: timed out while waiting for video generation")
            print(f"Task ID: {task_id}")
            sys.exit(2)

        time.sleep(args.poll_interval)


if __name__ == "__main__":
    main()
