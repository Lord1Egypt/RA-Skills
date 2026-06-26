#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


CLAIM_LINE_RE = re.compile(r"^\s*-\s+(.*\S)\s*$")
ID_RE = re.compile(r"^\s*-\s+id:\s*(\S+)\s*$")
FIELD_RE = re.compile(r"^\s{2}([a-zA-Z0-9_]+):\s*(.*)\s*$")


@dataclass
class EvidenceEntry:
    evidence_id: str
    statement: str
    classification: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a first-pass experiment gap report from a claims list and an evidence ledger draft."
        )
    )
    parser.add_argument("claims", help="Markdown file containing bullet-list claims.")
    parser.add_argument("ledger", help="Evidence ledger markdown file.")
    parser.add_argument("-o", "--output", help="Write output to file instead of stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    claims_path = Path(args.claims).expanduser().resolve()
    ledger_path = Path(args.ledger).expanduser().resolve()

    if not claims_path.exists():
        print(f"Missing claims file: {claims_path}", file=sys.stderr)
        return 1
    if not ledger_path.exists():
        print(f"Missing ledger file: {ledger_path}", file=sys.stderr)
        return 1

    claims = parse_claims(claims_path.read_text(encoding="utf-8"))
    evidence = parse_ledger(ledger_path.read_text(encoding="utf-8"))
    output = render_gap_report(claims, evidence)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    return 0


def parse_claims(text: str) -> list[str]:
    structured_claims: list[str] = []
    current_text = ""

    for raw_line in text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("- Claim:"):
            if current_text:
                structured_claims.append(current_text)
            current_text = stripped.split(":", 1)[1].strip()

    if current_text:
        structured_claims.append(current_text)

    if structured_claims:
        return structured_claims

    claims: list[str] = []
    for line in text.splitlines():
        match = CLAIM_LINE_RE.match(line)
        if match:
            claims.append(match.group(1).strip())
    return claims


def parse_ledger(text: str) -> list[EvidenceEntry]:
    entries: list[EvidenceEntry] = []
    current_id = ""
    current_statement = ""
    current_classification = "unverified"

    for line in text.splitlines():
        id_match = ID_RE.match(line)
        if id_match:
            if current_id:
                entries.append(
                    EvidenceEntry(
                        evidence_id=current_id,
                        statement=current_statement,
                        classification=current_classification,
                    )
                )
            current_id = id_match.group(1)
            current_statement = ""
            current_classification = "unverified"
            continue

        field_match = FIELD_RE.match(line)
        if field_match:
            field, value = field_match.groups()
            value = strip_quotes(value.strip())
            if field == "statement":
                current_statement = value
            elif field == "classification":
                current_classification = value

    if current_id:
        entries.append(
            EvidenceEntry(
                evidence_id=current_id,
                statement=current_statement,
                classification=current_classification,
            )
        )

    return entries


def render_gap_report(claims: list[str], evidence: list[EvidenceEntry]) -> str:
    lines = [
        "# Experiment Gap Report Draft",
        "",
        "This draft was generated automatically. Review every suggested gap before using it for paper planning.",
        "",
        "## Current claim set",
        "",
    ]

    for claim in claims:
        lines.append(f"- {claim}")

    lines.extend(
        [
            "",
            "## Gap triage",
            "",
            "| Gap ID | Severity | Category | Blocked claims | Why it matters | What resolves it | Owner | Next step |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )

    gaps = build_gap_rows(claims, evidence)
    for index, gap in enumerate(gaps, start=1):
        lines.append(
            "| {gap_id} | {severity} | {category} | {blocked} | {reason} | {resolve} | {owner} | {next_step} |".format(
                gap_id=f"G{index:02d}",
                severity=gap["severity"],
                category=gap["category"],
                blocked=escape_pipes(gap["blocked_claims"]),
                reason=escape_pipes(gap["why"]),
                resolve=escape_pipes(gap["resolve"]),
                owner=escape_pipes(gap["owner"]),
                next_step=escape_pipes(gap["next_step"]),
            )
        )

    return "\n".join(lines) + "\n"


def build_gap_rows(claims: list[str], evidence: list[EvidenceEntry]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    verified_count = sum(1 for entry in evidence if entry.classification in {"verified_fact", "project_evidence"})
    unverified_count = sum(1 for entry in evidence if entry.classification == "unverified")
    project_evidence_count = sum(1 for entry in evidence if entry.classification == "project_evidence")
    verified_text = " ".join(
        entry.statement.lower() for entry in evidence if entry.classification in {"verified_fact", "project_evidence"}
    )
    comparative_claims = any(
        token in claim.lower() for claim in claims for token in ["comparative", "improves", "outperforms", "baseline"]
    )
    needs_metric_detail = any(
        token in " ".join(claims).lower()
        for token in ["metric", "citation quality", "result provenance", "baseline fairness", "evaluation setup"]
    )
    has_metric_signal = "candidate metric fact:" in verified_text or any(
        token in verified_text for token in ["success rate", "accuracy", "precision", "recall", "f1"]
    )

    if verified_count == 0:
        rows.append(
            {
                "severity": "blocker",
                "category": "result provenance",
                "blocked_claims": "all major claims",
                "why": "There is no verified_fact or project_evidence item in the ledger.",
                "resolve": "Add at least one verified result table, project artifact, or primary source-backed fact.",
                "owner": "project team",
                "next_step": "Promote the strongest source to verified_fact or add project-native evidence.",
            }
        )

    if unverified_count > 0:
        rows.append(
            {
                "severity": "major",
                "category": "source verification",
                "blocked_claims": "claims that depend on external sources",
                "why": "Some evidence entries are still unverified and should not anchor strong paper claims.",
                "resolve": "Check each external source against its primary reference and update classifications.",
                "owner": "paper lead",
                "next_step": "Verify the top-priority external sources used in related work or comparisons.",
            }
        )

    if comparative_claims and project_evidence_count == 0:
        rows.append(
            {
                "severity": "blocker",
                "category": "direct result evidence",
                "blocked_claims": "comparative result claims",
                "why": "Comparative claims exist, but there is no project_evidence item that captures direct internal result evidence.",
                "resolve": "Add a reviewed result artifact with metric, scope, and baseline context before keeping comparative claims.",
                "owner": "experiment owner",
                "next_step": "Create or import a structured result artifact for the strongest comparative result.",
            }
        )

    if comparative_claims and "candidate baseline fact:" not in verified_text:
        rows.append(
            {
                "severity": "blocker",
                "category": "baseline coverage",
                "blocked_claims": "comparative performance claims",
                "why": "Comparative wording appears in the claims set, but the verified evidence does not yet capture explicit baseline expectations.",
                "resolve": "Confirm direct baselines, baseline fairness, and benchmark fit before keeping comparative language.",
                "owner": "experiment owner",
                "next_step": "Review the baseline set against the benchmark-baseline checklist.",
            }
        )

    if needs_metric_detail and not has_metric_signal:
        rows.append(
            {
                "severity": "major",
                "category": "metric definition",
                "blocked_claims": "evaluation framing and comparison claims",
                "why": "The current verified evidence does not yet capture explicit metric definitions or metric-oriented evaluation facts.",
                "resolve": "Add reviewed metric definitions from benchmark pages, papers, or result artifacts.",
                "owner": "paper lead",
                "next_step": "Extract the top metric definitions and add them as reviewed facts before drafting evaluation text.",
            }
        )

    if any(token in " ".join(claims).lower() for token in ["real-world", "real world", "generalization", "long-horizon"]):
        rows.append(
            {
                "severity": "major",
                "category": "evaluation scope",
                "blocked_claims": "generalization or deployment claims",
                "why": "The claims imply scope that may exceed the currently verified evidence.",
                "resolve": "State scope limits clearly or add evaluation evidence that matches the claim breadth.",
                "owner": "paper lead",
                "next_step": "Check whether the claim should be narrowed to the evaluated setting.",
            }
        )

    if not rows:
        rows.append(
            {
                "severity": "minor",
                "category": "review",
                "blocked_claims": "none",
                "why": "No obvious blockers were inferred from the current draft inputs.",
                "resolve": "Manually review benchmark fit, baseline fit, and ablation expectations.",
                "owner": "paper lead",
                "next_step": "Run a manual pass over the claim audit and gap triage references.",
            }
        )

    return rows


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def escape_pipes(value: str) -> str:
    return value.replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
