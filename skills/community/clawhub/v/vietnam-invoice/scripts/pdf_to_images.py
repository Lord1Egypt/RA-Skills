"""PDF 转图片工具 - 越南发票验真 skill 子能力

将 PDF 每页转为 PNG 图片，供 Claude 多模态识别使用。

用法:
    # 输出 PNG 文件到指定目录
    python pdf_to_images.py input.pdf -o ./output_dir

    # 输出 base64 到 stdout（供管道调用）
    python pdf_to_images.py input.pdf --base64

    # 指定 DPI（默认 200）
    python pdf_to_images.py input.pdf -o ./output_dir --dpi 300
"""

import argparse
import base64
import io
import os
import sys


def pdf_to_images(pdf_path: str, dpi: int = 200) -> list[bytes]:
    """将 PDF 每页转为 PNG bytes"""
    import pymupdf
    from PIL import Image

    result = []
    scale = dpi / 96  # 96 是 PDF 默认 DPI
    with pymupdf.open(pdf_path) as doc:
        for page in doc:
            mat = pymupdf.Matrix(scale, scale)
            pix = page.get_pixmap(matrix=mat)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            result.append(buf.getvalue())
    return result


def main():
    parser = argparse.ArgumentParser(description="PDF 转图片工具")
    parser.add_argument("input", help="PDF 文件路径")
    parser.add_argument("-o", "--output-dir", help="输出目录（保存为 PNG 文件）")
    parser.add_argument("--base64", action="store_true",
                        help="输出 base64 到 stdout（JSON 数组）")
    parser.add_argument("--dpi", type=int, default=200, help="输出 DPI（默认 200）")
    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"错误: 文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    images = pdf_to_images(args.input, dpi=args.dpi)
    print(f"共 {len(images)} 页", file=sys.stderr)

    if args.base64:
        import json
        print(json.dumps([base64.b64encode(b).decode() for b in images]))
    elif args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        for i, data in enumerate(images, 1):
            path = os.path.join(args.output_dir, f"page_{i}.png")
            with open(path, "wb") as f:
                f.write(data)
            print(f"  已保存: {path}", file=sys.stderr)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
