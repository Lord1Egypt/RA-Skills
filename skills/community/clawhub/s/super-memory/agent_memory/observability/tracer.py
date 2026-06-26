"""Tracing utilities for Agent Memory operations with distributed trace context propagation."""
from __future__ import annotations

import functools
import logging
import os
import threading
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional

logger = logging.getLogger(__name__)

_tracer = None
_meter = None


def _get_service_name() -> str:
    return os.environ.get("AGENT_MEMORY_SERVICE_NAME", "agent-memory")


def get_tracer():
    global _tracer
    if _tracer is not None:
        return _tracer

    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.resources import Resource

        resource = Resource.create({"service.name": _get_service_name(), "service.version": "12.0.0"})
        provider = TracerProvider(resource=resource)

        exporter_name = os.environ.get("AGENT_MEMORY_TRACE_EXPORTER", "none")
        if exporter_name == "otlp":
            from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
            from opentelemetry.sdk.trace.export import BatchSpanProcessor
            endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
            provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint)))
        elif exporter_name == "console":
            from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
            provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

        trace.set_tracer_provider(provider)
        _tracer = trace.get_tracer("agent-memory", "12.0.0")
    except ImportError:
        _tracer = _NoOpTracer()

    return _tracer


def get_meter():
    global _meter
    if _meter is not None:
        return _meter

    try:
        from opentelemetry import metrics
        from opentelemetry.sdk.metrics import MeterProvider
        from opentelemetry.sdk.resources import Resource

        resource = Resource.create({"service.name": _get_service_name(), "service.version": "12.0.0"})
        provider = MeterProvider(resource=resource)

        exporter_name = os.environ.get("AGENT_MEMORY_METRIC_EXPORTER", "none")
        if exporter_name == "otlp":
            from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
            from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
            endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
            reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=endpoint))
            provider = MeterProvider(resource=resource, metric_readers=[reader])
        elif exporter_name == "prometheus":
            from opentelemetry.exporter.prometheus import PrometheusMetricReader
            port = int(os.environ.get("AGENT_MEMORY_PROMETHEUS_PORT", "9465"))
            reader = PrometheusMetricReader(port=port)
            provider = MeterProvider(resource=resource, metric_readers=[reader])

        metrics.set_meter_provider(provider)
        _meter = metrics.get_meter("agent-memory", "12.0.0")
    except ImportError:
        _meter = _NoOpMeter()

    return _meter


class _NoOpTracer:
    def start_span(self, name, **kwargs):
        return _NoOpSpan()

    def start_as_current_span(self, name, **kwargs):
        from contextlib import contextmanager

        @contextmanager
        def _cm():
            yield _NoOpSpan()

        return _cm()


class _NoOpSpan:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def set_attribute(self, key, value):
        pass

    def add_event(self, name, **kwargs):
        pass

    def record_exception(self, exc, **kwargs):
        pass

    def end(self):
        pass


class _NoOpMeter:
    def create_counter(self, name, **kwargs):
        return _NoOpInstrument()

    def create_histogram(self, name, **kwargs):
        return _NoOpInstrument()

    def create_up_down_counter(self, name, **kwargs):
        return _NoOpInstrument()

    def create_observable_counter(self, name, **kwargs):
        return _NoOpInstrument()

    def create_observable_gauge(self, name, **kwargs):
        return _NoOpInstrument()


class _NoOpInstrument:
    def add(self, amount, **kwargs):
        pass

    def record(self, amount, **kwargs):
        pass


# ---------------------------------------------------------------------------
# Distributed Trace Context Propagation (W3C traceparent format)
# ---------------------------------------------------------------------------

@dataclass
class TraceContext:
    """Distributed trace context for cross-service trace linking.

    Follows W3C Trace Context specification (traceparent header format).
    """
    trace_id: str
    span_id: str
    parent_span_id: str = ""
    baggage: Dict[str, str] = field(default_factory=dict)

    # W3C traceparent version
    _VERSION = "00"
    # W3C traceparent trace-flags (01 = sampled)
    _TRACE_FLAGS_SAMPLED = "01"
    _TRACE_FLAGS_NOT_SAMPLED = "00"

    @property
    def sampled(self) -> bool:
        return bool(self._sampled_flag)

    @sampled.setter
    def sampled(self, value: bool):
        self._sampled_flag = value

    def __post_init__(self):
        self._sampled_flag = True

    def to_traceparent(self) -> str:
        """Serialize to W3C traceparent header value.

        Format: {version}-{trace_id}-{span_id}-{trace_flags}
        Example: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
        """
        flags = self._TRACE_FLAGS_SAMPLED if self._sampled_flag else self._TRACE_FLAGS_NOT_SAMPLED
        return f"{self._VERSION}-{self.trace_id}-{self.span_id}-{flags}"

    @classmethod
    def from_traceparent(cls, value: str) -> "TraceContext | None":
        """Parse a W3C traceparent header value."""
        try:
            parts = value.split("-")
            if len(parts) != 4 or parts[0] != cls._VERSION:
                return None
            trace_id = parts[1]
            span_id = parts[2]
            flags = parts[3]
            if len(trace_id) != 32 or len(span_id) != 16:
                return None
            ctx = cls(trace_id=trace_id, span_id=span_id)
            ctx._sampled_flag = flags == cls._TRACE_FLAGS_SAMPLED
            return ctx
        except Exception:
            return None

    @classmethod
    def new(cls, parent_context: "TraceContext | None" = None) -> "TraceContext":
        """Create a new TraceContext, optionally linked to a parent."""
        trace_id = parent_context.trace_id if parent_context else _generate_trace_id()
        span_id = _generate_span_id()
        parent_span_id = parent_context.span_id if parent_context else ""
        ctx = cls(trace_id=trace_id, span_id=span_id, parent_span_id=parent_span_id)
        if parent_context:
            ctx.baggage = dict(parent_context.baggage)
        return ctx


