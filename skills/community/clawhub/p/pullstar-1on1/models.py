"""
models.py — Python data model definitions for PullStar 1-on-1
Phase 1 scope: IngestedProfile, ScoredProfile (velocity + pr_quality), SkillOutput

These TypedDicts mirror the TypeScript interfaces in ui/src/types/pullstar.ts.
Scripts import from here to get typed dicts they can serialize to JSON directly.
"""

from __future__ import annotations
from typing import Literal, TypedDict


# ---------------------------------------------------------------------------
# Ingestion primitives
# ---------------------------------------------------------------------------

class PullRequest(TypedDict):
    number: int
    title: str
    url: str
    repository: str
    status: Literal["open", "merged", "closed"]
    created_at: str         # ISO 8601
    merged_at: str | None   # ISO 8601
    lines_added: int
    lines_deleted: int
    files_changed: int
    commit_count: int
    description_length: int  # char count only — no raw content
    label_names: list[str]
    base_branch: str
    reviews_received_count: int


class ReviewGiven(TypedDict):
    repository: str
    pr_number: int
    pr_title: str
    state: Literal["approved", "changes_requested", "commented"]
    submitted_at: str  # ISO 8601
    body_length: int   # char count only — no raw content


class ReviewReceived(TypedDict):
    reviewer_login: str
    pr_number: int
    state: Literal["approved", "changes_requested", "commented"]
    submitted_at: str  # ISO 8601
    body_length: int   # char count only — no raw content


# ---------------------------------------------------------------------------
# IngestedProfile — written by ingest.py
# ---------------------------------------------------------------------------

class SummaryStats(TypedDict):
    total_prs_authored: int
    prs_merged: int
    prs_open: int
    prs_closed_unmerged: int
    total_reviews_given: int
    total_reviews_received: int
    total_lines_added: int
    total_lines_deleted: int
    avg_pr_size_lines: float
    active_weeks: int
    total_weeks: int


class IngestedProfile(TypedDict):
    engineer_login: str
    engineer_name: str | None
    org: str
    lookback_days: int
    ingested_at: str           # ISO 8601
    prs_authored: list[PullRequest]
    reviews_given: list[ReviewGiven]
    reviews_received: list[ReviewReceived]
    summary_stats: SummaryStats


# ---------------------------------------------------------------------------
# ScoredProfile — written by score.py
# Phase 1: velocity + pr_quality only
# ---------------------------------------------------------------------------

class DimensionScore(TypedDict):
    score: int
    max: int                              # always 20
    confidence: Literal["high", "medium", "low"]
    signals: list[str]                    # 1–3 human-readable observations
    flags: list[str]                      # 0–2 anomaly strings


class Phase1Dimensions(TypedDict):
    velocity:   DimensionScore
    pr_quality: DimensionScore
    # Phase 2 will add: review_participation, collaboration, consistency


class Flag(TypedDict):
    severity: Literal["info", "caution", "notable"]
    dimension: str
    message: str


class ScoredProfile(TypedDict):
    engineer_login: str
    scored_at: str        # ISO 8601
    lookback_days: int
    dimensions: Phase1Dimensions
    total_score: int      # sum of scored dimensions (0–40 in Phase 1)
    confidence: Literal["high", "medium", "low"]
    data_volume_note: str | None   # set when total_prs_authored < 5
    flags: list[Flag]


# ---------------------------------------------------------------------------
# SkillOutput — written by generate_brief.py, read by the UI
# ---------------------------------------------------------------------------

class SkillOutput(TypedDict):
    version: Literal["1.0"]
    generated_at: str       # ISO 8601
    engineer_login: str
    engineer_name: str | None
    org: str
    lookback_days: int
    scored_profile: ScoredProfile
    brief: str              # full markdown brief from AI
