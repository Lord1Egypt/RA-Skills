"""
三级熔断器 — 引擎级 / 阶段级 / 全局级
──────────────────────────────────────
原设计只有全或无熔断，一个引擎挂了整条链熔断。
现在改为三级粒度：单引擎失败只熔断该引擎，不影响同阶段其他引擎。
"""
from __future__ import annotations

import time
import logging
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class CircuitState(str, Enum):
    CLOSED = "closed"              # 正常通行
    OPEN = "open"                  # 熔断打开，拒绝请求
    HALF_OPEN = "half_open"        # 半开，尝试恢复


@dataclass
class CircuitConfig:
    """熔断器配置"""
    failure_threshold: int = 3          # 连续失败N次 → 熔断
    timeout_seconds: float = 120.0      # 单步超时
    half_open_seconds: float = 30.0     # 半开状态持续时间
    recovery_success_threshold: int = 2  # 半开状态下成功N次 → 恢复


@dataclass
class CircuitStats:
    """熔断器统计"""
    total_calls: int = 0
    total_failures: int = 0
    total_successes: int = 0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    last_failure_time: float = 0.0
    last_success_time: float = 0.0
    last_state_change: float = field(default_factory=time.time)
    state: CircuitState = CircuitState.CLOSED


class CircuitBreaker:
    """
    单个熔断器实例 — 可用于引擎级或阶段级

    状态转换:
        CLOSED ──连续失败N次──→ OPEN
        OPEN   ──半开时间到──→ HALF_OPEN
        HALF_OPEN ──成功──→ CLOSED (重置计数)
        HALF_OPEN ──失败──→ OPEN (重新熔断)
    """

    def __init__(self, name: str, config: Optional[CircuitConfig] = None):
        self.name = name
        self.config = config or CircuitConfig()
        self.stats = CircuitStats()
        self._lock = threading.Lock()

    def call(self, func, *args, **kwargs):
        """通过熔断器调用函数"""
        with self._lock:
            if not self._allow_request():
                raise CircuitBreakerOpenError(
                    f"Circuit breaker [{self.name}] is OPEN. "
                    f"Consecutive failures: {self.stats.consecutive_failures}"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _allow_request(self) -> bool:
        """检查是否允许请求通过"""
        if self.stats.state == CircuitState.CLOSED:
            return True

        if self.stats.state == CircuitState.OPEN:
            elapsed = time.time() - self.stats.last_state_change
            if elapsed >= self.config.half_open_seconds:
                logger.info(f"Circuit [{self.name}] transitioning OPEN → HALF_OPEN")
                self.stats.state = CircuitState.HALF_OPEN
                self.stats.last_state_change = time.time()
                return True
            return False

        if self.stats.state == CircuitState.HALF_OPEN:
            return True

        return False

    def _on_success(self):
        with self._lock:
            self.stats.total_calls += 1
            self.stats.total_successes += 1
            self.stats.consecutive_successes += 1
            self.stats.consecutive_failures = 0
            self.stats.last_success_time = time.time()

            if self.stats.state == CircuitState.HALF_OPEN:
                if self.stats.consecutive_successes >= self.config.recovery_success_threshold:
                    logger.info(f"Circuit [{self.name}] recovered: HALF_OPEN → CLOSED")
                    self.stats.state = CircuitState.CLOSED
                    self.stats.last_state_change = time.time()
                    self.stats.consecutive_successes = 0

    def _on_failure(self):
        with self._lock:
            self.stats.total_calls += 1
            self.stats.total_failures += 1
            self.stats.consecutive_failures += 1
            self.stats.consecutive_successes = 0
            self.stats.last_failure_time = time.time()

            if self.stats.state == CircuitState.CLOSED:
                if self.stats.consecutive_failures >= self.config.failure_threshold:
                    logger.warning(
                        f"Circuit [{self.name}] tripped: CLOSED → OPEN "
                        f"({self.stats.consecutive_failures} consecutive failures)"
                    )
                    self.stats.state = CircuitState.OPEN
                    self.stats.last_state_change = time.time()

            elif self.stats.state == CircuitState.HALF_OPEN:
                logger.warning(f"Circuit [{self.name}] re-tripped: HALF_OPEN → OPEN")
                self.stats.state = CircuitState.OPEN
                self.stats.last_state_change = time.time()

    def reset(self):
        """手动重置熔断器"""
        with self._lock:
            logger.info(f"Circuit [{self.name}] manually reset to CLOSED")
            self.stats = CircuitStats()

    def is_open(self) -> bool:
        return self.stats.state == CircuitState.OPEN


class CircuitBreakerOpenError(Exception):
    """熔断器打开时抛出的异常"""
    pass


class TieredCircuitBreaker:
    """
    三级熔断器管理器
    ─────────────────
    L1 (引擎级): 每个搜索引擎独立熔断，一个引擎挂了不影响其他
    L2 (阶段级): 某阶段所有引擎都被熔断 → 熔断该阶段
    L3 (全局级): 两个以上阶段被熔断 → 全局熔断，降级返回
    """

    def __init__(self):
        # L1: 引擎级熔断器
        self._engine_breakers: dict[str, CircuitBreaker] = {}
        self._engine_lock = threading.Lock()

        # L2: 阶段级熔断器
        self._phase_breakers: dict[str, CircuitBreaker] = {}

        # L3: 全局熔断器
        self.global_breaker = CircuitBreaker(
            "global",
            CircuitConfig(
                failure_threshold=3,
                timeout_seconds=600,
                half_open_seconds=60,
                recovery_success_threshold=3,
            ),
        )

    def get_engine_breaker(self, engine_name: str) -> CircuitBreaker:
        """获取或创建引擎级熔断器"""
        with self._engine_lock:
            if engine_name not in self._engine_breakers:
                self._engine_breakers[engine_name] = CircuitBreaker(
                    f"engine:{engine_name}",
                    CircuitConfig(
                        failure_threshold=3,
                        timeout_seconds=15,
                        half_open_seconds=30,
                    ),
                )
            return self._engine_breakers[engine_name]

    def get_phase_breaker(self, phase_name: str) -> CircuitBreaker:
        """获取或创建阶段级熔断器"""
        if phase_name not in self._phase_breakers:
            self._phase_breakers[phase_name] = CircuitBreaker(
                f"phase:{phase_name}",
                CircuitConfig(
                    failure_threshold=3,
                    timeout_seconds=120,
                    half_open_seconds=60,
                ),
            )
        return self._phase_breakers[phase_name]

    def engine_call(self, engine_name: str, func, *args, **kwargs):
        """通过引擎级熔断器调用"""
        breaker = self.get_engine_breaker(engine_name)
        return breaker.call(func, *args, **kwargs)

    def phase_call(self, phase_name: str, func, *args, **kwargs):
        """通过阶段级熔断器调用"""
        breaker = self.get_phase_breaker(phase_name)
        return breaker.call(func, *args, **kwargs)

    def check_phase_health(self, phase_name: str, engine_names: list[str]) -> bool:
        """
        检查阶段健康度 — 如果该阶段所有引擎都被熔断，触发阶段级熔断
        返回 True 表示阶段可用，False 表示所有引擎都挂了
        """
        all_open = all(
            self.get_engine_breaker(en).is_open()
            for en in engine_names
        )
        if all_open:
            logger.error(f"Phase [{phase_name}]: ALL engines are OPEN — phase is dead")
            # 触发阶段级熔断
            phase_breaker = self.get_phase_breaker(phase_name)
            for _ in range(self._phase_breakers[phase_name].config.failure_threshold):
                phase_breaker._on_failure()
            return False
        return True

    def check_global_health(self, phase_names: list[str], engine_groups: dict[str, list[str]]) -> bool:
        """
        检查全局健康度
        如果两个以上阶段所有引擎都挂了 → 触发全局熔断
        """
        dead_phases = 0
        for phase_name in phase_names:
            engines = engine_groups.get(phase_name, [])
            if engines and not self.check_phase_health(phase_name, engines):
                dead_phases += 1

        if dead_phases >= 2:
            logger.critical(f"GLOBAL CIRCUIT BREAKER TRIPPED: {dead_phases} phases dead")
            self.global_breaker._on_failure()
            return False
        return True

    def get_status_report(self) -> dict:
        """获取完整的熔断状态报告"""
        engines_status = {
            name: {
                "state": cb.stats.state.value,
                "failures": cb.stats.consecutive_failures,
                "total_calls": cb.stats.total_calls,
            }
            for name, cb in self._engine_breakers.items()
        }
        phases_status = {
            name: {
                "state": cb.stats.state.value,
                "failures": cb.stats.consecutive_failures,
            }
            for name, cb in self._phase_breakers.items()
        }
        return {
            "global": {
                "state": self.global_breaker.stats.state.value,
                "failures": self.global_breaker.stats.consecutive_failures,
            },
            "engines": engines_status,
            "phases": phases_status,
        }
