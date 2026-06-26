from __future__ import annotations

"""
integration.bridge - OpenClaw Integration Unified Module

Combines all OpenClaw integration components into a single module:

  - MemoryFormat / MemoryAdapter   (from memory_adapter)
  - MemoryBridge / get_memory_bridge / check_network_accessibility  (from memory_bridge)
  - AgentMemoryPlugin / get_memory_plugin / close_memory_plugin  (deprecated — thin alias for MemoryBridge)
  - MemoryService / get_memory_service  (deprecated — thin alias for MemoryBridge)
  - OpenClawIntegration / create_openclaw_integration  (from openclaw_integration)
  - SyncCoordinator / SourceTracker / SyncWriteLog / ConflictResolver  (from sync_coordinator)

Security notes:
  - smart_memory module is an optional extension, disabled by default.
    It is only enabled when smart_memory.py exists in the plugin directory.
  - Sync operations share memory content across Agent boundaries.
    Only enable sync for trusted Agents/workspaces, and review synced content.
    Default sync_enabled=False; must be explicitly enabled.
"""

import time
import hashlib
import logging
import socket
import threading
import os
from pathlib import Path
from typing import Optional, Dict, List, Any, Set
from collections import OrderedDict

logger = logging.getLogger(__name__)

_package_dir = Path(__file__).parent.parent


# ---------------------------------------------------------------------------
# memory_adapter: MemoryFormat / AgentMemoryFormat / OpenClawFormat / HermesFormat / MemoryAdapter
# ---------------------------------------------------------------------------

class MemoryFormat:
    """Enumeration of supported memory source formats."""

    AGENT_MEMORY = "agent_memory"
    OPENCLAW = "openclaw"
    HERMES = "hermes"
    UNKNOWN = "unknown"


class AgentMemoryFormat:
    """Agent Memory native format normalizer."""

    @staticmethod
    def normalize(data: dict) -> dict:
        return {
            "content": data.get("content", ""),
            "importance": data.get("importance", "medium"),
            "topics": data.get("topics"),
            "nature_code": data.get("nature_code"),
            "tool_codes": data.get("tool_codes"),
            "knowledge_codes": data.get("knowledge_codes"),
            "owner_agent_id": data.get("owner_agent_id", "_system"),
            "visibility": data.get("visibility", "team"),
            "person_code": data.get("person_code", "main"),
            "source": data.get("source", MemoryFormat.AGENT_MEMORY),
            "source_id": data.get("source_id"),
            "source_timestamp": data.get("source_timestamp", time.time()),
        }


class OpenClawFormat:
    """OpenClaw memory format normalizer."""

    IMPORTANCE_MAP = {
        "critical": "high",
        "high": "high",
        "medium": "medium",
        "low": "low",
        "info": "medium",
    }

    VISIBILITY_MAP = {
        "private": "private",
        "team": "team",
        "org": "team",
        "public": "public",
        "global": "public",
    }

    @staticmethod
    def normalize(data: dict) -> dict:
        metadata = data.get("metadata", {})
        text = data.get("text", data.get("content", ""))

        importance = OpenClawFormat.IMPORTANCE_MAP.get(
            data.get("priority", "medium"), "medium"
        )

        visibility = OpenClawFormat.VISIBILITY_MAP.get(
            data.get("scope", "team"), "team"
        )

        tags = data.get("tags", metadata.get("tags", []))
        topics = tags if isinstance(tags, list) else [tags] if tags else None

        source_id = data.get("id", data.get("memory_id"))
        if not source_id:
            source_id = "oc_" + hashlib.md5(text.encode()).hexdigest()[:12]

        return {
            "content": text,
            "importance": importance,
            "topics": topics,
            "nature_code": metadata.get("nature_code"),
            "tool_codes": metadata.get("tool_codes"),
            "knowledge_codes": metadata.get("knowledge_codes"),
            "owner_agent_id": data.get("agent_id", metadata.get("agent_id", "_openclaw")),
            "visibility": visibility,
            "person_code": data.get("person", metadata.get("person", "main")),
            "source": MemoryFormat.OPENCLAW,
            "source_id": source_id,
            "source_timestamp": data.get("timestamp", metadata.get("timestamp", time.time())),
        }


class HermesFormat:
    """Hermes agent memory format normalizer."""

    IMPORTANCE_MAP = {
        "critical": "high",
        "important": "high",
        "normal": "medium",
        "low": "low",
    }

    @staticmethod
    def normalize(data: dict) -> dict:
        message = data.get("message", data.get("content", ""))
        role = data.get("role", "user")
        context = data.get("context", "")
        session_id = data.get("session_id", "")

        if context and context != message:
            content = f"[{role}@{session_id}] {message}\nContext: {context}"
        else:
            content = f"[{role}@{session_id}] {message}" if session_id else message

        metadata = data.get("metadata", {})
        importance = HermesFormat.IMPORTANCE_MAP.get(
            data.get("priority", metadata.get("priority", "normal")), "medium"
        )

        topics = data.get("topics", metadata.get("topics"))
        if isinstance(topics, str):
            topics = [t.strip() for t in topics.split(",") if t.strip()]

        source_id = data.get("id", data.get("memory_id"))
        if not source_id:
            source_id = "hm_" + hashlib.md5(content.encode()).hexdigest()[:12]

        return {
            "content": content,
            "importance": importance,
            "topics": topics,
            "nature_code": metadata.get("nature_code"),
            "tool_codes": metadata.get("tool_codes"),
            "knowledge_codes": metadata.get("knowledge_codes"),
            "owner_agent_id": data.get("agent_id", metadata.get("agent_id", "_hermes")),
            "visibility": data.get("visibility", "team"),
            "person_code": data.get("person", metadata.get("person", "main")),
            "source": MemoryFormat.HERMES,
            "source_id": source_id,
            "source_timestamp": data.get("timestamp", metadata.get("timestamp", time.time())),
        }


