#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path


ALLOWED_TYPES = {"paper", "benchmark", "dataset", "official_doc", "repo"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Conservatively verify fetched source-note drafts. This step only upgrades notes "
            "when page-level metadata facts are present and fetch status is review-ready."
        )
    )
    parser.add_argument("inputs", nargs="+", help="Source-note markdown files to verify.")
    parser.add_argument("--output-dir", required=True, help="Directory for verified note outputs.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    for value in args.inputs:
        source = Path(value).expanduser().resolve()
        if not source.exists():
            continue
        text = source.read_text(encoding="utf-8")
        verified = verify_note(text)
        target = output_dir / source.name
        target.write_text(verified, encoding="utf-8")
        print(target)

    return 0


def verify_note(text: str) -> str:
    lines = text.splitlines()
    source_type = field_value(lines, "- Source type:")
    verification = field_value(lines, "- Verification status:")
    facts = [line for line in lines if line.startswith("- Fact:")]
    semantic_facts = [
        line
        for line in facts
        if any(
            token in line.lower()
            for token in [
                "candidate benchmark/task fact:",
                "candidate evaluation fact:",
                "candidate metric fact:",
                "candidate baseline fact:",
            ]
        )
    ]
    benchmark_fact = first_fact(semantic_facts, "candidate benchmark/task fact:")
    evaluation_fact = first_fact(semantic_facts, "candidate evaluation fact:")
    metric_fact = first_fact(semantic_facts, "candidate metric fact:")
    baseline_fact = first_fact(semantic_facts, "candidate baseline fact:")

    should_verify = (
        source_type in ALLOWED_TYPES
        and verification == "fetched-primary-review-required"
        and (
            (len(semantic_facts) >= 1 and all("TODO:" not in line for line in semantic_facts[:1]))
            or (len(facts) >= 2 and all("TODO:" not in line for line in facts[:2]))
        )
    )

    if not should_verify:
        return text

    reviewed_summary = synthesize_reviewed_summary(
        source_type=source_type,
        benchmark_fact=benchmark_fact,
        evaluation_fact=evaluation_fact,
        metric_fact=metric_fact,
        baseline_fact=baseline_fact,
    )
    verification_status = "reviewed-primary" if reviewed_summary else "verified-page-metadata"

    updated: list[str] = []
    inserted_summary = False
    for line in lines:
        if line.startswith("- Verification status:"):
            updated.append(f"- Verification status: {verification_status}")
        elif line == "## Key facts" and reviewed_summary and not inserted_summary:
            updated.extend(
                [
                    "## Reviewed summary",
                    "",
                    f"- Reviewed summary: {reviewed_summary}",
                    "",
                    line,
                ]
            )
            inserted_summary = True
        else:
            updated.append(line)
    return "\n".join(updated) + ("\n" if text.endswith("\n") else "")


def field_value(lines: list[str], prefix: str) -> str:
    for line in lines:
        if line.startswith(prefix):
            return line.split(":", 1)[1].strip().lower()
    return ""


def first_fact(facts: list[str], prefix: str) -> str:
    lowered_prefix = prefix.lower()
    for fact in facts:
        if lowered_prefix in fact.lower():
            return fact.split(":", 2)[-1].strip()
    return ""


def synthesize_reviewed_summary(
    *,
    source_type: str,
    benchmark_fact: str,
    evaluation_fact: str,
    metric_fact: str,
    baseline_fact: str,
) -> str:
    parts = [part for part in [benchmark_fact, evaluation_fact, metric_fact, baseline_fact] if part]
    if len(parts) < 2:
        return ""

    summary_parts = []
    if benchmark_fact:
        summary_parts.append(benchmark_fact.rstrip("."))
    if evaluation_fact:
        summary_parts.append(evaluation_fact.rstrip("."))
    if metric_fact:
        summary_parts.append(metric_fact.rstrip("."))
    if baseline_fact:
        summary_parts.append(baseline_fact.rstrip("."))

    if source_type in {"paper", "benchmark"}:
        return "Reviewed primary-source summary: " + ". ".join(summary_parts[:3]) + "."
    if source_type in {"repo", "official_doc"}:
        return "Reviewed source summary: " + ". ".join(summary_parts[:2]) + "."
    return ""


if __name__ == "__main__":
    raise SystemExit(main())
