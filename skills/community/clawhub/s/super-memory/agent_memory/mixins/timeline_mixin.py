from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class TimelineMixin:
    def take_snapshot(self, label: str = None, at_ts: int = None, description: str = None) -> dict:
        """创建记忆快照"""
        return self.timeline.take_snapshot(label=label, at_ts=at_ts, description=description)

    def list_snapshots(self, limit: int = 50) -> list[dict]:
        """列出所有快照"""
        return self.timeline.list_snapshots(limit=limit)

    def get_snapshot(self, snapshot_id: str) -> dict | None:
        """获取快照详情"""
        return self.timeline.get_snapshot(snapshot_id)

    def diff_memories(self, from_ts: int = None, to_ts: int = None,
                      from_snapshot: str = None, to_snapshot: str = None,
                      topic: str = None) -> dict:
        """对比两个时间点的记忆差异"""
        return self.timeline.diff(from_ts=from_ts, to_ts=to_ts,
                                  from_snapshot=from_snapshot, to_snapshot=to_snapshot,
                                  topic=topic)

    def diff_natural(self, from_ts: int = None, to_ts: int = None,
                     from_snapshot: str = None, to_snapshot: str = None) -> str:
        """自然语言风格的差异描述"""
        return self.timeline.diff_natural(from_ts=from_ts, to_ts=to_ts,
                                          from_snapshot=from_snapshot, to_snapshot=to_snapshot)

    def blame_memory(self, memory_id: str) -> dict:
        """追溯记忆来源"""
        return self.timeline.blame(memory_id)

    def blame_natural(self, memory_id: str) -> str:
        """自然语言风格的来源描述"""
        return self.timeline.blame_natural(memory_id)

    def get_timeline_stats(self) -> dict:
        """时间旅行系统统计"""
        return self.timeline.get_timeline_stats()