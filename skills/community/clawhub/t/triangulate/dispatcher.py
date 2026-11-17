"""
Layer 3: 执行调度器 (Execution Dispatcher)

职责：
- 接收 TaskDAG，按拓扑顺序并发执行子任务
- 全局超时熔断 + 退避重试策略（指数退避 + 抖动）
- 部分失败隔离（单个子任务失败不影响其他）
- 输出 ExecutionReport
"""
from __future__ import annotations

import logging
import random
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeoutError
from typing import Any, Callable, Dict, List, Optional, Tuple

from schemas import (
    ExecutionReport,
    ExecutionResult,
    ExecutionStatus,
    SubTask,
    TaskDAG,
)

logger = logging.getLogger(__name__)


# ============================================================================
# 重试配置
# ============================================================================

# 默认只重试 IO/网络/超时类异常，编程错误不应重试
RETRYABLE_EXCEPTIONS = (
    TimeoutError,
    FutureTimeoutError,  # concurrent.futures.TimeoutError
    ConnectionError,
    ConnectionRefusedError,
    ConnectionResetError,
    OSError,             # 文件被占用、网络不可达等
    BrokenPipeError,
)


class RetryConfig:
    """退避重试配置。支持自定义重试判定回调 custom_retryable_check。"""

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        backoff_factor: float = 2.0,
        jitter: bool = True,
        retryable_exceptions: Tuple = RETRYABLE_EXCEPTIONS,
        custom_retryable_check: Optional[Callable[[Exception], bool]] = None,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.backoff_factor = backoff_factor
        self.jitter = jitter
        self.retryable_exceptions = retryable_exceptions
        self.custom_retryable_check = custom_retryable_check

    def get_delay(self, attempt: int) -> float:
        """计算第 attempt 次重试的延迟（秒）"""
        delay = min(
            self.base_delay * (self.backoff_factor ** attempt),
            self.max_delay,
        )
        if self.jitter:
            delay = delay * (0.5 + random.random())  # 50%-150% 抖动
        return delay

    def is_retryable(self, exception: Exception) -> bool:
        """判断异常是否可重试（先检查元组，再检查自定义回调）。"""
        if isinstance(exception, self.retryable_exceptions):
            return True
        if self.custom_retryable_check is not None:
            try:
                return self.custom_retryable_check(exception)
            except Exception:
                return False
        return False


# ============================================================================
# 调度器
# ============================================================================

