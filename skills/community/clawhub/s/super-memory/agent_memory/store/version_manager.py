"""Memory version management — extracted from MemoryStore.

Handles version history, version tracking, and revert operations.
"""

import json as _json
import logging

logger = logging.getLogger(__name__)


class VersionManager:
    """Manages memory version history and rollback.

    Extracted from MemoryStore to separate versioning concerns.
    """

    def __init__(self, store):
        """Initialize with a reference to the parent store.

        Args:
            store: MemoryStore instance (for conn access and transaction)
        """
        self._store = store

    def get_versions(self, memory_id, limit=20):
        """Get version history for a memory (from old to new).

        Returns:
            List of version dicts with version_id, content, importance,
            topics, change_reason, created_at fields.
        """
        rows = self._store.conn.execute(
            """SELECT version_id, content, content_hash, importance, topics_json, change_reason, created_at
               FROM memory_versions
               WHERE memory_id = ?
               ORDER BY version_id ASC
               LIMIT ?""",
            (memory_id, limit),
        ).fetchall()

        versions = []
        for r in rows:
            v = dict(r)
            try:
                v["topics"] = _json.loads(v.pop("topics_json", "[]"))
            except Exception:
                v["topics"] = []
            versions.append(v)

        # Append current version as latest
        current = self._store.conn.execute(
            "SELECT content, content_hash, importance, created_at FROM memories WHERE memory_id = ? AND deleted=0",
            (memory_id,),
        ).fetchone()
        if current:
            versions.append({
                "version_id": len(versions) + 1,
                "content": current["content"],
                "content_hash": current["content_hash"],
                "importance": current["importance"],
                "topics": [t["code"] for t in self._store._batch_get_topics([memory_id]).get(memory_id, [])],
                "change_reason": "current",
                "created_at": current["created_at"],
                "is_current": True,
            })

        return versions

    def revert_to_version(self, memory_id, version_number):
        """Revert a memory to a specific version.

        Args:
            memory_id: The memory to revert.
            version_number: Version number to revert to (1-based).

        Returns:
            dict with 'reverted' bool and 'memory_id'.
        """
        versions = self.get_versions(memory_id)
        if not versions:
            return {"reverted": False, "reason": "No version history found"}

        target = None
        for v in versions:
            if v.get("version_number") == version_number or v.get("version_id") == version_number:
                target = v
                break

        if target is None:
            return {"reverted": False, "reason": f"Version {version_number} not found"}

        old_content = target.get("content", "")
        if not old_content:
            return {"reverted": False, "reason": "Version content is empty"}

        self._store.update_memory(memory_id, old_content, change_reason=f"Reverted to version {version_number}")
        return {"reverted": True, "memory_id": memory_id, "version_reverted_to": version_number}

    def create_version(self, memory_id, content, metadata=None):
        """Create a new version entry for a memory.

        Args:
            memory_id: The memory ID.
            content: The content to snapshot.
            metadata: Optional metadata JSON string.

        Returns:
            The new version number.
        """
        # Get current max version number
        row = self._store.conn.execute(
            "SELECT COALESCE(MAX(version_id), 0) as max_ver FROM memory_versions WHERE memory_id = ?",
            (memory_id,),
        ).fetchone()
        max_ver = row["max_ver"] if row else 0

        with self._store.transaction() as conn:
            conn.execute(
                "INSERT INTO memory_versions (memory_id, version_id, content, content_hash, importance, topics_json, change_reason) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (memory_id, max_ver + 1, content, "", "", metadata or "[]", "manual_snapshot"),
            )
        return max_ver + 1
