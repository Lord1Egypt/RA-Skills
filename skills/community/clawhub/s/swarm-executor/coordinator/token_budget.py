"""
全局Token预算器 - 实时监控Tier配额，自动降级机制
"""
import time
from typing import Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import threading
import json


class TierLevel(Enum):
    """Tier分级"""
    TIER_0 = "Tier 0"  # DeepSeek，85%配额
    TIER_1 = "Tier 1"  # qwen-plus，5%配额
    TIER_2 = "Tier 2"  # 豆包，10%配额
    TIER_3 = "Tier 3"  # 兜底模型


@dataclass
class TierQuota:
    """Tier配额配置"""
    tier: TierLevel
    percentage: float  # 百分比配额
    used_tokens: int = 0
    max_tokens: Optional[int] = None  # 可选：绝对Token限制
    auto_downgrade_to: Optional[TierLevel] = None  # 自动降级目标
    
    @property
    def usage_percentage(self) -> float:
        """使用百分比"""
        if self.max_tokens:
            return (self.used_tokens / self.max_tokens) * 100
        return 0.0
    
    @property
    def remaining_tokens(self) -> Optional[int]:
        """剩余Token数量"""
        if self.max_tokens:
            return max(0, self.max_tokens - self.used_tokens)
        return None
    
    def can_use(self, tokens: int) -> bool:
        """检查是否可以使用指定数量的Token"""
        if self.max_tokens:
            return self.used_tokens + tokens <= self.max_tokens
        return True  # 如果没有绝对限制，则始终允许


@dataclass
class TokenUsageRecord:
    """Token使用记录"""
    timestamp: float
    tier: TierLevel
    tokens: int
    agent_id: str
    task_id: str
    success: bool = True


