#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ID_RE = re.compile(r"^\s*-\s+id:\s*(\S+)\s*$")
FIELD_RE = re.compile(r"^\s{2}([a-zA-Z0-9_]+):\s*(.*)\s*$")
CLAIM_LINE_RE = re.compile(r"^\s*-\s+(.*\S)\s*$")

DOMAIN_KEYWORDS = {
    "long horizon",
    "manipulation",
    "robot",
    "robotics",
    "browser",
    "browsing",
    "web",
    "retrieval",
    "citation",
    "code",
    "qa",
}


@dataclass
class EvidenceEntry:
    evidence_id: str
    statement: str
    classification: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a fairness review draft for comparative research claims."
    )
    parser.add_argument("claims", help="Markdown file containing claims.")
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
    output = render_fairness_report(claims, evidence)

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
                entries.append(EvidenceEntry(current_id, current_statement, current_classification))
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
        entries.append(EvidenceEntry(current_id, current_statement, current_classification))
    return entries


def render_fairness_report(claims: list[str], evidence: list[EvidenceEntry]) -> str:
    project_entries = [entry for entry in evidence if entry.classification == "project_evidence"]
    verified_entries = [entry for entry in evidence if entry.classification == "verified_fact"]
    comparative_claims = [
        claim
        for claim in claims
        if any(token in claim.lower() for token in ["comparative", "improves", "outperforms", "baseline"])
    ]

    checks = build_checks(project_entries, verified_entries, comparative_claims)

    lines = [
        "# Comparison Fairness Review Draft",
        "",
        "This draft estimates whether comparative claims look fair enough to keep. Review every item before using it in paper text.",
        "",
        "## Comparative claims under review",
        "",
    ]
    if comparative_claims:
        for claim in comparative_claims:
            lines.append(f"- {claim}")
    else:
        lines.append("- No explicit comparative claim detected.")

    lines.extend(
        [
            "",
            "## Fairness checks",
            "",
            "| Check | Status | Why it matters | Current signal | Next action |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for check in checks:
        lines.append(
            f"| {escape_pipes(check['name'])} | {check['status']} | {escape_pipes(check['why'])} | {escape_pipes(check['signal'])} | {escape_pipes(check['next'])} |"
        )

    return "\n".join(lines) + "\n"


def build_checks(project_entries: list[EvidenceEntry], verified_entries: list[EvidenceEntry], comparative_claims: list[str]) -> list[dict[str, str]]:
    project_text = " ".join(entry.statement.lower() for entry in project_entries)
    verified_text = " ".join(entry.statement.lower() for entry in verified_entries)
    baselines = extract_baselines(project_entries)
    project_metrics = extract_metrics(project_entries)
    verified_metrics = extract_metrics(verified_entries)
    scope_overlap = extract_scope_terms(project_text) & extract_scope_terms(verified_text)

    checks: list[dict[str, str]] = []

    checks.append(
        {
            "name": "Direct result evidence",
            "status": status_label(bool(project_entries), severe=True),
            "why": "Comparative claims need project-native evidence, not just external benchmark descriptions.",
            "signal": f"{len(project_entries)} project_evidence entries found." if project_entries else "No project_evidence entry found.",
            "next": "Import at least one reviewed result artifact before keeping comparative wording." if not project_entries else "Keep the strongest direct result artifact near the final comparison claim.",
        }
    )

    checks.append(
        {
            "name": "Baseline breadth",
            "status": "pass" if len(baselines) >= 2 else "warn" if len(baselines) == 1 else "fail",
            "why": "A comparative claim should usually rest on more than one task-aligned baseline.",
            "signal": f"Baselines found: {', '.join(baselines)}" if baselines else "No explicit baseline names detected in project evidence.",
            "next": "Add at least one more benchmark-aligned baseline or narrow the claim." if len(baselines) < 2 else "Check whether each baseline is truly task- and embodiment-aligned.",
        }
    )

    metric_union = sorted({*project_metrics, *verified_metrics})
    checks.append(
        {
            "name": "Metric grounding",
            "status": "pass" if project_metrics and verified_metrics else "warn" if project_metrics or verified_metrics else "fail",
            "why": "The comparison should name a metric in project results and anchor that metric in benchmark or paper evidence.",
            "signal": f"Project metrics: {', '.join(project_metrics) or 'none'}; verified-source metrics: {', '.join(verified_metrics) or 'none'}",
            "next": "Add reviewed metric definitions from primary benchmark or paper sources." if not (project_metrics and verified_metrics) else "Confirm that the project and benchmark use the same metric definition.",
        }
    )

    checks.append(
        {
            "name": "Scope alignment",
            "status": "pass" if scope_overlap else "warn",
            "why": "Results and benchmark references should point to the same task family or evaluation scope.",
            "signal": f"Shared scope terms: {', '.join(sorted(scope_overlap))}" if scope_overlap else "No clear shared scope terms between project and verified external evidence.",
            "next": "Narrow the claim or add explicit benchmark/task definitions that match the result artifact scope." if not scope_overlap else "Manually verify that scope overlap is real, not only lexical.",
        }
    )

    verified_baseline_signal = "candidate baseline fact:" in verified_text or "baseline" in verified_text
    checks.append(
        {
            "name": "External fairness anchor",
            "status": "pass" if verified_baseline_signal else "warn",
            "why": "Benchmark or paper sources should explicitly indicate what counts as a fair baseline comparison.",
            "signal": "Verified external evidence includes baseline expectations." if verified_baseline_signal else "No explicit external fairness anchor detected.",
            "next": "Add or review benchmark notes that state baseline expectations." if not verified_baseline_signal else "Cross-check the chosen baselines against the benchmark baseline checklist.",
        }
    )

    if not comparative_claims:
        for check in checks:
            if check["status"] == "fail":
                check["status"] = "warn"
                check["next"] = "Only relevant if comparative wording is introduced later."

    return checks


def extract_baselines(entries: list[EvidenceEntry]) -> list[str]:
    found: list[str] = []
    seen: set[str] = set()
    marker = "candidate baseline fact:"
    for entry in entries:
        lowered = entry.statement.lower()
        if marker not in lowered:
            continue
        tail = entry.statement.lower().split(marker, 1)[1]
        if "against" in tail:
            tail = tail.split("against", 1)[1]
        for part in [piece.strip(" .") for piece in tail.split(",") if piece.strip()]:
            normalized = part.replace("_", " ").replace("-", " ").strip()
            if normalized and normalized not in seen:
                seen.add(normalized)
                found.append(normalized)
    return found


def extract_metrics(entries: list[EvidenceEntry]) -> list[str]:
    metrics: list[str] = []
    seen: set[str] = set()
    for entry in entries:
        lowered = entry.statement.lower()
        if "candidate metric fact:" in lowered:
            tail = entry.statement.lower().split("candidate metric fact:", 1)[1]
            for token in ["success rate", "accuracy", "precision", "recall", "f1", "pass@k", "score"]:
                if token in tail and token not in seen:
                    seen.add(token)
                    metrics.append(token)
        else:
            for token in ["success rate", "accuracy", "precision", "recall", "f1", "pass@k", "score"]:
                if token in lowered and token not in seen:
                    seen.add(token)
                    metrics.append(token)
    return metrics


def extract_scope_terms(text: str) -> set[str]:
    return {term for term in DOMAIN_KEYWORDS if term in text}


def status_label(ok: bool, *, severe: bool = False) -> str:
    if ok:
        return "pass"
    return "fail" if severe else "warn"


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def escape_pipes(value: str) -> str:
    return value.replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
