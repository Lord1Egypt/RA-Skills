from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sds_generator.models import FinalSDSDocument, OutputArtifacts
from sds_generator.models.source import ParsedSourceDocument


def _path_string(path: Path | None) -> str | None:
    return str(path) if path is not None else None


def build_run_manifest(
    *,
    documents: list[ParsedSourceDocument],
    final_document: FinalSDSDocument,
    artifacts: OutputArtifacts,
    settings: dict[str, Any],
) -> dict[str, Any]:
    return {
        "contract_version": 1,
        "run_root": str(artifacts.run_root),
        "settings": settings,
        "inputs": {
            "template_file": final_document.document_meta.template_file,
            "prompt_file": final_document.document_meta.prompt_file,
            "source_files": [
                {
                    "file_name": document.file_name,
                    "file_path": document.file_path,
                    "file_type": document.file_type.value,
                    "source_profile": document.source_profile.value,
                    "source_authority": document.source_authority,
                    "revision_date": document.revision_date,
                    "likely_scanned": document.likely_scanned,
                    "ocr_pages_used": list(document.ocr_pages_used),
                }
                for document in documents
            ],
        },
        "document_meta": {
            "run_metadata_version": final_document.document_meta.run_metadata_version,
            "generation_mode": final_document.document_meta.generation_mode.value,
            "ready_for_release": final_document.document_meta.release_eligible,
            "critical_conflicts_present": final_document.document_meta.critical_conflicts_present,
        },
        "outputs": {
            "docx_path": _path_string(artifacts.docx_path),
            "pdf_path": _path_string(artifacts.pdf_path),
            "structured_json_path": _path_string(artifacts.structured_json_path),
            "content_policy_report_path": _path_string(artifacts.content_policy_report_path),
            "ocr_audit_path": _path_string(artifacts.ocr_audit_path),
            "field_source_map_csv_path": _path_string(artifacts.field_source_map_csv_path),
            "field_source_map_md_path": _path_string(artifacts.field_source_map_md_path),
            "review_checklist_path": _path_string(artifacts.review_checklist_path),
            "template_fill_report_path": _path_string(artifacts.template_fill_report_path),
        },
    }


def write_run_manifest(
    *,
    documents: list[ParsedSourceDocument],
    final_document: FinalSDSDocument,
    artifacts: OutputArtifacts,
    settings: dict[str, Any],
) -> dict[str, Any]:
    if artifacts.run_manifest_path is None:
        raise ValueError("OutputArtifacts.run_manifest_path must be configured.")
    artifacts.run_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_run_manifest(
        documents=documents,
        final_document=final_document,
        artifacts=artifacts,
        settings=settings,
    )
    with artifacts.run_manifest_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")
    return payload
