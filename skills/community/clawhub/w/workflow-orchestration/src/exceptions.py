"""
Exception handler for handling workflow exceptions and rollbacks.
"""

from typing import Dict, Any
from dataclasses import dataclass
from enum import Enum


class ExceptionType(Enum):
    """Exception type enumeration."""
    REQUIREMENT_CHANGE = "requirement_change"
    TECHNICAL_DEBT = "technical_debt"
    QUALITY_GATE_FAILURE = "quality_gate_failure"
    PRODUCTION_ISSUE = "production_issue"
    PERFORMANCE_REGRESSION = "performance_regression"


class SeverityLevel(Enum):
    """Exception severity enumeration."""
    MINOR = "minor"
    MAJOR = "major"
    CRITICAL = "critical"


@dataclass
class ExceptionResult:
    """Exception handling result."""
    exception_type: ExceptionType
    severity: SeverityLevel
    handled: bool
    action_taken: str
    rollback_triggered: bool

    def to_dict(self) -> Dict:
        return {
            "exception_type": self.exception_type.value,
            "severity": self.severity.value,
            "handled": self.handled,
            "action_taken": self.action_taken,
            "rollback_triggered": self.rollback_triggered
        }


@dataclass
class RollbackResult:
    """Rollback result."""
    rollback_type: str
    success: bool
    rollback_to_phase: str
    message: str

    def to_dict(self) -> Dict:
        return {
            "rollback_type": self.rollback_type,
            "success": self.success,
            "rollback_to_phase": self.rollback_to_phase,
            "message": self.message
        }


class ExceptionHandler:
    """Exception handler for handling workflow exceptions."""

    def __init__(self):
        self._exception_handlers = self._build_default_handlers()
        self._rollback_triggers = self._build_default_rollback_triggers()

    def _build_default_handlers(self) -> Dict:
        """Build default exception handlers."""
        return {
            ExceptionType.REQUIREMENT_CHANGE: {
                "minor": "adjust_requirements",
                "major": "re_evaluate_design",
                "critical": "restart_workflow"
            },
            ExceptionType.TECHNICAL_DEBT: {
                "minor": "log_and_continue",
                "major": "pause_and_assess",
                "critical": "rollback_to_design"
            },
            ExceptionType.QUALITY_GATE_FAILURE: {
                "minor": "fix_issues",
                "major": "pause_and_fix",
                "critical": "rollback_to_development"
            },
            ExceptionType.PRODUCTION_ISSUE: {
                "minor": "monitor",
                "major": "hotfix",
                "critical": "immediate_rollback"
            },
            ExceptionType.PERFORMANCE_REGRESSION: {
                "minor": "optimize",
                "major": "pause_and_optimize",
                "critical": "rollback_to_development"
            }
        }

    def _build_default_rollback_triggers(self) -> Dict:
        """Build default rollback triggers."""
        return {
            "quality_gate_failure_3_times": "rollback_to_design",
            "performance_regression_50%": "rollback_to_development",
            "production_p1_issue": "immediate_rollback",
            "design_defect_critical": "rollback_to_requirement"
        }

    def handle_exception(self, exception_type: ExceptionType, severity: SeverityLevel, context: Dict) -> ExceptionResult:
        """Handle an exception."""
        handler = self._exception_handlers.get(exception_type, {})
        action = handler.get(severity, "log_and_continue")

        # Determine if rollback should be triggered
        rollback_triggered = False
        if exception_type == ExceptionType.QUALITY_GATE_FAILURE and severity == SeverityLevel.CRITICAL:
            rollback_triggered = True
            action = "rollback_to_development"
        elif exception_type == ExceptionType.PRODUCTION_ISSUE and severity == SeverityLevel.CRITICAL:
            rollback_triggered = True
            action = "immediate_rollback"
        elif action in ["rollback_to_design", "rollback_to_development", "rollback_to_requirement", "immediate_rollback"]:
            rollback_triggered = True

        return ExceptionResult(
            exception_type=exception_type,
            severity=severity,
            handled=True,
            action_taken=action,
            rollback_triggered=rollback_triggered
        )

    def trigger_rollback(self, trigger: str, context: Dict) -> RollbackResult:
        """Trigger a rollback."""
        rollback_to = self._rollback_triggers.get(trigger, "previous_phase")

        return RollbackResult(
            rollback_type=trigger,
            success=True,
            rollback_to_phase=rollback_to,
            message=f"Rollback triggered: {trigger}, rolling back to {rollback_to}"
        )

    def add_exception_handler(self, exception_type: ExceptionType, severity: SeverityLevel, action: str) -> None:
        """Add an exception handler."""
        if exception_type not in self._exception_handlers:
            self._exception_handlers[exception_type] = {}
        self._exception_handlers[exception_type][severity] = action

    def add_rollback_trigger(self, trigger: str, rollback_to: str) -> None:
        """Add a rollback trigger."""
        self._rollback_triggers[trigger] = rollback_to