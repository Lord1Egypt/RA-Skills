"""Unified metrics — single entry point combining MemoryMetrics + MetricsCollector."""
from __future__ import annotations

import logging
import threading
import time
from typing import Any

from .metrics import MemoryMetrics
from ..infra.metrics import MetricsCollector

logger = logging.getLogger(__name__)


class UnifiedMetrics:
    """Single entry point for all metrics — combines MemoryMetrics + MetricsCollector.

    - MemoryMetrics: per-operation latency/count (tenant-aware)
    - MetricsCollector: business metrics (QPS, latency percentiles, storage stats)
    - Simple counters and gauges for ad-hoc instrumentation
    - System metrics (CPU/memory/disk) via MetricsCollector's store access
    """

    def __init__(self, config=None, max_tenants: int = 10000):
        self._memory_metrics = MemoryMetrics()
        self._system_metrics = MetricsCollector()
        self._counters: dict[str, dict[str, Any]] = {}
        self._gauges: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._max_tenants = max_tenants
        self._tenant_last_access: dict[str, float] = {}

    # ── Operation recording (proxied to MemoryMetrics) ──────────────

    def record_operation(
        self,
        operation: str,
        duration: float,
        tenant_id: str | None = None,
        is_error: bool = False,
        **labels,
    ):
        """Record an operation with latency in milliseconds."""
        self._memory_metrics.record(operation, duration, tenant_id=tenant_id, is_error=is_error)  # type: ignore[arg-type]
        if tenant_id:
            with self._lock:
                self._tenant_last_access[tenant_id] = time.time()
                self._evict_tenants_if_needed()

    # ── Simple counters ─────────────────────────────────────────────

    def record_counter(self, name: str, value: int = 1, **labels):
        """Increment a named counter."""
        key = self._label_key(name, labels)
        with self._lock:
            if key not in self._counters:
                self._counters[key] = {"name": name, "value": 0, "labels": labels}
            self._counters[key]["value"] += value

    # ── Simple gauges ───────────────────────────────────────────────

    def record_gauge(self, name: str, value: float, **labels):
        """Set a named gauge to an absolute value."""
        key = self._label_key(name, labels)
        with self._lock:
            self._counters.pop(key, None)  # same name+labels cannot be both counter and gauge
            self._gauges[key] = {"name": name, "value": value, "labels": labels}

    # ── System metrics ──────────────────────────────────────────────

    def get_system_metrics(self) -> dict:
        """Get CPU/memory/disk stats via MonitoringSystem (requires psutil)."""
        try:
            from ..infra.metrics import get_monitoring_system
            monitor = get_monitoring_system()
            return monitor.get_system_status()
        except Exception as e:
            logger.debug("System metrics unavailable: %s", e)
            return {}

    # ── Operation summaries ─────────────────────────────────────────

    def get_operation_summary(
        self,
        operation: str | None = None,
        tenant_id: str | None = None,
    ) -> dict:
        """Get operation metrics summary, optionally filtered by operation or tenant."""
        if tenant_id:
            return self._memory_metrics.get_tenant_summary(tenant_id)
        summary = self._memory_metrics.get_summary()
        if operation and "operations" in summary:
            ops = summary["operations"].get(operation)
            if ops is not None:
                return {"operation": operation, **ops}
            return {}
        return summary

    # ── Comprehensive snapshot ──────────────────────────────────────

    def get_all_metrics(self) -> dict:
        """Return a comprehensive snapshot of all metric sources."""
        result: dict[str, Any] = {}

        # 1. Per-operation metrics from MemoryMetrics
        result["operations"] = self._memory_metrics.get_summary()

        # 2. Business metrics from MetricsCollector
        result["business"] = self._system_metrics.get_summary()

        # 3. Counters and gauges
        with self._lock:
            result["counters"] = {
                k: {"name": v["name"], "value": v["value"], "labels": v["labels"]}
                for k, v in self._counters.items()
            }
            result["gauges"] = {
                k: {"name": v["name"], "value": v["value"], "labels": v["labels"]}
                for k, v in self._gauges.items()
            }

        # 4. System metrics
        result["system"] = self.get_system_metrics()

        return result

    # ── Tenant cleanup (fix MemoryMetrics unbounded growth) ─────────

    def cleanup_tenant(self, tenant_id: str):
        """Remove all metrics for a specific tenant."""
        with self._lock:
            self._memory_metrics._tenant_ops.pop(tenant_id, None)
            self._tenant_last_access.pop(tenant_id, None)
        logger.debug("Cleaned up metrics for tenant: %s", tenant_id)

    def cleanup_idle_tenants(self, max_idle_seconds: float = 3600):
        """Remove metrics for tenants that haven't been accessed recently."""
        now = time.time()
        with self._lock:
            idle_tenants = [
                tid for tid, last_access in self._tenant_last_access.items()
                if now - last_access > max_idle_seconds
            ]
        for tid in idle_tenants:
            self.cleanup_tenant(tid)
        if idle_tenants:
            logger.info("Cleaned up %d idle tenants (idle > %ds)", len(idle_tenants), max_idle_seconds)

    # ── Internal helpers ────────────────────────────────────────────

    def _label_key(self, name: str, labels: dict) -> str:
        if not labels:
            return name
        sorted_labels = sorted(labels.items())
        label_str = ",".join(f"{k}={v}" for k, v in sorted_labels)
        return f"{name}{{{label_str}}}"

    def _evict_tenants_if_needed(self):
        """LRU eviction of oldest tenant metrics when max_tenants is exceeded."""
        if len(self._tenant_last_access) <= self._max_tenants:
            return
        # Sort by last access time, evict oldest 10%
        evict_count = max(1, len(self._tenant_last_access) - self._max_tenants + self._max_tenants // 10)
        sorted_tenants = sorted(self._tenant_last_access.items(), key=lambda x: x[1])
        for tid, _ in sorted_tenants[:evict_count]:
            self._memory_metrics._tenant_ops.pop(tid, None)
            self._tenant_last_access.pop(tid, None)
        logger.debug("Evicted %d tenant metrics (max_tenants=%d)", evict_count, self._max_tenants)

    # ── Direct access to underlying collectors (backward compat) ────

    @property
    def memory_metrics(self) -> MemoryMetrics:
        return self._memory_metrics

    @property
    def system_metrics(self) -> MetricsCollector:
        return self._system_metrics


_unified_metrics: UnifiedMetrics | None = None


def get_unified_metrics() -> UnifiedMetrics:
    global _unified_metrics
    if _unified_metrics is None:
        _unified_metrics = UnifiedMetrics()
    return _unified_metrics
