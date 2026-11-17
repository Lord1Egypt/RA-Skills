#!/usr/bin/env python3
"""
连环画图片合并为 PDF 工具
支持 fpdf2 (优先) 和 Pillow (降级) 两种后端
"""

import argparse
import os
import re
import sys
from pathlib import Path


def find_pages(directory: str) -> list[str]:
    """在目录中查找页面图片并按文件名自然排序"""
    page_dir = Path(directory) / "pages"
    search_dir = page_dir if page_dir.is_dir() else Path(directory)

    extensions = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
    files = [
        str(f) for f in search_dir.iterdir()
        if f.is_file() and f.suffix.lower() in extensions
    ]

    # 自然排序：提取数字部分进行数值比较
    def natural_key(path: str):
        name = Path(path).stem
        numbers = re.findall(r"\d+", name)
        return [int(n) if n.isdigit() else n.lower() for n in re.split(r"(\d+)", name)]

    files.sort(key=natural_key)
    return files


def merge_with_fpdf(pages: list[str], output_path: str):
    """使用 fpdf2 合并图片为 PDF（自定义页面尺寸）"""
    from fpdf import FPDF
    from PIL import Image

    # ✅ 关键：指定单位为 pt，使后续尺寸计算一致
    pdf = FPDF(unit="pt")
    pdf.set_auto_page_break(auto=False)

    for img_path in pages:
        img = Image.open(img_path)
        # 确保 RGB 模式（PDF 不支持 RGBA/P 等）
        if img.mode != "RGB":
            img = img.convert("RGB")

        width_pt = img.width * 72 / 96   # px → pt @96DPI
        height_pt = img.height * 72 / 96

        # ✅ 修复：先 add_page()，再用 set_page_size() 设置自定义尺寸
        pdf.add_page()
        pdf.set_page_size(width_pt, height_pt)
        pdf.image(img_path, x=0, y=0, w=width_pt, h=height_pt)

    pdf.output(output_path)


def merge_with_pillow(pages: list[str], output_path: str):
    """使用 Pillow 合并图片为 PDF（降级方案）"""
    from PIL import Image

    images = []
    for img_path in pages:
        img = Image.open(img_path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        images.append(img)

    if not images:
        print("错误：没有可处理的图片", file=sys.stderr)
        sys.exit(1)

    first = images[0]
    rest = images[1:] if len(images) > 1 else []
    first.save(
        output_path,
        "PDF",
        resolution=96.0,
        save_all=True,
        append_images=rest,
    )


def main():
    parser = argparse.ArgumentParser(description="将连环画页面图片合并为 PDF")
    parser.add_argument("directory", help="包含页面图片的目录路径")
    parser.add_argument("-o", "--output", help="输出 PDF 文件路径（默认：<目录名>.pdf）")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"错误：目录不存在: {args.directory}", file=sys.stderr)
        sys.exit(1)

    pages = find_pages(args.directory)
    if not pages:
        print(f"错误：未在 {args.directory} 中找到图片文件", file=sys.stderr)
        sys.exit(1)

    print(f"找到 {len(pages)} 个页面")

    output_path = args.output
    if not output_path:
        dir_name = Path(args.directory).resolve().name
        output_path = f"{dir_name}.pdf"

    # 优先尝试 fpdf2，失败则降级到 Pillow
    try:
        merge_with_fpdf(pages, output_path)
        print(f"✅ 已使用 fpdf2 生成: {output_path}")
    except ImportError:
        print("⚠️  fpdf2 未安装，降级使用 Pillow...", file=sys.stderr)
        merge_with_pillow(pages, output_path)
        print(f"✅ 已使用 Pillow 生成: {output_path}")
    except Exception as e:
        print(f"⚠️  fpdf2 出错 ({e})，降级使用 Pillow...", file=sys.stderr)
        merge_with_pillow(pages, output_path)
        print(f"✅ 已使用 Pillow 生成: {output_path}")


if __name__ == "__main__":
    main()