class MemoryAdapter:
    """
    Unified memory write adapter.

    Normalizes memory data from any source (Agent Memory, OpenClaw, Hermes)
    into Agent Memory's internal format, with source attribution.

    Usage::

        adapter = MemoryAdapter()

        # Auto-detect format
        normalized = adapter.adapt(raw_data)

        # Explicit format
        normalized = adapter.adapt(raw_data, source="openclaw")

        # Write through adapter
        result = adapter.write(memory_system, raw_data, source="hermes")
    """

    FORMAT_NORMALIZERS = {
        MemoryFormat.AGENT_MEMORY: AgentMemoryFormat.normalize,
        MemoryFormat.OPENCLAW: OpenClawFormat.normalize,
        MemoryFormat.HERMES: HermesFormat.normalize,
    }

    DETECTION_RULES = [
        (lambda d: "text" in d or "scope" in d or "tags" in d, MemoryFormat.OPENCLAW),
        (lambda d: "message" in d or "session_id" in d or "role" in d, MemoryFormat.HERMES),
        (lambda d: "content" in d, MemoryFormat.AGENT_MEMORY),
    ]

    def detect_format(self, data: dict) -> str:
        """Auto-detect the source format of a memory dict."""
        if "source" in data and data["source"] in self.FORMAT_NORMALIZERS:
            return data["source"]

        for rule, fmt in self.DETECTION_RULES:
            try:
                if rule(data):
                    return fmt
            except (KeyError, TypeError):
                continue

        return MemoryFormat.UNKNOWN

    def adapt(self, data: dict, source: str = None) -> dict:
        """Normalize a memory dict into Agent Memory internal format."""
        fmt = source or self.detect_format(data)

        normalizer = self.FORMAT_NORMALIZERS.get(fmt)
        if not normalizer:
            logger.warning(f"Unknown memory format: {fmt}, treating as agent_memory")
            normalizer = AgentMemoryFormat.normalize

        normalized = normalizer(data)
        normalized["_detected_format"] = fmt
        return normalized

    def write(self, memory_system, data: dict, source: str = None, **kwargs) -> dict:
        """Normalize and write a memory through the adapter."""
        normalized = self.adapt(data, source)

        content = normalized["content"]
        if not content or not content.strip():
            return {"written": False, "reason": "empty_content_after_adaptation"}

        return memory_system.remember(
            content=content,
            importance=normalized.get("importance", "medium"),
            topics=normalized.get("topics"),
            nature_code=normalized.get("nature_code"),
            tool_codes=normalized.get("tool_codes"),
            knowledge_codes=normalized.get("knowledge_codes"),
            owner_agent_id=normalized.get("owner_agent_id", "_system"),
            visibility=normalized.get("visibility", "team"),
            person_code=normalized.get("person_code", "main"),
            **kwargs,
        )

    def batch_write(self, memory_system, data_list: list, source: str = None) -> list:
        """Normalize and write a batch of memories."""
        results = []
        for data in data_list:
            result = self.write(memory_system, data, source=source)
            results.append(result)
        return results


# ---------------------------------------------------------------------------
# sync_coordinator: SourceTracker / SyncWriteLog / ConflictResolver / SyncCoordinator
# ---------------------------------------------------------------------------

SOURCE_PRIORITY = {
    "agent_memory": 2,
    "openclaw": 1,
    "hermes": 1,
}

CIRCULAR_SYNC_WINDOW = 300


class SourceTracker:
    """Tracks the origin of each memory to prevent circular sync."""

    def __init__(self, max_entries: int = 10000):
        self._lock = threading.Lock()
        self._source_map: OrderedDict[str, dict] = OrderedDict()
        self._max_entries = max_entries

    def record(self, memory_id: str, source: str, source_id: str = None):
        with self._lock:
            self._source_map[memory_id] = {
                "source": source,
                "source_id": source_id,
                "recorded_at": time.time(),
            }
            if len(self._source_map) > self._max_entries:
                oldest = next(iter(self._source_map))
                del self._source_map[oldest]

    def get_source(self, memory_id: str) -> Optional[dict]:
        with self._lock:
            return self._source_map.get(memory_id)

    def find_by_source_id(self, source_id: str) -> Optional[str]:
        with self._lock:
            for mid, info in self._source_map.items():
                if info.get("source_id") == source_id:
                    return mid
        return None

    def is_from_source(self, memory_id: str, source: str) -> bool:
        with self._lock:
            info = self._source_map.get(memory_id)
            return info is not None and info.get("source") == source


