#!/usr/bin/env python3
"""Extract readable text from common input formats for distillation."""


try:
    import os as _boot_os, sys as _boot_sys
    _boot_sys.path.insert(0, _boot_os.path.dirname(_boot_os.path.abspath(__file__)))
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass

import argparse
import re
import sys
import zipfile
from pathlib import Path

import project_paths


def extract_txt(path):
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_docx(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8", "ignore")
    return "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", xml))


def extract_epub(path):
    import html

    parts = []
    with zipfile.ZipFile(path) as z:
        names = [n for n in z.namelist() if n.endswith((".html", ".xhtml", ".htm"))]
        for n in names:
            raw = z.read(n).decode("utf-8", "ignore")
            text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
            text = re.sub(r"\s+", " ", text).strip()
            if text:
                parts.append(text)
    return "\n\n".join(parts)


def extract_pdf(path):
    """PDF 抽取：pdftotext 走三级解析（env → PATH → codex runtime）。"""
    import subprocess

    exe, source = project_paths.find_pdftotext()
    if not exe:
        print(project_paths.pdftotext_help(), file=sys.stderr)
        raise SystemExit(3)
    out = subprocess.run(
        [exe, "-layout", str(path), "-"],
        capture_output=True,
        text=True,
    )
    if out.returncode != 0 and not out.stdout.strip():
        print(f"[PDF_EXTRACT_EMPTY] pdftotext rc={out.returncode} ({source})", file=sys.stderr)
        print((out.stderr or "").strip()[:400], file=sys.stderr)
    return out.stdout


def extract_mobi(path):
    try:
        import mobi

        tempdir, filepath = mobi.extract(str(path))
        return Path(filepath).read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return f"[MOBI_EXTRACT_FAILED] {exc}\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    path = Path(args.input)
    suffix = path.suffix.lower()
    if suffix == ".txt" or suffix == ".md":
        text = extract_txt(path)
    elif suffix == ".docx":
        text = extract_docx(path)
    elif suffix == ".epub":
        text = extract_epub(path)
    elif suffix == ".pdf":
        text = extract_pdf(path)
    elif suffix == ".mobi":
        text = extract_mobi(path)
    elif suffix in (".srt", ".vtt"):
        text = extract_txt(path)
    else:
        print(f"UNSUPPORTED {suffix}; provide TXT/MD/EPUB/PDF/DOCX/MOBI/SRT/VTT")
        return

    clean = re.sub(r"\n{3,}", "\n\n", text).strip()
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(clean, encoding="utf-8")
    print("clean chars", len(clean))
    print("output", out)


if __name__ == "__main__":
    main()
