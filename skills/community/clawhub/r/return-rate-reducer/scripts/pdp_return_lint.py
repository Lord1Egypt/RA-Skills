#!/usr/bin/env python3
"""
Lint a product page markdown for return-risk factors.

Checks for missing dimensions, absent size guide references, vague material
descriptions, overstatements, and missing compatibility info.

Usage:
    python3 scripts/pdp_return_lint.py --in product_page.md
    python3 scripts/pdp_return_lint.py --in product_page.md --category fashion
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass(frozen=True)
class LintIssue:
    category: str
    message: str
    evidence: str = ""


VAGUE_MATERIAL = [
    "premium material",
    "high-quality material",
    "quality fabric",
    "fine material",
    "luxurious fabric",
    "soft material",
    "durable material",
]

OVERSTATEMENTS = [
    r"\bperfect fit\b",
    r"\bfits everyone\b",
    r"\bone size fits all\b",
    r"\buniversal fit\b",
    r"\bexact match\b",
    r"\bexactly as shown\b",
    r"\bidentical to\b",
]

DIMENSION_PATTERNS = [
    r"\d+\s*(?:cm|mm|in(?:ch)?|inches|ft|feet|oz|grams?|g\b|kg|lb|lbs)",
    r"\d+\s*[\"\']\s*(?:x|\×)\s*\d+",
    r"\d+\s*x\s*\d+\s*(?:cm|mm|in|inches)",
]

SIZE_GUIDE_REFS = [
    "size guide", "size chart", "sizing guide", "measurement guide",
    "fit guide", "size table", "how to measure",
]


def word_count(text: str) -> int:
    return len(re.findall(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)?", text))


def lint_page(text: str, category: str = "") -> List[LintIssue]:
    issues: List[LintIssue] = []
    lower = text.lower()

    has_dimensions = any(re.search(p, text, re.IGNORECASE) for p in DIMENSION_PATTERNS)
    if not has_dimensions:
        issues.append(LintIssue(
            "Dimensions",
            "No dimensions found. Missing measurements are a top driver of 'not as described' returns.",
        ))

    for phrase in VAGUE_MATERIAL:
        if phrase in lower:
            issues.append(LintIssue(
                "Material",
                f"Vague material description: '{phrase}'. Specify the actual material (e.g. '100% organic cotton, 180gsm').",
                phrase,
            ))

    for pattern in OVERSTATEMENTS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        for match in matches:
            issues.append(LintIssue(
                "Overstatement",
                f"Risky claim: '{match}'. Fit and appearance vary; overstatements cause expectation-mismatch returns.",
                match,
            ))

    if category.lower() in ("fashion", "apparel", "clothing", "shoes", "jewelry"):
        has_size_guide = any(ref in lower for ref in SIZE_GUIDE_REFS)
        if not has_size_guide:
            issues.append(LintIssue(
                "Size guide",
                "No size guide reference found. Fashion products without size guides have significantly higher size-related returns.",
            ))

    if category.lower() in ("electronics", "tech", "accessories"):
        compat_keywords = ["compatible with", "works with", "fits", "supported", "not compatible"]
        has_compat = any(kw in lower for kw in compat_keywords)
        if not has_compat:
            issues.append(LintIssue(
                "Compatibility",
                "No compatibility info found. Electronics returns spike when customers can't verify device fit before purchase.",
            ))

    has_weight = bool(re.search(r"\d+\s*(?:oz|grams?|g\b|kg|lb|lbs)", text, re.IGNORECASE))
    if not has_weight:
        issues.append(LintIssue(
            "Weight",
            "No product weight found. Weight affects perceived quality — 'heavier than expected' or 'too light' appears in return reviews.",
        ))

    wc = word_count(text)
    if wc < 80:
        issues.append(LintIssue(
            "Length",
            f"Description is very short ({wc} words). Thin descriptions leave gaps that customers fill with assumptions — leading to returns.",
        ))

    return issues


def format_issues(issues: List[LintIssue]) -> str:
    if not issues:
        return "PDP RETURN LINT: OK (no return-risk issues found)"
    out = ["PDP RETURN LINT: issues found\n"]
    for i, issue in enumerate(issues, 1):
        out.append(f"{i}. [{issue.category}] {issue.message}")
        if issue.evidence:
            out.append(f"   Evidence: {issue.evidence}")
    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lint a product page for return-risk factors."
    )
    parser.add_argument("--in", dest="in_path", required=True, help="Path to product page markdown.")
    parser.add_argument("--category", default="", help="Product category (fashion, electronics, beauty, home).")
    args = parser.parse_args()

    text = Path(args.in_path).expanduser().read_text(encoding="utf-8")
    issues = lint_page(text, category=args.category)
    print(format_issues(issues))

    if issues:
        sys.exit(1)


if __name__ == "__main__":
    main()
