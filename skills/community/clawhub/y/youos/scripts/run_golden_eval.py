"""Run golden benchmark evaluation against curated test cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml

from app.core.settings import get_var_dir

ROOT_DIR = Path(__file__).resolve().parents[1]
GOLDEN_PATH = ROOT_DIR / "configs" / "benchmarks" / "golden.yaml"
# Per-instance: results from each instance's nightly land in its own var/
# so multiple instances don't clobber each other's last-eval JSON.
RESULTS_PATH = get_var_dir() / "golden_results.json"


def load_golden_cases(path: Path | None = None) -> list[dict[str, Any]]:
    """Load golden benchmark cases from YAML."""
    p = path or GOLDEN_PATH
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    return data.get("cases", [])


def score_case(
    case: dict[str, Any],
    draft: str,
    detected_mode: str,
    detected_language: str | None = None,
) -> dict[str, Any]:
    """Score a single golden benchmark case."""
    draft_lower = draft.lower()
    words = draft.split()
    word_count = len(words)

    # Keyword hit rate
    expected_keywords = case.get("expected_keywords", [])
    if expected_keywords:
        hits = sum(1 for kw in expected_keywords if kw.lower() in draft_lower)
        keyword_hit_rate = hits / len(expected_keywords)
    else:
        keyword_hit_rate = 1.0

    # Mode match
    expected_mode = case.get("expected_mode", "work")
    mode_match = detected_mode == expected_mode

    # Brevity check
    max_words = case.get("max_words", 100)
    brevity_pass = word_count <= max_words

    # Language detection check
    expected_language = case.get("expected_language")
    language_match = True
    if expected_language and detected_language:
        language_match = detected_language == expected_language

    # Overall pass/warn/fail — max_words violation is now a fail condition
    if not brevity_pass:
        status = "fail"
    elif keyword_hit_rate >= 0.5 and mode_match and language_match:
        status = "pass"
    elif keyword_hit_rate >= 0.25 or mode_match:
        status = "warn"
    else:
        status = "fail"

    result = {
        "case_id": case["id"],
        "description": case.get("description", ""),
        "keyword_hit_rate": round(keyword_hit_rate, 2),
        "mode_match": mode_match,
        "detected_mode": detected_mode,
        "expected_mode": expected_mode,
        "word_count": word_count,
        "max_words": max_words,
        "brevity_pass": brevity_pass,
        "status": status,
    }
    if expected_language:
        result["expected_language"] = expected_language
        result["detected_language"] = detected_language
        result["language_match"] = language_match
    return result


def run_golden_eval(
    *,
    generate_fn=None,
    database_url: str | None = None,
    configs_dir: Path | None = None,
    golden_path: Path | None = None,
) -> dict[str, Any]:
    """Run the full golden evaluation suite.

    If generate_fn is None, returns empty results (for testing without model).
    """
    cases = load_golden_cases(golden_path)
    results: list[dict[str, Any]] = []

    for case in cases:
        if generate_fn is not None:
            output = generate_fn(
                case["inbound"],
                database_url=database_url,
                configs_dir=configs_dir,
            )
            draft = output.get("draft", "")
            detected_mode = output.get("detected_mode", "unknown")
            detected_language = output.get("detected_language")
        else:
            draft = ""
            detected_mode = "unknown"
            detected_language = None

        result = score_case(case, draft, detected_mode, detected_language)
        results.append(result)

    total = len(results)
    passed = sum(1 for r in results if r["status"] == "pass")
    warned = sum(1 for r in results if r["status"] == "warn")
    failed = sum(1 for r in results if r["status"] == "fail")

    summary = {
        "total": total,
        "passed": passed,
        "warned": warned,
        "failed": failed,
        "results": results,
    }

    return summary


def save_results(summary: dict[str, Any], path: Path | None = None) -> None:
    """Save golden results to JSON."""
    p = path or RESULTS_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)


def format_scorecard(summary: dict[str, Any]) -> str:
    """Format golden benchmark results as a scorecard."""
    lines: list[str] = []
    lines.append("Golden Benchmark Results")
    lines.append("=" * 60)

    for r in summary["results"]:
        icon = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}.get(r["status"], "?")
        kw_pct = int(r["keyword_hit_rate"] * 100)
        lines.append(f"  {r['case_id']:<30} {icon:<5} | kw={kw_pct}% mode={'Y' if r['mode_match'] else 'N'} words={r['word_count']}/{r['max_words']}")

    lines.append("=" * 60)
    lines.append(f"  Total: {summary['total']} | Pass: {summary['passed']} | Warn: {summary['warned']} | Fail: {summary['failed']}")
    return "\n".join(lines)


def main() -> None:
    from app.core.settings import get_settings
    from app.db.bootstrap import resolve_sqlite_path

    parser = argparse.ArgumentParser(description="Run golden benchmark evaluation")
    parser.add_argument("--golden", type=Path, default=GOLDEN_PATH, help="Path to golden.yaml")
    parser.add_argument("--summary-only", action="store_true", help="Print scorecard without saving")
    parser.add_argument("--db-path", type=Path, default=resolve_sqlite_path(get_settings().database_url))
    args = parser.parse_args()

    from app.generation.service import DraftRequest, generate_draft

    database_url = f"sqlite:///{args.db_path}"
    configs_dir = ROOT_DIR / "configs"

    def _generate(prompt_text, *, database_url, configs_dir):
        response = generate_draft(
            DraftRequest(inbound_message=prompt_text),
            database_url=database_url,
            configs_dir=configs_dir,
        )
        return {
            "draft": response.draft,
            "detected_mode": response.detected_mode,
            "confidence": response.confidence,
        }

    summary = run_golden_eval(
        generate_fn=_generate,
        database_url=database_url,
        configs_dir=configs_dir,
        golden_path=args.golden,
    )

    print(format_scorecard(summary))

    if not args.summary_only:
        save_results(summary)
        print(f"\nResults saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
