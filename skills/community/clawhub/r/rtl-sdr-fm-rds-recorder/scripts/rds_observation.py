#!/usr/bin/env python3
"""RDS observation collection and normalization helpers.

Only `ps` and `partial_ps` are used as naming inputs.
`pi` is retained only as auxiliary/debug evidence.
Other redsea fields are intentionally ignored for station naming.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class CandidateMetadata:
    score: int
    shape_class: str


@dataclass
class RdsEvidence:
    """Aggregated RDS evidence collected during one decode attempt."""

    ps_counts: dict[str, int] = field(default_factory=dict)
    partial_ps_counts: dict[str, int] = field(default_factory=dict)
    pi_counts: dict[str, int] = field(default_factory=dict)
    raw_ps_counts: dict[str, int] = field(default_factory=dict)
    raw_partial_ps_counts: dict[str, int] = field(default_factory=dict)
    candidate_metadata: dict[str, CandidateMetadata] = field(default_factory=dict)
    total_objects: int = 0
    valid_objects: int = 0
    sniff_duration_sec: float = 0.0
    rtl_fm_stderr_first_line: str | None = None


def create_rds_evidence() -> RdsEvidence:
    return RdsEvidence()


def update_count(counts: dict[str, int], key: str) -> None:
    counts[key] = counts.get(key, 0) + 1


def sanitize_station_name(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9 +&._-]+", "", value.strip())
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip(" +&-_.")
    return cleaned or "UnknownStation"


def add_redsea_object(evidence: RdsEvidence, obj: dict) -> None:
    """Accumulate one redsea JSON object.

    Naming inputs are intentionally limited to `ps` and `partial_ps`.
    `pi` is kept only as auxiliary/debug evidence.
    Other redsea fields are ignored on purpose.
    """
    evidence.total_objects += 1

    ps = obj.get("ps")
    if ps:
        update_count(evidence.raw_ps_counts, str(ps))
        candidate = sanitize_station_name(str(ps))
        if len(candidate) >= 3 and candidate != "UnknownStation":
            update_count(evidence.ps_counts, candidate)
        evidence.valid_objects += 1
        return

    partial_ps = obj.get("partial_ps")
    if partial_ps:
        update_count(evidence.raw_partial_ps_counts, str(partial_ps))
        candidate = sanitize_station_name(str(partial_ps))
        if len(candidate) >= 3 and candidate != "UnknownStation":
            update_count(evidence.partial_ps_counts, candidate)
        evidence.valid_objects += 1
        return

    pi = obj.get("pi")
    if pi:
        update_count(evidence.pi_counts, str(pi))
        evidence.valid_objects += 1
