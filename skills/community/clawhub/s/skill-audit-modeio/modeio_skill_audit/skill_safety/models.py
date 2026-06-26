from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, TypedDict


class FileRecord(TypedDict):
    path_obj: Path
    rel_path: str
    text: str
    lines: List[str]
    is_prompt_surface: bool
    is_executable_surface: bool


class ScanStats(TypedDict):
    total_files_seen: int
    candidate_files: int
    files_scanned: int
    skipped_large_files: int
    skipped_unreadable_files: int
    skipped_large_executable_files: int
    skipped_unreadable_executable_files: int


class LayerStateEntry(TypedDict):
    executed: bool
    finding_count: int


LayerState = Dict[str, LayerStateEntry]


class Finding(TypedDict, total=False):
    layer: str
    rule_id: str
    category: str
    severity: str
    confidence: str
    exploitability: float
    reach: float
    file: str
    line: int
    snippet: str
    why: str
    fix: str
    tags: List[str]
    context: Dict[str, Any]
    finding_kind: str
    risk_contribution_raw: float
    risk_contribution: float
    evidence_id: str
