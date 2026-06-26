# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pdfplumber>=0.10.0",
#     "Pillow>=10.0.0",
#     "pytesseract>=0.3.10",
#     "pdf2image>=1.17.0",
# ]
# ///
"""Classify accounting documents (Invoice/PO/Statement/Other) and route to the right extractor.

Usage:
  uv run classify_document.py /path/to/document.pdf
  uv run classify_document.py document.pdf --classify-only
  uv run classify_document.py document.pdf --output-dir ~/accounting/
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ocr_utils import eprint, extract_from_file

# Classification keywords with weights
INVOICE_KEYWORDS = {
    "hóa đơn giá trị gia tăng": 20, "hóa đơn gtgt": 20,
    "hóa đơn": 15, "hoá đơn": 15,
    "invoice": 10, "tax invoice": 15, "invoice no": 12, "invoice number": 12,
    "invoice date": 10, "thuế gtgt": 12, "mã số thuế": 10,
    "đơn vị bán": 8, "thuế suất": 10, "tiền thuế": 8,
    "vat": 8, "subtotal": 6, "payment due": 7, "amount due": 7,
    "ký hiệu": 6, "bill to": 8,
}
PO_KEYWORDS = {
    "purchase order": 20, "đơn đặt hàng": 20, "đơn mua hàng": 20,
    "phiếu mua hàng": 15, "p.o.": 10, "po number": 15, "po no": 15, "po #": 15,
    "delivery date": 10, "ngày giao hàng": 10, "hạn giao": 10,
    "ship to": 8, "order date": 8, "nhà cung cấp": 6,
    "đơn vị cung cấp": 8, "procurement": 6,
}
STATEMENT_KEYWORDS = {
    "sao kê tài khoản": 25, "bank statement": 20, "account statement": 20,
    "statement of account": 20, "sao kê": 20,
    "số dư đầu kỳ": 15, "số dư cuối kỳ": 15,
    "opening balance": 12, "closing balance": 12,
    "transaction history": 15, "transaction date": 10,
    "giao dịch": 8, "ngân hàng": 6, "số tài khoản": 10,
    "chủ tài khoản": 8, "debit": 6, "credit": 6,
    "account number": 8,
}
DOC_TYPES = {"invoice": INVOICE_KEYWORDS, "po": PO_KEYWORDS, "statement": STATEMENT_KEYWORDS}


def classify_document(text: str) -> dict:
    text_lower = text.lower()
    scores = {}
    for doc_type, keywords in DOC_TYPES.items():
        score = 0
        matched = []
        for keyword, weight in keywords.items():
            count = text_lower.count(keyword)
            if count > 0:
                score += weight * min(count, 3)
                matched.append(keyword)
        scores[doc_type] = {"score": score, "matched": matched}

    max_score = max(s["score"] for s in scores.values())
    if max_score == 0:
        return {"type": "other", "confidence": 0, "scores": {k: v["score"] for k, v in scores.items()}, "matched_keywords": {}}

    winner = max(scores, key=lambda k: scores[k]["score"])
    sorted_scores = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    if sorted_scores[1]["score"] > 0:
        confidence = min(100, int((1 - sorted_scores[1]["score"] / sorted_scores[0]["score"]) * 100 + 50))
    else:
        confidence = min(100, max(60, sorted_scores[0]["score"]))

    return {
        "type": winner,
        "confidence": confidence,
        "scores": {k: v["score"] for k, v in scores.items()},
        "matched_keywords": {k: v["matched"] for k, v in scores.items() if v["matched"]},
    }


ROUTER_MAP = {
    "invoice": {"script": "extract_invoice.py", "output": "invoice_tracking.xlsx"},
    "po": {"script": "extract_po.py", "output": "po_tracking.xlsx"},
    "statement": {"script": "extract_statement.py", "output": None},
}


def main():
    parser = argparse.ArgumentParser(description="Classify accounting documents and route to extractors")
    parser.add_argument("file", help="Path to the document file (PDF, JPG, PNG)")
    parser.add_argument("--classify-only", action="store_true", help="Only classify, don't generate route command")
    parser.add_argument("--output-dir", default=".", help="Base directory for output files")
    args = parser.parse_args()

    file_path = os.path.abspath(args.file)
    if not os.path.exists(file_path):
        eprint(f"File not found: {file_path}")
        sys.exit(1)

    eprint(f"Classifying: {file_path}")
    ocr = extract_from_file(file_path)
    eprint(f"OCR method: {ocr.method} | Confidence: {ocr.confidence}%")

    if not ocr.text.strip():
        eprint("Warning: No text extracted. Cannot classify.")
        print(json.dumps({
            "file": file_path, "type": "other", "confidence": 0,
            "action": "manual_review",
            "ocr_method": ocr.method, "ocr_confidence": ocr.confidence,
            "message": "No text extracted from file. Check OCR dependencies.",
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    classification = classify_document(ocr.text)
    doc_type = classification["type"]
    confidence = classification["confidence"]

    eprint(f"Classification: {doc_type} (confidence: {confidence}%)")
    eprint(f"Scores: {classification['scores']}")

    if args.classify_only:
        print(json.dumps({
            "file": file_path,
            "ocr_method": ocr.method, "ocr_confidence": ocr.confidence,
            **classification,
        }, ensure_ascii=False, indent=2))
        return

    if doc_type == "other" or confidence < 50:
        print(json.dumps({
            "file": file_path, "type": doc_type, "confidence": confidence,
            "action": "manual_review",
            "ocr_method": ocr.method, "ocr_confidence": ocr.confidence,
            "message": "Document could not be classified with sufficient confidence. Human review required.",
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    route = ROUTER_MAP[doc_type]
    scripts_dir = str(Path(__file__).resolve().parent)
    script_path = os.path.join(scripts_dir, route["script"])

    cmd_parts = ["uv", "run", script_path, file_path]
    if route["output"]:
        cmd_parts.extend(["--output", os.path.join(args.output_dir, route["output"])])

    result = {
        "file": file_path,
        "type": doc_type,
        "confidence": confidence,
        "action": "extract",
        "command": " ".join(cmd_parts),
        "ocr_method": ocr.method,
        "ocr_confidence": ocr.confidence,
        "scores": classification["scores"],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if confidence < 75:
        eprint(f"Note: Classification confidence is {confidence}%. Consider reviewing the result.")


if __name__ == "__main__":
    main()
