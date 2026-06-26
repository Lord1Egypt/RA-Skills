from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json

from .client import SherpaDeskClient
from .db import (
    finish_ingest_run,
    initialize_db,
    now_iso,
    start_ingest_run,
    upsert_accounts,
    upsert_tickets,
    upsert_technicians,
    upsert_users,
)
from .settings import Settings
from .sync_state import get_json_state, set_json_state, set_sync_state
from .time_utils import parse_sherpadesk_timestamp


@dataclass
class SeedResult:
    status: str
    message: str
    stats: dict | None = None


@dataclass
class DeltaSyncResult:
    status: str
    message: str
    stats: dict | None = None


def _missing_api_config_message() -> str:
    return (
        "Database initialized, but live SherpaDesk ingest is still blocked until a staged SherpaDesk API key exists under .SherpaMind/private/secrets/, "
        "organization/instance access is confirmed, and the real endpoint contract is verified."
    )


def _build_client(settings: Settings) -> SherpaDeskClient:
    assert settings.api_key is not None
    return SherpaDeskClient(
        api_base_url=settings.api_base_url,
        api_key=settings.api_key,
        api_user=settings.api_user,
        org_key=settings.org_key,
        instance_key=settings.instance_key,
        timeout_seconds=settings.request_timeout_seconds,
        min_interval_seconds=settings.request_min_interval_seconds,
        request_tracking_db_path=settings.db_path,
    )


def _require_live_context(settings: Settings) -> str | None:
    if not settings.api_key:
        return _missing_api_config_message()
    if not settings.org_key or not settings.instance_key:
        return (
            "API token is present, but SHERPADESK_ORG_KEY and SHERPADESK_INSTANCE_KEY are still missing. "
            "Run organization discovery first."
        )
    return None


def seed_all(settings: Settings) -> SeedResult:
    initialize_db(settings.db_path)
    error = _require_live_context(settings)
    if error:
        status = "needs_org_context" if "ORG_KEY" in error else "needs_config"
        return SeedResult(status=status, message=error)

    run_id = start_ingest_run(
        settings.db_path,
        mode="seed",
        notes=f"page_size={settings.seed_page_size}, max_pages={settings.seed_max_pages}",
    )
    try:
        client = _build_client(settings)
        synced_at = now_iso()
        accounts = client.list_paginated("accounts", page_size=settings.seed_page_size, max_pages=settings.seed_max_pages)
        upsert_accounts(settings.db_path, accounts, synced_at=synced_at)

        users = client.list_paginated("users", page_size=settings.seed_page_size, max_pages=settings.seed_max_pages)
        upsert_users(settings.db_path, users, synced_at=synced_at)

        technicians = client.list_paginated("technicians", page_size=settings.seed_page_size, max_pages=settings.seed_max_pages)
        upsert_technicians(settings.db_path, technicians, synced_at=synced_at)

        tickets = client.list_paginated("tickets", page_size=settings.seed_page_size, max_pages=settings.seed_max_pages)
        upsert_tickets(settings.db_path, tickets, synced_at=synced_at)

        stats = {
            "accounts": len(accounts),
            "users": len(users),
            "technicians": len(technicians),
            "tickets": len(tickets),
            "synced_at": synced_at,
            "page_size": settings.seed_page_size,
            "max_pages": settings.seed_max_pages,
        }
        set_sync_state(settings.db_path, "seed.last_success_at", synced_at)
        set_sync_state(settings.db_path, "seed.last_stats", json.dumps(stats, sort_keys=True))
        finish_ingest_run(settings.db_path, run_id, status="success", notes=json.dumps(stats, sort_keys=True))
        return SeedResult(
            status="ok",
            message="Initial seed completed for accounts, users, technicians, and tickets.",
            stats=stats,
        )
    except Exception as exc:
        finish_ingest_run(settings.db_path, run_id, status="failed", notes=f"{type(exc).__name__}: {exc}")
        raise


def sync_hot_open_tickets(settings: Settings) -> DeltaSyncResult:
    initialize_db(settings.db_path)
    error = _require_live_context(settings)
    if error:
        status = "needs_org_context" if "ORG_KEY" in error else "needs_config"
        return DeltaSyncResult(status=status, message=error)

    run_id = start_ingest_run(
        settings.db_path,
        mode="sync_hot_open",
        notes=f"hot_open_pages={settings.hot_open_pages}",
    )
    try:
        client = _build_client(settings)
        synced_at = now_iso()
        tickets = client.list_paginated(
            "tickets",
            page_size=settings.seed_page_size,
            max_pages=settings.hot_open_pages,
            extra_params={"status": "open"},
        )
        upsert_tickets(settings.db_path, tickets, synced_at=synced_at)
        open_ids = sorted(int(ticket["id"]) for ticket in tickets)
        set_json_state(
            settings.db_path,
            "sync.hot_open.last_state",
            {
                "last_success_at": synced_at,
                "pages": settings.hot_open_pages,
                "open_ticket_ids": open_ids,
                "open_ticket_count": len(open_ids),
            },
        )
        stats = {
            "synced_at": synced_at,
            "pages": settings.hot_open_pages,
            "open_ticket_count": len(open_ids),
        }
        finish_ingest_run(settings.db_path, run_id, status="success", notes=json.dumps(stats, sort_keys=True))
        return DeltaSyncResult(status="ok", message="Hot open-ticket sync completed.", stats=stats)
    except Exception as exc:
        finish_ingest_run(settings.db_path, run_id, status="failed", notes=f"{type(exc).__name__}: {exc}")
        raise


