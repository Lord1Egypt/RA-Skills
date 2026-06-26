from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Sequence, Set, Tuple

from ..common import (
    is_non_runtime_line,
    line_has_any,
    line_is_trusted_bootstrap,
    line_number_for_substring,
    normalize_relative_path,
)
from ..constants import (
    DESTRUCTIVE_RULES,
    DOWNLOAD_EXEC_PATTERN,
    EXTERNAL_URL_PATTERN,
    HOOK_RISK_PATTERNS,
    HOOK_TARGET_EXEC_PATTERNS,
    HOOK_TARGET_SKIP_PREFIXES,
    HOOK_TARGET_SPLIT_PATTERN,
    HOOK_TARGET_WRITE_PATTERNS,
    INSTALL_HOOK_LOCAL_SCRIPT_PATTERN,
    INSTALL_HOOK_NAMES,
    LAYER_SUPPLY,
    NETWORK_SINK_PATTERNS,
    PY_OS_SYSTEM_PATTERN,
    PY_SETUP_INSTALL_HOOK_PATTERNS,
    PY_SUBPROCESS_EXEC_PATTERN,
    WORKFLOW_USES_PATTERN,
)
from ..finding import add_finding, mark_layer_executed
from ..models import FileRecord, Finding, LayerState


def _scan_workflow_command(
    rel_path: str,
    line_no: int,
    command_line: str,
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    if DOWNLOAD_EXEC_PATTERN.search(command_line):
        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_SUPPLY,
            rule_id="E_WORKFLOW_DOWNLOAD_EXEC",
            category="E",
            severity="critical",
            confidence="high",
            file_path=rel_path,
            line=line_no,
            snippet=command_line,
            why="Workflow command performs download-and-exec.",
            fix="Require downloaded artifact verification and local execution only.",
            tags=["workflow", "download-exec"],
            exploitability=0.95,
            reach=0.85,
        )

    for pattern, rule_id, severity, confidence, why in DESTRUCTIVE_RULES:
        if pattern.search(command_line):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SUPPLY,
                rule_id=f"E_WORKFLOW_{rule_id}",
                category="E",
                severity=severity,
                confidence=confidence,
                file_path=rel_path,
                line=line_no,
                snippet=command_line,
                why=f"Workflow command: {why}",
                fix="Limit destructive workflow commands to controlled maintenance pipelines.",
                tags=["workflow", "destructive"],
                exploitability=0.90,
                reach=0.85,
            )


def _scan_workflow_blocks(
    rel_path: str,
    lines: Sequence[str],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    idx = 0
    while idx < len(lines):
        current = lines[idx]

        single = re.match(r"^\s*run:\s*(.+)$", current)
        if single and single.group(1).strip() not in {"|", ">"}:
            _scan_workflow_command(
                rel_path,
                idx + 1,
                single.group(1).strip(),
                findings,
                dedupe,
                layer_state,
            )
            idx += 1
            continue

        block = re.match(r"^(\s*)run:\s*[|>]\s*$", current)
        if block:
            base_indent = len(block.group(1))
            idx += 1
            while idx < len(lines):
                line = lines[idx]
                if not line.strip():
                    idx += 1
                    continue
                indent = len(line) - len(line.lstrip(" "))
                if indent <= base_indent:
                    break
                _scan_workflow_command(
                    rel_path,
                    idx + 1,
                    line.strip(),
                    findings,
                    dedupe,
                    layer_state,
                )
                idx += 1
            continue

        idx += 1


def _scan_workflow_uses(
    rel_path: str,
    lines: Sequence[str],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    for idx, raw_line in enumerate(lines, start=1):
        match = WORKFLOW_USES_PATTERN.match(raw_line)
        if not match:
            continue
        ref = match.group(1).strip()
        if ref.startswith("./"):
            continue

        if "@" not in ref:
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SUPPLY,
                rule_id="E_WORKFLOW_ACTION_UNPINNED",
                category="E",
                severity="medium",
                confidence="high",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="GitHub Action reference is not pinned to an immutable ref.",
                fix="Pin action reference to a full commit SHA.",
                tags=["workflow", "action-pinning", "hygiene"],
                exploitability=0.80,
                reach=0.75,
            )
            continue

        action_name, action_ref = ref.rsplit("@", 1)
        if re.fullmatch(r"[0-9a-fA-F]{40}", action_ref):
            continue

        severity = "medium"
        confidence = "high"
        why = "GitHub Action uses a mutable tag/ref instead of commit SHA pinning."
        if action_ref.lower() in {"main", "master", "latest"}:
            severity = "medium"
            why = "GitHub Action points to floating branch ref."
        elif action_ref.startswith("v"):
            severity = "medium"
            why = "GitHub Action uses mutable version tag instead of immutable SHA."

        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_SUPPLY,
            rule_id="E_WORKFLOW_ACTION_MUTABLE_REF",
            category="E",
            severity=severity,
            confidence=confidence,
            file_path=rel_path,
            line=idx,
            snippet=raw_line,
            why=why,
            fix=f"Pin {action_name} to a full 40-char commit SHA.",
            tags=["workflow", "action-pinning", "hygiene"],
            exploitability=0.75,
            reach=0.70,
        )


