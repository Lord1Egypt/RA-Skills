from __future__ import annotations

LEGACY_DELIVERABLE_KINDS = {
    "markdown_report",
    "pdf_report",
    "docx_report",
    "html_report",
    "xlsx",
    "csv",
    "package",
    "unknown",
}

LEGACY_EXPECTED_FORMATS_BY_KIND = {
    "markdown_report": {"markdown"},
    "pdf_report": {"pdf"},
    "docx_report": {"docx"},
    "html_report": {"html", "htm"},
    "xlsx": {"xlsx"},
    "csv": {"csv"},
    "package": {"package"},
}


def expected_formats_for_kind(primary_kind: str) -> set[str]:
    return LEGACY_EXPECTED_FORMATS_BY_KIND.get(
        str(primary_kind or "").strip().lower(),
        set(),
    )


def kind_for_artifact_format(artifact_format: str) -> str | None:
    if artifact_format == "package":
        return "package"
    if artifact_format in {"markdown", "md"}:
        return "markdown_report"
    if artifact_format in {"pdf", "docx"}:
        return f"{artifact_format}_report"
    if artifact_format in {"html", "htm"}:
        return "html_report"
    if artifact_format in {"xlsx", "csv"}:
        return artifact_format
    return None
