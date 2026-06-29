from __future__ import annotations

from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent.parent

DANGEROUS_IDENTIFIERS = [
    "FORMAT_ALIASES",
    "_explicit_user_format_kind",
    "context_blob",
    "geo_markers",
    "local_discovery_terms",
    "draft_signals",
    "addressing_markers",
    "official_signals",
    "user_gen_signals",
    "SOURCE_TAGS",
    "official_source",
    "official_domain",
    "authoritative_tag",
    "user_generated_platform",
    "short_formats",
    "long_formats",
]

FORBIDDEN_OUTPUT_CONTRACT_IDENTIFIERS = [
    "CANONICAL_DELIVERABLE_KINDS",
    "EXPECTED_FORMATS_BY_PRIMARY_KIND",
    "_format_to_deliverable_kind",
    "mimetypes.guess_type",
    "extension_to_media_type",
    "media_type_to_extension",
    "mime_type_to_kind",
    "format_to_deliverable_kind",
]


def _production_python_files() -> list[Path]:
    return sorted(path for path in SCRIPTS_DIR.glob("research_mode*.py") if path.is_file())


def _new_output_contract_python_files() -> list[Path]:
    return sorted(
        path
        for path in _production_python_files()
        if path.name != "research_mode_legacy_deliverables.py"
    )


def test_language_driven_validation_identifiers_do_not_return() -> None:
    haystack = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in _production_python_files()
    )
    offenders = [name for name in DANGEROUS_IDENTIFIERS if name in haystack]
    assert offenders == []


def test_output_contract_does_not_use_format_dictionaries() -> None:
    haystack = "\n".join(
        path.read_text(encoding="utf-8", errors="replace")
        for path in _new_output_contract_python_files()
    )
    offenders = [
        name for name in FORBIDDEN_OUTPUT_CONTRACT_IDENTIFIERS if name in haystack
    ]
    assert offenders == []


def test_guardrail_free_text_format_decision_stays_unknown() -> None:
    from research_mode_finalization import build_deliverable_format_decision

    state = {
        "goal": "请准备 PDF 报告",
        "working_memory": {"deliverable": "请准备 PDF 报告"},
    }
    result = build_deliverable_format_decision(
        state=state,
        finalization=None,
        report_markdown="",
        artifact_check=None,
    )

    assert result["source"] == "unknown"
    assert result["selected_kind"] == "unknown"


def test_guardrail_provider_error_text_stays_generic() -> None:
    from research_mode_surface_delivery import (
        DELIVERY_NOTIFICATION_ERROR,
        classify_delivery_error,
    )

    assert classify_delivery_error("thread target exploded") == DELIVERY_NOTIFICATION_ERROR
