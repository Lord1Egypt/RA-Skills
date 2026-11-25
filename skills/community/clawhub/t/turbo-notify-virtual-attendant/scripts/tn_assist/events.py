"""Event parsing and routing.

The router decides who an event is from, using structured fields only. Message text
never takes part in the decision: a stranger cannot become an administrator by what
they write. All knowledge of the wire shape lives in the three small functions
``_sender_number``, ``_recipient`` and ``_origin`` so a contract change touches one place.
"""

from __future__ import annotations

import enum
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any

from tn_assist.paths import ContactKey, InvalidContactKey

_MESSAGE_TYPES = frozenset({"message.received", "message.replied", "message.sent"})


class Route(enum.Enum):
    DROP_DUPLICATE = "drop_duplicate"
    DROP_FOREIGN_NUMBER = "drop_foreign_number"
    DROP_GROUP = "drop_group"
    DROP_OTHER = "drop_other"
    TAKEOVER = "takeover"
    ADMIN = "admin"
    ATTENDANT = "attendant"
    CONTACT = "contact"


@dataclass(frozen=True)
class Event:
    id: str
    type: str
    number_id: str
    created_at: str
    data: dict[str, Any]


@dataclass(frozen=True)
class RoutingContext:
    bound_number_id: str
    connected_number: str
    admins: frozenset[str]
    seen: Callable[[str], bool]


def parse_events(
    payload: Any, *, on_malformed: Callable[[object], None] | None = None
) -> list[Event]:
    """Parse an API page (``{"data": [...]}``) or a bare list. Malformed items are skipped."""
    items: Iterable[Any]
    if isinstance(payload, dict):
        items = payload.get("data") or []
    elif isinstance(payload, list):
        items = payload
    else:
        items = []
    events: list[Event] = []
    for item in items:
        event = _parse_one(item)
        if event is None:
            if on_malformed is not None:
                on_malformed(item)
            continue
        events.append(event)
    return events


def _parse_one(item: Any) -> Event | None:
    if not isinstance(item, dict):
        return None
    data = item.get("data")
    eid, etype = item.get("id"), item.get("type")
    if not isinstance(eid, str) or not isinstance(etype, str) or not isinstance(data, dict):
        return None
    return Event(
        id=eid,
        type=etype,
        number_id=str(item.get("number_id") or ""),
        created_at=str(item.get("created_at") or ""),
        data=data,
    )


def _origin(event: Event) -> str:
    return str(event.data.get("origin") or "")


def _recipient(event: Event) -> dict[str, Any]:
    to = event.data.get("to")
    return to if isinstance(to, dict) else {}


def _sender_number(event: Event) -> str | None:
    sender = event.data.get("from")
    number = sender.get("number") if isinstance(sender, dict) else None
    return number if isinstance(number, str) else None


def _key(raw: str | None) -> ContactKey | None:
    if not raw:
        return None
    try:
        return ContactKey.parse(raw)
    except InvalidContactKey:
        return None


def sender_key(event: Event) -> ContactKey | None:
    return _key(_sender_number(event))


def is_group(event: Event) -> bool:
    return bool(_recipient(event).get("group_id"))


def is_self_chat(event: Event, connected_number: str) -> bool:
    """A chat of the connected number with itself, typed by a person on the device."""
    if is_group(event) or _origin(event) != "native":
        return False
    connected = _key(connected_number)
    sender = sender_key(event)
    recipient = _key(_recipient(event).get("number"))
    return connected is not None and sender == connected and recipient == connected


def classify(event: Event, ctx: RoutingContext) -> Route:
    if ctx.seen(event.id):
        return Route.DROP_DUPLICATE
    if event.number_id != ctx.bound_number_id:
        return Route.DROP_FOREIGN_NUMBER
    if event.type not in _MESSAGE_TYPES:
        return Route.DROP_OTHER
    if is_group(event):
        return Route.DROP_GROUP

    connected = _key(ctx.connected_number)
    sender = sender_key(event)
    direction = str(event.data.get("direction") or "")

    if is_self_chat(event, ctx.connected_number):
        return Route.ADMIN if connected in ctx.admins else Route.ATTENDANT
    if sender is not None and sender == connected:
        # From the connected number but not the self-chat: our own sends or a person on the phone.
        if direction == "outbound" and _origin(event) == "native":
            return Route.TAKEOVER
        return Route.DROP_OTHER
    if direction == "inbound" and sender is not None:
        return Route.ADMIN if sender in ctx.admins else Route.CONTACT
    return Route.DROP_OTHER
