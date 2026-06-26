#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import time
from pathlib import Path
from typing import Optional

from super_memori_common import MEMORY_DIR, WORKSPACE, now_iso, read_state, write_state, sha256_text

HOT_BUFFER_RUNTIME_DIR = Path(
    os.environ.get(
        "SUPER_MEMORI_HOT_BUFFER_DIR",
        "/dev/shm" if Path("/dev/shm").exists() else "/tmp",
    )
).expanduser()
HOT_BUFFER_PATH = HOT_BUFFER_RUNTIME_DIR / "openclaw-super-memori-hot-buffer.json"
HOT_BUFFER_DEFAULT_MIB = 32
HOT_BUFFER_MAX_MIB = 128
HOT_BUFFER_ALLOWED_MIB = {32, 64, 128}
HOT_BUFFER_RETENTION_SECONDS = 6 * 3600
HOT_BUFFER_UNVERIFIED_STALE_SECONDS = 2 * 3600
HOT_BUFFER_MAX_RECOVERY_ENTRIES = 64
HIGH_SIGNAL_ACTION_TYPES = {
    "edit",
    "create",
    "delete",
    "move",
    "config_patch",
    "service_enable",
    "service_disable",
    "service_restart",
    "package_install",
    "package_remove",
    "cleanup",
    "reindex",
    "setting_change",
    "rollback",
    "sequence_start",
    "sequence_end",
    "partially_failed_write",
}
NOISE_ACTION_TYPES = {"read", "query", "search", "list", "inspect", "status_check", "noop"}

CHANGE_DIR = MEMORY_DIR / "semantic" / "agent-change-memory"
CHANGE_LOG = CHANGE_DIR / "change-log.md"
CHANGE_INDEX = CHANGE_DIR / "change-index.md"
CHANGE_AUDIT = CHANGE_DIR / "change-audit.md"
ROLLBACK_LESSONS = CHANGE_DIR / "rollback-lessons.md"
PACKAGE_HISTORY = CHANGE_DIR / "package-history.md"
CONFIG_HISTORY = CHANGE_DIR / "config-history.md"
SERVICE_HISTORY = CHANGE_DIR / "service-history.md"

DEFAULT_SCAN_ROOTS = [str(WORKSPACE), str(Path.home())]


def _hot_buffer_target_bytes() -> int:
    raw = os.environ.get("SUPER_MEMORI_HOT_BUFFER_TARGET_MIB", str(HOT_BUFFER_DEFAULT_MIB)).strip()
    try:
        mib = int(raw)
    except Exception:
        mib = HOT_BUFFER_DEFAULT_MIB
    if mib not in HOT_BUFFER_ALLOWED_MIB:
        if mib <= 32:
            mib = 32
        elif mib <= 64:
            mib = 64
        else:
            mib = 128
    mib = min(max(mib, HOT_BUFFER_DEFAULT_MIB), HOT_BUFFER_MAX_MIB)
    return mib * 1024 * 1024


def _ensure_dir() -> None:
    CHANGE_DIR.mkdir(parents=True, exist_ok=True)
    HOT_BUFFER_RUNTIME_DIR.mkdir(parents=True, exist_ok=True)


def _truncate_summary(value: str, limit: int = 240) -> str:
    text = (value or "").strip()
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def _hot_buffer_payload() -> dict:
    _ensure_dir()
    if HOT_BUFFER_PATH.exists():
        try:
            payload = json.loads(HOT_BUFFER_PATH.read_text(encoding="utf-8"))
            if isinstance(payload, dict) and isinstance(payload.get("entries", []), list):
                payload.setdefault("drop_count", 0)
                payload.setdefault("last_seq_id", 0)
                payload.setdefault("target_size_bytes", _hot_buffer_target_bytes())
                return payload
        except Exception:
            pass
    return {
        "enabled": True,
        "target_size_bytes": _hot_buffer_target_bytes(),
        "drop_count": 0,
        "last_seq_id": 0,
        "entries": [],
        "integrity": "ok",
    }


def _write_hot_buffer(payload: dict) -> None:
    _ensure_dir()
    payload["target_size_bytes"] = _hot_buffer_target_bytes()
    tmp = HOT_BUFFER_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(HOT_BUFFER_PATH)


def _hot_buffer_size_bytes(payload: Optional[dict] = None) -> int:
    payload = payload or _hot_buffer_payload()
    return len(json.dumps(payload, ensure_ascii=False).encode("utf-8"))


def _hot_event_active_final_state(event: dict) -> bool:
    if event.get("status") == "reverted":
        return False
    if event.get("verification_state") in {"unverified", "failed", "applied_but_unverified"}:
        return False
    return True


