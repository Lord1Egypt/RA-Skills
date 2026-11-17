"""
Saga 事务编排器 — 副作用管理与回滚。

Triangulate 工作流中涉及 sessions_spawn（创建子会话）等副作用操作。
Saga 模式确保：任一步骤失败 → 逆序调用已执行步骤的补偿操作。
"""
from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional

from schemas import SagaReport, SagaStepResult
from exceptions import SagaConfigurationError

logger = logging.getLogger(__name__)


# ============================================================================
# Saga 步骤定义
# ============================================================================

@dataclass
class SagaStep:
    """Saga 事务步骤：正向操作 + 补偿操作。_compensated 幂等标记确保补偿只执行一次。"""
    name: str
    action: Callable[[], Any]
    compensate: Callable[[], Any]
    metadata: dict = field(default_factory=dict)

    _compensated: bool = field(default=False, init=False, repr=False)
    _executed: bool = field(default=False, init=False, repr=False)

    def execute(self) -> SagaStepResult:
        """执行正向操作"""
        self._executed = True
        try:
            output = self.action()
            return SagaStepResult(
                step_name=self.name,
                success=True,
                output=output,
            )
        except Exception as e:
            logger.error(f"Saga 步骤 '{self.name}' 执行失败: {e}")
            return SagaStepResult(
                step_name=self.name,
                success=False,
                error=str(e),
            )

    def rollback(self) -> SagaStepResult:
        """执行补偿操作（幂等：多次调用只执行一次）"""
        if self._compensated:
            logger.info(f"Saga 步骤 '{self.name}' 已补偿过，跳过重复回滚")
            return SagaStepResult(
                step_name=self.name,
                success=True,
                compensated=True,
            )
        self._compensated = True
        try:
            self.compensate()
            return SagaStepResult(
                step_name=self.name,
                success=True,
                compensated=True,
            )
        except Exception as e:
            logger.error(f"Saga 补偿 '{self.name}' 失败: {e}")
            return SagaStepResult(
                step_name=self.name,
                success=False,
                compensated=True,
                compensation_error=str(e),
            )


# ============================================================================
# Saga 编排器
# ============================================================================

