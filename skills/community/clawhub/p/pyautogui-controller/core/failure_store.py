import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class FailureStore:
    def __init__(self, out_dir: Path = Path("runtime/failures")):
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def record(self, payload: Dict[str, Any]) -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        path = self.out_dir / f"failure_{ts}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, default=str), encoding="utf-8")
        return str(path)
