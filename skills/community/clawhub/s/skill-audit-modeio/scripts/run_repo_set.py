#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


def _load_repo_set(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("repo-set must be a JSON array")
    for idx, item in enumerate(payload, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"repo-set item {idx} must be an object")
        if not isinstance(item.get("repo"), str) or not isinstance(item.get("label"), str):
            raise ValueError(f"repo-set item {idx} requires string fields repo and label")
    return payload


def _run_eval(script: Path, repo_dir: Path) -> tuple[dict[str, Any] | None, str | None]:
    proc = subprocess.run(
        [sys.executable, str(script), "evaluate", "--target-repo", str(repo_dir), "--json"],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout).strip()
        return None, err
    try:
        return json.loads(proc.stdout), None
    except ValueError as exc:
        return None, f"invalid evaluate output: {exc}"


def _metrics(results: list[dict[str, Any]]) -> dict[str, Any]:
    valid = [r for r in results if r.get("decision")]
    distribution: dict[str, dict[str, int]] = {}
    tp = fp = fn = 0

    for row in valid:
        label = row["label"]
        decision = row["decision"]
        distribution.setdefault(label, {})
        distribution[label][decision] = distribution[label].get(decision, 0) + 1

        predicted_bad = decision in {"reject", "caution"}
        actual_bad = label == "risky"
        if predicted_bad and actual_bad:
            tp += 1
        if predicted_bad and not actual_bad:
            fp += 1
        if not predicted_bad and actual_bad:
            fn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0

    return {
        "distribution": distribution,
        "precision": round(precision, 3),
        "recall": round(recall, 3),
        "tp": tp,
        "fp": fp,
        "fn": fn,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Run skill-audit benchmark against a repo-set JSON manifest.")
    parser.add_argument("--repo-set", required=True, help="Path to repo set JSON file.")
    parser.add_argument("--repos-root", required=True, help="Root directory containing cloned repos as owner__repo.")
    parser.add_argument(
        "--script",
        default=str(Path(__file__).resolve().parents[1] / "scripts" / "skill_safety_assessment.py"),
        help="Path to skill_safety_assessment.py script.",
    )
    parser.add_argument("--output", default=None, help="Optional output JSON path.")
    parser.add_argument("--limit", type=int, default=0, help="Optional limit on number of repos.")
    args = parser.parse_args()

    repo_set_path = Path(args.repo_set).expanduser().resolve()
    repos_root = Path(args.repos_root).expanduser().resolve()
    script_path = Path(args.script).expanduser().resolve()

    if not repo_set_path.exists():
        print(f"Error: --repo-set does not exist: {repo_set_path}", file=sys.stderr)
        return 2
    if not repos_root.exists() or not repos_root.is_dir():
        print(f"Error: --repos-root must be an existing directory: {repos_root}", file=sys.stderr)
        return 2
    if not script_path.exists():
        print(f"Error: --script does not exist: {script_path}", file=sys.stderr)
        return 2

    cases = _load_repo_set(repo_set_path)
    if args.limit and args.limit > 0:
        cases = cases[: args.limit]

    started = time.time()
    results: list[dict[str, Any]] = []
    for case in cases:
        repo = case["repo"]
        label = case["label"]
        local = repos_root / repo.replace("/", "__")
        if not local.exists():
            results.append(
                {
                    "repo": repo,
                    "label": label,
                    "decision": None,
                    "risk_score": None,
                    "error": "missing local clone",
                }
            )
            continue

        payload, err = _run_eval(script_path, local)
        if err:
            results.append(
                {
                    "repo": repo,
                    "label": label,
                    "decision": None,
                    "risk_score": None,
                    "error": err,
                }
            )
            continue

        assert payload is not None
        results.append(
            {
                "repo": repo,
                "label": label,
                "decision": payload.get("scoring", {}).get("suggested_decision"),
                "risk_score": payload.get("scoring", {}).get("risk_score"),
                "finding_count": payload.get("summary", {}).get("finding_count", 0),
                "actionable_finding_count": payload.get("summary", {}).get("actionable_finding_count", 0),
                "error": None,
            }
        )

    meta = _metrics(results)
    summary = {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "duration_sec": round(time.time() - started, 2),
        "repo_set": str(repo_set_path),
        "repos_root": str(repos_root),
        "target_count": len(cases),
        **meta,
        "results": results,
    }

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
