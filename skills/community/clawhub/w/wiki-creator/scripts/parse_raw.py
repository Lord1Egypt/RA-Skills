"""parse_raw.py — 多格式解析 → 干净 markdown

支持格式:
    .pdf, .xlsx, .xls, .csv, .docx, .doc, .pptx, .md, .txt, .json, .html

用法:
    python parse_raw.py <file> [--raw-root <raw-root>]

输出到 stdout：解析后的干净 markdown（含 §章节 标记，便于 LLM 在页面中标注来源 §<章节>）。

依赖（按需安装）：
    pip install pypdf openpyxl python-docx python-pptx beautifulsoup4

若依赖缺失，会回退到纯文本读取并提示。
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

# Windows 默认 stdout 是 GBK，强制 utf-8 输出，避免 UnicodeEncodeError
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _try_import(name: str):
    try:
        return __import__(name)
    except ImportError:
        return None


def parse_pdf(path: Path) -> str:
    pypdf = _try_import("pypdf")
    if pypdf is None:
        return _fallback_text(path, "pypdf 未安装")
    reader = pypdf.PdfReader(str(path))
    parts = []
    for i, page in enumerate(reader.pages, 1):
        text = page.extract_text() or ""
        parts.append(f"## §page-{i}\n\n{text}\n")
    return "\n".join(parts)


def parse_xlsx(path: Path) -> str:
    openpyxl = _try_import("openpyxl")
    if openpyxl is None:
        return _fallback_text(path, "openpyxl 未安装")
    wb = openpyxl.load_workbook(str(path), data_only=True)
    parts = []
    for sheet in wb.worksheets:
        parts.append(f"## §sheet-{sheet.title}\n")
        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            continue
        # markdown 表格
        header = rows[0]
        parts.append("| " + " | ".join(_cell(c) for c in header) + " |")
        parts.append("|" + "|".join("---" for _ in header) + "|")
        for row in rows[1:]:
            # 对齐列数
            cells = list(row) + [None] * (len(header) - len(row))
            parts.append("| " + " | ".join(_cell(c) for c in cells[: len(header)]) + " |")
        parts.append("")
    return "\n".join(parts)


def parse_csv(path: Path) -> str:
    parts = ["## §table\n"]
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return ""
    header = rows[0]
    parts.append("| " + " | ".join(header) + " |")
    parts.append("|" + "|".join("---" for _ in header) + "|")
    for row in rows[1:]:
        cells = list(row) + [""] * (len(header) - len(row))
        parts.append("| " + " | ".join(cells[: len(header)]) + " |")
    parts.append("")
    return "\n".join(parts)


def parse_docx(path: Path) -> str:
    docx = _try_import("docx")
    if docx is None:
        return _fallback_text(path, "python-docx 未安装")
    doc = docx.Document(str(path))
    parts = []
    section_idx = 0
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        if para.style and para.style.name.startswith("Heading"):
            section_idx += 1
            parts.append(f"## §heading-{section_idx} {text}\n")
        else:
            parts.append(text)
    return "\n".join(parts)


def parse_pptx(path: Path) -> str:
    pptx = _try_import("pptx")
    if pptx is None:
        return _fallback_text(path, "python-pptx 未安装")
    prs = pptx.Presentation(str(path))
    parts = []
    for i, slide in enumerate(prs.slides, 1):
        parts.append(f"## §slide-{i}\n")
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    t = "".join(run.text for run in para.runs).strip()
                    if t:
                        parts.append(t)
        parts.append("")
    return "\n".join(parts)


def parse_html(path: Path) -> str:
    bs4 = _try_import("bs4")
    if bs4 is None:
        return _fallback_text(path, "beautifulsoup4 未安装")
    soup = bs4.BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text("\n")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    return "## §html-body\n\n" + "\n".join(lines)


def parse_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    # 给 markdown 标题加 §前缀，便于来源标注
    lines = text.splitlines()
    out = []
    sec = 0
    for ln in lines:
        if ln.startswith("#"):
            sec += 1
            out.append(f"## §heading-{sec} {ln.lstrip('#').strip()}\n")
        else:
            out.append(ln)
    return "\n".join(out)


def _cell(v) -> str:
    if v is None:
        return ""
    s = str(v).replace("\n", " ").replace("|", "\\|")
    return s


def _fallback_text(path: Path, reason: str) -> str:
    try:
        return f"## §raw\n\n（解析回退：{reason}）\n\n" + path.read_text(
            encoding="utf-8", errors="ignore"
        )
    except Exception as e:
        return f"## §raw\n\n（解析失败：{reason}；读取错误：{e}）\n"


PARSERS = {
    ".pdf": parse_pdf,
    ".xlsx": parse_xlsx,
    ".xls": parse_xlsx,
    ".csv": parse_csv,
    ".docx": parse_docx,
    ".doc": parse_docx,
    ".pptx": parse_pptx,
    ".html": parse_html,
    ".htm": parse_html,
    ".md": parse_text,
    ".markdown": parse_text,
    ".txt": parse_text,
    ".json": parse_text,
}


def parse(path: Path) -> str:
    ext = path.suffix.lower()
    parser = PARSERS.get(ext, parse_text)
    try:
        content = parser(path)
    except Exception as e:
        content = f"## §raw\n\n（解析异常：{e}）\n"
    header = f"# 源文件：{path.name}\n\n> 路径：raw/{path.name}\n> 解析器：{ext}\n\n"
    return header + content


def main() -> int:
    parser = argparse.ArgumentParser(description="解析 raw 文件 → 干净 markdown")
    parser.add_argument("file", help="raw 文件路径")
    parser.add_argument(
        "-o", "--output", help="输出到文件（utf-8）；不指定则输出到 stdout"
    )
    args = parser.parse_args()

    path = Path(args.file).expanduser().resolve()
    if not path.exists():
        print(f"错误：文件不存在 {path}", file=sys.stderr)
        return 1

    content = parse(path)
    if args.output:
        Path(args.output).write_text(content, encoding="utf-8")
        print(f"已写入 {args.output}（{len(content)} 字符）", file=sys.stderr)
    else:
        print(content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
