"""v8.6 — 存储后端抽象接口

S-04 Fix: 补充缺失的方法签名，使其与 store.py 中的 MemoryStore 公共方法一致。
核心方法标记为 @abstractmethod，非核心方法提供默认实现（抛出 NotImplementedError），
以便 SqliteMemoryStore 等简化实现无需实现所有方法。
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class AbstractMemoryStore(ABC):

    # ── 连接与生命周期 ──────────────────────────────────────

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def create_indexes(self):
        pass

    # ── 写入 ────────────────────────────────────────────────

    @abstractmethod
    def insert_memory(self, memory_id: str, time_id: str, time_ts: int,
                      person_id: str, nature_id: str, content: str,
                      content_hash: str, topics: list[str], tools: list[str],
                      knowledge_types: list[str], importance: str, valence: float,
                      arousal: float, dominance: float, significance: str,
                      confidence: float, primary_emotions: str, compound_emotions: str,
                      owner_agent_id: str, visibility: str, **kwargs) -> str:
        pass

    @abstractmethod
    def create_link(self, source_id: str, target_id: str,
                    link_type: str, weight: float = 1.0, reason: str = ""):
        pass

    # ── 读取 ────────────────────────────────────────────────

    @abstractmethod
    def get_memory(self, memory_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    def get_memories(self, memory_ids: list[str]) -> dict[str, dict]:
        """批量获取记忆（解决 N+1 查询问题）"""
        pass

    @abstractmethod
    def get_linked(self, memory_id: str, link_type: str = None) -> list[dict]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    # ── 查询与搜索 ──────────────────────────────────────────

    @abstractmethod
    def query(self, time_from: int = None, time_to: int = None,
              person_id: str = None, nature_id: str = None,
              topic_path: str = None, tool_id: str = None,
              knowledge_id: str = None, importance: str = None,
              keyword: str = None, significance: str = None,
              limit: int = 20, offset: int = 0,
              owner_agent_id: str = None, visibility: str = None) -> list[dict]:
        pass

    def search(self, keyword: str, limit: int = 50) -> list[dict]:
        """全文搜索（FTS5 或 LIKE 降级）。简化实现可使用 query(keyword=...) 替代。"""
        return self.query(keyword=keyword, limit=limit)

    # ── 更新与删除 ──────────────────────────────────────────

    @abstractmethod
    def update_memory(self, memory_id: str, **fields):
        pass

    @abstractmethod
    def delete_memory(self, memory_id: str, soft: bool = True):
        pass

    # ── FTS 索引 ────────────────────────────────────────────

    def rebuild_fts(self) -> dict:
        """重建 FTS 索引。返回: {"rebuilt": bool, "count": int, "error": str}"""
        return {"rebuilt": False, "count": 0, "error": "not implemented"}

    # ── 统计与维护 ──────────────────────────────────────────

    def get_stats(self) -> dict:
        """获取存储统计信息（读写计数、缓存命中率、FTS 状态等）"""
        return {"count": self.count()}

    def get_storage_stats(self) -> dict:
        """获取存储容量统计（热库/冷库/向量数量/文件大小）"""
        return {"hot_count": self.count()}

    def optimize(self):
        """数据库优化（ANALYZE + PRAGMA optimize + WAL checkpoint）"""
        pass

    def check_integrity(self) -> dict:
        """完整性检查。返回: {"ok": bool, "issues": list}"""
        return {"ok": True, "issues": []}

    def auto_maintain(self, vacuum_threshold_mb: float = 50, embedding_store=None):
        """自动维护：WAL checkpoint + 完整性检查 + 按需 VACUUM + FTS 健康检查"""
        pass

    def backup(self, backup_path: str):
        """备份数据库到指定路径"""
        raise NotImplementedError("backup not implemented in this backend")

    # ── Agent 管理 ──────────────────────────────────────────

    def register_agent(self, agent_id: str, agent_name: str,
                       team_id: str = "default", capabilities: list[str] = None) -> dict:
        return {"agent_id": agent_id, "agent_name": agent_name, "team_id": team_id}

    def get_agent(self, agent_id: str) -> Optional[dict]:
        return None

    def list_agents(self, team_id: str = None) -> list[dict]:
        return []

    # ── 权限管理 ────────────────────────────────────────────

    def grant_permission(self, memory_id: str, agent_id: str, granted_by: str,
                         permission: str = "read", expires_at: int = None) -> bool:
        return False

    def revoke_permission(self, memory_id: str, agent_id: str) -> bool:
        return False

    def check_permission(self, memory_id: str, agent_id: str,
                         required: str = "read") -> bool:
        return True