class TokenBudgetManager:
    """全局Token预算管理器"""
    
    def __init__(self, total_budget: Optional[int] = None):
        """
        初始化Token预算管理器
        
        Args:
            total_budget: 总Token预算（可选）
        """
        self.total_budget = total_budget
        self.tier_quotas: Dict[TierLevel, TierQuota] = {}
        self.usage_history: List[TokenUsageRecord] = []
        self._lock = threading.RLock()
        
        # 默认Tier配置（基于AGENTS.md）
        self._setup_default_tiers()
        
        # 自动降级映射
        self._downgrade_map = {
            TierLevel.TIER_0: TierLevel.TIER_1,
            TierLevel.TIER_1: TierLevel.TIER_2,
            TierLevel.TIER_2: TierLevel.TIER_3,
            TierLevel.TIER_3: None  # 无降级目标
        }
    
    def _setup_default_tiers(self):
        """设置默认Tier配置"""
        # 基于AGENTS.md的默认配额
        default_quotas = [
            (TierLevel.TIER_0, 85.0, None),  # 85%配额，无绝对限制
            (TierLevel.TIER_1, 5.0, None),   # 5%配额
            (TierLevel.TIER_2, 10.0, None),  # 10%配额
            (TierLevel.TIER_3, 0.0, None),   # 兜底，0%配额（仅异常使用）
        ]
        
        for tier, percentage, max_tokens in default_quotas:
            self.tier_quotas[tier] = TierQuota(
                tier=tier,
                percentage=percentage,
                max_tokens=max_tokens,
                auto_downgrade_to=self._downgrade_map.get(tier)
            )
    
    def set_tier_quota(self, tier_name: Union[str, TierLevel], percentage: float, 
                      max_tokens: Optional[int] = None) -> bool:
        """
        设置Tier配额
        
        Args:
            tier_name: Tier名称或TierLevel枚举
            percentage: 百分比配额
            max_tokens: 最大Token数量（可选）
            
        Returns:
            bool: 设置是否成功
        """
        with self._lock:
            # 转换tier_name为TierLevel
            if isinstance(tier_name, str):
                try:
                    tier = TierLevel(tier_name)
                except ValueError:
                    # 尝试匹配（不区分大小写）
                    tier = next((t for t in TierLevel if t.value.lower() == tier_name.lower()), None)
                    if not tier:
                        return False
            else:
                tier = tier_name
            
            if tier not in self.tier_quotas:
                self.tier_quotas[tier] = TierQuota(
                    tier=tier,
                    percentage=percentage,
                    max_tokens=max_tokens,
                    auto_downgrade_to=self._downgrade_map.get(tier)
                )
            else:
                self.tier_quotas[tier].percentage = percentage
                self.tier_quotas[tier].max_tokens = max_tokens
            
            return True
    
    def can_use_tier(self, tier_name: Union[str, TierLevel], tokens: int) -> Tuple[bool, Optional[TierLevel]]:
        """
        检查是否可以使用指定Tier
        
        Args:
            tier_name: Tier名称
            tokens: 需要的Token数量
            
        Returns:
            Tuple[bool, Optional[TierLevel]]: (是否可用, 建议降级目标)
        """
        with self._lock:
            # 转换tier_name为TierLevel
            if isinstance(tier_name, str):
                try:
                    tier = TierLevel(tier_name)
                except ValueError:
                    return False, None
            else:
                tier = tier_name
            
            if tier not in self.tier_quotas:
                return False, None
            
            quota = self.tier_quotas[tier]
            
            # 检查是否可用
            if quota.can_use(tokens):
                return True, None
            else:
                # 配额不足，返回降级目标
                return False, quota.auto_downgrade_to
    
    def use_tokens(self, tier_name: Union[str, TierLevel], tokens: int, 
                  agent_id: str = "unknown", task_id: str = "unknown") -> bool:
        """
        使用Token并更新配额
        
        Args:
            tier_name: Tier名称
            tokens: 使用的Token数量
            agent_id: Agent ID
            task_id: 任务ID
            
        Returns:
            bool: 使用是否成功
        """
        with self._lock:
            # 转换tier_name为TierLevel
            if isinstance(tier_name, str):
                try:
                    tier = TierLevel(tier_name)
                except ValueError:
                    return False
            else:
                tier = tier_name
            
            if tier not in self.tier_quotas:
                return False
            
            quota = self.tier_quotas[tier]
            
            # 检查是否可用
            if not quota.can_use(tokens):
                return False
            
            # 更新使用量
            quota.used_tokens += tokens
            
            # 记录使用历史
            record = TokenUsageRecord(
                timestamp=time.time(),
                tier=tier,
                tokens=tokens,
                agent_id=agent_id,
                task_id=task_id,
                success=True
            )
            self.usage_history.append(record)
            
            # 清理历史记录（保留最近1000条）
            if len(self.usage_history) > 1000:
                self.usage_history = self.usage_history[-1000:]
            
            return True
    
    def get_tier_usage(self, tier_name: Union[str, TierLevel]) -> Dict[str, any]:
        """
        获取Tier使用情况
        
        Args:
            tier_name: Tier名称
            
        Returns:
            Dict[str, any]: 使用情况统计
        """
        with self._lock:
            # 转换tier_name为TierLevel
            if isinstance(tier_name, str):
                try:
                    tier = TierLevel(tier_name)
                except ValueError:
                    return {}
            else:
                tier = tier_name
            
            if tier not in self.tier_quotas:
                return {}
            
            quota = self.tier_quotas[tier]
            
            return {
                "tier": tier.value,
                "percentage": quota.percentage,
                "used_tokens": quota.used_tokens,
                "max_tokens": quota.max_tokens,
                "usage_percentage": quota.usage_percentage,
                "remaining_tokens": quota.remaining_tokens,
                "auto_downgrade_to": quota.auto_downgrade_to.value if quota.auto_downgrade_to else None
            }
    
    def get_all_tier_usage(self) -> Dict[str, Dict[str, any]]:
        """
        获取所有Tier的使用情况
        
        Returns:
            Dict[str, Dict[str, any]]: 所有Tier的使用情况
        """
        with self._lock:
            result = {}
            for tier, quota in self.tier_quotas.items():
                result[tier.value] = self.get_tier_usage(tier)
            return result
    
    def auto_downgrade(self, tier_name: Union[str, TierLevel]) -> Optional[TierLevel]:
        """
        自动降级到下一个可用Tier
        
        Args:
            tier_name: 当前Tier名称
            
        Returns:
            Optional[TierLevel]: 降级后的Tier，如果无法降级则返回None
        """
        with self._lock:
            # 转换tier_name为TierLevel
            if isinstance(tier_name, str):
                try:
                    current_tier = TierLevel(tier_name)
                except ValueError:
                    return None
            else:
                current_tier = tier_name
            
            # 获取降级链
            downgrade_chain = []
            tier = current_tier
            
            while tier in self._downgrade_map:
                next_tier = self._downgrade_map[tier]
                if next_tier:
                    downgrade_chain.append(next_tier)
                    tier = next_tier
                else:
                    break
            
            # 寻找第一个可用的Tier
            for target_tier in downgrade_chain:
                if target_tier in self.tier_quotas:
                    quota = self.tier_quotas[target_tier]
                    # 检查是否有配额（百分比>0）
                    if quota.percentage > 0:
                        return target_tier
            
            return None
    
    def reset_usage(self, tier_name: Optional[Union[str, TierLevel]] = None):
        """
        重置使用统计
        
        Args:
            tier_name: 要重置的Tier名称，如果为None则重置所有
        """
        with self._lock:
            if tier_name is None:
                # 重置所有Tier
                for quota in self.tier_quotas.values():
                    quota.used_tokens = 0
                self.usage_history.clear()
            else:
                # 重置指定Tier
                if isinstance(tier_name, str):
                    try:
                        tier = TierLevel(tier_name)
                    except ValueError:
                        return
                else:
                    tier = tier_name
                
                if tier in self.tier_quotas:
                    self.tier_quotas[tier].used_tokens = 0
                    # 清理该Tier的历史记录
                    self.usage_history = [r for r in self.usage_history if r.tier != tier]
    
    def get_usage_summary(self, hours: int = 24) -> Dict[str, any]:
        """
        获取指定时间段内的使用摘要
        
        Args:
            hours: 小时数
            
        Returns:
            Dict[str, any]: 使用摘要
        """
        with self._lock:
            cutoff_time = time.time() - (hours * 3600)
            
            recent_records = [
                r for r in self.usage_history 
                if r.timestamp >= cutoff_time
            ]
            
            total_tokens = sum(r.tokens for r in recent_records)
            
            tier_breakdown = {}
            for record in recent_records:
                tier_name = record.tier.value
                if tier_name not in tier_breakdown:
                    tier_breakdown[tier_name] = {
                        "tokens": 0,
                        "count": 0,
                        "agents": set()
                    }
                tier_breakdown[tier_name]["tokens"] += record.tokens
                tier_breakdown[tier_name]["count"] += 1
                tier_breakdown[tier_name]["agents"].add(record.agent_id)
            
            # 转换agents为列表
            for tier_data in tier_breakdown.values():
                tier_data["agents"] = list(tier_data["agents"])
            
            return {
                "period_hours": hours,
                "total_tokens": total_tokens,
                "record_count": len(recent_records),
                "tier_breakdown": tier_breakdown,
                "timestamp": time.time()
            }


# 全局预算管理器实例
_global_budget_manager: Optional[TokenBudgetManager] = None


def get_global_budget_manager(total_budget: Optional[int] = None) -> TokenBudgetManager:
    """
    获取全局预算管理器实例（单例模式）
    
    Args:
        total_budget: 总Token预算
        
    Returns:
        TokenBudgetManager: 全局预算管理器实例
    """
    global _global_budget_manager
    
    if _global_budget_manager is None:
        _global_budget_manager = TokenBudgetManager(total_budget)
    
    return _global_budget_manager