# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json
from datetime import date
from mimetypes import guess_type
from pathlib import Path

from common import (
    build_private_download_url,
    build_public_url,
    load_config,
    resolve_access_mode,
    upload_file as _upload_file,
)

DEFAULT_EXPIRES_IN = 1800

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".bmp", ".svg", ".ico", ".tiff", ".tif", ".avif"}
VIDEO_EXTS = {".mp4", ".webm", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".m4v", ".ts", ".3gp"}
AUDIO_EXTS = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a", ".wma", ".opus", ".ape"}


def classify_media(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix in IMAGE_EXTS:
        return "images"
    if suffix in VIDEO_EXTS:
        return "videos"
    if suffix in AUDIO_EXTS:
        return "audio"
    mime, _ = guess_type(file_path.name)
    if mime:
        if mime.startswith("image/"):
            return "images"
        if mime.startswith("video/"):
            return "videos"
        if mime.startswith("audio/"):
            return "audio"
    return "others"


def infer_object_key(file_path: Path) -> str:
    category = classify_media(file_path)
    today = date.today().strftime("%Y%m%d")
    return f"{today}/{category}/{file_path.name}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="上传本地文件到七牛并返回交付链接")
    parser.add_argument(
        "file",
        type=Path,
        help="本地文件路径",
    )
    parser.add_argument(
        "--key",
        help="对象 key；不传则自动生成为 日期/类型/文件名",
    )
    access_mode_group = parser.add_mutually_exclusive_group()
    access_mode_group.add_argument(
        "--private-url",
        action="store_true",
        help="强制返回带签名的私有下载链接",
    )
    access_mode_group.add_argument(
        "--public-url",
        action="store_true",
        help="强制返回公网链接",
    )
    parser.add_argument(
        "--expires-in",
        type=int,
        default=DEFAULT_EXPIRES_IN,
        help="私有下载链接有效期，默认 600 秒",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    file_path = args.file.expanduser().resolve()  # type: ignore[union-attr]
    if not file_path.exists():
        raise FileNotFoundError(f"未找到本地文件: {file_path}")
    if args.expires_in <= 0:
        raise ValueError("--expires-in 必须大于 0")

    object_key = args.key or infer_object_key(file_path)
    config = load_config()
    upload_response = _upload_file(file_path=file_path, object_key=object_key, config=config)
    base_url = build_public_url(config["public_domain"], object_key)
    access_mode = resolve_access_mode(
        is_private_bucket=bool(config["is_private"]),
        prefer_private=args.private_url,
        prefer_public=args.public_url,
    )

    result: dict[str, object] = {
        "storage_provider": "qiniu",
        "bucket": config["bucket"],
        "object_key": object_key,
        "local_path": str(file_path),
        "upload_response": upload_response,
        "is_private_bucket": bool(config["is_private"]),
        "access_mode": access_mode,
        "base_url": base_url,
    }

    if access_mode == "private":
        private_url = build_private_download_url(
            access_key=config["access_key"],
            secret_key=config["secret_key"],
            base_url=base_url,
            expires_in=args.expires_in,
        )
        result["private_url"] = private_url
        result["delivery_url"] = private_url
        result["expires_in"] = args.expires_in
    else:
        result["public_url"] = base_url
        result["delivery_url"] = base_url

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
