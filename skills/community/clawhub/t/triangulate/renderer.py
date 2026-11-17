"""
Layer 6: 输出渲染器 (Output Renderer)

职责：
- 从 PipelineContext 渲染 FinalReport
- 纯渲染，无副作用
- 即使部分数据缺失，也能生成可读的报告
"""
from __future__ import annotations

import textwrap
from collections import Counter
from typing import List, Optional

from schemas import (
    ConsensusVerdict,
    DecisionResult,
    ExecutionReport,
    FinalReport,
    StrategyRound,
    Tier,
    UserInput,
)


# ============================================================================
# 渲染器
# ============================================================================

class ReportRenderer:
    """Triangulate 最终报告渲染器"""

    # 分隔线宽度
    SEPARATOR_WIDTH = 47

    def render(
        self,
        validated_input: UserInput,
        strategy_rounds: List[StrategyRound],
        exec_report: Optional[ExecutionReport],
        review_results: List[DecisionResult],
        degraded: bool = False,
    ) -> FinalReport:
        """
        从各阶段数据渲染 FinalReport。

        保证即使部分数据缺失，也不会输出空字段导致残缺报告。

        Args:
            degraded: 是否触发过降级策略（如使用了默认决策而非真实 agent 输出）
        """
        # 提取核心结论
        core_conclusions = self._extract_core_conclusions(
            strategy_rounds, review_results
        )

        # 提取分歧点
        divergent_points = self._extract_divergent_points(strategy_rounds)

        # 提取不确定性
        uncertainties = self._extract_uncertainties(
            strategy_rounds, review_results
        )

        # 确定配置档次
        tier = self._determine_tier(strategy_rounds, validated_input)

        # 决策者数量
        dm_count = sum(len(r.decisions) for r in strategy_rounds) if strategy_rounds else 0

        # 视角编码
        perspective_code = (
            validated_input.preferred_templates[0]
            if validated_input.preferred_templates
            else None
        )

        return FinalReport(
            task_description=validated_input.task_description,
            tier=tier,
            executor_count=exec_report.total_tasks if exec_report else 0,
            decision_maker_count=dm_count,
            perspective_code=perspective_code,
            core_conclusions=core_conclusions,
            divergent_points=divergent_points,
            uncertainties=uncertainties,
            execution_stats=exec_report,
            degraded=degraded,
        )

    # ------------------------------------------------------------------
    # Markdown 渲染
    # ------------------------------------------------------------------

    def render_markdown(self, report: FinalReport) -> str:
        """
        将 FinalReport 渲染为 Markdown 格式。

        完全保留原 SKILL.md 中定义的输出格式。
        """
        lines = []

        # 头部
        lines.append("═" * self.SEPARATOR_WIDTH)
        lines.append("🔺 Triangulate 分析报告")
        lines.append("─" * self.SEPARATOR_WIDTH)
        lines.append("")

        # 任务描述
        lines.append(f"📌 任务：{report.task_description}")

        # 降级警告
        if report.degraded:
            lines.append("⚠️  **注意：本次分析使用了降级策略**（部分阶段使用了默认值而非真实 Agent 输出）")
            lines.append("")

        # 配置信息
        lines.append(
            f"⚙️ 配置：{report.tier.value} | "
            f"执行器×{report.executor_count} | "
            f"决策者×{report.decision_maker_count}"
        )

        # 视角
        if report.perspective_code:
            lines.append(f"🧩 视角：{report.perspective_code}")

        lines.append("")

        # 核心结论
        lines.append("📊 核心结论")
        if report.core_conclusions:
            for i, conclusion in enumerate(report.core_conclusions, 1):
                # 确保每条结论非空
                if conclusion and conclusion.strip():
                    lines.append(f"{'①②③④⑤'[i-1] if i <= 5 else '·'} {conclusion}")
        else:
            lines.append("（分析未产生共识结论，请查看分歧点）")
        lines.append("")

        # 分歧点
        if report.divergent_points:
            lines.append("🔍 分歧点")
            for point in report.divergent_points:
                lines.append(f"- {point}")
            lines.append("")

        # 不确定性
        if report.uncertainties:
            lines.append("⚠️ 不确定性")
            for u in report.uncertainties:
                lines.append(f"- {u}")
            lines.append("")

        # 执行统计
        if report.execution_stats and report.execution_stats.total_tasks > 0:
            lines.append("📈 执行统计")
            es = report.execution_stats
            lines.append(f"- 总任务数：{es.total_tasks}")
            lines.append(f"- 成功：{es.completed} | 失败：{es.failed} | 超时：{es.timed_out} | 取消：{es.cancelled}")
            lines.append(f"- 总耗时：{es.total_duration_seconds:.1f}s")
            if es.total_tokens_used > 0:
                lines.append(f"- Token 消耗：{es.total_tokens_used}")
            lines.append("")

        # 尾部
        lines.append("═" * self.SEPARATOR_WIDTH)

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # 内部提取方法
    # ------------------------------------------------------------------

    def _extract_core_conclusions(
        self,
        strategy_rounds: List[StrategyRound],
        review_results: List[DecisionResult],
    ) -> List[str]:
        """提取核心结论"""
        conclusions: List[str] = []
        seen = set()

        # 从最后一轮策略中取共识点
        if strategy_rounds:
            last_round = strategy_rounds[-1]
            if last_round.verdict == ConsensusVerdict.CONSENSUS:
                for d in last_round.decisions:
                    for finding in d.top_findings:
                        normalized = finding.strip()
                        if normalized and normalized not in seen:
                            conclusions.append(finding)
                            seen.add(normalized)

        # 从审阅结果补充
        for d in review_results:
            for finding in d.top_findings:
                normalized = finding.strip()
                if normalized and normalized not in seen:
                    conclusions.append(finding)
                    seen.add(normalized)

        # 兜底：如果没有共识结论
        if not conclusions:
            if strategy_rounds:
                for rnd in strategy_rounds:
                    for d in rnd.decisions:
                        conclusions.append(f"[{d.agent_id}] {d.reasoning[:100]}...")
                        if len(conclusions) >= 3:
                            break
                    if len(conclusions) >= 3:
                        break

        return conclusions[:5]

    def _extract_divergent_points(
        self, strategy_rounds: List[StrategyRound]
    ) -> List[str]:
        """提取分歧点"""
        points: List[str] = []
        for rnd in strategy_rounds:
            if rnd.verdict == ConsensusVerdict.DIVERGENCE:
                configs = set(d.config.value for d in rnd.decisions)
                if len(configs) > 1:
                    points.append(f"配置档次分歧：{' vs '.join(configs)}")

                importances = [d.importance for d in rnd.decisions]
                if max(importances) - min(importances) > 1:
                    points.append(
                        f"重要性评分分歧：{min(importances)}-{max(importances)}"
                    )

                risks = []
                for d in rnd.decisions:
                    risks.extend(d.risks)
                if risks:
                    points.append(f"风险关注点不一致：涉及 {len(risks)} 个不同风险项")

        return points

    def _extract_uncertainties(
        self,
        strategy_rounds: List[StrategyRound],
        review_results: List[DecisionResult],
    ) -> List[str]:
        """提取不确定性"""
        uncertainties: List[str] = []

        for rnd in strategy_rounds:
            for d in rnd.decisions:
                if d.confidence < 0.5:
                    uncertainties.append(
                        f"决策者 {d.agent_id} 置信度较低 ({d.confidence:.0%})"
                    )

        # 去重
        return list(dict.fromkeys(uncertainties))[:5]

    def _determine_tier(
        self,
        strategy_rounds: List[StrategyRound],
        validated_input: UserInput,
    ) -> Tier:
        """确定最终配置档次"""
        if strategy_rounds:
            last_round = strategy_rounds[-1]
            if last_round.decisions:
                configs = [d.config for d in last_round.decisions]
                most_common = Counter(configs).most_common(1)
                if most_common:
                    return most_common[0][0]

        # 兜底：按重要性推断
        if validated_input.importance >= 4:
            return Tier.FULL
        elif validated_input.importance >= 2:
            return Tier.BALANCED
        return Tier.LIGHT
