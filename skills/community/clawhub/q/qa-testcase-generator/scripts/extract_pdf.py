#!/usr/bin/env python3
"""
PDF 文本提取工具 — 供 SKILL.md 阶段一/二使用。
从 PDF 文件中提取所有文本，输出结构化 Markdown 格式供 AI 分析。

用法:
    python scripts/extract_pdf.py <path/to/file.pdf> [-o output.txt]
    python scripts/extract_pdf.py <path/to/file.pdf>  # 输出到 stdout

依赖: pdfplumber (推荐) 或 pdfminer.six
"""
import sys, os, argparse
from pathlib import Path


def extract_with_pdfplumber(path: str) -> str:
    """使用 pdfplumber 提取文本（保留页面结构）"""
    import pdfplumber
    pages = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages, 1):
            text = page.extract_text() or ""
            if text.strip():
                pages.append(f"--- Page {i} ---\n{text.strip()}")
    return "\n\n".join(pages)


def extract_with_pdfminer(path: str) -> str:
    """使用 pdfminer 提取文本（备用方案）"""
    from pdfminer.high_level import extract_text
    text = extract_text(path)
    return text.strip()


def extract_pdf(path: str) -> str:
    """顺序尝试各 PDF 库，返回文本"""
    try:
        text = extract_with_pdfplumber(path)
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception as e:
        print(f"[警告] pdfplumber 提取失败: {e}", file=sys.stderr)

    try:
        text = extract_with_pdfminer(path)
        if text.strip():
            return text
    except ImportError:
        pass
    except Exception as e:
        print(f"[警告] pdfminer 提取失败: {e}", file=sys.stderr)

    raise RuntimeError(f"无法提取 PDF 文本: 没有可用的 PDF 库（请安装 pdfplumber 或 pdfminer.six）")


def main():
    parser = argparse.ArgumentParser(description="从 PDF 文件提取文本")
    parser.add_argument("input", help="PDF 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径（默认输出到 stdout）")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"错误: 文件不存在 - {src}", file=sys.stderr)
        sys.exit(1)
    if src.suffix.lower() != ".pdf":
        print(f"警告: 输入文件不是 .pdf 格式: {src}", file=sys.stderr)

    text = extract_pdf(str(src))
    header = f"# 提取自: {src.name}\n# 页数: {text.count('--- Page')}\n# 总字符: {len(text)}\n\n"

    if args.output:
        dst = Path(args.output)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(header + text, encoding="utf-8")
        print(f"文本已提取到: {dst}", file=sys.stdout)
    else:
        sys.stdout.write(header + text)


if __name__ == "__main__":
    main()
