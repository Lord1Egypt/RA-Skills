"""
Layer 4: 共识引擎 (Consensus Engine)

职责：
- 接收统一格式的 DecisionResult 列表
- 执行拜占庭共识判定（≥2/3 一致）
- 输出 ConsensusVerdict
- 分歧管理（最多 2 轮自动重试，第 3 轮转交用户）
"""
from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Tuple

from schemas import (
    ConsensusOutput,
    ConsensusVerdict,
    DecisionResult,
    DivergenceAction,
    ExecutionReport,
    ExecutionStatus,
    Tier,
    UserInput,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 共识引擎
# ============================================================================

class ConsensusEngine:
    """拜占庭共识引擎 — ≥2/3 一致则采纳"""

    # 各配置档次的数值映射（用于重要性比较）
    TIER_WEIGHTS: Dict[Tier, int] = {
        Tier.FULL: 3,
        Tier.BALANCED: 2,
        Tier.LIGHT: 1,
        Tier.SKILL_DISPATCH: 3,
    }

    def __init__(
        self,
        agreement_threshold: float = 2.0 / 3.0,
        max_divergence_rounds: int = 2,
        importance_tolerance: int = 1,
        tier_tolerance: int = 1,
    ):
        """
        Args:
            agreement_threshold: 共识阈值（默认 2/3）
            max_divergence_rounds: 最大分歧轮次
            importance_tolerance: 重要性评分的容忍差值
            tier_tolerance: 档次权重的容忍差值
        """
        self.agreement_threshold = agreement_threshold
        self.max_divergence_rounds = max_divergence_rounds
        self.importance_tolerance = importance_tolerance
        self.tier_tolerance = tier_tolerance

    # ------------------------------------------------------------------
    # 决策收集
    # ------------------------------------------------------------------

    def gather_decisions(
        self,
        validated_input: UserInput,
        round_number: int,
    ) -> List[DecisionResult]:
        """收集决策者意见。当没有真实 Agent 时返回内置兜底决策。

        Returns:
            List[DecisionResult]: 至少 1 个决策者的统一格式结果
        """
        # 基类返回兜底决策（子类可覆盖注入真实 Agent 逻辑）
        return self._generate_fallback_decisions(validated_input)

    def _generate_fallback_decisions(
        self, validated_input: UserInput
    ) -> List[DecisionResult]:
        """当没有真实 Agent 时生成兜底决策。"""
        tier = (
            Tier.FULL if validated_input.importance >= 4
            else Tier.BALANCED if validated_input.importance >= 2
            else Tier.LIGHT
        )
        return [
            DecisionResult(
                agent_id="A",
                importance=validated_input.importance,
                config=tier,
                reasoning=f"基于任务描述 '{validated_input.task_description[:30]}...' 进行主视角分析",
                top_findings=[f"需要深入分析: {validated_input.task_description[:50]}"],
                confidence=0.85,
            ),
            DecisionResult(
                agent_id="B",
                importance=validated_input.importance,
                config=tier,
                reasoning=f"批判性审视 '{validated_input.task_description[:30]}...' 的风险和盲区",
                risks=["可能存在信息不完整的风险"],
                top_findings=[f"需要验证假设: {validated_input.task_description[:50]}"],
                confidence=0.75,
            ),
            DecisionResult(
                agent_id="C",
                importance=validated_input.importance,
                config=tier,
                reasoning=f"务实评估 '{validated_input.task_description[:30]}...' 的落地可行性",
                top_findings=[f"最小可行方案: {validated_input.task_description[:50]}"],
                confidence=0.80,
            ),
        ]

    # ------------------------------------------------------------------
    # 共识判定
    # ------------------------------------------------------------------

    def evaluate(self, decisions: List[DecisionResult]) -> ConsensusOutput:
        """
        对决策结果执行拜占庭共识判定。

        判定逻辑：
        1. config (Tier) 比较 — 权重差 ≤ tolerance → 一致
        2. importance 比较 — 差值 ≤ tolerance → 一致
        3. top_findings 语义比较 — 共享关键词 ≥ 1 → 一致

        ≥2/3 决策者在以上 3 个维度都一致 → CONSENSUS
        否则 → DIVERGENCE（若轮次 < max）或 FALLBACK_TO_USER
        """
        if len(decisions) < 2:
            return ConsensusOutput(
                verdict=ConsensusVerdict.FALLBACK_TO_USER,
                agreement_count=len(decisions),
                total_participants=len(decisions),
                requires_user_intervention=True,
            )

        total = len(decisions)

        # 维度一：config 比较
        config_agreement = self._check_config_agreement(decisions)

        # 维度二：importance 比较
        importance_agreement = self._check_importance_agreement(decisions)

        # 维度三：top_findings 语义比较
        findings_agreement = self._check_findings_agreement(decisions)

        # 综合判定
        agreements = [config_agreement, importance_agreement, findings_agreement]
        agreed_dimensions = sum(1 for a in agreements if a[0])

        # 至少 2/3 维度一致 → 共识
        threshold_count = int(total * self.agreement_threshold)
        is_consensus = agreed_dimensions >= threshold_count

        if is_consensus:
            agreed_points = self._extract_agreed_points(decisions)
            return ConsensusOutput(
                verdict=ConsensusVerdict.CONSENSUS,
                agreement_count=total,
                total_participants=total,
                agreed_points=agreed_points,
            )

        # 分歧
        divergent_points = {}
        for i, (agreed, reason) in enumerate(agreements):
            if not agreed:
                divergent_points[f"dimension_{i+1}"] = [reason]

        return ConsensusOutput(
            verdict=ConsensusVerdict.DIVERGENCE,
            agreement_count=agreed_dimensions,
            total_participants=total,
            divergent_points=divergent_points,
            divergence_rounds=0,
            requires_user_intervention=False,
            recommended_action=DivergenceAction.RETRY,
        )

    # ------------------------------------------------------------------
    # 分歧管理
    # ------------------------------------------------------------------

    def handle_divergence(
        self,
        decisions: List[DecisionResult],
        current_round: int,
    ) -> ConsensusOutput:
        """处理分歧。current_round ≤ max 时自动重试，超过则转交用户。"""
        if current_round > self.max_divergence_rounds:
            logger.warning(
                f"分歧已达 {current_round} 轮（上限 {self.max_divergence_rounds}），"
                f"转交用户裁决"
            )
            return ConsensusOutput(
                verdict=ConsensusVerdict.FALLBACK_TO_USER,
                agreement_count=0,
                total_participants=len(decisions),
                requires_user_intervention=True,
                divergence_rounds=current_round,
                recommended_action=DivergenceAction.FALLBACK,
            )

        # 自动重试 — 将分歧信息反馈给决策者
        return ConsensusOutput(
            verdict=ConsensusVerdict.DIVERGENCE,
            agreement_count=0,
            total_participants=len(decisions),
            divergence_rounds=current_round,
            requires_user_intervention=False,
            recommended_action=DivergenceAction.RETRY,
        )

    # ------------------------------------------------------------------
    # 结果审阅
    # ------------------------------------------------------------------

    def review_results(self, exec_report: ExecutionReport) -> List[DecisionResult]:
        """对执行结果进行审阅。

        Returns:
            List[DecisionResult]: 正常情况返回 2 个审阅者（B + C），空报告时返回空列表。
        """
        if exec_report.total_tasks == 0:
            logger.warning("执行报告为空，跳过审阅")
            return []

        # 计算成功率
        success_rate = (
            exec_report.completed / exec_report.total_tasks
            if exec_report.total_tasks > 0
            else 0.0
        )

        # 从成功的执行结果中提取结论
        findings: List[str] = []
        for result in exec_report.results:
            if result.status == ExecutionStatus.SUCCESS and result.output:
                # 截取前 200 字符作为审阅摘要
                snippet = result.output[:200].strip()
                if snippet:
                    findings.append(snippet)

        # 如果没有可提取的结论，基于统计数据生成
        if not findings:
            findings = [
                f"执行完成率: {success_rate:.0%} "
                f"({exec_report.completed}/{exec_report.total_tasks})"
            ]
            if exec_report.failed > 0:
                findings.append(
                    f"注意: {exec_report.failed} 个子任务失败，"
                    f"可能影响结论完整性"
                )

        # 生成批判视角（B）审阅
        review_b = DecisionResult(
            agent_id="B",
            importance=3,
            config=Tier.BALANCED,
            reasoning=(
                f"审阅了 {exec_report.completed}/{exec_report.total_tasks} 个成功执行的子任务，"
                f"成功率 {success_rate:.0%}，"
                f"总耗时 {exec_report.total_duration_seconds:.1f}s"
            ),
            risks=(
                ["部分子任务失败，结论可能不完整"]
                if exec_report.failed > 0
                else []
            ),
            top_findings=findings[:3] or ["执行层已产出结果，可进入输出阶段"],
            confidence=success_rate,
        )

        # 生成实用视角（C）审阅
        review_c = DecisionResult(
            agent_id="C",
            importance=3,
            config=Tier.BALANCED,
            reasoning=(
                f"务实评估：{exec_report.total_tasks} 个子任务中 "
                f"{exec_report.completed} 个完成，"
                f"可直接用于最终报告"
            ),
            top_findings=(
                findings[:2]
                if len(findings) >= 2
                else (findings or ["执行层产出已汇总"])
            ),
            confidence=min(success_rate * 1.1, 1.0),  # 务实视角略乐观
        )

        return [review_b, review_c]

    # ------------------------------------------------------------------
    # 内部判定方法
    # ------------------------------------------------------------------

    def _check_config_agreement(
        self, decisions: List[DecisionResult]
    ) -> Tuple[bool, str]:
        """检查配置档次是否一致"""
        if not decisions:
            return False, "无决策数据"

        weights = [self.TIER_WEIGHTS[d.config] for d in decisions]
        max_diff = max(weights) - min(weights)

        if max_diff <= self.tier_tolerance:
            return True, f"档次一致 (最大差异 {max_diff})"
        return False, f"档次分歧 (最大差异 {max_diff} > {self.tier_tolerance})"

    def _check_importance_agreement(
        self, decisions: List[DecisionResult]
    ) -> Tuple[bool, str]:
        """检查重要性评分是否一致"""
        if not decisions:
            return False, "无决策数据"

        importances = [d.importance for d in decisions]
        max_diff = max(importances) - min(importances)

        if max_diff <= self.importance_tolerance:
            return True, f"重要性一致 (最大差异 {max_diff})"
        return False, f"重要性分歧 (最大差异 {max_diff} > {self.importance_tolerance})"

    def _check_findings_agreement(
        self, decisions: List[DecisionResult]
    ) -> Tuple[bool, str]:
        """检查 top_findings 是否语义一致（共享关键词法）"""
        if not decisions:
            return False, "无决策数据"

        # 提取所有 findings 的关键词
        all_keywords: List[set] = []
        for d in decisions:
            keywords = set()
            for finding in d.top_findings:
                # 简单分词
                words = finding.lower().split()
                keywords.update(w for w in words if len(w) > 1)
            all_keywords.append(keywords)

        if not all_keywords:
            return False, "无 findings 数据"

        # 检查每对决策者之间是否有共享关键词
        agreement_count = 0
        total_pairs = 0
        for i in range(len(all_keywords)):
            for j in range(i + 1, len(all_keywords)):
                total_pairs += 1
                if all_keywords[i] & all_keywords[j]:  # 有交集
                    agreement_count += 1

        if total_pairs == 0:
            return False, "无法比较"

        ratio = agreement_count / total_pairs
        if ratio >= self.agreement_threshold:
            return True, f"结论语义一致 (匹配率 {ratio:.0%})"
        return False, f"结论分歧 (匹配率 {ratio:.0%} < {self.agreement_threshold:.0%})"

    def _extract_agreed_points(
        self, decisions: List[DecisionResult]
    ) -> List[str]:
        """提取共识点"""
        # 收集所有 findings，去重
        all_points = []
        seen = set()
        for d in decisions:
            for finding in d.top_findings:
                normalized = finding.strip().lower()
                if normalized not in seen:
                    all_points.append(finding)
                    seen.add(normalized)
        return all_points[:5]  # 最多 5 条


# ============================================================================
# 默认引擎实例
# ============================================================================

default_consensus_engine = ConsensusEngine()
