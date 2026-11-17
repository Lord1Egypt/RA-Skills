"""
线程安全的执行上下文 — PipelineContext 的线程安全包装器。

使用 threading.RLock 保护读写，提供 update/get/apply 接口。
"""
from __future__ import annotations

import threading
from typing import Optional

from pipeline import PipelineContext


class ExecutionContext:
    """线程安全的执行上下文包装器。

    替代 orchestrator._run_workflow() 中的 nonlocal ctx_ref 模式，
    确保在 Saga 步骤/非 Saga 步骤/异常路径下对 PipelineContext 的读写都是原子的。
    """

    def __init__(self, initial_ctx: PipelineContext):
        self._ctx: PipelineContext = initial_ctx
        self._lock = threading.RLock()

    def update(self, new_ctx: PipelineContext) -> PipelineContext:
        """线程安全地更新上下文，返回新值"""
        with self._lock:
            self._ctx = new_ctx
            return self._ctx

    def get(self) -> PipelineContext:
        """线程安全地获取当前上下文"""
        with self._lock:
            return self._ctx

    def apply(self, new_ctx: Optional[PipelineContext] = None) -> PipelineContext:
        """更新上下文（如果提供）并返回当前值。

        便捷方法：一步完成 update + get。
        """
        if new_ctx is not None:
            return self.update(new_ctx)
        return self.get()

    @property
    def ctx(self) -> PipelineContext:
        """只读访问（加锁，与 update/get 保持一致的线程安全语义）"""
        with self._lock:
            return self._ctx