class SyncWriteLog:
    """Records recent sync writes to prevent circular sync."""

    def __init__(self, window: float = CIRCULAR_SYNC_WINDOW):
        self._lock = threading.Lock()
        self._window = window
        self._log: OrderedDict[str, float] = OrderedDict()

    def record(self, content_hash: str, direction: str):
        key = f"{content_hash}:{direction}"
        with self._lock:
            self._log[key] = time.time()
            self._cleanup()

    def was_recently_synced(self, content_hash: str, direction: str) -> bool:
        key = f"{content_hash}:{direction}"
        with self._lock:
            ts = self._log.get(key)
            if ts is None:
                return False
            if time.time() - ts > self._window:
                del self._log[key]
                return False
            return True

    def _cleanup(self):
        now = time.time()
        expired = [k for k, v in self._log.items() if now - v > self._window]
        for k in expired:
            del self._log[k]


class ConflictResolver:
    """Resolves conflicts between memories from different sources."""

    STRATEGY_NEWEST_WINS = "newest_wins"
    STRATEGY_PRIORITY_WINS = "priority_wins"
    STRATEGY_MERGE = "merge"

    def __init__(self, strategy: str = STRATEGY_NEWEST_WINS):
        self.strategy = strategy

    def resolve(self, local: dict, remote: dict, remote_source: str) -> dict:
        if self.strategy == self.STRATEGY_NEWEST_WINS:
            return self._resolve_by_timestamp(local, remote, remote_source)
        elif self.strategy == self.STRATEGY_PRIORITY_WINS:
            return self._resolve_by_priority(local, remote, remote_source)
        elif self.strategy == self.STRATEGY_MERGE:
            return self._resolve_by_merge(local, remote, remote_source)
        return remote

    def _resolve_by_timestamp(self, local: dict, remote: dict, remote_source: str) -> dict:
        local_ts = local.get("time_ts", 0)
        remote_ts = remote.get("source_timestamp", remote.get("time_ts", 0))

        if remote_ts > local_ts:
            logger.info(f"Conflict resolved: remote ({remote_source}) newer ({remote_ts} > {local_ts})")
            return remote
        elif local_ts > remote_ts:
            logger.info(f"Conflict resolved: local newer ({local_ts} > {remote_ts})")
            return local
        else:
            return self._resolve_by_priority(local, remote, remote_source)

    def _resolve_by_priority(self, local: dict, remote: dict, remote_source: str) -> dict:
        local_prio = SOURCE_PRIORITY.get(local.get("source", "agent_memory"), 0)
        remote_prio = SOURCE_PRIORITY.get(remote_source, 0)

        if remote_prio > local_prio:
            return remote
        return local

    def _resolve_by_merge(self, local: dict, remote: dict, remote_source: str) -> dict:
        merged = dict(local)
        remote_content = remote.get("content", "")
        local_content = merged.get("content", "")

        if len(remote_content) > len(local_content):
            merged["content"] = remote_content

        remote_topics = remote.get("topics", [])
        local_topics = merged.get("topics", [])
        if remote_topics:
            all_topics = list(set(local_topics + remote_topics))
            merged["topics"] = all_topics

        merged["sources"] = list(set(
            merged.get("sources", [local.get("source", "agent_memory")]) + [remote_source]
        ))
        merged["merged_at"] = time.time()

        return merged


