"""
工作单元 (Unit of Work) — 统一 Saga/无 Saga 路径的事务边界。

替代 StepExecutor + Saga 的闭包注册-执行时间窗口问题：
- 所有操作先注册，再统一执行
- 补偿操作在执行时注册（而非注册时），消除闭包捕获过期引用
- 回滚失败记录到专门的日志，不被静默吞掉
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional

from pipeline import PipelineContext
from execution_context import ExecutionContext
from pipeline_guard import enforce_stage_contract
from side_effects import SideEffectCollector

logger = logging.getLogger(__name__)


class StepDefinition:
    """单个工作流步骤定义"""

    def __init__(
        self,
        step_name: str,
        action_fn: Callable[[ExecutionContext], PipelineContext],
        has_side_effects: bool = False,
        guard_stage: Optional[str] = None,
    ):
        self.step_name = step_name
        self.action_fn = action_fn
        self.has_side_effects = has_side_effects
        self.guard_stage = guard_stage


class WorkflowUnitOfWork:
    """工作流事务边界 — 确保失败时所有副作用自动撤销。

    用法:
        uow = WorkflowUnitOfWork(
            exec_ctx=exec_ctx,
            on_ctx_sync=lambda ctx: orchestrator._sync_ctx(ctx),
            state_machine=state_machine,
            side_effects=side_effects,
            session_manager=session_manager,
        )
        uow.add_step("strategy", lambda ec: run_strategy_phase(ec.get(), ...), has_side_effects=True, guard_stage="STRATEGY")
        uow.add_step("execute", lambda ec: run_execute_phase(ec.get(), ...), has_side_effects=True, guard_stage="EXECUTE")
        result = uow.execute()  # 全部成功返回 ctx，任一步骤失败自动逆序回滚
    """

    def __init__(
        self,
        exec_ctx: ExecutionContext,
        on_ctx_sync: Callable[[PipelineContext], None],
        state_machine: Any = None,
        side_effects: Optional[SideEffectCollector] = None,
        session_manager: Any = None,
    ):
        """
        Args:
            exec_ctx: 线程安全的执行上下文
            on_ctx_sync: 上下文同步回调（orchestrator 的 _sync_ctx）
            state_machine: 显式状态机
            side_effects: 副作用收集器
            session_manager: 会话管理器（回滚时需要 terminate 方法）
        """
        self._exec_ctx = exec_ctx
        self._on_ctx_sync = on_ctx_sync
        self._state_machine = state_machine
        self._side_effects = side_effects or SideEffectCollector()
        self._session_manager = session_manager
        self._steps: List[StepDefinition] = []
        self._compensations: List[Callable[[], None]] = []
        self._executed_steps: List[str] = []
        self._failed_compensations: List[Dict[str, str]] = []

    # ------------------------------------------------------------------
    # 注册步骤
    # ------------------------------------------------------------------

    def add_step(
        self,
        step_name: str,
        action_fn: Callable[[ExecutionContext], PipelineContext],
        has_side_effects: bool = False,
        guard_stage: Optional[str] = None,
    ) -> "WorkflowUnitOfWork":
        """注册一个工作流步骤（链式调用）。

        Args:
            step_name: 步骤名称
            action_fn: 执行函数，接收 ExecutionContext，返回新 PipelineContext
            has_side_effects: 是否产生副作用
            guard_stage: 阶段间契约守卫名称
        """
        self._steps.append(StepDefinition(
            step_name=step_name,
            action_fn=action_fn,
            has_side_effects=has_side_effects,
            guard_stage=guard_stage,
        ))
        return self

    # ------------------------------------------------------------------
    # 执行
    # ------------------------------------------------------------------

    def execute(self) -> PipelineContext:
        """执行所有已注册的步骤。

        按注册顺序执行。任一步骤失败 → 逆序调用已执行步骤的补偿操作。

        Returns:
            PipelineContext: 执行完成后的上下文

        Raises:
            Exception: 任一步骤失败时，先回滚再重新抛出
        """
        self._executed_steps = []
        self._compensations = []
        self._failed_compensations = []

        try:
            for step in self._steps:
                new_ctx = self._execute_step(step)
                self._executed_steps.append(step.step_name)
                # 执行成功后注册补偿操作（此时引用是新鲜的）
                self._compensations.append(
                    self._make_compensation(step.step_name)
                )

            return self._exec_ctx.get()

        except Exception as e:
            logger.error(
                f"WorkflowUnitOfWork 在步骤 '{self._steps[len(self._executed_steps)].step_name}' "
                f"失败，开始逆序回滚 {len(self._executed_steps)} 个已执行步骤"
            )
            self._rollback_executed_steps()
            raise

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------

    def _execute_step(self, step: StepDefinition) -> PipelineContext:
        """执行单个步骤并同步上下文。"""
        new_ctx = step.action_fn(self._exec_ctx)

        # 单一写入点：先写 ExecutionContext（线程安全），再通过回调同步
        self._exec_ctx.update(new_ctx)
        self._on_ctx_sync(new_ctx)

        if self._state_machine:
            self._state_machine.set_pipeline_context(new_ctx)

        # 追踪副作用
        if step.has_side_effects:
            self._side_effects.track_step(step.step_name, new_ctx)

        # 阶段间契约守卫
        if step.guard_stage:
            enforce_stage_contract(step.guard_stage, new_ctx)

        # 一致性校验
        new_ctx.assert_consistency()

        return new_ctx

    def _make_compensation(self, step_name: str) -> Callable[[], None]:
        """创建补偿操作闭包（在执行时创建，引用是新鲜的）。"""

        def compensate():
            sessions = self._side_effects.get_step_sessions(step_name)
            if sessions:
                logger.info(
                    f"UoW 回滚步骤 '{step_name}': 清理 {len(sessions)} 个 sessions"
                )
                self._side_effects.rollback_step(step_name, self._session_manager)
            else:
                logger.debug(f"步骤 '{step_name}' 无副作用，跳过回滚")

        return compensate

    def _rollback_executed_steps(self) -> None:
        """逆序执行已注册的补偿操作。"""
        for i in range(len(self._compensations) - 1, -1, -1):
            step_name = self._executed_steps[i]
            try:
                self._compensations[i]()
                logger.info(f"UoW 补偿步骤 '{step_name}' 完成")
            except Exception as comp_err:
                logger.error(f"UoW 补偿步骤 '{step_name}' 失败: {comp_err}")
                self._failed_compensations.append({
                    "step": step_name,
                    "error": str(comp_err),
                })

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------

    def get_executed_steps(self) -> List[str]:
        """获取已执行步骤列表"""
        return list(self._executed_steps)

    def get_failed_compensations(self) -> List[Dict[str, str]]:
        """获取补偿失败的记录"""
        return list(self._failed_compensations)

    @property
    def step_count(self) -> int:
        return len(self._steps)

    # ------------------------------------------------------------------
    # 重置
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """重置工作单元（每次新工作流执行前调用）"""
        self._steps.clear()
        self._compensations.clear()
        self._executed_steps.clear()
        self._failed_compensations.clear()
