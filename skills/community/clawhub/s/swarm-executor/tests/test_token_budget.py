"""
测试Token预算管理器
"""
import pytest
import time
from coordinator.token_budget import TokenBudgetManager, TierLevel


class TestTokenBudgetManager:
    """TokenBudgetManager测试类"""
    
    @pytest.fixture
    def budget_manager(self):
        """创建预算管理器实例"""
        return TokenBudgetManager()
    
    def test_default_tiers(self, budget_manager):
        """测试默认Tier配置"""
        # 验证默认Tier存在
        assert TierLevel.TIER_0 in budget_manager.tier_quotas
        assert TierLevel.TIER_1 in budget_manager.tier_quotas
        assert TierLevel.TIER_2 in budget_manager.tier_quotas
        assert TierLevel.TIER_3 in budget_manager.tier_quotas
        
        # 验证默认配额
        tier0 = budget_manager.tier_quotas[TierLevel.TIER_0]
        tier1 = budget_manager.tier_quotas[TierLevel.TIER_1]
        tier2 = budget_manager.tier_quotas[TierLevel.TIER_2]
        tier3 = budget_manager.tier_quotas[TierLevel.TIER_3]
        
        assert tier0.percentage == 85.0
        assert tier1.percentage == 5.0
        assert tier2.percentage == 10.0
        assert tier3.percentage == 0.0
    
    def test_set_tier_quota(self, budget_manager):
        """测试设置Tier配额"""
        # 设置新配额
        assert budget_manager.set_tier_quota("Tier 0", 80.0, max_tokens=8000) == True
        
        # 验证设置
        usage = budget_manager.get_tier_usage("Tier 0")
        assert usage["percentage"] == 80.0
        assert usage["max_tokens"] == 8000
        
        # 测试无效Tier名称
        assert budget_manager.set_tier_quota("Invalid Tier", 50.0) == False
    
    def test_can_use_tier(self, budget_manager):
        """测试检查Tier可用性"""
        # 设置Tier 0的最大Token限制
        budget_manager.set_tier_quota("Tier 0", 85.0, max_tokens=1000)
        
        # 检查可用性
        can_use, downgrade_target = budget_manager.can_use_tier("Tier 0", 500)
        assert can_use == True
        assert downgrade_target is None
        
        # 检查超出限制的情况
        can_use, downgrade_target = budget_manager.can_use_tier("Tier 0", 1500)
        assert can_use == False
        assert downgrade_target == TierLevel.TIER_1
    
    def test_use_tokens(self, budget_manager):
        """测试使用Token"""
        # 设置Tier 0的最大Token限制
        budget_manager.set_tier_quota("Tier 0", 85.0, max_tokens=1000)
        
        # 使用Token
        assert budget_manager.use_tokens("Tier 0", 300, "003", "task_001") == True
        
        # 验证使用量
        usage = budget_manager.get_tier_usage("Tier 0")
        assert usage["used_tokens"] == 300
        assert usage["remaining_tokens"] == 700
        
        # 尝试使用超出限制的Token
        assert budget_manager.use_tokens("Tier 0", 800, "003", "task_002") == False
        
        # 验证使用量未改变
        usage = budget_manager.get_tier_usage("Tier 0")
        assert usage["used_tokens"] == 300
    
    def test_get_all_tier_usage(self, budget_manager):
        """测试获取所有Tier使用情况"""
        # 设置一些使用量
        budget_manager.set_tier_quota("Tier 0", 85.0, max_tokens=1000)
        budget_manager.set_tier_quota("Tier 1", 5.0, max_tokens=100)
        
        budget_manager.use_tokens("Tier 0", 300, "003", "task_001")
        budget_manager.use_tokens("Tier 1", 50, "004", "task_002")
        
        # 获取所有使用情况
        all_usage = budget_manager.get_all_tier_usage()
        
        # 验证数据
        assert "Tier 0" in all_usage
        assert "Tier 1" in all_usage
        
        assert all_usage["Tier 0"]["used_tokens"] == 300
        assert all_usage["Tier 1"]["used_tokens"] == 50
    
    def test_auto_downgrade(self, budget_manager):
        """测试自动降级"""
        # 设置Tier配额
        budget_manager.set_tier_quota("Tier 0", 85.0, max_tokens=1000)
        budget_manager.set_tier_quota("Tier 1", 5.0, max_tokens=100)
        budget_manager.set_tier_quota("Tier 2", 10.0, max_tokens=200)
        
        # 使用所有Tier 0 Token
        budget_manager.use_tokens("Tier 0", 1000, "003", "task_001")
        
        # 测试自动降级
        downgraded_tier = budget_manager.auto_downgrade("Tier 0")
        assert downgraded_tier == TierLevel.TIER_1
        
        # 使用所有Tier 1 Token
        budget_manager.use_tokens("Tier 1", 100, "004", "task_002")
        
        # 再次测试自动降级
        downgraded_tier = budget_manager.auto_downgrade("Tier 0")
        assert downgraded_tier == TierLevel.TIER_2
        
        # 使用所有Tier 2 Token
        budget_manager.use_tokens("Tier 2", 200, "005", "task_003")
        
        # 测试无可用Tier的情况
        downgraded_tier = budget_manager.auto_downgrade("Tier 0")
        assert downgraded_tier == TierLevel.TIER_3  # 兜底Tier
    
    def test_reset_usage(self, budget_manager):
        """测试重置使用统计"""
        # 设置并使用Token
        budget_manager.set_tier_quota("Tier 0", 85.0, max_tokens=1000)
        budget_manager.use_tokens("Tier 0", 300, "003", "task_001")
        budget_manager.use_tokens("Tier 0", 200, "003", "task_002")
        
        # 验证使用量
        usage = budget_manager.get_tier_usage("Tier 0")
        assert usage["used_tokens"] == 500
        
        # 重置指定Tier
        budget_manager.reset_usage("Tier 0")
        
        # 验证重置
        usage = budget_manager.get_tier_usage("Tier 0")
        assert usage["used_tokens"] == 0
        
        # 重置所有Tier
        budget_manager.use_tokens("Tier 0", 100, "003", "task_003")
        budget_manager.use_tokens("Tier 1", 50, "004", "task_004")
        
        budget_manager.reset_usage()
        
        # 验证所有Tier都被重置
        all_usage = budget_manager.get_all_tier_usage()
        for tier_usage in all_usage.values():
            assert tier_usage["used_tokens"] == 0
    
    def test_get_usage_summary(self, budget_manager):
        """测试获取使用摘要"""
        # 设置并使用Token
        budget_manager.set_tier_quota("Tier 0", 85.0, max_tokens=1000)
        budget_manager.set_tier_quota("Tier 1", 5.0, max_tokens=100)
        
        # 使用一些Token
        budget_manager.use_tokens("Tier 0", 300, "003", "task_001")
        budget_manager.use_tokens("Tier 0", 200, "003", "task_002")
        budget_manager.use_tokens("Tier 1", 50, "004", "task_003")
        
        # 获取24小时摘要
        summary = budget_manager.get_usage_summary(hours=24)
        
        # 验证摘要数据
        assert summary["total_tokens"] == 550
        assert summary["record_count"] == 3
        
        # 验证Tier分解
        assert "Tier 0" in summary["tier_breakdown"]
        assert "Tier 1" in summary["tier_breakdown"]
        
        assert summary["tier_breakdown"]["Tier 0"]["tokens"] == 500
        assert summary["tier_breakdown"]["Tier 1"]["tokens"] == 50
        
        # 验证Agent列表
        assert "003" in summary["tier_breakdown"]["Tier 0"]["agents"]
        assert "004" in summary["tier_breakdown"]["Tier 1"]["agents"]
    
    def test_usage_history_cleanup(self, budget_manager):
        """测试使用历史清理"""
        # 添加大量使用记录
        for i in range(1500):
            budget_manager.use_tokens("Tier 0", 1, "003", f"task_{i}")
        
        # 验证历史记录被清理（保留最近1000条）
        assert len(budget_manager.usage_history) == 1000
        
        # 验证最早的任务被清理
        task_ids = [r.task_id for r in budget_manager.usage_history]
        assert "task_0" not in task_ids  # 最早的任务被清理
        assert "task_1499" in task_ids   # 最近的任务还在


if __name__ == "__main__":
    pytest.main([__file__, "-v"])