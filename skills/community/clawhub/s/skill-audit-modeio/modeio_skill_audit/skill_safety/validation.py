from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .common import normalize_decision, snippets_match
from .constants import CATEGORY_VALUES, CONFIDENCE_VALUES, DECISION_VALUES, SEVERITY_VALUES
from .context import parse_context_profile
from .engine import scan_repository
from .json_utils import extract_first_json_object
from .scoring import minimum_score_floor, severity_floor_decision


def _extract_json_summary(assessment_text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    heading = re.search(r"#\s*JSON_SUMMARY", assessment_text, flags=re.IGNORECASE)
    if not heading:
        return None, "Missing # JSON_SUMMARY section."

    tail = assessment_text[heading.end() :]
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", tail, flags=re.IGNORECASE | re.DOTALL)
    payload = fenced.group(1) if fenced else extract_first_json_object(tail)
    if not payload:
        return None, "Could not locate JSON object under # JSON_SUMMARY."

    try:
        parsed = json.loads(payload)
    except ValueError as exc:
        return None, f"Invalid JSON_SUMMARY payload: {exc}"
    if not isinstance(parsed, dict):
        return None, "JSON_SUMMARY payload must be a JSON object."
    return parsed, None


def validate_assessment_output(
    assessment_text: str,
    scan_result: Dict[str, Any],
) -> Dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []

    summary, parse_error = _extract_json_summary(assessment_text)
    if parse_error:
        return {
            "valid": False,
            "errors": [parse_error],
            "warnings": warnings,
            "stats": {},
        }

    required_summary_keys = {
        "decision",
        "risk_score",
        "confidence",
        "findings",
        "exploit_chain",
        "safe_subset",
        "coverage_notes",
    }
    missing_summary_keys = sorted(required_summary_keys - set(summary.keys()))
    if missing_summary_keys:
        errors.append("JSON_SUMMARY missing required keys: " + ", ".join(missing_summary_keys))

    decision = normalize_decision(summary.get("decision"))
    if decision not in DECISION_VALUES:
        errors.append("JSON_SUMMARY.decision must be one of reject/caution/approve.")

    risk_score = summary.get("risk_score")
    if not isinstance(risk_score, int) or not (0 <= risk_score <= 100):
        errors.append("JSON_SUMMARY.risk_score must be an integer between 0 and 100.")

    confidence = summary.get("confidence")
    if confidence not in CONFIDENCE_VALUES:
        errors.append("JSON_SUMMARY.confidence must be one of low/medium/high.")

    exploit_chain = summary.get("exploit_chain")
    if not isinstance(exploit_chain, list) or not all(isinstance(item, str) for item in exploit_chain):
        errors.append("JSON_SUMMARY.exploit_chain must be an array of strings.")

    safe_subset = summary.get("safe_subset")
    if not isinstance(safe_subset, list) or not all(isinstance(item, str) for item in safe_subset):
        errors.append("JSON_SUMMARY.safe_subset must be an array of strings.")

    coverage_notes = summary.get("coverage_notes")
    if not isinstance(coverage_notes, str) or not coverage_notes.strip():
        errors.append("JSON_SUMMARY.coverage_notes must be a non-empty string.")

    findings_value = summary.get("findings")
    if not isinstance(findings_value, list):
        errors.append("JSON_SUMMARY.findings must be an array.")
        findings_value = []

    scan_findings = scan_result.get("findings", [])
    evidence_by_id: Dict[str, Dict[str, Any]] = {}
    for item in scan_findings:
        evidence_id = item.get("evidence_id")
        if isinstance(evidence_id, str):
            evidence_by_id[evidence_id] = item

    required_highlight_refs = set(scan_result.get("required_highlight_evidence_ids", []) or [])
    seen_refs: set[str] = set()
    referenced_evidence: Dict[str, Dict[str, Any]] = {}

    required_finding_keys = {
        "id",
        "severity",
        "category",
        "file",
        "line",
        "snippet",
        "why",
        "fix",
        "evidence_refs",
    }

    for idx, finding in enumerate(findings_value, start=1):
        if not isinstance(finding, dict):
            errors.append(f"findings[{idx}] must be an object.")
            continue

        missing = sorted(required_finding_keys - set(finding.keys()))
        if missing:
            errors.append(f"findings[{idx}] missing required keys: {', '.join(missing)}")
            continue

        severity = finding.get("severity")
        category = finding.get("category")
        if severity not in SEVERITY_VALUES:
            errors.append(f"findings[{idx}].severity must be low/medium/high/critical.")
        if category not in CATEGORY_VALUES:
            errors.append(f"findings[{idx}].category must be one of A/B/C/D/E.")

        file_value = str(finding.get("file", "")).replace("\\", "/")
        line_value = finding.get("line")
        if not isinstance(line_value, int):
            errors.append(f"findings[{idx}].line must be an integer.")
            continue

        refs = finding.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            errors.append(f"findings[{idx}].evidence_refs must be a non-empty array.")
            continue

        location_match = False
        snippet_match = False
        for ref in refs:
            if not isinstance(ref, str):
                errors.append(f"findings[{idx}] has non-string evidence ref.")
                continue

            evidence = evidence_by_id.get(ref)
            if evidence is None:
                errors.append(f"findings[{idx}] references unknown evidence id: {ref}")
                continue

            seen_refs.add(ref)
            referenced_evidence[ref] = evidence

            evidence_file = str(evidence.get("file", "")).replace("\\", "/")
            evidence_line = int(evidence.get("line", 0))
            if evidence_file == file_value and evidence_line == line_value:
                location_match = True
            if snippets_match(str(finding.get("snippet", "")), str(evidence.get("snippet", ""))):
                snippet_match = True

        if not location_match:
            errors.append(f"findings[{idx}] file/line does not match any referenced evidence entry.")
        if not snippet_match:
            errors.append(f"findings[{idx}] snippet does not match referenced evidence snippet(s).")

    missing_required_refs = sorted(required_highlight_refs - seen_refs)
    if missing_required_refs:
        errors.append("Missing required highlight evidence references: " + ", ".join(missing_required_refs))

    partial_coverage = bool(scan_result.get("summary", {}).get("partial_coverage"))
    if partial_coverage and decision == "approve":
        errors.append("approve decision is invalid when script scan reports partial coverage.")

    if isinstance(risk_score, int):
        if risk_score >= 70 and decision != "reject":
            errors.append("risk_score >= 70 requires decision reject.")
        if 35 <= risk_score < 70 and decision == "approve":
            errors.append("risk_score >= 35 cannot use approve decision.")

    referenced = list(referenced_evidence.values())
    minimum_decision = severity_floor_decision(referenced, partial_coverage)
    minimum_score = minimum_score_floor(referenced)

    if minimum_decision == "reject" and decision != "reject":
        errors.append("Referenced evidence includes critical risk; decision must be reject.")
    elif minimum_decision == "caution" and decision == "approve":
        errors.append("Referenced evidence includes high risk; decision cannot be approve.")

    if isinstance(risk_score, int) and risk_score < minimum_score:
        errors.append(f"risk_score is below evidence-derived minimum floor ({minimum_score}).")

    if not findings_value and scan_findings:
        warnings.append("Assessment contains no findings while script scan produced evidence.")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stats": {
            "assessment_finding_count": len(findings_value),
            "script_finding_count": len(scan_findings),
            "required_highlight_refs": sorted(required_highlight_refs),
            "referenced_evidence_ids": sorted(seen_refs),
            "minimum_score_floor": minimum_score,
            "minimum_decision_floor": minimum_decision,
        },
    }


