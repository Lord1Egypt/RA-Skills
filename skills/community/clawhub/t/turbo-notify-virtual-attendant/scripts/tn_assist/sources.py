"""Other MCP servers as business sources.

They are read-only information providers, never a channel. Each one is classified:
``public`` (usable for customers), ``internal`` (administrators and attendants),
``admin_only`` (administrators) or ``off``. A source nobody classified is ``off``.
Widening access always needs an explicit confirmation; narrowing never does.
"""

from __future__ import annotations

import enum
import re
from dataclasses import dataclass, replace
from typing import Any, Iterable, Literal

from tn_assist.paths import Workspace
from tn_assist.store import read_json, write_json_atomic

Mode = Literal["snapshot", "live"]
Role = Literal["contact", "admin", "attendant"]
_WRITE_WORDS = re.compile(
    r"(^|[_\-.\s]|(?<=[a-z]))(create|update|delete|remove|send|write|post|put|set|cancel|pay|charge|"
    r"transfer|approve|insert|drop|reply|publish|upload|merge|assign|add)([_\-.\s]|(?=[A-Z])|$)",
    re.IGNORECASE,
)


class SourceClass(enum.Enum):
    OFF = "off"
    ADMIN_ONLY = "admin_only"
    INTERNAL = "internal"
    PUBLIC = "public"


_RANK = {
    SourceClass.OFF: 0,
    SourceClass.ADMIN_ONLY: 1,
    SourceClass.INTERNAL: 2,
    SourceClass.PUBLIC: 3,
}


class NeedsConfirmation(Exception):
    """The change widens who can reach the source's data; confirm it first."""


class WriteToolError(ValueError):
    """A write-capable tool can never be allowed."""


def is_probably_write(tool_name: str) -> bool:
    """A conservative name check: a tool that sounds like it changes something is refused."""
    return bool(_WRITE_WORDS.search(tool_name))


@dataclass(frozen=True)
class Source:
    name: str
    cls: SourceClass = SourceClass.OFF
    mode: Mode = "snapshot"
    live_tools: tuple[str, ...] = ()
    personal: bool = False

    def to_json(self) -> dict[str, Any]:
        return {
            "cls": self.cls.value,
            "mode": self.mode,
            "live_tools": list(self.live_tools),
            "personal": self.personal,
        }

    @classmethod
    def from_json(cls, name: str, data: dict[str, Any]) -> Source:
        return cls(
            name,
            SourceClass(data.get("cls", "off")),
            data.get("mode", "snapshot"),
            tuple(data.get("live_tools") or ()),
            bool(data.get("personal", False)),
        )


class SourceRegistry:
    def __init__(self, ws: Workspace, sources: dict[str, Source], markers: dict[str, list[str]]):
        self.ws = ws
        self._sources = sources
        self._markers = markers

    @classmethod
    def load(cls, ws: Workspace) -> SourceRegistry:
        data = read_json(ws.path("sources.json"), {})
        data = data if isinstance(data, dict) else {}
        sources = {n: Source.from_json(n, d) for n, d in (data.get("sources") or {}).items()}
        return cls(ws, sources, {k: list(v) for k, v in (data.get("markers") or {}).items()})

    def _save(self) -> None:
        write_json_atomic(
            self.ws.path("sources.json"),
            {
                "sources": {n: s.to_json() for n, s in self._sources.items()},
                "markers": self._markers,
            },
        )

    def get(self, name: str) -> Source | None:
        return self._sources.get(name)

    def all(self) -> list[Source]:
        return sorted(self._sources.values(), key=lambda s: s.name)

    def discovered(self, names: Iterable[str]) -> None:
        changed = False
        for name in names:
            if name not in self._sources:
                self._sources[name] = Source(name)
                changed = True
        if changed:
            self._save()

    def classify(
        self,
        name: str,
        cls: SourceClass,
        *,
        mode: Mode = "snapshot",
        live_tools: tuple[str, ...] = (),
        personal: bool = False,
        confirmed: bool = False,
    ) -> None:
        old = self._sources[name]  # KeyError for a server nobody discovered
        for tool in live_tools:
            if is_probably_write(tool):
                raise WriteToolError(tool)
        widening = (
            _RANK[cls] > _RANK[old.cls]
            or (old.personal and not personal)
            or (old.mode == "snapshot" and mode == "live")
            or bool(set(live_tools) - set(old.live_tools))
        )
        if widening and not confirmed:
            raise NeedsConfirmation(name)
        self._sources[name] = replace(
            old, cls=cls, mode=mode, live_tools=tuple(live_tools), personal=personal
        )
        self._save()

    def allowed_for(self, role: Role, *, assisted: bool, in_session: bool) -> list[Source]:
        """Sources whose **live tools** a role's turn may use. Snapshots need no tool."""
        allowed: list[Source] = []
        for source in self.all():
            if source.cls is SourceClass.OFF:
                continue
            if role == "contact":
                if source.cls is not SourceClass.PUBLIC or source.mode != "live" or not in_session:
                    continue
                if source.personal and not assisted:
                    continue
            elif role == "attendant" and source.cls is SourceClass.ADMIN_ONLY:
                continue
            allowed.append(source)
        return allowed

    def add_marker(self, name: str, marker: str) -> None:
        self._markers.setdefault(name, [])
        if marker not in self._markers[name]:
            self._markers[name].append(marker)
            self._save()

    def non_public_markers(self) -> list[str]:
        out: list[str] = []
        for name, markers in self._markers.items():
            source = self._sources.get(name)
            if source is not None and source.cls is not SourceClass.PUBLIC:
                out += markers
        return out
