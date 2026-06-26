#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path

from replay_common import DEFAULT_REPLAY_FILE, load_jsonl, write_json


TRAIT_TERMS = {
    "structured academic output": ["thesis", "evidence", "draft structure", "claim-to-evidence"],
    "no fabricated citations": ["never invent", "do not invent", "source lead", "missing metadata"],
    "missing metadata flagged": ["missing", "metadata", "source metadata"],
    "clear mvp scope": ["mvp", "scope", "non-goals"],
    "testable acceptance criteria": ["acceptance criteria", "testable", "observable"],
    "implementation handoff": ["dev handoff", "handoff", "implementation"],
    "credential safety": ["credential", "secret", "token", "never be logged"],
    "health check": ["health check"],
    "failure handling": ["failure", "retry"],
    "deterministic script contract": ["input", "output", "exit code", "deterministic"],
    "input validation": ["validate", "validation"],
    "failure modes": ["failure modes", "exit codes"],
    "clear structure": ["workflow", "output contract", "quality gates"],
    "explicit assumptions": ["assumptions", "state assumptions"],
    "actionable output": ["output contract", "expected output", "handoff"],
}


def read_skill_text(skill_dir: Path) -> str:
    parts = []
    for path in [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*"))]:
        if path.exists() and path.is_file():
            parts.append(path.read_text(encoding="utf-8", errors="ignore"))
    return "\n".join(parts).lower()


def case_score(text: str, case: dict) -> dict:
    traits = case.get("expected_traits") or []
    checks = []
    for trait in traits:
        terms = TRAIT_TERMS.get(trait, [trait])
        matched = [term for term in terms if term.lower() in text]
        checks.append({"trait": trait, "passed": bool(matched)})
    passed = sum(1 for check in checks if check["passed"])
    score = round((passed / max(1, len(checks))) * 100)
    return {"case_id": case.get("id"), "score": score, "passed": score >= 70, "checks_run": len(checks)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run offline replay evaluation for a skill candidate.")
    parser.add_argument("--skill-dir", required=True)
    parser.add_argument("--cases", default=str(DEFAULT_REPLAY_FILE))
    parser.add_argument("--skill", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--min-score", type=int, default=70)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    cases = load_jsonl(Path(args.cases).expanduser())
    if args.skill:
        cases = [case for case in cases if case.get("skill") == args.skill]
    text = read_skill_text(skill_dir)
    results = [case_score(text, case) for case in cases]
    avg = round(sum(item["score"] for item in results) / len(results)) if results else 0
    status = "no-cases" if not results else "ok"
    payload = {
        "status": status,
        "skill": args.skill or skill_dir.name,
        "cases_run": len(results),
        "score": avg,
        "passed": bool(results) and avg >= args.min_score and all(item["passed"] for item in results),
        "details_hidden": True,
    }
    if args.output:
        write_json(Path(args.output).expanduser(), {**payload, "case_results": results})
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
    if not results:
        return 0
    return 0 if payload["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