def load_scan_file(path_value: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    scan_path = Path(path_value).expanduser().resolve()
    try:
        payload = json.loads(scan_path.read_text(encoding="utf-8"))
    except OSError as exc:
        return None, f"failed to read --scan-file: {exc}"
    except ValueError as exc:
        return None, f"invalid --scan-file JSON: {exc}"
    if not isinstance(payload, dict):
        return None, "invalid --scan-file JSON: expected object root"
    return payload, None


def enforce_scan_integrity(
    scan_result: Dict[str, Any],
    target_repo: Path,
    max_findings: int,
) -> Tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    context_payload = scan_result.get("context_profile")
    context_json = json.dumps(context_payload) if isinstance(context_payload, dict) and context_payload else None
    profile, _ = parse_context_profile(context_json=context_json)

    fresh = scan_repository(target_repo=target_repo, max_findings=max_findings, context_profile=profile)

    expected_repo_fp = str(scan_result.get("integrity", {}).get("repo_fingerprint", ""))
    actual_repo_fp = str(fresh.get("integrity", {}).get("repo_fingerprint", ""))
    if expected_repo_fp and actual_repo_fp and expected_repo_fp != actual_repo_fp:
        errors.append("scan integrity mismatch: repo_fingerprint changed since scan artifact was produced.")

    expected_commit = str(scan_result.get("run", {}).get("commit_sha", ""))
    actual_commit = str(fresh.get("run", {}).get("commit_sha", ""))
    if expected_commit and actual_commit and expected_commit != actual_commit:
        errors.append("scan integrity mismatch: commit SHA changed since scan artifact was produced.")

    if not expected_repo_fp:
        warnings.append("scan file has no repo_fingerprint; integrity check limited.")
    if not expected_commit:
        warnings.append("scan file has no commit_sha; integrity check limited.")

    return errors, warnings
