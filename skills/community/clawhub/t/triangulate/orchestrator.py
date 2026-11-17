"""
顶层编排器 — Triangulate 工作流的总控制器。

使用显式状态机驱动，每个阶段有独立超时。
通过 WorkflowUnitOfWork 执行 7 个工作流步骤，统一事务边界。
异常路径和执行路径均受 PipelineGuard 阶段间契约保护。
通过 ContextBus 单一写入点同步上下文到所有持有者。
"""
from __future__ import annotations

import logging
import threading
import time
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
    WorkflowCheckpoint,
    WorkflowPhase,
)
from state_machine import WorkflowStateMachine, TransitionResult
from saga import WorkflowSaga, SagaConfigurationError
from circuit_breaker import CircuitBreakerEngine, BreakerAction
from idempotency import IdempotencyGuard
from pipeline import PipelineContext
from context_bus import ContextBus
from middleware import (
    MiddlewareChain,
    IdempotencyMiddleware,
    CircuitBreakerMiddleware,
)
from timeout_manager import TimeoutManager
from execution_context import ExecutionContext
from side_effects import SideEffectCollector
from step_executor import StepExecutor
from unit_of_work import WorkflowUnitOfWork
from pipeline_guard import enforce_stage_contract, PipelineContractError
from exceptions import WorkflowFailedError, PipelineConsistencyError

