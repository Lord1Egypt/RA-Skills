"""Word document word count and statistics.

Extracts text from .docx files and provides detailed character/word statistics.
Supports both terminal display and JSON output for programmatic use.

Usage:
    python3 word_count.py document.docx
    python3 word_count.py document.docx --format json
    python3 word_count.py document.docx --preview 200
"""

import argparse
import json
import math
import re
import sys
import zipfile
from pathlib import Path

import defusedxml.minidom

WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# Average chars per A4 page (Chinese document, ~30 lines × ~35 chars)
CHARS_PER_PAGE = 1050


def count_words(input_file: str, preview_len: int = 0) -> tuple[dict, str]:
    """Count words and characters in a DOCX file.

    Args:
        input_file: Path to the .docx file.
        preview_len: Number of characters to include in preview (0 = no preview).

    Returns:
        Tuple of (stats_dict, message_string).
        stats_dict is None on error.
    """
    input_path = Path(input_file)

    if not input_path.exists():
        return None, f"Error: File not found: {input_file}"

    suffix = input_path.suffix.lower()
    if suffix not in (".docx", ".doc"):
        return None, f"Error: Unsupported file format: {suffix} (expected .docx or .doc)"

    if suffix == ".doc":
        return None, (
            "Error: .doc format requires conversion to .docx first. "
            "Use: python3 convert_docx.py input.doc --to docx --output converted.docx"
        )

    try:
        paragraphs_text, full_text = _extract_text_from_docx(input_path)
    except zipfile.BadZipFile:
        return None, f"Error: File is not a valid DOCX (ZIP) file: {input_file}"
    except Exception as e:
        return None, f"Error: Failed to read file: {e}"

    stats = _compute_stats(full_text, paragraphs_text)

    if preview_len > 0:
        stats["preview"] = full_text[:preview_len]

    return stats, "OK"


def _extract_text_from_docx(docx_path: Path) -> tuple[list[str], str]:
    """Extract text from a DOCX file.

    Returns:
        Tuple of (list of paragraph texts, full concatenated text).
    """
    with zipfile.ZipFile(docx_path, "r") as zf:
        if "word/document.xml" not in zf.namelist():
            raise ValueError("No word/document.xml found in DOCX")
        with zf.open("word/document.xml") as f:
            dom = defusedxml.minidom.parseString(f.read())

    paragraphs = dom.getElementsByTagNameNS(WORD_NS, "p")
    paragraphs_text = []

    for para in paragraphs:
        t_nodes = para.getElementsByTagNameNS(WORD_NS, "t")
        para_text = ""
        for t_node in t_nodes:
            if t_node.firstChild and t_node.firstChild.data:
                para_text += t_node.firstChild.data
        paragraphs_text.append(para_text)

    full_text = "".join(paragraphs_text)
    return paragraphs_text, full_text


def _compute_stats(full_text: str, paragraphs_text: list[str]) -> dict:
    """Compute detailed word/character statistics."""
    total_chars = len(full_text)
    chars_no_space = len(full_text.replace(" ", "").replace("\u3000", ""))

    chinese_chars = len(re.findall(r"[\u4e00-\u9fff]", full_text))
    english_words = len(re.findall(r"[a-zA-Z]+", full_text))
    digit_groups = len(re.findall(r"[0-9]+", full_text))
    punctuation = len(re.findall(
        r"[，。、；：？！\u201c\u201d\u2018\u2019（）《》【】—…·.,;:!?\"'(){}\[\]]",
        full_text,
    ))

    non_empty_paragraphs = [p for p in paragraphs_text if p.strip()]
    paragraph_count = len(non_empty_paragraphs)

    estimated_pages = max(1, math.ceil(chars_no_space / CHARS_PER_PAGE))

    return {
        "total_chars": total_chars,
        "total_chars_no_space": chars_no_space,
        "chinese_chars": chinese_chars,
        "english_words": english_words,
        "digit_groups": digit_groups,
        "punctuation": punctuation,
        "paragraphs": paragraph_count,
        "estimated_pages": estimated_pages,
    }


def _format_table(stats: dict) -> str:
    """Format stats as a readable table string."""
    lines = [
        "=== 文档字数统计 ===",
        f"总字符数（含空格）:   {stats['total_chars']:,}",
        f"总字符数（不含空格）: {stats['total_chars_no_space']:,}",
        f"中文字数:             {stats['chinese_chars']:,}",
        f"英文单词数:           {stats['english_words']:,}",
        f"数字串数:             {stats['digit_groups']:,}",
        f"标点符号数:           {stats['punctuation']:,}",
        f"段落数:               {stats['paragraphs']:,}",
        f"预估页数（A4）:       ~{stats['estimated_pages']} 页",
    ]

    if "preview" in stats:
        lines.append(f"\n--- 前 {len(stats['preview'])} 字预览 ---")
        lines.append(stats["preview"])

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Count words and characters in a Word document"
    )
    parser.add_argument("input_file", help="Input DOCX file")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--preview",
        type=int,
        default=0,
        help="Include first N characters as preview (default: 0, no preview)",
    )
    args = parser.parse_args()

    stats, message = count_words(args.input_file, preview_len=args.preview)

    if stats is None:
        print(message, file=sys.stderr)
        raise SystemExit(1)

    if args.format == "json":
        stats["file"] = args.input_file
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        print(_format_table(stats))


if __name__ == "__main__":
    main()
