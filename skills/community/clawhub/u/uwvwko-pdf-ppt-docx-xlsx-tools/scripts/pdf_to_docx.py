"""PDF → DOCX

用法:
    python pdf_to_docx.py input.pdf [output.docx] [--start N] [--end N] [--multi]

参数:
    input.pdf   - PDF 文件路径
    output.docx - 输出文件路径 (默认: output.docx)
    --start N   - 起始页码 (从 0 开始, 默认: 0)
    --end N     - 结束页码 (不含, 默认: None 即到末尾)
    --multi     - 启用多进程加速 (适用于大文件)
"""
from pdf2docx import Converter
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("用法: python pdf_to_docx.py input.pdf [output.docx] [--start N] [--end N] [--multi]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    out_path = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else "output.docx"

    if not os.path.isfile(pdf_path):
        print(f"错误: 文件不存在 - {pdf_path}")
        sys.exit(1)

    # 解析可选参数
    kwargs = {}
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--start" and i + 1 < len(args):
            kwargs["start"] = int(args[i + 1])
            i += 2
        elif args[i] == "--end" and i + 1 < len(args):
            kwargs["end"] = int(args[i + 1])
            i += 2
        elif args[i] == "--multi":
            kwargs["multi_processing"] = True
            i += 1
        else:
            i += 1

    cv = Converter(pdf_path)
    cv.convert(out_path, **kwargs)
    cv.close()
    print(f"完成: {pdf_path} -> {out_path}")


if __name__ == "__main__":
    main()