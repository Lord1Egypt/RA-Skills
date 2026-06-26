"""
spirit/memory_partition.py — Memory Partitioning

Automatically separates personal memories from work memories,
enabling privacy control and enterprise offboarding.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PartitionResult:
    """Result of memory partitioning."""
    personal_count: int = 0
    work_count: int = 0
    enterprise_count: int = 0
    unclassified_count: int = 0
    total: int = 0


class MemoryPartition:
    """Partition memories into personal/work/enterprise scopes.

    Uses the existing tenant_id and visibility fields:
    - tenant_id="default" or "personal" → personal
    - tenant_id="work" → work
    - tenant_id starts with "ent_" → enterprise

    For unclassified memories, uses content heuristics to auto-classify.
    """

    # Heuristic keywords for classification
    _WORK_KEYWORDS = {
        "项目", "需求", "会议", "客户", "方案", "代码", "部署", "测试",
        "project", "meeting", "client", "requirement", "deploy", "sprint",
        "standup", "review", "deadline", "任务", "排期",
    }
    _PERSONAL_KEYWORDS = {
        "周末", "家人", "孩子", "旅游", "电影", "游戏", "健身",
        "weekend", "family", "vacation", "movie", "game", "hobby",
        "喜欢", "讨厌", "心情", "感觉",
    }

    def __init__(self, store=None):
        self.store = store

    def classify_memory(self, memory: dict) -> str:
        """Classify a single memory into a scope.

        Returns: "personal", "work", or "enterprise"
        """
        # First check explicit tenant_id
        tenant = memory.get("tenant_id", "default")
        if tenant.startswith("ent_"):
            return "enterprise"
        if tenant in ("work",):
            return "work"
        if tenant in ("personal",):
            return "personal"

        # Check visibility hint
        vis = memory.get("visibility", "")
        if vis == "private":
            return "personal"
        if vis == "team":
            return "work"

        # Check source
        source = memory.get("source", "")
        if source in ("dingtalk", "email", "calendar", "enterprise_wechat"):
            return "work"
        if source in ("wechat", "clipboard"):
            return "personal"

        # Content heuristic
        content = memory.get("content", "").lower()
        work_score = sum(1 for kw in self._WORK_KEYWORDS if kw in content)
        personal_score = sum(1 for kw in self._PERSONAL_KEYWORDS if kw in content)

        if work_score > personal_score:
            return "work"
        elif personal_score > work_score:
            return "personal"

        return "work"  # Default to work (more conservative)

    def partition_all(self, limit: int = 1000) -> PartitionResult:
        """Partition all unclassified memories.

        Updates tenant_id for memories that don't have an explicit scope.
        """
        result = PartitionResult()

        if not self.store:
            return result

        try:
            memories = self.store.query(limit=limit) if hasattr(self.store, 'query') else []
            result.total = len(memories)

            for mem in memories:
                scope = self.classify_memory(mem)
                if scope == "personal":
                    result.personal_count += 1
                elif scope == "work":
                    result.work_count += 1
                elif scope == "enterprise":
                    result.enterprise_count += 1
                else:
                    result.unclassified_count += 1

                # Update tenant_id if not set
                mid = mem.get("id", "")
                current_tenant = mem.get("tenant_id", "default")
                if current_tenant == "default" and mid:
                    try:
                        self.store.update_memory(mid, {"tenant_id": scope})
                    except Exception:
                        pass

        except Exception as e:
            logger.error("Memory partition failed: %s", e)

        return result

    def export_partition(self, scope: str, format: str = "json") -> list[dict]:
        """Export memories of a specific partition (for offboarding).

        Args:
            scope: "personal", "work", or "enterprise"
            format: Export format (currently only "json")

        Returns:
            List of memory dicts in the specified partition
        """
        if not self.store:
            return []

        try:
            memories = self.store.query(limit=10000) if hasattr(self.store, 'query') else []
            return [m for m in memories if self.classify_memory(m) == scope]
        except Exception as e:
            logger.error("Partition export failed: %s", e)
            return []
