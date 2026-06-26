from __future__ import annotations

from collections import Counter
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.feedback import apply_feedback, default_memory
from scripts.common import load_json
from core.storage import LocalStateStore


def load_memory(path: str) -> dict[str, Any]:
    try:
        payload = load_json(path)
        if isinstance(payload, dict):
            return {**default_memory(), **payload}
    except FileNotFoundError:
        pass
    return default_memory()


def save_memory(path: str, payload: dict[str, Any]) -> None:
    LocalStateStore(Path(path).parent).save_memory(payload, Path(path).name)
