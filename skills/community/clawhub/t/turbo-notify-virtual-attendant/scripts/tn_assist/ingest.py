"""Ingest: persist first, think later.

Order of work for each event: transcript line, queue item, ledger entry. A crash anywhere replays
safely: the transcript write is idempotent per event id, the queue merges event ids, and only the
ledger entry marks an event as fully handled. The cursor is saved last, once the whole batch is
safe, so a lost cursor only means seeing events again.
"""

from __future__ import annotations

import json
import os
from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from tn_assist.config import admin_numbers, load_config
from tn_assist.events import (
    Event,
    Route,
    RoutingContext,
    classify,
    parse_events,
    sender_key,
)
from tn_assist.memory import Card, Fact
from tn_assist.paths import ContactKey, InvalidContactKey, Workspace
from tn_assist.queue import Kind, WorkItem, drop_outbox_for, enqueue
from tn_assist.state import mark_takeover
from tn_assist.store import (
    append_jsonl,
    append_jsonl_once,
    read_json,
    read_jsonl,
    write_json_atomic,
)
from tn_assist.threads import thread_path
from tn_assist.timeutil import parse_iso, utc_iso

GAP_ALARM = timedelta(minutes=30)
PAGE_LIMIT = 100
MAX_PAGES = 50


@dataclass
class IngestResult:
    items: list[WorkItem] = field(default_factory=list)
    dropped: dict[str, int] = field(default_factory=dict)
    new_cursor: str | None = None
    gap_alarm: bool = False
    first_foreign: bool = False


@dataclass(frozen=True)
class CollectResult:
    events: list[Event]
    newest_id: str | None
    truncated: bool = False


def collect_since(
    fetch_page: Callable[[dict[str, str]], list[Event]],
    cursor: str | None,
    limit: int = PAGE_LIMIT,
) -> CollectResult:
    """Everything newer than ``cursor``, newest first, following the platform's polling rule.

    A full page means more exist: descend with ``starting_after`` until the previous cursor is found
    or a short page ends the stream. Without a cursor nothing is returned (history is never
    replayed); the newest id is returned so the caller can prime the cursor.
    """
    params = {"limit": str(limit)}
    if cursor:
        params["ending_before"] = cursor
    page = fetch_page(params)
    if cursor is None:
        return CollectResult([], page[0].id if page else None)
    batch = list(page)
    pages = 1
    while len(page) == limit and pages < MAX_PAGES:
        page = fetch_page({"limit": str(limit), "starting_after": batch[-1].id})
        pages += 1
        found = False
        for event in page:
            if event.id == cursor:
                found = True
                break
            batch.append(event)
        if found:
            break
    truncated = len(page) == limit and pages >= MAX_PAGES
    return CollectResult(batch, batch[0].id if batch else None, truncated)


LEDGER_MAX = 50_000
LEDGER_KEEP = 20_000


