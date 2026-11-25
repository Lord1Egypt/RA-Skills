"""Writing the number's knowledge base from the configurator's side."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Literal

from tn_assist.paths import PathEscapeError, Workspace

Visibility = Literal["public", "internal"]
_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*(?:/[A-Za-z0-9][A-Za-z0-9._-]*)*\.md$")
_DEFAULT_FILES = {
    "pt": {
        "tone.md": (
            "como falar com os clientes",
            "Fale de forma simpática, curta e clara. Use o idioma do cliente.\n",
        ),
        "handoff.md": (
            "quando chamar uma pessoa",
            "Quando não souber responder, ou quando o cliente pedir uma pessoa, diga que alguém "
            "da equipe vai continuar a conversa. Não invente preço, prazo ou promessa.\n",
        ),
    },
    "en": {
        "tone.md": (
            "how to talk to customers",
            "Be friendly, short and clear. Use the customer's language.\n",
        ),
        "handoff.md": (
            "when to call a person",
            "When you do not know the answer, or the customer asks for a person, say that "
            "someone on the team will continue the conversation. Do not invent a price, a "
            "deadline or a promise.\n",
        ),
    },
}


class InvalidKnowledgePath(ValueError):
    """The path is not a plain markdown file name inside the knowledge folder."""


def _index(ws: Workspace) -> Path:
    return ws.path("knowledge", "INDEX.md")


def write_knowledge(
    ws: Workspace, name: str, text: str, *, visibility: Visibility, description: str
) -> str:
    """Write ``name`` under the knowledge folder and list it in the index; returns the path."""
    if not _NAME.match(name) or ".." in name.split("/") or name.startswith("internal/"):
        raise InvalidKnowledgePath(name)
    relative = f"internal/{name}" if visibility == "internal" else name
    try:
        target = ws.path("knowledge", relative)
    except PathEscapeError as error:
        raise InvalidKnowledgePath(name) from error
    target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8")
    target.chmod(0o600)
    index = _index(ws)
    lines = index.read_text(encoding="utf-8").splitlines() if index.exists() else []
    lines = [ln for ln in lines if not ln.startswith(f"- {relative}:")]
    lines.append(f"- {relative}: {' '.join(description.split())[:120]}")
    index.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    index.write_text("\n".join(lines) + "\n", encoding="utf-8")
    index.chmod(0o600)
    return relative


def seed_defaults(ws: Workspace, lang: str = "pt") -> None:
    """Safe, generic files so a new workspace can answer before anything is taught."""
    for name, (description, text) in _DEFAULT_FILES["en" if lang == "en" else "pt"].items():
        if not ws.path("knowledge", name).exists():
            write_knowledge(ws, name, text, visibility="public", description=description)