def _hot_event_priority(event: dict) -> tuple[int, int, int]:
    verification_state = (event.get("verification_state") or "").casefold()
    risk_level = (event.get("risk_level") or "unknown").casefold()
    status = (event.get("status") or "").casefold()
    seq_id = int(event.get("seq_id") or 0)
    verification_score = 2 if verification_state in {"unverified", "failed", "applied_but_unverified"} else 0
    risk_score = {"high": 2, "medium": 1, "low": 0}.get(risk_level, 1)
    completed_score = 0 if status in {"reverted", "applied", "written", "completed", "verified"} else 1
    return (verification_score + risk_score + completed_score, seq_id, seq_id)


def _eviction_sort_key(event: dict) -> tuple[int, int, int]:
    verification_state = (event.get("verification_state") or "").casefold()
    risk_level = (event.get("risk_level") or "unknown").casefold()
    status = (event.get("status") or "").casefold()
    seq_id = int(event.get("seq_id") or 0)
    low_value = 0 if verification_state in {"verified", "written", "ok"} and risk_level == "low" and status in {"applied", "written", "completed", "verified"} else 1
    return (low_value, seq_id, seq_id)


def _recent_duplicate(payload: dict, event: dict) -> bool:
    recent = payload.get("entries", [])[-5:]
    signature = (
        event.get("action_type"),
        tuple(event.get("affected_paths", [])),
        tuple(event.get("affected_packages", [])),
        tuple(event.get("affected_services", [])),
        event.get("command_or_patch_summary"),
        event.get("status"),
    )
    for prior in recent:
        prior_sig = (
            prior.get("action_type"),
            tuple(prior.get("affected_paths", [])),
            tuple(prior.get("affected_packages", [])),
            tuple(prior.get("affected_services", [])),
            prior.get("command_or_patch_summary"),
            prior.get("status"),
        )
        if prior_sig == signature:
            return True
    return False


def _normalize_hot_entry(entry: dict, *, seq_id: int) -> dict:
    timestamp = entry.get("timestamp") or now_iso()
    return {
        "event_id": entry.get("event_id") or sha256_text(f"hot:{timestamp}:{entry.get('actor','agent')}:{entry.get('action_type','edit')}:{entry.get('target_scope','system')}:{seq_id}")[:16],
        "seq_id": seq_id,
        "timestamp": timestamp,
        "actor": entry.get("actor") or "agent",
        "task_id": entry.get("task_id") or None,
        "run_id": entry.get("run_id") or None,
        "target_scope": entry.get("target_scope") or "system",
        "action_type": entry.get("action_type") or "edit",
        "affected_paths": _normalize_paths(entry.get("affected_paths") or entry.get("exact_paths")),
        "affected_packages": _normalize_list(entry.get("affected_packages") or entry.get("package_names")),
        "affected_services": _normalize_list(entry.get("affected_services") or entry.get("services_touched")),
        "command_or_patch_summary": _truncate_summary(entry.get("command_or_patch_summary") or entry.get("why_change_was_made") or entry.get("new_value_summary") or entry.get("action_type") or ""),
        "status": entry.get("status") or "applied",
        "verification_state": entry.get("verification_state") or "unverified",
        "rollback_hint": _truncate_summary(entry.get("rollback_hint") or entry.get("rollback_method") or ""),
        "risk_level": entry.get("risk_level") or "unknown",
        "residue_risk": entry.get("residue_risk") or ("possible" if entry.get("verification_state") in {"unverified", "applied_but_unverified"} else "low"),
        "linked_change_id": entry.get("linked_change_id") or None,
        "active_final_state": False,
    }


def compact_hot_buffer() -> dict:
    payload = _hot_buffer_payload()
    target = _hot_buffer_target_bytes()
    now_ts = time.time()
    entries = []
    for event in payload.get("entries", []):
        ts = event.get("timestamp")
        try:
            age_seconds = max(0, int(now_ts - time.mktime(time.strptime(ts[:19], "%Y-%m-%dT%H:%M:%S")))) if ts else 0
        except Exception:
            age_seconds = 0
        event = dict(event)
        event["active_final_state"] = _hot_event_active_final_state(event)
        if age_seconds > HOT_BUFFER_RETENTION_SECONDS and event.get("verification_state") not in {"unverified", "failed", "applied_but_unverified"}:
            payload["drop_count"] = int(payload.get("drop_count", 0)) + 1
            continue
        entries.append(event)
    entries.sort(key=lambda item: int(item.get("seq_id") or 0))
    payload["entries"] = entries
    while _hot_buffer_size_bytes(payload) > target and payload.get("entries"):
        payload["entries"].sort(key=_eviction_sort_key)
        payload["entries"].pop(0)
        payload["drop_count"] = int(payload.get("drop_count", 0)) + 1
        payload["entries"].sort(key=lambda item: int(item.get("seq_id") or 0))
    payload["integrity"] = "ok"
    _write_hot_buffer(payload)
    return hot_buffer_health_status()


