from __future__ import annotations

from datetime import UTC, date, datetime
from typing import Any

from pydantic import Field, computed_field

from .common import BoundingBox, FileType, SDSBaseModel, SourceProfileName


class SourceProfile(SDSBaseModel):
    name: SourceProfileName
    authority: int
    description: str | None = None


class SourceDescriptor(SDSBaseModel):
    file_path: str
    file_name: str
    file_type: FileType
    source_profile: SourceProfileName
    source_authority: int
    revision_date: date | str | None = None
    date_of_first_issue: date | str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class PageWord(SDSBaseModel):
    text: str
    page_number: int
    bbox: BoundingBox
    block_no: int | None = None
    line_no: int | None = None
    word_no: int | None = None


class PageBlock(SDSBaseModel):
    block_id: str
    page_number: int
    text: str
    bbox: BoundingBox
    block_type: str = "text"
    order_index: int | None = None
    column_index: int | None = None
    is_header_footer_noise: bool = False
    is_section_heading: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


SourceBlock = PageBlock


class ParsedPage(SDSBaseModel):
    page_number: int
    width: float | None = None
    height: float | None = None
    rotation: int | None = None
    raw_text: str = ""
    normalized_text: str = ""
    blocks: list[PageBlock] = Field(default_factory=list)
    words: list[PageWord] = Field(default_factory=list)
    column_count: int = 1
    likely_scanned: bool = False
    ocr_used: bool = False
    ocr_backend: str | None = None
    ocr_confidence: float | None = None
    ocr_cache_hit: bool = False
    removed_noise_block_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @computed_field
    @property
    def text_length(self) -> int:
        return len(self.normalized_text or self.raw_text or "")


class SectionBlock(SDSBaseModel):
    section_number: int
    canonical_name: str
    heading_text: str
    start_page: int | None = None
    end_page: int | None = None
    pages: list[int] = Field(default_factory=list)
    block_ids: list[str] = Field(default_factory=list)
    text: str = ""
    detection_pattern: str | None = None
    detection_confidence: float | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class ParsedSourceDocument(SDSBaseModel):
    file_path: str
    file_name: str
    file_type: FileType
    source_profile: SourceProfileName
    source_authority: int
    parser_name: str
    revision_date: date | str | None = None
    date_of_first_issue: date | str | None = None
    pages: list[ParsedPage] = Field(default_factory=list)
    blocks: list[PageBlock] = Field(default_factory=list)
    sections: dict[int, SectionBlock] = Field(default_factory=dict)
    raw_text: str = ""
    normalized_text: str = ""
    parser_warnings: list[str] = Field(default_factory=list)
    likely_scanned: bool = False
    ocr_backend: str | None = None
    ocr_pages_used: list[int] = Field(default_factory=list)
    ocr_cache_hits: list[int] = Field(default_factory=list)
    ocr_low_confidence_pages: list[int] = Field(default_factory=list)
    source_metadata: dict[str, Any] = Field(default_factory=dict)
    parsed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @computed_field
    @property
    def section_numbers_present(self) -> list[int]:
        return sorted(self.sections.keys())
