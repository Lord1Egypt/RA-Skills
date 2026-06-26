from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Sequence

from .common import canonical_json
from .constants import (
    ATTACK_SURFACE_RULE_IDS,
    CONFIDENCE_MULT,
    CONFIDENCE_RANK,
    HYGIENE_RULE_IDS,
    LAYER_CAPABILITY,
    LAYER_MULT,
    LAYER_PROMPT,
    LAYER_SECRET,
    LAYER_STATIC,
    LAYER_SUPPLY,
    REQUIRED_LAYERS,
    SEVERITY_BASE,
    SEVERITY_RANK,
)
from .models import FileRecord, Finding


def score_finding(finding: Finding) -> float:
    severity = str(finding.get("severity", "low"))
    confidence = str(finding.get("confidence", "low"))
    layer = str(finding.get("layer", LAYER_STATIC))
    exploitability = float(finding.get("exploitability", 0.8))
    reach = float(finding.get("reach", 0.8))

    base = SEVERITY_BASE.get(severity, 0.0)
    conf_mult = CONFIDENCE_MULT.get(confidence, 0.7)
    layer_mult = LAYER_MULT.get(layer, 1.0)
    value = base * conf_mult * layer_mult * exploitability * reach
    return round(value, 2)


def finding_sort_key(finding: Finding) -> tuple[int, int, float, str, int, str]:
    severity_rank = SEVERITY_RANK.get(str(finding.get("severity", "low")), 0)
    confidence_rank = CONFIDENCE_RANK.get(str(finding.get("confidence", "low")), 0)
    score = float(finding.get("risk_contribution", 0.0))
    file_value = str(finding.get("file", ""))
    line_value = int(finding.get("line", 0))
    rule_id = str(finding.get("rule_id", ""))
    return (-severity_rank, -confidence_rank, -score, file_value, line_value, rule_id)


def build_evidence_id(commit_sha: str, finding: Finding) -> str:
    payload = {
        "commit_sha": commit_sha,
        "layer": finding.get("layer"),
        "rule_id": finding.get("rule_id"),
        "file": finding.get("file"),
        "line": finding.get("line"),
        "snippet": finding.get("snippet"),
    }
    digest = hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest().upper()
    return f"E-{digest[:10]}"


def derive_decision(
    risk_score: int,
    actionable_findings: Sequence[Finding],
    hygiene_findings: Sequence[Finding],
    coverage_ratio: float,
    partial_coverage: bool,
) -> str:
    has_critical_actionable = any(str(item.get("severity")) == "critical" for item in actionable_findings)
    has_high_actionable = any(str(item.get("severity")) == "high" for item in actionable_findings)
    has_high_attack_surface = any(
        str(item.get("rule_id")) in ATTACK_SURFACE_RULE_IDS and str(item.get("severity")) in {"high", "critical"}
        for item in actionable_findings
    )
    hygiene_score = sum(float(item.get("risk_contribution", 0.0)) for item in hygiene_findings)

    if has_high_attack_surface:
        return "reject"
    if coverage_ratio < 0.75:
        return "caution"
    if has_critical_actionable:
        return "reject"
    if risk_score >= 70 and actionable_findings:
        return "reject"
    if has_high_actionable or risk_score >= 35:
        return "caution"
    if hygiene_score >= 18:
        return "caution"
    if partial_coverage:
        return "caution"
    return "approve"


def overall_confidence(findings: Sequence[Finding], coverage_ratio: float) -> str:
    if coverage_ratio < 0.80:
        return "low"
    if any(item.get("severity") == "critical" and item.get("confidence") == "high" for item in findings):
        return "high"
    if findings:
        return "medium"
    return "high"


def determine_applicable_layers(records: Sequence[FileRecord]) -> set[str]:
    applicable: set[str] = set()
    runtime_suffixes = {".py", ".js", ".ts", ".tsx", ".mjs", ".cjs", ".sh", ".bash", ".zsh", ".ps1"}

    for record in records:
        path_obj: Path = record["path_obj"]
        rel_norm = str(path_obj).replace("\\", "/")

        if record.get("is_prompt_surface"):
            applicable.add(LAYER_PROMPT)
        if path_obj.name == "SKILL.md":
            applicable.add(LAYER_CAPABILITY)
        if path_obj.suffix.lower() in runtime_suffixes:
            applicable.add(LAYER_STATIC)
            applicable.add(LAYER_SECRET)
        if rel_norm.startswith(".github/workflows/") or path_obj.name in {
            "package.json",
            "requirements.txt",
            "pyproject.toml",
            "package-lock.json",
            "pnpm-lock.yaml",
            "yarn.lock",
            "bun.lockb",
        }:
            applicable.add(LAYER_SUPPLY)

    if not applicable:
        return set(REQUIRED_LAYERS)
    return applicable


def classify_finding_kind(finding: Finding) -> str:
    rule_id = str(finding.get("rule_id", ""))
    context = finding.get("context", {})
    surface = str(context.get("surface", "runtime"))

    if rule_id in ATTACK_SURFACE_RULE_IDS:
        return "security_actionable"
    if rule_id in HYGIENE_RULE_IDS:
        return "hygiene"
    if surface in {"docs", "example", "test-fixture"}:
        return "hygiene"
    return "security_actionable"


def severity_floor_decision(findings: Sequence[Finding], partial_coverage: bool) -> str:
    if partial_coverage:
        return "caution"
    if any(item.get("severity") == "critical" for item in findings):
        return "reject"
    if any(item.get("severity") == "high" for item in findings):
        return "caution"
    return "approve"


def minimum_score_floor(findings: Sequence[Finding]) -> int:
    total = 0.0
    has_critical = False
    has_high = False

    for item in findings:
        value = item.get("risk_contribution")
        if isinstance(value, (int, float)):
            total += float(value)
        else:
            total += SEVERITY_BASE.get(str(item.get("severity", "low")), 0.0)
        if item.get("severity") == "critical":
            has_critical = True
        if item.get("severity") == "high":
            has_high = True

    floor = int(min(100, round(total * 0.70)))
    if has_critical:
        floor = max(70, floor)
    elif has_high:
        floor = max(35, floor)
    return floor