def record_hot_change_event(**kwargs) -> dict:
    action_type = (kwargs.get("action_type") or "edit").casefold()
    status = (kwargs.get("status") or "applied").casefold()
    if action_type in NOISE_ACTION_TYPES:
        return {"status": "skipped-noise", "reason": "noise-action"}
    if action_type not in HIGH_SIGNAL_ACTION_TYPES and status not in {"failed", "reverted", "partially_applied", "applied_but_unverified", "planned", "dry-run"}:
        return {"status": "skipped-noise", "reason": "not-high-signal"}
    payload = _hot_buffer_payload()
    next_seq = int(payload.get("last_seq_id") or 0) + 1
    event = _normalize_hot_entry(kwargs, seq_id=next_seq)
    if _recent_duplicate(payload, event):
        return {"status": "duplicate", "event_id": event["event_id"], "seq_id": next_seq}
    event["active_final_state"] = _hot_event_active_final_state(event)
    payload["entries"].append(event)
    payload["last_seq_id"] = next_seq
    _write_hot_buffer(payload)
    compact_hot_buffer()
    return {"status": "written", "event_id": event["event_id"], "seq_id": next_seq, "record": event}


def update_hot_change_event_status(event_id: str, **updates) -> dict:
    payload = _hot_buffer_payload()
    for idx, event in enumerate(payload.get("entries", [])):
        if event.get("event_id") != event_id:
            continue
        updated = dict(event)
        for key in [
            "status",
            "verification_state",
            "rollback_hint",
            "risk_level",
            "residue_risk",
            "linked_change_id",
            "command_or_patch_summary",
        ]:
            if key in updates and updates.get(key) is not None:
                updated[key] = _truncate_summary(str(updates[key])) if key in {"rollback_hint", "command_or_patch_summary"} else updates[key]
        updated["active_final_state"] = _hot_event_active_final_state(updated)
        payload["entries"][idx] = updated
        _write_hot_buffer(payload)
        return {"status": "updated", "event_id": event_id, "record": updated}
    return {"status": "missing", "event_id": event_id}


def query_recent_hot_changes(*, limit: int = 10, include_reverted: bool = False) -> list[dict]:
    payload = _hot_buffer_payload()
    entries = []
    for event in reversed(payload.get("entries", [])):
        event = dict(event)
        event["active_final_state"] = _hot_event_active_final_state(event)
        if not include_reverted and event.get("status") == "reverted":
            continue
        entries.append(event)
        if len(entries) >= limit:
            break
    return entries


def query_unverified_recent_changes(*, limit: int = 10) -> list[dict]:
    out = []
    for event in query_recent_hot_changes(limit=HOT_BUFFER_MAX_RECOVERY_ENTRIES, include_reverted=True):
        if event.get("verification_state") in {"unverified", "failed", "applied_but_unverified"}:
            out.append(event)
        if len(out) >= limit:
            break
    return out


def detect_interrupted_change_sequence(*, limit: int = 10) -> dict:
    recent = query_recent_hot_changes(limit=HOT_BUFFER_MAX_RECOVERY_ENTRIES, include_reverted=True)
    interrupted = []
    for event in recent:
        status = (event.get("status") or "").casefold()
        verification_state = (event.get("verification_state") or "").casefold()
        action_type = (event.get("action_type") or "").casefold()
        if action_type == "sequence_start" or status in {"planned", "partially_applied", "failed", "applied_but_unverified", "dry-run"} or verification_state in {"unverified", "failed", "applied_but_unverified"}:
            interrupted.append(event)
        if len(interrupted) >= limit:
            break
    return {"status": "warn" if interrupted else "ok", "interrupted": interrupted}


def build_hot_recovery_bundle(*, query: str | None = None, limit: int = 8) -> dict:
    recent = query_recent_hot_changes(limit=limit, include_reverted=True)
    unverified = query_unverified_recent_changes(limit=limit)
    interrupted = detect_interrupted_change_sequence(limit=limit)
    query_lc = (query or "").casefold()
    selected = recent
    if any(token in query_lc for token in ["не заверш", "unfinished", "interrupted", "непровер", "unverified"]):
        selected = unverified or interrupted.get("interrupted", [])
    elif any(token in query_lc for token in ["только что", "недавно", "recent", "just changed", "latest changes"]):
        selected = recent
    return {
        "source": "hot-change-buffer",
        "query": query,
        "recent": recent,
        "unverified": unverified,
        "interrupted": interrupted.get("interrupted", []),
        "selected": selected[:limit],
        "decision": "hot-recovery" if selected else "no-recent-hot-change",
        "hot_buffer_health": hot_buffer_health_status(),
        "truth_note": "hot buffer is not canonical truth; direct live inspection and durable change-memory remain stronger for exact current machine state",
    }


