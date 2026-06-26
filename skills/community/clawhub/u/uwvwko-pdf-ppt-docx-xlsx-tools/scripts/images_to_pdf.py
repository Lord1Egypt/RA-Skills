"""图片 → PDF

用法:
    python images_to_pdf.py image1.png image2.jpg ... [output.pdf]

参数:
    image1.png ... - 一个或多个图片文件 (PNG/JPG/JPEG/BMP/TIFF/WebP)
    output.pdf     - 输出文件路径 (默认: output.pdf)

说明:
    支持混合格式，每张图片占一页，自动适配页面大小
"""
import fitz
import sys
import os


SUPPORTED = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def main():
    if len(sys.argv) < 2:
        print("用法: python images_to_pdf.py image1.png image2.jpg ... [output.pdf]")
        sys.exit(1)

    # 最后一个参数如果不是图片，则视为输出路径
    images = []
    out_path = "output.pdf"
    for arg in sys.argv[1:]:
        if os.path.isfile(arg) and os.path.splitext(arg)[1].lower() in SUPPORTED:
            images.append(arg)
        else:
            out_path = arg

    if not images:
        print("错误: 未提供有效的图片文件")
        sys.exit(1)

    doc = fitz.open()
    for img_path in images:
        img = fitz.open(img_path)
        page = doc.new_page(width=img[0].rect.width, height=img[0].rect.height)
        page.insert_image(page.rect, filename=img_path)
        img.close()
        print(f"Added: {img_path}")

    doc.save(out_path)
    doc.close()
    print(f"完成: {len(images)} 张图片 -> {out_path}")


if __name__ == "__main__":
    main()