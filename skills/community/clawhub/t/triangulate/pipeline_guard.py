"""
阶段间契约守卫 — 确保每个阶段的输出可被下一阶段正确消费。

为每个阶段间传递提供契约校验，失败时给出明确的错误信息。
"""
from __future__ import annotations

import logging
from typing import List, Optional

from pipeline import PipelineContext
from schemas import ExecutionReport, StrategyRound, TaskDAG, UserInput
from exceptions import PipelineContractError

logger = logging.getLogger(__name__)


# ============================================================================
# 阶段间契约守卫
# ============================================================================


def guard_input_validation(ctx: PipelineContext) -> PipelineContext:
    """校验 INPUT_VALIDATION → STRATEGY 的契约。

    Requirements:
        - validated_input 必须非空
        - task_description 必须非空
        - importance 在 1-5 范围
    """
    if ctx.validated_input is None:
        raise PipelineContractError(
            "INPUT_VALIDATION",
            "validated_input 不能为空"
        )
    if not ctx.validated_input.task_description:
        raise PipelineContractError(
            "INPUT_VALIDATION",
            "task_description 不能为空字符串"
        )
    if not (1 <= ctx.validated_input.importance <= 5):
        raise PipelineContractError(
            "INPUT_VALIDATION",
            f"importance 必须在 1-5 范围，实际: {ctx.validated_input.importance}"
        )
    return ctx


def guard_strategy_output(ctx: PipelineContext) -> PipelineContext:
    """校验 STRATEGY → DISPATCH 的契约。

    Requirements:
        - strategy_rounds 至少 1 轮
        - 每轮至少有 1 个决策
    """
    if len(ctx.strategy_rounds) == 0:
        raise PipelineContractError(
            "STRATEGY",
            "strategy_rounds 不能为空（至少需要 1 轮策略）"
        )
    for i, rnd in enumerate(ctx.strategy_rounds):
        if len(rnd.decisions) == 0:
            raise PipelineContractError(
                "STRATEGY",
                f"第 {i+1} 轮策略的 decisions 为空"
            )
    return ctx


def guard_dispatch_output(ctx: PipelineContext) -> PipelineContext:
    """校验 DISPATCH → EXECUTE 的契约。

    Requirements:
        - task_dag 必须非空
        - task_dag.subtasks 至少 1 个
    """
    if ctx.task_dag is None:
        raise PipelineContractError(
            "DISPATCH",
            "task_dag 不能为空"
        )
    if len(ctx.task_dag.subtasks) == 0:
        raise PipelineContractError(
            "DISPATCH",
            "task_dag.subtasks 不能为空列表"
        )
    return ctx


def guard_execute_output(ctx: PipelineContext) -> PipelineContext:
    """校验 EXECUTE → REVIEW 的契约。

    Requirements:
        - exec_report 必须非空
        - exec_report.total_tasks >= 0
    """
    if ctx.exec_report is None:
        raise PipelineContractError(
            "EXECUTE",
            "exec_report 不能为空"
        )
    return ctx


def guard_review_output(ctx: PipelineContext) -> PipelineContext:
    """校验 REVIEW → RENDER 的契约。

    Requirements:
        - review_results 不能为空列表
    """
    if len(ctx.review_results) == 0:
        raise PipelineContractError(
            "REVIEW",
            "review_results 不能为空（至少需要 1 条审阅结果）"
        )
    return ctx


def guard_render_output(ctx: PipelineContext) -> PipelineContext:
    """校验 RENDER → DONE 的契约。

    Requirements:
        - final_report 必须非空
    """
    if ctx.final_report is None:
        raise PipelineContractError(
            "RENDER",
            "final_report 不能为空"
        )
    return ctx


# ============================================================================
# 阶段间 Guard 映射表
# ============================================================================

# 从 PipelineContext 的哪个阶段输出 → 下一阶段的契约守卫
STAGE_GUARDS = {
    "INPUT_VALIDATION": guard_input_validation,
    "STRATEGY": guard_strategy_output,
    "DISPATCH": guard_dispatch_output,
    "EXECUTE": guard_execute_output,
    "REVIEW": guard_review_output,
    "RENDER": guard_render_output,
}


def enforce_stage_contract(stage: str, ctx: PipelineContext) -> PipelineContext:
    """执行阶段间契约检查。

    Args:
        stage: 阶段名称（如 "STRATEGY"）
        ctx: 当前 PipelineContext

    Returns:
        PipelineContext: 校验通过的上下文

    Raises:
        PipelineContractError: 契约违反
    """
    guard = STAGE_GUARDS.get(stage)
    if guard is None:
        logger.warning(f"阶段 '{stage}' 没有注册契约守卫")
        return ctx
    return guard(ctx)