# 阶段函数
from pipeline_steps import (
    run_strategy_phase,
    run_breaker_divergence,
    run_dispatch_phase,
    run_execute_phase,
    run_breaker_failure,
    run_review_phase,
    run_render_phase,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 阶段超时配置
# ============================================================================

DEFAULT_PHASE_TIMEOUTS: Dict[WorkflowPhase, float] = {
    WorkflowPhase.INPUT_VALIDATION: 30,
    WorkflowPhase.STRATEGY: 180,
    WorkflowPhase.DISPATCH: 60,
    WorkflowPhase.EXECUTE: 300,
    WorkflowPhase.REVIEW: 120,
    WorkflowPhase.RENDER: 30,
}

DEFAULT_GLOBAL_TIMEOUT = 600
MAX_STRATEGY_ROUNDS = 3

# 阶段到 Guard 名称的映射
_STAGE_GUARD_MAP = {
    WorkflowPhase.INPUT_VALIDATION: "INPUT_VALIDATION",
    WorkflowPhase.STRATEGY: "STRATEGY",
    WorkflowPhase.DISPATCH: "DISPATCH",
    WorkflowPhase.EXECUTE: "EXECUTE",
    WorkflowPhase.REVIEW: "REVIEW",
    WorkflowPhase.RENDER: "RENDER",
}


# ============================================================================
# 编排器
# ============================================================================

class TriangulateOrchestrator:
    """Triangulate 工作流编排器 V1.0.0

    用法:
        from service_container import ServiceContainer
        orch = (
            ServiceContainer()
            .register_input_adapter(adapter)
            .register_decomposer(decomposer)
            .register_dispatcher(dispatcher)
            .register_consensus_engine(consensus)
            .register_renderer(renderer)
            .with_saga()
            .build()
        )
        result = orch.run(user_input)
    """

    def __init__(
        self,
        input_adapter: Any = None,
        decomposer: Any = None,
        dispatcher: Any = None,
        consensus_engine: Any = None,
        renderer: Any = None,
        session_manager: Any = None,
        phase_timeouts: Optional[Dict[WorkflowPhase, float]] = None,
        enable_saga: bool = True,
        enable_idempotency: bool = True,
        enable_circuit_breaker: bool = True,
        on_session_created: Optional[Callable[[str, str], None]] = None,
    ):
        """初始化编排器。"""
        # 核心模块引用
        self.input_adapter = input_adapter
        self.decomposer = decomposer
        self.dispatcher = dispatcher
        self.consensus_engine = consensus_engine
        self.renderer = renderer
        self.session_manager = session_manager
        self._on_session_created = on_session_created
        self._enable_saga = enable_saga

        # 基础设施
        self.state_machine = WorkflowStateMachine()
        self._timeout_manager = TimeoutManager(
            global_timeout=DEFAULT_GLOBAL_TIMEOUT,
            phase_timeouts=phase_timeouts or dict(DEFAULT_PHASE_TIMEOUTS),
        )
        # Saga 实例保留用于外部集成和向后兼容（如 tests/saga_tests.py）
        # 主工作流已由 WorkflowUnitOfWork 驱动，不再通过 Saga 闭包注册步骤
        self._saga = (
            WorkflowSaga(session_manager=session_manager).set_global_timeout(DEFAULT_GLOBAL_TIMEOUT)
            if enable_saga else None
        )
        self._idempotency = IdempotencyGuard(ttl_seconds=1800) if enable_idempotency else None
        self._breaker = CircuitBreakerEngine() if enable_circuit_breaker else None

        # PipelineContext + ContextBus（单一写入点 + 变更广播）
        initial_ctx: PipelineContext = PipelineContext.create(
            checkpoint=self.state_machine.checkpoint,
        )
        self._bus = ContextBus(initial_ctx)
        self._ctx: PipelineContext = initial_ctx
        self.state_machine.set_pipeline_context(self._ctx)

        # 注册 ContextBus 变更回调：所有消费者通过回调同步，而非手动赋值
        self._bus.on_changed(lambda ctx: setattr(self, '_ctx', ctx))
        self._bus.on_changed(lambda ctx: self.state_machine.set_pipeline_context(ctx))
        # StepExecutor 在 run() 中创建，此处预注册回调（若未创建则忽略）
        self._bus.on_changed(
            lambda ctx: self._step_executor.sync_context(ctx) if self._step_executor else None
        )

        # 副作用收集器
        self._side_effects = SideEffectCollector()

        # StepExecutor（ExecutionContext 访问 + ContextBus 回调兼容）
        self._step_executor: Optional[StepExecutor] = None

        # 中间件责任链
        self._middleware_chain = MiddlewareChain()
        if self._idempotency:
            self._middleware_chain.add(IdempotencyMiddleware(self._idempotency))
        if self._breaker:
            self._middleware_chain.add(CircuitBreakerMiddleware(self._breaker, DEFAULT_GLOBAL_TIMEOUT))

    # ==================================================================
    # 上下文同步回调（ContextBus 单一写入点）
    # ==================================================================

    def _sync_ctx(self, new_ctx: PipelineContext) -> None:
        """原子同步：通过 ContextBus 单一写入点驱动所有消费者。

        ContextBus.write() 内部会触发所有注册的 on_changed 回调，
        包括 self._ctx、state_machine、step_executor 的同步。
        不再手动逐个赋值，消除四重写入的非原子问题。
        """
        self._bus.write(new_ctx)

    # ==================================================================
    # 主入口
    # ==================================================================

    def run(self, user_input: Any) -> FinalReport:
        """执行完整 Triangulate 工作流。"""
        self._timeout_manager.start()
        self._ctx = PipelineContext.create(
            checkpoint=self.state_machine.checkpoint,
            workflow_start_time=time.time(),
        )
        self.state_machine.set_pipeline_context(self._ctx)
        self._bus.write(self._ctx)  # 同步初始状态到 ContextBus
        self._side_effects.clear()

        # 创建 ExecutionContext（UoW 通过它访问 PipelineContext）
        self._step_executor = StepExecutor(
            exec_ctx=ExecutionContext(self._ctx),
            on_ctx_sync=self._sync_ctx,
            state_machine=self.state_machine,
            side_effects=self._side_effects,
            saga=None,  # UoW 已接管事务回滚，不再通过 Saga 闭包注册
        )

        failed = False
        try:
            # ---- Phase: INPUT_VALIDATION ----
            validated_input = self._run_phase(
                WorkflowPhase.INPUT_VALIDATION,
                lambda: self._validate_input(user_input),
            )
            self._ctx = self._ctx.evolve(validated_input=validated_input)
            enforce_stage_contract("INPUT_VALIDATION", self._ctx)

            # ---- [中间件: before_all] ----
            self._ctx = self._middleware_chain.before_all(self._ctx)
            self._ctx.assert_consistency()

            # 检查中间件是否要求跳过执行
            idempotency_mw = self._middleware_chain.get(IdempotencyMiddleware)
            if idempotency_mw and idempotency_mw.should_skip_execution:
                logger.info("幂等性缓存命中，直接返回缓存结果")
                self.state_machine.force_transition(WorkflowPhase.DONE)
                return idempotency_mw.cached_result

            breaker_mw = self._middleware_chain.get(CircuitBreakerMiddleware)
            if breaker_mw and breaker_mw.is_stopped:
                raise WorkflowFailedError(
                    f"熔断中间件阻止执行: {breaker_mw.stop_reason}"
                )

            # ---- [统一编排路径] ----
            final_report = self._run_workflow()

            # ---- [中间件: after_all] ----
            self._middleware_chain.after_all(self._ctx, final_report)

            # ---- Phase: DONE ----
            self.state_machine.transition(WorkflowPhase.DONE)
            self._ctx = self._ctx.evolve(final_report=final_report)
            return final_report

        except WorkflowFailedError:
            failed = True
            raise
        except Exception as e:
            failed = True
            logger.exception(f"未预期的异常: {e}")
            raise WorkflowFailedError(
                f"工作流异常终止: {e}",
                checkpoint=self.state_machine.checkpoint,
            ) from e
        finally:
            if failed:
                self._handle_failure()

    # ==================================================================
    # 统一编排执行（WorkflowUnitOfWork 事务边界）
    # ==================================================================

    def _run_workflow(self) -> FinalReport:
        """执行 7 个标准工作流步骤，使用 WorkflowUnitOfWork 统一事务边界。

        补偿操作在执行时创建（而非注册时），消除闭包捕获过期引用问题。
        任一步骤失败 → 逆序回滚所有已执行步骤的副作用。
        """
        exec_ctx = self._step_executor.get_exec_ctx()
        exec_ctx.update(self._ctx)

        uow = WorkflowUnitOfWork(
            exec_ctx=exec_ctx,
            on_ctx_sync=self._sync_ctx,
            state_machine=self.state_machine,
            side_effects=self._side_effects,
            session_manager=self.session_manager,
        )

        # ---- 步骤 1: 策略阶段 ----
        uow.add_step(
            step_name="strategy",
            action_fn=lambda ec: self._run_phase(
                WorkflowPhase.STRATEGY,
                lambda: run_strategy_phase(
                    ec.get(), self.consensus_engine, self._generate_default_decisions
                ),
            ),
            has_side_effects=True,
            guard_stage="STRATEGY",
        )

        # ---- 步骤 2: 熔断检查-共识分歧 ----
        uow.add_step(
            step_name="breaker_divergence",
            action_fn=lambda ec: run_breaker_divergence(ec.get(), self._breaker),
            has_side_effects=False,
        )

        # ---- 步骤 3: 任务拆解 ----
        uow.add_step(
            step_name="dispatch",
            action_fn=lambda ec: self._run_phase(
                WorkflowPhase.DISPATCH,
                lambda: run_dispatch_phase(ec.get(), self.decomposer),
            ),
            has_side_effects=False,
            guard_stage="DISPATCH",
        )

        # ---- 步骤 4: 执行层 ----
        uow.add_step(
            step_name="execute",
            action_fn=lambda ec: self._run_phase(
                WorkflowPhase.EXECUTE,
                lambda: run_execute_phase(ec.get(), self.dispatcher),
            ),
            has_side_effects=True,
            guard_stage="EXECUTE",
        )

        # ---- 步骤 5: 熔断检查-执行失败率 ----
        uow.add_step(
            step_name="breaker_failure",
            action_fn=lambda ec: run_breaker_failure(
                ec.get(), self._breaker, self.decomposer,
                run_execute_phase_fn=lambda c: run_execute_phase(c, self.dispatcher),
            ),
            has_side_effects=False,
        )

        # ---- 步骤 6: 审阅 ----
        uow.add_step(
            step_name="review",
            action_fn=lambda ec: self._run_phase(
                WorkflowPhase.REVIEW,
                lambda: run_review_phase(
                    ec.get(), self.consensus_engine, self._generate_default_decisions
                ),
            ),
            has_side_effects=False,
            guard_stage="REVIEW",
        )

        # ---- 步骤 7: 渲染 ----
        uow.add_step(
            step_name="render",
            action_fn=lambda ec: self._run_phase(
                WorkflowPhase.RENDER,
                lambda: run_render_phase(ec.get(), self.renderer),
            ),
            has_side_effects=False,
            guard_stage="RENDER",
        )

        # ---- 执行：WorkflowUnitOfWork 统一处理 Saga/无 Saga 路径 ----
        uow.execute()

        # 获取结果
        ctx = exec_ctx.get()
        if ctx.final_report is None:
            raise WorkflowFailedError("工作流完成但未产生最终报告")
        return ctx.final_report

    # ==================================================================
    # 失败处理
    # ==================================================================

    def _handle_failure(self):
        """统一失败处理：保存检查点 + 记录未清理的副作用。

        WorkflowUnitOfWork 已在 _run_workflow() 中执行了回滚，
        此处仅处理 UoW 未覆盖的极端情况（如 run() 在 UoW 创建前失败）。
        """
        try:
            self.state_machine.force_transition(WorkflowPhase.FAILED)
        except Exception:
            pass

        # 1. 先保存检查点 — 记录失败时的完整状态
        try:
            self.state_machine.save_checkpoint()
        except Exception as e:
            logger.error(f"保存检查点失败: {e}")

        # 2. 仅清理 UoW 未覆盖的残留 sessions
        all_sids = self._side_effects.get_all_sessions()
        if all_sids:
            if self.session_manager:
                summary = self._side_effects.rollback_all(self.session_manager)
                if summary["terminated_count"]:
                    logger.warning(
                        f"_handle_failure 清理残留: 回滚 {summary['terminated_count']} 个 sessions"
                    )
                if summary["failed_count"]:
                    logger.error(
                        f"_handle_failure: {summary['failed_count']} 个 session 终止失败"
                    )
            else:
                logger.warning(
                    f"无 session_manager，无法清理 {len(all_sids)} 个残留 sessions: {all_sids}"
                )

        logger.info("工作流失败，检查点已保存。")

    # ==================================================================
    # 各阶段实现
    # ==================================================================

    def _validate_input(self, user_input: Any) -> UserInput:
        """阶段：输入校验"""
        if self.input_adapter:
            return self.input_adapter.validate(user_input)

        if isinstance(user_input, UserInput):
            return user_input
        if isinstance(user_input, str):
            return UserInput(task_description=user_input)
        if isinstance(user_input, dict):
            # 字段白名单：只接受 UserInput 的已知字段，拒绝未知字段
            allowed_fields = set(UserInput.model_fields.keys())
            filtered = {k: v for k, v in user_input.items() if k in allowed_fields}
            dropped = set(user_input.keys()) - allowed_fields
            if dropped:
                logger.warning(f"输入 dict 中包含未知字段，已被丢弃: {sorted(dropped)}")
            return UserInput(**filtered)
        raise ValueError(f"不支持的输入类型: {type(user_input)}")

    def _generate_default_decisions(self, validated_input: UserInput) -> List[DecisionResult]:
        """生成默认决策（mock/测试环境兜底）"""
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

    # ==================================================================
    # 保护机制
    # ==================================================================

    def _run_phase(self, phase: WorkflowPhase, fn: Callable) -> Any:
        """带超时和状态机转换的阶段执行包装器。

        使用 threading.Event 实现真正超时中断：
        - 超时后通过 Event 信号通知后台线程停止
        - 不依赖 ThreadPoolExecutor.__exit__() 等待线程
        """
        # 同步最新 ctx 到状态机
        self.state_machine.set_pipeline_context(self._ctx)

        # 全局超时检查
        if self._timeout_manager.is_global_timeout():
            raise WorkflowFailedError(
                "全局超时，工作流终止",
                checkpoint=self.state_machine.checkpoint,
            )

        result = self.state_machine.transition(phase)
        if not result.success:
            raise WorkflowFailedError(
                f"状态转换失败: {result.reason}",
                checkpoint=self.state_machine.checkpoint,
            )

        self._timeout_manager.start_phase(phase)
        self._ctx = self._ctx.record_phase_start(phase)

        phase_timeout = self._timeout_manager.phase_timeouts.get(phase, 60)

        # 使用 Event 实现真正的超时中断
        done_event = threading.Event()
        result_holder: Dict[str, Any] = {"output": None, "error": None}

        def _wrapped_fn():
            try:
                result_holder["output"] = fn()
            except Exception as e:
                result_holder["error"] = e
            finally:
                done_event.set()

        thread = threading.Thread(target=_wrapped_fn, daemon=True)
        thread.start()

        try:
            # 等待线程完成或超时
            finished = done_event.wait(timeout=phase_timeout)
            if not finished:
                # 真正超时：线程可能仍在运行但不再等待
                self._timeout_manager.end_phase(phase)
                elapsed = self._timeout_manager.get_phase_elapsed(phase)
                logger.error(
                    f"阶段 {phase.value} 超时中断！"
                    f"(限制: {phase_timeout}s, 实际耗时: {elapsed:.1f}s)"
                )
                raise WorkflowFailedError(
                    f"阶段 {phase.value} 超时 ({phase_timeout}s)",
                    checkpoint=self.state_machine.checkpoint,
                )

            # 检查是否有异常
            if result_holder["error"] is not None:
                raise result_holder["error"]

            output = result_holder["output"]

            self._timeout_manager.end_phase(phase)
            elapsed = self._timeout_manager.get_phase_elapsed(phase)
            logger.info(f"阶段 {phase.value} 完成 (耗时: {elapsed:.1f}s)")

            if self._timeout_manager.is_phase_timeout(phase):
                logger.warning(
                    f"阶段 {phase.value} 实际耗时超过预设超时 ({phase_timeout}s)"
                )

            return output
        except WorkflowFailedError:
            self._timeout_manager.end_phase(phase)
            guard_name = _STAGE_GUARD_MAP.get(phase)
            if guard_name:
                try:
                    enforce_stage_contract(guard_name, self._ctx)
                except PipelineContractError as ce:
                    logger.error(f"阶段 {phase.value} 失败且输出契约违反: {ce}")
            raise
        except Exception as e:
            self._timeout_manager.end_phase(phase)
            elapsed = self._timeout_manager.get_phase_elapsed(phase)
            logger.error(f"阶段 {phase.value} 失败 (耗时: {elapsed:.1f}s): {e}")
            guard_name = _STAGE_GUARD_MAP.get(phase)
            if guard_name:
                try:
                    enforce_stage_contract(guard_name, self._ctx)
                except PipelineContractError as ce:
                    logger.error(f"阶段 {phase.value} 失败且输出契约违反: {ce}")
            raise

    # ==================================================================
    # 检查点管理
    # ==================================================================

    def save_checkpoint(self) -> str:
        self.state_machine.set_pipeline_context(self._ctx)
        return self.state_machine.save_checkpoint()

    def resume_from_checkpoint(self, name: str) -> bool:
        """从检查点恢复。

        load_checkpoint() 会将状态机置于冻结模式，
        恢复后重新绑定 PipelineContext 以恢复实时投影模式。
        """
        ok = self.state_machine.load_checkpoint(name)
        if ok:
            cp = self.state_machine.checkpoint

            if cp.created_sessions and self.session_manager:
                valid_sessions = []
                for sid in cp.created_sessions:
                    try:
                        if self.session_manager.is_alive(sid):
                            valid_sessions.append(sid)
                        else:
                            logger.warning(
                                f"检查点中的 session {sid} 已失效，从恢复列表中移除"
                            )
                    except Exception:
                        valid_sessions.append(sid)
                cp.created_sessions = valid_sessions

            # 重新绑定 PipelineContext，解冻检查点，同步到 ContextBus
            self._ctx = self._ctx.evolve(degraded=cp.degraded)
            self.state_machine.set_pipeline_context(self._ctx)
            self._bus.write(self._ctx)
        return ok

    def reset(self):
        """重置编排器状态"""
        self.state_machine = WorkflowStateMachine()
        self._timeout_manager.start()
        self._ctx = PipelineContext.create(
            checkpoint=self.state_machine.checkpoint,
        )
        self.state_machine.set_pipeline_context(self._ctx)
        self._bus = ContextBus(self._ctx)  # 重建 ContextBus
        # 重新注册 ContextBus 变更回调
        self._bus.on_changed(lambda ctx: setattr(self, '_ctx', ctx))
        self._bus.on_changed(lambda ctx: self.state_machine.set_pipeline_context(ctx))
        self._bus.on_changed(
            lambda ctx: self._step_executor.sync_context(ctx) if self._step_executor else None
        )
        self._side_effects.clear()
        if self._step_executor:
            self._step_executor.reset()
        if self._breaker:
            self._breaker.reset()
        if self._saga:
            self._saga.reset_steps()

    def get_progress(self) -> Dict[str, Any]:
        progress = self.state_machine.get_state_summary()
        progress["degraded"] = self._ctx.degraded
        if self._breaker:
            progress["breaker"] = self._breaker.get_report()
        if self._idempotency:
            progress["idempotency"] = self._idempotency.get_stats()
        progress["timeout"] = self._timeout_manager.get_report()
        progress["side_effects"] = {
            "tracked_steps": self._side_effects.tracked_step_count,
            "total_sessions": self._side_effects.total_session_count,
        }
        return progress

    # ==================================================================
    # Saga / Sessions 暴露接口（保持向后兼容）
    # ==================================================================

    def register_session(self, session_id: str):
        """注册一个由 sessions_spawn 创建的会话 ID（外部调度时调用）"""
        self._ctx = self._ctx.add_execution_session(session_id)
        self.state_machine.set_pipeline_context(self._ctx)

    def register_strategy_session(self, session_id: str):
        """注册策略阶段创建的 session"""
        self._ctx = self._ctx.add_strategy_session(session_id)
        self.state_machine.set_pipeline_context(self._ctx)

    def _auto_register_session(self, session_id: str, phase: str = "execution"):
        """自动注册 session ID（内部使用）"""
        if self._on_session_created:
            self._on_session_created(session_id, phase)
        if phase == "strategy":
            self.register_strategy_session(session_id)
        else:
            self.register_session(session_id)

    def get_saga(self) -> Optional[WorkflowSaga]:
        return self._saga

    def signal_user_interrupt(self):
        if self._breaker:
            self._breaker.signal_user_interrupt()
