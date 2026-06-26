from __future__ import annotations

from typing import Sequence, Set, Tuple

from ..common import line_number_for_substring
from ..constants import LAYER_CAPABILITY
from ..finding import add_finding, mark_layer_executed
from ..models import FileRecord, Finding, LayerState


def scan_capability_contract_mismatch(
    records: Sequence[FileRecord],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    mark_layer_executed(layer_state, LAYER_CAPABILITY)

    skill_record: FileRecord | None = None
    for record in records:
        if record["path_obj"].name == "SKILL.md":
            skill_record = record
            break
    if not skill_record:
        return

    skill_text = skill_record["text"].lower()
    skill_lines = skill_record["lines"]
    skill_rel = skill_record["rel_path"]

    has_destructive_behavior = any(
        item.get("category") == "C" and item.get("severity") in {"high", "critical"}
        for item in findings
    )
    has_network_behavior = any(
        "network-egress" in item.get("tags", []) or "suspicious-egress" in item.get("tags", [])
        for item in findings
    )
    has_download_exec = any(
        str(item.get("rule_id", "")).startswith("D_DOWNLOAD")
        or str(item.get("rule_id", "")) in {"E_INSTALL_HOOK_DOWNLOAD_EXEC", "E_WORKFLOW_DOWNLOAD_EXEC"}
        for item in findings
    )

    if "read-only" in skill_text and has_destructive_behavior:
        line_no = line_number_for_substring(skill_lines, "read-only")
        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_CAPABILITY,
            rule_id="C_CAPABILITY_READONLY_MISMATCH",
            category="C",
            severity="high",
            confidence="medium",
            file_path=skill_rel,
            line=line_no,
            snippet=skill_lines[line_no - 1] if 0 < line_no <= len(skill_lines) else "read-only",
            why="Declared read-only behavior conflicts with detected destructive execution patterns.",
            fix="Align contract and implementation. Remove destructive behavior or narrow capability statement.",
            tags=["capability-contract"],
            exploitability=0.75,
            reach=0.70,
        )

    if any(token in skill_text for token in {"local-only", "no network", "without network"}) and has_network_behavior:
        line_no = 1
        for token in ("local-only", "no network", "without network"):
            if token in skill_text:
                line_no = line_number_for_substring(skill_lines, token)
                break
        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_CAPABILITY,
            rule_id="C_CAPABILITY_NETWORK_MISMATCH",
            category="C",
            severity="high",
            confidence="medium",
            file_path=skill_rel,
            line=line_no,
            snippet=skill_lines[line_no - 1] if 0 < line_no <= len(skill_lines) else "local-only/no network",
            why="Declared local-only/no-network contract conflicts with detected network egress behavior.",
            fix="Update contract to reflect egress capability or remove outbound network behavior.",
            tags=["capability-contract", "network-egress"],
            exploitability=0.75,
            reach=0.70,
        )

    if "never execute code" in skill_text and has_download_exec:
        line_no = line_number_for_substring(skill_lines, "never execute code")
        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_CAPABILITY,
            rule_id="C_CAPABILITY_EXECUTION_MISMATCH",
            category="C",
            severity="critical",
            confidence="high",
            file_path=skill_rel,
            line=line_no,
            snippet=skill_lines[line_no - 1] if 0 < line_no <= len(skill_lines) else "never execute code",
            why="Contract denies code execution but download/exec behavior is present.",
            fix="Remove execution behavior or revise contract and require explicit high-risk gating.",
            tags=["capability-contract", "remote-exec"],
            exploitability=0.90,
            reach=0.80,
        )
