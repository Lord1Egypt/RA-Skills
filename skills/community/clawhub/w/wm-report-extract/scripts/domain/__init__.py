"""Declarative domain config + thin arbitration policy for wm-report-extract."""
from __future__ import annotations

from domain.catalogs import (
    INDUSTRY_EXT_GROUPS,
    NARRATIVE_REQUIRED_IDS,
    PRIORITY_GROUPS_BASE,
    TABLE_CATALOG,
    TABLE_SPEC_BY_ID,
)
from domain.industry import (
    INDUSTRY_HINTS,
    TITLE_INDUSTRY_HINTS,
    TITLE_TRANSPORT_SEGMENT_HINTS,
    TRANSPORT_NEGATIVE_HINTS,
    TRANSPORT_SEGMENT_HINTS,
)
from domain.policy import apply_industry_arbitration
from domain.signatures import (
    CHAPTER_RE,
    CN_NUM,
    HIGH_CONFIDENCE_SIGNATURES,
    STRUCTURAL_RULES,
    STMT_TITLE_TOKS,
    SUBSECTION_ANCHORS,
    SUBSIDIARY_HEADER_TOKS,
    TABLE_SIGNATURES,
    TYPE_HINT_SIGNATURES,
)

__all__ = [
    "CHAPTER_RE",
    "CN_NUM",
    "SUBSECTION_ANCHORS",
    "HIGH_CONFIDENCE_SIGNATURES",
    "TYPE_HINT_SIGNATURES",
    "TABLE_SIGNATURES",
    "SUBSIDIARY_HEADER_TOKS",
    "STMT_TITLE_TOKS",
    "STRUCTURAL_RULES",
    "INDUSTRY_HINTS",
    "TITLE_INDUSTRY_HINTS",
    "TRANSPORT_SEGMENT_HINTS",
    "TRANSPORT_NEGATIVE_HINTS",
    "TITLE_TRANSPORT_SEGMENT_HINTS",
    "PRIORITY_GROUPS_BASE",
    "INDUSTRY_EXT_GROUPS",
    "NARRATIVE_REQUIRED_IDS",
    "TABLE_CATALOG",
    "TABLE_SPEC_BY_ID",
    "apply_industry_arbitration",
]
