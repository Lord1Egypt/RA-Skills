"""Is a newer version of the skill out? Asked on every tick, answered from a one-hour cache.

This is the helper's only network call besides the runner's own: one GET of ``latest.json`` from
the module's public repository. It never raises and never blocks service: a failed check is just
silence.
"""

from __future__ import annotations

import json
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Literal

from tn_assist.i18n import Lang, t
from tn_assist.paths import Workspace
from tn_assist.store import read_json, write_json_atomic
from tn_assist.timeutil import parse_iso, utc_iso

LATEST_URL = "https://raw.githubusercontent.com/turbo-notify/agent-skills/main/latest.json"
CACHE_OK = timedelta(hours=1)
CACHE_FAILED = timedelta(minutes=10)
Harness = Literal["claude-code", "claude-desktop", "codex", "antigravity"]
_HARNESSES: tuple[Harness, ...] = ("claude-code", "claude-desktop", "codex", "antigravity")


def parse_version(raw: str) -> tuple[int, int, int]:
    parts = raw.strip().lstrip("v").split(".")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError(f"not a version: {raw!r}")
    major, minor, patch = (int(p) for p in parts)
    return major, minor, patch


def update_hint(harness: Harness | None, lang: Lang) -> str:
    if harness is not None:
        return t(f"update_hint_{harness.replace('-', '_')}", lang)
    return "; ".join(t(f"update_hint_{h.replace('-', '_')}", lang) for h in _HARNESSES)


@dataclass(frozen=True)
class UpdateNotice:
    installed: str
    latest: str
    command: str
    notes_url: str | None
    min_workspace_schema: int

    def text(self, lang: Lang) -> str:
        return t(
            "update_notice",
            lang,
            latest=self.latest,
            installed=self.installed,
            command=self.command,
        )


def fetch_latest(timeout: float = 3.0) -> Any:
    with urllib.request.urlopen(LATEST_URL, timeout=timeout) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def _valid(payload: Any) -> bool:
    if not isinstance(payload, dict) or not isinstance(payload.get("version"), str):
        return False
    try:
        parse_version(payload["version"])
    except ValueError:
        return False
    return True


def check(
    ws: Workspace,
    installed: str,
    fetch: Callable[[], Any] | None,
    now: datetime,
    *,
    harness: Harness | None = None,
    lang: Lang = "pt",
) -> UpdateNotice | None:
    cache_path = ws.path("update-check.json")
    cache = read_json(cache_path, {})
    cache = cache if isinstance(cache, dict) else {}
    latest = cache.get("latest")
    checked_at = cache.get("checked_at")
    ttl = CACHE_OK if cache.get("ok") else CACHE_FAILED
    fresh = isinstance(checked_at, str) and now - parse_iso(checked_at) < ttl
    if not fresh and fetch is not None:
        try:
            payload = fetch()
        except Exception:  # noqa: BLE001 - a failed check must never stop the service
            payload = None
        ok = _valid(payload)
        write_json_atomic(
            cache_path,
            {"checked_at": utc_iso(now), "ok": ok, "latest": payload if ok else latest},
        )
        latest = payload if ok else latest
    if not _valid(latest):
        return None
    assert isinstance(latest, dict)
    try:
        newer = parse_version(latest["version"]) > parse_version(installed)
    except ValueError:
        return None
    if not newer:
        return None
    return UpdateNotice(
        installed=installed,
        latest=latest["version"],
        command=update_hint(harness, lang),
        notes_url=latest.get("notes_url"),
        min_workspace_schema=int(latest.get("min_workspace_schema", 1)),
    )