def _extract_hook_target_paths(command: str) -> list[str]:
    targets: list[str] = []
    segments = HOOK_TARGET_SPLIT_PATTERN.split(command)
    for segment in segments:
        candidate = segment.strip()
        if not candidate:
            continue
        if any(candidate.startswith(prefix + " ") or candidate == prefix for prefix in HOOK_TARGET_SKIP_PREFIXES):
            continue
        local_script_match = INSTALL_HOOK_LOCAL_SCRIPT_PATTERN.search(candidate)
        if not local_script_match:
            continue
        target = normalize_relative_path(local_script_match.group(2))
        if target:
            targets.append(target)
    return targets


def _scan_install_hook_target_script(
    *,
    package_rel_path: str,
    hook_name: str,
    command: str,
    records_by_rel: dict[str, FileRecord],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    package_dir = normalize_relative_path(str(Path(package_rel_path).parent))

    for target in _extract_hook_target_paths(command):
        candidate_paths = [target]
        if package_dir and package_dir not in {".", ""}:
            candidate_paths.append(normalize_relative_path(str(Path(package_dir) / target)))

        record = None
        for candidate in candidate_paths:
            record = records_by_rel.get(candidate)
            if record:
                break
        if not record:
            continue

        target_lines: Sequence[str] = record["lines"]
        has_exec = False
        has_write = False
        has_network = False
        has_download_exec = False
        has_shell_exec = False
        best_line_no = 1
        best_snippet = target_lines[0] if target_lines else target

        for idx, raw_line in enumerate(target_lines, start=1):
            if is_non_runtime_line(raw_line):
                continue
            if not has_exec and line_has_any(raw_line, HOOK_TARGET_EXEC_PATTERNS):
                has_exec = True
                best_line_no = idx
                best_snippet = raw_line
            if "shell: true" in raw_line.lower() or "shell=true" in raw_line.lower():
                has_shell_exec = True
                if best_line_no == 1:
                    best_line_no = idx
                    best_snippet = raw_line
            if not has_write and line_has_any(raw_line, HOOK_TARGET_WRITE_PATTERNS):
                has_write = True
                if best_line_no == 1:
                    best_line_no = idx
                    best_snippet = raw_line
            if not has_network and (line_has_any(raw_line, NETWORK_SINK_PATTERNS) or EXTERNAL_URL_PATTERN.search(raw_line)):
                has_network = True
                if best_line_no == 1:
                    best_line_no = idx
                    best_snippet = raw_line
            if DOWNLOAD_EXEC_PATTERN.search(raw_line):
                has_download_exec = True
                best_line_no = idx
                best_snippet = raw_line
                break

        if not (has_exec or has_write or has_network or has_download_exec):
            continue

        rule_id = "E_INSTALL_HOOK_TARGET_SCRIPT_BEHAVIOR"
        severity = "high"
        confidence = "medium"
        why = "Install hook target script performs sensitive runtime behavior."
        fix = "Move install-time side effects behind explicit reviewed commands and validate artifact integrity."
        exploitability = 0.80
        reach = 0.80

        if has_download_exec:
            rule_id = "E_INSTALL_HOOK_TARGET_DOWNLOAD_EXEC"
            severity = "critical"
            confidence = "high"
            why = "Install hook target script performs download-and-exec behavior."
            exploitability = 0.92
            reach = 0.86
        elif has_exec and has_network and has_write:
            rule_id = "E_INSTALL_HOOK_TARGET_STAGED_EXEC"
            severity = "high"
            confidence = "high"
            why = "Install hook target script combines network, file write, and command execution."
            exploitability = 0.88
            reach = 0.84
        elif has_exec and (has_network or has_write):
            severity = "high"
            confidence = "medium"
            why = "Install hook target script combines command execution with network/file side effects."
        elif has_exec:
            severity = "medium"
            confidence = "medium"
            why = "Install hook target script executes commands during install lifecycle."
            if has_shell_exec:
                severity = "high"
                confidence = "high"
                why = "Install hook target script uses shell-enabled command execution during install lifecycle."

        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_SUPPLY,
            rule_id=rule_id,
            category="E",
            severity=severity,
            confidence=confidence,
            file_path=record["rel_path"],
            line=best_line_no,
            snippet=best_snippet,
            why=why,
            fix=fix,
            tags=["install-hook", hook_name, "hook-target", f"source:{package_rel_path}"],
            exploitability=exploitability,
            reach=reach,
        )


