"""Per-contact conversation state."""

from __future__ import annotations

import enum
from dataclasses import asdict, dataclass, field, replace
from pathlib import Path
from typing import Any

from tn_assist.paths import ContactKey, Workspace
from tn_assist.store import read_json, write_json_atomic


class ContactState(enum.Enum):
    ACTIVE = "active"
    HANDOFF = "handoff"
    PAUSED = "paused"
    DO_NOT_CONTACT = "do_not_contact"


@dataclass(frozen=True)
class ContactRecord:
    state: ContactState = ContactState.ACTIVE
    reason: str | None = None
    human_takeover: bool = False
    language: str | None = None
    since: str | None = None
    counters: dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> dict[str, Any]:
        data = asdict(self)
        data["state"] = self.state.value
        return data

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> ContactRecord:
        return cls(
            state=ContactState(data.get("state", "active")),
            reason=data.get("reason"),
            human_takeover=bool(data.get("human_takeover", False)),
            language=data.get("language"),
            since=data.get("since"),
            counters=dict(data.get("counters") or {}),
        )


def _path(ws: Workspace, key: ContactKey) -> Path:
    return ws.contact_dir(key) / "state.json"


def load_state(ws: Workspace, key: ContactKey) -> ContactRecord:
    data = read_json(_path(ws, key), None)
    return ContactRecord.from_json(data) if isinstance(data, dict) else ContactRecord()


def save_state(ws: Workspace, key: ContactKey, record: ContactRecord) -> None:
    write_json_atomic(_path(ws, key), record.to_json())


def pause_unless_opted_out(
    ws: Workspace, key: ContactKey, *, reason: str, at: str, takeover: bool = False
) -> ContactRecord:
    """Pause the assistant for a contact. An opt-out is never weakened by a pause or a takeover."""
    current = load_state(ws, key)
    if current.state is ContactState.DO_NOT_CONTACT:
        record = replace(current, human_takeover=current.human_takeover or takeover)
    else:
        record = replace(
            current,
            state=ContactState.PAUSED,
            reason=reason,
            human_takeover=current.human_takeover or takeover,
            since=at,
        )
    save_state(ws, key, record)
    return record


def mark_takeover(ws: Workspace, key: ContactKey, at: str) -> ContactRecord:
    return pause_unless_opted_out(ws, key, reason="takeover", at=at, takeover=True)
