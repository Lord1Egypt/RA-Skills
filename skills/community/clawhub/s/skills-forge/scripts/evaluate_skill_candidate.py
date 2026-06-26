#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


PROFILE_CHECKS = {
    "academic": [
        ("citation styles", ["apa", "mla", "chicago", "harvard"]),
        ("source metadata", ["metadata", "missing-fields", "missing fields", "source lead"]),
        ("anti-fabrication", ["never invent", "do not invent", "fake citation", "fake reference"]),
    ],
    "product": [
        ("mvp scope", ["mvp", "must-have", "non-goals", "not-now"]),
        ("testable handoff", ["acceptance criteria", "dev handoff", "observable", "testable"]),
        ("prioritization", ["must-have", "should-have", "not-now"]),
    ],
    "integration": [
        ("credential safety", ["credential", "secret", "token", "never be logged"]),
        ("health checks", ["health check", "failure", "retry"]),
        ("external system setup", ["api", "oauth", "webhook", "connector", "integration"]),
    ],
    "script": [
        ("script contract", ["input", "output", "exit code", "validation"]),
        ("safe mutation", ["dry-run", "validate", "failure", "exit codes"]),
        ("deterministic execution", ["script", "cli", "machine-readable", "deterministic"]),
    ],
    "workflow": [
        ("repeatability", ["recurring", "repeatable", "stable workflow"]),
        ("output contract", ["output contract", "expected output", "quality checks"]),
        ("decision rules", ["decision", "quality gate", "assumptions"]),
    ],
}


PROFILE_HINTS = {
    profile: sorted({term for _, terms in checks for term in terms})
    for profile, checks in PROFILE_CHECKS.items()
}


def read_candidate(skill_dir: Path) -> tuple[str, list[str]]:
    pieces = []
    paths = []
    for path in [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*"))]:
        if path.exists() and path.is_file():
            paths.append(str(path.relative_to(skill_dir)))
            pieces.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(pieces).lower(), paths


def infer_profile(text: str) -> str:
    scores = {
        profile: sum(1 for term in hints if term in text)
        for profile, hints in PROFILE_HINTS.items()
    }
    profile, score = max(scores.items(), key=lambda item: item[1])
    return profile if score else "workflow"


def run_checks(text: str, profile: str) -> list[dict]:
    checks = []
    for name, terms in PROFILE_CHECKS.get(profile, PROFILE_CHECKS["workflow"]):
        matched = [term for term in terms if term in text]
        checks.append(
            {
                "name": name,
                "passed": bool(matched),
                "matched_terms": matched,
            }
        )
    return checks


def summarize(checks: list[dict]) -> tuple[bool, int]:
    passed_count = sum(1 for check in checks if check["passed"])
    score = round((passed_count / max(1, len(checks))) * 100)
    return passed_count == len(checks), score


def main() -> int:
    parser = argparse.ArgumentParser(description="Run hidden smoke evaluation for a skill candidate.")
    parser.add_argument("skill_dir", help="Candidate skill directory.")
    parser.add_argument("--profile", default="auto", help="Expected profile or auto.")
    parser.add_argument(
        "--show-details",
        action="store_true",
        help="Show internal check details. Keep off for user-facing runs.",
    )
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    text, files_read = read_candidate(skill_dir)
    profile = infer_profile(text) if args.profile == "auto" else args.profile
    checks = run_checks(text, profile)
    passed, score = summarize(checks)

    payload = {
        "passed": passed,
        "score": score,
        "profile": profile,
        "checks_run": len(checks),
        "details_hidden": not args.show_details,
    }
    if args.show_details:
        payload["files_read"] = files_read
        payload["checks"] = checks

    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print("PASS" if passed else "FAIL")
        print(f"score={score} profile={profile} checks_run={len(checks)}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
