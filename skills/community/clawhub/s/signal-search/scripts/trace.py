"""scripts/trace.py - 可观测追踪（默认关，observability.trace）。轻量 JSONL 日志。"""

import json
import os
import time
from typing import Any, Dict, List

from common import load_config as _load_cfg


class Trace:
    def __init__(self, cfg: dict = None):
        o = (cfg or _load_cfg()).get("observability", {})
        self.enabled = o.get("trace", False)
        self.dir = o.get("log_dir", ".trace/")
        self.events: List[Dict[str, Any]] = []
        self.run_id = str(int(time.time() * 1000))
        if self.enabled:
            os.makedirs(self.dir, exist_ok=True)

    def event(self, name: str, data: Dict[str, Any] = None) -> None:
        e = {"t": round(time.time(), 3), "name": name, "data": data or {}}
        self.events.append(e)
        if self.enabled:
            try:
                with open(
                    os.path.join(self.dir, self.run_id + ".jsonl"), "a", encoding="utf-8"
                ) as f:
                    f.write(json.dumps(e, ensure_ascii=False) + "\n")
            except Exception:
                pass

    def snapshot(self) -> Dict[str, Any]:
        return {"run_id": self.run_id, "events": self.events}
