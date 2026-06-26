"""Memory link management — extracted from MemoryStore.

Handles relationships between memories (causal, entity, reference links).
"""

import logging

logger = logging.getLogger(__name__)


class LinkManager:
    """Manages relationships between memories.

    Extracted from MemoryStore to separate linking concerns.
    """

    def __init__(self, store):
        """Initialize with a reference to the parent store."""
        self._store = store

    def insert_link(self, source_id, target_id, link_type="related", weight=1.0, reason=None, metadata=None):
        """Create a link between two memories.

        Args:
            source_id: Source memory ID.
            target_id: Target memory ID.
            link_type: Type of link (e.g., "causal", "entity", "reference").
            weight: Link weight (default 1.0).
            reason: Optional reason for the link.
            metadata: Optional metadata (ignored, kept for API compat).

        Returns:
            True on success, None on skip.
        """
        if not source_id or not target_id:
            logger.warning("insert_link skipped: source_id=%s, target_id=%s", source_id, target_id)
            return None
        if source_id == target_id:
            return None
        with self._store.transaction() as conn:
            conn.execute(
                """INSERT INTO memory_links (source_id, target_id, link_type, weight, reason)
                   VALUES (?, ?, ?, ?, ?)""",
                (source_id, target_id, link_type, weight, reason),
            )
        self._store._invalidate_cache()
        return True

    def get_linked(self, memory_id, link_type=None, direction="both", depth=1, limit=50):
        """Get memories linked to the given memory.

        Args:
            memory_id: The memory ID to query.
            link_type: Optional filter by link type.
            direction: "outgoing", "incoming", or "both" (default "both").
            depth: Traversal depth (default 1).
            limit: Max results (default 50).

        Returns:
            List of linked memory dicts with _link_weight, _link_type, _link_depth metadata.
        """
        from collections import deque

        visited = set()
        link_meta = {}

        queue = deque([(memory_id, 1, 1.0)])
        while queue:
            current_id, d, weight = queue.popleft()
            if d > depth or current_id in visited:
                continue
            visited.add(current_id)

            conditions = []
            params = []

            if direction in ("outgoing", "both"):
                conditions.append("source_id = ?")
                params.append(current_id)
            if direction in ("incoming", "both"):
                conditions.append("target_id = ?")
                params.append(current_id)

            where_dir = " OR ".join(conditions)
            if link_type:
                where_dir += " AND link_type = ?"
                params.append(link_type)

            links = self._store.conn.execute(
                f"SELECT * FROM memory_links WHERE {where_dir}",
                params,
            ).fetchall()

            for link in links:
                target = link["target_id"] if link["source_id"] == current_id else link["source_id"]
                if target not in visited:
                    link_meta[target] = {
                        "_link_weight": weight * link["weight"],
                        "_link_type": link["link_type"],
                        "_link_depth": d,
                    }
                    queue.append((target, d + 1, weight * link["weight"]))

        fetch_ids = [mid for mid in link_meta if mid != memory_id]
        if not fetch_ids:
            return []

        memories_map = self._store.get_memories(fetch_ids)
        results = []
        for mid in fetch_ids:
            mem = memories_map.get(mid)
            if mem:
                mem.update(link_meta[mid])
                results.append(mem)
        return results[:limit]

    def delete_link(self, source_id, target_id, link_type=None):
        """Delete a link between memories.

        Args:
            source_id: Source memory ID.
            target_id: Target memory ID.
            link_type: Optional link type filter.

        Returns:
            True on success.
        """
        if link_type:
            with self._store.transaction() as conn:
                conn.execute(
                    "DELETE FROM memory_links WHERE source_id = ? AND target_id = ? AND link_type = ?",
                    (source_id, target_id, link_type),
                )
        else:
            with self._store.transaction() as conn:
                conn.execute(
                    "DELETE FROM memory_links WHERE source_id = ? AND target_id = ?",
                    (source_id, target_id),
                )
        self._store._invalidate_cache()
        return True
