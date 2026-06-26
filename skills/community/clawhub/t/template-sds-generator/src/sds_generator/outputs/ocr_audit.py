from __future__ import annotations

import json
from pathlib import Path

from sds_generator.models.source import ParsedSourceDocument


def build_ocr_audit_report(documents: list[ParsedSourceDocument]) -> dict[str, object]:
    document_entries: list[dict[str, object]] = []
    for document in documents:
        page_entries = [
            {
                "page_number": page.page_number,
                "likely_scanned": page.likely_scanned,
                "ocr_used": page.ocr_used,
                "ocr_backend": page.ocr_backend,
                "ocr_confidence": page.ocr_confidence,
                "ocr_cache_hit": page.ocr_cache_hit,
            }
            for page in document.pages
        ]
        document_entries.append(
            {
                "file_name": document.file_name,
                "likely_scanned": document.likely_scanned,
                "ocr_backend": document.ocr_backend,
                "ocr_pages_used": list(document.ocr_pages_used),
                "ocr_cache_hits": list(document.ocr_cache_hits),
                "ocr_low_confidence_pages": list(document.ocr_low_confidence_pages),
                "parser_warnings": list(document.parser_warnings),
                "pages": page_entries,
            }
        )

    return {
        "contract_version": 1,
        "documents": document_entries,
    }


def write_ocr_audit_report(documents: list[ParsedSourceDocument], output_path: Path) -> dict[str, object]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_ocr_audit_report(documents)
    with output_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return payload