def hot_buffer_health_status() -> dict:
    payload = _hot_buffer_payload()
    size_bytes = _hot_buffer_size_bytes(payload)
    target = _hot_buffer_target_bytes()
    entries = payload.get("entries", [])
    pressure = round(size_bytes / target, 4) if target else 0.0
    integrity = "ok"
    if any(int(entry.get("seq_id") or 0) <= 0 for entry in entries):
        integrity = "warn"
    return {
        "hot_buffer_enabled": True,
        "hot_buffer_runtime_path": str(HOT_BUFFER_PATH),
        "hot_buffer_size_target": target,
        "hot_buffer_size_bytes": size_bytes,
        "hot_buffer_entries": len(entries),
        "hot_buffer_pressure": pressure,
        "hot_buffer_drop_count": int(payload.get("drop_count", 0) or 0),
        "hot_buffer_integrity": integrity,
    }


def _human_size(num_bytes: Optional[int]) -> Optional[str]:
    if num_bytes is None:
        return None
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(num_bytes)
    for unit in units:
        if size < 1024.0 or unit == units[-1]:
            return f"{size:.1f}{unit}" if unit != "B" else f"{int(size)}B"
        size /= 1024.0
    return f"{int(size)}B"


def _normalize_paths(paths: Optional[list[str]]) -> list[str]:
    return [str(Path(p).expanduser()) for p in (paths or []) if p]


def _normalize_list(values: Optional[list[str]]) -> list[str]:
    return [str(v) for v in (values or []) if v]


def _default_record(status: str, action_type: str, target_scope: str, *, actor: str = "agent") -> dict:
    return {
        "change_id": sha256_text(f"{now_iso()}:{actor}:{action_type}:{target_scope}")[:16],
        "timestamp": now_iso(),
        "actor": actor,
        "host_profile": None,
        "target_scope": target_scope,
        "action_type": action_type,
        "status": status,
        "exact_paths": [],
        "exact_files_touched": [],
        "package_names": [],
        "services_touched": [],
        "old_value_summary": "",
        "new_value_summary": "",
        "command_or_patch_summary": "",
        "why_change_was_made": "",
        "expected_effect": "",
        "observed_effect": "",
        "risk_level": "unknown",
        "rollback_possible": True,
        "rollback_method": "",
        "verification_steps": [],
        "verification_state": "unverified",
        "related_findings": [],
        "related_skills": [],
        "confidence": 0.5,
        "freshness": "current",
        "validation_state": status,
        "notes": [],
    }


def _append_jsonl(path: Path, record: dict) -> None:
    _ensure_dir()
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def _write_jsonl(path: Path, records: list[dict]) -> None:
    _ensure_dir()
    lines = [json.dumps(record, ensure_ascii=False) for record in records]
    path.write_text(("\n".join(lines) + ("\n" if lines else "")), encoding="utf-8")


def _write_markdown_index(records: list[dict]) -> None:
    lines = ["# Agent Change Index", "#tags: agent-change-memory, system-change-log, rollback, audit", ""]
    for record in records[-100:]:
        lines.extend([
            f"## {record['change_id']} — {record['action_type']} — {record['status']}",
            f"- timestamp: {record['timestamp']}",
            f"- actor: {record['actor']}",
            f"- host_profile: {record.get('host_profile')}",
            f"- target_scope: {record['target_scope']}",
            f"- exact_paths: {', '.join(record.get('exact_paths', [])) or 'none'}",
            f"- package_names: {', '.join(record.get('package_names', [])) or 'none'}",
            f"- services_touched: {', '.join(record.get('services_touched', [])) or 'none'}",
            f"- verification_state: {record.get('verification_state')}",
            f"- validation_state: {record.get('validation_state')}",
            f"- risk_level: {record.get('risk_level')}",
            "",
        ])
    CHANGE_INDEX.write_text("\n".join(lines), encoding="utf-8")


def _write_category_history(path: Path, title: str, records: list[dict], key: str) -> None:
    lines = [f"# {title}", "#tags: agent-change-memory, history, audit", ""]
    for record in records[-100:]:
        items = record.get(key) or []
        if not items:
            continue
        lines.extend([
            f"## {record['change_id']} — {record['status']} — {record['timestamp']}",
            f"- action_type: {record['action_type']}",
            f"- items: {', '.join(items)}",
            f"- why_change_was_made: {record.get('why_change_was_made', '')}",
            f"- expected_effect: {record.get('expected_effect', '')}",
            f"- observed_effect: {record.get('observed_effect', '')}",
            f"- rollback_possible: {record.get('rollback_possible')}",
            f"- verification_state: {record.get('verification_state')}",
            "",
        ])
    path.write_text("\n".join(lines), encoding="utf-8")


