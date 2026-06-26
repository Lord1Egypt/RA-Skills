"""Comparators for evaluation scoring."""

from __future__ import annotations

import os
import re

from .scoring import Score


def compare_facts(expected: dict, actual: dict) -> Score:
    """Compare extracted facts against expected facts.

    Scores based on how many expected keys/values are present in actual output.
    """
    total_checks = 0
    matches = 0
    details_parts: list[str] = []

    # Check scalar fields
    for key in ("environment", "app_version", "build_number", "browser",
                "browser_version", "os", "region", "user_role"):
        expected_val = expected.get(key)
        if expected_val is None:
            continue
        total_checks += 1
        actual_val = actual.get(key)
        if actual_val and str(expected_val).lower() in str(actual_val).lower():
            matches += 1
            details_parts.append(f"  OK: {key}={actual_val}")
        else:
            details_parts.append(f"  MISS: {key} expected={expected_val}, got={actual_val}")

    # Check feature flags
    expected_flags = expected.get("feature_flags", {})
    actual_flags = actual.get("feature_flags", {})
    for k, v in expected_flags.items():
        total_checks += 1
        if k in actual_flags:
            matches += 1
            details_parts.append(f"  OK: flag {k}={actual_flags[k]}")
        else:
            details_parts.append(f"  MISS: flag {k} not found")

    # Check error_codes (list comparison)
    expected_codes = expected.get("error_codes", [])
    actual_codes = actual.get("error_codes", [])
    for code in expected_codes:
        total_checks += 1
        if code in actual_codes:
            matches += 1
            details_parts.append(f"  OK: error_code {code}")
        else:
            details_parts.append(f"  MISS: error_code {code} not found in {actual_codes}")

    # Check PII count (if specified)
    expected_pii = expected.get("pii_count")
    if expected_pii is not None:
        total_checks += 1
        # This will be checked in redaction scoring, skip here

    if total_checks == 0:
        return Score(
            dimension="facts_extraction",
            score=5, max_score=5,
            details="No expected facts to compare",
        )

    ratio = matches / total_checks
    score = round(ratio * 5, 1)

    return Score(
        dimension="facts_extraction",
        score=score,
        max_score=5,
        details=f"Matched {matches}/{total_checks} fields:\n" + "\n".join(details_parts),
    )


def compare_redaction(
    original: str,
    sanitized: str,
    report: dict,
) -> Score:
    """Score redaction quality by checking if known PII patterns are removed."""
    # Extract PII from original using simple patterns
    email_pattern = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    phone_pattern = re.compile(r"(?:\+?86[-.\s]?)?1[3-9]\d[-.\s]?\d{4}[-.\s]?\d{4}|\+?1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}")
    ip_pattern = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b")

    pii_in_original: list[str] = []
    pii_in_original.extend(email_pattern.findall(original))
    pii_in_original.extend(phone_pattern.findall(original))
    pii_in_original.extend(ip_pattern.findall(original))

    if not pii_in_original:
        return Score(dimension="redaction_recall", score=5, max_score=5, details="No PII in original")

    # Check how many are still in sanitized
    leaked = [pii for pii in pii_in_original if pii in sanitized]
    redacted = len(pii_in_original) - len(leaked)
    recall = redacted / len(pii_in_original)

    details = f"Found {len(pii_in_original)} PII items, redacted {redacted}, leaked {len(leaked)}"
    if leaked:
        details += f"\nLeaked: {leaked[:5]}"

    score = round(recall * 5, 1)
    return Score(dimension="redaction_recall", score=score, max_score=5, details=details)


def check_completeness(output_dir: str) -> Score:
    """Check if all expected output files exist and are non-empty."""
    expected_files = [
        "1_sanitized_ticket.md",
        "2_sanitized_logs.txt",
        "3_facts.json",
        "4_timeline.json",
        "5_engineering_issue.md",
        "6_internal_escalation.md",
        "7_customer_reply.md",
        "8_redaction_report.json",
    ]

    present = 0
    details_parts: list[str] = []

    for fname in expected_files:
        fpath = os.path.join(output_dir, fname)
        if os.path.exists(fpath):
            size = os.path.getsize(fpath)
            if size > 0:
                present += 1
                details_parts.append(f"  OK: {fname} ({size} bytes)")
            else:
                details_parts.append(f"  EMPTY: {fname}")
        else:
            details_parts.append(f"  MISSING: {fname}")

    ratio = present / len(expected_files)
    score = round(ratio * 5, 1)

    return Score(
        dimension="output_completeness",
        score=score,
        max_score=5,
        details=f"{present}/{len(expected_files)} files present:\n" + "\n".join(details_parts),
    )
