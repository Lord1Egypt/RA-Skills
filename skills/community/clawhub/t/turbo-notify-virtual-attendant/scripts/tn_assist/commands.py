"""The command surface: parsing, who may run what, and the confirmation of destructive ones.

Commands are plain WhatsApp messages that start with ``/``. They exist in Portuguese and English.
A message from a customer never reaches this module: routing decides that before any text is read.
"""

from __future__ import annotations

import secrets
import unicodedata
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Literal

from tn_assist.paths import Workspace
from tn_assist.store import read_json, write_json_atomic
from tn_assist.timeutil import parse_iso, utc_iso

Role = Literal["admin", "attendant"]
CONFIRMATION_TTL = timedelta(minutes=10)
_ADD = {"add", "adicionar", "novo"}
_REMOVE = {"remove", "remover", "rm", "delete", "apagar"}
_LIST = {"list", "listar", "lista"}

_ALIASES: dict[str, str] = {
    "ajuda": "help",
    "help": "help",
    "status": "status",
    "fila": "queue",
    "queue": "queue",
    "enviar": "send",
    "send": "send",
    "resumo": "digest",
    "digest": "digest",
    "retomar": "resume",
    "resume": "resume",
    "assumir": "takeover",
    "takeover": "takeover",
    "cliente": "contact",
    "contact": "contact",
    "conversa": "thread",
    "thread": "thread",
    "nota": "note",
    "note": "note",
    "clientes": "contacts",
    "contacts": "contacts",
    "admins": "admins",
    "admin": "admin",
    "ensinar": "teach",
    "teach": "teach",
    "pronto": "done",
    "done": "done",
    "publico": "public",
    "public": "public",
    "interno": "internal",
    "internal": "internal",
    "conhecimento": "kb",
    "kb": "kb",
    "fontes": "sources",
    "sources": "sources",
    "pausar": "pause",
    "pause": "pause",
    "esquecer": "forget",
    "forget": "forget",
    "modo": "mode",
    "mode": "mode",
    "politica": "policy",
    "policy": "policy",
    "idioma": "lang",
    "lang": "lang",
    "confirmar": "confirm",
    "confirm": "confirm",
}

_BOTH = frozenset({"admin", "attendant"})
_ADMIN = frozenset({"admin"})
AUTHORIZATION: dict[str, frozenset[str]] = {
    **{n: _BOTH for n in ("help", "status", "queue", "send", "digest", "resume", "takeover")},
    **{n: _BOTH for n in ("contact", "thread", "note")},
    **{
        n: _ADMIN
        for n in (
            "contacts",
            "admins",
            "admin_add",
            "admin_remove",
            "teach",
            "done",
            "public",
            "internal",
            "kb",
            "sources",
            "pause",
            "forget",
            "mode",
            "policy",
            "lang",
            "confirm",
        )
    },
}


@dataclass(frozen=True)
class Command:
    name: str
    args: tuple[str, ...]
    raw: str
    tail: str = ""

    @property
    def rest(self) -> str:
        """Everything after the first argument, with its spacing kept (a draft's new text)."""
        parts = self.tail.split(None, 1)
        return parts[1] if len(parts) > 1 else ""


def _fold(word: str) -> str:
    base = unicodedata.normalize("NFKD", word.lower())
    return "".join(ch for ch in base if not unicodedata.combining(ch))


def parse_command(text: str) -> Command | None:
    stripped = text.strip()
    if not stripped.startswith("/") or stripped.startswith("//") or len(stripped) < 2:
        return None
    head, _, tail = stripped[1:].partition(" ")
    name = _ALIASES.get(_fold(head))
    if name is None:
        return None
    tail = tail.strip()
    if name == "admin":
        sub, _, after = tail.partition(" ")
        sub_folded = _fold(sub)
        after = after.strip()
        if sub_folded in _ADD:
            return Command("admin_add", tuple(after.split()), stripped, after)
        if sub_folded in _REMOVE:
            return Command("admin_remove", tuple(after.split()), stripped, after)
        return Command("admins", (), stripped, "")
    return Command(name, tuple(tail.split()), stripped, tail)


_READ_ONLY = frozenset(
    {"help", "status", "queue", "digest", "contact", "thread", "contacts", "admins", "policy"}
)


def is_read_only(cmd: Command) -> bool:
    """Commands that change nothing. Only these may run because a model suggested them."""
    if cmd.name in _READ_ONLY:
        return True
    if cmd.name == "kb":
        return not (cmd.args and _fold(cmd.args[0]) in _REMOVE)
    return cmd.name == "sources" and not cmd.args


def authorize(cmd: Command, role: Role) -> bool:
    return role in AUTHORIZATION.get(cmd.name, frozenset())


def needs_confirmation(cmd: Command) -> bool:
    if cmd.name in ("forget", "admin_remove"):
        return True
    return cmd.name == "kb" and bool(cmd.args) and _fold(cmd.args[0]) in _REMOVE


def _pending_path(ws: Workspace) -> Path:
    return ws.path("pending-confirmations.json")


def issue_confirmation(ws: Workspace, actor: str, cmd: Command, now: datetime) -> str:
    code = f"{secrets.randbelow(10_000):04d}"
    data = read_json(_pending_path(ws), {})
    data = data if isinstance(data, dict) else {}
    data[actor] = {"code": code, "raw": cmd.raw, "expires_at": utc_iso(now + CONFIRMATION_TTL)}
    write_json_atomic(_pending_path(ws), data)
    return code


def confirm(ws: Workspace, actor: str, code: str, now: datetime) -> Command | None:
    """The command waiting for ``actor``'s confirmation, once, if the code is right and fresh."""
    data = read_json(_pending_path(ws), {})
    data = data if isinstance(data, dict) else {}
    entry = data.get(actor)
    if not isinstance(entry, dict) or entry.get("code") != code:
        return None
    if parse_iso(entry["expires_at"]) < now:
        data.pop(actor, None)
        write_json_atomic(_pending_path(ws), data)
        return None
    data.pop(actor, None)
    write_json_atomic(_pending_path(ws), data)
    return parse_command(entry["raw"])
