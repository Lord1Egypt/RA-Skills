"""Layered memory per contact: raw transcript, window, episodes, card, policy.

- L0 ``transcript.jsonl``: append-only, every line with the event id it came from.
- L1 window: the newest lines not yet compacted that fit a token budget.
- L2 ``episodes/NNN.md``: summaries of older chunks (written by a model turn, stored here).
- L3 ``card.json``: stable facts with their source (administrator beats attendant beats inferred).
- ``memory-policy.json``: the numbers, followed as written.
"""

from __future__ import annotations

import dataclasses
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Literal

from tn_assist.paths import ContactKey, Workspace
from tn_assist.sanitize import clean_fact_value
from tn_assist.store import (
    append_jsonl_once,
    read_json,
    read_jsonl,
    write_json_atomic,
)
from tn_assist.timeutil import utc_iso
from tn_assist.tokens import estimate_tokens

CARD_CAP_TOKENS = 1500
Source = Literal["inferred", "platform", "attendant", "admin"]
# "platform" is what Turbo Notify reports (the name WhatsApp shows): not written by the model, so a
# customer's words cannot forge it. A model-inferred fact never replaces it.
_RANK = {"inferred": 0, "platform": 1, "attendant": 2, "admin": 3}


AUTO_RESUME_MIN_MINUTES = 5


@dataclass(frozen=True)
class Policy:
    pack_budget_contact: int = 6000
    pack_budget_admin: int = 8000
    window_turns: int = 40
    compaction_trigger_tokens: int = 3000
    raw_retention_days: int = 90
    episodes_in_pack: int = 2
    reply_cap_per_hour: int = 6
    reply_cap_per_day: int = 30
    handoff_reminder_hours: int = 4
    auto_resume_after_minutes: int | None = None  # off; at least AUTO_RESUME_MIN_MINUTES

    @classmethod
    def load(cls, ws: Workspace) -> Policy:
        data = read_json(ws.path("memory-policy.json"), {})
        known = {f.name for f in dataclasses.fields(cls)}
        values = {k: v for k, v in (data.items() if isinstance(data, dict) else []) if k in known}
        return cls(**values)


@dataclass(frozen=True)
class Line:
    event_id: str
    role: str
    direction: str
    type: str
    at: str
    text: str
    kind: str = "message"
    hydrated: bool = True
    truncated: bool = False
    message_id: str | None = None


def _transcript(ws: Workspace, key: ContactKey) -> Path:
    return ws.contact_dir(key) / "transcript.jsonl"


def read_lines_at(path: Path) -> list[Line]:
    rows = read_jsonl(path)
    overrides: dict[str, str | None] = {
        str(r["for"]): r.get("text") for r in rows if r.get("kind") == "text"
    }
    lines: list[Line] = []
    for row in rows:
        kind = row.get("kind")
        if kind == "text":
            continue
        if kind == "gap":
            lines.append(
                Line(str(row["id"]), "system", "", "gap", str(row.get("to", "")), "[gap]", "gap")
            )
            continue
        event_id = str(row["id"])
        text = row.get("text")
        hydrated = text is not None
        truncated = False
        if text is None and event_id in overrides:
            override = overrides[event_id]
            hydrated = True
            if override is None:
                truncated = True
                text = row.get("preview") or ""
            else:
                text = override
        if text is None:
            text = row.get("preview") or ""
        lines.append(
            Line(
                event_id,
                str(row.get("role", "")),
                str(row.get("dir", "")),
                str(row.get("type") or "text"),
                str(row.get("at", "")),
                str(text),
                "message",
                hydrated,
                truncated,
                row.get("msg"),
            )
        )
    return lines


def read_lines(ws: Workspace, key: ContactKey) -> list[Line]:
    return read_lines_at(_transcript(ws, key))


def append_line(
    ws: Workspace, key: ContactKey, *, role: str, text: str, event_id: str, at: str
) -> bool:
    row: dict[str, Any] = {
        "id": event_id,
        "at": at,
        "role": role,
        "dir": "in" if role == "contact" else "out",
        "type": "text",
        "preview": "",
        "text": text,
    }
    return append_jsonl_once(_transcript(ws, key), row)


def set_text_at(path: Path, event_id: str, text: str | None) -> None:
    append_jsonl_once(
        path, {"id": f"text-{event_id}", "kind": "text", "for": event_id, "text": text}
    )


def set_line_text(ws: Workspace, key: ContactKey, event_id: str, text: str | None) -> None:
    set_text_at(_transcript(ws, key), event_id, text)


def _memory_state(ws: Workspace, key: ContactKey) -> dict[str, Any]:
    data = read_json(ws.contact_dir(key) / "memory.json", {})
    return data if isinstance(data, dict) else {}


def _uncompacted(ws: Workspace, key: ContactKey) -> list[Line]:
    lines = read_lines(ws, key)
    through = _memory_state(ws, key).get("compacted_through")
    if through:
        for index, line in enumerate(lines):
            if line.event_id == through:
                return lines[index + 1 :]
    return lines


def read_window(ws: Workspace, key: ContactKey, budget_tokens: int) -> list[Line]:
    policy = Policy.load(ws)
    chosen: list[Line] = []
    used = 0
    for line in reversed(_uncompacted(ws, key)):
        cost = estimate_tokens(line.text)
        if chosen and (used + cost > budget_tokens or len(chosen) >= policy.window_turns):
            break
        if not chosen and cost > budget_tokens:
            continue
        chosen.append(line)
        used += cost
    return list(reversed(chosen))


COMPACTION_CHUNK_MAX = 60


