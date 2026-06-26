from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
import json
import math
import time
from typing import Any, Callable

from .analysis import get_api_usage_summary
from .db import connect, prune_api_request_events
from .documents import ensure_current_ticket_materialization, get_ticket_document_materialization_status
from .enrichment import enrich_priority_ticket_details
from .ingest import sync_cold_closed_audit, sync_hot_open_tickets, sync_warm_closed_tickets
from .observability import generate_runtime_status_artifacts
from .paths import ensure_path_layout
from .public_artifacts import generate_public_snapshot
from .settings import Settings, load_settings
from .sync_state import get_json_state, set_json_state
from .vector_index import build_vector_index, get_vector_index_status
from .watch import watch_new_tickets


@dataclass
class TaskSpec:
    name: str
    every_seconds: int
    runner: Callable[[Settings], Any]
    budget_class: str = "core"


@dataclass(frozen=True)
class BudgetPlan:
    mode: str
    reserve_requests: int
    spare_requests: int
    open_ticket_count: int
    bootstrap_complete: bool
    cold_pages_per_run: int
    enrichment_limit: int
    cold_every_seconds: int
    enrichment_every_seconds: int
    allow_important: bool
    allow_deferrable: bool


@dataclass(frozen=True)
class ColdBootstrapStatus:
    total_tickets: int
    closed_tickets: int
    detailed_closed_tickets: int
    remaining_closed_without_detail: int
    detail_coverage_ratio: float
    completed_cycles: int
    bootstrap_complete: bool
    bootstrap_started_at: str | None
    bootstrap_completed_at: str | None
    last_progress_at: str | None


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _load_state() -> dict[str, Any]:
    paths = ensure_path_layout()
    if not paths.service_state_file.exists():
        return {"started_at": _now_iso(), "tasks": {}}
    return json.loads(paths.service_state_file.read_text())


def _save_state(state: dict[str, Any]) -> None:
    paths = ensure_path_layout()
    paths.service_state_file.write_text(json.dumps(state, indent=2, sort_keys=True))


def _append_log(message: str) -> None:
    paths = ensure_path_layout()
    with paths.service_log.open("a", encoding="utf-8") as f:
        f.write(f"[{_now_iso()}] {message}\n")


def _get_cold_bootstrap_status(settings: Settings) -> ColdBootstrapStatus:
    with connect(settings.db_path) as conn:
        counts = conn.execute(
            """
            SELECT
                COUNT(*) AS total_tickets,
                SUM(CASE WHEN status = 'Closed' THEN 1 ELSE 0 END) AS closed_tickets,
                SUM(CASE WHEN status = 'Closed' AND td.ticket_id IS NOT NULL THEN 1 ELSE 0 END) AS detailed_closed_tickets
            FROM tickets t
            LEFT JOIN ticket_details td ON td.ticket_id = t.id
            """
        ).fetchone()
    cold_state = get_json_state(settings.db_path, "sync.cold_closed.last_state", default={}) or {}
    bootstrap_state = get_json_state(settings.db_path, "service.cold_bootstrap", default={}) or {}
    closed_tickets = int(counts["closed_tickets"] or 0)
    detailed_closed_tickets = int(counts["detailed_closed_tickets"] or 0)
    remaining = max(0, closed_tickets - detailed_closed_tickets)
    completed_cycles = int(cold_state.get("completed_cycles", 0) or 0)
    bootstrap_complete = bool(bootstrap_state.get("bootstrap_complete"))
    return ColdBootstrapStatus(
        total_tickets=int(counts["total_tickets"] or 0),
        closed_tickets=closed_tickets,
        detailed_closed_tickets=detailed_closed_tickets,
        remaining_closed_without_detail=remaining,
        detail_coverage_ratio=round((detailed_closed_tickets / closed_tickets), 4) if closed_tickets else 1.0,
        completed_cycles=completed_cycles,
        bootstrap_complete=bootstrap_complete,
        bootstrap_started_at=bootstrap_state.get("bootstrap_started_at"),
        bootstrap_completed_at=bootstrap_state.get("bootstrap_completed_at"),
        last_progress_at=bootstrap_state.get("last_progress_at"),
    )


