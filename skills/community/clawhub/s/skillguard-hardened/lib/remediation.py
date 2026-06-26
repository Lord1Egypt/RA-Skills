from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lib.discovery import ensure_directory, path_is_within, render_policy_path, resolve_workspace
from lib.policy import output_paths


def _state_path(policy: dict[str, Any]) -> Path:
    return output_paths(policy)["quarantine_dir"] / "state.json"


def _load_state(policy: dict[str, Any]) -> dict[str, Any]:
    state_path = _state_path(policy)
    if not state_path.exists():
        return {"items": []}
    with state_path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _save_state(policy: dict[str, Any], state: dict[str, Any]) -> Path:
    state_path = _state_path(policy)
    ensure_directory(state_path.parent)
    with state_path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2, ensure_ascii=False)
    return state_path


def _append_audit_log(policy: dict[str, Any], event: dict[str, Any]) -> Path:
    audit_log = output_paths(policy)["audit_log"]
    ensure_directory(audit_log.parent)
    with audit_log.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
    return audit_log


def _allowed_paths(policy: dict[str, Any]) -> list[Path]:
    workspace = resolve_workspace()
    roots = [render_policy_path(raw_root, workspace) for raw_root in policy.get("allowed_roots", [])]
    roots.append(output_paths(policy)["quarantine_dir"])
    return roots


def _assert_safe_target(path: Path, policy: dict[str, Any]) -> Path:
    resolved = path.resolve()
    for root in _allowed_paths(policy):
        if root.exists() and path_is_within(resolved, root):
            return resolved
    raise ValueError(f"Refusing to operate outside allowed roots: {resolved}")


def resolve_skill_reference(reference: str, policy: dict[str, Any]) -> Path:
    candidate = Path(reference)
    if candidate.exists():
        return _assert_safe_target(candidate, policy)

    workspace = resolve_workspace()
    for raw_root in policy.get("allowed_roots", []):
        root = render_policy_path(raw_root, workspace)
        named = root / reference
        if named.exists():
            return _assert_safe_target(named, policy)

    quarantine_root = output_paths(policy)["quarantine_dir"]
    if quarantine_root.exists():
        for child in quarantine_root.iterdir():
            if child.name == reference or child.name.endswith(f"-{reference}"):
                return _assert_safe_target(child, policy)

    raise FileNotFoundError(f"Skill reference not found: {reference}")


def quarantine_skill(skill_path: Path, policy: dict[str, Any], reason: str) -> dict[str, Any]:
    source = _assert_safe_target(skill_path, policy)
    quarantine_root = ensure_directory(output_paths(policy)["quarantine_dir"])
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    destination = quarantine_root / f"{timestamp}-{source.name}"
    counter = 1
    while destination.exists():
        counter += 1
        destination = quarantine_root / f"{timestamp}-{counter}-{source.name}"

    shutil.move(str(source), str(destination))

    state = _load_state(policy)
    entry = {
        "skill_name": source.name,
        "original_path": str(source),
        "quarantine_path": str(destination),
        "reason": reason,
        "quarantined_at": datetime.now(timezone.utc).isoformat(),
    }
    state["items"] = [item for item in state.get("items", []) if item.get("original_path") != str(source)]
    state["items"].append(entry)
    _save_state(policy, state)
    _append_audit_log(policy, {"action": "quarantine", **entry})
    return entry


def list_quarantined(policy: dict[str, Any]) -> list[dict[str, Any]]:
    return _load_state(policy).get("items", [])


def restore_skill(reference: str, policy: dict[str, Any]) -> dict[str, Any]:
    state = _load_state(policy)
    items = state.get("items", [])
    matched = None
    for item in items:
        quarantine_path = Path(item["quarantine_path"])
        if reference in {item["skill_name"], item["original_path"], str(quarantine_path), quarantine_path.name}:
            matched = item
            break
    if not matched:
        raise FileNotFoundError(f"No quarantined skill matches: {reference}")

    destination = Path(matched["original_path"]).resolve()
    allowed_destination = _assert_safe_target(destination, policy)
    ensure_directory(allowed_destination.parent)
    source = _assert_safe_target(Path(matched["quarantine_path"]), policy)
    shutil.move(str(source), str(allowed_destination))

    state["items"] = [item for item in items if item is not matched]
    _save_state(policy, state)
    event = {
        "action": "restore",
        "skill_name": matched["skill_name"],
        "original_path": matched["original_path"],
        "quarantine_path": matched["quarantine_path"],
        "restored_at": datetime.now(timezone.utc).isoformat(),
    }
    _append_audit_log(policy, event)
    return event


def delete_skill(reference: str, policy: dict[str, Any]) -> dict[str, Any]:
    target = resolve_skill_reference(reference, policy)
    if not target.exists():
        raise FileNotFoundError(f"Skill path does not exist: {target}")

    if not target.is_dir():
        raise ValueError(f"Skill target must be a directory: {target}")

    event = {
        "action": "delete",
        "path": str(target),
        "deleted_at": datetime.now(timezone.utc).isoformat(),
    }
    shutil.rmtree(target)

    state = _load_state(policy)
    state["items"] = [
        item
        for item in state.get("items", [])
        if item.get("quarantine_path") != event["path"] and item.get("original_path") != event["path"]
    ]
    _save_state(policy, state)
    _append_audit_log(policy, event)
    return event


def remediate_skill(skill_path: Path, policy: dict[str, Any], action: str, reason: str | None = None) -> dict[str, Any]:
    normalized = action.lower()
    if normalized == "quarantine":
        if not reason:
            reason = "SkillGuard remediation requested"
        return quarantine_skill(skill_path, policy, reason)
    if normalized == "delete":
        return delete_skill(str(skill_path), policy)
    raise ValueError(f"Unsupported remediation action: {action}")
