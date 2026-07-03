#!/usr/bin/env python3
"""llm_judge.py 单元测试"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from llm_judge import LLMJudge, _get_category, A_CATEGORY_MAP, HK_CATEGORY_MAP


class TestGetCategory:
    """测试分类映射功能"""

    def test_a_stock_known_type(self):
        """测试A股已知类型"""
        assert _get_category("A股", "回购股权") == "股权股本类"
        assert _get_category("A股", "季度报告") == "财务报告类"
        assert _get_category("A股", "资产重组") == "重大事项类"
        assert _get_category("A股", "停牌提示") == "交易提示类"

    def test_a_stock_unknown_type(self):
        """测试A股未知类型（应回退到默认值）"""
        result = _get_category("A股", "未知类型")
        assert result == "一般公告类"

    def test_hk_stock_known_type(self):
        """测试港股已知类型"""
        assert _get_category("港股", "业绩预告") == "业绩快报"
        assert _get_category("港股", "年度报告") == "财务报告"
        assert _get_category("港股", "权益变动") == "股权股本"

    def test_hk_stock_unknown_type(self):
        """测试港股未知类型（应回退到默认值）"""
        result = _get_category("港股", "未知类型")
        assert result == "一般公告"


class TestLLMJudge:
    """测试LLM判断器"""

    def test_disabled_judge(self):
        """测试禁用时的判断"""
        judge = LLMJudge(api_key="", enabled=False)
        result = judge.judge("测试标题", "测试股票")
        assert result["valuable"] is True
        assert result["category"] == "一般公告类"
        assert result["type"] == "个股其他公告"

    def test_stats_initial(self):
        """测试初始统计信息"""
        judge = LLMJudge(api_key="", enabled=False)
        stats = judge.stats
        assert stats["total"] == 0
        assert stats["valuable"] == 0
        assert stats["skip"] == 0
        assert stats["error"] == 0

    def test_report_empty(self):
        """测试空统计报告"""
        judge = LLMJudge(api_key="", enabled=False)
        report = judge.report()
        assert "未进行任何判断" in report

    def test_category_maps_populated(self):
        """测试分类映射已填充"""
        assert len(A_CATEGORY_MAP) == 8
        assert len(HK_CATEGORY_MAP) == 7

    def test_from_config_disabled(self):
        """测试从配置创建（禁用状态）"""
        from config_manager import AppConfig, LLMConfig
        config = AppConfig(llm=LLMConfig(enabled=False))
        judge = LLMJudge.from_config(config)
        assert judge.enabled is False
