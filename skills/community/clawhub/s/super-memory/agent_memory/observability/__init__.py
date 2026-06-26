"""Agent Memory Observability — OpenTelemetry integration."""
from __future__ import annotations

try:
    import importlib.util
    _HAS_OTEL = importlib.util.find_spec("opentelemetry") is not None
except Exception:
    _HAS_OTEL = False

from .tracer import get_tracer, get_meter, MemoryTracer, TraceContext, inject_trace_context, extract_trace_context, trace_with_context  # noqa: E501
from .metrics import MemoryMetrics
from .unified import UnifiedMetrics, get_unified_metrics
from .alerting import AlertManager, AlertLevel, get_alert_manager

__all__ = [
    "get_tracer", "get_meter", "MemoryTracer", "MemoryMetrics",
    "UnifiedMetrics", "get_unified_metrics",
    "TraceContext", "inject_trace_context", "extract_trace_context", "trace_with_context",
    "AlertManager", "AlertLevel", "get_alert_manager",
    "_HAS_OTEL",
]
