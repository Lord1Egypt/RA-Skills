"""
共识引擎测试 — 验证拜占庭共识判定逻辑。
"""
import pytest
import sys
sys.path.insert(0, "..")

from schemas import (
    ConsensusOutput,
    ConsensusVerdict,
    DecisionResult,
    Tier,
)
from consensus import ConsensusEngine


class TestConsensusEngine:
    """共识引擎测试"""

    @pytest.fixture
    def engine(self):
        return ConsensusEngine()

    @pytest.fixture
    def agreeing_decisions(self):
        """一致的决策（全量 + 重要性 4-5 + 相似 findings）"""
        return [
            DecisionResult(
                agent_id="A",
                importance=4,
                config=Tier.FULL,
                reasoning="需要全面评估以确保架构决策的正确性",
                top_findings=["PostgreSQL 适合事务场景", "需要考虑扩展性"],
                confidence=0.9,
            ),
            DecisionResult(
                agent_id="B",
                importance=5,
                config=Tier.FULL,
                reasoning="这是一个高风险决策，需要全面分析",
                top_findings=["PostgreSQL 事务支持更好", "扩展性需要关注"],
                confidence=0.85,
            ),
            DecisionResult(
                agent_id="C",
                importance=4,
                config=Tier.FULL,
                reasoning="从务实角度出发，全面评估可以避免后期返工",
                top_findings=["PostgreSQL 是更好的选择", "扩展性方案需讨论"],
                confidence=0.8,
            ),
        ]

    @pytest.fixture
    def diverging_decisions(self):
        """分歧的决策"""
        return [
            DecisionResult(
                agent_id="A",
                importance=5,
                config=Tier.FULL,
                reasoning="这是重大决策，需要全面评估",
                top_findings=["方案A 是最佳选择"],
                confidence=0.9,
            ),
            DecisionResult(
                agent_id="B",
                importance=2,
                config=Tier.LIGHT,
                reasoning="这不是什么大问题，简单处理即可",
                top_findings=["任何方案都可以"],
                confidence=0.3,
            ),
            DecisionResult(
                agent_id="C",
                importance=3,
                config=Tier.BALANCED,
                reasoning="折中方案即可满足需求",
                top_findings=["方案B 可以考虑"],
                confidence=0.5,
            ),
        ]

    def test_consensus_with_agreeing_decisions(self, engine, agreeing_decisions):
        """一致决策应判定为共识"""
        result = engine.evaluate(agreeing_decisions)
        assert result.verdict == ConsensusVerdict.CONSENSUS
        assert result.agreement_count > 0

    def test_divergence_with_disagreeing_decisions(self, engine, diverging_decisions):
        """分歧决策应判定为分歧"""
        result = engine.evaluate(diverging_decisions)
        assert result.verdict == ConsensusVerdict.DIVERGENCE

    def test_fallback_on_exceeded_rounds(self, engine, diverging_decisions):
        """超过最大轮次应转交用户"""
        result = engine.handle_divergence(diverging_decisions, current_round=3)
        assert result.verdict == ConsensusVerdict.FALLBACK_TO_USER
        assert result.requires_user_intervention

    def test_retry_within_limit(self, engine, diverging_decisions):
        """在限制内应建议重试"""
        result = engine.handle_divergence(diverging_decisions, current_round=1)
        assert result.verdict == ConsensusVerdict.DIVERGENCE

    def test_insufficient_decisions(self, engine):
        """少于 2 个决策应转交用户"""
        result = engine.evaluate([
            DecisionResult(
                agent_id="A",
                importance=3,
                config=Tier.BALANCED,
                reasoning="只有一个决策者，无法达成共识",
                top_findings=["need more input"],
                confidence=0.5,
            ),
        ])
        assert result.verdict == ConsensusVerdict.FALLBACK_TO_USER

    def test_empty_decisions(self, engine):
        """空决策列表"""
        result = engine.evaluate([])
        assert result.verdict == ConsensusVerdict.FALLBACK_TO_USER

    def test_config_agreement_detection(self, engine):
        """配置一致性检测"""
        decisions = [
            DecisionResult(
                agent_id="A", importance=4, config=Tier.FULL,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.8,
            ),
            DecisionResult(
                agent_id="B", importance=4, config=Tier.FULL,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.8,
            ),
            DecisionResult(
                agent_id="C", importance=4, config=Tier.FULL,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.8,
            ),
        ]
        agreed, reason = engine._check_config_agreement(decisions)
        assert agreed

    def test_config_divergence_detection(self, engine):
        """配置分歧检测"""
        decisions = [
            DecisionResult(
                agent_id="A", importance=4, config=Tier.FULL,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.8,
            ),
            DecisionResult(
                agent_id="B", importance=4, config=Tier.LIGHT,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.8,
            ),
        ]
        agreed, reason = engine._check_config_agreement(decisions)
        assert not agreed

    def test_importance_agreement(self, engine):
        """重要性一致检测"""
        decisions = [
            DecisionResult(
                agent_id="A", importance=4, config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.8,
            ),
            DecisionResult(
                agent_id="B", importance=5, config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["test"], confidence=0.8,
            ),
        ]
        agreed, _ = engine._check_importance_agreement(decisions)
        assert agreed  # 差值 1 ≤ tolerance 1

    def test_findings_agreement_by_keyword(self, engine):
        """通过共享关键词检测结论一致"""
        decisions = [
            DecisionResult(
                agent_id="A", importance=4, config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["PostgreSQL 事务支持更好"],
                confidence=0.8,
            ),
            DecisionResult(
                agent_id="B", importance=4, config=Tier.BALANCED,
                reasoning="足够长的推理理由说明",
                top_findings=["PostgreSQL 扩展性需要关注"],
                confidence=0.8,
            ),
        ]
        agreed, _ = engine._check_findings_agreement(decisions)
        assert agreed  # 共享 "postgresql"
