#!/usr/bin/env python3
"""
Cross-platform LanceDB memory backend for OpenClaw/Clawdbot.

Compatible with Windows, macOS, and Linux.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    import lancedb
except ImportError as exc:
    raise RuntimeError(
        "lancedb is not installed. Run: pip install lancedb pandas pyarrow"
    ) from exc


def _default_db_path() -> Path:
    env_path = os.getenv("OPENCLAW_LANCEDB_PATH")
    if env_path:
        return Path(env_path).expanduser()

    if os.name == "nt":
        base = Path(os.getenv("CLAWTEST_ROOT", r"D:\clawtest"))
        return base / "memory" / "lancedb"

    return Path.home() / ".clawdbot" / "memory" / "lancedb"


class FinalLanceMemory:
    """LanceDB memory integration with stable text retrieval."""

    TABLE_NAME = "memories"

    def __init__(self, db_path: Optional[str] = None):
        target = Path(db_path).expanduser() if db_path else _default_db_path()
        self.db_path = target
        self.db_path.mkdir(parents=True, exist_ok=True)
        self.db = lancedb.connect(str(self.db_path))
        self._ensure_table()

    def _ensure_table(self) -> None:
        try:
            self.db.open_table(self.TABLE_NAME)
        except Exception:
            self._create_table()

    def _create_table(self) -> None:
        bootstrap = [
            {
                "id": 1,
                "timestamp": datetime.now().isoformat(),
                "content": "LanceDB memory initialized",
                "metadata": json.dumps({"type": "system"}),
            }
        ]
        self.db.create_table(self.TABLE_NAME, data=bootstrap)

    def _table(self):
        return self.db.open_table(self.TABLE_NAME)

    def _next_id(self) -> int:
        table = self._table()
        rows = table.to_pandas()
        if rows.empty or "id" not in rows.columns:
            return 1
        max_id = int(rows["id"].max())
        return max_id + 1

    def add_memory(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> int:
        table = self._table()
        memory_id = self._next_id()
        payload = {
            "id": memory_id,
            "timestamp": datetime.now().isoformat(),
            "content": content,
            "metadata": json.dumps(metadata or {}, ensure_ascii=True),
        }
        table.add([payload])
        return memory_id

    def search_memories(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        table = self._table()
        rows = table.to_pandas()
        if rows.empty:
            return []

        normalized_query = query.strip().lower()
        if not normalized_query:
            result = rows.sort_values("timestamp", ascending=False).head(limit)
            return result.to_dict("records")

        mask = rows["content"].fillna("").str.lower().str.contains(normalized_query, regex=False)
        result = rows[mask].sort_values("timestamp", ascending=False).head(limit)
        return result.to_dict("records")

    def get_all_memories(self) -> List[Dict[str, Any]]:
        table = self._table()
        rows = table.to_pandas()
        if rows.empty:
            return []
        return rows.sort_values("timestamp", ascending=False).to_dict("records")


final_memory = FinalLanceMemory()


def add_memory(content: str, metadata: Optional[Dict[str, Any]] = None) -> int:
    return final_memory.add_memory(content, metadata)


def search_memories(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    return final_memory.search_memories(query, limit)


def get_all_memories() -> List[Dict[str, Any]]:
    return final_memory.get_all_memories()


if __name__ == "__main__":
    print("Testing cross-platform LanceDB memory backend...")
    sample_id = add_memory(
        content="This is a test memory for LanceDB integration",
        metadata={"type": "test", "importance": 8},
    )
    print(f"Added memory with ID: {sample_id}")
    print(f"Search results: {len(search_memories('test memory'))} memories found")
    print(f"Total memories: {len(get_all_memories())}")