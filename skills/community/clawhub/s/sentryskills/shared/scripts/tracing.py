"""OpenTelemetry tracing configuration for TrinityGuard.

This module provides distributed tracing with OpenTelemetry.
"""

from __future__ import annotations

import os
import time
from contextlib import contextmanager
from typing import Any, Dict, Optional

try:
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
    from opentelemetry.sdk.trace import sampling
    from opentelemetry import metrics
    from opentelemetry.sdk.metrics import MeterProvider
    from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
    from opentelemetry.sdk.resources import Resource, SERVICE_NAME, SERVICE_VERSION
    OPENTELEMETRY_AVAILABLE = True
except ImportError:
    OPENTELEMETRY_AVAILABLE = False
    # Create dummy classes
    class TracerProvider:
        pass
    class trace:
        @staticmethod
        def get_tracer(name):
            return DummyTracer()
    class DummyTracer:
        @contextmanager
        def start_as_current_span(self, name, **kwargs):
            return DummySpan()
    class DummySpan:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def set_attribute(self, key, value):
            pass
        def add_event(self, name, attributes=None):
            pass
        def set_status(self, status):
            pass
        def record_exception(self, exception):
            pass
    class DummyContextManager:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass


if OPENTELEMETRY_AVAILABLE:
    # Global tracer provider
    _tracer_provider: Optional[TracerProvider] = None
    _meter_provider: Optional[MeterProvider] = None
    _tracer: Optional[trace.Tracer] = None
    _meter: Optional[metrics.Meter] = None

    def configure_tracing(
        service_name: str = "trinityguard",
        service_version: str = "3.2.0",
        console_export: bool = True,
        sample_rate: float = 1.0
    ):
        """Configure OpenTelemetry tracing.

        Args:
            service_name: Name of the service
            service_version: Version of the service
            console_export: Whether to export traces to console
            sample_rate: Sampling rate (0.0 to 1.0)
        """
        global _tracer_provider, _tracer

        # Create resource
        resource = Resource.create({
            SERVICE_NAME: service_name,
            SERVICE_VERSION: service_version,
            "deployment.environment": os.environ.get("TRINITYGUARD_ENVIRONMENT", "development")
        })

        # Create tracer provider
        _tracer_provider = TracerProvider(resource=resource)

        # Add console exporter (for development)
        if console_export:
            console_exporter = ConsoleSpanExporter()
            _tracer_provider.add_span_processor(BatchSpanProcessor(console_exporter))

        # Set sampling
        sampler = sampling.TraceIdRatioBased(sample_rate)
        _tracer_provider = TracerProvider(resource=resource, sampler=sampler)

        # Set global tracer
        trace.set_tracer_provider(_tracer_provider)
        _tracer = trace.get_tracer(__name__)

    def configure_metrics(
        service_name: str = "trinityguard",
        service_version: str = "3.2.0",
        console_export: bool = True,
        export_interval_ms: int = 15000
    ):
        """Configure OpenTelemetry metrics.

        Args:
            service_name: Name of the service
            service_version: Version of the service
            console_export: Whether to export metrics to console
            export_interval_ms: Export interval in milliseconds
        """
        global _meter_provider, _meter

        # Create resource
        resource = Resource.create({
            SERVICE_NAME: service_name,
            SERVICE_VERSION: service_version,
        })

        # Create meter provider
        _meter_provider = MeterProvider(resource=resource)

        # Add console exporter (for development)
        if console_export:
            console_exporter = ConsoleMetricExporter()
            reader = PeriodicExportingMetricReader(console_exporter, export_interval_ms=export_interval_ms/1000)
            _meter_provider = MeterProvider(resource=resource, metric_readers=[reader])

        # Set global meter provider
        metrics.set_meter_provider(_meter_provider)
        _meter = metrics.get_meter(__name__)

    def get_tracer():
        """Get the global tracer.

        Returns:
            OpenTelemetry Tracer instance
        """
        if _tracer is None:
            configure_tracing()
        return _tracer

    def get_meter():
        """Get the global meter.

        Returns:
            OpenTelemetry Meter instance
        """
        if _meter is None:
            configure_metrics()
        return _meter

    @contextmanager
    def trace_span(
        name: str,
        attributes: Dict[str, Any] = None,
        tracer=None
    ):
        """Context manager for creating a span.

        Args:
            name: Span name
            attributes: Initial attributes
            tracer: Optional tracer (uses default if not provided)

        Example:
            with trace_span("preflight_check", {"request_id": "abc-123"}):
                # do work
                pass
        """
        if tracer is None:
            tracer = get_tracer()

        with tracer.start_as_current_span(name, attributes=attributes or {}) as span:
            try:
                yield span
            except Exception as e:
                span.record_exception(e)
                span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                raise
            else:
                span.set_status(trace.Status(trace.StatusCode.OK))

    def add_span_event(name: str, attributes: Dict[str, Any] = None):
        """Add an event to the current span.

        Args:
            name: Event name
            attributes: Event attributes
        """
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            current_span.add_event(name, attributes)

    def set_span_attribute(key: str, value: Any):
        """Set an attribute on the current span.

        Args:
            key: Attribute key
            value: Attribute value
        """
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            current_span.set_attribute(key, value)

    def record_exception(exception: Exception):
        """Record an exception on the current span.

        Args:
            exception: Exception to record
        """
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            current_span.record_exception(exception)

