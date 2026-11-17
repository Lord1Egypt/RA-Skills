"""时间戳与 ISO 展示。"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Optional


def now_unix() -> int:
    return int(time.time())


def unix_to_iso(ts: Optional[int]) -> Optional[str]:
    if ts is None:
        return None
    try:
        return datetime.fromtimestamp(int(ts)).isoformat(timespec="seconds")
    except (ValueError, OSError, OverflowError):
        return None