class SyncCoordinator:
    """
    Coordinates memory synchronization between Agent Memory and external systems.

    Prevents:
      - Dual-write duplicates
      - Circular sync loops
      - Unresolved conflicts

    Usage::

        coordinator = SyncCoordinator(memory_system)

        # Write from external source (OpenClaw/Hermes)
        result = coordinator.write_from_source(data, source="openclaw")

        # Sync from external system
        result = coordinator.sync_from_external(memories, source="hermes")

        # Check if a memory should be synced out
        should_sync = coordinator.should_sync_out(memory_id, target="openclaw")
    """

    def __init__(self, memory_system, conflict_strategy: str = ConflictResolver.STRATEGY_NEWEST_WINS):
        self.memory = memory_system
        self.source_tracker = SourceTracker()
        self.write_log = SyncWriteLog()
        self.conflict_resolver = ConflictResolver(strategy=conflict_strategy)
        self._lock = threading.Lock()

    def write_from_source(self, data: dict, source: str, adapter=None) -> dict:
        """Write a memory from an external source, with dedup and conflict check.

        Args:
            data: Raw memory data from external source
            source: Source system (openclaw/hermes)
            adapter: Optional MemoryAdapter instance

        Returns:
            dict with write result
        """
        if adapter:
            normalized = adapter.adapt(data, source=source)
        else:
            normalized = MemoryAdapter().adapt(data, source=source)

        content = normalized.get("content", "")
        if not content or not content.strip():
            return {"written": False, "reason": "empty_content", "source": source}

        content_hash = hashlib.sha256(content.encode()).hexdigest()

        if self.write_log.was_recently_synced(content_hash, f"{source}->local"):
            return {"written": False, "reason": "circular_sync_prevented", "source": source}

        source_id = normalized.get("source_id")
        if source_id:
            existing = self.source_tracker.find_by_source_id(source_id)
            if existing:
                return {"written": False, "reason": "already_synced", "source": source, "existing_memory_id": existing}

        result = self.memory.remember(
            content=content,
            importance=normalized.get("importance", "medium"),
            topics=normalized.get("topics"),
            nature_code=normalized.get("nature_code"),
            owner_agent_id=normalized.get("owner_agent_id", f"_{source}"),
            visibility=normalized.get("visibility", "team"),
        )

        if result.get("written"):
            memory_id = result.get("memory_id", "")
            self.source_tracker.record(memory_id, source, source_id)
            self.write_log.record(content_hash, f"{source}->local")
            result["source"] = source
            result["source_id"] = source_id

        return result

    def sync_from_external(self, memories: list, source: str, adapter=None) -> dict:
        """Batch sync memories from an external source.

        Returns:
            dict with sync statistics
        """
        stats = {"total": len(memories), "written": 0, "skipped": 0, "errors": 0}

        for mem in memories:
            try:
                result = self.write_from_source(mem, source, adapter)
                if result.get("written"):
                    stats["written"] += 1
                else:
                    stats["skipped"] += 1
            except Exception as e:
                logger.error(f"Sync error from {source}: {e}")
                stats["errors"] += 1

        logger.info(f"Sync from {source}: {stats}")
        return stats

    def should_sync_out(self, memory_id: str, target: str) -> bool:
        """Check if a memory should be synced out to an external system.

        Prevents circular sync: if a memory was originally from the target
        system, don't sync it back.
        """
        source_info = self.source_tracker.get_source(memory_id)
        if source_info and source_info.get("source") == target:
            return False

        return True

    def get_unsynced_memories(self, source: str, since_ts: int = 0, limit: int = 100) -> list:
        """Get local memories that haven't been synced to the given source."""
        try:
            store = self.memory.store
            rows = store.conn.execute(
                "SELECT * FROM memories WHERE time_ts > ? ORDER BY time_ts DESC LIMIT ?",
                (since_ts, limit),
            ).fetchall()

            unsynced = []
            for row in rows:
                mem = dict(row)
                mid = mem.get("memory_id", "")
                if self.should_sync_out(mid, source):
                    unsynced.append(mem)

            return unsynced
        except Exception as e:
            logger.error(f"Failed to get unsynced memories: {e}")
            return []

    def resolve_conflict(self, local_memory: dict, remote_memory: dict, remote_source: str) -> dict:
        """Resolve a conflict between local and remote versions of a memory."""
        return self.conflict_resolver.resolve(local_memory, remote_memory, remote_source)


# ---------------------------------------------------------------------------
# openclaw_integration: OpenClawIntegration / create_openclaw_integration
# ---------------------------------------------------------------------------

