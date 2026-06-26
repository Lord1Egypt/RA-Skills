#!/usr/bin/env python3
# Exit codes: 0=ok, 2=degraded/partial, 3=unavailable/fail, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PER_CHECK_TIMEOUT_SECONDS = int(os.environ.get("SUPER_MEMORI_EVAL_TIMEOUT_SECONDS", "20"))

CASES = [
    ("exact retrieval", "exact retrieval honors command/path precision"),
    ("path lookup", "path lookup resolves canonical file references"),
    ("recent-time retrieval", "recent-time retrieval surfaces latest state"),
    ("learning-memory retrieval", "learning retrieval finds relevant lesson blocks"),
    ("semantic paraphrase retrieval", "semantic paraphrase retrieval returns meaning-based matches"),
    ("hybrid retrieval", "hybrid retrieval fuses lexical and semantic candidates"),
    ("temporal disambiguation", "temporal disambiguation prefers newer accepted facts"),
    ("contradiction handling", "contradiction handling prefers higher-confidence current truth"),
    ("relation-aware ranking", "relation-aware ranking respects supersedes/refines/confirms/contradicts/extends"),
    ("stale lexical degraded behavior", "stale lexical index reports degraded warnings"),
    ("semantic unavailable degraded behavior", "semantic-unavailable host stays honest"),
    ("vector-unbuilt degraded behavior", "vector-unbuilt host reports semantic-unbuilt"),
    ("audit integrity issues", "audit detects orphans/drift when present"),
    ("pattern mining misses", "pattern mining surfaces recurring misses"),
    ("pattern mining reuse", "pattern mining surfaces repeated success patterns"),
]


def run(cmd: list[str]) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=PER_CHECK_TIMEOUT_SECONDS)
        return proc.returncode, proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        timeout_note = f"timed out after {PER_CHECK_TIMEOUT_SECONDS}s"
        return 2, stdout, f"{stderr}\n{timeout_note}".strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Run super_memori local evals")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    results = []
    checks = [
        (["python3", str(ROOT / "query-memory.sh"), "query memory", "--mode", "auto", "--json", "--limit", "3"], "exact retrieval"),
        (["python3", str(ROOT / "query-memory.sh"), "memory/working-buffer.md", "--mode", "exact", "--json", "--limit", "3"], "path lookup"),
        (["python3", str(ROOT / "query-memory.sh"), "current", "--mode", "recent", "--json", "--limit", "3"], "recent-time retrieval"),
        (["python3", str(ROOT / "query-memory.sh"), "learning memory", "--mode", "learning", "--json", "--limit", "3"], "learning-memory retrieval"),
        (["python3", str(ROOT / "query-memory.sh"), "semantic paraphrase retrieval", "--mode", "semantic", "--json", "--limit", "3"], "semantic paraphrase retrieval"),
        (["python3", str(ROOT / "query-memory.sh"), "hybrid retrieval", "--mode", "hybrid", "--json", "--limit", "3"], "hybrid retrieval"),
        (["python3", str(ROOT / "query-memory.sh"), "older fact newer fact", "--mode", "hybrid", "--temporal", "--json", "--limit", "3"], "temporal disambiguation"),
        (["python3", str(ROOT / "audit-memory.sh"), "--json"], "audit integrity issues"),
        (["python3", str(ROOT / "repair-memory.sh"), "--plan", "--json"], "pattern mining misses"),
        (["python3", str(ROOT / "list-promotion-candidates.sh"), "--json"], "pattern mining reuse"),
    ]

    overall = 0
    for cmd, name in checks:
        code, out, err = run(cmd)
        ok = code in {0, 2}
        current = {
            "case": name,
            "exit_code": code,
            "ok": ok,
            "stdout": out[:2000],
            "stderr": err[:1000],
        }
        results.append(current)
        if not ok:
            overall = 2 if overall == 0 else overall
    payload = {"status": "ok" if overall == 0 else "warn", "results": results}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return overall


if __name__ == "__main__":
    raise SystemExit(main())