def _read_records() -> list[dict]:
    if not CHANGE_LOG.exists():
        return []
    records = []
    for line in CHANGE_LOG.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("{"):
            try:
                records.append(json.loads(line))
            except Exception:
                continue
    return records


def _rewrite_change_artifacts(records: list[dict]) -> None:
    _write_jsonl(CHANGE_LOG, records)
    _write_markdown_index(records)
    _write_category_history(PACKAGE_HISTORY, "Package History", records, "package_names")
    _write_category_history(CONFIG_HISTORY, "Config History", records, "exact_paths")
    _write_category_history(SERVICE_HISTORY, "Service History", records, "services_touched")
    _write_rollbacks(records)
    state = read_state()
    state["agent_change_last_updated_at"] = now_iso()
    state["agent_change_record_count"] = len(records)
    state["hot_change_buffer_last_updated_at"] = now_iso()
    write_state(state)


def _persist_record(record: dict) -> dict:
    _ensure_dir()
    state = read_state()
    record = {**_default_record(record.get("status", "planned"), record.get("action_type", "edit"), record.get("target_scope", "system"), actor=record.get("actor", "agent")), **record}
    record.setdefault("change_id", sha256_text(f"{record['timestamp']}:{record['action_type']}:{record['target_scope']}:{record.get('command_or_patch_summary','')}" )[:16])
    hot_result = record_hot_change_event(
        actor=record.get("actor"),
        task_id=record.get("task_id"),
        run_id=record.get("run_id"),
        target_scope=record.get("target_scope"),
        action_type=record.get("action_type"),
        affected_paths=record.get("exact_paths"),
        affected_packages=record.get("package_names"),
        affected_services=record.get("services_touched"),
        command_or_patch_summary=record.get("command_or_patch_summary") or record.get("why_change_was_made") or record.get("new_value_summary") or record.get("action_type"),
        status=record.get("status"),
        verification_state=record.get("verification_state"),
        rollback_hint=record.get("rollback_method"),
        risk_level=record.get("risk_level"),
        residue_risk="possible" if record.get("verification_state") in {"unverified", "applied_but_unverified", "failed"} else "low",
        linked_change_id=record.get("change_id"),
    )
    _append_jsonl(CHANGE_LOG, record)
    records = _read_records()
    _rewrite_change_artifacts(records)
    if hot_result.get("status") == "written":
        update_hot_change_event_status(hot_result["event_id"], linked_change_id=record["change_id"], verification_state=record.get("verification_state"), status=record.get("status"))
    return {"status": "written", "change_id": record["change_id"], "record": record, "hot_buffer": hot_result}


def _write_rollbacks(records: list[dict]) -> None:
    lines = ["# Rollback Lessons", "#tags: agent-change-memory, rollback, lessons", ""]
    for record in records[-100:]:
        if not record.get("rollback_possible"):
            continue
        lines.extend([
            f"## {record['change_id']} — {record['status']}",
            f"- action_type: {record['action_type']}",
            f"- rollback_method: {record.get('rollback_method', '')}",
            f"- verification_state: {record.get('verification_state')}",
            f"- risk_level: {record.get('risk_level')}",
            "",
        ])
    ROLLBACK_LESSONS.write_text("\n".join(lines), encoding="utf-8")
    audit_lines = ["# Change Audit", "#tags: agent-change-memory, audit, drift", ""]
    for record in records[-100:]:
        audit_lines.extend([
            f"## {record['change_id']} — {record['status']}",
            f"- timestamp: {record['timestamp']}",
            f"- action_type: {record['action_type']}",
            f"- status: {record['status']}",
            f"- verification_state: {record.get('verification_state')}",
            f"- freshness: {record.get('freshness')}",
            f"- confidence: {record.get('confidence')}",
            "",
        ])
    CHANGE_AUDIT.write_text("\n".join(audit_lines), encoding="utf-8")


