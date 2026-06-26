"""
engines/decay_policy.py - 统一衰减策略配置

将 decay.py / memory_lifecycle.py / memory_tier.py / MaintainEngine 的四套阈值
统一为单一配置源，消除阈值冲突。
"""

from dataclasses import dataclass, field


@dataclass
class DecayPolicy:
    """
    统一衰减策略 — 所有衰减/分层/生命周期模块共享同一配置。

    时间线:
      active (0 ~ dormant_days) → dormant (dormant_days ~ archived_days) → archived (> archived_days)

    重要度修正:
      high:  永不自动衰减
      medium: 标准衰减
      low:   加速衰减 (low_multiplier 倍速)
    """

    dormant_days: int = 30
    archived_days: int = 180
    deleted_days: int = 365

    low_multiplier: float = 0.33
    high_never_decay: bool = True

    merge_similarity_threshold: float = 0.80

    quality_weight_in_decay: float = 0.3

    tier_hot_days: int = 7
    tier_cold_days: int = 30

    @property
    def low_dormant_days(self) -> int:
        return max(7, int(self.dormant_days * self.low_multiplier))

    @property
    def low_archived_days(self) -> int:
        return max(30, int(self.archived_days * self.low_multiplier))

    @property
    def medium_dormant_days(self) -> int:
        return self.dormant_days

    @property
    def medium_archived_days(self) -> int:
        return self.archived_days

    def get_dormant_days(self, importance: str) -> int:
        if importance == "high" and self.high_never_decay:
            return 999999
        if importance == "low":
            return self.low_dormant_days
        return self.dormant_days

    def get_archived_days(self, importance: str) -> int:
        if importance == "high" and self.high_never_decay:
            return 999999
        if importance == "low":
            return self.low_archived_days
        return self.archived_days

    def should_decay(self, age_days: float, importance: str, quality_score: float = 0.5) -> str:
        """
        判断记忆应处于哪个阶段。

        返回: 'active' | 'dormant' | 'archived' | 'deleted'
        """
        if importance == "high" and self.high_never_decay:
            return "active"

        effective_dormant = self.get_dormant_days(importance)
        effective_archived = self.get_archived_days(importance)

        if quality_score > 0.7:
            effective_dormant = int(effective_dormant * 1.5)
            effective_archived = int(effective_archived * 1.5)

        if age_days < effective_dormant:
            return "active"
        if age_days < effective_archived:
            return "dormant"
        if age_days < self.deleted_days:
            return "archived"
        return "deleted"


DEFAULT_DECAY_POLICY = DecayPolicy()