def _generate_trace_id() -> str:
    return uuid.uuid4().hex


def _generate_span_id() -> str:
    return uuid.uuid4().hex[:16]


def inject_trace_context(headers: dict, context: TraceContext | None = None) -> dict:
    """Inject trace context into HTTP headers (W3C traceparent + tracestate + baggage).

    Args:
        headers: Existing headers dict to inject into.
        context: TraceContext to inject. If None, uses current active context.

    Returns:
        The headers dict with trace context headers added.
    """
    if context is None:
        context = _current_trace_context()

    if context is not None:
        headers["traceparent"] = context.to_traceparent()
        if context.parent_span_id:
            headers["tracestate"] = f"parent={context.parent_span_id}"
        if context.baggage:
            baggage_parts = [f"{k}={v}" for k, v in sorted(context.baggage.items())]
            headers["baggage"] = ",".join(baggage_parts)

    return headers


def extract_trace_context(headers: dict) -> TraceContext | None:
    """Extract trace context from HTTP headers (W3C traceparent format).

    Args:
        headers: HTTP headers dict (case-insensitive lookup).

    Returns:
        TraceContext if valid traceparent found, else None.
    """
    # Case-insensitive header lookup
    lower_headers = {k.lower(): v for k, v in headers.items()}

    traceparent = lower_headers.get("traceparent")
    if not traceparent:
        return None

    ctx = TraceContext.from_traceparent(traceparent)
    if ctx is None:
        return None

    # Extract baggage
    baggage_str = lower_headers.get("baggage", "")
    if baggage_str:
        for pair in baggage_str.split(","):
            pair = pair.strip()
            if "=" in pair:
                k, v = pair.split("=", 1)
                ctx.baggage[k.strip()] = v.strip()

    return ctx


# Thread-local storage for active trace context
_trace_context_local: threading.local | None = None

try:
    _trace_context_local = threading.local()
except Exception:
    pass


def _current_trace_context() -> TraceContext | None:
    """Get the current active TraceContext from thread-local storage."""
    if _trace_context_local is not None:
        return getattr(_trace_context_local, "current", None)
    return None


def _set_current_trace_context(ctx: TraceContext | None):
    """Set the current active TraceContext in thread-local storage."""
    if _trace_context_local is not None:
        _trace_context_local.current = ctx  # type: ignore[attr-defined]


@contextmanager
def trace_with_context(operation_name: str, trace_context: TraceContext | None = None):
    """Context manager that creates a child span under the given or current trace context.

    Args:
        operation_name: Name of the operation being traced.
        trace_context: Optional parent TraceContext. If None, uses current context
                       or creates a new root context.

    Yields:
        The child TraceContext for this span.
    """
    parent = trace_context or _current_trace_context()
    child_ctx = TraceContext.new(parent_context=parent)

    previous = _current_trace_context()
    _set_current_trace_context(child_ctx)

    start = time.perf_counter()
    try:
        yield child_ctx
    finally:
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.debug(
            "trace: %s completed in %.1fms (trace_id=%s, span_id=%s)",
            operation_name, elapsed_ms, child_ctx.trace_id, child_ctx.span_id,
        )
        _set_current_trace_context(previous)


class MemoryTracer:
    def __init__(self):
        self._tracer = get_tracer()
        self._meter = get_meter()
        self._init_metrics()

    def _init_metrics(self):
        self.remember_counter = self._meter.create_counter(
            "agent_memory_remember_total",
            description="Total number of remember operations",
        )
        self.recall_counter = self._meter.create_counter(
            "agent_memory_recall_total",
            description="Total number of recall operations",
        )
        self.recall_latency = self._meter.create_histogram(
            "agent_memory_recall_latency_ms",
            description="Recall operation latency in milliseconds",
        )
        self.remember_latency = self._meter.create_histogram(
            "agent_memory_remember_latency_ms",
            description="Remember operation latency in milliseconds",
        )
        self.memory_count = self._meter.create_up_down_counter(
            "agent_memory_count",
            description="Current number of stored memories",
        )
        self.error_counter = self._meter.create_counter(
            "agent_memory_errors_total",
            description="Total number of errors",
        )

    def trace_remember(self, func: Callable, parent_context: TraceContext | None = None) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with trace_with_context("remember", parent_context):
                start = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    self.remember_counter.add(1)
                    self.remember_latency.record(elapsed_ms)
                    return result
                except Exception as e:
                    self.error_counter.add(1, {"operation": "remember", "error_type": type(e).__name__})
                    raise

        return wrapper

    def trace_recall(self, func: Callable, parent_context: TraceContext | None = None) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with trace_with_context("recall", parent_context):
                start = time.perf_counter()
                try:
                    result = func(*args, **kwargs)
                    elapsed_ms = (time.perf_counter() - start) * 1000
                    self.recall_counter.add(1)
                    self.recall_latency.record(elapsed_ms)
                    return result
                except Exception as e:
                    self.error_counter.add(1, {"operation": "recall", "error_type": type(e).__name__})
                    raise

        return wrapper


_memory_tracer: Optional[MemoryTracer] = None


def get_memory_tracer() -> MemoryTracer:
    global _memory_tracer
    if _memory_tracer is None:
        _memory_tracer = MemoryTracer()
    return _memory_tracer
