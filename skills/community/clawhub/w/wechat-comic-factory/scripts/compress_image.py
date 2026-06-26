from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path
from typing import Any

from PIL import Image


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from common import (  # noqa: E402
    SkillError,
    ensure_directory,
    load_config,
    read_json_file,
    setup_logger,
    update_json_file,
)


def open_as_rgb(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        if image.mode == "RGB":
            return image.copy()
        if "A" in image.getbands():
            background = Image.new("RGB", image.size, "white")
            background.paste(image, mask=image.split()[-1])
            return background
        return image.convert("RGB")


def center_crop_to_ratio(image: Image.Image, target_ratio: float) -> Image.Image:
    width, height = image.size
    current_ratio = width / height
    if abs(current_ratio - target_ratio) < 0.001:
        return image

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        offset = (width - new_width) // 2
        return image.crop((offset, 0, offset + new_width, height))

    new_height = int(width / target_ratio)
    offset = (height - new_height) // 2
    return image.crop((0, offset, width, offset + new_height))


def save_jpeg_with_target(
    image: Image.Image,
    output_path: Path,
    *,
    target_kb: int | None = None,
    quality_start: int = 92,
    quality_min: int = 55,
    resize_step: float = 0.92,
) -> dict[str, Any]:
    ensure_directory(output_path.parent)
    working_image = image.copy()
    current_quality = quality_start

    while True:
        buffer = io.BytesIO()
        working_image.save(buffer, format="JPEG", quality=current_quality, optimize=True)
        size_kb = round(len(buffer.getvalue()) / 1024, 2)
        if target_kb is None or size_kb <= target_kb or current_quality <= quality_min:
            output_path.write_bytes(buffer.getvalue())
            return {
                "path": str(output_path),
                "size_kb": size_kb,
                "quality": current_quality,
                "width": working_image.width,
                "height": working_image.height,
            }
        current_quality -= 7
        if current_quality < quality_min:
            resized_width = max(480, int(working_image.width * resize_step))
            resized_height = max(480, int(working_image.height * resize_step))
            working_image = working_image.resize((resized_width, resized_height), Image.Resampling.LANCZOS)
            current_quality = quality_start


def compress_image_assets(manifest_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    output_dir = ensure_directory(output_dir)
    logger = setup_logger("wechat_comic_factory", output_dir)
    manifest = read_json_file(manifest_path)
    config = load_config(required_paths=["defaults.cover_width", "defaults.cover_height", "defaults.cover_max_kb"])
    defaults = config.get("defaults", {})

    cover_width = int(defaults.get("cover_width", 900))
    cover_height = int(defaults.get("cover_height", 500))
    cover_max_kb = int(defaults.get("cover_max_kb", 64))

    images = manifest.get("images", [])
    if not images:
        raise SkillError("compress_image", "manifest.json 中没有图片可压缩")

    publish_dir = ensure_directory(Path(output_dir) / "publish")
    cover_source_path = Path(output_dir) / images[0]["image_path"]
    cover_image = open_as_rgb(cover_source_path)
    cover_image = center_crop_to_ratio(cover_image, cover_width / cover_height)
    cover_image = cover_image.resize((cover_width, cover_height), Image.Resampling.LANCZOS)
    cover_result = save_jpeg_with_target(
        cover_image,
        publish_dir / "cover.jpg",
        target_kb=cover_max_kb,
    )
    logger.info("封面图压缩完成，size_kb=%s", cover_result["size_kb"])

    body_results: list[dict[str, Any]] = []
    for image in images:
        source_path = Path(output_dir) / image["image_path"]
        body_image = open_as_rgb(source_path)
        max_side = max(body_image.width, body_image.height)
        if max_side > 1280:
            scale = 1280 / max_side
            resized = (
                max(1, int(body_image.width * scale)),
                max(1, int(body_image.height * scale)),
            )
            body_image = body_image.resize(resized, Image.Resampling.LANCZOS)
        target_path = publish_dir / f"{int(image['index']):02d}.jpg"
        compression = save_jpeg_with_target(body_image, target_path, target_kb=768)
        body_results.append(
            {
                "index": image["index"],
                "caption": image.get("caption"),
                "source_path": image["image_path"],
                "wechat_path": target_path.relative_to(output_dir).as_posix(),
                "compression": compression,
            }
        )

    assets_payload = {
        "comic_type": manifest.get("comic_type"),
        "topic": manifest.get("topic"),
        "title": manifest.get("title"),
        "intro": manifest.get("intro"),
        "ending": manifest.get("ending"),
        "manifest_path": str(Path(manifest_path)),
        "cover_path": Path(cover_result["path"]).relative_to(output_dir).as_posix(),
        "cover_source_path": images[0]["image_path"],
        "images": body_results,
        "markdown_path": str(Path(output_dir) / "article.md"),
    }
    assets_path = update_json_file(Path(output_dir) / "publish_assets.json", assets_payload)
    logger.info("发布素材信息已写入，assets_path=%s", assets_path)
    return {
        "success": True,
        "stage": "compress_image",
        "title": str(manifest.get("title", "")).strip(),
        "assets_path": str(assets_path),
        "cover_path": assets_payload["cover_path"],
        "output_dir": str(output_dir),
    }


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="压缩封面图和正文图")
    parser.add_argument("--manifest_path", required=True, help="manifest.json 路径")
    parser.add_argument("--output_dir", required=True, help="输出目录")
    return parser


def main() -> None:
    parser = build_arg_parser()
    args = parser.parse_args()
    try:
        result = compress_image_assets(args.manifest_path, args.output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except SkillError as exc:
        print(json.dumps({"success": False, **exc.to_dict()}, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
