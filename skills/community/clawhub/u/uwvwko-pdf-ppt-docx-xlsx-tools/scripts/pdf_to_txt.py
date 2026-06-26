"""PDF → 纯文本 (TXT)

用法:
    python pdf_to_txt.py input.pdf [output.txt]

参数:
    input.pdf   - PDF 文件路径
    output.txt  - 输出文件路径 (默认: output.txt)
"""
import fitz
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("用法: python pdf_to_txt.py input.pdf [output.txt]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output.txt"

    if not os.path.isfile(pdf_path):
        print(f"错误: 文件不存在 - {pdf_path}")
        sys.exit(1)

    doc = fitz.open(pdf_path)
    with open(out_path, "w", encoding="utf-8") as f:
        for i, page in enumerate(doc):
            text = page.get_text()
            f.write(f"--- Page {i + 1} ---\n{text}\n\n")

    total = len(doc)
    doc.close()
    print(f"完成: {total} 页文本已提取 -> {out_path}")


if __name__ == "__main__":
    main()