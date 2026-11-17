"""
中间件责任链 — Triangulate 工作流的横切关注点。

每个中间件有 before() / after() 钩子，按责任链顺序执行。
"""
from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional

from schemas import FinalReport, UserInput, WorkflowPhase
from circuit_breaker import CircuitBreakerEngine, BreakerAction
from idempotency import IdempotencyGuard
from pipeline import PipelineContext

logger = logging.getLogger(__name__)


# ============================================================================
# 中间件抽象
# ============================================================================

class Middleware(ABC):
    """中间件基类 — before/after 钩子"""

    @abstractmethod
    def before(self, ctx: PipelineContext) -> PipelineContext:
        """工作流执行前"""
        ...

    @abstractmethod
    def after(self, ctx: PipelineContext, result: Optional[FinalReport]) -> None:
        """工作流执行后"""
        ...


# ============================================================================
# 幂等性中间件
# ============================================================================

class IdempotencyMiddleware(Middleware):
    """幂等性中间件：前置缓存检查 + 后置缓存写入"""

    def __init__(self, guard: IdempotencyGuard):
        self.guard = guard
        self._input_hash: Optional[str] = None
        self._cache_hit: bool = False
        self._cached_result: Optional[FinalReport] = None

    def before(self, ctx: PipelineContext) -> PipelineContext:
        """检查幂等性缓存。"""
        if ctx.validated_input is None:
            return ctx
        cached_result, is_hit = self.guard.check_cache(ctx.validated_input)
        if is_hit:
            logger.info("幂等性缓存命中，将跳过执行")
            self._cache_hit = True
            self._cached_result = cached_result
        return ctx

    def after(self, ctx: PipelineContext, result: Optional[FinalReport]) -> None:
        """写入幂等性缓存。"""
        if result and not self._cache_hit and ctx.validated_input:
            self.guard.cache_result(ctx.validated_input, result)

    @property
    def should_skip_execution(self) -> bool:
        """是否应跳过实际执行（缓存命中）"""
        return self._cache_hit

    @property
    def cached_result(self) -> Optional[FinalReport]:
        return self._cached_result


# ============================================================================
# 熔断中间件
# ============================================================================

class CircuitBreakerMiddleware(Middleware):
    """熔断中间件：前置超时/中断检查 + 后置阶段间熔断检查"""

    def __init__(self, breaker: CircuitBreakerEngine, global_timeout: float = 600):
        self.breaker = breaker
        self.global_timeout = global_timeout
        self._stopped: bool = False
        self._stop_reason: str = ""
        # 后置检查结果
        self._post_divergence_triggered: bool = False
        self._post_failure_triggered: bool = False
        self._post_action: Optional[BreakerAction] = None

    def before(self, ctx: PipelineContext) -> PipelineContext:
        """前置检查：全局超时 + 用户中断"""
        elapsed = ctx.elapsed_seconds
        if self.breaker.check_global_timeout(elapsed, self.global_timeout) == BreakerAction.STOP:
            self._stopped = True
            self._stop_reason = "全局超时"
            logger.warning("熔断中间件：全局超时")
        if self.breaker.check_user_interrupt() == BreakerAction.STOP:
            self._stopped = True
            self._stop_reason = "用户中断"
            logger.warning("熔断中间件：用户中断")
        return ctx

    def after(self, ctx: PipelineContext, result: Optional[FinalReport]) -> None:
        """后置检查：共识分歧 + 执行失败率 + Token 预算"""
        # 检查共识分歧
        if ctx.divergence_rounds > 0:
            action = self.breaker.check_consensus_divergence(ctx.divergence_rounds)
            if action == BreakerAction.FALLBACK_TO_USER:
                self._post_divergence_triggered = True
                self._post_action = action
                logger.warning(
                    f"熔断中间件(after): 共识分歧 {ctx.divergence_rounds} 轮 → FALLBACK_TO_USER"
                )

        # 检查执行失败率
        if ctx.exec_report is not None and ctx.exec_report.total_tasks > 0:
            action = self.breaker.check_task_failure_rate(ctx.exec_report)
            if action == BreakerAction.REDISTRIBUTE:
                self._post_failure_triggered = True
                self._post_action = action
                logger.warning(
                    f"熔断中间件(after): 失败率 {ctx.exec_report.failure_rate:.1%} → REDISTRIBUTE"
                )

    @property
    def is_stopped(self) -> bool:
        return self._stopped

    @property
    def stop_reason(self) -> str:
        return self._stop_reason

    @property
    def post_action(self) -> Optional[BreakerAction]:
        """后置检查触发的熔断动作"""
        return self._post_action

    @property
    def triggered_divergence(self) -> bool:
        """是否触发了共识分歧熔断"""
        return self._post_divergence_triggered

    @property
    def triggered_failure_rate(self) -> bool:
        """是否触发了执行失败率熔断"""
        return self._post_failure_triggered


# ============================================================================
# 中间件责任链
# ============================================================================

class MiddlewareChain:
    """中间件责任链 — 按顺序执行 before/after 钩子"""

    def __init__(self, middlewares: Optional[List[Middleware]] = None):
        self._middlewares: List[Middleware] = middlewares or []

    def add(self, middleware: Middleware) -> "MiddlewareChain":
        self._middlewares.append(middleware)
        return self

    def before_all(self, ctx: PipelineContext) -> PipelineContext:
        """执行所有中间件的 before 钩子"""
        for mw in self._middlewares:
            ctx = mw.before(ctx)
        return ctx

    def after_all(self, ctx: PipelineContext, result: Optional[FinalReport]) -> None:
        """执行所有中间件的 after 钩子"""
        for mw in reversed(self._middlewares):  # 逆序（类似回滚）
            mw.after(ctx, result)

    def get(self, middleware_class: type) -> Optional[Middleware]:
        """按类型查找中间件"""
        for mw in self._middlewares:
            if isinstance(mw, middleware_class):
                return mw
        return None

    @property
    def middlewares(self) -> List[Middleware]:
        return list(self._middlewares)
