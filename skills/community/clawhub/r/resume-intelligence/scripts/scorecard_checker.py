#!/usr/bin/env python3
"""Check whether a resume scorecard includes required review sections."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = [
    "Recommendation",
    "Page-Length Strategy",
    "ATS Safety",
    "Recruiter First-Page Strength",
    "Keyword Coverage",
    "Top Fixes Before Applying",
    "Unsupported or Risky Claims",
    "Detailed Resume Gaps",
    "Final Notes",
]


@dataclass(frozen=True)
class ScorecardCheckResult:
    ok: bool
    missing_sections: list[str]


def has_heading(markdown: str, heading: str) -> bool:
    expected_h2 = f"## {heading}"
    expected_h3 = f"### {heading}"
    return any(line.strip() in {expected_h2, expected_h3} for line in markdown.splitlines())


def check_scorecard_text(markdown: str) -> ScorecardCheckResult:
    missing = [section for section in REQUIRED_SECTIONS if not has_heading(markdown, section)]
    return ScorecardCheckResult(ok=not missing, missing_sections=missing)


def render_result(result: ScorecardCheckResult) -> str:
    if result.ok:
        return "Scorecard sections: ok\n"
    return "Missing scorecard sections:\n" + "\n".join(
        f"- {section}" for section in result.missing_sections
    ) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scorecard", help="Path to resume-scorecard.md.")
    args = parser.parse_args()

    result = check_scorecard_text(Path(args.scorecard).read_text(encoding="utf-8"))
    print(render_result(result), end="")
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
