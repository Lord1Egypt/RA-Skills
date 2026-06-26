from __future__ import annotations

import re
from pathlib import Path
from typing import Dict, Sequence, Set, Tuple

from ..common import is_literal_safe_exec, is_non_runtime_line, line_has_any, nearest_distance
from ..constants import (
    BASE64_PIPE_PATTERN,
    DESTRUCTIVE_RULES,
    DOWNLOAD_EXEC_PATTERN,
    EXEC_RULES,
    JS_DYNAMIC_EVAL_PATTERN,
    LAYER_EVASION,
    LAYER_STATIC,
    POWERSHELL_ENCODED_PATTERN,
    PRIVILEGED_OPERATION_RULES,
    PROMPT_STEGO_PATTERN,
    PY_DYNAMIC_EXEC_PATTERN,
    STEGO_TECHNIQUE_PATTERN,
    UNICODE_TAG_BUILD_PATTERN,
    UNICODE_TAG_RANGE_PATTERN,
)
from ..finding import add_finding, mark_layer_executed
from ..models import FileRecord, Finding, LayerState


def _is_detection_meta_line(raw_line: str) -> bool:
    stripped = raw_line.strip()
    lowered = stripped.lower()
    if stripped.startswith(("r\"", "r'", '"', "'")) and "0xE0000" in stripped:
        return True
    if "0xe0000" in lowered and "stripped" in lowered:
        return True
    if "for ch in raw_line" in lowered and "0xe0000" in lowered:
        return True
    if "pattern.search(raw_line)" in lowered:
        return True
    if any(token in lowered for token in ("rule_id=", "why=", "fix=", "add_finding(")):
        return True
    return False


def _scan_multiline_subprocess_shell_true(
    rel_path: str,
    lines: Sequence[str],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    call_pattern = re.compile(r"\bsubprocess\.(run|Popen|call|check_call|check_output)\s*\(")
    for idx, raw_line in enumerate(lines, start=1):
        if not call_pattern.search(raw_line):
            continue
        window_end = min(len(lines), idx + 7)
        window = "\n".join(lines[idx - 1 : window_end])
        if "shell=True" not in window:
            continue
        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_STATIC,
            rule_id="C_SUBPROCESS_SHELL_TRUE_MULTILINE",
            category="C",
            severity="high",
            confidence="high",
            file_path=rel_path,
            line=idx,
            snippet=raw_line,
            why="Multiline subprocess call enables shell=True command execution.",
            fix="Avoid shell=True and pass command arguments as explicit arrays.",
            tags=["exec-surface", "multiline"],
            exploitability=0.85,
            reach=0.80,
        )


def _extract_node_exec_aliases(lines: Sequence[str]) -> Dict[str, int]:
    aliases: Dict[str, int] = {}
    require_pattern = re.compile(
        r"\{\s*([^}]+)\s*\}\s*=\s*require\(\s*['\"]child_process['\"]\s*\)",
        re.IGNORECASE,
    )
    import_pattern = re.compile(
        r"\{\s*([^}]+)\s*\}\s*from\s*['\"]child_process['\"]",
        re.IGNORECASE,
    )

    for idx, raw_line in enumerate(lines, start=1):
        match = require_pattern.search(raw_line) or import_pattern.search(raw_line)
        if not match:
            continue
        tokens = [token.strip() for token in match.group(1).split(",") if token.strip()]
        for token in tokens:
            parts = [part.strip() for part in token.split(":", 1)]
            if len(parts) == 2:
                original, alias = parts[0], parts[1]
            else:
                original, alias = parts[0], parts[0]
            if original in {"exec", "execSync"} and alias:
                aliases[alias] = idx
    return aliases


def _scan_node_exec_alias_usage(
    rel_path: str,
    lines: Sequence[str],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    aliases = _extract_node_exec_aliases(lines)
    if not aliases:
        return

    for alias in sorted(aliases):
        call_pattern = re.compile(rf"\b{re.escape(alias)}\s*\(")
        for idx, raw_line in enumerate(lines, start=1):
            if idx == aliases[alias]:
                continue
            if not call_pattern.search(raw_line):
                continue
            if is_literal_safe_exec(raw_line):
                add_finding(
                    findings,
                    dedupe,
                    layer_state,
                    layer=LAYER_STATIC,
                    rule_id="C_NODE_EXEC_ALIAS_LITERAL_SAFE",
                    category="C",
                    severity="low",
                    confidence="medium",
                    file_path=rel_path,
                    line=idx,
                    snippet=raw_line,
                    why="Node exec alias executes a fixed literal command with low injection surface.",
                    fix="Keep command literal and avoid concatenating untrusted inputs.",
                    tags=["exec-surface", "node", "literal-safe", "hygiene"],
                    exploitability=0.30,
                    reach=0.45,
                )
                continue
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_STATIC,
                rule_id="C_NODE_EXEC_ALIAS_CALL",
                category="C",
                severity="high",
                confidence="high",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="Node child_process exec alias is invoked, enabling shell command execution.",
                fix="Avoid child_process exec/execSync and use safer process execution patterns.",
                tags=["exec-surface", "node"],
                exploitability=0.85,
                reach=0.80,
            )