def _scan_package_hooks(
    rel_path: str,
    lines: Sequence[str],
    text: str,
    records_by_rel: dict[str, FileRecord],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    try:
        payload = json.loads(text)
    except (TypeError, ValueError):
        return

    scripts = payload.get("scripts")
    if not isinstance(scripts, dict):
        return

    for hook in sorted(INSTALL_HOOK_NAMES):
        command = scripts.get(hook)
        if not isinstance(command, str):
            continue

        local_script_match = INSTALL_HOOK_LOCAL_SCRIPT_PATTERN.search(command)
        is_risky = line_has_any(command, HOOK_RISK_PATTERNS)
        if not is_risky and not local_script_match:
            continue

        line_no = line_number_for_substring(lines, f'"{hook}"')

        if is_risky:
            rule_id = "E_INSTALL_HOOK_RISKY_COMMAND"
            severity = "high"
            confidence = "high"
            why = "Install lifecycle hook executes high-risk command behavior."
            if DOWNLOAD_EXEC_PATTERN.search(command):
                rule_id = "E_INSTALL_HOOK_DOWNLOAD_EXEC"
                severity = "critical"
                why = "Install hook performs download-and-exec behavior."
                if line_is_trusted_bootstrap(command):
                    severity = "high"
                    confidence = "medium"
                    why = "Install hook performs bootstrap download-and-exec from known domain."

            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SUPPLY,
                rule_id=rule_id,
                category="E",
                severity=severity,
                confidence=confidence,
                file_path=rel_path,
                line=line_no,
                snippet=f"{hook}: {command}",
                why=why,
                fix="Remove risky lifecycle hook behavior and move to reviewed build scripts.",
                tags=["install-hook", hook],
                exploitability=0.90,
                reach=0.85,
            )

        _scan_install_hook_target_script(
            package_rel_path=rel_path,
            hook_name=hook,
            command=command,
            records_by_rel=records_by_rel,
            findings=findings,
            dedupe=dedupe,
            layer_state=layer_state,
        )

        if local_script_match and not is_risky:
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SUPPLY,
                rule_id="E_INSTALL_HOOK_SCRIPT_EXECUTION",
                category="E",
                severity="medium",
                confidence="high",
                file_path=rel_path,
                line=line_no,
                snippet=f"{hook}: {command}",
                why="Install lifecycle hook executes a local script.",
                fix="Review hook script behavior and keep install-time side effects minimal.",
                tags=["install-hook", hook, "hygiene"],
                exploitability=0.70,
                reach=0.75,
            )


def _scan_requirements(
    rel_path: str,
    lines: Sequence[str],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    for idx, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        if line.startswith(("http://", "https://", "git+https://", "git+ssh://")):
            add_finding(
                findings,
                dedupe,
                layer_state,
                layer=LAYER_SUPPLY,
                rule_id="E_PY_REQUIREMENT_REMOTE_SOURCE",
                category="E",
                severity="high",
                confidence="medium",
                file_path=rel_path,
                line=idx,
                snippet=raw_line,
                why="Requirement points directly to remote source URL.",
                fix="Prefer vetted index packages and pin immutable versions/hashes.",
                tags=["dependency", "python"],
                exploitability=0.75,
                reach=0.70,
            )
            continue

        if "==" in line or "@" in line:
            continue

        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_SUPPLY,
            rule_id="E_PY_REQUIREMENT_UNPINNED",
            category="E",
            severity="medium",
            confidence="high",
            file_path=rel_path,
            line=idx,
            snippet=raw_line,
            why="Python dependency is not pinned to an exact version.",
            fix="Pin dependency to exact version and include hash where possible.",
            tags=["dependency", "python"],
            exploitability=0.60,
            reach=0.65,
        )


