#!/usr/bin/env python3
"""
claims-validator.py — validate claims/verifications/decisions integrity for a deliberation run.

Usage:
    python claims-validator.py [--state-dir state/]

Returns exit code 0 if all checks pass, 1 if any check fails. Prints findings to stderr.

Checks performed:
1. Every claim_id referenced in verifications exists in claims.jsonl
2. Every evidence_ref in verifications points to a real file
3. Every claim with status `tested_*` has at least one verification linking to it
4. No claim is in status `superseded` without a later claim citing it as `supersedes`
5. Every decision has at least 1 citation
6. Every claim has a `testable_as` field
7. Every verification has evidence_refs >= 2 (unless NOT_APPLICABLE)
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set


def load_jsonl(path: Path) -> List[Dict]:
    """Load JSONL file, return list of dicts. Tolerate empty lines."""
    entries = []
    if not path.exists():
        return entries
    with path.open('r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"ERROR {path}:{line_num} — invalid JSON: {e}", file=sys.stderr)
    return entries


def validate(state_dir: Path) -> List[str]:
    """Run all validation checks, return list of error messages."""
    errors = []

    claims = load_jsonl(state_dir / "claims.jsonl")
    verifications = load_jsonl(state_dir / "verifications.jsonl")
    decisions = load_jsonl(state_dir / "decisions.jsonl")

    claim_ids: Set[str] = {c.get("id") for c in claims if c.get("id")}
    repo_root = state_dir.parent

    # Check 1: claim_ids in verifications exist
    for v in verifications:
        vid = v.get("id", "<unknown>")
        for cid in v.get("claims_affected", []):
            if cid not in claim_ids:
                errors.append(f"verification {vid} references unknown claim {cid}")
        for change in v.get("claim_status_changes", []):
            cid = change.get("claim_id")
            if cid and cid not in claim_ids:
                errors.append(f"verification {vid} status_change for unknown claim {cid}")

    # Check 2 + 7: evidence_refs valid and ≥2
    for v in verifications:
        vid = v.get("id", "<unknown>")
        if v.get("result") == "NOT_APPLICABLE":
            continue  # NOT_APPLICABLE allowed to have 0 evidence_refs

        refs = v.get("evidence_refs", [])
        if len(refs) < 2:
            errors.append(f"verification {vid} has only {len(refs)} evidence_refs (need ≥2)")

        for ref in refs:
            # ref format: "artifacts/round_N/role.md#section" or "state/decisions.jsonl#L5"
            file_part = ref.split("#")[0]
            full_path = repo_root / file_part
            if not full_path.exists():
                errors.append(f"verification {vid} evidence_ref points to missing file: {file_part}")

    # Check 3: claims with tested_* status have linking verifications
    tested_claims = {
        c["id"] for c in claims
        if c.get("status", "").startswith("tested_")
        or c.get("status") == "partially_refuted"
    }
    verified_claim_ids: Set[str] = set()
    for v in verifications:
        verified_claim_ids.update(v.get("claims_affected", []))

    for cid in tested_claims:
        if cid not in verified_claim_ids:
            errors.append(f"claim {cid} has tested status but no verification links to it")

    # Check 4: superseded claims have a later claim with supersedes link
    superseded = {c["id"] for c in claims if c.get("status") == "superseded"}
    superseding_targets: Set[str] = {c.get("supersedes") for c in claims if c.get("supersedes")}

    for cid in superseded:
        if cid not in superseding_targets:
            errors.append(f"claim {cid} is marked superseded but no later claim supersedes it")

    # Check 5: decisions have at least 1 citation
    for d in decisions:
        did = d.get("id", "<unknown>")
        if not d.get("cites"):
            errors.append(f"decision {did} has no citations")

    # Check 6: claims have testable_as
    for c in claims:
        cid = c.get("id", "<unknown>")
        if not c.get("testable_as"):
            errors.append(f"claim {cid} missing testable_as field")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate claims/verifications/decisions integrity.")
    parser.add_argument("--state-dir", default="state", help="Path to state directory (default: state/)")
    args = parser.parse_args()

    state_dir = Path(args.state_dir).resolve()
    if not state_dir.is_dir():
        print(f"ERROR: state directory not found: {state_dir}", file=sys.stderr)
        sys.exit(1)

    errors = validate(state_dir)

    if errors:
        print(f"VALIDATION FAILED: {len(errors)} errors found", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)

    print("VALIDATION PASSED: all checks succeeded")
    sys.exit(0)


if __name__ == "__main__":
    main()
