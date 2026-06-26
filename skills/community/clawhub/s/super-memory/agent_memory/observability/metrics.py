"""Pre-defined metrics for Agent Memory operations."""
from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional


@dataclass
class OperationMetric:
    operation: str
    count: int = 0
    total_ms: float = 0.0
    min_ms: float = float('inf')
    max_ms: float = 0.0
    error_count: int = 0

    @property
    def avg_ms(self) -> float:
        return self.total_ms / self.count if self.count > 0 else 0

    def record(self, latency_ms: float, is_error: bool = False):
        self.count += 1
        self.total_ms += latency_ms
        self.min_ms = min(self.min_ms, latency_ms)
        self.max_ms = max(self.max_ms, latency_ms)
        if is_error:
            self.error_count += 1


class MemoryMetrics:
    def __init__(self):
        self._ops: dict[str, OperationMetric] = {}
        self._lock = threading.Lock()
        self._tenant_ops: dict[str, dict[str, OperationMetric]] = {}

    def record(self, operation: str, latency_ms: float, tenant_id: str = None, is_error: bool = False):
        with self._lock:
            if operation not in self._ops:
                self._ops[operation] = OperationMetric(operation=operation)
            self._ops[operation].record(latency_ms, is_error)

            if tenant_id:
                if tenant_id not in self._tenant_ops:
                    self._tenant_ops[tenant_id] = {}
                if operation not in self._tenant_ops[tenant_id]:
                    self._tenant_ops[tenant_id][operation] = OperationMetric(operation=operation)
                self._tenant_ops[tenant_id][operation].record(latency_ms, is_error)

    def get_summary(self) -> dict:
        with self._lock:
            return {
                "operations": {
                    name: {
                        "count": op.count,
                        "avg_ms": round(op.avg_ms, 2),
                        "min_ms": round(op.min_ms, 2) if op.min_ms != float('inf') else 0,
                        "max_ms": round(op.max_ms, 2),
                        "error_count": op.error_count,
                    }
                    for name, op in self._ops.items()
                },
                "tenants": len(self._tenant_ops),
            }

    def get_tenant_summary(self, tenant_id: str) -> dict:
        with self._lock:
            ops = self._tenant_ops.get(tenant_id, {})
            return {
                "tenant_id": tenant_id,
                "operations": {
                    name: {
                        "count": op.count,
                        "avg_ms": round(op.avg_ms, 2),
                        "error_count": op.error_count,
                    }
                    for name, op in ops.items()
                },
            }

    def reset(self):
        with self._lock:
            self._ops.clear()
            self._tenant_ops.clear()


_metrics_instance: Optional[MemoryMetrics] = None


def get_metrics() -> MemoryMetrics:
    global _metrics_instance
    if _metrics_instance is None:
        _metrics_instance = MemoryMetrics()
    return _metrics_instance
