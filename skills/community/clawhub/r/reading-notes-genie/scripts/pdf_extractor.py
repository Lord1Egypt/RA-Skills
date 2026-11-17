#!/usr/bin/env python3
"""
pdf_extractor.py — PDF 文字萃取器
支援：加密 PDF、圖片掃描（OCR）、多欄排版、書籤導航
依賴：pypdf（純 Python）、pdfplumber（文字+表格）、Pillow+tesseract（OCR）
"""

import sys
import json
import argparse
import io
from pathlib import Path
from typing import Optional

# ── 依賴偵測 ─────────────────────────────────────────────────────────────────
def _has(mod: str) -> bool:
    try:
        __import__(mod); return True
    except ImportError:
        return False

HAS_PDFPLUMBER = _has("pdfplumber")
HAS_PYPDF      = _has("pypdf")
HAS_PIL        = _has("PIL")
HAS_TESSERACT  = _has("pytesseract")

if HAS_PIL and HAS_TESSERACT:
    import pytesseract
    from PIL import Image


# ── PDF 結構 ─────────────────────────────────────────────────────────────────

class PDFExtractionResult:
    def __init__(self, path: str):
        self.path       = Path(path)
        self.pages: list[dict] = []   # [{page_num, text, chars, tables}]
        self.metadata: dict         = {}
        self.outline: list[dict]   = []   # 書籤 [{title, level, page}]
        self.is_encrypted: bool     = False
        self.warnings: list[str]    = []

    def add_page(self, num: int, text: str, tables: list[list] = None):
        self.pages.append({
            "page_num": num,
            "text": text,
            "chars": len(text),
            "tables": tables or [],
        })

    def total_chars(self) -> int:
        return sum(p["chars"] for p in self.pages)

    def to_dict(self) -> dict:
        return {
            "metadata": self.metadata,
            "outline": self.outline,
            "pages_summary": [
                {"page_num": p["page_num"], "chars": p["chars"], "tables": len(p["tables"])}
                for p in self.pages
            ],
            "total_pages": len(self.pages),
            "total_chars": self.total_chars(),
            "is_encrypted": self.is_encrypted,
        }


# ── 文字萃取 ─────────────────────────────────────────────────────────────────

def _extract_with_pypdf(result: PDFExtractionResult):
    """pypdf 萃取（書籤 + 基本文字）"""
    from pypdf import PdfReader

    reader = PdfReader(result.path)

    # Metadata
    meta = reader.metadata
    if meta:
        result.metadata = {
            "title":   getattr(meta, "title",   "") or "",
            "author":  getattr(meta, "author",  "") or "",
            "subject": getattr(meta, "subject", "") or "",
            "creator": getattr(meta, "creator", "") or "",
        }

    # 加密
    result.is_encrypted = reader.is_encrypted
    if reader.is_encrypted and not reader.decrypt(""):
        result.warnings.append("PDF 已加密且無法自動解密，需要密碼")
        return

    # Outline（書籤）
    try:
        def walk_outline(item, level=0):
            items = []
            if hasattr(item, "destination"):
                dest = item.destination
                title = dest.get("/Title", "")
                if callable(title):
                    title = str(title())
                result.outline.append({
                    "title": title,
                    "level": level,
                    "page": dest.page.number + 1 if dest.page else 0,
                })
                items.append(title)
            if hasattr(item, "kids"):
                for child in item.kids:
                    items.extend(walk_outline(child, level + 1))
            return items
        if reader.outline:
            for top in reader.outline:
                walk_outline(top)
    except Exception:
        pass

    # 文字萃取（每頁）
    if HAS_PDFPLUMBER:
        _extract_with_pdfplumber(result)
    else:
        for i, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            result.add_page(i, text)


def _extract_with_pdfplumber(result: PDFExtractionResult):
    """pdfplumber 萃取（更好的文字 + 表格）"""
    import pdfplumber

    with pdfplumber.open(result.path) as pdf:
        result.metadata.setdefault("title",   str(result.path.stem))

        for i, page in enumerate(pdf.pages, 1):
            # 表格
            tables: list[list[list[str]]] = page.extract_tables() or []

            # 文字
            text = page.extract_text() or ""

            # 若文字太少，嘗試 OCR
            if len(text.strip()) < 50 and HAS_PIL and HAS_TESSERACT:
                ocr_text = _ocr_page_image(result.path, i)
                if ocr_text:
                    text = f"[OCR]\n{ocr_text}"
                    result.warnings.append(f"第 {i} 頁使用 OCR 萃取")

            result.add_page(i, text, tables)


