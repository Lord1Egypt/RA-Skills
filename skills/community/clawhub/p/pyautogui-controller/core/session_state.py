import json
import time
from pathlib import Path
from typing import Any, Dict, Optional


class SessionStateStore:
    def __init__(self, path: Optional[Path] = None):
        self.path = path or (Path("runtime") / "session_state.json")

    def load(self) -> Dict[str, Any]:
        try:
            if not self.path.exists():
                return {}
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def save(self, payload: Dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    def update(self, **kwargs) -> Dict[str, Any]:
        data = self.load()
        data.update(kwargs)
        data["updated_at"] = time.time()
        self.save(data)
        return data

    def get_recent(self, ttl_seconds: int = 180) -> Dict[str, Any]:
        data = self.load()
        ts = data.get("updated_at")
        if not ts:
            return {}
        if (time.time() - float(ts)) > ttl_seconds:
            return {}
        return data
