from __future__ import annotations

from pathlib import Path
from typing import Set, Tuple

from ..common import (
    is_defensive_prompt_line,
    is_non_runtime_line,
    line_has_any,
    line_is_trusted_bootstrap,
    looks_like_example_line,
)
from ..constants import (
    ATTACK_CONTENT_DECLARATION_RULES,
    DOCS_COMMAND_RISK_PATTERNS,
    LAYER_PROMPT,
    PROMPT_EXFIL_RULES,
    PROMPT_OVERRIDE_RULES,
)
from ..finding import add_finding, mark_layer_executed
from ..models import FileRecord, Finding, LayerState


def scan_prompt_semantics(
    record: FileRecord,
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    mark_layer_executed(layer_state, LAYER_PROMPT)
    rel_path = record["rel_path"]
    lines = record["lines"]

    for idx, raw_line in enumerate(lines, start=1):
        if is_non_runtime_line(raw_line):
            continue
        if looks_like_example_line(raw_line):
            continue
        if is_defensive_prompt_line(raw_line):
            continue

        for pattern, rule_id, severity, confidence, why, fix in PROMPT_OVERRIDE_RULES:
            if pattern.search(raw_line):
                add_finding(
                    findings,
                    dedupe,
                    layer_state,
                    layer=LAYER_PROMPT,
                    rule_id=rule_id,
                    category="A",
                    severity=severity,
                    confidence=confidence,
                    file_path=rel_path,
                    line=idx,
                    snippet=raw_line,
                    why=why,
                    fix=fix,
                    tags=["prompt-injection", "hierarchy"],
                    exploitability=0.75,
                    reach=0.65,
                )

        for pattern, rule_id, severity, confidence, why, fix in PROMPT_EXFIL_RULES:
            if pattern.search(raw_line):
                add_finding(
                    findings,
                    dedupe,
                    layer_state,
                    layer=LAYER_PROMPT,
                    rule_id=rule_id,
                    category="B",
                    severity=severity,
                    confidence=confidence,
                    file_path=rel_path,
                    line=idx,
                    snippet=raw_line,
                    why=why,
                    fix=fix,
                    tags=["prompt-injection", "secret-exfiltration", "attack-surface"],
                    exploitability=0.90,
                    reach=0.85,
                )

        for pattern, rule_id, severity, confidence, why, fix in ATTACK_CONTENT_DECLARATION_RULES:
            if pattern.search(raw_line):
                add_finding(
                    findings,
                    dedupe,
                    layer_state,
                    layer=LAYER_PROMPT,
                    rule_id=rule_id,
                    category="A" if rule_id.startswith("A_") else "E",
                    severity=severity,
                    confidence=confidence,
                    file_path=rel_path,
                    line=idx,
                    snippet=raw_line,
                    why=why,
                    fix=fix,
                    tags=["attack-surface", "demo-content"],
                    exploitability=0.72,
                    reach=0.70,
                )


def scan_docs_command_risk(
    record: FileRecord,
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    rel_path = record["rel_path"]
    path_obj: Path = record["path_obj"]
    if path_obj.suffix.lower() not in {".md", ".txt", ".html", ".htm"}:
        return

    mark_layer_executed(layer_state, LAYER_PROMPT)
    for idx, raw_line in enumerate(record["lines"], start=1):
        if is_non_runtime_line(raw_line):
            continue
        if not line_has_any(raw_line, DOCS_COMMAND_RISK_PATTERNS):
            continue

        severity = "high"
        confidence = "medium"
        why = "Documentation includes direct download-and-exec command example."
        fix = "Replace with verified artifact workflow and checksum/signature verification steps."
        if line_is_trusted_bootstrap(raw_line):
            severity = "medium"
            why = "Documentation includes download-and-exec command from a known bootstrap domain."
            fix = "Prefer pinned release artifacts and integrity checks over pipe-to-shell examples."

        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_PROMPT,
            rule_id="E_DOCS_DOWNLOAD_EXEC_COMMAND",
            category="E",
            severity=severity,
            confidence=confidence,
            file_path=rel_path,
            line=idx,
            snippet=raw_line,
            why=why,
            fix=fix,
            tags=["docs", "download-exec", "attack-surface"],
            exploitability=0.60,
            reach=0.55,
        )
