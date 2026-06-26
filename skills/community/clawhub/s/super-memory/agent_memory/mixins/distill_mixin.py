from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class DistillMixin:
    def distill(self, force: bool = False) -> dict:
        """
        手动触发记忆蒸馏。

        将原始对话记忆逐层抽象为结构化知识：
        原始记忆 → 主题摘要 → 知识图谱 → 个人百科

        参数:
            force: 强制全量重新蒸馏（忽略增量阈值）

        返回: 各层蒸馏结果
        """
        return self.distiller.distill(force=force)

    def get_distill_stats(self) -> dict:
        """获取蒸馏系统统计"""
        return self.distiller.get_distill_stats()