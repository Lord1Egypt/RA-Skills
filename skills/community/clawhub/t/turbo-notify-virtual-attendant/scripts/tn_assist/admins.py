"""The administrator registry and its audit trail.

Rules the code enforces, whatever a message says:
- the first administrator comes from the configurator, never from a WhatsApp message;
- later changes come from an existing administrator;
- the last administrator cannot be removed;
- the connected number (the one attendants hold) can be registered only by the configurator and
  only after an explicit confirmation of the warning; an administrator over WhatsApp is refused.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from tn_assist.config import load_config
from tn_assist.paths import ContactKey, InvalidContactKey, Workspace
from tn_assist.store import append_jsonl, read_json, write_json_atomic
from tn_assist.timeutil import utc_iso

Via = Literal["configurator", "whatsapp"]
SCHEMA = 1


class AdminError(Exception):
    """Base class for registry refusals."""


class NotAnAdministrator(AdminError):
    """The actor is not allowed to change the registry."""


class LastAdministratorError(AdminError):
    """Removing this administrator would leave nobody."""


class ConnectedNumberNeedsConfigurator(AdminError):
    """Over WhatsApp, nobody can register the connected number."""


class ConnectedNumberNeedsConfirmation(AdminError):
    """The configurator must confirm the separation warning first."""


class Registry:
    def __init__(self, ws: Workspace, entries: list[dict[str, Any]]) -> None:
        self._ws = ws
        self._entries = entries

    @classmethod
    def load(cls, ws: Workspace) -> Registry:
        data = read_json(ws.path("admins.json"), {})
        entries = data.get("admins", []) if isinstance(data, dict) else []
        return cls(ws, [dict(e) for e in entries if isinstance(e, dict) and e.get("number")])

    def numbers(self) -> frozenset[str]:
        return frozenset(str(e["number"]) for e in self._entries)

    def is_admin(self, number: str) -> bool:
        try:
            return str(ContactKey.parse(number)) in self.numbers()
        except InvalidContactKey:
            return False

    def connected_is_admin(self) -> bool:
        connected = self._connected()
        return connected is not None and str(connected) in self.numbers()

    def _connected(self) -> ContactKey | None:
        raw = load_config(self._ws).get("connected_number")
        try:
            return ContactKey.parse(str(raw)) if raw else None
        except InvalidContactKey:
            return None

    def _save(self) -> None:
        write_json_atomic(self._ws.path("admins.json"), {"schema": SCHEMA, "admins": self._entries})

    def _audit(self, record: dict[str, Any]) -> None:
        append_jsonl(self._ws.path("audit.log"), record)

    def add(
        self,
        number: str,
        name: str | None,
        *,
        by: str,
        via: Via,
        message_id: str | None = None,
        confirmed_connected: bool = False,
        now: datetime | None = None,
    ) -> bool:
        key = ContactKey.parse(number)
        moment = utc_iso(now or datetime.now(timezone.utc))
        connected = self._connected()
        is_connected = connected is not None and key == connected
        if via == "whatsapp":
            if not self.is_admin(by):
                raise NotAnAdministrator("only an administrator can add one")
            if is_connected:
                raise ConnectedNumberNeedsConfigurator(
                    "the connected number needs the configurator"
                )
        if is_connected and not confirmed_connected:
            raise ConnectedNumberNeedsConfirmation("confirm the warning first")
        if str(key) in self.numbers():
            return False
        self._entries.append(
            {"number": str(key), "name": name, "added_at": moment, "added_by": by, "via": via}
        )
        self._save()
        record: dict[str, Any] = {
            "at": moment,
            "action": "add",
            "number": str(key),
            "by": by,
            "via": via,
            "message_id": message_id,
        }
        if is_connected:
            record["connected_number_confirmed"] = True
        self._audit(record)
        return True

    def remove(
        self,
        number: str,
        *,
        by: str,
        message_id: str | None = None,
        now: datetime | None = None,
    ) -> bool:
        key = ContactKey.parse(number)
        if by != "configurator" and not self.is_admin(by):
            raise NotAnAdministrator("only an administrator can remove one")
        if str(key) not in self.numbers():
            return False
        if len(self._entries) == 1:
            raise LastAdministratorError("the last administrator cannot be removed")
        self._entries = [e for e in self._entries if e["number"] != str(key)]
        self._save()
        self._audit(
            {
                "at": utc_iso(now or datetime.now(timezone.utc)),
                "action": "remove",
                "number": str(key),
                "by": by,
                "message_id": message_id,
            }
        )
        return True