def _update_cold_bootstrap_status(settings: Settings) -> ColdBootstrapStatus:
    status = _get_cold_bootstrap_status(settings)
    now = _now_iso()
    state = get_json_state(settings.db_path, "service.cold_bootstrap", default={}) or {}
    changed = False
    if status.closed_tickets > 0 and not state.get("bootstrap_started_at"):
        state["bootstrap_started_at"] = now
        changed = True
    if status.remaining_closed_without_detail < int(state.get("remaining_closed_without_detail", status.closed_tickets) or status.closed_tickets):
        state["last_progress_at"] = now
        changed = True
    state["remaining_closed_without_detail"] = status.remaining_closed_without_detail
    state["detail_coverage_ratio"] = status.detail_coverage_ratio
    state["completed_cycles"] = status.completed_cycles
    if status.completed_cycles >= 1 and status.remaining_closed_without_detail == 0 and not state.get("bootstrap_complete"):
        state["bootstrap_complete"] = True
        state["bootstrap_completed_at"] = now
        changed = True
    if changed:
        set_json_state(settings.db_path, "service.cold_bootstrap", state)
    return _get_cold_bootstrap_status(settings)


def _estimate_reserved_requests(settings: Settings) -> int:
    hot_runs_per_hour = max(1.0, 3600 / max(1, settings.service_hot_open_every_seconds))
    warm_runs_per_hour = 3600 / max(1, settings.service_warm_closed_every_seconds)
    hot_requests_per_run = max(2, settings.hot_open_pages * 2)
    warm_requests_per_run = max(1, settings.warm_closed_pages)
    reserve = int(math.ceil(hot_runs_per_hour * hot_requests_per_run + warm_runs_per_hour * warm_requests_per_run + 30))
    return max(60, reserve)


