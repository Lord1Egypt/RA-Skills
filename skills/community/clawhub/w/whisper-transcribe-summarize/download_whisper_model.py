#!/usr/bin/env python3
import argparse
import os
import sys

try:
    import whisper
except ImportError as exc:
    raise SystemExit(
        "未安装 openai-whisper。请先运行: python3 -m pip install -U openai-whisper"
    ) from exc


def default_cache_dir(download_dir: str | None) -> str:
    if download_dir:
        return os.path.abspath(os.path.expanduser(download_dir))
    return os.path.join(os.path.expanduser("~"), ".cache", "whisper")


def main() -> None:
    parser = argparse.ArgumentParser(description="下载 Whisper 模型到本地缓存")
    parser.add_argument(
        "model",
        choices=["tiny", "base", "small", "medium", "large"],
        help="要下载的 Whisper 模型名",
    )
    parser.add_argument(
        "--download-dir",
        default=None,
        help="自定义下载目录；默认使用 ~/.cache/whisper",
    )
    args = parser.parse_args()

    cache_dir = default_cache_dir(args.download_dir)
    os.makedirs(cache_dir, exist_ok=True)

    print(f"开始下载模型: {args.model}")
    print(f"下载目录: {cache_dir}")

    whisper.load_model(args.model, download_root=cache_dir)

    print("完成")
    print("模型:", args.model)
    print("缓存目录:", cache_dir)


if __name__ == "__main__":
    main()
