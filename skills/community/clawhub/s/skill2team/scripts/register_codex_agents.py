#!/usr/bin/env python3
"""Register or unregister Skill2Team Codex custom-agent packages.

This helper is intentionally conservative. It removes only files recorded in
the matching Skill2Team registry manifest, or files that carry explicit
Skill2Team ownership markers for the same team id.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


MANAGED_BY = "skill2team"
REGISTRY_DIR = Path(".codex") / "s2t-agent-registrations"
AGENTS_DIR = Path(".codex") / "agents"
CONFIG_PATH = Path(".codex") / "config.toml"
S2T_AGENT_METADATA_KEYS = {"managed_by", "s2t_team_id", "s2t_entry_agent", "entry_agent"}


def slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "team"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Keep machine JSON ASCII-escaped so legacy Windows readers do not corrupt it.
    path.write_text(json.dumps(obj, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def toml_string(value: str) -> str:
    return json.dumps(str(value), ensure_ascii=True)


def within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def old_registry_path(codex_root: Path, team_id: str) -> Path:
    return codex_root / REGISTRY_DIR / f"{slug(team_id)}.json"


def runtime_files_exist(codex_root: Path, manifest: dict[str, Any]) -> bool:
    files = manifest.get("registered_files") or []
    if not files:
        return False
    return all((codex_root / rel).exists() for rel in files)


def entry_artifact_registered(manifest: dict[str, Any]) -> bool:
    entry = str(manifest.get("entry_agent_id") or "")
    files = [str(rel) for rel in manifest.get("registered_files") or []]
    return bool(entry and any(Path(rel).stem == entry for rel in files))


def usable_registration(codex_root: Path, manifest: dict[str, Any]) -> bool:
    return (
        manifest.get("managed_by") == MANAGED_BY
        and manifest.get("registration_status") == "registered"
        and manifest.get("entry_agent_runnable") is True
        and entry_artifact_registered(manifest)
        and runtime_files_exist(codex_root, manifest)
    )


def same_meta_contract(existing: dict[str, Any], requested: dict[str, Any]) -> bool:
    keys = [
        "team_id",
        "team_kind",
        "source_skill",
        "target_runtime",
        "entry_agent_id",
        "skill2team_version",
        "meta_team_contract_version",
        "meta_team_signature",
    ]
    return all(existing.get(key) == requested.get(key) for key in keys)


def package_registry(package_dir: Path) -> dict[str, Any]:
    candidates = [
        package_dir / "s2t-agent-registry.json",
        package_dir / ".codex" / "s2t-agent-registry.json",
    ]
    for path in candidates:
        if path.exists():
            return read_json(path)
    agent_files = sorted((package_dir / ".codex" / "agents").glob("*.toml"))
    if not agent_files:
        raise SystemExit(f"No registry and no .codex/agents/*.toml found in {package_dir}")
    team_id = slug(package_dir.name)
    prefix = f"s2t-{team_id}"
    entry = next((p.stem for p in agent_files if p.stem.endswith("-entry")), f"{prefix}-entry")
    return {
        "schema_version": 1,
        "managed_by": MANAGED_BY,
        "team_id": team_id,
        "team_kind": "target",
        "target_runtime": "codex",
        "name_prefix": prefix,
        "entry_agent_id": entry,
        "agents": [
            {
                "agent_id": p.stem,
                "role": "unknown",
                "entry": p.stem == entry,
                "artifact_path": str(Path(".codex") / "agents" / p.name).replace("\\", "/"),
            }
            for p in agent_files
        ],
    }


def package_register_readiness(package_dir: Path) -> dict[str, Any]:
    candidates = [
        package_dir / "register-readiness-contract.json",
        package_dir / ".codex" / "register-readiness-contract.json",
    ]
    for path in candidates:
        if path.exists():
            return read_json(path)
    return {}


def validate_register_ready_package(package_dir: Path, registry: dict[str, Any]) -> list[str]:
    """Validate that the package can support hard register-time runtime checks."""
    blockers: list[str] = []
    readiness = dict(registry.get("register_readiness_policy") or package_register_readiness(package_dir))
    if not readiness:
        blockers.append("missing register-readiness-contract.json and register_readiness_policy")
    elif readiness.get("package_supports_register_hard_runtime_requirements") is not True:
        blockers.append("package does not declare support for register hard runtime requirements")
        blockers.extend(str(b) for b in readiness.get("register_blockers") or [])

    agents = registry.get("agents") or []
    entry = str(registry.get("entry_agent_id") or "")
    if not agents:
        blockers.append("registry has no planned agents")
    if not entry:
        blockers.append("registry has no entry_agent_id")
    if entry and not any(str(a.get("agent_id")) == entry or Path(str(a.get("artifact_path") or "")).stem == entry for a in agents):
        blockers.append(f"entry agent {entry} is not represented in registry agents")

    for agent in agents:
        artifact_rel = Path(str(agent.get("artifact_path") or ""))
        source = package_dir / artifact_rel
        if not source.exists():
            source = package_dir / ".codex" / "agents" / f"{agent.get('agent_id')}.toml"
        if not source.exists():
            blockers.append(f"missing planned agent artifact: {agent.get('agent_id')} ({artifact_rel})")
        elif source.suffix != ".toml":
            blockers.append(f"planned Codex agent artifact is not TOML: {source}")

    docs_needed = [
        package_dir / "docs" / "team-usage-guide.md",
        package_dir / "docs" / "runtime-invocation-contract.md",
        package_dir / "docs" / "register-readiness-contract.md",
        package_dir / "runtime-invocation-contract.json",
        package_dir / "register-readiness-contract.json",
    ]
    for path in docs_needed:
        if not path.exists():
            blockers.append(f"missing required package artifact for register readiness: {path.relative_to(package_dir)}")
    return blockers



def has_matching_marker(path: Path, team_id: str) -> bool:
    if not path.exists() or not path.is_file():
        return False
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return (
        f'managed_by = "{MANAGED_BY}"' in text
        and f's2t_team_id = "{team_id}"' in text
    )


def s2t_metadata_key(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("#"):
        stripped = stripped[1:].lstrip()
    if "=" not in stripped:
        return ""
    return stripped.split("=", 1)[0].strip()


def strip_s2t_agent_metadata(text: str) -> str:
    """Remove Skill2Team-only top-level TOML keys before Codex loads the file.

    Ownership markers are kept as comments by with_markers().  The removal is
    limited to the header before developer_instructions so instruction text is
    not edited accidentally.
    """
    lines: list[str] = []
    in_header = True
    for line in text.splitlines():
        if in_header and line.lstrip().startswith("developer_instructions"):
            in_header = False
        if in_header and s2t_metadata_key(line) in S2T_AGENT_METADATA_KEYS:
            continue
        lines.append(line)
    return "\n".join(lines).lstrip("\n")


def configured_agent_names(text: str) -> set[str]:
    return set(re.findall(r"(?m)^\s*\[agents\.([A-Za-z0-9_-]+)\]\s*$", text))


def remove_agent_config_blocks(text: str, agent_names: set[str]) -> str:
    if not agent_names:
        return text
    lines = text.splitlines()
    out: list[str] = []
    i = 0
    block_re = re.compile(r"^\s*\[agents\.([A-Za-z0-9_-]+)\]\s*$")
    table_re = re.compile(r"^\s*\[[^\]]+\]\s*$")
    while i < len(lines):
        match = block_re.match(lines[i])
        if match and match.group(1) in agent_names:
            i += 1
            while i < len(lines) and not table_re.match(lines[i]):
                i += 1
            while out and out[-1] == "":
                out.pop()
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out).rstrip() + ("\n" if out else "")


def ensure_agents_settings(text: str, min_threads: int) -> str:
    lines = text.splitlines()
    agents_start = next((i for i, line in enumerate(lines) if re.match(r"^\s*\[agents\]\s*$", line)), None)
    if agents_start is None:
        prefix = text.rstrip()
        addition = f"[agents]\nmax_threads = {max(1, min_threads)}\nmax_depth = 1\n"
        return (prefix + "\n\n" + addition if prefix else addition)

    agents_end = len(lines)
    for i in range(agents_start + 1, len(lines)):
        if re.match(r"^\s*\[[^\]]+\]\s*$", lines[i]):
            agents_end = i
            break

    block = lines[agents_start + 1:agents_end]
    seen_threads = False
    seen_depth = False
    for idx, line in enumerate(block):
        if re.match(r"^\s*max_threads\s*=", line):
            seen_threads = True
            current = re.search(r"=\s*(\d+)", line)
            if current and int(current.group(1)) < min_threads:
                block[idx] = f"max_threads = {min_threads}"
        elif re.match(r"^\s*max_depth\s*=", line):
            seen_depth = True
    inserts: list[str] = []
    if not seen_threads:
        inserts.append(f"max_threads = {max(1, min_threads)}")
    if not seen_depth:
        inserts.append("max_depth = 1")
    if inserts:
        block = inserts + block
    return "\n".join(lines[:agents_start + 1] + block + lines[agents_end:]).rstrip() + "\n"


def ensure_feature_flags(text: str) -> str:
    required = {"multi_agent": "true", "enable_fanout": "true"}
    lines = text.splitlines()
    features_start = next((i for i, line in enumerate(lines) if re.match(r"^\s*\[features\]\s*$", line)), None)
    if features_start is None:
        prefix = text.rstrip()
        addition = "[features]\n" + "\n".join(f"{key} = {value}" for key, value in required.items()) + "\n"
        return (prefix + "\n\n" + addition if prefix else addition)

    features_end = len(lines)
    for i in range(features_start + 1, len(lines)):
        if re.match(r"^\s*\[[^\]]+\]\s*$", lines[i]):
            features_end = i
            break

    block = lines[features_start + 1:features_end]
    seen: set[str] = set()
    for idx, line in enumerate(block):
        match = re.match(r"^\s*([A-Za-z0-9_-]+)\s*=", line)
        if not match:
            continue
        key = match.group(1)
        if key in required:
            block[idx] = f"{key} = {required[key]}"
            seen.add(key)
    for key, value in required.items():
        if key not in seen:
            block.append(f"{key} = {value}")
    return "\n".join(lines[:features_start + 1] + block + lines[features_end:]).rstrip() + "\n"


def merge_codex_agent_config(codex_root: Path, registered_files: list[str]) -> dict[str, Any]:
    config_path = codex_root / CONFIG_PATH
    agent_names = [Path(rel).stem for rel in registered_files if Path(rel).suffix == ".toml"]
    if not agent_names:
        return {"config_path": str(config_path), "agent_config_entries": []}

    config_path.parent.mkdir(parents=True, exist_ok=True)
    text = config_path.read_text(encoding="utf-8") if config_path.exists() else "# Skill2Team Codex project config.\n"
    text = ensure_feature_flags(text)
    text = remove_agent_config_blocks(text, set(agent_names))
    min_threads = max(len(configured_agent_names(text) | set(agent_names)), len(agent_names), 1)
    text = ensure_agents_settings(text, min_threads)
    text = text.rstrip() + "\n\n"
    for name in agent_names:
        text += f"[agents.{name}]\nconfig_file = {toml_string(f'./agents/{name}.toml')}\n\n"
    config_path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return {
        "config_path": str(config_path),
        "agent_config_entries": agent_names,
        "config_file_key": "config_file",
        "config_file_base": "relative_to_project_codex_config",
        "required_feature_flags": {
            "multi_agent": True,
            "enable_fanout": True,
        },
    }


def target_team_execution_guard_manifest(entry: str) -> dict[str, Any]:
    return {
        "schema_version": "s2t-target-team-execution-guard-v1",
        "target_runtime": "codex",
        "codex_target_team_execution_requires_real_registered_agents": True,
        "codex_target_team_execution_requires_real_specialist_handoffs": True,
        "codex_target_team_execution_allows_real_session_subagents_when_registered_agents_unavailable": True,
        "session_subagent_success_status": "real_session_target_subagents",
        "block_status": "target-team execution blocked",
        "forbid_single_agent_or_sequential_simulation": True,
        "entry_agent_id": entry,
        "rule": "If the registered entry agent cannot hand off to named specialist agents through Codex, use real current-session target subagents only when the active Codex thread can launch independent subagents for the generated target profiles and record target_run_fanout_status=real_session_target_subagents. Otherwise stop with target-team execution blocked; do not continue as sequential or single-agent simulation.",
    }


def registration_next_prompt_templates(team_id: str, entry: str, package_dir: Path, runtime_smoke_test_passed: bool) -> dict[str, str]:
    smoke_prompt = (
        "Start Skill2Team.\n"
        "Route: source-to-team.\n"
        "Delivery: package.\n"
        "Execution path: direct-skill.\n"
        "Target runtime: codex.\n"
        "Model invocation policy: use OpenAI Codex; do not call direct model APIs.\n"
        f"Team id: {team_id}.\n"
        f"Package path: {package_dir}.\n"
        "Post-package Codex action: run post-registration smoke tests for registered entry invocation, specialist handoff to every planned specialist, "
        "strict reviewer/verifier gate blocking, and state/artifact handoff. If this same running Codex thread reports `agent type is currently not available`, start a fresh thread or reload the workspace before retrying because newly written .codex agent config may not hot-load. Only mark entry_agent_runnable=true after evidence exists. "
        "If specialist handoff cannot run, report target-team execution blocked and do not continue as sequential or single-agent simulation."
    )
    use_prompt = (
        f"Use the registered `{entry}` agent.\n"
        "Task: <what you want this team to do>.\n"
        "Inputs: <files, state path, or pasted context>.\n"
        "Start with intake and state lookup. Use shallow specialist handoffs. "
        "If specialist handoff cannot actually run, stop with `target-team execution blocked`, explain the reason, and give recovery steps; do not continue as sequential or single-agent simulation. "
        "Do not let the entry agent approve its own specialist outputs."
    )
    session_fanout_prompt = (
        "Run this registered-but-not-smoke-tested Skill2Team target package through real current-session Codex subagents.\n"
        f"Team id: {team_id}.\n"
        f"Package path: {package_dir}.\n"
        f"Entry role: `{entry}`.\n"
        "Read the package registry, generated target-agent list, agent profiles, runtime invocation contract, and team usage guide. "
        "Spawn real independent subagents for the generated specialist roles. Record `target_run_fanout_status=real_session_target_subagents`, "
        "`registered_target_team_smoke_status=pending_hot_reload_or_new_thread`, and `registered_agent_invocation_verified=false`. "
        "Do not describe this as registered target-team execution, and do not continue as sequential or single-agent simulation."
    )
    diagnose_prompt = (
        "Start Skill2Team.\n"
        "Route: source-to-team.\n"
        "Delivery: package.\n"
        "Execution path: direct-skill.\n"
        "Target runtime: codex.\n"
        "Model invocation policy: use OpenAI Codex; do not call direct model APIs.\n"
        f"Team id: {team_id}.\n"
        "Post-package Codex action: diagnose why the registered Codex team is not runnable. Check .codex/config.toml [features] multi_agent and enable_fanout, "
        "each [agents.<id>] config_file entry, the installed TOML files, whether the current thread was started after those files were installed, and the runtime transcript for entry/specialist handoff. "
        "Until this is fixed, the entry agent must return target-team execution blocked instead of sequential or single-agent simulation."
    )
    return {
        "next_if_smoke_not_passed": smoke_prompt,
        "next_if_smoke_passed": use_prompt,
        "next_if_same_thread_agent_types_unavailable": session_fanout_prompt,
        "diagnose_runnable_blocker": diagnose_prompt,
        "recommended_next": use_prompt if runtime_smoke_test_passed else smoke_prompt,
    }


def remove_codex_agent_config(codex_root: Path, agent_names: list[str]) -> None:
    config_path = codex_root / CONFIG_PATH
    if not agent_names or not config_path.exists():
        return
    text = config_path.read_text(encoding="utf-8")
    updated = remove_agent_config_blocks(text, set(agent_names))
    if updated != text:
        config_path.write_text(updated, encoding="utf-8")


def unregister(codex_root: Path, team_id: str, *, force_delete_foreign: bool = False) -> list[str]:
    removed: list[str] = []
    registry = old_registry_path(codex_root, team_id)
    config_agent_names: list[str] = []
    allowed_roots = [
        (codex_root / AGENTS_DIR).resolve(),
        (codex_root / REGISTRY_DIR).resolve(),
    ]

    files: list[Path] = []
    if registry.exists():
        data = read_json(registry)
        for rel in data.get("registered_files", []):
            files.append(codex_root / rel)
            if Path(rel).suffix == ".toml":
                config_agent_names.append(Path(rel).stem)
        files.append(registry)
    else:
        # Conservative fallback: exact marker scan only.
        for p in (codex_root / AGENTS_DIR).glob("*.toml"):
            if has_matching_marker(p, team_id):
                files.append(p)
                config_agent_names.append(p.stem)

    remove_codex_agent_config(codex_root, config_agent_names)

    for path in sorted(set(files), key=lambda p: str(p)):
        resolved = path.resolve()
        if not any(within(resolved, root) for root in allowed_roots):
            raise SystemExit(f"Refusing to delete outside Codex agent registry roots: {path}")
        if not path.exists():
            continue
        if path.suffix == ".toml" and not force_delete_foreign and not has_matching_marker(path, team_id):
            print(f"skip foreign or unmarked agent file: {path}", file=sys.stderr)
            continue
        path.unlink()
        removed.append(str(path.relative_to(codex_root)).replace("\\", "/"))
    return removed


def with_markers(text: str, team_id: str, entry_agent: str) -> str:
    cleaned = strip_s2t_agent_metadata(text)
    prefix = "\n".join(
        [
            f'# managed_by = "{MANAGED_BY}"',
            f'# s2t_team_id = "{team_id}"',
            f'# s2t_entry_agent = "{entry_agent}"',
        ]
    )
    return prefix + "\n" + cleaned


def register(package_dir: Path, codex_root: Path, *, replace: bool = True, force_regenerate: bool = False, runtime_smoke_test_passed: bool = False) -> dict[str, Any]:
    registry = package_registry(package_dir)
    if registry.get("managed_by") != MANAGED_BY:
        raise SystemExit("Package registry is not managed_by=skill2team")
    if registry.get("target_runtime") not in {None, "codex"}:
        raise SystemExit(f"Package target_runtime is not codex: {registry.get('target_runtime')}")

    readiness_blockers = validate_register_ready_package(package_dir, registry)
    if readiness_blockers:
        raise SystemExit(
            "Package is not ready to support register-time hard runtime requirements:\n"
            + "\n".join(f"- {b}" for b in readiness_blockers)
        )

    team_id = slug(str(registry.get("team_id") or package_dir.name))
    entry = slug(str(registry.get("entry_agent_id") or f"s2t-{team_id}-entry"))
    is_meta_team = registry.get("team_kind") == "meta" and team_id == "s2t-meta"
    manifest_path = old_registry_path(codex_root, team_id)

    if is_meta_team and manifest_path.exists():
        existing = read_json(manifest_path)
        if same_meta_contract(existing, registry) and usable_registration(codex_root, existing) and not force_regenerate:
            return {
                "status": "already_registered",
                "team_id": team_id,
                "entry_agent_id": str(existing.get("entry_agent_id") or entry),
                "manifest_path": str(manifest_path),
                "skill2team_version": existing.get("skill2team_version"),
                "meta_team_contract_version": existing.get("meta_team_contract_version"),
                "meta_team_signature": existing.get("meta_team_signature"),
                "registered_files": existing.get("registered_files", []),
                "removed_files": [],
                "next_use_prompt_templates": existing.get("next_use_prompt_templates") or registration_next_prompt_templates(team_id, str(existing.get("entry_agent_id") or entry), package_dir, True),
                "reason": "same Skill2Team meta-team version and signature already registered",
            }
        if not force_regenerate and existing.get("registration_status") == "registered":
            raise SystemExit(
                "Existing s2t-meta registration has a different version/signature. "
                "Refusing to delete it without explicit --force-regenerate."
            )

    removed: list[str] = []
    if replace or force_regenerate:
        removed = unregister(codex_root, team_id)

    target_agents = codex_root / AGENTS_DIR
    target_agents.mkdir(parents=True, exist_ok=True)

    registered_files: list[str] = []
    for agent in registry.get("agents", []):
        artifact_rel = Path(str(agent.get("artifact_path") or ""))
        source = package_dir / artifact_rel
        if not source.exists():
            source = package_dir / ".codex" / "agents" / f"{agent.get('agent_id')}.toml"
        if not source.exists():
            raise SystemExit(f"Missing agent artifact for {agent.get('agent_id')}: {artifact_rel}")
        if source.suffix != ".toml":
            raise SystemExit(f"Codex agent artifact must be TOML: {source}")
        destination = target_agents / source.name
        text = source.read_text(encoding="utf-8-sig")
        destination.write_text(with_markers(text, team_id, entry), encoding="utf-8")
        registered_files.append(str(destination.relative_to(codex_root)).replace("\\", "/"))

    runtime_config_update = merge_codex_agent_config(codex_root, registered_files)
    next_templates = registration_next_prompt_templates(team_id, entry, package_dir, runtime_smoke_test_passed)

    manifest = dict(registry)
    runtime_invocation_policy = dict(manifest.get("runtime_invocation_policy") or {})
    runtime_smoke_test_status = "passed" if runtime_smoke_test_passed else "required_not_run_by_helper"
    registered_target_team_smoke_status = "passed" if runtime_smoke_test_passed else "pending_hot_reload_or_new_thread"
    runtime_invocation_policy.update(
        {
            "target_team_registration_status": "registered",
            "entry_agent_runnable": bool(runtime_smoke_test_passed),
            "registered_entry_agent_prompt_allowed": bool(runtime_smoke_test_passed),
            "registered_target_team_smoke_status": registered_target_team_smoke_status,
            "registered_agent_invocation_verified": bool(runtime_smoke_test_passed),
            "target_run_fanout_status": "not_started",
            "allowed_current_session_target_fanout_status": "real_session_target_subagents",
            "target_team_execution_guard_policy": target_team_execution_guard_manifest(entry),
            "registered_entry_agent_prompt_allowed_when": (
                "runtime smoke-test evidence recorded"
                if runtime_smoke_test_passed
                else "after entry invocation and specialist handoff smoke tests pass"
            ),
            "current_task_execution_mode": (
                "registered_entry_agent_available"
                if runtime_smoke_test_passed
                else "registered_files_installed_but_runtime_smoke_test_required"
            ),
            "runtime_smoke_test_status": runtime_smoke_test_status,
        }
    )
    manifest.update(
        {
            "schema_version": 1,
            "managed_by": MANAGED_BY,
            "team_id": team_id,
            "target_runtime": "codex",
            "entry_agent_id": entry,
            "registration_status": "registered",
            "target_team_registration_status": "registered",
            "runtime_smoke_test_status": runtime_smoke_test_status,
            "registered_target_team_smoke_status": registered_target_team_smoke_status,
            "target_run_fanout_status": "not_started",
            "allowed_current_session_target_fanout_status": "real_session_target_subagents",
            "entry_agent_runnable": bool(runtime_smoke_test_passed),
            "registered_agent_invocation_verified": bool(runtime_smoke_test_passed),
            "target_team_execution_guard_policy": target_team_execution_guard_manifest(entry),
            "registered_files": registered_files,
            "planned_registered_files": registry.get("planned_registered_files", registered_files),
            "previous_registration_action": "replaced" if removed else "none",
            "removed_files": removed,
            "runtime_config_update": runtime_config_update,
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "package_dir": str(package_dir.resolve()),
            "runtime_invocation_policy": runtime_invocation_policy,
            "next_use_prompt_templates": next_templates,
            "target_team_runtime_status": {
                "registration_status": "registered",
                "entry_agent_id": entry,
                "entry_agent_runnable": bool(runtime_smoke_test_passed),
                "registered_agent_invocation_verified": bool(runtime_smoke_test_passed),
                "runtime_smoke_test_status": runtime_smoke_test_status,
                "registered_target_team_smoke_status": registered_target_team_smoke_status,
                "target_run_fanout_status": "not_started",
                "allowed_current_session_target_fanout_status": "real_session_target_subagents",
                "registered_files_count": len(registered_files),
                "runtime_config_update": runtime_config_update,
                "hard_requirement": "Do not claim registered runnable multi-agent execution until entry invocation and specialist handoff smoke tests pass. If registered handoff is unavailable in the active thread, real current-session target subagents may run only with target_run_fanout_status=real_session_target_subagents and registered smoke status pending. Otherwise stop with target-team execution blocked; do not run sequential or single-agent simulation.",
            },
            "artifact_hashes": {
                rel: sha256_file(codex_root / rel) for rel in registered_files
            },
        }
    )
    write_json(manifest_path, manifest)
    return {
        "status": "registered" if runtime_smoke_test_passed else "registered_pending_runtime_smoke_test",
        "team_id": team_id,
        "entry_agent_id": entry,
        "manifest_path": str(manifest_path),
        "registered_files": registered_files,
        "removed_files": removed,
        "runtime_config_update": runtime_config_update,
        "runtime_smoke_test_status": runtime_smoke_test_status,
        "registered_target_team_smoke_status": registered_target_team_smoke_status,
        "target_run_fanout_status": "not_started",
        "allowed_current_session_target_fanout_status": "real_session_target_subagents",
        "entry_agent_runnable": bool(runtime_smoke_test_passed),
        "next_use_prompt_templates": next_templates,
        "next_required_action": (
            "ready_to_invoke_registered_entry_agent"
            if runtime_smoke_test_passed
            else "run runtime smoke tests for entry invocation, specialist handoffs, review gate blocking, and state/artifact handoff before claiming registered runnable agents; if same-thread agent types are unavailable but real subagents can run, use next_if_same_thread_agent_types_unavailable"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-dir", help="Generated Skill2Team Codex package directory.")
    parser.add_argument("--codex-root", default=".", help="Codex project root that contains or will contain .codex/.")
    parser.add_argument("--team-id", help="Team id to unregister. Optional for register when package registry has team_id.")
    parser.add_argument("--unregister", action="store_true", help="Unregister a team instead of registering package agents.")
    parser.add_argument("--no-replace", action="store_true", help="Do not remove existing registration before installing.")
    parser.add_argument("--force-regenerate", action="store_true", help="For s2t-meta only: replace an existing different-version meta-team registration after manifest-scoped uninstall.")
    parser.add_argument("--force-delete-foreign", action="store_true", help="Allow deletion of old manifest-listed TOML files without Skill2Team markers.")
    parser.add_argument(
        "--runtime-smoke-test-passed",
        action="store_true",
        help="Set only after the runtime has actually invoked the entry agent, specialist handoffs, reviewer gate, and state/artifact handoff. Without this, registration is installed but not marked runnable.",
    )
    args = parser.parse_args()

    codex_root = Path(args.codex_root).resolve()
    if args.unregister:
        if not args.team_id:
            raise SystemExit("--team-id is required with --unregister")
        removed = unregister(codex_root, slug(args.team_id), force_delete_foreign=args.force_delete_foreign)
        print(json.dumps({"status": "unregistered", "team_id": slug(args.team_id), "removed_files": removed}, ensure_ascii=False, indent=2))
        return 0

    if not args.package_dir:
        raise SystemExit("--package-dir is required unless --unregister is used")
    result = register(
        Path(args.package_dir).resolve(),
        codex_root,
        replace=not args.no_replace,
        force_regenerate=args.force_regenerate,
        runtime_smoke_test_passed=args.runtime_smoke_test_passed,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
