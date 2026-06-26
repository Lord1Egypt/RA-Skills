from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
import json

from redis import Redis

from .models import SituationReport


class StateStore(ABC):
    @abstractmethod
    def load_latest_report(self) -> SituationReport | None:
        raise NotImplementedError

    @abstractmethod
    def save_latest_report(self, report: SituationReport) -> None:
        raise NotImplementedError

    @abstractmethod
    def save_checkpoint(self, key: str, timestamp: datetime) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_checkpoint(self, key: str) -> datetime | None:
        raise NotImplementedError


class JsonStateStore(StateStore):
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _read(self) -> dict[str, object]:
        if not self.path.exists():
            return {"checkpoints": {}}
        return json.loads(self.path.read_text())

    def _write(self, payload: dict[str, object]) -> None:
        self.path.write_text(json.dumps(payload, indent=2))

    def load_latest_report(self) -> SituationReport | None:
        payload = self._read().get("latest_report")
        if not payload:
            return None
        return SituationReport.from_dict(payload)

    def save_latest_report(self, report: SituationReport) -> None:
        payload = self._read()
        payload["latest_report"] = report.to_dict()
        self._write(payload)

    def save_checkpoint(self, key: str, timestamp: datetime) -> None:
        payload = self._read()
        checkpoints = payload.setdefault("checkpoints", {})
        checkpoints[key] = timestamp.isoformat()
        self._write(payload)

    def load_checkpoint(self, key: str) -> datetime | None:
        payload = self._read()
        raw = payload.get("checkpoints", {}).get(key)
        if not raw:
            return None
        return datetime.fromisoformat(raw)


class RedisStateStore(StateStore):
    def __init__(self, url: str) -> None:
        self.client = Redis.from_url(url, decode_responses=True)

    def load_latest_report(self) -> SituationReport | None:
        payload = self.client.get("mts:latest_report")
        if not payload:
            return None
        return SituationReport.from_dict(json.loads(payload))

    def save_latest_report(self, report: SituationReport) -> None:
        self.client.set("mts:latest_report", json.dumps(report.to_dict()))

    def save_checkpoint(self, key: str, timestamp: datetime) -> None:
        self.client.hset("mts:checkpoints", key, timestamp.isoformat())

    def load_checkpoint(self, key: str) -> datetime | None:
        raw = self.client.hget("mts:checkpoints", key)
        if not raw:
            return None
        return datetime.fromisoformat(raw)


def build_state_store(redis_url: str | None, fallback_path: Path) -> StateStore:
    if redis_url:
        return RedisStateStore(redis_url)
    return JsonStateStore(fallback_path)