class ExecutionDispatcher:
    """执行调度器 — 并发执行子任务 + 超时 + 重试"""

    def __init__(
        self,
        executor_factory: Optional[Callable[[SubTask], Any]] = None,
        retry_config: Optional[RetryConfig] = None,
        global_timeout: float = 300,
        max_workers: int = 5,
    ):
        """
        Args:
            executor_factory: 子任务执行器工厂（默认用内置 mock）
            retry_config: 重试策略
            global_timeout: 全局超时（秒）
            max_workers: 最大并发数
        """
        self.executor_factory = executor_factory or self._default_executor
        self.retry_config = retry_config or RetryConfig()
        self.global_timeout = global_timeout
        self.max_workers = max_workers

    def dispatch(self, dag: TaskDAG) -> ExecutionReport:
        """
        调度执行 TaskDAG 中的所有子任务。

        策略：
        1. 按拓扑排序确定执行顺序（无依赖→全并行）
        2. 每个子任务独立超时
        3. 失败子任务自动重试
        4. 全局超时熔断

        Returns:
            ExecutionReport: 执行汇总报告
        """
        if not dag.subtasks:
            return ExecutionReport(
                total_tasks=0, completed=0, failed=0,
                timed_out=0, cancelled=0, results=[],
            )

        start_time = time.time()
        results: List[ExecutionResult] = []

        # 拓扑排序
        sorted_ids = dag._topological_sort()

        # 按层级分组（同一层级可并行）
        levels = self._group_by_level(dag, sorted_ids)
        logger.info(f"TaskDAG 共 {len(levels)} 个执行层级，{len(dag.subtasks)} 个子任务")

        for level_idx, level_ids in enumerate(levels):
            # 检查全局超时
            if time.time() - start_time > self.global_timeout:
                logger.warning(f"全局超时 ({self.global_timeout}s)，取消剩余 {len(dag.subtasks) - len(results)} 个子任务")
                remaining = [
                    t for t in dag.subtasks
                    if t.id not in {r.subtask_id for r in results}
                ]
                for t in remaining:
                    results.append(ExecutionResult(
                        subtask_id=t.id,
                        status=ExecutionStatus.CANCELLED,
                        error="全局超时，任务被取消",
                    ))
                break

            # 并行执行当前层级
            level_subtasks = [
                t for t in dag.subtasks if t.id in level_ids
            ]
            level_start = time.time()

            with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
                futures = {
                    pool.submit(self._execute_with_retry, t): t
                    for t in level_subtasks
                }

                for future in futures:
                    subtask = futures[future]
                    remaining_timeout = self.global_timeout - (time.time() - start_time)

                    if remaining_timeout <= 0:
                        results.append(ExecutionResult(
                            subtask_id=subtask.id,
                            status=ExecutionStatus.CANCELLED,
                            error="全局超时",
                        ))
                        continue

                    try:
                        result = future.result(timeout=min(
                            remaining_timeout,
                            subtask.timeout_seconds + 10,  # 额外 10s 缓冲
                        ))
                        results.append(result)
                    except FutureTimeoutError:
                        results.append(ExecutionResult(
                            subtask_id=subtask.id,
                            status=ExecutionStatus.TIMEOUT,
                            error=f"子任务超时 ({subtask.timeout_seconds}s)",
                            duration_seconds=time.time() - level_start,
                        ))

            logger.info(
                f"层级 {level_idx+1}/{len(levels)} 完成 "
                f"(耗时: {time.time() - level_start:.1f}s)"
            )

        # 汇总
        total_duration = time.time() - start_time
        return self._build_report(results, total_duration)

    # ------------------------------------------------------------------
    # 内部方法
    # ------------------------------------------------------------------

    def _execute_with_retry(self, subtask: SubTask) -> ExecutionResult:
        """带退避重试的执行。"""
        last_error: Optional[str] = None
        total_retries = 0

        for attempt in range(self.retry_config.max_retries + 1):
            start = time.time()
            try:
                output = self.executor_factory(subtask)
                duration = time.time() - start
                return ExecutionResult(
                    subtask_id=subtask.id,
                    status=ExecutionStatus.SUCCESS,
                    output=str(output) if output else None,
                    duration_seconds=duration,
                    retry_count=attempt,
                )
            except Exception as e:
                if self.retry_config.is_retryable(e):
                    # 可重试异常（IO/网络/超时/用户自定义）
                    last_error = str(e)
                    total_retries = attempt

                    if attempt < self.retry_config.max_retries:
                        delay = self.retry_config.get_delay(attempt)
                        logger.warning(
                            f"子任务 '{subtask.id}' 第 {attempt+1} 次失败(可重试): {type(e).__name__}，"
                            f"{delay:.1f}s 后重试"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"子任务 '{subtask.id}' 已达最大重试次数 "
                            f"({self.retry_config.max_retries})，最终失败"
                        )
                else:
                    # 不可重试异常（编程错误：ValueError, TypeError 等）→ 立即失败
                    logger.error(
                        f"子任务 '{subtask.id}' 遇到不可重试异常 {type(e).__name__}: {e}，"
                        f"立即终止"
                    )
                    return ExecutionResult(
                        subtask_id=subtask.id,
                        status=ExecutionStatus.FAILED,
                        error=f"不可重试异常: {type(e).__name__}: {e}",
                        duration_seconds=time.time() - start,
                        retry_count=attempt,
                    )

        return ExecutionResult(
            subtask_id=subtask.id,
            status=ExecutionStatus.FAILED,
            error=last_error,
            duration_seconds=time.time() - start,
            retry_count=total_retries,
        )

    def _group_by_level(self, dag: TaskDAG, sorted_ids: List[str]) -> List[List[str]]:
        """按拓扑层级分组"""
        if not dag.subtasks:
            return []

        id_to_subtask = {t.id: t for t in dag.subtasks}
        levels: List[List[str]] = []
        assigned: set = set()

        while len(assigned) < len(sorted_ids):
            level: List[str] = []
            for tid in sorted_ids:
                if tid in assigned:
                    continue
                subtask = id_to_subtask.get(tid)
                if not subtask:
                    continue
                deps = set(subtask.depends_on)
                if deps.issubset(assigned):
                    level.append(tid)
            if not level:
                # 防止死循环（不应该发生，但防御）
                remaining = set(sorted_ids) - assigned
                logger.error(f"无法分组的任务: {remaining}")
                level = list(remaining)
            levels.append(level)
            assigned.update(level)

        return levels

    def _build_report(
        self, results: List[ExecutionResult], total_duration: float
    ) -> ExecutionReport:
        """构建执行报告"""
        completed = sum(1 for r in results if r.status == ExecutionStatus.SUCCESS)
        failed = sum(1 for r in results if r.status == ExecutionStatus.FAILED)
        timed_out = sum(1 for r in results if r.status == ExecutionStatus.TIMEOUT)
        cancelled = sum(1 for r in results if r.status == ExecutionStatus.CANCELLED)

        total_tokens = sum(r.tokens_used for r in results)

        return ExecutionReport(
            total_tasks=len(results),
            completed=completed,
            failed=failed,
            timed_out=timed_out,
            cancelled=cancelled,
            results=results,
            total_tokens_used=total_tokens,
            total_duration_seconds=total_duration,
        )

    def _default_executor(self, subtask: SubTask) -> str:
        """默认执行器（mock，实际使用时替换为 sessions_spawn）"""
        logger.info(f"[Mock] 执行子任务: {subtask.id} — {subtask.goal}")
        time.sleep(0.1)  # 模拟延迟
        return f"[{subtask.id}] 完成: {subtask.goal}"


# 注意：熔断器功能已统一由 circuit_breaker.py 的 CircuitBreakerEngine 提供。
# dispatcher 如需熔断能力，通过依赖注入传入 CircuitBreakerEngine 实例。
