"""CLI runner for YouOS evaluation suite."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from app.evaluation.service import EvalRequest, EvalSuiteResult, run_eval_suite
from app.generation.service import DraftRequest, generate_draft

ROOT_DIR = Path(__file__).resolve().parents[1]


def _generate_for_eval(
    prompt_text: str,
    *,
    database_url: str,
    configs_dir: Path,
) -> dict[str, Any]:
    """Wrap generate_draft for the eval runner interface."""
    response = generate_draft(
        DraftRequest(inbound_message=prompt_text),
        database_url=database_url,
        configs_dir=configs_dir,
    )
    return {
        "draft": response.draft,
        "detected_mode": response.detected_mode,
        "confidence": response.confidence,
        "precedent_count": len(response.precedent_used),
    }


def _format_scorecard(result: EvalSuiteResult) -> str:
    lines: list[str] = []
    lines.append(f"YouOS Eval — config: {result.config_tag} | {result.run_at}")
    lines.append("━" * 60)

    for cr in result.case_results:
        icon = {"pass": "✅", "warn": "⚠️", "fail": "❌"}.get(cr.pass_fail, "?")
        kw_pct = int(cr.scores.get("keyword_hit_rate", 0) * 100)
        wc = cr.scores.get("word_count", 0)
        lines.append(f" {cr.case_key:<30} {icon} {cr.pass_fail:<5} | mode={cr.detected_mode:<8} conf={cr.confidence:<6} kw={kw_pct}%{'':<4} words={wc}")

    lines.append("━" * 60)

    total = result.total_cases
    avg_conf = 0.0
    avg_kw = 0.0
    if total:
        avg_conf = sum(cr.scores.get("confidence_score", 0) for cr in result.case_results) / total
        avg_kw = sum(cr.scores.get("keyword_hit_rate", 0) for cr in result.case_results) / total

    lines.append(f" Total: {total} | Pass: {result.passed} | Warn: {result.warned} | Fail: {result.failed}")
    lines.append(f" Avg confidence: {avg_conf:.2f} | Avg keyword hit: {avg_kw:.2f}")
    return "\n".join(lines)


def main() -> None:
    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    parser = argparse.ArgumentParser(description="Run YouOS evaluation suite")
    parser.add_argument("--case", type=str, default=None, help="Run a specific case by key")
    parser.add_argument("--tag", type=str, default="default", help="Config tag label for this run")
    parser.add_argument("--summary-only", action="store_true", help="Print scorecard without saving to DB")
    parser.add_argument(
        "--db-path",
        type=Path,
        default=resolve_sqlite_path(get_settings().database_url),
        help="Path to SQLite database",
    )
    args = parser.parse_args()

    database_url = f"sqlite:///{args.db_path}"
    configs_dir = ROOT_DIR / "configs"

    request = EvalRequest(
        case_key=args.case,
        config_tag=args.tag,
    )

    result = run_eval_suite(
        request,
        generate_fn=_generate_for_eval,
        database_url=database_url,
        configs_dir=configs_dir,
        persist=not args.summary_only,
    )

    print(_format_scorecard(result))


if __name__ == "__main__":
    main()