def _ocr_page_image(pdf_path: Path, page_num: int) -> str:
    """將 PDF 頁面轉圖片後 OCR"""
    try:
        import subprocess
        # 用 pdftoppm（poppler-utils）轉圖片
        result = subprocess.run(
            ["pdftoppm", "-f", str(page_num), "-l", str(page_num),
             "-png", "-r", "200", str(pdf_path), "/tmp/ocr_page"],
            capture_output=True, timeout=30
        )
        img_path = Path(f"/tmp/ocr_page-{page_num:04d}.png")
        if not img_path.exists():
            # fallback: 用 pypdf 轉
            return ""
        image = Image.open(img_path)
        text = pytesseract.image_to_string(image, lang="chi_sim+eng")
        img_path.unlink(missing_ok=True)
        return text
    except Exception:
        return ""


def _extract_by_pdftotext(result: PDFExtractionResult):
    """pdftotext CLI 工具（最穩定的 fallback）"""
    import subprocess
    try:
        proc = subprocess.run(
            ["pdftotext", "-layout", str(result.path), "-"],
            capture_output=True, timeout=60
        )
        if proc.returncode == 0:
            raw = proc.stdout.decode("utf-8", errors="replace")
            # 按頁分段（簡單 heuristic：換頁 + 連續大寫）
            pages = raw.split("\f")
            for i, pg in enumerate(pages, 1):
                pg = pg.strip()
                if pg:
                    result.add_page(i, pg)
        else:
            result.warnings.append(f"pdftotext failed: {proc.stderr.decode()}")
    except FileNotFoundError:
        result.warnings.append("pdftotext 未安裝（poppler-utils）")
    except Exception as e:
        result.warnings.append(f"pdftotext error: {e}")


# ── 主程式 ─────────────────────────────────────────────────────────────────────

def extract_pdf(path: str) -> PDFExtractionResult:
    result = PDFExtractionResult(path)

    if not result.path.exists():
        result.warnings.append(f"檔案不存在：{path}")
        return result

    size_mb = result.path.stat().st_size / 1024 / 1024
    if size_mb > 50:
        result.warnings.append(f"PDF 大小 {size_mb:.1f} MB，大檔案萃取時間較長")

    if HAS_PYPDF:
        _extract_with_pypdf(result)
    elif _has("pypdf"):
        _extract_with_pypdf(result)
    else:
        _extract_by_pdftotext(result)

    # 最終 fallback：直接用 pdftotext
    if not result.pages and not result.warnings:
        _extract_by_pdftotext(result)

    return result


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PDF 文字萃取工具")
    parser.add_argument("file", help="PDF 檔案路徑")
    parser.add_argument("--output", "-o", help="JSON 輸出路徑")
    parser.add_argument("--pages", action="store_true", help="包含每頁完整文字")
    parser.add_argument("--no-ocr", dest="no_ocr", action="store_true",
                        help="停用 OCR（加速）")
    args = parser.parse_args()

    # 全域停用 OCR
    if args.no_ocr:
        global HAS_PIL, HAS_TESSERACT
        HAS_PIL = False; HAS_TESSERACT = False

    result = extract_pdf(args.file)

    # 摘要輸出
    print(f"📄 {result.path.name}")
    print(f"   頁數：{result.total_pages}")
    print(f"   總字數：{result.total_chars():,}")
    if result.is_encrypted:
        print("   🔒 已加密")
    for w in result.warnings:
        print(f"   ⚠️  {w}")

    # Outline
    if result.outline:
        print("   📑 書籤：")
        for b in result.outline[:10]:
            indent = "  " * b["level"]
            print(f"     {indent}· {b['title']} (p.{b['page']})")
        if len(result.outline) > 10:
            print(f"     ... 共 {len(result.outline)} 個書籤")

    # 輸出 JSON
    out = result.to_dict()
    if args.pages:
        out["pages"] = result.pages

    if args.output:
        Path(args.output).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n✅ 已寫入：{args.output}")
    else:
        print("\n" + json.dumps(out, ensure_ascii=False, indent=2)[:3000])


if __name__ == "__main__":
    main()
