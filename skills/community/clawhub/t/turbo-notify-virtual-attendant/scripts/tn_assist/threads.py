"""Where each conversation's lines live."""

from __future__ import annotations

from pathlib import Path

from tn_assist.paths import ContactKey, Workspace


def thread_path(ws: Workspace, kind: str, contact: str | None) -> Path:
    """The transcript file for a work-item kind and the person behind it."""
    if kind == "contact":
        assert contact is not None
        return ws.contact_dir(ContactKey.parse(contact)) / "transcript.jsonl"
    if kind == "admin":
        assert contact is not None
        return ws.path("threads", "admin", ContactKey.parse(contact) + ".jsonl")
    if kind == "attendant":
        return ws.path("threads", "attendant", "self.jsonl")
    raise ValueError(f"no thread for kind {kind!r}")