def _ledger_ids(ws: Workspace) -> set[str]:
    rows = read_jsonl(ws.path("ledger.jsonl"))
    if len(rows) > LEDGER_MAX:
        rows = rows[-LEDGER_KEEP:]
        path = ws.path("ledger.jsonl")
        tmp = path.with_suffix(".tmp")
        tmp.write_text(
            "".join(json.dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8"
        )
        os.replace(tmp, path)
    return {str(row["id"]) for row in rows if "id" in row}


def _line(event: Event, role: str, direction: str) -> dict[str, Any]:
    data = event.data
    return {
        "id": event.id,
        "msg": data.get("id"),
        "at": data.get("at") or event.created_at,
        "role": role,
        "dir": direction,
        "type": data.get("content_type"),
        "preview": data.get("preview") or "",
        "text": None,
    }


def _recipient_key(event: Event) -> ContactKey | None:
    to = event.data.get("to")
    number = to.get("number") if isinstance(to, dict) else None
    try:
        return ContactKey.parse(number) if isinstance(number, str) else None
    except InvalidContactKey:
        return None


def _remember_name(ws: Workspace, key: ContactKey, event: Event, at: str) -> None:
    """The name WhatsApp shows for the customer, kept as a platform fact (people can override)."""
    sender = event.data.get("from")
    name = sender.get("name") if isinstance(sender, dict) else None
    if not isinstance(name, str) or not name.strip():
        return
    card = Card.load(ws, key)
    current = card.get("name")
    if (
        current is None
        or current.source == "inferred"
        or (current.source == "platform" and current.value != name.strip())
    ):
        card.merge([Fact("name", name, "platform", at)])
        card.save()


def _mark_gap(ws: Workspace, start: str, end: str) -> None:
    record_id = f"gap-{end}"
    append_jsonl_once(ws.path("gaps.jsonl"), {"id": record_id, "from": start, "to": end})
    contacts = ws.root / "contacts"
    if contacts.is_dir():
        for directory in contacts.iterdir():
            transcript = directory / "transcript.jsonl"
            if transcript.exists():
                append_jsonl_once(
                    transcript, {"id": record_id, "kind": "gap", "from": start, "to": end}
                )


def ingest(ws: Workspace, events: Sequence[Event], now: datetime) -> IngestResult:
    config = load_config(ws)
    ledger = _ledger_ids(ws)
    ctx = RoutingContext(
        bound_number_id=str(config.get("bound_number_id", "")),
        connected_number=str(config.get("connected_number", "")),
        admins=admin_numbers(ws),
        seen=lambda eid: eid in ledger,
    )
    result = IngestResult()
    dropped: Counter[str] = Counter()
    cursor_state = read_json(ws.path("cursor.json"), {})
    cursor_state = cursor_state if isinstance(cursor_state, dict) else {}
    now_iso = utc_iso(now)

    last_tick = cursor_state.get("last_tick_at")
    if last_tick and now - parse_iso(last_tick) > GAP_ALARM:
        result.gap_alarm = True
        _mark_gap(ws, str(last_tick), now_iso)

    grouped: dict[tuple[Kind, str | None], list[str]] = {}
    for event in reversed(list(events)):  # the API is newest first; work oldest first
        route = classify(event, ctx)
        if route is Route.DROP_DUPLICATE:
            dropped[route.value] += 1
            continue
        if route in (Route.DROP_FOREIGN_NUMBER, Route.DROP_GROUP, Route.DROP_OTHER):
            dropped[route.value] += 1
        elif route is Route.TAKEOVER:
            key = _recipient_key(event)
            if key is not None:
                append_jsonl_once(
                    thread_path(ws, "contact", key), _line(event, "attendant_native", "out")
                )
                mark_takeover(ws, key, now_iso)
                drop_outbox_for(
                    ws, str(key)
                )  # a person answered: a queued bot reply must not follow
        else:
            kind: Kind = "contact" if route is Route.CONTACT else "admin"
            who: str | None
            if route is Route.ATTENDANT:
                kind, who = "attendant", None
                append_jsonl_once(thread_path(ws, kind, None), _line(event, "attendant", "in"))
            else:
                sender = sender_key(event)
                who = str(sender) if sender is not None else None
                role = "contact" if route is Route.CONTACT else "admin"
                append_jsonl_once(thread_path(ws, kind, who), _line(event, role, "in"))
                if route is Route.CONTACT and sender is not None:
                    _remember_name(ws, sender, event, now_iso)
            grouped.setdefault((kind, who), []).append(event.id)
            result.items.append(
                enqueue(ws, WorkItem.new(kind, who, tuple(grouped[(kind, who)]), now))
            )
        append_jsonl(ws.path("ledger.jsonl"), {"id": event.id, "at": now_iso})
        ledger.add(event.id)

    # one item per (kind, contact) per call: keep the last (fully merged) version
    unique: dict[str, WorkItem] = {item.key: item for item in result.items}
    result.items = list(unique.values())

    stats = read_json(ws.path("stats.json"), {})
    stats = stats if isinstance(stats, dict) else {}
    for name, count in dropped.items():
        if name == "drop_foreign_number" and not stats.get("foreign_notified"):
            result.first_foreign = True
            stats["foreign_notified"] = True
        stats[name] = int(stats.get(name, 0)) + count
    if dropped:
        write_json_atomic(ws.path("stats.json"), stats)
    result.dropped = dict(dropped)

    newest = events[0].id if events else None
    state = {
        "last_event_id": newest or cursor_state.get("last_event_id"),
        "last_tick_at": now_iso,
    }
    if not state["last_event_id"] and cursor_state.get("primed_at"):
        state["primed_at"] = cursor_state["primed_at"]  # still waiting for the first event
    write_json_atomic(ws.path("cursor.json"), state)
    result.new_cursor = newest
    return result


def parse_and_ingest(ws: Workspace, payload: Any, now: datetime) -> IngestResult:
    return ingest(ws, parse_events(payload), now)


@dataclass(frozen=True)
class FetchPlan:
    done: bool
    params: dict[str, str]
    truncated: bool = False


def fetch_plan(
    pages: Sequence[Sequence[Event]], cursor: str | None, limit: int = PAGE_LIMIT
) -> FetchPlan:
    """What to ask the platform next, given the pages already read (newest page first).

    The same rule as :func:`collect_since`, for callers that fetch the pages themselves (an agent
    calling the ``list_events`` tool): a full page means more; stop when the previous cursor is seen
    or a short page ends the stream.
    """
    if not pages:
        if cursor is None:
            return FetchPlan(False, {"limit": "1"})
        return FetchPlan(False, {"limit": str(limit), "ending_before": cursor})
    if cursor is None:
        return FetchPlan(True, {})
    if any(event.id == cursor for page in pages for event in page):
        return FetchPlan(True, {})
    last = pages[-1]
    if len(pages) >= MAX_PAGES:
        return FetchPlan(True, {}, truncated=True)
    if len(last) < limit or not last:
        return FetchPlan(True, {})
    return FetchPlan(False, {"limit": str(limit), "starting_after": last[-1].id})