class WorkflowSaga:
    """Triangulate 工作流的 Saga 编排器

    用法:
        saga = WorkflowSaga()
        saga.add_step(
            name="input_validation",
            action=lambda: adapter.validate(user_input),
            compensate=lambda: None,  # 纯校验，无副作用
        )
        saga.add_step(
            name="spawn_decision_agents",
            action=lambda: spawn_agents(3),
            compensate=lambda: terminate_all(session_ids),  # 回滚：终止所有子会话
        )
        report = saga.execute()
    """

    def __init__(self, session_manager: Optional[Any] = None):
        self.steps: List[SagaStep] = []
        self.session_manager = session_manager
        self._created_sessions: List[str] = []
        self._global_timeout: Optional[float] = None

    def add_step(
        self,
        name: str,
        action: Callable[[], Any],
        compensate: Callable[[], Any],
        metadata: Optional[dict] = None,
    ) -> "WorkflowSaga":
        """添加 Saga 步骤（链式调用）"""
        self.steps.append(SagaStep(
            name=name,
            action=action,
            compensate=compensate,
            metadata=metadata or {},
        ))
        return self

    def set_global_timeout(self, seconds: float) -> "WorkflowSaga":
        """设置全局超时"""
        self._global_timeout = seconds
        return self

    def reset_steps(self):
        """重置所有步骤的补偿状态（用于 orchestrator.reset() 后复用 Saga）"""
        self.steps.clear()
        self._created_sessions.clear()

    def _reset_compensation_flags(self):
        """重置所有步骤的 _compensated 标记（每次 execute() 前调用）"""
        for step in self.steps:
            step._compensated = False
            step._executed = False

    def execute(self) -> SagaReport:
        """执行所有 Saga 步骤。任一步骤失败 → 逆序回滚所有已执行步骤。"""
        import time
        self._reset_compensation_flags()
        start_time = time.time()
        executed_steps: List[SagaStepResult] = []
        failed_step_name: Optional[str] = None

        for i, step in enumerate(self.steps):
            # 检查全局超时
            if self._global_timeout and (time.time() - start_time) > self._global_timeout:
                failed_step_name = step.name
                logger.warning(f"Saga 全局超时 ({self._global_timeout}s)，在步骤 '{step.name}' 中断")
                break

            result = step.execute()
            executed_steps.append(result)

            if not result.success:
                failed_step_name = step.name
                logger.error(f"Saga 在步骤 {i+1}/{len(self.steps)} '{step.name}' 失败")
                break

        # 判断是否全部成功
        all_success = failed_step_name is None

        if all_success:
            return SagaReport(
                success=True,
                steps=executed_steps,
                total_steps=len(self.steps),
                successful_steps=len(executed_steps),
                rolled_back_steps=0,
            )

        # ---- 回滚阶段 ----
        rollback_results: List[SagaStepResult] = []
        successful_before_failure = executed_steps[:-1]  # 排除失败的那一步

        for step_result in reversed(successful_before_failure):
            # 找到对应的 SagaStep 执行补偿
            step_name = step_result.step_name
            original_step = next(
                (s for s in self.steps if s.name == step_name), None
            )
            if original_step:
                rollback_result = original_step.rollback()
                rollback_results.append(rollback_result)

        return SagaReport(
            success=False,
            steps=executed_steps,
            failed_step=failed_step_name,
            total_steps=len(self.steps),
            successful_steps=len(successful_before_failure),
            rolled_back_steps=len(rollback_results),
            error=executed_steps[-1].error if executed_steps else None,
        )


    # ------------------------------------------------------------------
    # 内部方法（被 orchestrator 使用）
    # ------------------------------------------------------------------

    def _spawn_and_track(
        self, spawn_fn: Callable, session_ids_ref: List[str]
    ) -> Any:
        """[Deprecated] 执行 spawn 并追踪 session IDs。请使用 SideEffectCollector。"""
        logger.warning(
            "Saga._spawn_and_track() 已废弃，请使用 SideEffectCollector 追踪 sessions"
        )
        result = spawn_fn()
        if hasattr(result, "session_ids"):
            ids = result.session_ids
        elif isinstance(result, list):
            ids = [str(r) for r in result]
        else:
            ids = [str(result)]
        session_ids_ref.clear()
        session_ids_ref.extend(ids)
        self._created_sessions.extend(ids)
        return result

    def _terminate_sessions(self, session_ids_ref: List[str]) -> None:
        """[Deprecated] 终止追踪的 sessions。请使用 SideEffectCollector.rollback_all()。"""
        if not self.session_manager:
            logger.error(
                "Saga 回滚失败: session_manager 未注入，"
                "无法终止 %d 个 sessions: %s。"
                "请确保在 orchestrator 中注入 session_manager。",
                len(session_ids_ref),
                session_ids_ref,
            )
            raise SagaConfigurationError(
                f"Saga 回滚无法终止 {len(session_ids_ref)} 个 sessions："
                f"session_manager 未注入。"
            )
        for sid in session_ids_ref:
            try:
                self.session_manager.terminate(sid)
                logger.info(f"已终止 session: {sid}")
            except Exception as e:
                logger.error(f"终止 session {sid} 失败: {e}")
        session_ids_ref.clear()


# ============================================================================
# 便捷工厂函数
# ============================================================================

def create_triangulate_saga(
    session_manager: Optional[Any] = None,
    global_timeout: float = 600,
) -> WorkflowSaga:
    """创建 Triangulate 工作流的标准 Saga 实例"""
    return WorkflowSaga(
        session_manager=session_manager,
    ).set_global_timeout(global_timeout)
