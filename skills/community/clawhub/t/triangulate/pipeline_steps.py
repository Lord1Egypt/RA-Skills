"""
管线阶段函数 — Triangulate 工作流的 7 个独立阶段函数。

每个函数签名 (PipelineContext, dependencies) -> PipelineContext，
可独立测试，不依赖 orchestrator 实例。
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional

from schemas import (
    ConsensusVerdict,
    DecisionResult,
    DivergenceAction,
    ExecutionReport,
    FinalReport,
    StrategyRound,
    SubTask,
    TaskDAG,
    Tier,
    UserInput,
    WorkflowPhase,
)
from pipeline import PipelineContext
from circuit_breaker import BreakerAction

logger = logging.getLogger(__name__)

MAX_STRATEGY_ROUNDS = 3


# ============================================================================
# 策略阶段
# ============================================================================

def run_strategy_phase(
    ctx: PipelineContext,
    consensus_engine: Any,
    generate_default_decisions: Callable[[UserInput], List[DecisionResult]],
) -> PipelineContext:
    """阶段：决策层 — 3 视角共识

    返回新的 PipelineContext，包含 strategy_rounds 和 divergence_rounds。
    """
    if not consensus_engine:
        logger.warning("没有共识引擎，使用兜底策略")
        decisions = generate_default_decisions(ctx.validated_input)
        strategy_round = StrategyRound(
            round_number=1,
            decisions=decisions,
            verdict=ConsensusVerdict.CONSENSUS,
        )
        return ctx.evolve(
            strategy_rounds=[strategy_round],
            degraded=True,
            divergence_rounds=0,
        )

    rounds: List[StrategyRound] = []
    divergence_rounds = 0

    for round_num in range(1, MAX_STRATEGY_ROUNDS + 1):
        decisions = consensus_engine.gather_decisions(ctx.validated_input, round_num)

        if not decisions:
            logger.warning(
                f"策略阶段第 {round_num} 轮：gather_decisions 返回空！使用默认决策兜底。"
            )
            decisions = generate_default_decisions(ctx.validated_input)

        verdict_output = consensus_engine.evaluate(decisions)
        strategy_round = StrategyRound(
            round_number=round_num,
            decisions=decisions,
            verdict=verdict_output.verdict,
        )
        rounds.append(strategy_round)

        if verdict_output.verdict == ConsensusVerdict.CONSENSUS:
            break

        if verdict_output.verdict == ConsensusVerdict.FALLBACK_TO_USER:
            logger.info("分歧超限，转交用户裁决")
            break

        if verdict_output.verdict == ConsensusVerdict.DIVERGENCE:
            divergence_rounds = round_num
            handle_result = consensus_engine.handle_divergence(decisions, round_num)
            if handle_result.verdict == ConsensusVerdict.FALLBACK_TO_USER:
                logger.info("handle_divergence 判定转交用户")
                break
            logger.info(f"第 {round_num} 轮分歧，进入第 {round_num + 1} 轮重试")

    return ctx.evolve(
        strategy_rounds=rounds,
        divergence_rounds=divergence_rounds,
        degraded=ctx.degraded or (divergence_rounds >= 2),
    )


# ============================================================================
# 熔断检查 — 共识分歧
# ============================================================================

def run_breaker_divergence(
    ctx: PipelineContext,
    breaker: Any,
) -> PipelineContext:
    """检查共识分歧是否触发熔断"""
    if breaker:
        divergence_rounds = ctx.divergence_rounds
        action = breaker.check_consensus_divergence(divergence_rounds)
        if action == BreakerAction.FALLBACK_TO_USER:
            logger.warning(
                f"共识分歧触发熔断 (divergence_rounds={divergence_rounds})，转交用户"
            )
            return ctx.evolve(degraded=True)
    return ctx


# ============================================================================
# 任务拆解阶段
# ============================================================================

def run_dispatch_phase(
    ctx: PipelineContext,
    decomposer: Any,
) -> PipelineContext:
    """阶段：管理层 — 任务拆解"""
    if not decomposer:
        logger.warning("没有拆解器，创建默认单任务 DAG")
        dag = TaskDAG(subtasks=[
            SubTask(
                id="subtask-default",
                goal=ctx.validated_input.task_description,
                completion_criteria="完成分析并返回结果",
                output_format="Markdown 报告",
            )
        ])
    else:
        strategy = ctx.strategy_rounds[-1] if ctx.strategy_rounds else None
        dag = decomposer.decompose(strategy, ctx.validated_input)

    return ctx.evolve(task_dag=dag)


# ============================================================================
# 执行阶段
# ============================================================================

def run_execute_phase(
    ctx: PipelineContext,
    dispatcher: Any,
) -> PipelineContext:
    """阶段：执行层 — 并行执行子任务"""
    if not dispatcher:
        logger.warning("没有调度器，返回空执行报告")
        report = ExecutionReport(
            total_tasks=0, completed=0, failed=0,
            timed_out=0, cancelled=0, results=[],
        )
    else:
        report = dispatcher.dispatch(ctx.task_dag)

    return ctx.evolve(exec_report=report)


# ============================================================================
# 熔断检查 — 执行失败率（含 REDISTRIBUTE）
# ============================================================================

def run_breaker_failure(
    ctx: PipelineContext,
    breaker: Any,
    decomposer: Any,
    run_execute_phase_fn: Callable[[PipelineContext], PipelineContext],
) -> PipelineContext:
    """检查执行失败率是否触发熔断。

    使用 CircuitBreakerEngine.execute_action() 统一处理熔断动作，
    消除分散在 pipeline_steps 中的熔断执行逻辑。
    """
    if not breaker:
        return ctx

    if ctx.exec_report is None:
        logger.warning("exec_report 为空，跳过失败率检查")
        return ctx

    action = breaker.check_task_failure_rate(ctx.exec_report)
    if action == BreakerAction.CONTINUE:
        return ctx

    # 使用统一的 execute_action 接口
    result = breaker.execute_action(
        action,
        ctx=ctx,
        decomposer=decomposer,
        dispatcher=None,  # dispatcher 由 run_execute_phase_fn 内部使用
    )
    ctx = result.get("new_ctx", ctx)

    # 如果 REDISTRIBUTE 没有内置 dispatcher，使用回调函数重执行
    if action == BreakerAction.REDISTRIBUTE and ctx.task_dag:
        ctx = run_execute_phase_fn(ctx)

    return ctx


# ============================================================================
# 审阅阶段
# ============================================================================

def run_review_phase(
    ctx: PipelineContext,
    consensus_engine: Any,
    generate_default_decisions: Callable[[UserInput], List[DecisionResult]],
) -> PipelineContext:
    """阶段：决策层审阅"""
    if not consensus_engine:
        results = generate_default_decisions(
            ctx.validated_input or UserInput(task_description="默认任务")
        )
    else:
        results = consensus_engine.review_results(ctx.exec_report)

        if not results and ctx.strategy_rounds:
            last_round = ctx.strategy_rounds[-1]
            results = last_round.decisions

    return ctx.evolve(review_results=results)


# ============================================================================
# 渲染阶段
# ============================================================================

def run_render_phase(
    ctx: PipelineContext,
    renderer: Any,
) -> PipelineContext:
    """阶段：输出渲染。

    无 renderer 时使用 ReportRenderer 的 render 方法作为唯一兜底逻辑，
    消除与 renderer.py 的重复代码。
    """
    if renderer is None:
        # 使用 ReportRenderer 作为默认渲染器（唯一兜底路径）
        from renderer import ReportRenderer
        renderer = ReportRenderer()

    report = renderer.render(
        ctx.validated_input,
        ctx.strategy_rounds,
        ctx.exec_report,
        ctx.review_results,
        degraded=ctx.degraded,
    )

    return ctx.evolve(final_report=report)
