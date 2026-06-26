# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pdfplumber>=0.10.0",
#     "Pillow>=10.0.0",
#     "pytesseract>=0.3.10",
#     "pdf2image>=1.17.0",
# ]
# ///
"""
Shared OCR and text extraction utilities for accounting document processing.

Supports:
- Digital PDFs (text-layer extraction via pdfplumber)
- Scanned PDFs (image conversion + OCR via pdf2image + pytesseract)
- Image files: JPG, JPEG, PNG, TIFF, BMP (direct OCR via pytesseract)

Dependencies:
- System: tesseract-ocr, tesseract-ocr-vie (for Vietnamese), poppler-utils (for pdf2image)
- Python: pdfplumber, Pillow, pytesseract, pdf2image
"""

from __future__ import annotations

import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


@dataclass
class OCRResult:
    """Result of text extraction from a document."""
    text: str
    pages: list[str]
    tables: list[list]
    method: str  # "pdfplumber", "ocr", "hybrid"
    confidence: float  # 0-100 estimated quality
    source_file: str


def _check_tesseract() -> bool:
    """Check if tesseract is available."""
    import shutil
    return shutil.which("tesseract") is not None


def _check_poppler() -> bool:
    """Check if poppler-utils (pdftoppm) is available for pdf2image."""
    import shutil
    return shutil.which("pdftoppm") is not None


def _get_tesseract_langs() -> list[str]:
    """Get list of installed tesseract languages."""
    import subprocess
    try:
        result = subprocess.run(
            ["tesseract", "--list-langs"],
            capture_output=True, text=True, timeout=10,
        )
        langs = result.stdout.strip().split("\n")[1:]  # skip header line
        return [l.strip() for l in langs if l.strip()]
    except Exception:
        return []


def _build_lang_string() -> str:
    """Build tesseract language string, preferring vie+eng if available."""
    langs = _get_tesseract_langs()
    parts = []
    if "vie" in langs:
        parts.append("vie")
    if "eng" in langs:
        parts.append("eng")
    return "+".join(parts) if parts else "eng"


def extract_text_pdfplumber(pdf_path: str) -> tuple[list[str], list[list]]:
    """Extract text and tables from PDF using pdfplumber (works on digital PDFs)."""
    import pdfplumber

    pages = []
    tables = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            pages.append(page_text or "")
            page_tables = page.extract_tables()
            if page_tables:
                tables.extend(page_tables)
    return pages, tables


def extract_text_ocr_image(image_path: str) -> tuple[str, float]:
    """OCR a single image file. Returns (text, confidence)."""
    import pytesseract
    from PIL import Image

    if not _check_tesseract():
        eprint("ERROR: tesseract is not installed. Install with: sudo apt install tesseract-ocr tesseract-ocr-vie")
        return "", 0.0

    lang = _build_lang_string()
    img = Image.open(image_path)

    # Pre-process for better OCR: convert to grayscale, increase contrast
    img = img.convert("L")

    # Get text with confidence data
    data = pytesseract.image_to_data(img, lang=lang, output_type=pytesseract.Output.DICT)
    text = pytesseract.image_to_string(img, lang=lang)

    # Calculate average confidence from word-level data
    confidences = [int(c) for c in data["conf"] if int(c) > 0]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    return text, avg_confidence


def extract_text_ocr_pdf(pdf_path: str) -> tuple[list[str], float]:
    """OCR a scanned PDF by converting pages to images first."""
    if not _check_poppler():
        eprint("ERROR: poppler-utils not installed. Install with: sudo apt install poppler-utils")
        return [], 0.0

    from pdf2image import convert_from_path

    images = convert_from_path(pdf_path, dpi=300)
    pages = []
    confidences = []

    for i, img in enumerate(images):
        # Save temp image for OCR
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
            img.save(tmp.name, "PNG")
            text, conf = extract_text_ocr_image(tmp.name)
            pages.append(text)
            confidences.append(conf)
            os.unlink(tmp.name)

    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
    return pages, avg_conf


