from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .client import SherpaDeskClient
from .db import initialize_db, now_iso, upsert_tickets
from .settings import Settings
from .sync_state import set_json_state


@dataclass
class WatchResult:
    status: str
    message: str
    stats: dict[str, Any] | None = None


def _load_watch_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "known_open_ticket_ids": [],
            "last_watch_at": None,
            "open_ticket_snapshot": {},
        }
    return json.loads(path.read_text())


def _save_watch_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True))


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


def _snapshot_ticket(ticket: dict[str, Any]) -> dict[str, Any]:
    return {
        "updated_time": ticket.get("updated_time"),
        "status": ticket.get("status"),
        "is_new_user_post": ticket.get("is_new_user_post"),
        "is_new_tech_post": ticket.get("is_new_tech_post"),
        "next_step_date": ticket.get("next_step_date"),
        "subject": ticket.get("subject"),
        "account_name": ticket.get("account_name"),
    }


def watch_new_tickets(settings: Settings) -> WatchResult:
    initialize_db(settings.db_path)
    if not settings.api_key:
        return WatchResult(
            status="needs_config",
            message=(
                "Watcher is blocked until a staged SherpaDesk API key exists under .SherpaMind/private/secrets/."
            ),
        )
    if not settings.org_key or not settings.instance_key:
        return WatchResult(
            status="needs_org_context",
            message=(
                "Watcher is blocked until staged org/instance settings exist under .SherpaMind/private/config/settings.env."
            ),
        )

    client = _build_client(settings)
    open_tickets = client.list_paginated(
        "tickets",
        page_size=settings.seed_page_size,
        max_pages=settings.hot_open_pages,
        extra_params={"status": "open"},
    )
    synced_at = now_iso()
    upsert_tickets(settings.db_path, open_tickets, synced_at=synced_at)

    prior_state = _load_watch_state(settings.watch_state_path)
    prior_ids = {int(ticket_id) for ticket_id in prior_state.get("known_open_ticket_ids", [])}
    prior_snapshot = {str(k): v for k, v in prior_state.get("open_ticket_snapshot", {}).items()}
    current_ids = {int(ticket["id"]) for ticket in open_tickets}

    new_ids = sorted(current_ids - prior_ids)
    closed_or_missing_ids = sorted(prior_ids - current_ids)

    new_id_set = set(new_ids)
    changed_tickets = []
    current_snapshot = {}
    for ticket in open_tickets:
        ticket_id = str(ticket["id"])
        snap = _snapshot_ticket(ticket)
        current_snapshot[ticket_id] = snap
        if int(ticket["id"]) in new_id_set:
            continue
        if prior_snapshot.get(ticket_id) != snap:
            changed_tickets.append(
                {
                    "id": ticket.get("id"),
                    "subject": ticket.get("subject"),
                    "account_name": ticket.get("account_name"),
                    "updated_time": ticket.get("updated_time"),
                    "status": ticket.get("status"),
                    "is_new_user_post": ticket.get("is_new_user_post"),
                    "is_new_tech_post": ticket.get("is_new_tech_post"),
                    "next_step_date": ticket.get("next_step_date"),
                }
            )

    new_tickets = [ticket for ticket in open_tickets if int(ticket["id"]) in new_id_set]

    next_state = {
        "known_open_ticket_ids": sorted(current_ids),
        "last_watch_at": synced_at,
        "hot_open_pages": settings.hot_open_pages,
        "observed_open_ticket_count": len(current_ids),
        "new_ticket_ids_last_run": new_ids,
        "removed_open_ticket_ids_last_run": closed_or_missing_ids,
        "open_ticket_snapshot": current_snapshot,
    }
    _save_watch_state(settings.watch_state_path, next_state)
    set_json_state(settings.db_path, "watch.last_state", next_state)

    return WatchResult(
        status="ok",
        message="Open-ticket watcher poll completed.",
        stats={
            "watched_pages": settings.hot_open_pages,
            "observed_open_ticket_count": len(current_ids),
            "new_ticket_count": len(new_ids),
            "changed_open_ticket_count": len(changed_tickets),
            "removed_open_ticket_count": len(closed_or_missing_ids),
            "new_tickets": [
                {
                    "id": ticket.get("id"),
                    "subject": ticket.get("subject"),
                    "account_name": ticket.get("account_name"),
                    "created_time": ticket.get("created_time"),
                    "updated_time": ticket.get("updated_time"),
                    "priority_name": ticket.get("priority_name") or ticket.get("priority"),
                    "status": ticket.get("status"),
                }
                for ticket in new_tickets
            ],
            "changed_tickets": changed_tickets,
            "notify_channel_configured": bool(settings.notify_channel),
        },
    )
