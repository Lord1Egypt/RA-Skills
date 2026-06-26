from __future__ import annotations

from datetime import UTC, date, datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


NO_DATA_DISPLAY = "No data available"


class SDSBaseModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        validate_assignment=True,
        str_strip_whitespace=True,
    )


class GenerationMode(str, Enum):
    DRAFT = "draft"
    RELEASE = "release"


class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"


class SourceProfileName(str, Enum):
    MANUFACTURER_GRADE = "manufacturer_grade"
    DISTRIBUTOR_GRADE = "distributor_grade"
    AGGREGATOR_GRADE = "aggregator_grade"
    UNCLASSIFIED = "unclassified"


class ReviewSeverity(str, Enum):
    CRITICAL = "critical"
    MODERATE = "moderate"
    MINOR = "minor"
    INFO = "info"


class ReviewStatus(str, Enum):
    UNRESOLVED = "unresolved"
    CONFLICT_RESOLVED_CONSERVATIVE = "conflict_resolved_conservative"
    FORCED_NO_DATA = "forced_no_data"
    OVERRIDDEN_FIXED_COMPANY = "overridden_fixed_company"
    WARNING = "warning"
    PASS = "pass"


class ChecklistBucket(str, Enum):
    CRITICAL_CONFLICTS = "critical_conflicts"
    FORCED_NO_DATA = "forced_no_data"
    SOURCE_CAVEATS = "source_caveats"
    OCR_LOW_CONFIDENCE = "ocr_low_confidence"
    SYSTEM_OVERRIDES = "system_overrides"
    LAYOUT_BRANDING_QA = "layout_branding_qa"
    RELEASE_GATE = "release_gate"


class ValueStatus(str, Enum):
    MISSING = "missing"
    SELECTED = "selected"
    CONFLICT = "conflict"
    OVERRIDDEN = "overridden"
    CANDIDATE_ONLY = "candidate_only"
    REVIEW_REQUIRED = "review_required"
    NOT_APPLICABLE = "not_applicable"
    SYSTEM_DEFAULT = "system_default"
    USER_OVERRIDE = "user_override"
    DERIVED = "derived"


class OriginKind(str, Enum):
    SOURCE_DOCUMENT = "source_document"
    COMPANY_CONFIG = "company_config"
    TEMPLATE_DEFAULT = "template_default"
    USER_OVERRIDE = "user_override"
    DERIVED = "derived"
    MANUAL_DEFAULT = "manual_default"


class TransportMode(str, Enum):
    DOT = "dot"
    ADR_RID = "adr_rid"
    IMDG = "imdg"
    IATA = "iata"


class BoundingBox(SDSBaseModel):
    x0: float
    y0: float
    x1: float
    y1: float


class SourceLocator(SDSBaseModel):
    page: int | None = None
    block_id: str | None = None
    paragraph_index: int | None = None
    table_index: int | None = None
    row_index: int | None = None
    cell_index: int | None = None
    line_number: int | None = None


class SourceReference(SDSBaseModel):
    file_name: str
    file_path: str | None = None
    source_profile: SourceProfileName | None = None
    source_authority: int | None = None
    source_revision_date: date | str | None = None
    page: int | None = None
    section: int | None = None
    excerpt: str | None = None
    locator: SourceLocator | None = None


class SourceValueEvidence(SDSBaseModel):
    file: str
    page: int | None = None
    section: int | None = None
    value: Any = None
    excerpt: str | None = None


class SourceSummary(SDSBaseModel):
    file_name: str
    source_profile: SourceProfileName
    source_authority: int
    revision_date: date | str | None = None
    product_name: str | None = None
    cas_number: str | None = None
    notes: list[str] = Field(default_factory=list)


class ReviewNote(SDSBaseModel):
    field_path: str
    severity: ReviewSeverity
    status: ReviewStatus
    chosen_value: Any = None
    why: str
    source_values: list[SourceValueEvidence] = Field(default_factory=list)
    release_blocking: bool = False
    checklist_bucket: ChecklistBucket | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class RunWarning(SDSBaseModel):
    code: str
    message: str
    severity: ReviewSeverity = ReviewSeverity.INFO
    source_reference: SourceReference | None = None
