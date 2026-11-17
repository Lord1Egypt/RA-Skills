"""
可执行熔断器 — 将 SKILL.md 中的自然语言熔断条件转为可执行逻辑。

6 条默认规则：TASK_FAILURE_RATE >50% → REDISTRIBUTE
              CONSENSUS_DIVERGENCE >2轮 → FALLBACK_TO_USER
              EXECUTOR_TIMEOUT → SKIP
              USER_INTERRUPT → STOP
              GLOBAL_TIMEOUT → STOP
              TOKEN_BUDGET_EXCEEDED → DEGRADE
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from schemas import (
    CircuitBreakerConfig,
    CircuitState,
    ExecutionReport,
    ExecutionResult,
    ExecutionStatus,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 熔断条件枚举
# ============================================================================

class BreakerCondition(str, Enum):
    """熔断条件"""
    TASK_FAILURE_RATE = "task_failure_rate"       # 子任务失败率 > 50%
    CONSENSUS_DIVERGENCE = "consensus_divergence"  # 共识分歧 > 2 轮
    EXECUTOR_TIMEOUT = "executor_timeout"          # 执行器超时
    USER_INTERRUPT = "user_interrupt"              # 用户中途打断
    GLOBAL_TIMEOUT = "global_timeout"              # 全局超时
    TOKEN_BUDGET_EXCEEDED = "token_budget_exceeded" # Token 预算超限


# ============================================================================
# 熔断动作枚举
# ============================================================================

class BreakerAction(str, Enum):
    """熔断动作"""
    REDISTRIBUTE = "redistribute"         # 重新分配
    DEGRADE = "degrade"                   # 降级执行
    SKIP = "skip"                         # 跳过
    FALLBACK_TO_USER = "fallback_to_user" # 转交用户
    STOP = "stop"                         # 立即停止
    CONTINUE = "continue"                 # 继续（不触发熔断）


# ============================================================================
# 熔断规则
# ============================================================================

@dataclass
class BreakerRule:
    """单条熔断规则"""
    condition: BreakerCondition
    threshold: Any
    action: BreakerAction
    description: str = ""


# ============================================================================
# 熔断引擎
# ============================================================================

class CircuitBreakerEngine:
    """Triangulate 可执行熔断引擎"""

    # 默认熔断规则表（对应原 SKILL.md 的熔断条件）
    DEFAULT_RULES: List[BreakerRule] = [
        BreakerRule(
            condition=BreakerCondition.TASK_FAILURE_RATE,
            threshold=0.5,
            action=BreakerAction.REDISTRIBUTE,
            description="子任务失败率 > 50% → 重新分配或降级执行",
        ),
        BreakerRule(
            condition=BreakerCondition.CONSENSUS_DIVERGENCE,
            threshold=2,
            action=BreakerAction.FALLBACK_TO_USER,
            description="共识分歧 > 2 轮 → 转交用户全权裁定",
        ),
        BreakerRule(
            condition=BreakerCondition.EXECUTOR_TIMEOUT,
            threshold=True,
            action=BreakerAction.SKIP,
            description="执行器超时 → 跳过该执行器，其他照常汇总",
        ),
        BreakerRule(
            condition=BreakerCondition.USER_INTERRUPT,
            threshold=True,
            action=BreakerAction.STOP,
            description="用户中途打断 → 立即停止，返回已有结果",
        ),
        BreakerRule(
            condition=BreakerCondition.GLOBAL_TIMEOUT,
            threshold=True,
            action=BreakerAction.STOP,
            description="全局超时 → 立即停止，返回已有结果",
        ),
        BreakerRule(
            condition=BreakerCondition.TOKEN_BUDGET_EXCEEDED,
            threshold=True,
            action=BreakerAction.DEGRADE,
            description="Token 预算超限 → 降级到轻量配置",
        ),
    ]

    def __init__(self, rules: Optional[List[BreakerRule]] = None):
        self.rules = rules or self.DEFAULT_RULES
        self.rule_map: Dict[BreakerCondition, BreakerRule] = {
            r.condition: r for r in self.rules
        }
        self.triggered_conditions: List[BreakerCondition] = []
        self.user_interrupted: bool = False

    # ------------------------------------------------------------------
    # 条件检查
    # ------------------------------------------------------------------

    def check_task_failure_rate(self, report: ExecutionReport) -> Optional[BreakerAction]:
        """
        检查子任务失败率。

        规则: failure_rate > 50% → REDISTRIBUTE
        """
        rule = self.rule_map.get(BreakerCondition.TASK_FAILURE_RATE)
        if not rule:
            return None

        failure_rate = report.failure_rate
        if failure_rate > rule.threshold:
            logger.warning(
                f"熔断触发: 子任务失败率 {failure_rate:.1%} > {rule.threshold:.0%}"
            )
            self.triggered_conditions.append(BreakerCondition.TASK_FAILURE_RATE)
            return BreakerAction.REDISTRIBUTE

        return BreakerAction.CONTINUE

    def check_consensus_divergence(self, divergence_rounds: int) -> Optional[BreakerAction]:
        """
        检查共识分歧轮次。

        规则: divergence_rounds > 2 → FALLBACK_TO_USER
        """
        rule = self.rule_map.get(BreakerCondition.CONSENSUS_DIVERGENCE)
        if not rule:
            return None

        if divergence_rounds > rule.threshold:
            logger.warning(
                f"熔断触发: 共识分歧 {divergence_rounds} 轮 > {rule.threshold} 轮"
            )
            self.triggered_conditions.append(BreakerCondition.CONSENSUS_DIVERGENCE)
            return BreakerAction.FALLBACK_TO_USER

        return BreakerAction.CONTINUE

    def check_executor_timeout(self, result: ExecutionResult) -> Optional[BreakerAction]:
        """
        检查执行器超时。

        规则: status == TIMEOUT → SKIP
        """
        if result.status == ExecutionStatus.TIMEOUT:
            logger.info(f"执行器超时: {result.subtask_id}，跳过")
            self.triggered_conditions.append(BreakerCondition.EXECUTOR_TIMEOUT)
            return BreakerAction.SKIP
        return BreakerAction.CONTINUE

    def check_user_interrupt(self) -> Optional[BreakerAction]:
        """
        检查用户打断。

        规则: user_interrupted → STOP
        """
        if self.user_interrupted:
            logger.warning("用户中断信号已触发")
            self.triggered_conditions.append(BreakerCondition.USER_INTERRUPT)
            return BreakerAction.STOP
        return BreakerAction.CONTINUE

    def check_global_timeout(self, elapsed: float, limit: float) -> Optional[BreakerAction]:
        """
        检查全局超时。

        规则: elapsed > limit → STOP
        """
        if elapsed > limit:
            logger.warning(f"全局超时: {elapsed:.1f}s > {limit:.1f}s")
            self.triggered_conditions.append(BreakerCondition.GLOBAL_TIMEOUT)
            return BreakerAction.STOP
        return BreakerAction.CONTINUE

    def check_token_budget(
        self, used: int, limit: int
    ) -> Optional[BreakerAction]:
        """
        检查 Token 预算。

        规则: used > limit → DEGRADE
        """
        if used > limit:
            logger.warning(f"Token 预算超限: {used} > {limit}")
            self.triggered_conditions.append(BreakerCondition.TOKEN_BUDGET_EXCEEDED)
            return BreakerAction.DEGRADE
        return BreakerAction.CONTINUE

    # ------------------------------------------------------------------
    # 熔断动作执行
    # ------------------------------------------------------------------

    def execute_action(
        self,
        action: BreakerAction,
        ctx: Any = None,
        decomposer: Any = None,
        dispatcher: Any = None,
    ) -> Dict[str, Any]:
        """执行熔断动作。

        根据动作类型执行相应的阻断逻辑：
        - REDISTRIBUTE: 重建 DAG 并重新执行
        - DEGRADE: 降级到轻量配置
        - SKIP: 跳过当前执行器
        - FALLBACK_TO_USER: 标记需要用户干预
        - STOP: 立即停止

        Args:
            action: 熔断动作类型
            ctx: PipelineContext（REDISTRIBUTE/DEGRADE 需要）
            decomposer: TaskDecomposer（REDISTRIBUTE 需要）
            dispatcher: ExecutionDispatcher（REDISTRIBUTE 需要）

        Returns:
            Dict: 包含 new_ctx（可能更新后的上下文）和 stop_reason
        """
        result: Dict[str, Any] = {"action": action.value, "stop": False, "new_ctx": ctx}

        if action == BreakerAction.REDISTRIBUTE:
            if decomposer and ctx and ctx.strategy_rounds:
                logger.warning("执行熔断动作 REDISTRIBUTE：重建 DAG 并重新执行")
                new_dag = decomposer.decompose(
                    ctx.strategy_rounds[-1] if ctx.strategy_rounds else None,
                    ctx.validated_input,
                )
                ctx = ctx.evolve(task_dag=new_dag, degraded=True)
                if dispatcher and ctx.task_dag:
                    new_report = dispatcher.dispatch(ctx.task_dag)
                    ctx = ctx.evolve(exec_report=new_report)
                result["new_ctx"] = ctx

        elif action == BreakerAction.DEGRADE:
            logger.warning("执行熔断动作 DEGRADE：降级到轻量配置")
            if ctx:
                from schemas import TaskDAG
                ctx = ctx.evolve(degraded=True)
                # 限制子任务数为 1（轻量模式），使用 evolve 创建新实例而非原地修改
                if ctx.task_dag and len(ctx.task_dag.subtasks) > 1:
                    new_dag = TaskDAG(subtasks=list(ctx.task_dag.subtasks[:1]))
                    ctx = ctx.evolve(task_dag=new_dag)
                result["new_ctx"] = ctx

        elif action == BreakerAction.SKIP:
            logger.info("执行熔断动作 SKIP：跳过当前执行器")
            result["skip"] = True

        elif action == BreakerAction.FALLBACK_TO_USER:
            logger.warning("执行熔断动作 FALLBACK_TO_USER：标记需要用户干预")
            if ctx:
                ctx = ctx.evolve(degraded=True)
                result["new_ctx"] = ctx

        elif action == BreakerAction.STOP:
            logger.warning("执行熔断动作 STOP：立即停止")
            result["stop"] = True
            result["stop_reason"] = (
                "用户中断" if self.user_interrupted else "全局超时"
            )

        return result

    # ------------------------------------------------------------------
    # 信号管理
    # ------------------------------------------------------------------

    def signal_user_interrupt(self):
        """发出用户中断信号"""
        self.user_interrupted = True
        logger.info("收到用户中断信号")

    def reset(self):
        """重置所有熔断状态"""
        self.triggered_conditions.clear()
        self.user_interrupted = False

    def get_report(self) -> Dict[str, Any]:
        """获取熔断器状态报告"""
        return {
            "triggered_conditions": [c.value for c in self.triggered_conditions],
            "user_interrupted": self.user_interrupted,
            "total_triggers": len(self.triggered_conditions),
        }
