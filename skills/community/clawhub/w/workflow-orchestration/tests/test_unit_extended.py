"""
Extended unit tests for workflow orchestration.
"""

import pytest
from src import WorkflowOrchestrator, WorkflowInstance, WorkflowStatus
from src.models import (
    WorkflowConfig, PhaseConfig, TransitionRule, TaskMetadata,
    ChangeType, SizeLevel, RiskLevel, PhaseResult
)
from src.exceptions import ExceptionType, SeverityLevel, ExceptionHandler
from src.registry import WorkflowRegistry
from src.executor import PhaseExecutor
from src.router import TaskRouter
import threading
import time


class TestBoundaryScenarios:
    """Test boundary scenarios."""

    def test_empty_context(self):
        """Test starting workflow with empty context."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {})
        assert instance.context == {}

    def test_none_artifacts(self):
        """Test handling None artifacts."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"artifacts": None})
        assert instance.artifacts == {}

    def test_invalid_change_type(self):
        """Test handling invalid change type."""
        with pytest.raises(ValueError):
            ChangeType("invalid_type")

    def test_invalid_size_level(self):
        """Test handling invalid size level."""
        with pytest.raises(ValueError):
            SizeLevel("invalid_size")

    def test_invalid_risk_level(self):
        """Test handling invalid risk level."""
        with pytest.raises(ValueError):
            RiskLevel("invalid_risk")

    def test_workflow_not_found(self):
        """Test starting workflow that doesn't exist."""
        orchestrator = WorkflowOrchestrator()
        with pytest.raises(ValueError, match="Workflow not found"):
            orchestrator.start_workflow("nonexistent", {})

    def test_instance_not_found(self):
        """Test operating on instance that doesn't exist."""
        orchestrator = WorkflowOrchestrator()
        with pytest.raises(ValueError, match="Instance not found"):
            orchestrator.advance_phase("nonexistent_id")

    def test_phase_not_found(self):
        """Test phase not found scenario."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {})
        instance.current_phase = "nonexistent_phase"
        with pytest.raises(ValueError, match="Current phase not found"):
            orchestrator.advance_phase(instance.id)


class TestArtifactValidation:
    """Test artifact validation."""

    def test_missing_required_artifacts(self):
        """Test missing required artifacts."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        # requirement phase requires proposal.md
        instance.artifacts = {}  # empty artifacts
        result = orchestrator.advance_phase(instance.id)
        assert not result.success

    def test_partial_required_artifacts(self):
        """Test partial required artifacts."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        # requirement phase requires proposal.md
        instance.artifacts = {"other.md": "content"}  # wrong artifact
        result = orchestrator.advance_phase(instance.id)
        assert not result.success

    def test_all_required_artifacts(self):
        """Test all required artifacts present."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test proposal"}
        })
        result = orchestrator.advance_phase(instance.id)
        assert result.success

    def test_no_required_artifacts(self):
        """Test phase with no required artifacts."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test"}
        })
        # Advance to requirement phase (requires proposal.md)
        orchestrator.advance_phase(instance.id, gate_passed=True)
        # Advance to design phase (requires design.md and tasks.md)
        instance.artifacts = {"design.md": "design", "tasks.md": "tasks"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success


class TestTransitionConditions:
    """Test phase transition conditions."""

    def test_transition_blocked_by_gate_failure(self):
        """Test transition blocked by gate failure."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test"}
        })
        # Fail the requirement gate
        result = orchestrator.advance_phase(instance.id, gate_passed=False)
        assert not result.success
        assert instance.status == WorkflowStatus.PAUSED

    def test_transition_blocked_by_missing_artifacts(self):
        """Test transition blocked by missing artifacts."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        instance.artifacts = {}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert not result.success

    def test_successful_transition(self):
        """Test successful transition."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test"}
        })
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "design"


class TestExceptionHandling:
    """Test exception handling scenarios."""

    def test_minor_exception_no_rollback(self):
        """Test minor exception doesn't trigger rollback."""
        handler = ExceptionHandler()
        result = handler.handle_exception(
            ExceptionType.TECHNICAL_DEBT,
            SeverityLevel.MINOR,
            {}
        )
        assert result.handled
        assert not result.rollback_triggered

    def test_critical_exception_triggers_rollback(self):
        """Test critical exception triggers rollback."""
        handler = ExceptionHandler()
        result = handler.handle_exception(
            ExceptionType.PRODUCTION_ISSUE,
            SeverityLevel.CRITICAL,
            {}
        )
        assert result.handled
        assert result.rollback_triggered

    def test_manual_rollback_trigger(self):
        """Test manual rollback trigger."""
        handler = ExceptionHandler()
        result = handler.trigger_rollback("quality_gate_failure_3_times", {})
        assert result.success
        assert "rollback_to_design" in result.rollback_to_phase

    def test_unknown_exception_type(self):
        """Test handling unknown exception type."""
        handler = ExceptionHandler()
        result = handler.handle_exception(
            ExceptionType.REQUIREMENT_CHANGE,
            SeverityLevel.MINOR,
            {}
        )
        assert result.handled
        # The default action for REQUIREMENT_CHANGE MINOR should be adjust_requirements
        assert result.action_taken in ["adjust_requirements", "log_and_continue"]