else:
    # Fallback implementations
    def configure_tracing(*args, **kwargs):
        """Configure tracing (no-op)."""
        pass

    def configure_metrics(*args, **kwargs):
        """Configure metrics (no-op)."""
        pass

    def get_tracer():
        """Get tracer (no-op)."""
        return DummyTracer()

    def get_meter():
        """Get meter (no-op)."""
        return None

    @contextmanager
    def trace_span(name: str, attributes: Dict[str, Any] = None, tracer=None):
        """Context manager for creating a span (no-op)."""
        yield DummySpan()

    def add_span_event(name: str, attributes: Dict[str, Any] = None):
        """Add event to span (no-op)."""
        pass

    def set_span_attribute(key: str, value: Any):
        """Set span attribute (no-op)."""
        pass

    def record_exception(exception: Exception):
        """Record exception (no-op)."""
        pass


# Span context helpers
class SpanContext:
    """Helper class for managing span context."""

    def __init__(self, request_id: str = None):
        """Initialize span context.

        Args:
            request_id: Optional request ID
        """
        self.request_id = request_id or self._generate_request_id()
        self.attributes = {}

    @staticmethod
    def _generate_request_id() -> str:
        """Generate a unique request ID."""
        import uuid
        return str(uuid.uuid4())

    def add_attribute(self, key: str, value: Any):
        """Add an attribute to be included in all child spans.

        Args:
            key: Attribute key
            value: Attribute value
        """
        self.attributes[key] = value

    def get_base_attributes(self) -> Dict[str, Any]:
        """Get base attributes for spans.

        Returns:
            Dictionary of base attributes
        """
        base = {
            'request_id': self.request_id,
            'service': 'trinityguard',
            'environment': os.environ.get('TRINITYGUARD_ENVIRONMENT', 'development'),
        }
        base.update(self.attributes)
        return base


def trace_operation(operation_name: str):
    """Decorator to trace an operation.

    Args:
        operation_name: Name of the operation

    Example:
        @trace_operation("preflight_decision")
        def preflight_decision(...):
            ...
    """
    if not OPENTELEMETRY_AVAILABLE:
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        return decorator

    def decorator(func):
        def wrapper(*args, **kwargs):
            with trace_span(operation_name):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    record_exception(e)
                    raise
        return wrapper
    return decorator


def is_available() -> bool:
    """Check if OpenTelemetry is available.

    Returns:
        True if opentelemetry libraries are installed
    """
    return OPENTELEMETRY_AVAILABLE


__all__ = [
    # Configuration
    'configure_tracing',
    'configure_metrics',
    # Accessors
    'get_tracer',
    'get_meter',
    # Context managers
    'trace_span',
    # Helpers
    'add_span_event',
    'set_span_attribute',
    'record_exception',
    'trace_operation',
    'SpanContext',
    # Utility
    'is_available',
]
