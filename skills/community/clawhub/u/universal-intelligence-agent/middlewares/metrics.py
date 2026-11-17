"""
监控指标导出 — Prometheus 兼容格式
──────────────────────────────────
追踪系统运行时的关键指标：
  - 请求计数
  - 各阶段耗时
  - 熔断器状态
  - 引擎健康度
  - 错误计数
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class MetricsSnapshot:
    """指标快照"""
    timestamp: float = field(default_factory=time.time)
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    degraded_requests: int = 0
    phase_durations: dict[str, list[float]] = field(default_factory=dict)
    engine_errors: dict[str, int] = field(default_factory=lambda: defaultdict(int))
    circuit_breaker_events: int = 0
    rollback_events: int = 0


class MetricsCollector:
    """
    指标收集器

    用法:
        collector = MetricsCollector()

        # 记录请求
        collector.record_request(success=True)

        # 记录阶段耗时
        collector.record_phase_duration("searching", 2.5)

        # 导出 Prometheus 格式
        prometheus_text = collector.export_prometheus()
    """

    def __init__(self):
        self._snapshot = MetricsSnapshot()
        self._start_time = time.time()

    def record_request(self, success: bool = True, degraded: bool = False):
        self._snapshot.total_requests += 1
        if degraded:
            self._snapshot.degraded_requests += 1
        if success:
            self._snapshot.successful_requests += 1
        else:
            self._snapshot.failed_requests += 1

    def record_phase_duration(self, phase: str, duration_seconds: float):
        if phase not in self._snapshot.phase_durations:
            self._snapshot.phase_durations[phase] = []
        self._snapshot.phase_durations[phase].append(duration_seconds)

    def record_engine_error(self, engine_name: str):
        self._snapshot.engine_errors[engine_name] += 1

    def record_circuit_breaker_trip(self):
        self._snapshot.circuit_breaker_events += 1

    def record_rollback(self):
        self._snapshot.rollback_events += 1

    def get_summary(self) -> dict:
        """获取指标摘要"""
        s = self._snapshot
        uptime = time.time() - self._start_time

        phase_stats = {}
        for phase, durations in s.phase_durations.items():
            if durations:
                phase_stats[phase] = {
                    "count": len(durations),
                    "avg_seconds": round(sum(durations) / len(durations), 3),
                    "max_seconds": round(max(durations), 3),
                    "min_seconds": round(min(durations), 3),
                }

        return {
            "uptime_seconds": round(uptime, 1),
            "total_requests": s.total_requests,
            "successful_requests": s.successful_requests,
            "failed_requests": s.failed_requests,
            "degraded_requests": s.degraded_requests,
            "success_rate": round(
                s.successful_requests / max(s.total_requests, 1), 3
            ),
            "circuit_breaker_events": s.circuit_breaker_events,
            "rollback_events": s.rollback_events,
            "phase_stats": phase_stats,
            "engine_errors": dict(s.engine_errors),
        }

    def export_prometheus(self) -> str:
        """导出为 Prometheus 文本格式"""
        s = self._snapshot
        uptime = time.time() - self._start_time

        lines = [
            "# HELP uia_uptime_seconds Total uptime in seconds",
            "# TYPE uia_uptime_seconds gauge",
            f"uia_uptime_seconds {uptime:.1f}",
            "",
            "# HELP uia_requests_total Total number of requests",
            "# TYPE uia_requests_total counter",
            f"uia_requests_total {s.total_requests}",
            "",
            "# HELP uia_requests_successful_total Total successful requests",
            "# TYPE uia_requests_successful_total counter",
            f"uia_requests_successful_total {s.successful_requests}",
            "",
            "# HELP uia_requests_failed_total Total failed requests",
            "# TYPE uia_requests_failed_total counter",
            f"uia_requests_failed_total {s.failed_requests}",
            "",
            "# HELP uia_requests_degraded_total Total degraded requests",
            "# TYPE uia_requests_degraded_total counter",
            f"uia_requests_degraded_total {s.degraded_requests}",
            "",
            "# HELP uia_circuit_breaker_events_total Circuit breaker trip events",
            "# TYPE uia_circuit_breaker_events_total counter",
            f"uia_circuit_breaker_events_total {s.circuit_breaker_events}",
            "",
            "# HELP uia_rollback_events_total Rollback events",
            "# TYPE uia_rollback_events_total counter",
            f"uia_rollback_events_total {s.rollback_events}",
        ]

        # 引擎错误
        if s.engine_errors:
            lines.extend([
                "",
                "# HELP uia_engine_errors_total Engine errors by name",
                "# TYPE uia_engine_errors_total counter",
            ])
            for engine, count in s.engine_errors.items():
                lines.append(
                    f'uia_engine_errors_total{{engine="{engine}"}} {count}'
                )

        return "\n".join(lines) + "\n"

    def reset(self):
        """重置所有指标"""
        self._snapshot = MetricsSnapshot()
        self._start_time = time.time()
