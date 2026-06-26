from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


class DistanceCache:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path).expanduser()
        self._data: dict[str, float] = {}
        self._dirty = False
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            self._data = {}
            return
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            self._data = {str(key): float(value) for key, value in raw.items()}
        except (ValueError, OSError, AttributeError) as exc:
            # A corrupt or unreadable cache should never brick the run.
            # Start fresh and let the next save overwrite the bad file.
            print(
                f"warning: distance cache at {self.path} is unreadable ({exc}); starting with an empty cache",
                file=sys.stderr,
            )
            self._data = {}
            self._dirty = True

    def save(self) -> None:
        if not self._dirty:
            return
        self.path.parent.mkdir(parents=True, exist_ok=True)
        # Write to a temp file and atomically replace so an interrupted run
        # can never leave a half-written (corrupt) cache behind.
        tmp_path = self.path.with_name(self.path.name + ".tmp")
        tmp_path.write_text(json.dumps(self._data, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(tmp_path, self.path)
        self._dirty = False

    @staticmethod
    def key(engine: str, start_address: str, end_address: str) -> str:
        raw = "\n".join(
            [
                engine.strip().lower(),
                " ".join(start_address.lower().split()),
                " ".join(end_address.lower().split()),
            ]
        )
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def get(self, engine: str, start_address: str, end_address: str) -> float | None:
        return self._data.get(self.key(engine, start_address, end_address))

    def set(self, engine: str, start_address: str, end_address: str, miles: float) -> None:
        self._data[self.key(engine, start_address, end_address)] = float(miles)
        self._dirty = True
