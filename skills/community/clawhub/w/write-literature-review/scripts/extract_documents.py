#!/usr/bin/env python3
"""Extract PDF, Word, CAJ-family and CNKI export files to UTF-8 text."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


SUPPORTED = {
    ".pdf", ".docx", ".doc", ".caj", ".nh", ".kdh",
    ".txt", ".ris", ".enw", ".nbib", ".xml",
}
CNKI_EXPORTS = {".txt", ".ris", ".enw", ".nbib", ".xml"}
CAJ_FAMILY = {".caj", ".nh", ".kdh"}
W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def command_exists(name: str) -> bool:
    return shutil.which(name) is not None


def run(command: list[str], timeout: int = 300) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        errors="replace",
        timeout=timeout,
        check=False,
    )


def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip() + ("\n" if text.strip() else "")


def looks_usable(text: str, minimum: int = 200) -> bool:
    compact = re.sub(r"\s+", "", text)
    if len(compact) < minimum:
        return False
    replacement_ratio = compact.count("\ufffd") / max(len(compact), 1)
    return replacement_ratio < 0.02


def decode_text_file(path: Path) -> tuple[str, str]:
    raw = path.read_bytes()
    for encoding in ("utf-8-sig", "gb18030", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            text = raw.decode(encoding)
        except UnicodeDecodeError:
            continue
        if "\x00" not in text[:1000] or encoding.startswith("utf-16"):
            return clean_text(text), encoding
    return clean_text(raw.decode("utf-8", errors="replace")), "utf-8-replace"


def extract_docx(path: Path) -> tuple[str, str, list[str]]:
    if not zipfile.is_zipfile(path):
        raise ValueError("文件不是有效的 DOCX/OOXML 压缩包")
    parts = [
        "word/document.xml",
        "word/footnotes.xml",
        "word/endnotes.xml",
    ]
    blocks: list[str] = []
    warnings: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        if "word/document.xml" not in names:
            raise ValueError("DOCX 缺少 word/document.xml")
        for part in parts:
            if part not in names:
                continue
            root = ET.fromstring(archive.read(part))
            for paragraph in root.iter(W_NS + "p"):
                chunks: list[str] = []
                for node in paragraph.iter():
                    if node.tag == W_NS + "t" and node.text:
                        chunks.append(node.text)
                    elif node.tag == W_NS + "tab":
                        chunks.append("\t")
                    elif node.tag in {W_NS + "br", W_NS + "cr"}:
                        chunks.append("\n")
                content = "".join(chunks).strip()
                if content:
                    blocks.append(content)
            if part != "word/document.xml":
                warnings.append(f"已提取 {part}")
    text = clean_text("\n\n".join(blocks))
    return text, "stdlib-ooxml", warnings


def extract_pdf_native(path: Path, work_dir: Path) -> tuple[str, str, list[str]]:
    warnings: list[str] = []
    if command_exists("pdftotext"):
        output = work_dir / "pdftotext.txt"
        result = run(["pdftotext", "-layout", "-enc", "UTF-8", str(path), str(output)])
        if result.returncode == 0 and output.exists():
            text = clean_text(output.read_text(encoding="utf-8", errors="replace"))
            if text:
                return text, "pdftotext-layout", warnings
        warnings.append(f"pdftotext 失败: {result.stderr.strip()[:300]}")

    if importlib.util.find_spec("pypdf"):
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        if reader.is_encrypted:
            try:
                reader.decrypt("")
            except Exception as exc:
                raise ValueError(f"PDF 已加密且无法读取: {exc}") from exc
        text = clean_text("\n\n".join((page.extract_text() or "") for page in reader.pages))
        if text:
            return text, "pypdf", warnings

    if importlib.util.find_spec("pdfplumber"):
        import pdfplumber  # type: ignore

        with pdfplumber.open(path) as pdf:
            text = clean_text("\n\n".join((page.extract_text() or "") for page in pdf.pages))
        if text:
            return text, "pdfplumber", warnings

    raise ValueError("没有可用的 PDF 文本提取器；请安装 poppler-utils、pypdf 或 pdfplumber")


def ocr_pdf(path: Path, work_dir: Path) -> tuple[str, str, list[str]]:
    if not command_exists("pdftoppm") or not command_exists("tesseract"):
        raise ValueError("OCR 需要 pdftoppm 和 tesseract")
    prefix = work_dir / "page"
    rendered = run(["pdftoppm", "-png", "-r", "220", str(path), str(prefix)], timeout=900)
    if rendered.returncode != 0:
        raise ValueError(f"PDF 页面渲染失败: {rendered.stderr.strip()[:400]}")
    images = sorted(work_dir.glob("page-*.png"))
    if not images:
        raise ValueError("PDF 页面渲染后未生成图片")
    pages = []
    warnings = ["文本来自 OCR，关键数字、公式和专有名词必须回到原页核验"]
    for image in images:
        result = run(["tesseract", str(image), "stdout", "-l", "chi_sim+eng"], timeout=300)
        if result.returncode != 0:
            result = run(["tesseract", str(image), "stdout", "-l", "eng"], timeout=300)
        if result.returncode != 0:
            warnings.append(f"{image.name} OCR 失败")
            continue
        pages.append(result.stdout)
    text = clean_text("\n\n".join(pages))
    if not text:
        raise ValueError("OCR 未提取到文本")
    return text, "tesseract-ocr", warnings


def extract_pdf(path: Path, work_dir: Path, allow_ocr: bool) -> tuple[str, str, list[str]]:
    try:
        text, method, warnings = extract_pdf_native(path, work_dir)
    except Exception as native_error:
        if allow_ocr:
            text, method, warnings = ocr_pdf(path, work_dir)
            warnings.insert(0, f"原生文本提取失败: {native_error}")
            return text, method, warnings
        raise
    if looks_usable(text):
        return text, method, warnings
    warnings.append("原生提取文本过短，文档可能是扫描件")
    if allow_ocr:
        ocr_text, ocr_method, ocr_warnings = ocr_pdf(path, work_dir)
        if len(re.sub(r"\s+", "", ocr_text)) > len(re.sub(r"\s+", "", text)):
            return ocr_text, ocr_method, warnings + ocr_warnings
    return text, method, warnings


def extract_legacy_doc(path: Path, work_dir: Path) -> tuple[str, str, list[str]]:
    if command_exists("antiword"):
        result = run(["antiword", str(path)])
        if result.returncode == 0 and result.stdout.strip():
            return clean_text(result.stdout), "antiword", []
    if command_exists("catdoc"):
        result = run(["catdoc", str(path)])
        if result.returncode == 0 and result.stdout.strip():
            return clean_text(result.stdout), "catdoc", []
    office = shutil.which("libreoffice") or shutil.which("soffice")
    if office:
        result = run([
            office, "--headless", "--convert-to", "txt:Text",
            "--outdir", str(work_dir), str(path),
        ], timeout=300)
        output = work_dir / f"{path.stem}.txt"
        if result.returncode == 0 and output.exists():
            text, encoding = decode_text_file(output)
            if text:
                return text, f"libreoffice-{encoding}", []
    raise ValueError("旧版 DOC 需要 antiword、catdoc 或 LibreOffice")


def convert_caj(path: Path, work_dir: Path) -> tuple[Path, str]:
    with path.open("rb") as stream:
        signature = stream.read(5)
    if signature == b"%PDF-":
        return path, "pdf-disguised"
    tool = shutil.which("caj2pdf")
    if not tool:
        raise ValueError("CAJ/NH/KDH 需要 caj2pdf；也可先在知网阅读器中导出为 PDF")
    output = work_dir / f"{path.stem}.pdf"
    result = run([tool, "convert", str(path), "-o", str(output)], timeout=900)
    if result.returncode != 0 or not output.exists():
        raise ValueError(f"caj2pdf 转换失败: {result.stderr.strip()[:400]}")
    return output, "caj2pdf"


def unique_output(stem: str, output_dir: Path, used: set[str]) -> Path:
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]+', "_", stem).strip(" .") or "document"
    candidate = safe
    index = 2
    while candidate.lower() in used:
        candidate = f"{safe}-{index}"
        index += 1
    used.add(candidate.lower())
    return output_dir / f"{candidate}.txt"


def collect_inputs(items: list[Path]) -> list[Path]:
    files: list[Path] = []
    for item in items:
        if item.is_dir():
            files.extend(path for path in item.rglob("*") if path.is_file())
        elif item.is_file():
            files.append(item)
    return sorted(dict.fromkeys(path.resolve() for path in files))


def process(path: Path, output: Path, allow_ocr: bool) -> dict[str, object]:
    suffix = path.suffix.lower()
    record: dict[str, object] = {
        "source": str(path),
        "format": suffix.lstrip(".") or "unknown",
        "status": "failed",
        "method": None,
        "output": None,
        "characters": 0,
        "full_text_likelihood": "unknown",
        "warnings": [],
        "error": None,
    }
    if suffix not in SUPPORTED:
        record["status"] = "unsupported"
        record["error"] = "不支持的文件格式"
        return record

    try:
        with tempfile.TemporaryDirectory(prefix="review-extract-") as temp:
            work_dir = Path(temp)
            if suffix == ".pdf":
                text, method, warnings = extract_pdf(path, work_dir, allow_ocr)
                likelihood = "likely-full-text"
            elif suffix == ".docx":
                text, method, warnings = extract_docx(path)
                likelihood = "likely-full-text"
            elif suffix == ".doc":
                text, method, warnings = extract_legacy_doc(path, work_dir)
                likelihood = "likely-full-text"
            elif suffix in CAJ_FAMILY:
                pdf, converter = convert_caj(path, work_dir)
                text, pdf_method, warnings = extract_pdf(pdf, work_dir, allow_ocr)
                method = f"{converter}+{pdf_method}"
                likelihood = "likely-full-text"
            else:
                text, encoding = decode_text_file(path)
                method = f"text-{encoding}"
                warnings = ["知网题录文件可能仅含元数据和摘要，不得标记为全文已读"]
                likelihood = "metadata-or-abstract"

        text = clean_text(text)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="utf-8")
        characters = len(text)
        status = "success" if looks_usable(text) else "warning"
        if not text:
            status = "failed"
            warnings.append("未提取到文本")
        record.update({
            "status": status,
            "method": method,
            "output": str(output.resolve()) if text else None,
            "characters": characters,
            "full_text_likelihood": likelihood,
            "warnings": warnings,
        })
    except Exception as exc:
        record["error"] = str(exc)
    return record


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path, help="Files or directories")
    parser.add_argument("--out-dir", type=Path, required=True, help="Output directory")
    parser.add_argument("--ocr", action="store_true", help="OCR scanned PDFs when possible")
    args = parser.parse_args()

    files = collect_inputs(args.inputs)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    text_dir = args.out_dir / "texts"
    used: set[str] = set()
    records = []
    for source in files:
        output = unique_output(source.stem, text_dir, used)
        records.append(process(source, output, args.ocr))

    summary = {
        "total": len(records),
        "success": sum(item["status"] == "success" for item in records),
        "warning": sum(item["status"] == "warning" for item in records),
        "failed": sum(item["status"] == "failed" for item in records),
        "unsupported": sum(item["status"] == "unsupported" for item in records),
    }
    manifest = {"summary": summary, "documents": records}
    manifest_path = args.out_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False))
    print(manifest_path.resolve())
    if summary["failed"] or summary["unsupported"]:
        sys.exit(2)


if __name__ == "__main__":
    main()
