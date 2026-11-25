"""Work items waiting for a model turn.

One pending item per ``(kind, contact)``: messages that arrive while it waits are merged into it,
so a person who sends three lines in a row is answered once. A leased item belongs to one worker
until ``lease_until``; an expired lease goes back to pending (a killed runner loses nothing).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Literal, cast

from tn_assist.paths import Workspace
from tn_assist.store import read_json, write_json_atomic
from tn_assist.timeutil import parse_iso, utc_iso

Kind = Literal["contact", "admin", "attendant", "compaction"]
_HYDRATED_KINDS = ("contact", "admin", "attendant")
MAX_EVENT_IDS = 200


@dataclass(frozen=True)
class WorkItem:
    id: str
    kind: Kind
    contact: str | None
    event_ids: tuple[str, ...]
    created_at: str
    hydrated_ids: tuple[str, ...] = ()
    handled_ids: tuple[str, ...] = ()
    attempts: int = 0
    rejected: int = 0  # answers the model gave that the helper refused (not outages)
    #: Which rule the last refused answer broke, in the helper's own words (never anyone's text).
    #: The pack of the next try carries it as one line.
    refusal: str = ""

    @classmethod
    def new(
        cls, kind: Kind, contact: str | None, event_ids: tuple[str, ...], now: datetime
    ) -> WorkItem:
        digest = hashlib.sha1(f"{kind}|{contact}|{event_ids[0]}".encode()).hexdigest()[:12]
        return cls(
            id=f"{kind}-{digest}",
            kind=kind,
            contact=contact,
            event_ids=tuple(event_ids),
            created_at=utc_iso(now),
        )

    @property
    def hydrate(self) -> bool:
        if self.kind not in _HYDRATED_KINDS:
            return False
        return any(e not in self.hydrated_ids for e in self.event_ids)

    @property
    def key(self) -> str:
        return f"{self.kind}__{self.contact or 'self'}"

    def to_json(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "contact": self.contact,
            "event_ids": list(self.event_ids),
            "created_at": self.created_at,
            "hydrated_ids": list(self.hydrated_ids),
            "handled_ids": list(self.handled_ids),
            "attempts": self.attempts,
            "rejected": self.rejected,
            "refusal": self.refusal,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> WorkItem:
        return cls(
            id=data["id"],
            kind=cast(Kind, data["kind"]),
            contact=data.get("contact"),
            event_ids=tuple(data["event_ids"]),
            created_at=data["created_at"],
            hydrated_ids=tuple(data.get("hydrated_ids") or ()),
            handled_ids=tuple(data.get("handled_ids") or ()),
            attempts=int(data.get("attempts", 0)),
            rejected=int(data.get("rejected", 0)),
            refusal=str(data.get("refusal") or ""),
        )


def _pending_dir(ws: Workspace) -> Path:
    return ws.path("queue", "pending")


def _leased_dir(ws: Workspace) -> Path:
    return ws.path("queue", "leased")


def _union(first: tuple[str, ...], second: tuple[str, ...]) -> tuple[str, ...]:
    return first + tuple(e for e in second if e not in first)


def _merge(old: WorkItem, new: WorkItem) -> WorkItem:
    """``old`` holds the older messages: they stay first, and what was already done is kept."""
    ids = _union(old.event_ids, new.event_ids)
    return replace(
        old,
        event_ids=ids[-MAX_EVENT_IDS:],
        hydrated_ids=_union(old.hydrated_ids, new.hydrated_ids),
        handled_ids=_union(old.handled_ids, new.handled_ids),
        attempts=max(old.attempts, new.attempts),
        rejected=max(old.rejected, new.rejected),
        refusal=old.refusal or new.refusal,
    )  # older lines stay in the transcript


def enqueue(ws: Workspace, item: WorkItem, *, older: bool = False) -> WorkItem:
    """Add ``item`` to the pending item with the same key. ``older`` says that ``item`` holds
    messages that came BEFORE the pending one (a lease that expired), so they go first."""
    path = _pending_dir(ws) / f"{item.key}.json"
    existing = read_json(path, None)
    if isinstance(existing, dict):
        pending = WorkItem.from_json(existing)
        merged = _merge(item, pending) if older else _merge(pending, item)
    else:
        merged = item
    write_json_atomic(path, merged.to_json())
    return merged


def drop_outbox_for(ws: Workspace, contact: str) -> None:
    """Forget deliveries still queued for a customer (an opt-out or erasure came after them)."""
    folder = ws.path("outbox")
    if not folder.is_dir():
        return
    for path in folder.glob("*.json"):
        op = read_json(path, {})
        if isinstance(op, dict) and contact in (op.get("contact"), op.get("to")):
            path.unlink()


def pending_count(ws: Workspace) -> int:
    directory = _pending_dir(ws)
    return len(list(directory.glob("*.json"))) if directory.is_dir() else 0


def _leased(ws: Workspace) -> list[tuple[Any, dict[str, Any]]]:
    directory = _leased_dir(ws)
    if not directory.is_dir():
        return []
    out = []
    for path in sorted(directory.glob("*.json")):
        data = read_json(path, None)
        if isinstance(data, dict):
            out.append((path, data))
    return out


def _reclaim_expired(ws: Workspace, now: datetime) -> None:
    for path, data in _leased(ws):
        if parse_iso(data["lease_until"]) <= now:
            item = WorkItem.from_json(data["item"])
            enqueue(ws, item, older=True)
            path.unlink()


def lease_next(
    ws: Workspace, kinds: tuple[str, ...], *, ttl_s: int, now: datetime
) -> WorkItem | None:
    _reclaim_expired(ws, now)
    busy = {WorkItem.from_json(d["item"]).key for _, d in _leased(ws)}
    directory = _pending_dir(ws)
    if not directory.is_dir():
        return None
    candidates = []
    for path in directory.glob("*.json"):
        data = read_json(path, None)
        if isinstance(data, dict) and data.get("kind") in kinds:
            item = WorkItem.from_json(data)
            if item.key not in busy:
                candidates.append((item.created_at, item.id, path, item))
    if not candidates:
        return None
    candidates.sort(key=lambda c: (c[0], c[1]))
    _, _, path, item = candidates[0]
    item = replace(item, attempts=item.attempts + 1)
    lease_until = utc_iso(now + timedelta(seconds=ttl_s))
    write_json_atomic(
        _leased_dir(ws) / f"{item.id}.json", {"item": item.to_json(), "lease_until": lease_until}
    )
    path.unlink()
    return item


def mark_hydrated(ws: Workspace, item_id: str, event_id: str) -> None:
    path = _leased_dir(ws) / f"{item_id}.json"
    data = read_json(path, None)
    if not isinstance(data, dict):
        return
    item = WorkItem.from_json(data["item"])
    if event_id not in item.hydrated_ids:
        item = replace(item, hydrated_ids=item.hydrated_ids + (event_id,))
    data["item"] = item.to_json()
    write_json_atomic(path, data)


def mark_handled(ws: Workspace, item_id: str, event_id: str) -> None:
    """A console line that a command already carried out; it is never run again."""
    path = _leased_dir(ws) / f"{item_id}.json"
    data = read_json(path, None)
    if not isinstance(data, dict):
        return
    item = WorkItem.from_json(data["item"])
    if event_id not in item.handled_ids:
        item = replace(item, handled_ids=item.handled_ids + (event_id,))
    data["item"] = item.to_json()
    write_json_atomic(path, data)


def mark_rejected(ws: Workspace, item_id: str, reason: str = "") -> int:
    """The model answered and the helper refused the answer. Returns how many it has refused.

    ``reason`` is the rule the answer broke; the next pack for the item says it in one line.
    """
    path = _leased_dir(ws) / f"{item_id}.json"
    data = read_json(path, None)
    if not isinstance(data, dict):
        return 0
    item = WorkItem.from_json(data["item"])
    item = replace(item, rejected=item.rejected + 1, refusal=reason)
    data["item"] = item.to_json()
    write_json_atomic(path, data)
    return item.rejected


def get_leased(ws: Workspace, item_id: str) -> WorkItem | None:
    data = read_json(_leased_dir(ws) / f"{item_id}.json", None)
    return WorkItem.from_json(data["item"]) if isinstance(data, dict) else None


def release_for_retry(ws: Workspace, item_id: str, now: datetime, delay_s: int) -> None:
    """Keep the item leased; it comes back after ``delay_s`` (a failed attempt, not a loop)."""
    path = _leased_dir(ws) / f"{item_id}.json"
    data = read_json(path, None)
    if isinstance(data, dict):
        data["lease_until"] = utc_iso(now + timedelta(seconds=delay_s))
        write_json_atomic(path, data)


def complete(ws: Workspace, item_id: str) -> None:
    path = _leased_dir(ws) / f"{item_id}.json"
    if path.exists():
        path.unlink()
