"""PDF → 图片 (PNG/JPG)

用法:
    python pdf_to_images.py input.pdf [output_dir] [dpi] [format]

参数:
    input.pdf   - PDF 文件路径
    output_dir  - 输出目录 (默认: ./pdf_images_output)
    dpi         - 分辨率 (默认: 200, 推荐 150~300)
    format      - 图片格式: png 或 jpg (默认: png)
"""
import fitz
import sys
import os


def main():
    pdf_path = sys.argv[1] if len(sys.argv) > 1 else ""
    out_dir = sys.argv[2] if len(sys.argv) > 2 else "./pdf_images_output"
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 200
    fmt = sys.argv[4].lower() if len(sys.argv) > 4 else "png"

    if not pdf_path:
        print("用法: python pdf_to_images.py input.pdf [output_dir] [dpi] [format]")
        sys.exit(1)

    if not os.path.isfile(pdf_path):
        print(f"错误: 文件不存在 - {pdf_path}")
        sys.exit(1)

    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)

    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=dpi)
        out = os.path.join(out_dir, f"page_{i + 1:04d}.{fmt}")
        pix.save(out)
        print(f"Saved: {out}")

    total = len(doc)
    doc.close()
    print(f"完成: {total} 页 -> {out_dir}")


if __name__ == "__main__":
    main()