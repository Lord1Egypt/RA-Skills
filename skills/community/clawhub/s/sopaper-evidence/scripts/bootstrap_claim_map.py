#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


CLAIM_LINE_RE = re.compile(r"^\s*-\s+(.*\S)\s*$")
FIELD_RE = re.compile(r"^\s{2}([a-zA-Z0-9_]+):\s*(.*)\s*$")
ID_RE = re.compile(r"^\s*-\s+id:\s*(\S+)\s*$")


@dataclass
class EvidenceEntry:
    evidence_id: str
    statement: str
    classification: str
    source_title: str
    source_type: str


@dataclass
class MatchCandidate:
    entry: EvidenceEntry
    score: int
    basis: str


@dataclass
class ClaimEntry:
    text: str
    claim_type: str
    current_status: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a first-pass claim-to-evidence map from a claims list and an evidence ledger draft. "
            "This script uses simple token overlap to suggest candidate evidence items."
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
    output = render_claim_map(claims, evidence)

    if args.output:
        output_path = Path(args.output).expanduser().resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
    else:
        sys.stdout.write(output)

    return 0


def parse_claims(text: str) -> list[ClaimEntry]:
    structured_claims: list[ClaimEntry] = []
    current_text = ""
    current_type = ""
    current_status = ""

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("- Claim:"):
            if current_text:
                structured_claims.append(
                    ClaimEntry(
                        text=current_text,
                        claim_type=current_type or "unspecified",
                        current_status=current_status or "unknown",
                    )
                )
            current_text = stripped.split(":", 1)[1].strip()
            current_type = ""
            current_status = ""
            continue

        if current_text and stripped.startswith("Claim type:"):
            current_type = stripped.split(":", 1)[1].strip()
            continue

        if current_text and stripped.startswith("Current status:"):
            current_status = stripped.split(":", 1)[1].strip()
            continue

    if current_text:
        structured_claims.append(
            ClaimEntry(
                text=current_text,
                claim_type=current_type or "unspecified",
                current_status=current_status or "unknown",
            )
        )

    if structured_claims:
        return structured_claims

    claims: list[ClaimEntry] = []
    for line in text.splitlines():
        match = CLAIM_LINE_RE.match(line)
        if match:
            claims.append(
                ClaimEntry(
                    text=match.group(1).strip(),
                    claim_type="unspecified",
                    current_status="unknown",
                )
            )
    return claims


def parse_ledger(text: str) -> list[EvidenceEntry]:
    entries: list[EvidenceEntry] = []
    current_id = ""
    current_statement = ""
    current_classification = "unverified"
    current_source_title = ""
    current_source_type = "other"

    for line in text.splitlines():
        id_match = ID_RE.match(line)
        if id_match:
            if current_id:
                entries.append(
                    EvidenceEntry(
                        evidence_id=current_id,
                        statement=current_statement,
                        classification=current_classification,
                        source_title=current_source_title,
                        source_type=current_source_type,
                    )
                )
            current_id = id_match.group(1)
            current_statement = ""
            current_classification = "unverified"
            current_source_title = ""
            current_source_type = "other"
            continue

        field_match = FIELD_RE.match(line)
        if field_match:
            field, value = field_match.groups()
            value = strip_quotes(value.strip())
            if field == "statement":
                current_statement = value
            elif field == "classification":
                current_classification = value
            elif field == "source_title":
                current_source_title = value
            elif field == "source_type":
                current_source_type = value

    if current_id:
        entries.append(
            EvidenceEntry(
                evidence_id=current_id,
                statement=current_statement,
                classification=current_classification,
                source_title=current_source_title,
                source_type=current_source_type,
            )
        )

    return entries