def extract_from_file(file_path: str) -> OCRResult:
    """
    Extract text from any supported document file.

    Strategy:
    1. For PDFs: try pdfplumber first (digital layer). If little text found,
       fall back to OCR (scanned PDF).
    2. For images: direct OCR.
    3. Returns OCRResult with text, tables, method used, and confidence.
    """
    file_path = os.path.abspath(file_path)
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        # Try digital extraction first
        pages, tables = extract_text_pdfplumber(file_path)
        full_text = "\n".join(pages)

        # Heuristic: if less than 50 chars per page on average, likely scanned
        avg_chars = len(full_text.strip()) / max(len(pages), 1)
        if avg_chars > 50:
            # Good digital text
            confidence = min(98.0, 70.0 + avg_chars / 20)
            return OCRResult(
                text=full_text,
                pages=pages,
                tables=tables,
                method="pdfplumber",
                confidence=round(confidence, 1),
                source_file=file_path,
            )

        # Scanned PDF — fall back to OCR
        eprint(f"Low text from pdfplumber ({avg_chars:.0f} chars/page), falling back to OCR...")
        ocr_pages, ocr_conf = extract_text_ocr_pdf(file_path)

        if ocr_pages and sum(len(p) for p in ocr_pages) > len(full_text.strip()):
            return OCRResult(
                text="\n".join(ocr_pages),
                pages=ocr_pages,
                tables=tables,  # Keep any tables from pdfplumber
                method="ocr",
                confidence=round(ocr_conf, 1),
                source_file=file_path,
            )

        # Hybrid: use whatever gave more text
        return OCRResult(
            text=full_text if full_text.strip() else "\n".join(ocr_pages),
            pages=pages if full_text.strip() else ocr_pages,
            tables=tables,
            method="hybrid",
            confidence=round(max(ocr_conf, 50.0), 1),
            source_file=file_path,
        )

    elif ext in (".jpg", ".jpeg", ".png", ".tiff", ".bmp"):
        text, confidence = extract_text_ocr_image(file_path)
        return OCRResult(
            text=text,
            pages=[text],
            tables=[],
            method="ocr",
            confidence=round(confidence, 1),
            source_file=file_path,
        )

    else:
        eprint(f"Unsupported file type: {ext}")
        return OCRResult(
            text="", pages=[], tables=[], method="none",
            confidence=0.0, source_file=file_path,
        )


# ─── Amount / Date Cleaning Utilities ───────────────────────────────────────

def clean_amount(text: str) -> float:
    """Clean a currency amount string into a float.

    Handles:
    - Vietnamese VND: 1.000.000 or 1,000,000 (no decimals)
    - International: 1,000.50 or 1.000,50
    - Currency symbols: VND, đ, $, €, £
    - Negative in parentheses: (500.000)
    """
    if not text:
        return 0.0
    cleaned = re.sub(r"[VNDvndđĐ$€£\s]", "", str(text).strip())
    is_negative = "(" in cleaned and ")" in cleaned
    cleaned = cleaned.replace("(", "").replace(")", "")

    if "." in cleaned and "," in cleaned:
        if cleaned.rindex(".") > cleaned.rindex(","):
            cleaned = cleaned.replace(",", "")
        else:
            cleaned = cleaned.replace(".", "").replace(",", ".")
    elif "." in cleaned:
        parts = cleaned.split(".")
        if len(parts) > 2 or (len(parts) == 2 and len(parts[-1]) == 3):
            cleaned = cleaned.replace(".", "")
    elif "," in cleaned:
        parts = cleaned.split(",")
        if len(parts) > 2 or (len(parts) == 2 and len(parts[-1]) == 3):
            cleaned = cleaned.replace(",", "")
        else:
            cleaned = cleaned.replace(",", ".")

    cleaned = re.sub(r"[^\d.\-]", "", cleaned)
    try:
        val = float(cleaned)
        return -val if is_negative else val
    except ValueError:
        return 0.0


def parse_date(text: str) -> str:
    """Parse a date string into YYYY-MM-DD format.

    Supports: dd/mm/yyyy, dd-mm-yyyy, dd.mm.yyyy, mm/dd/yyyy, yyyy-mm-dd
    """
    if not text:
        return ""
    text = text.strip()
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return text


def check_system_deps() -> dict:
    """Check all system dependencies and return status report."""
    import shutil
    report = {
        "tesseract": shutil.which("tesseract") is not None,
        "tesseract_langs": _get_tesseract_langs() if shutil.which("tesseract") else [],
        "poppler": shutil.which("pdftoppm") is not None,
    }
    report["vie_support"] = "vie" in report["tesseract_langs"]
    report["ready"] = report["tesseract"] and report["poppler"]
    return report


if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="OCR utilities for accounting documents")
    sub = parser.add_subparsers(dest="command")

    # Check dependencies
    sub.add_parser("check", help="Check system dependencies")

    # Extract text
    ext = sub.add_parser("extract", help="Extract text from a file")
    ext.add_argument("file", help="File to extract text from")
    ext.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.command == "check":
        report = check_system_deps()
        print(json.dumps(report, indent=2))
        if not report["ready"]:
            eprint("\nMissing dependencies. Install with:")
            if not report["tesseract"]:
                eprint("  sudo apt install tesseract-ocr tesseract-ocr-vie")
            if not report["poppler"]:
                eprint("  sudo apt install poppler-utils")
            sys.exit(1)
        else:
            eprint("All dependencies OK.")
            if not report["vie_support"]:
                eprint("  Note: Vietnamese language pack not installed. Run: sudo apt install tesseract-ocr-vie")

    elif args.command == "extract":
        result = extract_from_file(args.file)
        if args.json:
            print(json.dumps({
                "text": result.text,
                "pages": len(result.pages),
                "tables": len(result.tables),
                "method": result.method,
                "confidence": result.confidence,
                "source_file": result.source_file,
            }, ensure_ascii=False, indent=2))
        else:
            print(result.text)
            eprint(f"\n--- Method: {result.method} | Confidence: {result.confidence}% | Pages: {len(result.pages)} | Tables: {len(result.tables)} ---")

    else:
        parser.print_help()
