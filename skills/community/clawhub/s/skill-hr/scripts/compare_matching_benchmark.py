#!/usr/bin/env python3
"""Compare P02 outputs against gold labels in benchmarks/matching/cases.jsonl.

Usage:
  python compare_matching_benchmark.py \\
    --cases ../benchmarks/matching/cases.jsonl \\
    --outputs path/to/outputs.jsonl

Each line of outputs.jsonl must be a JSON object with:
  "case_id": "<same as case>",
  "p02": { ... P02 object per schemas/p02-output.schema.json ... }

Exit code 0 always; prints metrics and failures to stdout/stderr.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{path}:{line_no}: invalid JSON: {e}") from e
    return rows


def acceptable_ids(case: dict[str, Any]) -> set[str]:
    s: set[str] = set()
    gp = case.get("gold_primary_skill_id")
    if isinstance(gp, str) and gp:
        s.add(gp)
    extra = case.get("gold_acceptable_skill_ids")
    if isinstance(extra, list):
        for x in extra:
            if isinstance(x, str) and x:
                s.add(x)
    return s


def ranked_skill_ids(p02: dict[str, Any]) -> list[str]:
    cands = p02.get("candidates")
    if not isinstance(cands, list):
        return []
    scored: list[tuple[int, str]] = []
    for c in cands:
        if not isinstance(c, dict):
            continue
        sid = c.get("skill_id")
        sc = c.get("score")
        if isinstance(sid, str) and isinstance(sc, int):
            scored.append((sc, sid))
    scored.sort(key=lambda t: (-t[0], t[1]))
    return [sid for _, sid in scored]


def validate_p02_shape(p02: dict[str, Any], case: dict[str, Any]) -> list[str]:
    """Lightweight structural checks (no external jsonschema)."""
    errs: list[str] = []
    for key in ("recall_shortlist", "candidates", "best", "decision", "decision_rationale"):
        if key not in p02:
            errs.append(f"missing p02.{key}")

    best = p02.get("best")
    if isinstance(best, dict):
        if not isinstance(best.get("skill_id"), str):
            errs.append("best.skill_id must be string")
        if not isinstance(best.get("score"), int):
            errs.append("best.score must be int")

    rs = p02.get("recall_shortlist")
    cands = p02.get("candidates")
    if isinstance(rs, list) and isinstance(cands, list):
        rs_set = {x for x in rs if isinstance(x, str)}
        seen: set[str] = set()
        for i, c in enumerate(cands):
            if not isinstance(c, dict):
                errs.append(f"candidates[{i}] not object")
                continue
            sid = c.get("skill_id")
            if not isinstance(sid, str):
                errs.append(f"candidates[{i}].skill_id invalid")
                continue
            if sid not in rs_set:
                errs.append(f"candidate {sid} not in recall_shortlist")
            if sid in seen:
                errs.append(f"duplicate candidate skill_id {sid}")
            seen.add(sid)
        if seen != rs_set:
            missing = rs_set - seen
            extra = seen - rs_set
            if missing:
                errs.append(f"candidates missing shortlist ids: {sorted(missing)}")
            if extra:
                errs.append(f"candidates extra ids vs shortlist: {sorted(extra)}")

    jd = case.get("gold_jd")
    must = []
    if isinstance(jd, dict):
        mh = jd.get("must_have_competencies")
        if isinstance(mh, list):
            must = [str(x) for x in mh if x]

    if isinstance(cands, list):
        for i, c in enumerate(cands):
            if not isinstance(c, dict):
                continue
            subs = c.get("subscores")
            if not isinstance(subs, dict):
                errs.append(f"{c.get('skill_id')}: missing subscores")
                continue
            keys = (
                "outcome_fit",
                "competency_coverage",
                "tool_stack_fit",
                "quality_safety",
                "freshness_trust",
            )
            total = 0
            for k in keys:
                v = subs.get(k)
                if not isinstance(v, int):
                    errs.append(f"{c.get('skill_id')}: subscores.{k} not int")
                    break
                total += v
            else:
                sc = c.get("score")
                if isinstance(sc, int) and total != sc:
                    errs.append(
                        f"{c.get('skill_id')}: subscores sum {total} != score {sc}"
                    )
            matrix = c.get("competency_coverage_matrix")
            if not isinstance(matrix, list) or not matrix:
                errs.append(f"{c.get('skill_id')}: empty competency_coverage_matrix")
            elif must:
                comps = [
                    row.get("competency", "").strip().casefold()
                    for row in matrix
                    if isinstance(row, dict) and isinstance(row.get("competency"), str)
                ]
                for m in must:
                    mc = m.strip().casefold()
                    if mc not in comps:
                        errs.append(
                            f"{c.get('skill_id')}: matrix missing must_have {m!r}"
                        )

    return errs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path(__file__).resolve().parent.parent
        / "benchmarks"
        / "matching"
        / "cases.jsonl",
        help="Path to cases.jsonl",
    )
    parser.add_argument(
        "--outputs",
        type=Path,
        required=True,
        help="Path to outputs.jsonl (case_id + p02 per line)",
    )
    args = parser.parse_args()

    if not args.cases.is_file():
        print(f"Cases file not found: {args.cases}", file=sys.stderr)
        return 2
    if not args.outputs.is_file():
        print(f"Outputs file not found: {args.outputs}", file=sys.stderr)
        return 2

    cases = {c["case_id"]: c for c in load_jsonl(args.cases) if "case_id" in c}
    outputs_list = load_jsonl(args.outputs)
    outputs = {}
    for row in outputs_list:
        cid = row.get("case_id")
        if isinstance(cid, str):
            outputs[cid] = row

    missing = sorted(set(cases) - set(outputs))
    extra = sorted(set(outputs) - set(cases))
    if missing:
        print(f"Warning: outputs missing {len(missing)} case_ids", file=sys.stderr)
    if extra:
        print(f"Warning: outputs has unknown {len(extra)} case_ids", file=sys.stderr)

    decision_correct = 0
    decision_n = 0
    p1_correct = 0
    p1_n = 0
    p3_correct = 0
    p3_n = 0
    rr_sum = 0.0
    mrr_n = 0
    recall_hits = 0
    recall_n = 0
    failures: list[str] = []

    for cid, case in sorted(cases.items()):
        row = outputs.get(cid)
        if not row:
            failures.append(f"{cid}: no output row")
            continue
        p02 = row.get("p02")
        if not isinstance(p02, dict):
            failures.append(f"{cid}: p02 missing or not object")
            continue

        v_errs = validate_p02_shape(p02, case)
        if v_errs:
            for e in v_errs:
                failures.append(f"{cid}: validate: {e}")

        gold_dec = case.get("gold_decision")
        if gold_dec not in ("delegate", "confirm", "recruit"):
            failures.append(f"{cid}: bad gold_decision")
            continue

        decision_n += 1
        out_dec = p02.get("decision")
        if out_dec == gold_dec:
            decision_correct += 1
        else:
            failures.append(
                f"{cid}: decision got {out_dec!r} want {gold_dec!r}"
            )

        acc = acceptable_ids(case)
        primary = case.get("gold_primary_skill_id")
        is_recruit_gold = gold_dec == "recruit" or not (
            isinstance(primary, str) and primary
        )

        rs = p02.get("recall_shortlist")
        if isinstance(rs, list) and acc:
            recall_n += 1
            rs_set = {x for x in rs if isinstance(x, str)}
            if acc & rs_set:
                recall_hits += 1
            elif not is_recruit_gold:
                failures.append(
                    f"{cid}: recall_shortlist misses all acceptable {sorted(acc)}"
                )

        if is_recruit_gold:
            continue

        p1_n += 1
        best = p02.get("best")
        bid = best.get("skill_id") if isinstance(best, dict) else None
        if isinstance(bid, str) and bid in acc:
            p1_correct += 1
        else:
            failures.append(
                f"{cid}: P@1 best {bid!r} not in acceptable {sorted(acc)}"
            )

        ranked = ranked_skill_ids(p02)
        p3_n += 1
        top3 = set(ranked[:3])
        if acc & top3:
            p3_correct += 1
        else:
            failures.append(
                f"{cid}: P@3 no hit in top3 {ranked[:3]!r} acceptable {sorted(acc)}"
            )

        mrr_n += 1
        rr = 0.0
        for i, sid in enumerate(ranked, 1):
            if sid in acc:
                rr = 1.0 / i
                break
        rr_sum += rr
        if rr == 0.0:
            failures.append(f"{cid}: MRR miss ranked={ranked!r}")

    def pct(a: int, b: int) -> str:
        return f"{100.0 * a / b:.1f}%" if b else "n/a"

    print("=== skill-hr matching benchmark ===")
    print(f"cases: {len(cases)}  outputs: {len(outputs)}")
    print(f"decision accuracy: {decision_correct}/{decision_n} ({pct(decision_correct, decision_n)})")
    print(f"P@1: {p1_correct}/{p1_n} ({pct(p1_correct, p1_n)})")
    print(f"P@3: {p3_correct}/{p3_n} ({pct(p3_correct, p3_n)})")
    print(f"MRR: {rr_sum / mrr_n:.4f}" if mrr_n else "MRR: n/a")
    if recall_n:
        print(
            f"recall@shortlist (any acceptable in recall_shortlist): "
            f"{recall_hits}/{recall_n} ({pct(recall_hits, recall_n)})"
        )
    else:
        print("recall@shortlist: n/a")

    if failures:
        print("\n--- failures (deduped) ---", file=sys.stderr)
        for line in sorted(set(failures)):
            print(line, file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