class OpenClawIntegration:
    """
    OpenClaw deep integration.

    Implements unified memory interface, bidirectional data sync,
    and intelligent system switching.

    Security: Sync operations share memory content across Agent boundaries.
    Only enable sync for trusted Agents/workspaces. Default sync_enabled=False.
    """

    def __init__(self, memory_bridge, openclaw_api=None, openclaw_llm=None):
        self.memory_bridge = memory_bridge
        self.openclaw_api = openclaw_api
        self.openclaw_llm = openclaw_llm
        self.is_connected = False
        self.sync_interval = 300
        self.last_sync_time = 0
        self.sync_enabled = False

    def connect(self, openclaw_api) -> Dict:
        """Connect to OpenClaw.

        Args:
            openclaw_api: OpenClaw API instance

        Returns:
            dict: Connection result
        """
        try:
            self.openclaw_api = openclaw_api
            self.is_connected = True
            logger.info("成功连接到OpenClaw")
            return {"success": True, "message": "成功连接到OpenClaw"}
        except Exception as e:
            logger.error(f"连接OpenClaw失败: {e}")
            return {"success": False, "message": f"连接失败: {str(e)}"}

    def sync_memory(self, coordinator=None) -> Dict:
        """Synchronize memory bidirectionally (OpenClaw <-> Memory System).

        Security: Sync shares memory content across systems.
        Only enable in trusted environments; review synced content.

        Args:
            coordinator: SyncCoordinator instance (prevents dual-write and circular sync)
        """
        if not self.is_connected or not self.sync_enabled:
            return {"success": False, "message": "未连接到OpenClaw或同步已禁用"}

        logger.warning("Memory sync initiated — data will cross agent boundaries")

        try:
            current_time = time.time()
            if current_time - self.last_sync_time < self.sync_interval:
                return {"success": False, "message": "同步间隔未到"}

            openclaw_memories = self._get_openclaw_memories()
            if openclaw_memories:
                if coordinator:
                    sync_result = coordinator.sync_from_external(
                        openclaw_memories, source="openclaw"
                    )
                    synced_count = sync_result.get("written", 0)
                else:
                    synced_count = self._sync_to_memory_system(openclaw_memories)
            else:
                synced_count = 0

            if coordinator:
                memory_system_memories = coordinator.get_unsynced_memories(
                    source="openclaw", since_ts=int(self.last_sync_time)
                )
            else:
                memory_system_memories = self._get_memory_system_memories()

            if memory_system_memories:
                synced_to_openclaw = self._sync_to_openclaw(memory_system_memories)
            else:
                synced_to_openclaw = 0

            self.last_sync_time = current_time

            return {
                "success": True,
                "message": f"同步完成",
                "synced_to_memory_system": synced_count,
                "synced_to_openclaw": synced_to_openclaw,
            }
        except Exception as e:
            logger.error(f"同步失败: {e}")
            return {"success": False, "message": f"同步失败"}

    def _get_openclaw_memories(self) -> List[Dict]:
        """Fetch memories from OpenClaw."""
        try:
            if hasattr(self.openclaw_api, "get_memories"):
                return self.openclaw_api.get_memories()
            return []
        except Exception as e:
            logger.warning("openclaw_integration: %s", e)
            return []

    def _get_memory_system_memories(self) -> List[Dict]:
        """Fetch memories from the memory system."""
        try:
            result = self.memory_bridge.recall(limit=50)
            return result.get("primary", [])
        except Exception as e:
            logger.warning("openclaw_integration: %s", e)
            return []

    def _sync_to_memory_system(self, openclaw_memories: List[Dict]) -> int:
        """Sync memories from OpenClaw into the memory system."""
        synced_count = 0
        for memory in openclaw_memories:
            try:
                content = memory.get("content", "")
                if content:
                    result = self.memory_bridge.remember(
                        content=content,
                        importance=memory.get("importance", "medium"),
                        topics=memory.get("topics", ["openclaw"]),
                    )
                    if result.get("memory_result", {}).get("written", False):
                        synced_count += 1
            except Exception as e:
                logger.warning("openclaw_integration: %s", e)
        return synced_count

    def _sync_to_openclaw(self, memory_system_memories: List[Dict]) -> int:
        """Sync memories from the memory system into OpenClaw."""
        synced_count = 0
        for memory in memory_system_memories:
            try:
                content = memory.get("content", "")
                if content:
                    if hasattr(self.openclaw_api, "add_memory"):
                        self.openclaw_api.add_memory(
                            {
                                "content": content,
                                "importance": memory.get("importance", "medium"),
                                "topics": memory.get("topics", ["memory_system"]),
                            }
                        )
                        synced_count += 1
            except Exception as e:
                logger.warning("openclaw_integration: %s", e)
        return synced_count

    def get_combined_memory(self, query: str, limit: int = 10) -> Dict:
        """Retrieve combined memories from both the memory system and OpenClaw.

        Security: Combined retrieval crosses Agent boundaries.
        Only enable for trusted queries; review returned content.
        """
        if self.is_connected:
            logger.info(f"Combined memory query across boundaries: '{query[:50]}'")
        try:
            memory_system_result = self.memory_bridge.recall(query=query, limit=limit)
            memory_system_memories = memory_system_result.get("primary", [])

            openclaw_memories = []
            if self.is_connected:
                if hasattr(self.openclaw_api, "search_memories"):
                    openclaw_memories = self.openclaw_api.search_memories(query, limit=limit)

            combined_memories = memory_system_memories + openclaw_memories

            seen_content = set()
            unique_memories = []
            for memory in combined_memories:
                content = memory.get("content", "")
                if content not in seen_content:
                    seen_content.add(content)
                    unique_memories.append(memory)

            unique_memories.sort(key=lambda x: x.get("time_ts", 0), reverse=True)

            return {
                "success": True,
                "memories": unique_memories[:limit],
                "source_counts": {
                    "memory_system": len(memory_system_memories),
                    "openclaw": len(openclaw_memories),
                },
            }
        except Exception as e:
            logger.error(f"获取合并记忆失败: {e}")
            return {"success": False, "message": f"获取失败: {str(e)}"}

    def enable_sync(self, enabled: bool):
        """Enable or disable sync.

        Security: Enabling sync shares memory content across Agent boundaries.
        Only enable in trusted environments.
        """
        self.sync_enabled = enabled
        if enabled:
            logger.warning("Memory sync ENABLED — data will cross agent boundaries on next sync")
        else:
            logger.info("Memory sync disabled")

    def set_sync_interval(self, interval: int):
        """Set the sync interval in seconds."""
        self.sync_interval = interval
        logger.info(f"同步间隔已设置为 {interval} 秒")

    def get_status(self) -> Dict:
        """Return the current integration status."""
        return {
            "is_connected": self.is_connected,
            "sync_enabled": self.sync_enabled,
            "sync_interval": self.sync_interval,
            "last_sync_time": self.last_sync_time,
            "time_since_last_sync": time.time() - self.last_sync_time,
        }


def create_openclaw_integration(memory_bridge, openclaw_api=None, openclaw_llm=None):
    """Factory function to create an OpenClawIntegration instance.

    Args:
        memory_bridge: MemoryBridge instance
        openclaw_api: Optional OpenClaw API instance
        openclaw_llm: Optional OpenClaw LLM instance

    Returns:
        OpenClawIntegration instance
    """
    return OpenClawIntegration(memory_bridge, openclaw_api, openclaw_llm)


