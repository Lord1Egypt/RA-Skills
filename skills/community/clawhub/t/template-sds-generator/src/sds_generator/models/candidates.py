from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import Field

from .common import SDSBaseModel, SourceProfileName, SourceReference, ValueStatus


class FieldCandidate(SDSBaseModel):
    field_path: str
    raw_value: Any = None
    normalized_value: Any = None
    source_file: str
    source_profile: SourceProfileName
    source_authority: int
    source_revision_date: date | str | None = None
    page: int | None = None
    section: int | None = None
    excerpt: str
    extractor: str
    confidence: float = 0.0
    caveats: list[str] = Field(default_factory=list)
    label: str | None = None
    is_critical: bool = False
    source_reference: SourceReference | None = None


class CandidateEquivalenceGroup(SDSBaseModel):
    field_path: str
    semantic_key: str
    normalized_value: Any = None
    candidates: list[FieldCandidate] = Field(default_factory=list)
    completeness_score: int = 0
    specificity_score: int = 0
    authority_score: int = 0
    review_required: bool = False


class FieldDecision(SDSBaseModel):
    field_path: str
    status: ValueStatus
    chosen_value: Any = None
    chosen_group_key: str | None = None
    chosen_candidate_indices: list[int] = Field(default_factory=list)
    rationale: str | None = None
    review_required: bool = False
