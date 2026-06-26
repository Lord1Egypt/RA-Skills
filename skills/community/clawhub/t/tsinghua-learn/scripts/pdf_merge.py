#!/usr/bin/env python3
"""
pdf_merge.py — 图片合并为 PDF
将目录中的图片按文件名排序合并为单一 PDF。
支持: jpg/jpeg/png/webp/bmp/heic/heif

用法（CLI）：
  python scripts/pdf_merge.py --input-dir <目录> [--output <路径>]

输出 JSON：
  {"status": "ok", "path": "...", "pages": 12}
  {"status": "error", "message": "..."}
"""
import sys, os, json
sys.stdout.reconfigure(encoding='utf-8')

SUPPORTED = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".heic", ".heif")


def merge(input_dir, output=None):
    """将 input_dir 下的图片按文件名排序合并为 PDF。返回输出路径和页数。"""
    if not os.path.isdir(input_dir):
        return {"status": "error", "message": f"目录不存在: {input_dir}"}

    files = []
    for f in sorted(os.listdir(input_dir)):
        ext = os.path.splitext(f)[1].lower()
        if ext in SUPPORTED:
            files.append(os.path.join(input_dir, f))

    if not files:
        return {"status": "error", "message": "目录中无支持的图片文件"}

    images = []
    try:
        from PIL import Image
        from PIL import JpegImagePlugin, PngImagePlugin  # 确保编码器注册
        for fpath in files:
            ext = os.path.splitext(fpath)[1].lower()
            if ext in (".heic", ".heif"):
                from pillow_heif import open_heif
                heif = open_heif(fpath)
                img = Image.frombytes(
                    heif.mode, heif.size, heif.data,
                    "raw", heif.mode, heif.stride,
                )
            else:
                img = Image.open(fpath)
            images.append(img.convert("RGB"))

        if not images:
            return {"status": "error", "message": "图片加载失败"}

        if output is None:
            output = os.path.join(input_dir, "merged.pdf")

        images[0].save(output, save_all=True, append_images=images[1:])
        return {"status": "ok", "path": os.path.abspath(output), "pages": len(images)}

    except Exception as e:
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="图片合并为 PDF")
    parser.add_argument("--input-dir", required=True, help="图片目录")
    parser.add_argument("--output", default=None, help="输出 PDF 路径（默认 input-dir/merged.pdf）")
    args = parser.parse_args()

    result = merge(args.input_dir, args.output)
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result["status"] == "ok" else 1)
