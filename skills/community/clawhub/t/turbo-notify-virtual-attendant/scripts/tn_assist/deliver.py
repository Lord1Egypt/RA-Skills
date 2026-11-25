"""From abstract actions to concrete deliveries.

Each delivery is one call that trusted code makes: ``send`` (``send_text``), a normal message, with
an optional ``quote`` of an EARLIER message. The model never makes these calls. Idempotency keys
are derived from the work item, the recipient and the text, so a retry after a crash sends nothing
twice.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

from tn_assist.admins import Registry
from tn_assist.apply import Action, Draft, NotifyAdmins, NotifySelfChat, Reply, Say
from tn_assist.config import load_config
from tn_assist.i18n import Lang, t
from tn_assist.memory import Card
from tn_assist.paths import ContactKey, InvalidContactKey, Workspace
from tn_assist.store import read_json, write_json_atomic
from tn_assist.timeutil import utc_iso


def _key(seed: str, to: str, text: str) -> str:
    digest = hashlib.sha1(f"{seed}|{to}|{text}".encode()).hexdigest()
    return f"n-{digest[:32]}"


def _name(ws: Workspace, number: str) -> str:
    try:
        fact = Card.load(ws, ContactKey.parse(number)).get("name")
    except InvalidContactKey:
        return number
    return fact.value if fact else number


def expand(ws: Workspace, actions: list[Action], *, seed: str) -> list[dict[str, Any]]:
    config = load_config(ws)
    connected = str(config.get("connected_number", ""))
    admins = sorted(Registry.load(ws).numbers())
    lang: Lang = "en" if config.get("lang") == "en" else "pt"
    ops: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()

    def send(to: str, text: str) -> None:
        if (to, text) in seen:
            return
        seen.add((to, text))
        ops.append({"op": "send", "to": to, "text": text, "idempotency_key": _key(seed, to, text)})

    def to_people(text: str) -> None:
        for number in admins:
            send(number, text)
        if connected:
            send(connected, text)

    for action in actions:
        if isinstance(action, Reply):
            ops.append(
                {
                    "op": "send",
                    "to": action.contact,
                    "text": action.text,
                    "idempotency_key": action.idempotency_key,
                    "contact": action.contact,
                    "quote": action.quote_message_id,
                }
            )
        elif isinstance(action, (NotifyAdmins, NotifySelfChat)):
            to_people(action.text)
        elif isinstance(action, Say):
            send(connected if action.to == "self" else action.to, action.text)
        elif isinstance(action, Draft):
            to_people(
                t(
                    "draft_notice",
                    lang,
                    n=str(action.number),
                    name=_name(ws, action.contact),
                    number=action.contact,
                    text=action.text,
                )
            )
    return ops


# --- outbox: deliveries that must survive a crash or a failed call ----------------------------


def outbox_add(ws: Workspace, ops: list[dict[str, Any]], *, now: datetime | None = None) -> None:
    """Write each delivery down before trying it; the idempotency key makes a retry safe."""
    stamp = utc_iso(now or datetime.now(timezone.utc))
    for op in ops:
        path = ws.path("outbox", f"{op['idempotency_key']}.json")
        if not path.exists():
            write_json_atomic(path, {**op, "queued_at": stamp, "attempts": 0})


def outbox_update(ws: Workspace, op: dict[str, Any], **changes: Any) -> None:
    write_json_atomic(ws.path("outbox", f"{op['idempotency_key']}.json"), {**op, **changes})


def outbox_pending(ws: Workspace) -> list[dict[str, Any]]:
    folder = ws.path("outbox")
    if not folder.is_dir():
        return []
    rows = [read_json(p, None) for p in sorted(folder.glob("*.json"))]
    return [r for r in rows if isinstance(r, dict)]


def outbox_done(ws: Workspace, op: dict[str, Any]) -> None:
    path = ws.path("outbox", f"{op['idempotency_key']}.json")
    if path.exists():
        path.unlink()
