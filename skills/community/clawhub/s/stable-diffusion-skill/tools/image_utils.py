#!/usr/bin/env python3
"""
Image Utilities for Stable Diffusion Skill
- Base64 encoding/decoding
- Image resizing and preprocessing
- Mask generation helpers
- Result gallery generation
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


# ── Base64 Utilities ─────────────────────────────────────────────────────────────

def image_to_base64(image_path: str) -> str:
    """Convert image file to base64 string"""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def base64_to_image(b64_str: str, output_path: str):
    """Save base64 string as image file"""
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    # Strip data URI prefix if present
    if "," in b64_str:
        b64_str = b64_str.split(",", 1)[1]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(b64_str))
    print(f"✅ 保存图像: {output_path}")


# ── Image Preprocessing ──────────────────────────────────────────────────────────

def resize_image(image_path: str, width: int, height: int, output_path: str = None):
    """Resize image to given dimensions"""
    if not HAS_PIL:
        print("❌ 需要 Pillow: pip install Pillow")
        sys.exit(1)

    img = Image.open(image_path)
    resized = img.resize((width, height), Image.LANCZOS)

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_resized_{width}x{height}{ext}"

    resized.save(output_path)
    print(f"✅ 调整大小完成: {output_path} ({width}x{height})")
    return output_path


def resize_to_sd_size(image_path: str, output_path: str = None) -> str:
    """Resize image to nearest SD-compatible size (multiple of 8, max 1024)"""
    if not HAS_PIL:
        print("❌ 需要 Pillow: pip install Pillow")
        sys.exit(1)

    img = Image.open(image_path)
    w, h = img.size

    # Round to nearest multiple of 8
    def round_to_8(x):
        return max(8, (x // 8) * 8)

    # Scale down if too large
    max_dim = 1024
    if w > max_dim or h > max_dim:
        ratio = min(max_dim / w, max_dim / h)
        w = int(w * ratio)
        h = int(h * ratio)

    new_w = round_to_8(w)
    new_h = round_to_8(h)

    if (new_w, new_h) != img.size:
        img = img.resize((new_w, new_h), Image.LANCZOS)
        if output_path is None:
            base, ext = os.path.splitext(image_path)
            output_path = f"{base}_sd{ext}"
        img.save(output_path)
        print(f"✅ 调整为 SD 兼容尺寸: {new_w}x{new_h} -> {output_path}")
        return output_path
    else:
        print(f"ℹ️  图像尺寸 {w}x{h} 已是 SD 兼容格式")
        return image_path


def get_image_info(image_path: str):
    """Get image dimensions and format"""
    if not HAS_PIL:
        # Fallback: just show file size
        size = os.path.getsize(image_path)
        print(f"📸 文件: {image_path}")
        print(f"   大小: {size/1024:.1f} KB")
        return

    img = Image.open(image_path)
    w, h = img.size
    mode = img.mode
    fmt = img.format or "Unknown"

    print(f"📸 图像信息: {image_path}")
    print(f"   尺寸: {w} x {h}")
    print(f"   格式: {fmt}")
    print(f"   颜色模式: {mode}")
    print(f"   文件大小: {os.path.getsize(image_path)/1024:.1f} KB")

    # Check SD compatibility
    if w % 8 != 0 or h % 8 != 0:
        print(f"   ⚠️  尺寸不是8的倍数，建议调整")
    if w > 1024 or h > 1024:
        print(f"   ⚠️  尺寸过大，建议缩小到1024以内")


# ── Mask Utilities ───────────────────────────────────────────────────────────────

def create_blank_mask(image_path: str, output_path: str = None):
    """Create a blank (all black) mask with same size as input image"""
    if not HAS_PIL:
        print("❌ 需要 Pillow: pip install Pillow")
        sys.exit(1)

    img = Image.open(image_path)
    mask = Image.new("L", img.size, 0)  # All black = not masked

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_mask.png"

    mask.save(output_path)
    print(f"✅ 创建空白蒙版: {output_path}")
    print("   提示: 用图像编辑器在需要重绘的区域涂白色")
    return output_path


def create_rect_mask(image_path: str, x1: int, y1: int, x2: int, y2: int,
                     output_path: str = None, blur: int = 0):
    """Create a rectangular mask"""
    if not HAS_PIL:
        print("❌ 需要 Pillow: pip install Pillow")
        sys.exit(1)

    img = Image.open(image_path)
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle([x1, y1, x2, y2], fill=255)

    if blur > 0:
        mask = mask.filter(ImageFilter.GaussianBlur(blur))

    if output_path is None:
        base, ext = os.path.splitext(image_path)
        output_path = f"{base}_mask_rect.png"

    mask.save(output_path)
    print(f"✅ 创建矩形蒙版: {output_path} (区域: {x1},{y1} - {x2},{y2})")
    return output_path


# ── Gallery Generator ────────────────────────────────────────────────────────────

def generate_gallery(image_paths: list, output_html: str = "gallery.html", title: str = "SD Generation Gallery"):
    """Generate a simple HTML gallery from image paths"""
    images_html = []
    for path in image_paths:
        abs_path = os.path.abspath(path)
        filename = os.path.basename(path)
        images_html.append(f'''
        <div class="card">
            <img src="file:///{abs_path.replace(chr(92), "/")}" alt="{filename}">
            <div class="caption">{filename}</div>
        </div>''')

    html = f"""<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<style>
  body {{ font-family: Arial, sans-serif; background: #1a1a2e; color: #eee; margin: 20px; }}
  h1 {{ color: #e94560; text-align: center; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }}
  .card {{ background: #16213e; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.4); }}
  .card img {{ width: 100%; height: auto; display: block; }}
  .caption {{ padding: 8px 12px; font-size: 12px; color: #aaa; word-break: break-all; }}
</style>
</head>
<body>
<h1>🎨 {title}</h1>
<p style="text-align:center;color:#888">共 {len(image_paths)} 张图像</p>
<div class="grid">{''.join(images_html)}
</div>
</body>
</html>"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 图库已生成: {os.path.abspath(output_html)}")
    return output_html


def scan_output_dir(directory: str = "./sd_output") -> list:
    """Scan directory for generated images"""
    if not os.path.exists(directory):
        print(f"⚠️  目录不存在: {directory}")
        return []

    exts = {".png", ".jpg", ".jpeg", ".webp"}
    images = []
    for f in sorted(Path(directory).iterdir()):
        if f.suffix.lower() in exts:
            images.append(str(f))

    print(f"📂 找到 {len(images)} 张图像 in {directory}")
    return images


# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="SD Image Utilities")
    sub = parser.add_subparsers(dest="cmd")

    # info
    p_info = sub.add_parser("info", help="查看图像信息")
    p_info.add_argument("image")

    # resize
    p_resize = sub.add_parser("resize", help="调整图像尺寸")
    p_resize.add_argument("image")
    p_resize.add_argument("--width", type=int)
    p_resize.add_argument("--height", type=int)
    p_resize.add_argument("--sd-compat", action="store_true", help="自动调整为SD兼容尺寸")
    p_resize.add_argument("--output", "-o")

    # mask
    p_mask = sub.add_parser("mask", help="创建重绘蒙版")
    p_mask.add_argument("image")
    p_mask.add_argument("--blank", action="store_true", help="创建空白蒙版")
    p_mask.add_argument("--rect", nargs=4, type=int, metavar=("X1", "Y1", "X2", "Y2"),
                         help="创建矩形蒙版")
    p_mask.add_argument("--blur", type=int, default=0, help="蒙版边缘模糊半径")
    p_mask.add_argument("--output", "-o")

    # to-b64
    p_b64 = sub.add_parser("to-b64", help="图像转Base64")
    p_b64.add_argument("image")

    # from-b64
    p_fb64 = sub.add_parser("from-b64", help="Base64转图像")
    p_fb64.add_argument("b64_string")
    p_fb64.add_argument("--output", "-o", required=True)

    # gallery
    p_gallery = sub.add_parser("gallery", help="生成HTML图库")
    p_gallery.add_argument("--dir", default="./sd_output", help="图像目录")
    p_gallery.add_argument("--output", "-o", default="gallery.html")
    p_gallery.add_argument("--title", default="SD Generation Gallery")

    args = parser.parse_args()

    if args.cmd == "info":
        get_image_info(args.image)
    elif args.cmd == "resize":
        if args.sd_compat:
            resize_to_sd_size(args.image, args.output)
        elif args.width and args.height:
            resize_image(args.image, args.width, args.height, args.output)
        else:
            print("❌ 需要提供 --width --height 或 --sd-compat")
    elif args.cmd == "mask":
        if args.blank:
            create_blank_mask(args.image, args.output)
        elif args.rect:
            create_rect_mask(args.image, *args.rect, output_path=args.output, blur=args.blur)
        else:
            print("❌ 需要 --blank 或 --rect x1 y1 x2 y2")
    elif args.cmd == "to-b64":
        b64 = image_to_base64(args.image)
        print(b64[:100] + "...")
        print(f"(总长度: {len(b64)} 字符)")
    elif args.cmd == "from-b64":
        base64_to_image(args.b64_string, args.output)
    elif args.cmd == "gallery":
        images = scan_output_dir(args.dir)
        if images:
            generate_gallery(images, args.output, args.title)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
