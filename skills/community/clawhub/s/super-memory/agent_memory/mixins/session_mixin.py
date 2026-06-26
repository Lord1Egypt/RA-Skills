from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class SessionMixin:
    def l1_add(self, content: str, role: str = "user") -> dict:
        """添加到短期记忆"""
        return self.hierarchy.l1_add(content, role)

    def l1_context(self, max_tokens: int = 1500) -> str:
        """获取短期记忆上下文"""
        return self.hierarchy.l1_context(max_tokens)

    def flush_session(self) -> list[dict]:
        """对话结束：L1 沉淀到 L2（带去重）"""
        result = self.hierarchy.l1_flush_to_l2(self.pipeline, deduplicator=self.dedup)
        self.hierarchy.l1_clear()
        return result