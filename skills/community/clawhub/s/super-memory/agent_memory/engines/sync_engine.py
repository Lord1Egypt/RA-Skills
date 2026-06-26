"""
engines/sync_engine.py — Distributed Memory Synchronization

Provides eventual consistency between multiple AgentMemory instances
using CRDT-inspired conflict-free merge strategies.
"""

from dataclasses import dataclass, field
from typing import Optional, Callable
import time
import json
import hashlib
import logging

logger = logging.getLogger(__name__)


@dataclass
class SyncNode:
    node_id: str
    db_path: str
    last_sync: float = 0.0
    vector_clock: dict = field(default_factory=dict)
    status: str = "active"


@dataclass
class SyncOperation:
    op_type: str
    memory_id: str
    node_id: str
    timestamp: float
    vector_clock: dict
    data: dict = field(default_factory=dict)
    checksum: str = ""


@dataclass
class SyncResult:
    source_node: str
    target_node: str
    operations_applied: int
    conflicts_resolved: int
    operations_rejected: int
    duration_ms: float
    errors: list = field(default_factory=list)


class VectorClock:

    def __init__(self, node_id: str, clock: dict = None):
        self.node_id = node_id
        self.clock = dict(clock or {})

    def increment(self):
        self.clock[self.node_id] = self.clock.get(self.node_id, 0) + 1

    def merge(self, other: dict):
        for k, v in other.items():
            self.clock[k] = max(self.clock.get(k, 0), v)

    def happens_before(self, other: dict) -> bool:
        all_leq = True
        any_lt = False
        for k in set(list(self.clock.keys()) + list(other.keys())):
            a = self.clock.get(k, 0)
            b = other.get(k, 0)
            if a > b:
                all_leq = False
            if a < b:
                any_lt = True
        return all_leq and any_lt

    def is_concurrent(self, other: dict) -> bool:
        return not self.happens_before(other) and not VectorClock(self.node_id, other).happens_before(self.clock)

    def to_dict(self) -> dict:
        return dict(self.clock)


class CRDTMemory:

    @staticmethod
    def merge_memories(local: dict, remote: dict) -> dict:
        merged = dict(local)

        local_ts = local.get("updated_at", local.get("created_at", 0))
        remote_ts = remote.get("updated_at", remote.get("created_at", 0))

        if remote_ts > local_ts:
            for key in ["content", "importance", "nature_code", "quality_score"]:
                if key in remote:
                    merged[key] = remote[key]

        local_topics = set(local.get("topics", []))
        remote_topics = set(remote.get("topics", []))
        merged["topics"] = list(local_topics | remote_topics)

        local_tools = set(local.get("tool_codes", []))
        remote_tools = set(remote.get("tool_codes", []))
        merged["tool_codes"] = list(local_tools | remote_tools)

        merged["quality_score"] = max(
            local.get("quality_score", 0.5),
            remote.get("quality_score", 0.5)
        )

        local_emotion = local.get("emotion", {})
        remote_emotion = remote.get("emotion", {})
        if remote_emotion.get("timestamp", 0) > local_emotion.get("timestamp", 0):
            merged["emotion"] = remote_emotion
        else:
            merged["emotion"] = local_emotion

        local_vc = local.get("_vector_clock", {})
        remote_vc = remote.get("_vector_clock", {})
        merged_vc = {}
        for k in set(list(local_vc.keys()) + list(remote_vc.keys())):
            merged_vc[k] = max(local_vc.get(k, 0), remote_vc.get(k, 0))
        merged["_vector_clock"] = merged_vc

        return merged


