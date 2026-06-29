"""Compatibility regressions for task states created before reliability fields."""
from __future__ import annotations

import json
from pathlib import Path

from .helpers import assert_eq, assert_in, assert_true, json_out, run


def _write_legacy_state(root: Path, task_id: str) -> None:
    json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            task_id,
            "--goal",
            "Compatibility test for older task state",
        )
    )
    state_path = root / task_id / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.pop("queue", None)
    state.pop("delivery_intents", None)
    state.pop("reliability", None)
    owner = state.get("owner") or {}
    owner.pop("thread_id", None)
    owner.pop("topic_id", None)
    owner.pop("disabled_reason", None)
    state["owner"] = owner
    delivery = state.get("delivery") or {}
    delivery.pop("package_path", None)
    delivery.pop("notification_blocked", None)
    state["delivery"] = delivery
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def test_old_state_gets_reliability_defaults_on_status(root: Path) -> None:
    _write_legacy_state(root, "legacy-state-status")

    status = json_out(run("status", "--root", str(root), "--id", "legacy-state-status"))

    assert_in("queue", status, "status should expose queue defaults for old states")
    assert_eq(status["queue"].get("status"), "free", "old task should default to free queue state")
    assert_in(
        "delivery_intents",
        status,
        "status should expose durable delivery intent defaults for old states",
    )
    assert_true(
        isinstance(status["delivery_intents"], list),
        "delivery_intents default should be a list",
    )
    assert_in("thread_id", status["owner"], "owner should include thread_id default")
    assert_in("topic_id", status["owner"], "owner should include topic_id default")
    assert_in(
        "disabled_reason",
        status["owner"],
        "owner should include explicit disabled_reason default",
    )
    assert_in(
        "package_path",
        status["delivery"],
        "delivery should include package_path default",
    )
    assert_in(
        "reliability",
        status,
        "status should expose reliability defaults for old states",
    )
    assert_eq(
        status["reliability"].get("schema_version"),
        1,
        "old task should get reliability schema version default",
    )
    assert_eq(
        status["reliability"].get("failure_counters"),
        {},
        "old task should start with no reliability counters",
    )
    assert_eq(
        status["reliability"].get("last_events"),
        [],
        "old task should start with no reliability events",
    )

    summary = json_out(
        run("summary", "--root", str(root), "--id", "legacy-state-status", "--format", "json")
    )
    assert_eq(
        summary.get("operator_attention", {}).get("status"),
        "ok",
        "legacy state should not produce reliability attention by default",
    )
    health = json_out(
        run("health", "--root", str(root), "--id", "legacy-state-status", "--format", "json")
    )
    assert_eq(health.get("status"), "ok", "legacy state should be healthy by default")
    lease = json_out(run("begin", "--root", str(root), "--id", "legacy-state-status"))
    assert_eq(lease.get("status"), "leased", "legacy state should still lease work")


def test_old_state_without_output_contract_still_loads(root: Path) -> None:
    created = json_out(
        run(
            "create",
            "--root",
            str(root),
            "--id",
            "old-no-output-contract",
            "--goal",
            "Legacy state without output contract",
            "--skip-preflight",
        )
    )
    assert_eq(created["status"], "created", "create status")

    state_path = root / "old-no-output-contract" / "state.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.setdefault("working_memory", {}).pop("output_contract", None)
    state_path.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    summary = json_out(
        run(
            "summary",
            "--root",
            str(root),
            "--id",
            "old-no-output-contract",
            "--format",
            "json",
        )
    )
    health = json_out(
        run(
            "health",
            "--root",
            str(root),
            "--id",
            "old-no-output-contract",
            "--format",
            "json",
        )
    )

    assert_eq(summary["id"], "old-no-output-contract", "summary should load")
    assert_in(
        health["status"],
        ["ok", "repair_needed", "fresh_continuation_recommended"],
        "health should load",
    )
