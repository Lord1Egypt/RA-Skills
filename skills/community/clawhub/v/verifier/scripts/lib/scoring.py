#!/usr/bin/env python3

def _missing_for_case_type(case_type: str):
    defaults = {
        "offer": [
            "Needs original sender identity proof",
            "Needs official company or organization source",
            "Needs fuller context on requested action"
        ],
        "profile": [
            "Needs public identity cross-check",
            "Needs source context for profile claim"
        ],
        "screenshot": [
            "Needs raw screenshot text extraction",
            "Needs wider context around the screenshot"
        ],
        "website": [
            "Needs source summary",
            "Needs trust signals or ownership context"
        ],
        "message": [
            "Needs sender context",
            "Needs fuller message history"
        ],
        "source": [
            "Needs original source reference",
            "Needs summary of source claims"
        ],
        "claim": [
            "Needs original source URL or reference",
            "Needs supporting or contradicting evidence"
        ]
    }
    return defaults.get(case_type, ["Needs stronger supporting evidence"])

def score_case(case):
    evidence_items = case.get("evidence_items", [])
    supports = sum(1 for e in evidence_items if e.get("support_level") == "supports")
    contradicts = sum(1 for e in evidence_items if e.get("support_level") == "contradicts")
    neutral = sum(1 for e in evidence_items if e.get("support_level") == "neutral")

    red_flags = []
    green_flags = []
    missing_evidence = []

    if not case.get("claim"):
        missing_evidence.append("Needs a clear claim statement")

    if len(evidence_items) == 0:
        missing_evidence.extend(_missing_for_case_type(case.get("type", "claim")))
        return {
            "verdict": "inconclusive",
            "confidence": "low",
            "risk_level": "medium" if case.get("type") in ["offer", "message", "website"] else "low",
            "red_flags": red_flags,
            "green_flags": green_flags,
            "missing_evidence": missing_evidence,
            "recommended_next_step": "Add at least one structured evidence item before making a stronger judgment."
        }

    if contradicts > 0:
        red_flags.append(f"{contradicts} contradicting evidence item(s) present")
    if supports > 0:
        green_flags.append(f"{supports} supporting evidence item(s) present")
    if neutral > 0:
        green_flags.append(f"{neutral} neutral evidence item(s) recorded")

    if supports == 0 and contradicts == 0:
        missing_evidence.append("Needs evidence that clearly supports or contradicts the claim")
        return {
            "verdict": "inconclusive",
            "confidence": "low",
            "risk_level": "low",
            "red_flags": red_flags,
            "green_flags": green_flags,
            "missing_evidence": missing_evidence,
            "recommended_next_step": "Add stronger evidence with clear support_level values."
        }

    if contradicts > 0 and supports == 0:
        verdict = "likely_risky" if contradicts == 1 else "false_or_misleading"
        confidence = "medium" if contradicts == 1 else "high"
        risk_level = "medium" if contradicts == 1 else "high"
        return {
            "verdict": verdict,
            "confidence": confidence,
            "risk_level": risk_level,
            "red_flags": red_flags,
            "green_flags": green_flags,
            "missing_evidence": missing_evidence,
            "recommended_next_step": "Seek original-source confirmation before trusting or acting on this claim."
        }

    if supports > 0 and contradicts == 0:
        verdict = "likely_true" if supports == 1 else "verified"
        confidence = "medium" if supports == 1 else "high"
        risk_level = "low"
        return {
            "verdict": verdict,
            "confidence": confidence,
            "risk_level": risk_level,
            "red_flags": red_flags,
            "green_flags": green_flags,
            "missing_evidence": missing_evidence,
            "recommended_next_step": "Preserve source references in case further review is needed."
        }

    missing_evidence.append("Conflicting evidence needs stronger source resolution")
    return {
        "verdict": "inconclusive",
        "confidence": "low",
        "risk_level": "medium",
        "red_flags": red_flags,
        "green_flags": green_flags,
        "missing_evidence": missing_evidence,
        "recommended_next_step": "Resolve conflicts by adding higher-quality evidence or original-source context."
    }
