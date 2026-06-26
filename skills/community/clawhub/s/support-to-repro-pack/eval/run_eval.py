"""Evaluation framework — run test cases and score pipeline outputs."""

from __future__ import annotations

import json
import os

from .comparators import compare_facts, compare_redaction, check_completeness
from .scoring import Score, CaseScore, EvalResult
from .report import generate_markdown_report, generate_json_report


def run_eval(
    examples_dir: str,
    pipeline_fn=None,
) -> EvalResult:
    """Run evaluation across all test cases in examples_dir.

    Args:
        examples_dir: Directory containing case_easy/, case_medium/, case_hard/.
        pipeline_fn: Optional pipeline function override. Defaults to run_pipeline.

    Returns:
        EvalResult with per-case and aggregate scores.
    """
    if pipeline_fn is None:
        from repro_pack.pipeline import run_pipeline
        pipeline_fn = run_pipeline

    import tempfile

    cases = sorted([
        d for d in os.listdir(examples_dir)
        if os.path.isdir(os.path.join(examples_dir, d)) and d.startswith("case_")
    ])

    case_scores: list[CaseScore] = []

    for case_name in cases:
        case_dir = os.path.join(examples_dir, case_name)
        ticket_path = os.path.join(case_dir, "input_ticket.md")
        log_path = os.path.join(case_dir, "input_logs.txt")
        expected_facts_path = os.path.join(case_dir, "expected_facts.json")

        # Run pipeline
        with tempfile.TemporaryDirectory() as tmpdir:
            pipeline_fn(
                ticket_path=ticket_path if os.path.exists(ticket_path) else None,
                log_paths=[log_path] if os.path.exists(log_path) else [],
                output_dir=tmpdir,
            )

            # Score facts extraction
            facts_score = Score(dimension="facts_extraction", score=0, max_score=5, details="")
            if os.path.exists(expected_facts_path) and os.path.exists(os.path.join(tmpdir, "3_facts.json")):
                with open(expected_facts_path) as f:
                    expected = json.load(f)
                with open(os.path.join(tmpdir, "3_facts.json")) as f:
                    actual = json.load(f)
                facts_score = compare_facts(expected, actual)

            # Score redaction
            redaction_score = Score(dimension="redaction_recall", score=0, max_score=5, details="")
            sanitized_ticket_path = os.path.join(tmpdir, "1_sanitized_ticket.md")
            if os.path.exists(sanitized_ticket_path) and os.path.exists(ticket_path):
                with open(ticket_path) as f:
                    original = f.read()
                with open(sanitized_ticket_path) as f:
                    sanitized = f.read()
                with open(os.path.join(tmpdir, "8_redaction_report.json")) as f:
                    report = json.load(f)
                redaction_score = compare_redaction(original, sanitized, report)

            # Score output completeness
            completeness_score = check_completeness(tmpdir)

            case_scores.append(CaseScore(
                case_name=case_name,
                scores=[facts_score, redaction_score, completeness_score],
            ))

    return EvalResult(cases=case_scores)


def main() -> None:
    """CLI entry point for evaluation."""
    import sys

    examples_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples"
    )

    result = run_eval(examples_dir)

    # Print markdown report
    md = generate_markdown_report(result)
    print(md)

    # Also save JSON
    report_path = os.path.join(examples_dir, "..", "eval_report.json")
    with open(report_path, "w") as f:
        f.write(generate_json_report(result))
    print(f"\nJSON report saved to: {report_path}")


if __name__ == "__main__":
    main()