def _scan_unicode_tag_smuggling(
    rel_path: str,
    lines: Sequence[str],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    for idx, raw_line in enumerate(lines, start=1):
        if is_non_runtime_line(raw_line) or _is_detection_meta_line(raw_line):
            continue
        has_tag_chars = any(0xE0000 <= ord(ch) <= 0xE007F for ch in raw_line)
        if has_tag_chars or UNICODE_TAG_BUILD_PATTERN.search(raw_line) or UNICODE_TAG_RANGE_PATTERN.search(raw_line):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_EVASION,
                rule_id="D_UNICODE_TAG_SMUGGLING",
                category="D",
                severity="high",
                confidence="high",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="Unicode tag smuggling pattern can hide prompt-injection payloads.",
                fix="Reject hidden unicode-tag payloads and normalize text before safety checks.",
                tags=["obfuscation", "prompt-smuggling"],
                exploitability=0.85,
                reach=0.80,
            )


def _scan_prompt_steganography_content(
    rel_path: str,
    lines: Sequence[str],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    prompt_lines: list[int] = []
    technique_lines: list[int] = []

    for idx, raw_line in enumerate(lines, start=1):
        if _is_detection_meta_line(raw_line):
            continue
        if PROMPT_STEGO_PATTERN.search(raw_line):
            prompt_lines.append(idx)
        if STEGO_TECHNIQUE_PATTERN.search(raw_line):
            technique_lines.append(idx)

    if not prompt_lines or not technique_lines:
        return

    distance, target = nearest_distance(prompt_lines, technique_lines)
    if distance > 120:
        return

    snippet = lines[target - 1] if target - 1 < len(lines) else rel_path
    add_finding(
        findings,
        dedupe,
        layer_state,
        layer=LAYER_EVASION,
        rule_id="D_PROMPT_STEGANOGRAPHY_CONTENT",
        category="D",
        severity="high",
        confidence="medium",
        file_path=rel_path,
        line=target,
        snippet=snippet,
        why="Code appears to embed/extract hidden prompt payloads using steganographic techniques.",
        fix="Treat hidden prompt payload generation as hostile content and isolate it from execution paths.",
        tags=["prompt-smuggling", "steganography", "attack-surface"],
        exploitability=0.78,
        reach=0.72,
    )


def scan_exec_and_evasion(
    record: FileRecord,
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    mark_layer_executed(layer_state, LAYER_STATIC)
    mark_layer_executed(layer_state, LAYER_EVASION)

    path_obj: Path = record["path_obj"]
    rel_path = record["rel_path"]
    lines = record["lines"]

    if path_obj.name == "package.json":
        return

    _scan_multiline_subprocess_shell_true(rel_path, lines, findings, dedupe, layer_state)
    _scan_unicode_tag_smuggling(rel_path, lines, findings, dedupe, layer_state)
    _scan_prompt_steganography_content(rel_path, lines, findings, dedupe, layer_state)
    if path_obj.suffix.lower() in {".js", ".mjs", ".cjs", ".ts", ".tsx"}:
        _scan_node_exec_alias_usage(rel_path, lines, findings, dedupe, layer_state)

    for idx, raw_line in enumerate(lines, start=1):
        if is_non_runtime_line(raw_line) or _is_detection_meta_line(raw_line):
            continue

        for pattern, layer, rule_id, severity, confidence, why, fix in EXEC_RULES:
            if pattern.search(raw_line):
                if rule_id == "C_NODE_EXEC_CALL" and is_literal_safe_exec(raw_line):
                    add_finding(
                        findings,
                        dedupe,
                        layer_state,
                        layer=layer,
                        rule_id="C_NODE_EXEC_LITERAL_SAFE",
                        category="C",
                        severity="low",
                        confidence="medium",
                        file_path=rel_path,
                        line=idx,
                        snippet=raw_line,
                        why="Node exec call executes a fixed literal command with low injection surface.",
                        fix="Keep command literal and avoid concatenating untrusted inputs.",
                        tags=["exec-surface", "literal-safe", "hygiene"],
                        exploitability=0.30,
                        reach=0.45,
                    )
                    continue
                add_finding(
                    findings,
                    dedupe,
                    layer_state,
                    layer=layer,
                    rule_id=rule_id,
                    category="C",
                    severity=severity,
                    confidence=confidence,
                    file_path=rel_path,
                    line=idx,
                    snippet=raw_line,
                    why=why,
                    fix=fix,
                    tags=["exec-surface"],
                    exploitability=0.80,
                    reach=0.75,
                )

        for pattern, rule_id, why in PRIVILEGED_OPERATION_RULES:
            if not pattern.search(raw_line):
                continue
            severity = "high"
            confidence = "medium"
            lowered = raw_line.lower()
            if "sudo" in lowered or any(token in lowered for token in ("debugfs", "losetup", "fsck")):
                confidence = "high"
            if any(token in lowered for token in ("debugfs", "losetup", "modprobe", "insmod")):
                severity = "critical"
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_STATIC,
                rule_id=rule_id,
                category="C",
                severity=severity,
                confidence=confidence,
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why=why,
                fix="Restrict privileged host operations to explicitly approved maintenance flows.",
                tags=["privileged", "system"],
                exploitability=0.85,
                reach=0.82,
            )
            break

        if DOWNLOAD_EXEC_PATTERN.search(raw_line):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_EVASION,
                rule_id="D_DOWNLOAD_PIPE_EXEC",
                category="D",
                severity="critical",
                confidence="high",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="Remote content is piped directly into shell execution.",
                fix="Download artifact to disk, verify integrity/provenance, then execute trusted local file.",
                tags=["download-exec", "remote-exec"],
                exploitability=0.95,
                reach=0.90,
            )

        if BASE64_PIPE_PATTERN.search(raw_line):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_EVASION,
                rule_id="D_BASE64_PIPE_EXEC",
                category="D",
                severity="critical",
                confidence="high",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="Base64 decode pipeline is chained directly into shell execution.",
                fix="Do not execute decoded payloads directly. Use reviewed static scripts only.",
                tags=["obfuscation", "download-exec"],
                exploitability=0.90,
                reach=0.90,
            )

        if POWERSHELL_ENCODED_PATTERN.search(raw_line):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_EVASION,
                rule_id="D_POWERSHELL_ENCODED_COMMAND",
                category="D",
                severity="high",
                confidence="high",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="Encoded PowerShell command can hide runtime behavior.",
                fix="Replace encoded command invocation with reviewed plain-text script path.",
                tags=["obfuscation"],
                exploitability=0.85,
                reach=0.80,
            )

        if PY_DYNAMIC_EXEC_PATTERN.search(raw_line):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_EVASION,
                rule_id="D_PY_DYNAMIC_EXEC_BASE64",
                category="D",
                severity="high",
                confidence="high",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="Python exec() over decoded payload detected.",
                fix="Avoid dynamic exec of decoded data and use static vetted code paths.",
                tags=["obfuscation"],
                exploitability=0.85,
                reach=0.80,
            )

        if JS_DYNAMIC_EVAL_PATTERN.search(raw_line):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_EVASION,
                rule_id="D_JS_DYNAMIC_EVAL_BASE64",
                category="D",
                severity="high",
                confidence="medium",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="JavaScript dynamic eval over decoded payload detected.",
                fix="Remove eval/function-constructor execution and parse trusted structured data instead.",
                tags=["obfuscation"],
                exploitability=0.80,
                reach=0.75,
            )

        for pattern, rule_id, severity, confidence, why in DESTRUCTIVE_RULES:
            if pattern.search(raw_line):
                add_finding(
                    findings,
                    dedupe,
                    layer_state,
                    layer=LAYER_STATIC,
                    rule_id=rule_id,
                    category="C",
                    severity=severity,
                    confidence=confidence,
                    file_path=rel_path,
                    line=idx,
                    snippet=raw_line,
                    why=why,
                    fix="Restrict destructive commands to explicit reviewed maintenance workflows.",
                    tags=["destructive"],
                    exploitability=0.90,
                    reach=0.90,
                )
