from __future__ import annotations

from typing import Any, Dict, List, Optional


def rank_key(manifest: Dict[str, Any]) -> tuple[int, int, str]:
    return (
        int(manifest.get("new_articles", 0) or 0),
        int(manifest.get("deep_set_count", 0) or 0),
        str(manifest.get("finalize_finished_at") or manifest.get("finished_at") or ""),
    )


def select_winner(committed: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not committed:
        return None
    return max(committed, key=rank_key)
