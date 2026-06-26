from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class ReactorMixin:
    def get_pending_notifications(self) -> list[dict]:
        """
        获取待处理的主动通知（由 reactor 创建的任务）。
        Agent 应在对话开始时调用此方法，检查是否有待处理事项。

        返回: [{"task_id", "title", "memory_id", "deadline", ...}, ...]
        """
        return self.reactor.get_pending_notifications(self.store)

    def reactor_scan(self) -> dict:
        """
        手动触发 reactor 全量扫描（矛盾/衰减/决策链）。

        通常不需要手动调用 —— maintain() 会自动执行。
        """
        return self.reactor.scan(
            store=self.store,
            decay=self.decay,
            self_healing=self.self_healing,
            causal=self.causal,
        )