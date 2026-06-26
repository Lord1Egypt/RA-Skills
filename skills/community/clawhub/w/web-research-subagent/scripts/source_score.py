#!/usr/bin/env python3
"""Score candidate web sources with a simple research-quality checklist.

Usage:
  source_score.py --url https://example.com --primary --dated --specific --corroborated
  source_score.py --title "Blog post" --dated --specific --red-flag seo

This is a lightweight decision aid, not a truth oracle.
"""

import argparse

WEIGHTS = {
    "primary": 3,
    "official": 3,
    "dated": 1,
    "versioned": 1,
    "specific": 2,
    "author": 1,
    "citations": 1,
    "corroborated": 2,
}
RED_FLAGS = {
    "undated-changing-topic": -3,
    "seo": -2,
    "anonymous": -1,
    "no-evidence": -2,
    "outdated": -3,
    "sponsored": -1,
    "contradicted": -4,
}


def tier(score: int) -> str:
    if score >= 8:
        return "authoritative/strong"
    if score >= 5:
        return "usable with light verification"
    if score >= 2:
        return "useful for discovery; verify before relying"
    return "weak; avoid for final claims"


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a candidate research source.")
    parser.add_argument("--url", default="", help="Source URL")
    parser.add_argument("--title", default="", help="Source title")
    for flag in WEIGHTS:
        parser.add_argument(f"--{flag}", action="store_true", help=f"+{WEIGHTS[flag]}: source is {flag}")
    parser.add_argument(
        "--red-flag",
        action="append",
        choices=sorted(RED_FLAGS),
        default=[],
        help="Subtract for a reliability concern; may be repeated",
    )
    args = parser.parse_args()

    positives = [name for name in WEIGHTS if getattr(args, name)]
    score = sum(WEIGHTS[name] for name in positives) + sum(RED_FLAGS[name] for name in args.red_flag)

    label = args.title or args.url or "candidate source"
    print(f"Source: {label}")
    print(f"Score: {score}")
    print(f"Tier: {tier(score)}")
    if positives:
        print("Strengths: " + ", ".join(positives))
    if args.red_flag:
        print("Concerns: " + ", ".join(args.red_flag))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
