"""
pdf_to_text.py - PDF 文本提取模块
支持多种提取方式，按优先级：
  1. pdfminer.six（精确文本，保留段落结构）
  2. PyMuPDF / fitz（图片 PDF + 文字 PDF）
  3. pdfplumber（表格友好）
  4. pypdf2（纯文字 PDF）
  5. 在线 API 回退
"""

import os
import sys

_skill_dir = os.path.dirname(os.path.abspath(__file__))
if _skill_dir not in sys.path:
    sys.path.insert(0, _skill_dir)


def extract_text(pdf_path: str, max_pages: int = 0) -> str:
    """
    从 PDF 提取纯文本

    Args:
        pdf_path: PDF 文件路径
        max_pages: 最大提取页数（0 = 全部）
    Returns:
        纯文本字符串
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    size = os.path.getsize(pdf_path)
    if size > 50 * 1024 * 1024:
        print(f"[PDF] Warning: Large PDF ({size/1024/1024:.1f}MB), may take time", flush=True)

    # 尝试顺序
    extractors = [
        ("pdfminer",   _extract_pdfminer),
        ("pymupdf",    _extract_pymupdf),
        ("pdfplumber", _extract_pdfplumber),
        ("pypdf2",     _extract_pypdf2),
        ("pypdf",      _extract_pypdf),
    ]

    for name, fn in extractors:
        try:
            text = fn(pdf_path, max_pages)
            if text and len(text.strip()) > 100:
                print(f"[PDF] Extracted {len(text)} chars via {name}", flush=True)
                return _clean_text(text)
        except Exception as e:
            print(f"[PDF] {name} failed: {e}", flush=True)

    # 回退：OCR 或报告失败
    raise RuntimeError(
        f"None of the PDF extractors worked for: {pdf_path}\n"
        "Install one: pip install pdfminer.six  (recommended)"
    )


def _extract_pdfminer(pdf_path: str, max_pages: int) -> str:
    """pdfminer.six — 保留段落结构，最精确"""
    from pdfminer.high_level import extract_text
    return extract_text(pdf_path, maxpages=max_pages or 999)


def _extract_pymupdf(pdf_path: str, max_pages: int) -> str:
    """PyMuPDF / fitz"""
    import fitz  # pymupdf
    doc = fitz.open(pdf_path)
    pages = min(len(doc), max_pages) if max_pages else len(doc)
    parts = []
    for i in range(pages):
        parts.append(doc[i].get_text())
    doc.close()
    return "\n".join(parts)


def _extract_pdfplumber(pdf_path: str, max_pages: int) -> str:
    """pdfplumber — 表格友好"""
    import pdfplumber
    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages[:max_pages] if max_pages else pdf.pages
        return "\n".join(p.extract_text() or "" for p in pages)


def _extract_pypdf2(pdf_path: str, max_pages: int) -> str:
    """PyPDF2"""
    from PyPDF2 import PdfReader
    reader = PdfReader(pdf_path)
    pages = reader.pages[:max_pages] if max_pages else reader.pages
    return "\n".join(p.extract_text() or "" for p in pages)


def _extract_pypdf(pdf_path: str, max_pages: int) -> str:
    """pypdf（新版）"""
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    pages = reader.pages[:max_pages] if max_pages else reader.pages
    return "\n".join(p.extract_text() or "" for p in pages)


def _clean_text(text: str) -> str:
    """清理提取文本"""
    import re
    # 合并换行（保留段落边界）
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 去除多余空格
    text = re.sub(r' {2,}', ' ', text)
    # 去除孤立换行
    text = re.sub(r'(?<!\n)\n(?!\n)', ' ', text)
    # 去除零宽字符
    text = re.sub(r'[\u200b-\u200f\u2028-\u202f\ufeff]', '', text)
    return text.strip()


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PDF → Text Extractor")
    parser.add_argument("pdf_path", help="PDF file path")
    parser.add_argument("--max-pages", type=int, default=0,
                        help="Max pages to extract (0 = all)")
    parser.add_argument("--output", "-o", help="Output .txt file")
    args = parser.parse_args()

    text = extract_text(args.pdf_path, args.max_pages)
    print(f"Extracted {len(text)} characters")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Saved to {args.output}")
    else:
        print(text)