def render_claim_map(claims: list[ClaimEntry], evidence: list[EvidenceEntry]) -> str:
    lines = [
        "# Claim-to-Evidence Map Draft",
        "",
        "This draft was generated automatically. Review every suggested match before using it in downstream research work.",
        "",
        "## Major claims",
        "",
        "| Claim ID | Claim | Status | Evidence IDs | Notes |",
        "| --- | --- | --- | --- | --- |",
    ]

    for index, claim in enumerate(claims, start=1):
        matches = match_evidence_for_claim(claim, evidence)
        evidence_ids = ", ".join(item.entry.evidence_id for item in matches[:3])
        status = suggest_status(claim, matches)
        notes = suggest_note(claim, matches)
        lines.append(f"| C{index} | {escape_pipes(claim.text)} | {status} | {evidence_ids} | {escape_pipes(notes)} |")

    lines.extend(
        [
            "",
            "## Evidence notes",
            "",
            "| Evidence ID | Classification | Statement |",
            "| --- | --- | --- |",
        ]
    )

    for entry in evidence:
        statement = entry.statement or "TODO: fill exact statement."
        lines.append(
            f"| {entry.evidence_id} | {entry.classification} | {escape_pipes(statement)} |"
        )

    return "\n".join(lines) + "\n"


def match_evidence_for_claim(claim: ClaimEntry, evidence: list[EvidenceEntry]) -> list[MatchCandidate]:
    claim_tokens = tokenize(claim.text)
    claim_type_tokens = tokenize(claim.claim_type)
    scored: list[MatchCandidate] = []
    comparative = is_comparative_claim(claim)
    preferred_types = preferred_source_types(claim)

    for entry in evidence:
        if not is_placeholder_statement(entry.statement):
            statement_tokens = tokenize(entry.statement)
            overlap = len(claim_tokens & statement_tokens)
            if overlap > 0:
                type_boost = len(claim_type_tokens & statement_tokens)
                score = overlap * 10 + type_boost * 3 + classification_weight(entry.classification)
                score += statement_kind_boost(claim, entry.statement)
                if entry.source_type in preferred_types:
                    score += 4
                if comparative and entry.classification == "project_evidence":
                    score += 12
                if comparative and is_direct_result_statement(entry.statement):
                    score += 18
                if comparative and entry.source_title.lower() == "aggregated result artifacts":
                    score += 8
                scored.append(MatchCandidate(entry=entry, score=score, basis="statement"))
                continue

        title_tokens = tokenize(entry.source_title)
        title_overlap = len(claim_tokens & title_tokens)
        minimum_overlap = 2 if comparative else 1
        if title_overlap >= minimum_overlap:
            type_boost = len(claim_type_tokens & title_tokens)
            score = title_overlap + type_boost
            if entry.source_type in preferred_types:
                score += 2
            scored.append(MatchCandidate(entry=entry, score=score, basis="title"))

    scored.sort(key=lambda item: (-item.score, item.entry.evidence_id))
    return scored


def suggest_status(claim: ClaimEntry, matches: list[MatchCandidate]) -> str:
    if not matches:
        return "unsupported"
    if is_comparative_claim(claim):
        has_direct_result = any(
            match.basis == "statement"
            and match.entry.classification == "project_evidence"
            and is_direct_result_statement(match.entry.statement)
            for match in matches
        )
        has_baseline_context = any(
            match.basis == "statement"
            and has_baseline_signal(match.entry.statement)
            for match in matches
        )
        if has_direct_result and has_baseline_context:
            return "supported"
        if any(match.basis == "statement" and match.entry.classification in {"project_evidence", "verified_fact"} for match in matches):
            return "partial"
        return "unsupported"
    if any(
        match.basis == "statement"
        and match.entry.classification == "verified_fact"
        and not is_page_metadata_statement(match.entry.statement)
        for match in matches
    ):
        return "supported"
    if any(match.basis == "statement" and match.entry.classification == "verified_fact" for match in matches):
        return "partial"
    if any(match.basis == "statement" and match.entry.classification == "project_evidence" for match in matches):
        return "partial"
    if claim.current_status == "blocked":
        return "unsupported"
    return "unsupported"


