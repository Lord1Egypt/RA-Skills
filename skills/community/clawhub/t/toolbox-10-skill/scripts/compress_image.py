#!/usr/bin/env python3
"""
图片压缩工具 — 基于 Pillow
支持质量调节、尺寸缩放、格式转换，输出压缩率报告。
"""

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


# 格式支持的压缩参数
FORMAT_SETTINGS = {
    ".jpg": {"format": "JPEG", "quality_key": "quality", "optimize": True},
    ".jpeg": {"format": "JPEG", "quality_key": "quality", "optimize": True},
    ".png": {"format": "PNG", "quality_key": "optimize", "optimize": True},
    ".webp": {"format": "WEBP", "quality_key": "quality", "optimize": True},
    ".bmp": {"format": "BMP", "quality_key": None, "optimize": False},
    ".tiff": {"format": "TIFF", "quality_key": None, "optimize": True},
    ".tif": {"format": "TIFF", "quality_key": None, "optimize": True},
}


def compress_image(
    input_path: str,
    output_path: str = None,
    quality: int = 85,
    max_width: int = None,
    max_height: int = None,
    output_format: str = None,
    max_size_kb: int = None,
) -> dict:
    """
    压缩图片。
    """
    input_file = Path(input_path)
    if not input_file.exists():
        return {"success": False, "error": f"文件不存在: {input_path}"}

    input_size = input_file.stat().st_size

    # 读取图片
    try:
        img = Image.open(input_path)
        original_mode = img.mode
        original_size = img.size  # (width, height)
    except Exception as e:
        return {"success": False, "error": f"无法读取图片: {str(e)}"}

    # 确定输出格式
    if output_format:
        fmt = output_format.lower()
        if not fmt.startswith("."):
            fmt = f".{fmt}"
    elif output_path:
        fmt = Path(output_path).suffix.lower()
    else:
        fmt = input_file.suffix.lower()

    if fmt not in FORMAT_SETTINGS:
        # 默认使用 JPEG
        fmt = ".jpg"

    settings = FORMAT_SETTINGS.get(fmt, FORMAT_SETTINGS[".jpg"])

    # 智能模式转换
    # RGBA → RGB for JPEG
    if settings["format"] == "JPEG" and img.mode in ("RGBA", "P", "LA"):
        # 创建白色背景
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        if img.mode in ("RGBA", "LA"):
            background.paste(img, mask=img.split()[-1])
        img = background

    # PNG 保持 RGBA
    if settings["format"] in ("PNG", "WEBP") and img.mode == "RGBA":
        pass  # 保持透明
    elif img.mode not in ("RGB", "RGBA", "L", "LA"):
        img = img.convert("RGB")

    # 尺寸缩放
    if max_width or max_height:
        new_w, new_h = original_size
        if max_width and new_w > max_width:
            ratio = max_width / new_w
            new_w = max_width
            new_h = int(new_h * ratio)
        if max_height and new_h > max_height:
            ratio = max_height / new_h
            new_h = max_height
            new_w = int(new_w * ratio)
        if (new_w, new_h) != original_size:
            img = img.resize((new_w, new_h), Image.LANCZOS)

    # 确定输出路径
    if output_path is None:
        stem = input_file.stem
        output_dir = input_file.parent
        suffix = fmt if fmt.startswith(".") else f".{fmt}"
        output_file = output_dir / f"{stem}_compressed{suffix}"
    else:
        output_file = Path(output_path)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 保存参数
    save_kwargs = {}
    if settings["quality_key"] == "quality":
        save_kwargs["quality"] = quality
    if settings["optimize"]:
        save_kwargs["optimize"] = True

    save_format = settings["format"]

    # 最大文件大小模式：二分搜索质量
    if max_size_kb and settings["quality_key"] == "quality":
        best_data = None
        lo, hi = 5, 95
        target_bytes = max_size_kb * 1024

        for _ in range(8):
            mid = (lo + hi) // 2
            save_kwargs["quality"] = mid
            from io import BytesIO
            buf = BytesIO()
            img.save(buf, format=save_format, **save_kwargs)
            size = buf.tell()

            if size <= target_bytes:
                best_data = buf.getvalue()
                lo = mid + 1  # 尝试更高质量
                if abs(size - target_bytes) < target_bytes * 0.05:
                    break
            else:
                hi = mid - 1

        if best_data is None:
            # 最低质量也超出，用最低
            save_kwargs["quality"] = 5
            from io import BytesIO
            buf = BytesIO()
            img.save(buf, format=save_format, **save_kwargs)
            best_data = buf.getvalue()

        output_file.write_bytes(best_data)
        actual_quality = save_kwargs.get("quality", quality)
    else:
        img.save(str(output_file), format=save_format, **save_kwargs)
        actual_quality = quality

    # 统计结果
    output_size = output_file.stat().st_size
    compression_ratio = (1 - output_size / input_size) * 100 if input_size > 0 else 0

    return {
        "success": True,
        "output": str(output_file),
        "input_size": input_size,
        "output_size": output_size,
        "input_size_kb": round(input_size / 1024, 2),
        "output_size_kb": round(output_size / 1024, 2),
        "compression_ratio": round(compression_ratio, 1),
        "original_dimensions": {"width": original_size[0], "height": original_size[1]},
        "output_dimensions": {"width": img.width, "height": img.height},
        "format": save_format,
        "quality": actual_quality,
    }


def main():
    parser = argparse.ArgumentParser(description="图片压缩工具")
    parser.add_argument("input", help="输入图片路径")
    parser.add_argument("-o", "--output", help="输出图片路径")
    parser.add_argument(
        "-q", "--quality", type=int, default=85, help="压缩质量 (1-100, 默认85)"
    )
    parser.add_argument("--max-width", type=int, help="最大宽度 (px)")
    parser.add_argument("--max-height", type=int, help="最大高度 (px)")
    parser.add_argument(
        "--format",
        choices=["jpg", "jpeg", "png", "webp", "bmp"],
        help="输出格式",
    )
    parser.add_argument("--max-size", type=int, help="最大文件大小 (KB)")

    args = parser.parse_args()

    result = compress_image(
        input_path=args.input,
        output_path=args.output,
        quality=args.quality,
        max_width=args.max_width,
        max_height=args.max_height,
        output_format=args.format,
        max_size_kb=args.max_size,
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
