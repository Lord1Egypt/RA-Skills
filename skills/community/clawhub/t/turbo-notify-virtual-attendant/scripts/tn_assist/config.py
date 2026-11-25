"""Workspace configuration and the read side of the administrator registry."""

from __future__ import annotations

from typing import Any

from tn_assist.paths import Workspace
from tn_assist.store import read_json, write_json_atomic

SCHEMA_VERSION = 1


def load_config(ws: Workspace) -> dict[str, Any]:
    data = read_json(ws.path("config.json"), {})
    return data if isinstance(data, dict) else {}


def save_config(ws: Workspace, config: dict[str, Any]) -> None:
    write_json_atomic(ws.path("config.json"), config)


def admin_numbers(ws: Workspace) -> frozenset[str]:
    data = read_json(ws.path("admins.json"), {})
    admins = data.get("admins", []) if isinstance(data, dict) else []
    return frozenset(
        str(entry["number"]) for entry in admins if isinstance(entry, dict) and entry.get("number")
    )
