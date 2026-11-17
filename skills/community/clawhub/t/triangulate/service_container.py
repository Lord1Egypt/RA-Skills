"""
依赖注入容器 — Triangulate 的模块组装器。

用法:
    orch = (
        ServiceContainer()
        .register_input_adapter(InputAdapter())
        .register_decomposer(TaskDecomposer())
        .register_dispatcher(ExecutionDispatcher())
        .register_consensus_engine(ConsensusEngine())
        .register_renderer(ReportRenderer())
        .with_saga()
        .with_idempotency()
        .with_circuit_breaker()
        .build()
    )
"""
from __future__ import annotations

from typing import Any, Callable, Dict, Optional

from orchestrator import TriangulateOrchestrator
from schemas import WorkflowPhase


class ServiceContainer:
    """Triangulate 服务依赖注入容器 V1.0.0。链式调用，build() 生成 Orchestrator。"""

    def __init__(self):
        # 核心模块
        self._input_adapter: Any = None
        self._decomposer: Any = None
        self._dispatcher: Any = None
        self._consensus_engine: Any = None
        self._renderer: Any = None
        self._session_manager: Any = None

        # 保护机制
        self._enable_saga: bool = False
        self._enable_idempotency: bool = False
        self._enable_circuit_breaker: bool = False

        # 配置
        self._phase_timeouts: Optional[Dict[WorkflowPhase, float]] = None
        self._on_session_created: Optional[Callable[[str, str], None]] = None

    # ------------------------------------------------------------------
    # 核心模块注册
    # ------------------------------------------------------------------

    def register_input_adapter(self, adapter: Any) -> "ServiceContainer":
        """注册输入适配器 (Layer 1)"""
        self._input_adapter = adapter
        return self

    def register_decomposer(self, decomposer: Any) -> "ServiceContainer":
        """注册任务拆解器 (Layer 2)"""
        self._decomposer = decomposer
        return self

    def register_dispatcher(self, dispatcher: Any) -> "ServiceContainer":
        """注册执行调度器 (Layer 3)"""
        self._dispatcher = dispatcher
        return self

    def register_consensus_engine(self, engine: Any) -> "ServiceContainer":
        """注册共识引擎 (Layer 4)"""
        self._consensus_engine = engine
        return self

    def register_renderer(self, renderer: Any) -> "ServiceContainer":
        """注册输出渲染器 (Layer 6)"""
        self._renderer = renderer
        return self

    def register_session_manager(self, manager: Any) -> "ServiceContainer":
        """注册会话管理器（Saga 回滚用）"""
        self._session_manager = manager
        return self

    # ------------------------------------------------------------------
    # 保护机制开关
    # ------------------------------------------------------------------

    def with_saga(self, enabled: bool = True) -> "ServiceContainer":
        """启用/禁用 Saga 事务回滚"""
        self._enable_saga = enabled
        return self

    def with_idempotency(self, enabled: bool = True) -> "ServiceContainer":
        """启用/禁用幂等性缓存"""
        self._enable_idempotency = enabled
        return self

    def with_circuit_breaker(self, enabled: bool = True) -> "ServiceContainer":
        """启用/禁用熔断器"""
        self._enable_circuit_breaker = enabled
        return self

    # ------------------------------------------------------------------
    # 配置
    # ------------------------------------------------------------------

    def set_phase_timeouts(self, timeouts: Dict[WorkflowPhase, float]) -> "ServiceContainer":
        """设置阶段超时配置"""
        self._phase_timeouts = timeouts
        return self

    def set_session_callback(self, callback: Callable[[str, str], None]) -> "ServiceContainer":
        """设置 session 创建回调"""
        self._on_session_created = callback
        return self

    # ------------------------------------------------------------------
    # 构建
    # ------------------------------------------------------------------

    def build(self) -> TriangulateOrchestrator:
        """构建 TriangulateOrchestrator 实例。"""
        return TriangulateOrchestrator(
            input_adapter=self._input_adapter,
            decomposer=self._decomposer,
            dispatcher=self._dispatcher,
            consensus_engine=self._consensus_engine,
            renderer=self._renderer,
            session_manager=self._session_manager,
            phase_timeouts=self._phase_timeouts,
            enable_saga=self._enable_saga,
            enable_idempotency=self._enable_idempotency,
            enable_circuit_breaker=self._enable_circuit_breaker,
            on_session_created=self._on_session_created,
        )
