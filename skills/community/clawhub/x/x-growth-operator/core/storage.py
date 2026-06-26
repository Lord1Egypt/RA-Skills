from __future__ import annotations

from pathlib import Path
from typing import Any

from scripts.common import append_jsonl, load_json, write_json


class LocalStateStore:
    def __init__(self, root: str | Path = "data") -> None:
        self.root = Path(root)

    def path(self, *parts: str) -> Path:
        return self.root.joinpath(*parts)

    def load_json(self, name: str, default: Any | None = None) -> Any:
        path = self.path(name)
        try:
            return load_json(path)
        except FileNotFoundError:
            return default

    def save_json(self, name: str, payload: Any) -> Path:
        return write_json(self.path(name), payload)

    def append_jsonl(self, name: str, payload: Any) -> Path:
        return append_jsonl(self.path(name), payload)

    def load_mission(self, name: str = "mission.json") -> dict[str, Any]:
        payload = self.load_json(name, default={})
        return payload if isinstance(payload, dict) else {}

    def save_mission(self, mission: dict[str, Any], name: str = "mission.json") -> Path:
        return self.save_json(name, mission)

    def load_memory(self, name: str = "memory.json", default: dict[str, Any] | None = None) -> dict[str, Any]:
        payload = self.load_json(name, default=default or {})
        return payload if isinstance(payload, dict) else (default or {})

    def save_memory(self, memory: dict[str, Any], name: str = "memory.json") -> Path:
        return self.save_json(name, memory)

    def save_scored_opportunities(self, payload: dict[str, Any], name: str = "opportunities_scored.json") -> Path:
        return self.save_json(name, payload)

    def save_action_plan(self, payload: dict[str, Any], name: str = "action_plan.json") -> Path:
        return self.save_json(name, payload)

    def save_action(self, payload: dict[str, Any], name: str = "action.json") -> Path:
        return self.save_json(name, payload)

    def append_execution_event(self, payload: dict[str, Any], name: str = "execution_log.jsonl") -> Path:
        return self.append_jsonl(name, payload)