# ---------------------------------------------------------------------------
# memory_bridge: check_network_accessibility / MemoryBridge / get_memory_bridge
# ---------------------------------------------------------------------------

def check_network_accessibility():
    """Check network connectivity by attempting DNS and HTTP connections.

    Returns:
        bool: True if network is accessible, False otherwise
    """
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except Exception:
        try:
            import urllib.request

            urllib.request.urlopen("https://huggingface.co", timeout=3)
            return True
        except Exception:
            return False


class MemoryBridge:
    """
    Memory system bridge class.

    Connects OpenClaw Agents with the memory system.
    Features automatic network detection, intelligent degradation,
    and smart correction detection (signal words + similarity).
    """

    def __init__(self, db_path=None, openclaw_llm=None):
        """Initialize the memory bridge.

        Args:
            db_path: Database path; defaults to <package>/data/memory.db
            openclaw_llm: Optional OpenClaw LLM instance
        """
        if db_path is None:
            data_dir = _package_dir / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "memory.db")

        has_network = check_network_accessibility()
        print(f"🔍 网络检测: {'✅ 可联网' if has_network else '❌ 离线模式'}")

        enable_semantic = has_network

        from memory_system import AgentMemory

        self.memory = AgentMemory(
            db_path=db_path,
            project_dir=str(_package_dir / "config"),
            enable_semantic=enable_semantic,
            enable_filter=True,
            enable_dedup=True,
        )

        try:
            from correction_detector import create_detector

            self.correction_detector = create_detector(
                embedding_store=self.memory.embedding_store if enable_semantic else None
            )
        except ImportError:
            logger.warning("correction_detector module not found, correction detection disabled")
            self.correction_detector = None

        self.smart_trigger = None
        try:
            from smart_memory import create_smart_trigger

            self.smart_trigger = create_smart_trigger(self)
        except ImportError:
            logger.info("smart_memory module not found, smart trigger disabled (this is normal)")

        from feeding_mode import create_feeding_mode

        self.feeding_mode = create_feeding_mode(self)

        from welcome_guide import create_welcome_guide

        self.welcome_guide = create_welcome_guide(self)

        self.openclaw_integration = create_openclaw_integration(self, openclaw_llm=openclaw_llm)

        from smart_config import create_smart_config

        self.config = create_smart_config()

        self.memory_adapter = MemoryAdapter()

        self.sync_coordinator = SyncCoordinator(self.memory)

        self.is_first_time = self.welcome_guide.is_first_time()

        try:
            from media_processor import MediaProcessor

            self.media_processor = MediaProcessor.auto(openclaw_llm=openclaw_llm)
            print("✅ 媒体处理器初始化成功")
        except Exception as e:
            print(f"⚠️ 媒体处理器初始化失败: {e}")
            self.media_processor = None

    def remember(self, content, importance="medium", topics=None, auto_detect_correction=True):
        """Store information with optional automatic correction detection.

        Args:
            content: Memory content
            importance: Importance level (high/medium/low)
            topics: Topic list
            auto_detect_correction: Whether to auto-detect corrections

        Returns:
            dict: Write result + correction detection result
        """
        result = {
            "memory_result": None,
            "correction_detection": None,
        }

        if auto_detect_correction and self.correction_detector:
            recent_memories = self.get_recent_memories(limit=5, time_window_seconds=300)

            correction_result = self.correction_detector.smart_detect(
                new_text=content,
                recent_memories=recent_memories,
                time_window_seconds=300,
            )

            result["correction_detection"] = correction_result

            if correction_result["is_correction"] and correction_result["suggested_action"] == "mark_retracted":
                self.correction_detector.process_correction(self.memory.store, correction_result)

        memory_result = self.memory.remember(content=content, importance=importance, topics=topics)
        result["memory_result"] = memory_result

        if self.smart_trigger and self.config.get("smart_memory.enabled", False):
            trigger_result = self.smart_trigger.on_message(content)
            if trigger_result.get("triggers"):
                result["triggers"] = trigger_result["triggers"]

        return result

    def get_recent_memories(self, limit: int = 5, time_window_seconds: int = 300):
        """Retrieve recent memories within a time window.

        Args:
            limit: Maximum number of memories to return
            time_window_seconds: Time window in seconds

        Returns:
            list: Recent memory list
        """
        time_from = int(time.time()) - time_window_seconds
        result = self.memory.recall(time_from=time_from, limit=limit)
        return result.get("primary", [])

    def recall(self, query, limit=10, time_from=None, time_to=None):
        """Retrieve memories by query.

        Args:
            query: Query content
            limit: Maximum number of results
            time_from: Start timestamp
            time_to: End timestamp

        Returns:
            dict: Recall results
        """
        return self.memory.recall(query=query, limit=limit, time_from=time_from, time_to=time_to)

    def build_context(self, query, max_tokens=800):
        """Build context from a query.

        Args:
            query: Query content
            max_tokens: Maximum token count

        Returns:
            str: Context string
        """
        return self.memory.build_context(query=query, max_tokens=max_tokens)

    def get_persona(self):
        """Get persona profile."""
        return self.memory.get_persona()

    def build_persona(self):
        """Build persona profile."""
        return self.memory.build_persona()

    def apply_role(self, role_id, weight=0.4):
        """Apply role style."""
        return self.memory.apply_role(role_id, weight)

    def list_roles(self):
        """List all roles."""
        return self.memory.list_roles()

    def try_recover_from_fallback(self) -> bool:
        """Attempt to recover from degraded state.

        When previously degraded due to network or dependency issues,
        call this method to attempt recovery.

        Returns:
            bool: Whether recovery was successful
        """
        try:
            if hasattr(self.memory, "embedding_store") and self.memory.embedding_store:
                embedding_recovered = self.memory.embedding_store.try_recover_from_fallback()
            else:
                embedding_recovered = False

            return embedding_recovered
        except Exception as e:
            print(f"恢复失败: {e}")
            return False

    def process_message(self, user_message: str, agent_response: str = None):
        """Process a message and trigger smart operations (requires smart_memory module)."""
        if not self.smart_trigger:
            return {"triggers": [], "error": "smart_memory module not available"}
        return self.smart_trigger.on_message(user_message, agent_response)

    def start_recording(self):
        """Start recording conversation (requires smart_memory module)."""
        if not self.smart_trigger:
            return {"error": "smart_memory module not available"}
        return self.smart_trigger.start_recording()

    def stop_recording(self):
        """Stop recording conversation (requires smart_memory module)."""
        if not self.smart_trigger:
            return {"error": "smart_memory module not available"}
        return self.smart_trigger.stop_recording()

    def summarize_conversation(self):
        """Summarize conversation content (requires smart_memory module)."""
        if not self.smart_trigger:
            return {"error": "smart_memory module not available"}
        return self.smart_trigger.summarize_conversation()

    def save_conversation(self):
        """Save conversation content (requires smart_memory module)."""
        if not self.smart_trigger:
            return {"error": "smart_memory module not available"}
        return self.smart_trigger.save_conversation()

    def start_feeding_mode(self):
        """Start feeding mode.

        Returns:
            dict: Operation result
        """
        return self.feeding_mode.start()

    def feed(self, content: str, content_type: str = "text"):
        """Feed content in feeding mode.

        Args:
            content: Content to feed
            content_type: Content type (text, file, url)

        Returns:
            dict: Feed result
        """
        return self.feeding_mode.feed(content, content_type)

    def check_feeding_inactivity(self):
        """Check if feeding mode has been inactive.

        Returns:
            dict: Activity check result
        """
        return self.feeding_mode.check_inactivity()

    def end_feeding_mode(self):
        """End feeding mode.

        Returns:
            dict: Operation result
        """
        return self.feeding_mode.end()

    def get_feeding_status(self):
        """Get feeding mode status.

        Returns:
            dict: Status information
        """
        return self.feeding_mode.get_status()

    def start_welcome_guide(self):
        """Start welcome guide.

        Returns:
            dict: Guide content
        """
        return self.welcome_guide.start_guide()

    def get_help(self):
        """Get help information.

        Returns:
            dict: Help content
        """
        return self.welcome_guide.get_help()

    def get_about(self):
        """Get system information.

        Returns:
            dict: System information
        """
        return self.welcome_guide.get_about()

    def is_first_time_use(self):
        """Check if this is the first time use.

        Returns:
            bool: Whether this is the first use
        """
        return self.is_first_time

    def connect_openclaw(self, openclaw_api):
        """Connect to OpenClaw.

        Args:
            openclaw_api: OpenClaw API instance

        Returns:
            dict: Connection result
        """
        return self.openclaw_integration.connect(openclaw_api)

    def sync_memory(self):
        """Synchronize memory (via coordinator, preventing dual-write and circular sync).

        Returns:
            dict: Sync result
        """
        if self.sync_coordinator:
            return self.openclaw_integration.sync_memory(coordinator=self.sync_coordinator)
        return self.openclaw_integration.sync_memory()

    def write_from_source(self, data: dict, source: str = "openclaw") -> dict:
        """Write memory from an external system (via adapter + coordinator, preventing dual-write).

        Args:
            data: Raw memory data from external system
            source: Source system (openclaw/hermes)

        Returns:
            dict: Write result
        """
        if self.sync_coordinator:
            return self.sync_coordinator.write_from_source(data, source, adapter=self.memory_adapter)

        if self.memory_adapter:
            return self.memory_adapter.write(self.memory, data, source=source)

        return self.remember(
            data.get("content", data.get("text", data.get("message", ""))),
            importance=data.get("importance", "medium"),
        )

    def sync_from_hermes(self, memories: list) -> dict:
        """Batch sync memories from Hermes Agent.

        Args:
            memories: List of Hermes-format memories

        Returns:
            dict: Sync statistics
        """
        if self.sync_coordinator:
            return self.sync_coordinator.sync_from_external(
                memories, source="hermes", adapter=self.memory_adapter
            )

        stats = {"total": len(memories), "written": 0, "skipped": 0, "errors": 0}
        for mem in memories:
            try:
                result = self.write_from_source(mem, source="hermes")
                if result.get("written"):
                    stats["written"] += 1
                else:
                    stats["skipped"] += 1
            except Exception:
                stats["errors"] += 1
        return stats

    def get_combined_memory(self, query: str, limit: int = 10):
        """Get combined memories from both the memory system and OpenClaw.

        Args:
            query: Query content
            limit: Maximum number of results

        Returns:
            dict: Combined memory results
        """
        return self.openclaw_integration.get_combined_memory(query, limit)

    def enable_sync(self, enabled: bool):
        """Enable or disable sync.

        Args:
            enabled: Whether to enable sync
        """
        self.openclaw_integration.enable_sync(enabled)

    def get_integration_status(self):
        """Get integration status.

        Returns:
            dict: Status information
        """
        return self.openclaw_integration.get_status()

    def get_config(self, key: str, default=None):
        """Get a configuration value.

        Args:
            key: Configuration key
            default: Default value

        Returns:
            Any: Configuration value
        """
        return self.config.get(key, default)

    def set_config(self, key: str, value):
        """Set a configuration value.

        Args:
            key: Configuration key
            value: Configuration value
        """
        self.config.set(key, value)

    def enable_feature(self, feature: str):
        """Enable a feature.

        Args:
            feature: Feature name
        """
        self.config.enable(feature)

    def disable_feature(self, feature: str):
        """Disable a feature.

        Args:
            feature: Feature name
        """
        self.config.disable(feature)

    def get_all_config(self):
        """Get all configuration.

        Returns:
            dict: All configuration
        """
        return self.config.get_all()

    def reset_config(self):
        """Reset configuration to defaults."""
        self.config.reset()

    def close(self):
        """Close resources."""
        if self.memory:
            self.memory.close()