def compaction_chunk(ws: Workspace, key: ContactKey, policy: Policy) -> list[Line]:
    """The oldest uncompacted messages, leaving the newest ``window_turns // 2`` word for word."""
    lines = [ln for ln in _uncompacted(ws, key) if ln.kind == "message"]
    keep = max(1, policy.window_turns // 2)
    if len(lines) <= keep:
        return []
    return lines[: min(COMPACTION_CHUNK_MAX, len(lines) - keep)]


def lines_between(ws: Workspace, key: ContactKey, first: str, last: str) -> list[Line]:
    lines = [ln for ln in read_lines(ws, key) if ln.kind == "message"]
    ids = [ln.event_id for ln in lines]
    if first not in ids or last not in ids:
        return []
    return lines[ids.index(first) : ids.index(last) + 1]


def needs_compaction(ws: Workspace, key: ContactKey, policy: Policy) -> bool:
    total = sum(
        estimate_tokens(line.text) for line in _uncompacted(ws, key) if line.kind == "message"
    )
    return total > policy.compaction_trigger_tokens


def episodes(ws: Workspace, key: ContactKey) -> list[Path]:
    directory = ws.contact_dir(key) / "episodes"
    return sorted(directory.glob("*.md")) if directory.is_dir() else []


def write_episode(
    ws: Workspace,
    key: ContactKey,
    summary: str,
    *,
    covers: tuple[str, str],
    now: datetime | None = None,
) -> Path:
    directory = ws.contact_dir(key) / "episodes"
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    path = directory / f"{len(episodes(ws, key)) + 1:03d}.md"
    stamp = utc_iso(now) if now else ""
    path.write_text(
        f"covers: {covers[0]}..{covers[1]}\nwritten: {stamp}\n---\n{summary.strip()}\n",
        encoding="utf-8",
    )
    os.chmod(path, 0o600)
    state = _memory_state(ws, key)
    state["compacted_through"] = covers[1]
    write_json_atomic(ws.contact_dir(key) / "memory.json", state)
    return path


@dataclass(frozen=True)
class Fact:
    key: str
    value: str
    source: Source
    at: str


def replace_value(fact: Fact) -> Fact:
    return dataclasses.replace(fact, value=clean_fact_value(fact.value))


class Card:
    def __init__(self, ws: Workspace, key: ContactKey, facts: dict[str, Fact]) -> None:
        self._ws = ws
        self._key = key
        self._facts = facts

    @classmethod
    def load(cls, ws: Workspace, key: ContactKey) -> Card:
        data = read_json(ws.contact_dir(key) / "card.json", {})
        raw = data.get("facts", []) if isinstance(data, dict) else []
        facts = {
            str(r["key"]): Fact(str(r["key"]), str(r["value"]), r["source"], str(r["at"]))
            for r in raw
        }
        return cls(ws, key, facts)

    def get(self, key: str) -> Fact | None:
        return self._facts.get(key)

    def facts(self) -> list[Fact]:
        return sorted(self._facts.values(), key=lambda f: f.key)

    def merge(self, incoming: list[Fact]) -> None:
        for fact in incoming:
            fact = replace_value(fact)
            old = self._facts.get(fact.key)
            if (
                old is None
                or _RANK[fact.source] > _RANK[old.source]
                or (_RANK[fact.source] == _RANK[old.source] and fact.at >= old.at)
            ):
                self._facts[fact.key] = fact
        self._enforce_cap()

    def _enforce_cap(self) -> None:
        while estimate_tokens(self.render()) > CARD_CAP_TOKENS:
            droppable = [f for f in self._facts.values() if f.source != "admin"]
            if not droppable:
                return
            victim = min(droppable, key=lambda f: (_RANK[f.source], f.at, f.key))
            del self._facts[victim.key]

    def render(self) -> str:
        # values are cleaned again here: a card edited by hand must not forge a line either
        return "\n".join(
            f"- **{f.key}** ({f.source}): {clean_fact_value(f.value)}" for f in self.facts()
        )

    def save(self) -> None:
        payload = {"facts": [dataclasses.asdict(f) for f in self.facts()]}
        write_json_atomic(self._ws.contact_dir(self._key) / "card.json", payload)


def purge_expired(ws: Workspace, now: datetime) -> int:
    """Drop transcript lines older than the retention window. Returns message lines removed."""
    policy = Policy.load(ws)
    cutoff = utc_iso(now - timedelta(days=policy.raw_retention_days))
    removed = 0
    # the customers' transcripts, the copies a migration left, and the console threads
    transcripts = [
        *ws.root.glob("contacts/*/transcript.jsonl"),
        *ws.root.glob("backup/*/contacts/*/transcript.jsonl"),
        *ws.root.glob("threads/*/*.jsonl"),
        *ws.root.glob("backup/*/threads/*/*.jsonl"),
    ]
    for transcript in transcripts:
        rows = read_jsonl(transcript)
        dropped: set[str] = set()
        kept = []
        for row in rows:
            if row.get("kind") != "text" and str(row.get("at", "9999")) < cutoff:
                dropped.add(str(row.get("id")))
                if row.get("kind") is None:
                    removed += 1
                continue
            kept.append(row)
        kept = [r for r in kept if not (r.get("kind") == "text" and str(r.get("for")) in dropped)]
        if len(kept) != len(rows):
            tmp = transcript.with_suffix(".tmp")
            tmp.write_text(
                "".join(json.dumps(r, sort_keys=True) + "\n" for r in kept), encoding="utf-8"
            )
            os.chmod(tmp, 0o600)
            os.replace(tmp, transcript)
    return removed
