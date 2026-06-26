from __future__ import annotations

import copy
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from .json_utils import extract_first_json_object

CLASSIFICATION_VALUES = {"true_positive", "false_positive", "uncertain"}
ADJUSTMENT_VALUES = {"keep", "downgrade", "ignore"}
CONFIDENCE_VALUES = {"low", "medium", "high"}

ADJUSTMENT_FACTOR = {
    "keep": 1.0,
    "downgrade": 0.5,
    "ignore": 0.0,
}

CONFIDENCE_FACTOR = {
    "low": 0.90,
    "medium": 1.00,
    "high": 1.05,
}


def parse_adjudication_text(raw_text: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        payload = json.loads(raw_text)
        if isinstance(payload, dict):
            return payload, None
    except ValueError:
        pass

    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_text, flags=re.IGNORECASE | re.DOTALL)
    candidate = fenced.group(1) if fenced else extract_first_json_object(raw_text)
    if not candidate:
        return None, "Could not parse adjudication JSON payload."

    try:
        payload = json.loads(candidate)
    except ValueError as exc:
        return None, f"Invalid adjudication JSON: {exc}"
    if not isinstance(payload, dict):
        return None, "Adjudication payload must be a JSON object."
    return payload, None


def build_adjudication_prompt(scan_result: Dict[str, Any], profile: Optional[Dict[str, Any]] = None) -> str:
    findings = scan_result.get("findings", [])
    lines: List[str] = []
    lines.append("Skill Safety Assessment adjudication request")
    lines.append("Goal: classify each evidence item using repository context.")
    lines.append("")
    lines.append("Rules:")
    lines.append("1) Do not invent new evidence IDs.")
    lines.append("2) Use only E-* entries listed below.")
    lines.append("3) Mark false positives explicitly when context is docs/example/test-only.")
    lines.append("4) Keep high confidence only with strong path+snippet justification.")
    lines.append("")
    if profile:
        lines.append("Context profile:")
        lines.append("```json")
        lines.append(json.dumps(profile, ensure_ascii=False, indent=2))
        lines.append("```")
        lines.append("")

    lines.append("Evidence list:")
    if findings:
        for item in findings[:30]:
            lines.append(
                "- "
                + f"{item.get('evidence_id')} | {item.get('severity')}/{item.get('category')} | "
                + f"{item.get('file')}:{item.get('line')} | {item.get('rule_id')}"
            )
    else:
        lines.append("- none")

    lines.append("")
    lines.append("Return JSON only with this schema:")
    lines.append("```json")
    lines.append(
        json.dumps(
            {
                "evidence_decisions": [
                    {
                        "evidence_id": "E-XXXXXXXXXX",
                        "classification": "true_positive|false_positive|uncertain",
                        "adjustment": "keep|downgrade|ignore",
                        "confidence": "low|medium|high",
                        "rationale": "brief explanation tied to context",
                    }
                ],
                "overall_notes": "optional",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    lines.append("```")
    return "\n".join(lines)


def _validate_decisions(
    payload: Dict[str, Any],
    evidence_ids: set[str],
) -> Tuple[List[Dict[str, Any]], List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []
    decisions_raw = payload.get("evidence_decisions")
    if not isinstance(decisions_raw, list):
        return [], ["adjudication.evidence_decisions must be an array."], warnings

    decisions: List[Dict[str, Any]] = []
    seen_ids: set[str] = set()
    for idx, item in enumerate(decisions_raw, start=1):
        if not isinstance(item, dict):
            errors.append(f"evidence_decisions[{idx}] must be an object.")
            continue

        evidence_id = item.get("evidence_id")
        classification = item.get("classification")
        adjustment = item.get("adjustment")
        confidence = item.get("confidence")
        rationale = item.get("rationale")

        if not isinstance(evidence_id, str):
            errors.append(f"evidence_decisions[{idx}].evidence_id must be a string.")
            continue
        if evidence_id not in evidence_ids:
            errors.append(f"evidence_decisions[{idx}] references unknown evidence id: {evidence_id}")
            continue
        if evidence_id in seen_ids:
            errors.append(f"evidence_decisions[{idx}] duplicates evidence id: {evidence_id}")
            continue

        if classification not in CLASSIFICATION_VALUES:
            errors.append(
                f"evidence_decisions[{idx}].classification must be one of {', '.join(sorted(CLASSIFICATION_VALUES))}."
            )
            continue
        if adjustment not in ADJUSTMENT_VALUES:
            errors.append(
                f"evidence_decisions[{idx}].adjustment must be one of {', '.join(sorted(ADJUSTMENT_VALUES))}."
            )
            continue
        if confidence not in CONFIDENCE_VALUES:
            errors.append(
                f"evidence_decisions[{idx}].confidence must be one of {', '.join(sorted(CONFIDENCE_VALUES))}."
            )
            continue
        if not isinstance(rationale, str) or not rationale.strip():
            errors.append(f"evidence_decisions[{idx}].rationale must be a non-empty string.")
            continue

        seen_ids.add(evidence_id)
        decisions.append(
            {
                "evidence_id": evidence_id,
                "classification": classification,
                "adjustment": adjustment,
                "confidence": confidence,
                "rationale": rationale.strip(),
            }
        )

    missing = sorted(evidence_ids - seen_ids)
    if missing:
        warnings.append("No adjudication decision provided for evidence IDs: " + ", ".join(missing))
    return decisions, errors, warnings


def _derive_decision(score: int, active_findings: List[Dict[str, Any]], partial_coverage: bool) -> str:
    has_critical = any(item.get("severity") == "critical" for item in active_findings)
    has_high = any(item.get("severity") == "high" for item in active_findings)

    if partial_coverage:
        return "caution"
    if has_critical or score >= 70:
        return "reject"
    if has_high or score >= 35:
        return "caution"
    return "approve"


def merge_adjudication(scan_result: Dict[str, Any], adjudication: Dict[str, Any]) -> Dict[str, Any]:
    findings = scan_result.get("findings", [])
    evidence_ids = {
        str(item.get("evidence_id"))
        for item in findings
        if isinstance(item, dict) and isinstance(item.get("evidence_id"), str)
    }

    decisions, errors, warnings = _validate_decisions(adjudication, evidence_ids)
    if errors:
        return {
            "valid": False,
            "errors": errors,
            "warnings": warnings,
            "adjudicated": {},
        }

    decisions_by_id = {item["evidence_id"]: item for item in decisions}
    merged_findings: List[Dict[str, Any]] = []
    adjusted_risk_raw = 0.0

    for finding in findings:
        evidence_id = finding.get("evidence_id")
        if not isinstance(evidence_id, str):
            continue

        base_risk = float(finding.get("risk_contribution", 0.0))
        decision = decisions_by_id.get(
            evidence_id,
            {
                "classification": "uncertain",
                "adjustment": "keep",
                "confidence": "low",
                "rationale": "No adjudication provided; kept as uncertain.",
            },
        )
        factor = ADJUSTMENT_FACTOR[decision["adjustment"]] * CONFIDENCE_FACTOR[decision["confidence"]]
        adjusted = round(base_risk * factor, 2)

        item = copy.deepcopy(finding)
        item["adjudication"] = decision
        item["adjusted_risk_contribution"] = adjusted
        merged_findings.append(item)

        if decision["classification"] == "false_positive" and decision["adjustment"] == "ignore":
            continue
        adjusted_risk_raw += adjusted

    adjusted_risk_raw = round(adjusted_risk_raw, 2)
    obfuscation_bonus = 10 if any(item.get("category") == "D" for item in merged_findings) else 0
    coverage_penalty = int(scan_result.get("scoring", {}).get("coverage_penalty", 0))

    risk_score = min(100, int(round(adjusted_risk_raw + obfuscation_bonus + coverage_penalty)))
    partial_coverage = bool(scan_result.get("summary", {}).get("partial_coverage"))

    active_findings = [
        item
        for item in merged_findings
        if item.get("adjudication", {}).get("adjustment") != "ignore"
    ]
    decision = _derive_decision(risk_score, active_findings, partial_coverage)

    return {
        "valid": True,
        "errors": [],
        "warnings": warnings,
        "adjudicated": {
            "risk_raw": adjusted_risk_raw,
            "risk_score": risk_score,
            "suggested_decision": decision,
            "finding_count": len(active_findings),
            "findings": merged_findings,
            "overall_notes": adjudication.get("overall_notes", ""),
        },
    }
