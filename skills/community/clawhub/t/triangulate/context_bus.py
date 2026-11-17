"""
上下文总线 (Context Bus) — Triangulate 工作流的唯一状态写入点。

设计原则：
- 单一写入者：orchestrator.run() 主循环是唯一写入者
- 只读访问者：StepExecutor, StateMachine, Middleware, Saga 通过 get_snapshot() 获取只读快照
- 变更通知：on_context_changed 回调（推送而非拉取）
- 深拷贝快照：get_snapshot() 返回 deepcopy，杜绝共享引用

用法:
    bus = ContextBus()
    bus.write(ctx)                    # 唯一写入点
    snapshot = bus.get_snapshot()     # 只读深拷贝快照
    bus.on_changed(lambda ctx: ...)   # 注册变更回调
"""
from __future__ import annotations

import copy
import logging
import threading
from typing import Any, Callable, Dict, List, Optional

from pipeline import PipelineContext

logger = logging.getLogger(__name__)


class ContextBus:
    """上下文总线 — 唯一状态写入点 + 变更广播。

    解决 orchestrator._ctx / StepExecutor._exec_ctx / StateMachine._pipeline_ctx
    三个通道同时写入的不一致问题。
    """

    def __init__(self, initial_ctx: Optional[PipelineContext] = None):
        self._ctx: Optional[PipelineContext] = initial_ctx
        self._lock = threading.RLock()
        self._listeners: List[Callable[[PipelineContext], None]] = []
        self._version: int = 0
        self._history: List[Dict[str, Any]] = []  # 变更历史（最近 20 条）

    # ------------------------------------------------------------------
    # 写入（唯一入口）
    # ------------------------------------------------------------------

    def write(self, new_ctx: PipelineContext) -> PipelineContext:
        """唯一写入点 — 原子更新上下文并广播变更。

        所有对 PipelineContext 的更新必须通过此方法，
        确保变更通知被推送给所有监听者。

        Args:
            new_ctx: 新的 PipelineContext 实例

        Returns:
            PipelineContext: 写入后的上下文（与输入相同，方便链式调用）
        """
        with self._lock:
            old_ctx = self._ctx
            self._ctx = new_ctx
            self._version += 1

            # 记录变更历史（最近 20 条）
            changed_fields = self._diff(old_ctx, new_ctx)
            self._history.append({
                "version": self._version,
                "changed_fields": changed_fields,
            })
            if len(self._history) > 20:
                self._history = self._history[-20:]

        # 广播变更（在锁外执行，避免回调死锁）
        for listener in self._listeners:
            try:
                listener(new_ctx)
            except Exception as e:
                logger.error(f"ContextBus 变更通知回调失败: {e}")

        return new_ctx

    # ------------------------------------------------------------------
    # 读取（只读深拷贝快照）
    # ------------------------------------------------------------------

    def get_snapshot(self) -> PipelineContext:
        """获取当前上下文的深拷贝快照。

        返回 deepcopy，调用方可以安全修改而不影响总线中的版本。
        """
        with self._lock:
            if self._ctx is None:
                raise RuntimeError("ContextBus 未初始化：没有可用的上下文")
            return copy.deepcopy(self._ctx)

    def get(self) -> PipelineContext:
        """获取当前上下文引用（只读，禁止修改）。

        与 get_snapshot() 不同，返回的是直接引用。调用方不应修改返回值。
        仅用于需要性能且能保证不修改的场景。
        """
        with self._lock:
            if self._ctx is None:
                raise RuntimeError("ContextBus 未初始化：没有可用的上下文")
            return self._ctx

    # ------------------------------------------------------------------
    # 变更通知
    # ------------------------------------------------------------------

    def on_changed(self, listener: Callable[[PipelineContext], None]) -> Callable[[], None]:
        """注册变更回调。返回取消注册的函数。

        Args:
            listener: 接收新 PipelineContext 的回调

        Returns:
            Callable: 调用以取消注册
        """
        self._listeners.append(listener)
        return lambda: self._listeners.remove(listener) if listener in self._listeners else None

    # ------------------------------------------------------------------
    # 版本
    # ------------------------------------------------------------------

    @property
    def version(self) -> int:
        with self._lock:
            return self._version

    def get_history(self) -> List[Dict[str, Any]]:
        """获取变更历史（最近 20 条）"""
        with self._lock:
            return list(self._history)

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------

    def _diff(self, old_ctx: Optional[PipelineContext], new_ctx: PipelineContext) -> List[str]:
        """对比新旧上下文，返回变更的字段列表。"""
        if old_ctx is None:
            return ["__initial__"]

        changed = []
        # 对比关键字段
        checks = [
            ("validated_input", lambda c: c.validated_input is not None),
            ("strategy_rounds", lambda c: len(c.strategy_rounds)),
            ("task_dag", lambda c: c.task_dag is not None),
            ("exec_report", lambda c: c.exec_report is not None),
            ("review_results", lambda c: len(c.review_results)),
            ("final_report", lambda c: c.final_report is not None),
            ("divergence_rounds", lambda c: c.divergence_rounds),
            ("degraded", lambda c: c.degraded),
        ]

        for field_name, getter in checks:
            old_val = getter(old_ctx)
            new_val = getter(new_ctx)
            if old_val != new_val:
                changed.append(field_name)

        # 检查 session 变化
        if old_ctx.created_sessions != new_ctx.created_sessions:
            changed.append("created_sessions")

        return changed

    def reset(self) -> None:
        """重置总线（用于 orchestrator.reset()）"""
        with self._lock:
            self._ctx = None
            self._version = 0
            self._history.clear()
