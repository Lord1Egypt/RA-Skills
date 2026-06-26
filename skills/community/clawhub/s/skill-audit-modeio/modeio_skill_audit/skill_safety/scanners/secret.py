from __future__ import annotations

from typing import Set, Tuple

from ..common import is_non_runtime_line, line_has_any, nearest_distance
from ..constants import (
    ENV_SOURCE_PATTERNS,
    EXTERNAL_URL_PATTERN,
    LAYER_SECRET,
    NETWORK_SINK_PATTERNS,
    SUSPICIOUS_EGRESS_PATTERNS,
    SYSTEM_ENUM_PATTERNS,
)
from ..finding import add_finding, mark_layer_executed
from ..models import FileRecord, Finding, LayerState


def scan_secret_exfiltration(
    record: FileRecord,
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    mark_layer_executed(layer_state, LAYER_SECRET)

    rel_path = record["rel_path"]
    lines = record["lines"]

    source_lines: list[int] = []
    sink_lines: list[int] = []
    suspicious_lines: list[int] = []
    system_info_lines: list[int] = []

    for idx, raw_line in enumerate(lines, start=1):
        if is_non_runtime_line(raw_line):
            continue
        if line_has_any(raw_line, ENV_SOURCE_PATTERNS):
            source_lines.append(idx)
        if line_has_any(raw_line, NETWORK_SINK_PATTERNS):
            sink_lines.append(idx)
        if line_has_any(raw_line, SUSPICIOUS_EGRESS_PATTERNS) or EXTERNAL_URL_PATTERN.search(raw_line):
            suspicious_lines.append(idx)
        if line_has_any(raw_line, SYSTEM_ENUM_PATTERNS):
            system_info_lines.append(idx)

        if line_has_any(raw_line, ENV_SOURCE_PATTERNS) and line_has_any(raw_line, NETWORK_SINK_PATTERNS):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SECRET,
                rule_id="B_SOURCE_AND_SINK_SAME_LINE",
                category="B",
                severity="critical",
                confidence="high",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="Secret source and outbound network sink appear in the same statement.",
                fix="Remove direct source-to-sink transfer and enforce strict egress policy.",
                tags=["secret-exfiltration", "network-egress"],
                exploitability=0.95,
                reach=0.85,
            )

    if source_lines and sink_lines:
        distance, target = nearest_distance(source_lines, sink_lines)
        target_line = lines[target - 1] if target - 1 < len(lines) else ""

        if distance <= 50:
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SECRET,
                rule_id="B_SOURCE_TO_SINK_PROXIMITY",
                category="B",
                severity="high",
                confidence="medium",
                file_path=rel_path,
                line=target,
                snippet=target_line,
                why="Secret source and network sink are closely correlated in the same file.",
                fix="Introduce explicit data-flow guards and block secret-bearing outbound requests.",
                tags=["secret-exfiltration", "network-egress"],
                exploitability=0.80,
                reach=0.80,
            )

    if system_info_lines and sink_lines:
        distance, target = nearest_distance(system_info_lines, sink_lines)
        if distance <= 60:
            target_line = lines[target - 1] if target - 1 < len(lines) else ""
            severity = "medium"
            confidence = "medium"
            if suspicious_lines:
                suspicious_distance, _ = nearest_distance(system_info_lines, suspicious_lines)
                if suspicious_distance <= 60:
                    severity = "high"
                    confidence = "medium"

            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SECRET,
                rule_id="B_SYSTEM_INFO_NETWORK_CORRELATION",
                category="B",
                severity=severity,
                confidence=confidence,
                file_path=rel_path,
                line=target,
                snippet=target_line,
                why="System-identifying data is correlated with outbound network behavior.",
                fix="Review and minimize outbound transmission of host/user/system metadata.",
                tags=["system-exfiltration", "network-egress"],
                exploitability=0.75,
                reach=0.75,
            )
