# v5.3: Fully migrated to Pydantic v2 syntax.
#
# Key changes from v1:
#   @validator          → @field_validator (classmethod, with @classmethod decorator)
#   update_forward_refs() → model_rebuild()
#   class Config        → model_config = ConfigDict(...)
#   Optional[X]         → X | None  (idiomatic in v2, though Optional still works)
#
# requirements.txt entry: pydantic>=2.0.0

from __future__ import annotations

import logging
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional, Literal
from datetime import datetime, timezone

_models_logger = logging.getLogger("openclaw.models")


class ScrapedCompetitor(BaseModel):
    model_config = ConfigDict(strict=False)

    url:                  str
    title:                str | None              = None
    meta_description:     str | None              = None
    h1:                   str | None              = None
    h2s:                  List[str]               = []
    schema_types_found:   List[str]               = []   # e.g. ["FAQPage", "Article"]
    schema_raw:           str | None              = None  # raw JSON-LD string for analysis
    word_count:           int | None              = None
    readability_score:    float | None            = None
    content_summary:      str | None              = None  # block-by-block summary
    scrape_tier_used:     int                            # 1-6
    scrape_quality:       Literal["high", "medium", "low", "failed"]
    error:                str | None              = None


class TaskReferenceFile(BaseModel):
    model_config = ConfigDict(strict=False)

    run_id:                          str
    query:                           str
    search_intent:                   str           # "informational" | "commercial" | "navigational" | "transactional"
    gemini_synthesized_answer:       str
    gemini_reference_links:          List[str]
    competitors:                     List[ScrapedCompetitor]
    competitor_schema_types_combined: List[str]
    overall_scrape_quality:          Literal["high", "medium", "low"]
    overall_scrape_quality_score:    float
    # FIX (deprecation): datetime.utcnow() was removed in Python 3.12.
    # Replaced with a lambda returning a timezone-aware UTC datetime.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("competitors", mode="before")
    @classmethod
    def warn_if_no_usable_competitors(cls, v):
        """
        FIX (critical blocker): The previous validator raised a hard ValueError when all
        competitor scrapes failed, crashing the pipeline instead of allowing the
        grounded LLM answer to serve as the sole research source — which is the
        explicitly intended fallback documented in daily_worker.py Step 8.5.

        This validator now emits a warning log and returns the list unchanged so the
        pipeline can continue gracefully on grounded-data-only runs.
        """
        usable = [
            c for c in v
            if (c.get("scrape_quality") if isinstance(c, dict) else c.scrape_quality) != "failed"
        ]
        if len(usable) == 0:
            _models_logger.warning(
                "TaskReferenceFile: all competitor scrapes failed or competitors list is "
                "empty. Pipeline will rely solely on grounded LLM data for this run."
            )
        return v


class OutlineSection(BaseModel):
    h2:                str
    purpose:           str
    subsections:       List[str]                             = []
    content_type:      Literal["prose", "list", "table", "how_to_steps", "faq_block", "comparison"]
    target_word_count: int


class AnswerBlock(BaseModel):
    """
    The 40-60 word direct answer placed immediately after the H1.
    Primary featured snippet / AI answer engine target.
    """
    answer_text:               str   # 40-60 words, no hedging, no "in this article"
    answer_type:               Literal["definition", "process", "list", "table", "yes_no"]
    contains_primary_keyword:  bool = True


class ContentOutline(BaseModel):
    model_config = ConfigDict(strict=False)

    target_query:           str
    primary_keyword:        str
    secondary_keywords:     List[str]
    search_intent:          str
    page_title:             str          # <60 chars, primary keyword near front
    meta_description:       str          # 150-160 chars, includes CTA hook
    h1:                     str
    sections:               List[OutlineSection]
    answer_block:           AnswerBlock
    schema_types_to_generate: List[str]
    content_gaps_addressed: List[str]
    estimated_word_count:   int


class SchemaBlock(BaseModel):
    schema_type:  str
    json_ld:      str
    entity_count: int


class GeneratedContent(BaseModel):
    model_config = ConfigDict(strict=False)

    outline:             ContentOutline
    html_body:           str
    title_tag:           str
    meta_description:    str
    schema_blocks:       List[SchemaBlock]
    cta_injection_count: int
    word_count:          int
    readability_score:   float
    fact_check_passed:   bool
    fact_check_notes:    str | None = None


# model_rebuild() replaces update_forward_refs() from Pydantic v1.
# OutlineSection and AnswerBlock are defined before ContentOutline so no
# forward references exist, but model_rebuild() is kept as an explicit safety
# net in case class ordering ever changes during refactoring.
ContentOutline.model_rebuild()
GeneratedContent.model_rebuild()