def suggest_note(claim: ClaimEntry, matches: list[MatchCandidate]) -> str:
    if not matches:
        return "No matching evidence found. Review the claim wording or add supporting sources."
    if is_comparative_claim(claim):
        if suggest_status(claim, matches) == "supported":
            return "Direct result evidence and baseline context exist, but external source review is still needed before stronger paper claims."
        return "Potential leads exist, but comparative-result claims still require reviewed result evidence and a fair baseline set."
    if all(match.basis == "title" for match in matches[:3]):
        return "Potential title-level leads exist, but no reviewed evidence statement supports this claim yet."
    if all(match.entry.classification == "unverified" for match in matches[:3]):
        return "Potential matches exist, but all suggested evidence is still unverified."
    if any(is_page_metadata_statement(match.entry.statement) for match in matches[:3]):
        return "Verified page-level facts exist, but reviewed source statements are still needed for stronger support."
    return "Review suggested evidence ids and tighten the claim wording if support is weak."


def is_comparative_claim(claim: ClaimEntry) -> bool:
    lowered = f"{claim.claim_type} {claim.text}".lower()
    return any(token in lowered for token in ["comparative", "improves", "outperforms", "better than", "strong baselines"])


def preferred_source_types(claim: ClaimEntry) -> set[str]:
    lowered = f"{claim.claim_type} {claim.text}".lower()
    if any(token in lowered for token in ["benchmark", "position", "positioning", "dataset"]):
        return {"benchmark", "dataset", "paper", "official_doc"}
    if any(token in lowered for token in ["result", "improves", "outperforms", "baseline"]):
        return {"local_result", "paper", "benchmark"}
    return {"paper", "benchmark", "official_doc", "local_result"}


def classification_weight(classification: str) -> int:
    if classification == "verified_fact":
        return 8
    if classification == "project_evidence":
        return 5
    if classification == "inference":
        return 2
    return 0


def statement_kind_boost(claim: ClaimEntry, statement: str) -> int:
    lowered_claim = f"{claim.claim_type} {claim.text}".lower()
    lowered_statement = statement.lower()
    if "position" in lowered_claim and "candidate benchmark/task fact:" in lowered_statement:
        return 6
    if any(token in lowered_claim for token in ["evaluation", "baseline", "metric", "provenance"]) and (
        "candidate evaluation fact:" in lowered_statement or "candidate metric fact:" in lowered_statement
    ):
        return 8
    if "comparative" in lowered_claim and "candidate metric fact:" in lowered_statement:
        return 3
    if "comparative" in lowered_claim and is_direct_result_statement(statement):
        return 12
    if "comparative" in lowered_claim and has_baseline_signal(statement):
        return 8
    return 0


def is_page_metadata_statement(statement: str) -> bool:
    lowered = statement.lower()
    return lowered.startswith("fetched page title:") or lowered.startswith("meta description:")


def is_direct_result_statement(statement: str) -> bool:
    lowered = statement.lower()
    return "internal result artifact tracks" in lowered or "direct result evidence" in lowered


def has_baseline_signal(statement: str) -> bool:
    lowered = statement.lower()
    return "candidate baseline fact:" in lowered or " against " in lowered or "baseline" in lowered


def tokenize(value: str) -> set[str]:
    stopwords = {
        "the",
        "and",
        "for",
        "that",
        "this",
        "from",
        "with",
        "into",
        "claim",
        "observation",
        "summarize",
        "exact",
        "todo",
        "source",
        "example",
        "repository",
        "listing",
        "internal",
        "current",
        "using",
    }
    return {
        token
        for token in re.findall(r"[a-zA-Z0-9]+", value.lower())
        if len(token) > 2 and token not in stopwords
    }


def is_placeholder_statement(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered.startswith("todo:")


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1]
    return value


def escape_pipes(value: str) -> str:
    return value.replace("|", "\\|")


if __name__ == "__main__":
    raise SystemExit(main())