def record_agent_change(**kwargs) -> dict:
    kwargs.setdefault("actor", "agent")
    kwargs.setdefault("status", "applied")
    kwargs.setdefault("target_scope", "system")
    kwargs.setdefault("action_type", "edit")
    kwargs.setdefault("confidence", 0.7)
    kwargs.setdefault("freshness", "current")
    kwargs.setdefault("validation_state", kwargs.get("status", "applied"))
    kwargs.setdefault("verification_state", "verified" if kwargs.get("status") == "applied" else "unverified")
    kwargs["exact_paths"] = _normalize_paths(kwargs.get("exact_paths"))
    kwargs["exact_files_touched"] = _normalize_paths(kwargs.get("exact_files_touched"))
    kwargs["package_names"] = _normalize_list(kwargs.get("package_names"))
    kwargs["services_touched"] = _normalize_list(kwargs.get("services_touched"))
    kwargs["related_findings"] = _normalize_list(kwargs.get("related_findings"))
    kwargs["related_skills"] = _normalize_list(kwargs.get("related_skills"))
    kwargs["verification_steps"] = _normalize_list(kwargs.get("verification_steps"))
    return _persist_record(kwargs)


def record_failed_change(**kwargs) -> dict:
    kwargs["status"] = "failed"
    kwargs.setdefault("verification_state", "failed")
    kwargs.setdefault("freshness", "current")
    return record_agent_change(**kwargs)


def record_reverted_change(**kwargs) -> dict:
    kwargs["status"] = "reverted"
    kwargs.setdefault("verification_state", "verified")
    kwargs.setdefault("rollback_possible", True)
    return record_agent_change(**kwargs)


def reconcile_routine_change_history(*, target_scope: str, action_type: str, exact_paths: list[str] | None = None, command_or_patch_summary: str | None = None, risk_level: str = "low", related_skill: str | None = None, observed_effect: str = "", verification_steps: list[str] | None = None) -> dict:
    normalized_paths = _normalize_paths(exact_paths)
    verification_steps = _normalize_list(verification_steps)
    records = _read_records()
    matches = []
    for idx, record in enumerate(records):
        if record.get("target_scope") != target_scope:
            continue
        if record.get("action_type") != action_type:
            continue
        if normalized_paths and _normalize_paths(record.get("exact_paths")) != normalized_paths:
            continue
        if command_or_patch_summary and (record.get("command_or_patch_summary") or "") != command_or_patch_summary:
            continue
        if risk_level and (record.get("risk_level") or "") != risk_level:
            continue
        if related_skill and related_skill not in (record.get("related_skills") or []):
            continue
        matches.append((idx, record))

    kept_record = None
    collapsed_ids = []
    if matches:
        kept_index, kept_record = matches[-1]
        collapsed_ids = [record.get("change_id") for idx, record in matches[:-1]]
        updated = dict(kept_record)
        updated["status"] = "applied"
        updated["verification_state"] = "verified"
        updated["validation_state"] = "applied"
        updated["freshness"] = "current"
        updated["confidence"] = max(float(updated.get("confidence", 0.7) or 0.7), 0.9)
        if observed_effect:
            updated["observed_effect"] = observed_effect
        if verification_steps:
            updated["verification_steps"] = verification_steps
        notes = [str(note) for note in (updated.get("notes") or []) if note]
        if collapsed_ids:
            notes = [note for note in notes if not str(note).startswith("routine-maintenance-reconciled:")]
            notes.append(f"routine-maintenance-reconciled:{len(collapsed_ids)} older record(s): {', '.join(collapsed_ids)}")
        updated["notes"] = notes
        records = [record for idx, record in enumerate(records) if idx not in {match_idx for match_idx, _ in matches[:-1]}]
        kept_index = next(i for i, record in enumerate(records) if record.get("change_id") == kept_record.get("change_id"))
        records[kept_index] = updated
        kept_record = updated
        _rewrite_change_artifacts(records)
    else:
        created = record_agent_change(
            target_scope=target_scope,
            action_type=action_type,
            exact_paths=normalized_paths,
            command_or_patch_summary=command_or_patch_summary or action_type,
            risk_level=risk_level,
            verification_state="verified",
            status="applied",
            freshness="current",
            observed_effect=observed_effect,
            verification_steps=verification_steps,
            related_skills=[related_skill] if related_skill else [],
        )
        kept_record = created.get("record", {})

    matched_ids = {record.get("change_id") for _, record in matches}
    if kept_record.get("change_id"):
        matched_ids.add(kept_record.get("change_id"))
    payload = _hot_buffer_payload()
    touched_events = []
    canonical_event_kept = False
    for event in payload.get("entries", []):
        event_match = False
        if event.get("linked_change_id") in matched_ids:
            event_match = True
        elif command_or_patch_summary and event.get("command_or_patch_summary") == command_or_patch_summary and event.get("action_type") == action_type and event.get("target_scope") == target_scope:
            if not normalized_paths or _normalize_paths(event.get("affected_paths")) == normalized_paths:
                event_match = True
        if not event_match:
            continue
        event["linked_change_id"] = kept_record.get("change_id")
        event["residue_risk"] = "low"
        if not canonical_event_kept:
            event["status"] = "applied"
            event["verification_state"] = "verified"
            event["active_final_state"] = True
            canonical_event_kept = True
        else:
            event["status"] = "reverted"
            event["verification_state"] = "verified"
            event["active_final_state"] = False
        touched_events.append(event.get("event_id"))
    _write_hot_buffer(payload)
    compact_hot_buffer()
    return {
        "status": "reconciled",
        "change_id": kept_record.get("change_id"),
        "collapsed_change_ids": collapsed_ids,
        "matched_change_ids": sorted(change_id for change_id in matched_ids if change_id),
        "updated_hot_events": [event_id for event_id in touched_events if event_id],
        "record": kept_record,
    }


