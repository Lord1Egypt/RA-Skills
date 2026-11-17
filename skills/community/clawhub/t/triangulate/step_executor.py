"""
步骤执行器 — 原子执行单个工作流步骤，统一 Saga/无 Saga 路径。

交互时序：
  Saga 模式: StepExecutor → Saga.add_step → Saga.execute → action/compensate
  无 Saga 模式: StepExecutor → action 直接执行
  双重回滚防护: Saga compensate → SideEffectCollector.rollback_step()
                _handle_failure → SideEffectCollector.rollback_all() → 跳过已回滚
"""
from __future__ import annotations

import logging
from typing import Any, Callable, List, Optional

from pipeline import PipelineContext
from execution_context import ExecutionContext
from side_effects import SideEffectCollector
from pipeline_guard import enforce_stage_contract, PipelineContractError
from saga import WorkflowSaga

logger = logging.getLogger(__name__)


class StepExecutor:
    """[Deprecated] 步骤执行器 — 已被 WorkflowUnitOfWork 替代。

    当前仅用于维持 orchestrator 中的 ExecutionContext 访问和 ContextBus 回调兼容。
    主工作流的步骤执行和事务回滚已由 WorkflowUnitOfWork 接管。

    Saga 模式（saga 参数非 None）已废弃——不再通过闭包注册 Saga 步骤。

    用法（向后兼容）:
        executor = StepExecutor(
            exec_ctx=exec_ctx,
            on_ctx_sync=lambda ctx: orchestrator._sync_ctx(ctx),
            state_machine=state_machine,
            side_effects=side_effects,
            saga=None,  # UoW 已接管事务回滚
        )
    """

    def __init__(
        self,
        exec_ctx: ExecutionContext,
        on_ctx_sync: Callable[[PipelineContext], None],
        state_machine: Any = None,
        side_effects: Optional[SideEffectCollector] = None,
        saga: Optional[WorkflowSaga] = None,
    ):
        """
        Args:
            exec_ctx: 线程安全的执行上下文
            on_ctx_sync: 上下文同步回调（orchestrator 的 _sync_ctx）
            state_machine: 显式状态机
            side_effects: 副作用收集器
            saga: Saga 事务管理器（None = 无 Saga 模式）
        """
        self._exec_ctx = exec_ctx
        self._on_ctx_sync = on_ctx_sync
        self._state_machine = state_machine
        self._side_effects = side_effects or SideEffectCollector()
        self._saga = saga
        self._rolled_back_steps: set = set()  # 已回滚步骤标记

    def execute(
        self,
        step_name: str,
        action_fn: Callable[[ExecutionContext], PipelineContext],
        has_side_effects: bool = False,
        guard_stage: Optional[str] = None,
    ) -> None:
        """执行单个工作流步骤。

        统一路径：Saga 模式下注册步骤，无 Saga 模式下直接执行。
        副作用通过 SideEffectCollector 统一追踪。
        compensate 闭包实际执行回滚（不再空操作）。

        Args:
            step_name: 步骤名称
            action_fn: 执行函数，接收 ExecutionContext，返回新 PipelineContext
            has_side_effects: 是否产生副作用
            guard_stage: 阶段间契约守卫名称
        """
        has_saga = self._saga is not None

        # ---- action 闭包：执行 + 单一写入点同步 + 一致性校验 ----
        def action():
            new_ctx = action_fn(self._exec_ctx)
            # 单一写入点：先写 ExecutionContext（线程安全），再通过回调同步
            self._exec_ctx.update(new_ctx)
            self._on_ctx_sync(new_ctx)
            if self._state_machine:
                self._state_machine.set_pipeline_context(new_ctx)
            # 追踪副作用
            if has_side_effects:
                self._side_effects.track_step(step_name, new_ctx)
            # 阶段间契约守卫
            if guard_stage:
                enforce_stage_contract(guard_stage, new_ctx)
            # 每个步骤执行后自动校验 sessions 一致性
            new_ctx.assert_consistency()
            return new_ctx

        # ---- compensate 闭包：实际执行回滚 ----
        def compensate():
            if step_name in self._rolled_back_steps:
                logger.info(f"步骤 '{step_name}' 已回滚过，跳过重复回滚")
                return
            self._rolled_back_steps.add(step_name)
            # 实际回滚：终止该步骤产生的 sessions
            sessions = self._side_effects.get_step_sessions(step_name)
            if sessions:
                logger.info(
                    f"Saga 回滚步骤 '{step_name}': 清理 {len(sessions)} 个 sessions"
                )
                self._side_effects.rollback_step(step_name)
            else:
                logger.debug(f"步骤 '{step_name}' 无副作用，跳过回滚")

        if has_saga:
            self._saga.add_step(
                step_name, action, compensate,
                metadata={
                    "type": "side_effect" if has_side_effects else "pure_computation",
                },
            )
        else:
            action()

    def reset(self) -> None:
        """重置回滚标记（每次新工作流执行前调用）"""
        self._rolled_back_steps.clear()

    def sync_context(self, new_ctx: PipelineContext) -> None:
        """同步上下文到内部 ExecutionContext（由 orchestrator 回调调用）。"""
        self._exec_ctx.update(new_ctx)

    def get_exec_ctx(self) -> ExecutionContext:
        """获取内部 ExecutionContext 引用（由 orchestrator 调用）。"""
        return self._exec_ctx