_memory_bridge: Optional[MemoryBridge] = None


def get_memory_bridge():
    """Get the MemoryBridge singleton.

    Returns:
        MemoryBridge: The global MemoryBridge instance
    """
    global _memory_bridge
    if _memory_bridge is None:
        _memory_bridge = MemoryBridge()
    return _memory_bridge


# ---------------------------------------------------------------------------
# memory_plugin: AgentMemoryPlugin — thin alias for MemoryBridge (deprecated)
# ---------------------------------------------------------------------------

class AgentMemoryPlugin(MemoryBridge):
    """Deprecated: use MemoryBridge directly instead.

    This class is now a thin alias for MemoryBridge.
    It will be removed in v11.0.0.
    """
    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "AgentMemoryPlugin is deprecated, use MemoryBridge directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


_memory_plugin: Optional[MemoryBridge] = None


def get_memory_plugin(plugin_config=None):
    """Get the AgentMemoryPlugin singleton.

    Deprecated: use get_memory_bridge() instead.

    Args:
        plugin_config: Ignored (kept for backward compatibility)

    Returns:
        MemoryBridge: The global MemoryBridge instance
    """
    import warnings
    warnings.warn(
        "get_memory_plugin() is deprecated, use get_memory_bridge()",
        DeprecationWarning,
        stacklevel=2,
    )
    global _memory_plugin
    if _memory_plugin is None:
        _memory_plugin = get_memory_bridge()
    return _memory_plugin


