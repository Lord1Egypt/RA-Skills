#!/usr/bin/env python3
"""Render one non-authoritative operator view from safe-update artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from openclaw_safe_update import RehearsalError, parse_status


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RehearsalError(f"cannot read {path.name}") from exc


def link(label: str, target: str) -> str:
    return f"[{label}]({target})"


def render(
    artifact_dir: Path,
    repository_url: str,
    run_url: str | None,
    shadow_runs_index: Path | None = None,
) -> str:
    status = parse_status(read_json(artifact_dir / "verdict.json"))
    decision = status["decision_content"]
    gate_decision = decision["gate_decision"]
    target_root = status["candidate_roots"]["target"] or "unavailable"
    lines = [
        "# OpenClaw safe-update operator view",
        "",
        f"- **Canonical status:** `{status['verdict']}`",
        f"- **Phase:** `{status['phase']}`",
        f"- **Target candidate root:** `{target_root}`",
        f"- **Deterministic gate handling:** `{gate_decision['handling']}`",
        f"- **Post-activation E2E:** `{status['post_activation_e2e']}`",
        "- **Production apply allowed:** `false`",
        "- **Operator approval:** `false`",
        "",
        "## Baseline evidence",
        "",
    ]
    for evidence_id, evidence_status in sorted(
        decision["evidence_status"].items()
    ):
        lines.append(f"- `{evidence_id}`: `{evidence_status}`")

    lines.extend(["", "## Required deterministic gates", ""])
    required_gates = gate_decision["required_gates"]
    if required_gates:
        lines.extend(f"- `{gate_id}`" for gate_id in required_gates)
    else:
        lines.append("- None")

    shadow_path = artifact_dir / "impact-shadow.json"
    lines.extend(["", "## Shadow observations (non-authoritative)", ""])
    if shadow_path.is_file():
        try:
            shadow = read_json(shadow_path)
            if (
                not isinstance(shadow, dict)
                or shadow.get("schema")
                != "openclaw.safe_update.impact_shadow.v1"
            ):
                raise RehearsalError("impact shadow schema is invalid")
            collection_fields = (
                "would_add_checks",
                "would_flag_risks",
                "unmapped_members",
                "unmapped_packages",
            )
            if any(
                not isinstance(shadow.get(field), list)
                for field in collection_fields
            ):
                raise RehearsalError("impact shadow collections are invalid")
            risk_ids = [
                item.get("id")
                for item in shadow["would_flag_risks"]
                if isinstance(item, dict) and isinstance(item.get("id"), str)
            ]
            lines.extend(
                [
                    f"- Status: `{shadow.get('status', 'invalid')}`",
                    f"- Would block: `{str(bool(shadow.get('would_block'))).lower()}`",
                    f"- Suggested checks: `{len(shadow['would_add_checks'])}`",
                    f"- Risk observations: `{len(risk_ids)}`",
                    f"- Unmapped members: `{len(shadow['unmapped_members'])}`",
                    f"- Unmapped packages: `{len(shadow['unmapped_packages'])}`",
                ]
            )
            lines.extend(f"- Risk: `{risk_id}`" for risk_id in sorted(risk_ids))
        except RehearsalError:
            lines.append("- `invalid`; canonical status is unchanged")
    else:
        lines.append("- `not_available`; canonical status is unchanged")

    evidence_files = (
        "installation-candidate-lock.json",
        "installation-contract.json",
        "installation-attestation.json",
        "conservative-gates.json",
        "analysis-cache.json",
        "impact-shadow.json",
        "post-upgrade-e2e.json",
        "evidence-bundle.json",
        "verdict.json",
    )
    lines.extend(["", "## Evidence", ""])
    for name in evidence_files:
        availability = "available" if (artifact_dir / name).is_file() else "not_available"
        lines.append(f"- `{name}`: `{availability}`")
    if run_url:
        lines.append(f"- {link('Workflow run and uploaded artifact', run_url)}")

    repo = repository_url.rstrip("/")
    lines.extend(["", "## v1.3 progress", ""])
    if shadow_runs_index and shadow_runs_index.is_file():
        index = read_json(shadow_runs_index)
        if (
            isinstance(index, dict)
            and index.get("schema")
            == "openclaw.safe_update.shadow_runs_index.v1"
            and isinstance(index.get("completion"), dict)
        ):
            completion = index["completion"]
            lines.extend(
                [
                    f"- Exit decision: `{index.get('decision', 'invalid')}`",
                    f"- Fixture threshold: `{completion.get('fixtures_percent', 0)}%`",
                    f"- Field rehearsal threshold: `{completion.get('field_rehearsals_percent', 0)}%`",
                    f"- Candidate-root threshold: `{completion.get('candidate_roots_percent', 0)}%`",
                    f"- Selective omission enabled: `{str(bool(index.get('selective_omission_enabled'))).lower()}`",
                ]
            )
        else:
            lines.append("- Shadow-runs index: `invalid`; canonical status is unchanged")
    else:
        lines.append("- Shadow-runs index: `not_available`")
    lines.extend(
        [
            f"- {link('RFC and epic #7', repo + '/issues/7')}",
            f"- {link('v1.3 issue progress', repo + '/issues?q=is%3Aissue+label%3Av1.3')}",
            f"- {link('Pull request progress', repo + '/pulls?q=is%3Apr')}",
            "",
            "> This is a human-readable view. `verdict.json` is the only status authority.",
            "> Preflight does not prove live channels, MCPs, memory, migration, rollback, or post-activation behavior.",
            "",
        ]
    )
    return "\n".join(lines)


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--artifact-dir", type=Path, required=True)
    result.add_argument("--repository-url", required=True)
    result.add_argument("--run-url")
    result.add_argument("--shadow-runs-index", type=Path)
    result.add_argument("--output", type=Path)
    return result


def main() -> int:
    args = parser().parse_args()
    try:
        output = render(
            args.artifact_dir.resolve(),
            args.repository_url,
            args.run_url,
            args.shadow_runs_index.resolve() if args.shadow_runs_index else None,
        )
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(output, encoding="utf-8")
        else:
            print(output)
        return 0
    except RehearsalError as exc:
        print(f"blocked: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