def _scan_python_setup_supply_chain(
    rel_path: str,
    lines: Sequence[str],
    text: str,
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    if Path(rel_path).name != "setup.py":
        return

    has_install_hook = any(pattern.search(text) for pattern in PY_SETUP_INSTALL_HOOK_PATTERNS)
    has_network = False
    has_exec = False
    has_write = False
    best_line_no = 1
    best_snippet = lines[0] if lines else rel_path

    for idx, raw_line in enumerate(lines, start=1):
        if is_non_runtime_line(raw_line):
            continue

        line_network = line_has_any(raw_line, NETWORK_SINK_PATTERNS) or EXTERNAL_URL_PATTERN.search(raw_line) is not None
        line_exec = PY_SUBPROCESS_EXEC_PATTERN.search(raw_line) or PY_OS_SYSTEM_PATTERN.search(raw_line)
        line_write = (
            "open(" in raw_line and any(token in raw_line for token in ("'w'", '"w"', "'wb'", '"wb"'))
        ) or line_has_any(raw_line, HOOK_TARGET_WRITE_PATTERNS)

        if line_network and not has_network:
            has_network = True
            best_line_no = idx
            best_snippet = raw_line
        if line_exec and not has_exec:
            has_exec = True
            best_line_no = idx
            best_snippet = raw_line
        if line_write and not has_write:
            has_write = True
            if best_line_no == 1:
                best_line_no = idx
                best_snippet = raw_line

    if not (has_install_hook or has_network or has_exec):
        return

    if has_network and has_exec:
        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_SUPPLY,
            rule_id="E_PY_SETUP_NETWORK_EXEC",
            category="E",
            severity="critical",
            confidence="high",
            file_path=rel_path,
            line=best_line_no,
            snippet=best_snippet,
            why="setup.py combines network retrieval and command execution during package install flow.",
            fix="Remove setup-time network/exec behavior and move to reviewed, explicit build/release steps.",
            tags=["python-packaging", "install-hook", "attack-surface"],
            exploitability=0.95,
            reach=0.88,
        )
        return

    if has_install_hook and (has_network or has_exec or has_write):
        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_SUPPLY,
            rule_id="E_PY_SETUP_INSTALL_HOOK_BEHAVIOR",
            category="E",
            severity="high",
            confidence="high",
            file_path=rel_path,
            line=best_line_no,
            snippet=best_snippet,
            why="setup.py install hook performs side effects at install time.",
            fix="Avoid install-hook side effects and require explicit user-invoked setup steps.",
            tags=["python-packaging", "install-hook", "attack-surface"],
            exploitability=0.86,
            reach=0.82,
        )


def scan_supply_chain(
    records: Sequence[FileRecord],
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
) -> None:
    mark_layer_executed(layer_state, LAYER_SUPPLY)

    has_package_json = False
    has_lockfile = False
    records_by_rel = {
        normalize_relative_path(record["rel_path"]): record for record in records
    }

    for record in records:
        rel_path = record["path_obj"]
        rel = record["rel_path"]
        lines = record["lines"]
        text = record["text"]
        rel_norm = str(rel_path).replace("\\", "/")

        if rel_path.name == "package.json":
            has_package_json = True
            _scan_package_hooks(rel, lines, text, records_by_rel, findings, dedupe, layer_state)
        if rel_path.name in {"package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb"}:
            has_lockfile = True
        if rel_path.name == "requirements.txt":
            _scan_requirements(rel, lines, findings, dedupe, layer_state)
        if rel_path.name == "setup.py":
            _scan_python_setup_supply_chain(rel, lines, text, findings, dedupe, layer_state)

        if rel_norm.startswith(".github/workflows/") and rel_path.suffix.lower() in {".yml", ".yaml"}:
            _scan_workflow_blocks(rel, lines, findings, dedupe, layer_state)
            _scan_workflow_uses(rel, lines, findings, dedupe, layer_state)

    if has_package_json and not has_lockfile:
        add_finding(
            findings,
            dedupe,
            layer_state,
            layer=LAYER_SUPPLY,
            rule_id="E_NODE_LOCKFILE_MISSING",
            category="E",
            severity="medium",
            confidence="high",
            file_path="package.json",
            line=1,
            snippet="package.json without package-lock/yarn/pnpm lockfile",
            why="Node dependency lockfile is missing, reducing reproducibility and supply-chain integrity.",
            fix="Add and maintain a lockfile (package-lock.json, pnpm-lock.yaml, or yarn.lock).",
            tags=["dependency", "node"],
            exploitability=0.65,
            reach=0.70,
        )