def sync_warm_closed_tickets(settings: Settings) -> DeltaSyncResult:
    initialize_db(settings.db_path)
    error = _require_live_context(settings)
    if error:
        status = "needs_org_context" if "ORG_KEY" in error else "needs_config"
        return DeltaSyncResult(status=status, message=error)

    run_id = start_ingest_run(
        settings.db_path,
        mode="sync_warm_closed",
        notes=f"warm_closed_pages={settings.warm_closed_pages}, warm_closed_days={settings.warm_closed_days}",
    )
    try:
        client = _build_client(settings)
        synced_at = now_iso()
        cutoff = datetime.now(timezone.utc) - timedelta(days=settings.warm_closed_days)
        closed_tickets = client.list_paginated(
            "tickets",
            page_size=settings.seed_page_size,
            max_pages=settings.warm_closed_pages,
            extra_params={"status": "closed"},
        )
        warm_tickets = []
        for ticket in closed_tickets:
            candidate_time = ticket.get("closed_time") or ticket.get("updated_time") or ticket.get("created_time")
            dt = parse_sherpadesk_timestamp(candidate_time)
            if dt is None:
                continue
            if dt >= cutoff:
                warm_tickets.append(ticket)
        upsert_tickets(settings.db_path, warm_tickets, synced_at=synced_at)
        stats = {
            "synced_at": synced_at,
            "pages": settings.warm_closed_pages,
            "warm_closed_days": settings.warm_closed_days,
            "candidate_closed_ticket_count": len(closed_tickets),
            "warm_ticket_count": len(warm_tickets),
        }
        set_json_state(settings.db_path, "sync.warm_closed.last_state", stats)
        finish_ingest_run(settings.db_path, run_id, status="success", notes=json.dumps(stats, sort_keys=True))
        return DeltaSyncResult(status="ok", message="Warm closed-ticket sync completed.", stats=stats)
    except Exception as exc:
        finish_ingest_run(settings.db_path, run_id, status="failed", notes=f"{type(exc).__name__}: {exc}")
        raise


def sync_cold_closed_audit(settings: Settings, *, pages_per_run: int | None = None) -> DeltaSyncResult:
    initialize_db(settings.db_path)
    error = _require_live_context(settings)
    if error:
        status = "needs_org_context" if "ORG_KEY" in error else "needs_config"
        return DeltaSyncResult(status=status, message=error)

    pages_per_run = pages_per_run or settings.cold_closed_pages_per_run
    run_id = start_ingest_run(
        settings.db_path,
        mode="sync_cold_closed_audit",
        notes=f"cold_closed_pages_per_run={pages_per_run}",
    )
    try:
        client = _build_client(settings)
        synced_at = now_iso()
        state = get_json_state(settings.db_path, "sync.cold_closed.last_state", default={"next_page": 0, "completed_cycles": 0}) or {"next_page": 0, "completed_cycles": 0}
        start_page = int(state.get("next_page", 0))
        completed_cycles = int(state.get("completed_cycles", 0))
        closed_pages = []
        next_page = 0
        cycle_completed = False
        for page in range(start_page, start_page + pages_per_run):
            page_rows = client.get("tickets", params={"status": "closed", "limit": settings.seed_page_size, "page": page})
            if not isinstance(page_rows, list):
                raise TypeError(f"Expected list response from tickets page {page}, got {type(page_rows).__name__}")
            closed_pages.extend(page_rows)
            if len(page_rows) < settings.seed_page_size:
                next_page = 0
                cycle_completed = True
                break
        else:
            next_page = start_page + pages_per_run
        if cycle_completed:
            completed_cycles += 1
        upsert_tickets(settings.db_path, closed_pages, synced_at=synced_at)
        stats = {
            "synced_at": synced_at,
            "start_page": start_page,
            "next_page": next_page,
            "pages_scanned": pages_per_run,
            "cold_ticket_count": len(closed_pages),
            "cycle_completed": cycle_completed,
            "completed_cycles": completed_cycles,
        }
        set_json_state(settings.db_path, "sync.cold_closed.last_state", stats)
        finish_ingest_run(settings.db_path, run_id, status="success", notes=json.dumps(stats, sort_keys=True))
        return DeltaSyncResult(status="ok", message="Cold closed-ticket audit sync completed.", stats=stats)
    except Exception as exc:
        finish_ingest_run(settings.db_path, run_id, status="failed", notes=f"{type(exc).__name__}: {exc}")
        raise


def sync_delta(settings: Settings) -> DeltaSyncResult:
    initialize_db(settings.db_path)
    error = _require_live_context(settings)
    if error:
        status = "needs_org_context" if "ORG_KEY" in error else "needs_config"
        return DeltaSyncResult(status=status, message=error)
    return DeltaSyncResult(
        status="use_explicit_lanes",
        message=(
            "SherpaMind no longer uses a generic delta-sync path. Use the explicit lane commands or the background service instead: hot open sync, warm closed sync, and cold closed audit sync."
        ),
    )