def query_change_history(*, query: str | None = None, limit: int = 20, scope: str | None = None, status: str | None = None) -> list[dict]:
    q = (query or "").casefold().strip()
    if q and any(token in q for token in ["только что", "недавно", "recent", "just changed", "latest change", "latest changes"]):
        hot_recent = build_hot_recovery_bundle(query=query, limit=limit).get("selected", [])
        if hot_recent:
            return hot_recent[:limit]
    records = _read_records()
    out = []
    for record in reversed(records):
        blob = " ".join([
            record.get("change_id", ""), record.get("timestamp", ""), record.get("target_scope", ""), record.get("action_type", ""),
            record.get("status", ""), " ".join(record.get("exact_paths", [])), " ".join(record.get("exact_files_touched", [])),
            " ".join(record.get("package_names", [])), " ".join(record.get("services_touched", [])),
            record.get("old_value_summary", ""), record.get("new_value_summary", ""), record.get("why_change_was_made", ""),
        ]).casefold()
        if q and q not in blob:
            continue
        if scope and record.get("target_scope") != scope:
            continue
        if status and record.get("status") != status:
            continue
        out.append(record)
        if len(out) >= limit:
            break
    return out


def query_current_known_state(*, target_scope: str | None = None) -> dict:
    records = [r for r in _read_records() if not target_scope or r.get("target_scope") == target_scope]
    current = {}
    for record in reversed(records):
        if record.get("status") == "reverted" or record.get("verification_state") in {"unverified", "applied_but_unverified", "failed"}:
            continue
        for path in record.get("exact_paths", []):
            current[path] = record
        for pkg in record.get("package_names", []):
            current[f"pkg:{pkg}"] = record
        for svc in record.get("services_touched", []):
            current[f"svc:{svc}"] = record
    hot_bundle = build_hot_recovery_bundle(query="что только что изменилось", limit=8)
    return {
        "current": current,
        "records_considered": len(records),
        "target_scope": target_scope,
        "hot_recovery_recent": hot_bundle.get("selected", []),
        "hot_truth_note": hot_bundle.get("truth_note"),
    }


def query_package_history(package_name: str, limit: int = 20) -> list[dict]:
    q = package_name.casefold().strip()
    return [r for r in query_change_history(limit=200, query=q) if q in " ".join(r.get("package_names", [])).casefold()][:limit]


def query_service_history(service_name: str, limit: int = 20) -> list[dict]:
    q = service_name.casefold().strip()
    return [r for r in query_change_history(limit=200, query=q) if q in " ".join(r.get("services_touched", [])).casefold()][:limit]


def query_config_history(path: str, limit: int = 20) -> list[dict]:
    q = path.casefold().strip()
    return [r for r in query_change_history(limit=200, query=q) if q in " ".join(r.get("exact_paths", [])).casefold()][:limit]


def detect_conflict_with_prior_change(**kwargs) -> dict:
    paths = set(_normalize_paths(kwargs.get("exact_paths")))
    packages = set(_normalize_list(kwargs.get("package_names")))
    services = set(_normalize_list(kwargs.get("services_touched")))
    prior = query_change_history(limit=100, target_scope=kwargs.get("target_scope"))
    conflicts = []
    for record in prior:
        if record.get("status") in {"failed", "reverted"}:
            continue
        if paths.intersection(record.get("exact_paths", [])) or packages.intersection(record.get("package_names", [])) or services.intersection(record.get("services_touched", [])):
            conflicts.append({"change_id": record.get("change_id"), "status": record.get("status"), "action_type": record.get("action_type")})
    return {"conflict": bool(conflicts), "conflicts": conflicts}


def detect_repeat_action_risk(**kwargs) -> dict:
    recent = query_change_history(limit=50, query=" ".join(_normalize_paths(kwargs.get("exact_paths")) + _normalize_list(kwargs.get("package_names")) + _normalize_list(kwargs.get("services_touched"))))
    return {"repeat_risk": bool(recent), "recent_matches": recent[:5]}