def _build_budget_plan(settings: Settings, usage: dict[str, Any], bootstrap: ColdBootstrapStatus) -> BudgetPlan:
    remaining = int(usage.get("remaining_hourly_budget", settings.api_hourly_limit))
    open_count = int((get_json_state(settings.db_path, "watch.last_state", default={}) or {}).get("observed_open_ticket_count", 0) or 0)
    reserve = _estimate_reserved_requests(settings)
    spare = max(0, remaining - reserve)

    if not bootstrap.bootstrap_complete:
        if spare >= 250 and open_count <= 15:
            mode = "bootstrap_aggressive"
            cold_every = settings.service_cold_bootstrap_every_seconds
            enrich_every = settings.service_enrichment_bootstrap_every_seconds
            cold_pages = max(settings.cold_closed_bootstrap_pages_per_run, settings.cold_closed_pages_per_run)
            enrich_limit = max(settings.service_enrichment_bootstrap_limit, settings.service_enrichment_limit)
            allow_deferrable = True
        elif spare >= 120:
            mode = "bootstrap_balanced"
            cold_every = max(settings.service_cold_bootstrap_every_seconds * 2, 1800)
            enrich_every = max(settings.service_enrichment_bootstrap_every_seconds * 2, 1800)
            cold_pages = max(settings.cold_closed_pages_per_run, min(settings.cold_closed_bootstrap_pages_per_run, 6))
            enrich_limit = max(settings.service_enrichment_limit, min(settings.service_enrichment_bootstrap_limit, 120))
            allow_deferrable = True
        else:
            mode = "bootstrap_protected"
            cold_every = settings.service_cold_closed_every_seconds
            enrich_every = settings.service_enrichment_every_seconds
            cold_pages = settings.cold_closed_pages_per_run
            enrich_limit = settings.service_enrichment_limit
            allow_deferrable = spare >= 40
    else:
        if spare >= 180 and open_count <= 15:
            mode = "steady_opportunistic"
            cold_every = min(max(settings.service_cold_closed_every_seconds // 4, 21600), settings.service_cold_closed_every_seconds)
            enrich_every = min(max(settings.service_enrichment_every_seconds * 2, 14400), 21600)
            cold_pages = max(settings.cold_closed_pages_per_run, 3)
            enrich_limit = max(settings.service_enrichment_limit, 90)
            allow_deferrable = True
        else:
            mode = "steady_conservative"
            cold_every = settings.service_cold_closed_every_seconds
            enrich_every = max(settings.service_enrichment_every_seconds * 2, 14400)
            cold_pages = settings.cold_closed_pages_per_run
            enrich_limit = settings.service_enrichment_limit
            allow_deferrable = spare >= 25

    allow_important = remaining > max(20, reserve // 3)
    return BudgetPlan(
        mode=mode,
        reserve_requests=reserve,
        spare_requests=spare,
        open_ticket_count=open_count,
        bootstrap_complete=bootstrap.bootstrap_complete,
        cold_pages_per_run=cold_pages,
        enrichment_limit=enrich_limit,
        cold_every_seconds=int(cold_every),
        enrichment_every_seconds=int(enrich_every),
        allow_important=allow_important,
        allow_deferrable=allow_deferrable,
    )


def _effective_settings(settings: Settings, plan: BudgetPlan) -> Settings:
    return replace(
        settings,
        cold_closed_pages_per_run=plan.cold_pages_per_run,
        service_cold_closed_every_seconds=plan.cold_every_seconds,
        service_enrichment_every_seconds=plan.enrichment_every_seconds,
        service_enrichment_limit=plan.enrichment_limit,
    )


def _task_specs(settings: Settings) -> list[TaskSpec]:
    return [
        TaskSpec("hot_open", settings.service_hot_open_every_seconds, lambda s: (watch_new_tickets(s), sync_hot_open_tickets(s)), budget_class="core"),
        TaskSpec("warm_closed", settings.service_warm_closed_every_seconds, sync_warm_closed_tickets, budget_class="important"),
        TaskSpec("cold_closed", settings.service_cold_closed_every_seconds, lambda s: sync_cold_closed_audit(s, pages_per_run=s.cold_closed_pages_per_run), budget_class="deferrable"),
        TaskSpec("enrichment", settings.service_enrichment_every_seconds, lambda s: enrich_priority_ticket_details(s, limit=s.service_enrichment_limit, materialize_docs=True), budget_class="deferrable"),
        TaskSpec("retrieval_artifacts", settings.service_public_snapshot_every_seconds, lambda s: ensure_current_ticket_materialization(s.db_path), budget_class="lightweight"),
        TaskSpec("public_snapshot", settings.service_public_snapshot_every_seconds, lambda s: generate_public_snapshot(s.db_path), budget_class="lightweight"),
        TaskSpec("vector_refresh", settings.service_vector_refresh_every_seconds, lambda s: build_vector_index(s.db_path), budget_class="lightweight"),
        TaskSpec("runtime_status", settings.service_doctor_every_seconds, lambda s: generate_runtime_status_artifacts(s.db_path), budget_class="lightweight"),
        TaskSpec("doctor_marker", settings.service_doctor_every_seconds, lambda s: {"status": "ok", "checked_at": _now_iso()}, budget_class="lightweight"),
    ]


def _budget_gate(plan: BudgetPlan, spec: TaskSpec) -> tuple[bool, str | None]:
    if spec.budget_class == "important" and not plan.allow_important:
        return False, f"budget_protected mode={plan.mode} reserve={plan.reserve_requests} spare={plan.spare_requests}"
    if spec.budget_class == "deferrable" and not plan.allow_deferrable:
        return False, f"budget_protected mode={plan.mode} reserve={plan.reserve_requests} spare={plan.spare_requests}"
    return True, None


def _detect_immediate_local_repair_needs(settings: Settings) -> dict[str, str]:
    forced: dict[str, str] = {}
    materialization = get_ticket_document_materialization_status(settings.db_path)
    if materialization["needs_refresh"]:
        reason = (
            f"materialization_drift docs={materialization['document_count']}/{materialization['ticket_count']} "
            f"stale_docs={materialization['stale_docs']}"
        )
        for task_name in ("retrieval_artifacts", "public_snapshot", "vector_refresh", "runtime_status"):
            forced[task_name] = reason
        return forced

    vector_status = get_vector_index_status(settings.db_path)
    if (
        vector_status["missing_index_rows"]
        or vector_status["dangling_index_rows"]
        or vector_status["outdated_content_rows"]
    ):
        reason = (
            "vector_drift "
            f"missing={vector_status['missing_index_rows']} "
            f"dangling={vector_status['dangling_index_rows']} "
            f"outdated={vector_status['outdated_content_rows']}"
        )
        forced["vector_refresh"] = reason
        forced["runtime_status"] = reason
    return forced


def run_pending_tasks(settings: Settings | None = None) -> dict[str, Any]:
    settings = settings or load_settings()
    state = _load_state()
    tasks_state = state.setdefault("tasks", {})
    now = time.time()
    results = []

    pruned = prune_api_request_events(settings.db_path, settings.api_request_log_retention_days)
    if pruned:
        _append_log(f"api_request_events pruned={pruned}")
    usage = get_api_usage_summary(settings.db_path)
    bootstrap = _update_cold_bootstrap_status(settings)
    plan = _build_budget_plan(settings, usage, bootstrap)
    effective_settings = _effective_settings(settings, plan)
    state["api_usage_last_seen"] = usage
    state["budget_plan_last_seen"] = plan.__dict__
    state["cold_bootstrap_last_seen"] = bootstrap.__dict__
    forced_tasks = _detect_immediate_local_repair_needs(settings)

    for spec in _task_specs(effective_settings):
        task_state = tasks_state.setdefault(spec.name, {})
        last_run = float(task_state.get("last_run_epoch", 0))
        force_reason = forced_tasks.get(spec.name)
        if force_reason is None and now - last_run < spec.every_seconds:
            continue
        allowed, reason = _budget_gate(plan, spec)
        if not allowed:
            task_state.update({
                "last_skipped_at": _now_iso(),
                "last_skip_reason": reason,
            })
            results.append({"task": spec.name, "status": "skipped", "reason": reason, "forced": bool(force_reason), "force_reason": force_reason})
            _append_log(f"task={spec.name} status=skipped reason={reason}")
            continue
        try:
            result = spec.runner(effective_settings)
            task_state.update({
                "last_run_epoch": now,
                "last_status": "ok",
                "last_run_at": _now_iso(),
            })
            task_state.pop("last_error", None)
            task_state.pop("last_skip_reason", None)
            results.append({"task": spec.name, "status": "ok", "result": getattr(result, '__dict__', result), "forced": bool(force_reason), "force_reason": force_reason})
            _append_log(f"task={spec.name} status=ok mode={plan.mode}")
            usage = get_api_usage_summary(settings.db_path)
            bootstrap = _update_cold_bootstrap_status(settings)
            plan = _build_budget_plan(settings, usage, bootstrap)
            effective_settings = _effective_settings(settings, plan)
            state["api_usage_last_seen"] = usage
            state["budget_plan_last_seen"] = plan.__dict__
            state["cold_bootstrap_last_seen"] = bootstrap.__dict__
        except Exception as exc:
            task_state.update({
                "last_run_epoch": now,
                "last_status": "error",
                "last_run_at": _now_iso(),
                "last_error": f"{type(exc).__name__}: {exc}",
            })
            results.append({"task": spec.name, "status": "error", "error": f"{type(exc).__name__}: {exc}", "forced": bool(force_reason), "force_reason": force_reason})
            _append_log(f"task={spec.name} status=error error={type(exc).__name__}: {exc}")
            usage = get_api_usage_summary(settings.db_path)
            bootstrap = _update_cold_bootstrap_status(settings)
            plan = _build_budget_plan(settings, usage, bootstrap)
            state["api_usage_last_seen"] = usage
            state["budget_plan_last_seen"] = plan.__dict__
            state["cold_bootstrap_last_seen"] = bootstrap.__dict__
    state["last_loop_at"] = _now_iso()
    _save_state(state)
    return {
        "status": "ok",
        "results": results,
        "state_file": str(ensure_path_layout().service_state_file),
        "api_usage": usage,
        "budget_plan": plan.__dict__,
        "cold_bootstrap": bootstrap.__dict__,
        "retention_days": settings.api_request_log_retention_days,
        "pruned_request_events": pruned,
    }


def run_service_loop() -> int:
    settings = load_settings()
    _append_log("service loop starting")
    while True:
        run_pending_tasks(settings)
        time.sleep(30)
