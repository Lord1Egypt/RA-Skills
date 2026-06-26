from __future__ import annotations

from pathlib import Path
from typing import Any, Generic, TypeVar

from pydantic import Field, model_validator

from .common import (
    NO_DATA_DISPLAY,
    OriginKind,
    SDSBaseModel,
    SourceProfileName,
    SourceReference,
    ValueStatus,
)

T = TypeVar("T")


class StructuredFieldOrigin(SDSBaseModel):
    kind: OriginKind | None = None
    source_files: list[str] = Field(default_factory=list)
    derived_from: list[str] = Field(default_factory=list)
    selection_reason: str | None = None


class StructuredField(SDSBaseModel, Generic[T]):
    value: T | None = None
    display_value: Any = NO_DATA_DISPLAY
    status: ValueStatus = ValueStatus.MISSING
    sources: list[SourceReference] = Field(default_factory=list)
    review_flags: list[str] = Field(default_factory=list)
    origin: "StructuredFieldOrigin" = Field(default_factory=lambda: StructuredFieldOrigin())

    @model_validator(mode="after")
    def ensure_display_value(self) -> "StructuredField[T]":
        if self.value is None or self.value == "" or self.value == [] or self.value == {}:
            self.display_value = NO_DATA_DISPLAY
            if self.status == ValueStatus.SELECTED:
                self.status = ValueStatus.MISSING
        elif self.display_value == NO_DATA_DISPLAY:
            self.display_value = self.value
        return self


class FieldSourceMapRow(SDSBaseModel):
    field_path: str
    selected: bool = False
    selection_reason: str | None = None
    selection_detail: str | None = None
    display_value: str
    status: ValueStatus
    source_file: str
    source_profile: SourceProfileName
    source_authority: int
    source_revision_date: str | None = None
    page: int | None = None
    section: int | None = None
    raw_excerpt: str | None = None
    normalized_value: Any = None
    completeness_score: int = 0
    specificity_score: int = 0
    authority_score: int = 0
    confidence: float = 0.0
    caveats: list[str] = Field(default_factory=list)
    review_flag: bool = False


class StructuredAuditOutput(SDSBaseModel):
    review_notes: list[dict[str, Any]] = Field(default_factory=list)
    field_source_map_summary: list[dict[str, Any]] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)


class StructuredDataOutput(SDSBaseModel):
    contract_version: str = "1.0"
    document_meta: dict[str, Any]
    sections: dict[str, dict[str, StructuredField[Any]]]
    audit: StructuredAuditOutput


class OutputArtifacts(SDSBaseModel):
    run_root: Path
    normalized_dir: Path
    extracted_dir: Path
    reconciled_dir: Path
    final_dir: Path
    audit_dir: Path
    logs_dir: Path
    run_manifest_path: Path | None = None
    docx_path: Path
    pdf_path: Path | None = None
    template_fill_report_path: Path | None = None
    structured_json_path: Path
    content_policy_report_path: Path | None = None
    ocr_audit_path: Path | None = None
    field_source_map_csv_path: Path
    field_source_map_md_path: Path | None = None
    review_checklist_path: Path
    log_path: Path


class ReleasePackage(SDSBaseModel):
    release_dir: Path | None = None
    eligible: bool = False
    blocking_reasons: list[str] = Field(default_factory=list)
