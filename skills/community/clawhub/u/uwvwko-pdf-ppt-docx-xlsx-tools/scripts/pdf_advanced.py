"""PDF 高级操作: 合并 / 拆分 / 水印

用法:
    合并: python pdf_advanced.py merge file1.pdf file2.pdf ... [output.pdf]
    拆分: python pdf_advanced.py split input.pdf [output_dir] [--range 0-5,8-10]
    水印: python pdf_advanced.py watermark input.pdf "水印文字" [output.pdf] [--opacity 0.3] [--size 60] [--color #999999]
    提取页: python pdf_advanced.py extract input.pdf output.pdf --pages 0,2,5-8
    信息: python pdf_advanced.py info input.pdf
"""
import fitz
import sys
import os
import re


def merge(files, out_path):
    if len(files) < 2:
        print("错误: 合并至少需要 2 个 PDF 文件")
        sys.exit(1)
    doc = fitz.open()
    for f in files:
        if not os.path.isfile(f):
            print(f"错误: 文件不存在 - {f}")
            sys.exit(1)
        src = fitz.open(f)
        doc.insert_pdf(src)
        src.close()
        print(f"Added: {f}")
    doc.save(out_path)
    doc.close()
    print(f"完成: {len(files)} 个文件合并 -> {out_path}")


def split(pdf_path, out_dir, range_str=None):
    os.makedirs(out_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    pages = parse_range(range_str, len(doc)) if range_str else range(len(doc))

    for i in pages:
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
        out = os.path.join(out_dir, f"page_{i + 1:04d}.pdf")
        new_doc.save(out)
        new_doc.close()
        print(f"Saved: {out}")

    doc.close()
    print(f"完成: {len(list(pages))} 页 -> {out_dir}")


def watermark(pdf_path, text, out_path, opacity=0.3, size=60, color="#999999"):
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        rect = page.rect
        # 将十六进制颜色转为 RGB 元组
        r = int(color[1:3], 16) / 255
        g = int(color[3:5], 16) / 255
        b = int(color[5:7], 16) / 255
        page.insert_textbox(
            fitz.Rect(0, rect.height / 3, rect.width, rect.height * 2 / 3),
            text,
            fontsize=size,
            color=(r, g, b),
            opacity=opacity,
            rotate=45,
            align=1,
        )
        print(f"Page {i + 1} watermarked")
    doc.save(out_path)
    doc.close()
    print(f"完成: {len(doc)} 页 -> {out_path}")


def extract(pdf_path, out_path, pages_str):
    doc = fitz.open(pdf_path)
    pages = parse_range(pages_str, len(doc))
    new_doc = fitz.open()
    for i in pages:
        new_doc.insert_pdf(doc, from_page=i, to_page=i)
    new_doc.save(out_path)
    new_doc.close()
    doc.close()
    print(f"完成: {len(list(pages))} 页提取 -> {out_path}")


def info(pdf_path):
    doc = fitz.open(pdf_path)
    meta = doc.metadata
    print(f"文件: {pdf_path}")
    print(f"页数: {len(doc)}")
    print(f"标题: {meta.get('title', 'N/A')}")
    print(f"作者: {meta.get('author', 'N/A')}")
    print(f"创建者: {meta.get('creator', 'N/A')}")
    print(f"生产者: {meta.get('producer', 'N/A')}")
    print(f"创建时间: {meta.get('creationDate', 'N/A')}")
    print(f"修改时间: {meta.get('modDate', 'N/A')}")
    for i, page in enumerate(doc):
        print(f"  Page {i + 1}: {page.rect.width:.0f} x {page.rect.height:.0f} pts")
    doc.close()


def parse_range(range_str, total):
    """解析页码范围字符串，如 '0-5,8,10-12'"""
    pages = set()
    for part in range_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            start = int(start)
            end = int(end)
            pages.update(range(start, min(end, total)))
        else:
            p = int(part)
            if 0 <= p < total:
                pages.add(p)
    return sorted(pages)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "merge":
        out = sys.argv[-1] if not sys.argv[-1].endswith(".pdf") or os.path.isfile(sys.argv[-1]) else sys.argv[-1]
        files = [f for f in sys.argv[2:] if f != out and os.path.isfile(f)]
        if not out.endswith(".pdf") or not files:
            out = sys.argv[-1] if len(sys.argv) > 3 else "merged.pdf"
            files = [f for f in sys.argv[2:-1] if os.path.isfile(f)]
        merge(files, out)

    elif action == "split":
        pdf_path = sys.argv[2]
        out_dir = sys.argv[3] if len(sys.argv) > 3 else "./pdf_split_output"
        range_str = None
        for i, arg in enumerate(sys.argv):
            if arg == "--range" and i + 1 < len(sys.argv):
                range_str = sys.argv[i + 1]
        split(pdf_path, out_dir, range_str)

    elif action == "watermark":
        pdf_path = sys.argv[2]
        text = sys.argv[3]
        out_path = sys.argv[4] if len(sys.argv) > 4 and not sys.argv[4].startswith("--") else "watermarked.pdf"
        opacity, size, color = 0.3, 60, "#999999"
        for i, arg in enumerate(sys.argv):
            if arg == "--opacity" and i + 1 < len(sys.argv):
                opacity = float(sys.argv[i + 1])
            elif arg == "--size" and i + 1 < len(sys.argv):
                size = int(sys.argv[i + 1])
            elif arg == "--color" and i + 1 < len(sys.argv):
                color = sys.argv[i + 1]
        watermark(pdf_path, text, out_path, opacity, size, color)

    elif action == "extract":
        pdf_path = sys.argv[2]
        out_path = sys.argv[3]
        pages_str = None
        for i, arg in enumerate(sys.argv):
            if arg == "--pages" and i + 1 < len(sys.argv):
                pages_str = sys.argv[i + 1]
        if not pages_str:
            print("错误: 请通过 --pages 指定页码，如 --pages 0,2,5-8")
            sys.exit(1)
        extract(pdf_path, out_path, pages_str)

    elif action == "info":
        info(sys.argv[2])

    else:
        print(f"未知操作: {action}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()