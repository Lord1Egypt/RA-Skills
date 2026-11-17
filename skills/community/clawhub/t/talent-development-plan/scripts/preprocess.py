#!/usr/bin/env python3
"""
文档预处理脚本：将 PDF/DOCX/TXT/MD 等格式文件转为纯文本，保留表格结构。
优先使用 markitdown，降级为 python-docx 或 pdfplumber。
"""

import argparse
import json
import os
import sys


def preprocess_with_markitdown(input_file):
    """优先使用 markitdown 进行转换"""
    from markitdown import MarkItDown
    md = MarkItDown()
    result = md.convert(input_file)
    return result.text_content


def preprocess_docx(input_file):
    """使用 python-docx 提取 DOCX 全文+表格"""
    from docx import Document

    doc = Document(input_file)
    parts = []

    for element in doc.element.body:
        tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag

        if tag == "p":
            text = element.text or ""
            for run in element.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                if run.text:
                    text += run.text
            if text.strip():
                parts.append(text.strip())

        elif tag == "tbl":
            rows = element.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr")
            table_lines = []
            for row in rows:
                cells = row.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc")
                cell_texts = []
                for cell in cells:
                    cell_text = ""
                    for p in cell.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
                        for run in p.findall(".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                            if run.text:
                                cell_text += run.text
                    cell_texts.append(cell_text.strip().replace("\n", " "))
                if cell_texts:
                    table_lines.append("| " + " | ".join(cell_texts) + " |")
            if table_lines:
                # Add header separator
                col_count = len(table_lines[0].split("|")) - 2
                separator = "| " + " | ".join(["---"] * col_count) + " |"
                parts.append(table_lines[0])
                parts.append(separator)
                parts.extend(table_lines[1:])

    return "\n\n".join(parts)


def preprocess_pdf(input_file):
    """使用 pdfplumber 提取 PDF 全文+表格"""
    import pdfplumber

    parts = []
    with pdfplumber.open(input_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                parts.append(text)

            tables = page.extract_tables()
            for table in tables:
                if not table:
                    continue
                table_lines = []
                for row in table:
                    cell_texts = [
                        (cell or "").strip().replace("\n", " ")
                        for cell in row
                    ]
                    table_lines.append("| " + " | ".join(cell_texts) + " |")
                if table_lines:
                    col_count = len(table_lines[0].split("|")) - 2
                    separator = "| " + " | ".join(["---"] * col_count) + " |"
                    parts.append(table_lines[0])
                    parts.append(separator)
                    parts.extend(table_lines[1:])

    return "\n\n".join(parts)


def preprocess_txt(input_file):
    """直接读取纯文本/Markdown 文件"""
    with open(input_file, "r", encoding="utf-8") as f:
        return f.read()


def main():
    parser = argparse.ArgumentParser(
        description="将 PDF/DOCX/TXT/MD 文件预处理为纯文本，保留表格结构"
    )
    parser.add_argument("input_file", help="输入文件路径（支持 PDF/DOCX/TXT/MD）")
    parser.add_argument("-o", "--output", help="输出文件路径（不指定则输出到 stdout）")
    parser.add_argument("--encoding", default="utf-8", help="文本文件编码（默认 utf-8）")
    args = parser.parse_args()

    if not os.path.exists(args.input_file):
        result = {"status": "error", "message": f"文件不存在: {args.input_file}"}
        print(json.dumps(result, ensure_ascii=False))
        sys.exit(1)

    ext = os.path.splitext(args.input_file)[1].lower()
    text = ""
    method = ""

    # 策略1：优先 markitdown
    try:
        text = preprocess_with_markitdown(args.input_file)
        method = "markitdown"
    except Exception:
        # 策略2：按文件类型降级
        try:
            if ext in (".docx", ".doc"):
                text = preprocess_docx(args.input_file)
                method = "python-docx"
            elif ext == ".pdf":
                text = preprocess_pdf(args.input_file)
                method = "pdfplumber"
            elif ext in (".txt", ".md", ".markdown"):
                text = preprocess_txt(args.input_file)
                method = "direct-read"
            else:
                # 尝试按文本读取
                try:
                    text = preprocess_txt(args.input_file)
                    method = "direct-read-fallback"
                except Exception:
                    result = {
                        "status": "error",
                        "message": f"不支持的文件格式: {ext}",
                    }
                    print(json.dumps(result, ensure_ascii=False))
                    sys.exit(1)
        except Exception as e:
            result = {
                "status": "error",
                "message": f"预处理失败: {str(e)}",
                "file": args.input_file,
            }
            print(json.dumps(result, ensure_ascii=False))
            sys.exit(1)

    if args.output:
        os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        result = {
            "status": "success",
            "method": method,
            "output_file": args.output,
            "char_count": len(text),
            "line_count": text.count("\n") + 1,
        }
    else:
        result = {
            "status": "success",
            "method": method,
            "content": text,
            "char_count": len(text),
            "line_count": text.count("\n") + 1,
        }

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