def detect_unverified_change() -> list[dict]:
    durable = [r for r in _read_records() if r.get("verification_state") in {"unverified", "applied_but_unverified"} or r.get("status") in {"planned", "dry-run", "partially_applied"}]
    hot = query_unverified_recent_changes(limit=HOT_BUFFER_MAX_RECOVERY_ENTRIES)
    seen = {item.get("linked_change_id") or item.get("change_id") for item in durable}
    for event in hot:
        linked = event.get("linked_change_id")
        if linked and linked in seen:
            continue
        durable.append(event)
    return durable


def build_rollback_candidate(change_id: str) -> dict:
    for record in reversed(_read_records()):
        if record.get("change_id") == change_id:
            return {
                "change_id": change_id,
                "rollback_possible": bool(record.get("rollback_possible", True)),
                "rollback_method": record.get("rollback_method", ""),
                "risk_level": record.get("risk_level", "unknown"),
                "status": record.get("status"),
            }
    return {"change_id": change_id, "rollback_possible": False, "rollback_method": "", "risk_level": "unknown", "status": "missing"}


def build_change_recall_bundle(query: str, limit: int = 5) -> dict:
    query_lc = (query or "").casefold()
    hot_first = any(token in query_lc for token in ["только что", "недавно", "recent", "just changed", "latest changes", "не заверш", "unfinished", "не провер", "unverified"])
    hot_bundle = build_hot_recovery_bundle(query=query, limit=limit) if hot_first else None
    if hot_bundle and hot_bundle.get("selected"):
        best = hot_bundle["selected"][0]
        return {
            "query": query,
            "best_candidate": best,
            "candidates": hot_bundle["selected"],
            "confidence": 0.55,
            "adjusted_confidence": 0.55,
            "stale_penalty": 0.0,
            "evidence_basis": [item.get("linked_change_id") or item.get("event_id") for item in hot_bundle["selected"]],
            "decision": "hot-recovery",
            "no_skill_reason": None,
            "truth_note": hot_bundle.get("truth_note"),
        }
    hits = query_change_history(query=query, limit=limit)
    best = hits[0] if hits else None
    return {
        "query": query,
        "best_candidate": best,
        "candidates": hits,
        "confidence": best.get("confidence", 0.0) if isinstance(best, dict) else 0.0,
        "adjusted_confidence": best.get("confidence", 0.0) if isinstance(best, dict) else 0.0,
        "stale_penalty": 0.0,
        "evidence_basis": [item.get("change_id") or item.get("event_id") for item in hits],
        "decision": "recall" if best else "no-skill",
        "no_skill_reason": None if best else "no relevant changes",
        "truth_note": "direct live inspection remains stronger for exact current machine state",
    }


def audit_change_memory() -> dict:
    records = _read_records()
    conflicts = []
    duplicates = []
    unverified = []
    seen = set()
    for record in records:
        key = (tuple(record.get("exact_paths", [])), tuple(record.get("package_names", [])), tuple(record.get("services_touched", [])), record.get("action_type"), record.get("status"))
        if key in seen:
            duplicates.append(record.get("change_id"))
        else:
            seen.add(key)
        if record.get("verification_state") in {"unverified", "applied_but_unverified"}:
            unverified.append(record.get("change_id"))
        if record.get("status") in {"applied", "partially_applied"} and record.get("rollback_possible") is False:
            conflicts.append(record.get("change_id"))
    hot_health = hot_buffer_health_status()
    hot_unverified = query_unverified_recent_changes(limit=HOT_BUFFER_MAX_RECOVERY_ENTRIES)
    interrupted = detect_interrupted_change_sequence(limit=HOT_BUFFER_MAX_RECOVERY_ENTRIES)
    missing_durable_links = [
        event.get("event_id")
        for event in query_recent_hot_changes(limit=HOT_BUFFER_MAX_RECOVERY_ENTRIES, include_reverted=True)
        if event.get("linked_change_id") and event.get("linked_change_id") not in {record.get("change_id") for record in records}
    ]
    excessive_noise = hot_health.get("hot_buffer_pressure", 0.0) > 0.9 and hot_health.get("hot_buffer_entries", 0) > HOT_BUFFER_MAX_RECOVERY_ENTRIES // 2
    return {
        "status": "ok" if not conflicts and not interrupted.get("interrupted") and not missing_durable_links else "warn",
        "records": len(records),
        "duplicates": duplicates,
        "unverified": unverified,
        "conflicts": conflicts,
        "change_log": str(CHANGE_LOG),
        "change_index": str(CHANGE_INDEX),
        "hot_buffer": hot_health,
        "hot_unverified": [event.get("event_id") for event in hot_unverified],
        "hot_interrupted": [event.get("event_id") for event in interrupted.get("interrupted", [])],
        "hot_missing_durable_links": missing_durable_links,
        "hot_excessive_noise": excessive_noise,
    }
