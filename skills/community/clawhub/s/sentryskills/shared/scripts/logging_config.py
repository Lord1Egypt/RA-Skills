"""Structured logging configuration for TrinityGuard.

This module provides structured logging with JSON output and context enrichment.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict

try:
    import structlog
    STRUCTLOG_AVAILABLE = True
except ImportError:
    STRUCTLOG_AVAILABLE = False
    # Create dummy logger for graceful degradation
    class DummyLogger:
        def __init__(self, *args, **kwargs):
            self.logger = logging.getLogger(__name__)

        def info(self, msg, **kwargs):
            self.logger.info(msg)

        def warning(self, msg, **kwargs):
            self.logger.warning(msg)

        def error(self, msg, **kwargs):
            self.logger.error(msg)

        def debug(self, msg, **kwargs):
            self.logger.debug(msg)

        def exception(self, msg, **kwargs):
            self.logger.exception(msg)


if STRUCTLOG_AVAILABLE:
    def configure_struct_logging(
        json_output: bool = True,
        log_level: str = "INFO",
        service_name: str = "trinityguard"
    ):
        """Configure structured logging for TrinityGuard.

        Args:
            json_output: Whether to output JSON format
            log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            service_name: Service name for logs
        """

        # Configure processors
        processors = [
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
        ]

        # Add JSON or console renderer
        if json_output:
            processors.append(structlog.processors.JSONRenderer())
        else:
            processors.append(structlog.dev.ConsoleRenderer(colors=True))

        # Configure structlog
        structlog.configure(
            processors=processors,
            wrapper_class=structlog.stdlib.BoundLogger,
            context_class=dict,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

    def get_logger(name: str = None) -> Any:
        """Get a structured logger.

        Args:
            name: Logger name (optional)

        Returns:
            Structured logger instance
        """
        if name:
            return structlog.get_logger(name)
        return structlog.get_logger()

    class RequestContextProcessor:
        """Add request context to log records."""

        def __init__(self, request_id: str = None, user_id: str = None):
            self.request_id = request_id or self._generate_request_id()
            self.user_id = user_id

        def _generate_request_id(self) -> str:
            """Generate a unique request ID."""
            import uuid
            return str(uuid.uuid4())

        def __call__(self, logger, method_name, event_dict):
            """Processor to add request context."""
            event_dict['request_id'] = self.request_id
            if self.user_id:
                event_dict['user_id'] = self.user_id
            event_dict['service'] = 'trinityguard'
            event_dict['environment'] = os.environ.get('TRINITYGUARD_ENVIRONMENT', 'development')
            return event_dict

else:
    # Fallback to standard logging
    def configure_struct_logging(
        json_output: bool = True,
        log_level: str = "INFO",
        service_name: str = "trinityguard"
    ):
        """Configure standard logging as fallback."""
        level = getattr(logging, log_level.upper(), logging.INFO)
        logging.basicConfig(
            level=level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def get_logger(name: str = None):
        """Get a standard logger."""
        return DummyLogger()


def log_decision(
    stage: str,
    decision: str,
    reason: str = "",
    context: Dict[str, Any] = None
):
    """Log a decision event.

    Args:
        stage: Stage (preflight/runtime/output)
        decision: Decision (allow/downgrade/block/stop)
        reason: Optional reason
        context: Additional context
    """
    logger = get_logger('decision')

    log_data = {
        'event': 'decision_made',
        'stage': stage,
        'decision': decision,
        'timestamp': datetime.utcnow().isoformat(),
    }

    if reason:
        log_data['reason'] = reason

    if context:
        log_data.update(context)

    if decision == 'block' or decision == 'stop':
        logger.warning('Decision made', **log_data)
    elif decision == 'downgrade':
        logger.info('Decision made', **log_data)
    else:
        logger.debug('Decision made', **log_data)


def log_detection(
    detection_type: str,
    result: bool,
    context: Dict[str, Any] = None
):
    """Log a detection event.

    Args:
        detection_type: Type of detection
        result: Whether threat was detected
        context: Additional context
    """
    logger = get_logger('detection')

    log_data = {
        'event': 'detection_performed',
        'type': detection_type,
        'result': 'detected' if result else 'not_detected',
        'timestamp': datetime.utcnow().isoformat(),
    }

    if context:
        log_data.update(context)

    if result:
        logger.warning('Detection result', **log_data)
    else:
        logger.debug('Detection result', **log_data)


def log_early_exit(
    triggered: bool,
    reason: str = "",
    stages_skipped: list = None
):
    """Log an early exit event.

    Args:
        triggered: Whether early exit was triggered
        reason: Reason for early exit
        stages_skipped: List of stages skipped
    """
    logger = get_logger('early_exit')

    log_data = {
        'event': 'early_exit_check',
        'triggered': triggered,
        'timestamp': datetime.utcnow().isoformat(),
    }

    if reason:
        log_data['reason'] = reason

    if stages_skipped:
        log_data['stages_skipped'] = stages_skipped

    if triggered:
        logger.info('Early exit triggered', **log_data)
    else:
        logger.debug('Early exit check', **log_data)


def log_cache_operation(
    operation: str,
    cache_type: str,
    hit: bool = None,
    context: Dict[str, Any] = None
):
    """Log a cache operation.

    Args:
        operation: Operation (hit/miss/set/delete)
        cache_type: Cache type (detection/pattern)
        hit: Whether it was a cache hit (for hit/miss operations)
        context: Additional context
    """
    logger = get_logger('cache')

    log_data = {
        'event': 'cache_operation',
        'operation': operation,
        'cache_type': cache_type,
        'timestamp': datetime.utcnow().isoformat(),
    }

    if hit is not None:
        log_data['hit'] = hit

    if context:
        log_data.update(context)

    logger.debug('Cache operation', **log_data)


def log_error(
    error_type: str,
    error_message: str,
    context: Dict[str, Any] = None,
    exc_info: bool = False
):
    """Log an error event.

    Args:
        error_type: Type of error
        error_message: Error message
        context: Additional context
        exc_info: Whether to include exception info
    """
    logger = get_logger('error')

    log_data = {
        'event': 'error_occurred',
        'error_type': error_type,
        'error_message': error_message,
        'timestamp': datetime.utcnow().isoformat(),
    }

    if context:
        log_data.update(context)

    if exc_info:
        logger.exception('Error occurred', **log_data)
    else:
        logger.error('Error occurred', **log_data)


def log_invocation(
    user_prompt_length: int,
    planned_actions: list = None,
    context: Dict[str, Any] = None
):
    """Log a TrinityGuard invocation.

    Args:
        user_prompt_length: Length of user prompt
        planned_actions: List of planned actions
        context: Additional context
    """
    logger = get_logger('invocation')

    log_data = {
        'event': 'trinityguard_invoked',
        'user_prompt_length': user_prompt_length,
        'timestamp': datetime.utcnow().isoformat(),
    }

    if planned_actions:
        log_data['planned_actions'] = planned_actions

    if context:
        log_data.update(context)

    logger.info('TrinityGuard invoked', **log_data)


def is_available() -> bool:
    """Check if structured logging is available.

    Returns:
        True if structlog is installed
    """
    return STRUCTLOG_AVAILABLE


__all__ = [
    # Configuration
    'configure_struct_logging',
    'get_logger',
    # Logging functions
    'log_decision',
    'log_detection',
    'log_early_exit',
    'log_cache_operation',
    'log_error',
    'log_invocation',
    # Utility
    'is_available',
    # Processor
    'RequestContextProcessor',
]
