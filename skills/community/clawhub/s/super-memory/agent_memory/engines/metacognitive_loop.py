"""
engines/metacognitive_loop.py - 元认知反馈闭环

评估 → 策略调整 → 更好的检索

当检索结果置信度低时，闭环自动：
1. 降低相似度阈值（扩大搜索范围）
2. 启用激活扩散（发现关联记忆）
3. 增加质量权重（优先高质量记忆）
4. 切换深度评估模式
5. 连续低置信度达到阈值后启用图谱增强

置信度高时，逐步回归默认策略。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional
import time
import logging

logger = logging.getLogger(__name__)


@dataclass
class RecallStrategy:
    """可调检索参数，由元认知反馈驱动更新"""

    limit: int = 10
    similarity_threshold: float = 0.3
    quality_weight: float = 0.3
    spread_enabled: bool = False
    spread_hops: int = 2
    spread_decay: float = 0.6
    use_graph: bool = False

    assess_mode: str = "quick"
    confidence_threshold: float = 0.5

    consecutive_low_confidence: int = 0
    last_adjustment_time: float = 0.0
    adjustment_history: list = field(default_factory=list)

    MAX_CONSECUTIVE_LOW = 3
    ADJUSTMENT_COOLDOWN = 60


class MetacognitiveLoop:
    """
    元认知反馈闭环：评估 → 策略调整 → 更好检索

    当检索结果置信度低时，闭环自动：
    1. 降低相似度阈值（扩大搜索范围）
    2. 启用激活扩散（发现关联记忆）
    3. 增加质量权重（优先高质量记忆）
    4. 切换深度评估模式
    5. 连续 MAX_CONSECUTIVE_LOW 次低置信后启用图谱增强

    置信度高时，逐步回归默认策略。
    """

    DEFAULT_STRATEGY = RecallStrategy()

    def __init__(self, store=None):
        self.store = store
        self._strategies: dict[str, RecallStrategy] = {}
        self._feedback_log: list = []

    def get_strategy(self, agent_id: str = "default") -> RecallStrategy:
        return self._strategies.get(agent_id, RecallStrategy())

    def update_strategy(self, agent_id: str, assessment) -> RecallStrategy:
        strategy = self.get_strategy(agent_id)
        now = time.time()

        if now - strategy.last_adjustment_time < strategy.ADJUSTMENT_COOLDOWN:
            return strategy

        if assessment.confidence < strategy.confidence_threshold:
            strategy.consecutive_low_confidence += 1
            strategy = self._escalate(strategy, assessment)
        else:
            strategy.consecutive_low_confidence = max(0, strategy.consecutive_low_confidence - 1)
            strategy = self._relax(strategy)

        strategy.last_adjustment_time = now
        strategy.adjustment_history.append({
            "time": now,
            "confidence": assessment.confidence,
            "status": assessment.status,
            "consecutive_low": strategy.consecutive_low_confidence,
        })

        self._strategies[agent_id] = strategy
        return strategy

    def _escalate(self, strategy: RecallStrategy, assessment) -> RecallStrategy:
        n = strategy.consecutive_low_confidence

        if n >= 1:
            strategy.similarity_threshold = max(0.1, strategy.similarity_threshold - 0.05)
            strategy.limit = min(30, strategy.limit + 5)
            logger.info("MetacognitiveLoop: 降低阈值到 %.2f, 增加limit到 %d",
                        strategy.similarity_threshold, strategy.limit)

        if n >= 2:
            strategy.spread_enabled = True
            strategy.spread_hops = min(3, strategy.spread_hops + 1)
            strategy.quality_weight = min(0.5, strategy.quality_weight + 0.05)
            logger.info("MetacognitiveLoop: 启用扩散, hops=%d, quality_weight=%.2f",
                        strategy.spread_hops, strategy.quality_weight)

        if n >= strategy.MAX_CONSECUTIVE_LOW:
            strategy.use_graph = True
            strategy.assess_mode = "deep"
            logger.info("MetacognitiveLoop: 启用图谱增强, 切换deep评估")

        if assessment.gaps:
            strategy._targeted_gaps = assessment.gaps

        return strategy

    def _relax(self, strategy: RecallStrategy) -> RecallStrategy:
        defaults = self.DEFAULT_STRATEGY

        strategy.similarity_threshold = min(defaults.similarity_threshold,
                                            strategy.similarity_threshold + 0.02)
        strategy.quality_weight = max(defaults.quality_weight,
                                      strategy.quality_weight - 0.02)

        if strategy.consecutive_low_confidence == 0:
            strategy.spread_enabled = defaults.spread_enabled
            strategy.use_graph = defaults.use_graph
            strategy.assess_mode = defaults.assess_mode

        return strategy

    def record_feedback(self, agent_id: str, query: str, was_helpful: bool):
        self._feedback_log.append({
            "agent_id": agent_id,
            "query": query,
            "helpful": was_helpful,
            "time": time.time(),
        })

        strategy = self.get_strategy(agent_id)
        if not was_helpful:
            strategy.consecutive_low_confidence += 1
            self._strategies[agent_id] = strategy
        else:
            strategy.consecutive_low_confidence = max(0, strategy.consecutive_low_confidence - 1)
            self._strategies[agent_id] = strategy

    def get_current_strategy(self, agent_id: str = "default"):
        """Get the current adjusted strategy for recall engine to consume."""
        return self._strategies.get(agent_id)

    def get_stats(self, agent_id: str = "default") -> dict:
        strategy = self.get_strategy(agent_id)
        return {
            "consecutive_low_confidence": strategy.consecutive_low_confidence,
            "current_threshold": strategy.similarity_threshold,
            "current_limit": strategy.limit,
            "spread_enabled": strategy.spread_enabled,
            "use_graph": strategy.use_graph,
            "assess_mode": strategy.assess_mode,
            "adjustments": len(strategy.adjustment_history),
            "feedback_count": len(self._feedback_log),
        }