class TestRouterRoutingRules:
    """Test routing rules scenarios."""

    def test_add_custom_routing_rule(self):
        """Test adding custom routing rule."""
        router = TaskRouter()
        router.add_routing_rule("custom_rule", {
            "change_types": [ChangeType.FEATURE],
            "workflow": "custom"
        })
        rules = router.get_routing_rules()
        assert "custom_rule" in rules

    def test_multiple_routing_conditions(self):
        """Test routing with multiple conditions."""
        router = TaskRouter()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.XS,
            risk_level=RiskLevel.LOW,
            cross_module=False
        )
        workflow = router.route_task(metadata)
        assert workflow == "lightweight"

    def test_cross_module_routing(self):
        """Test routing with cross_module flag."""
        router = TaskRouter()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.LOW,
            cross_module=True
        )
        workflow = router.route_task(metadata)
        # cross_module doesn't change routing in current logic
        assert workflow == "lightweight"


class TestConcurrentSafety:
    """Test concurrent safety."""

    def test_concurrent_workflow_starts(self):
        """Test starting multiple workflows concurrently."""
        orchestrator = WorkflowOrchestrator()
        results = []

        def start_workflow():
            instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
            results.append(instance.id)

        threads = [threading.Thread(target=start_workflow) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 5
        assert len(set(results)) == 5  # All IDs are unique

    def test_concurrent_phase_advances(self):
        """Test advancing phases concurrently."""
        orchestrator = WorkflowOrchestrator()
        instances = [
            orchestrator.start_workflow("standard", {
                "change_type": "feature",
                "artifacts": {"proposal.md": "test"}
            })
            for _ in range(3)
        ]

        results = []

        def advance_phase(instance_id):
            result = orchestrator.advance_phase(instance_id, gate_passed=True)
            results.append(result.success)

        threads = [threading.Thread(target=advance_phase, args=(inst.id,)) for inst in instances]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 3
        assert all(results)  # All advances successful


class TestErrorRecovery:
    """Test error recovery."""

    def test_recovery_from_paused_state(self):
        """Test recovery from paused state."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        # Pause by failing gate
        result = orchestrator.advance_phase(instance.id, gate_passed=False)
        assert instance.status == WorkflowStatus.PAUSED

        # Recover by retrying with gate passed
        instance.status = WorkflowStatus.RUNNING
        instance.artifacts = {"proposal.md": "test"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success

    def test_recovery_from_rollback(self):
        """Test recovery from rollback."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test"}
        })
        # Trigger rollback
        result = orchestrator.handle_exception(
            instance.id,
            ExceptionType.QUALITY_GATE_FAILURE,
            SeverityLevel.CRITICAL
        )
        assert result.rollback_triggered
        # Status should be ROLLED_BACK after rollback
        assert instance.status == WorkflowStatus.ROLLED_BACK

        # Recovery: reset phase to a valid phase before continuing
        instance.status = WorkflowStatus.RUNNING
        instance.current_phase = "requirement"  # Reset to valid phase
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success


class TestPhaseExecutorMethods:
    """Test PhaseExecutor specific methods."""

    def test_set_gate_result_manual(self):
        """Test setting gate result manually."""
        executor = PhaseExecutor()
        executor.set_gate_result("test_gate", False)
        result = executor.get_gate_result("test_gate")
        assert result is False

    def test_validate_artifacts_empty_required(self):
        """Test validating artifacts with empty required list."""
        executor = PhaseExecutor()
        result = executor.validate_artifacts([], {"some.md": "content"})
        assert result is True

    def test_validate_artifacts_empty_existing(self):
        """Test validating artifacts with empty existing artifacts."""
        executor = PhaseExecutor()
        result = executor.validate_artifacts(["required.md"], {})
        assert result is False

    def test_execute_phase_with_gate_check(self):
        """Test executing phase with gate check."""
        executor = PhaseExecutor()
        phase = PhaseConfig(id="test", gate="test-gate", agent="test-agent")
        context = {"test-gate_passed": True, "artifacts": {}}
        result = executor.execute_phase(phase, context)
        assert result.gate_passed
        assert result.success


class TestWorkflowRegistryMethods:
    """Test WorkflowRegistry specific methods."""

    def test_get_nonexistent_workflow(self):
        """Test getting nonexistent workflow."""
        registry = WorkflowRegistry()
        result = registry.get_workflow("nonexistent")
        assert result is None

    def test_validate_nonexistent_workflow(self):
        """Test validating nonexistent workflow."""
        registry = WorkflowRegistry()
        result = registry.validate_workflow("nonexistent")
        assert result is False

    def test_register_and_retrieve_workflow(self):
        """Test registering and retrieving workflow."""
        registry = WorkflowRegistry()
        workflow = WorkflowConfig(
            name="test_workflow",
            description="Test workflow",
            phases=[
                PhaseConfig(id="phase1", gate="gate1")
            ]
        )
        registry.register_workflow(workflow)
        retrieved = registry.get_workflow("test_workflow")
        assert retrieved.name == "test_workflow"