class SyncEngine:

    SYNC_BATCH_SIZE = 100

    def __init__(self, store, node_id: str = "local"):
        self.store = store
        self.node_id = node_id
        self.vector_clock = VectorClock(node_id)
        self._peers: dict = {}
        self._sync_log: list = []
        self._pending_ops: list = []

    def add_peer(self, node_id: str, db_path: str):
        self._peers[node_id] = SyncNode(node_id=node_id, db_path=db_path)

    def remove_peer(self, node_id: str):
        self._peers.pop(node_id, None)

    def list_peers(self) -> list:
        return [
            {"node_id": p.node_id, "last_sync": p.last_sync, "status": p.status}
            for p in self._peers.values()
        ]

    def get_changes_since(self, since_timestamp: float, limit: int = 100) -> list:
        changes = []
        try:
            rows = self.store.execute_sql(
                "SELECT * FROM memories WHERE updated_at > ? OR created_at > ? ORDER BY created_at DESC LIMIT ?",
                (since_timestamp, since_timestamp, limit),
                fetch=True,
            )
            for row in rows:
                changes.append(dict(row))
        except Exception as e:
            logger.warning("获取变更失败: %s", e)
        return changes

    def sync_with_peer(self, peer_engine, direction: str = "bidirectional") -> dict:
        """Sync with another SyncEngine instance.

        Args:
            peer_engine: Another SyncEngine instance (not a SyncNode)
            direction: "push", "pull", or "bidirectional"
        """
        if not isinstance(peer_engine, SyncEngine):
            raise TypeError("peer_engine must be a SyncEngine instance")

        result = {"pushed": 0, "pulled": 0, "conflicts": 0}

        if direction in ("push", "bidirectional"):
            changes = self.get_changes_since(self._get_last_sync_with(peer_engine.node_id))
            for change in changes:
                try:
                    peer_engine.apply_remote_changes([change])
                    result["pushed"] += 1
                except Exception as e:
                    logger.debug("sync push conflict: %s", e)
                    result["conflicts"] += 1

        if direction in ("pull", "bidirectional"):
            last_sync = self._get_last_sync_with(peer_engine.node_id)
            changes = peer_engine.get_changes_since(last_sync)
            for change in changes:
                try:
                    self.apply_remote_changes([change])
                    result["pulled"] += 1
                except Exception as e:
                    logger.debug("sync pull conflict: %s", e)
                    result["conflicts"] += 1

        # Record sync
        self._record_sync(peer_engine.node_id, result)
        return result

    def _get_last_sync_with(self, peer_id: str) -> float:
        """Get the timestamp of last sync with a peer."""
        try:
            rows = self.store.execute_sql(
                "SELECT synced_at FROM sync_history WHERE peer_agent_id = ? ORDER BY synced_at DESC LIMIT 1",
                (peer_id,),
                fetch=True,
            )
            if rows:
                row = rows[0]
                return row["synced_at"]
        except Exception:
            pass
        # Fallback: check sync log for SyncResult entries
        for r in reversed(self._sync_log):
            if isinstance(r, SyncResult) and r.target_node == peer_id:
                # Use the sync log entry's creation time as approximation
                return time.time() - (r.duration_ms / 1000.0) if r.duration_ms > 0 else 0.0
        return 0.0

    def _record_sync(self, peer_agent_id: str, result: dict):
        """Record a sync event for future timestamp lookups."""
        try:
            self.store.register_schema("sync_history", """
                CREATE TABLE IF NOT EXISTS sync_history (
                    peer_agent_id TEXT,
                    synced_at REAL,
                    result TEXT
                );
            """)
            self.store.execute_sql(
                "INSERT INTO sync_history (peer_agent_id, synced_at, result) VALUES (?, ?, ?)",
                (peer_agent_id, time.time(), json.dumps(result)),
            )
        except Exception as e:
            logger.debug("_record_sync: %s", e)

    def sync_all(self) -> list:
        results = []
        for peer_id in list(self._peers.keys()):
            try:
                result = self.sync_with_peer(peer_id)
                results.append(result)
            except Exception as e:
                logger.warning("同步 %s 失败: %s", peer_id, e)
                results.append(SyncResult(
                    source_node=self.node_id,
                    target_node=peer_id,
                    operations_applied=0,
                    conflicts_resolved=0,
                    operations_rejected=0,
                    duration_ms=0,
                    errors=[str(e)],
                ))
        return results

    def apply_remote_changes(self, changes: list) -> dict:
        applied = 0
        conflicts = 0
        rejected = 0

        for change in changes:
            memory_id = change.get("memory_id", "")
            if not memory_id:
                rejected += 1
                continue

            local_mem = self.store.get_memory(memory_id)

            if local_mem is None:
                try:
                    self.store.store(
                        content=change.get("content", ""),
                        topics=change.get("topics", []),
                        importance=change.get("importance", "medium"),
                        memory_id=memory_id,
                    )
                    applied += 1
                except Exception as e:
                    logger.debug("apply_change insert_memory: %s", e)
                    rejected += 1
            else:
                merged = CRDTMemory.merge_memories(local_mem, change)

                local_vc = local_mem.get("_vector_clock", {})
                remote_vc = change.get("_vector_clock", {})
                vc = VectorClock(self.node_id, local_vc)

                if vc.is_concurrent(remote_vc):
                    conflicts += 1

                try:
                    self.store.update_memory(memory_id, merged)
                    applied += 1
                except Exception as e:
                    logger.debug("apply_change update_memory: %s", e)
                    rejected += 1

        self.vector_clock.increment()

        return {
            "applied": applied,
            "conflicts": conflicts,
            "rejected": rejected,
        }

    def create_checkpoint(self) -> dict:
        return {
            "node_id": self.node_id,
            "vector_clock": self.vector_clock.to_dict(),
            "peers": {k: {"last_sync": v.last_sync, "vector_clock": v.vector_clock}
                     for k, v in self._peers.items()},
            "timestamp": time.time(),
            "pending_ops": len(self._pending_ops),
        }

    def restore_from_checkpoint(self, checkpoint: dict):
        self.node_id = checkpoint.get("node_id", self.node_id)
        self.vector_clock = VectorClock(self.node_id, checkpoint.get("vector_clock", {}))
        for peer_id, peer_data in checkpoint.get("peers", {}).items():
            if peer_id in self._peers:
                self._peers[peer_id].last_sync = peer_data.get("last_sync", 0)
                self._peers[peer_id].vector_clock = peer_data.get("vector_clock", {})

    def get_stats(self) -> dict:
        return {
            "node_id": self.node_id,
            "peers": len(self._peers),
            "vector_clock": self.vector_clock.to_dict(),
            "syncs_completed": len(self._sync_log),
            "pending_operations": len(self._pending_ops),
        }
