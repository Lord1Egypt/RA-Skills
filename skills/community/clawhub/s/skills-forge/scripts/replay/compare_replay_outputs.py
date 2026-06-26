#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def run_eval(skill_dir: str, cases: str, skill: str, min_score: int) -> dict:
    completed = subprocess.run(
        [
            sys.executable,
            str(BASE_DIR / "run_replay_eval.py"),
            "--skill-dir",
            skill_dir,
            "--cases",
            cases,
            "--skill",
            skill,
            "--min-score",
            str(min_score),
            "--json",
        ],
        text=True,
        capture_output=True,
    )
    payload = json.loads(completed.stdout)
    payload["returncode"] = completed.returncode
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare baseline and candidate replay scores.")
    parser.add_argument("--baseline", required=True)
    parser.add_argument("--candidate", required=True)
    parser.add_argument("--cases", required=True)
    parser.add_argument("--skill", required=True)
    parser.add_argument("--min-score", type=int, default=70)
    parser.add_argument("--min-improvement", type=int, default=0)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    baseline = run_eval(args.baseline, args.cases, args.skill, args.min_score)
    candidate = run_eval(args.candidate, args.cases, args.skill, args.min_score)
    improvement = candidate["score"] - baseline["score"]
    passed = candidate["passed"] and improvement >= args.min_improvement
    payload = {
        "status": "ok",
        "skill": args.skill,
        "baseline_score": baseline["score"],
        "candidate_score": candidate["score"],
        "improvement": improvement,
        "cases_run": candidate["cases_run"],
        "passed": passed,
        "details_hidden": True,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
