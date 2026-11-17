"""
引擎健康度管理 — 自动降级策略
────────────────────────────
持续追踪每个搜索引擎的可用性，自动降级不可用引擎。
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class EngineHealthStatus(str, Enum):
    HEALTHY = "healthy"        # 正常运行
    DEGRADED = "degraded"      # 性能下降（高延迟）
    UNSTABLE = "unstable"      # 不稳定（间歇性失败）
    DEAD = "dead"               # 不可用（持续失败）


@dataclass
class EngineMetrics:
    """单个引擎的指标"""
    engine_name: str
    total_calls: int = 0
    success_count: int = 0
    failure_count: int = 0
    total_latency_ms: float = 0.0
    last_success_time: float = 0.0
    last_failure_time: float = 0.0
    consecutive_failures: int = 0
    consecutive_successes: int = 0
    status: EngineHealthStatus = EngineHealthStatus.HEALTHY
    degraded_since: float = 0.0

    @property
    def success_rate(self) -> float:
        total = self.total_calls
        return self.success_count / total if total > 0 else 1.0

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.total_calls if self.total_calls > 0 else 0.0

    @property
    def is_available(self) -> bool:
        return self.status != EngineHealthStatus.DEAD

    def record_success(self, latency_ms: float = 0):
        self.total_calls += 1
        self.success_count += 1
        self.total_latency_ms += latency_ms
        self.consecutive_successes += 1
        self.consecutive_failures = 0
        self.last_success_time = time.time()
        self._recalculate_status()

    def record_failure(self):
        self.total_calls += 1
        self.failure_count += 1
        self.consecutive_failures += 1
        self.consecutive_successes = 0
        self.last_failure_time = time.time()
        self._recalculate_status()

    def _recalculate_status(self):
        """根据指标重新计算引擎状态"""
        if self.consecutive_failures >= 5:
            self.status = EngineHealthStatus.DEAD
            self.degraded_since = time.time()
        elif self.consecutive_failures >= 3:
            self.status = EngineHealthStatus.UNSTABLE
            self.degraded_since = time.time()
        elif self.avg_latency_ms > 10000:  # 平均延迟超过10秒
            self.status = EngineHealthStatus.DEGRADED
        elif self.consecutive_successes >= 3:
            # 恢复
            self.status = EngineHealthStatus.HEALTHY
            self.degraded_since = 0.0

    def should_skip(self) -> bool:
        """是否应该跳过此引擎"""
        if self.status == EngineHealthStatus.DEAD:
            # DEAD 引擎至少等5分钟再试
            if time.time() - self.degraded_since < 300:
                return True
            # 恢复为 UNSTABLE 状态尝试
            self.status = EngineHealthStatus.UNSTABLE
        return False


class EngineHealthManager:
    """
    引擎健康度管理器

    用法:
        manager = EngineHealthManager()

        # 记录成功
        manager.record_success("baidu", latency_ms=1500)

        # 记录失败
        manager.record_failure("google")

        # 获取可用引擎列表
        available = manager.get_available_engines()

        # 获取健康报告
        report = manager.get_health_report()
    """

    def __init__(self):
        self._engines: dict[str, EngineMetrics] = {}

    def get_or_create(self, engine_name: str) -> EngineMetrics:
        if engine_name not in self._engines:
            self._engines[engine_name] = EngineMetrics(engine_name=engine_name)
        return self._engines[engine_name]

    def record_success(self, engine_name: str, latency_ms: float = 0):
        metrics = self.get_or_create(engine_name)
        metrics.record_success(latency_ms)
        logger.debug(f"Engine [{engine_name}]: success (rate={metrics.success_rate:.1%})")

    def record_failure(self, engine_name: str):
        metrics = self.get_or_create(engine_name)
        metrics.record_failure()
        logger.warning(
            f"Engine [{engine_name}]: failure "
            f"(consecutive={metrics.consecutive_failures}, status={metrics.status.value})"
        )

    def get_available_engines(self, engine_names: list[str]) -> list[str]:
        """获取可用的引擎列表（排除 DEAD 和应跳过的）"""
        available = []
        for name in engine_names:
            metrics = self.get_or_create(name)
            if not metrics.should_skip():
                available.append(name)
            else:
                logger.info(f"Engine [{name}] skipped: status={metrics.status.value}")

        # 按健康度排序：HEALTHY > DEGRADED > UNSTABLE
        def sort_key(name: str) -> int:
            m = self._engines.get(name)
            if not m:
                return 0
            order = {
                EngineHealthStatus.HEALTHY: 0,
                EngineHealthStatus.DEGRADED: 1,
                EngineHealthStatus.UNSTABLE: 2,
            }
            return order.get(m.status, 3)

        available.sort(key=sort_key)
        return available

    def get_health_report(self) -> dict:
        """获取完整健康报告"""
        report = {}
        for name, metrics in self._engines.items():
            report[name] = {
                "status": metrics.status.value,
                "success_rate": round(metrics.success_rate, 3),
                "avg_latency_ms": round(metrics.avg_latency_ms, 1),
                "total_calls": metrics.total_calls,
                "consecutive_failures": metrics.consecutive_failures,
            }
        return report

    def reset_engine(self, engine_name: str):
        """重置引擎状态"""
        self._engines[engine_name] = EngineMetrics(engine_name=engine_name)
        logger.info(f"Engine [{engine_name}]: reset to HEALTHY")
