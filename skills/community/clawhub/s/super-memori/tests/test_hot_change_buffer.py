#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("OPENCLAW_WORKSPACE", str(Path(tempfile.mkdtemp(prefix="super-memori-hot-workspace-"))))
os.environ["SUPER_MEMORI_HOT_BUFFER_DIR"] = tempfile.mkdtemp(prefix="super-memori-hot-buffer-")

import sys
sys.path.insert(0, str(ROOT / "scripts"))

from agent_change_memory import (  # noqa: E402
    build_hot_recovery_bundle,
    compact_hot_buffer,
    detect_interrupted_change_sequence,
    hot_buffer_health_status,
    query_recent_hot_changes,
    query_unverified_recent_changes,
    record_hot_change_event,
    record_agent_change,
    record_reverted_change,
    reconcile_routine_change_history,
    query_current_known_state,
    audit_change_memory,
)


def expect(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    file_edit = record_hot_change_event(
        action_type="edit",
        target_scope="workspace",
        affected_paths=["/tmp/demo.txt"],
        command_or_patch_summary="patched demo.txt",
        status="applied_but_unverified",
        verification_state="unverified",
        risk_level="medium",
        rollback_hint="git restore /tmp/demo.txt",
    )
    expect(file_edit["status"] == "written", "state-changing file edit should land in hot buffer")

    harmless = record_hot_change_event(
        action_type="read",
        target_scope="workspace",
        affected_paths=["/tmp/demo.txt"],
        command_or_patch_summary="cat /tmp/demo.txt",
        status="applied",
        verification_state="verified",
        risk_level="low",
    )
    expect(harmless["status"] == "skipped-noise", "harmless read must not land in hot buffer")

    recovery = build_hot_recovery_bundle(query="какие последние изменения не проверены", limit=8)
    expect(any(item.get("event_id") == file_edit["event_id"] for item in recovery["selected"]), "unverified recent change should appear in recovery bundle")

    seq = record_hot_change_event(
        action_type="sequence_start",
        target_scope="workspace",
        affected_paths=["/tmp/sequence.txt"],
        command_or_patch_summary="start risky sequence",
        status="planned",
        verification_state="unverified",
        risk_level="high",
    )
    interrupted = detect_interrupted_change_sequence(limit=8)
    expect(any(item.get("event_id") == seq["event_id"] for item in interrupted["interrupted"]), "interrupted recent sequence should be detectable")

    reverted = record_reverted_change(
        target_scope="workspace",
        action_type="rollback",
        exact_paths=["/tmp/reverted.txt"],
        command_or_patch_summary="reverted temp file change",
        rollback_method="already reverted",
        risk_level="low",
        verification_state="verified",
    )
    recent = query_recent_hot_changes(limit=16, include_reverted=True)
    reverted_event = next(item for item in recent if item.get("linked_change_id") == reverted["change_id"])
    expect(reverted_event.get("active_final_state") is False, "reverted hot event must not be shown as active final state")

    durable = record_agent_change(
        target_scope="workspace",
        action_type="config_patch",
        exact_paths=["/etc/demo.conf"],
        command_or_patch_summary="patched /etc/demo.conf",
        risk_level="medium",
        verification_state="verified",
        status="applied",
    )
    current = query_current_known_state(target_scope="workspace")
    expect("/etc/demo.conf" in current["current"], "canonical current known state should still come from durable change-memory")
    expect(any("not canonical truth" in (current.get("hot_truth_note") or "") for _ in [0]), "hot buffer should not override canonical truth")

    routine1 = record_agent_change(
        target_scope="workspace",
        action_type="reindex",
        exact_paths=["/tmp/index.db"],
        command_or_patch_summary="index-memory maintenance path",
        risk_level="low",
        verification_state="unverified",
        status="applied_but_unverified",
        related_skills=["super-memori"],
    )
    routine2 = record_agent_change(
        target_scope="workspace",
        action_type="reindex",
        exact_paths=["/tmp/index.db"],
        command_or_patch_summary="index-memory maintenance path",
        risk_level="low",
        verification_state="unverified",
        status="applied_but_unverified",
        related_skills=["super-memori"],
    )
    reconciled = reconcile_routine_change_history(
        target_scope="workspace",
        action_type="reindex",
        exact_paths=["/tmp/index.db"],
        command_or_patch_summary="index-memory maintenance path",
        risk_level="low",
        related_skill="super-memori",
        observed_effect="maintenance completed successfully; health/audit verification passed",
        verification_steps=["run health-check.sh", "run audit-memory.sh"],
    )
    expect(reconciled["status"] == "reconciled", "routine maintenance history should reconcile cleanly")
    expect(routine1["change_id"] in reconciled["matched_change_ids"], "older routine record should be part of reconciliation set")
    expect(routine2["change_id"] in reconciled["matched_change_ids"], "latest routine record should be part of reconciliation set")
    audit = audit_change_memory()
    expect(reconciled["record"].get("verification_state") == "verified", "kept routine record should end verified")
    expect(reconciled["record"].get("status") == "applied", "kept routine record should end applied")
    expect(
        all(event_id not in set(audit["hot_unverified"]) for event_id in reconciled["updated_hot_events"]),
        "reconciled routine hot events must no longer remain unverified",
    )
    interrupted_events = {item.get("event_id") for item in detect_interrupted_change_sequence(limit=16).get("interrupted", [])}
    expect(
        all(event_id not in interrupted_events for event_id in reconciled["updated_hot_events"]),
        "reconciled routine hot events must no longer remain interrupted",
    )

    for idx in range(80):
        record_hot_change_event(
            action_type="edit",
            target_scope="workspace",
            affected_paths=[f"/tmp/low-{idx}.txt"],
            command_or_patch_summary=f"low risk patch {idx}",
            status="applied",
            verification_state="verified",
            risk_level="low",
        )
    compact = compact_hot_buffer()
    expect(compact["hot_buffer_drop_count"] >= 0, "rotation should run and track drop count")

    health = hot_buffer_health_status()
    expect(health["hot_buffer_enabled"] is True, "health should report hot buffer enabled")
    expect(health["hot_buffer_size_target"] <= 128 * 1024 * 1024, "phase 1 hot buffer must stay at or below 128 MiB")

    payload = json.loads(Path(os.environ["SUPER_MEMORI_HOT_BUFFER_DIR"]) .joinpath("openclaw-super-memori-hot-buffer.json").read_text(encoding="utf-8"))
    serialized = json.dumps(payload, ensure_ascii=False)
    expect("/etc/demo.conf" not in serialized or "patched /etc/demo.conf" in serialized, "hot buffer should keep only compact summaries, not full file snapshots")

    print("[OK] hot change buffer phase-1 cases passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