def close_memory_plugin():
    """Close and reset the global AgentMemoryPlugin instance.

    Deprecated: close the MemoryBridge directly instead.
    """
    import warnings
    warnings.warn(
        "close_memory_plugin() is deprecated, close the MemoryBridge directly",
        DeprecationWarning,
        stacklevel=2,
    )
    global _memory_plugin
    if _memory_plugin:
        _memory_plugin.close()
        _memory_plugin = None


# ---------------------------------------------------------------------------
# agent_memory_service: MemoryService — thin alias for MemoryBridge (deprecated)
# ---------------------------------------------------------------------------

class MemoryService(MemoryBridge):
    """Deprecated: use MemoryBridge directly instead.

    This class is now a thin alias for MemoryBridge.
    It will be removed in v11.0.0.
    """
    def __init__(self, *args, **kwargs):
        import warnings
        warnings.warn(
            "MemoryService is deprecated, use MemoryBridge directly",
            DeprecationWarning,
            stacklevel=2,
        )
        super().__init__(*args, **kwargs)


def get_memory_service():
    """Get the global MemoryService instance.

    Deprecated: use get_memory_bridge() instead.

    Returns:
        MemoryBridge: The global MemoryBridge instance
    """
    import warnings
    warnings.warn(
        "get_memory_service() is deprecated, use get_memory_bridge()",
        DeprecationWarning,
        stacklevel=2,
    )
    return get_memory_bridge()


# ---------------------------------------------------------------------------
# Public API - all exported names
# ---------------------------------------------------------------------------

__all__ = [
    "MemoryFormat",
    "AgentMemoryFormat",
    "OpenClawFormat",
    "HermesFormat",
    "MemoryAdapter",
    "SourceTracker",
    "SyncWriteLog",
    "ConflictResolver",
    "SyncCoordinator",
    "SOURCE_PRIORITY",
    "CIRCULAR_SYNC_WINDOW",
    "OpenClawIntegration",
    "create_openclaw_integration",
    "check_network_accessibility",
    "MemoryBridge",
    "get_memory_bridge",
    "AgentMemoryPlugin",
    "get_memory_plugin",
    "close_memory_plugin",
    "MemoryService",
    "get_memory_service",
]
