"""
Basic functionality tests for workflow orchestration.
"""

import pytest
from src import WorkflowOrchestrator, WorkflowInstance, WorkflowStatus
from src.models import WorkflowConfig, PhaseConfig, TransitionRule, TaskMetadata, ChangeType, SizeLevel, RiskLevel
from src.exceptions import ExceptionType, SeverityLevel


class TestWorkflowOrchestrator:
    """Test WorkflowOrchestrator basic functionality."""

    def test_init_standard_template(self):
        """Test initialization with standard template."""
        orchestrator = WorkflowOrchestrator(template="standard")
        assert orchestrator is not None
        assert "standard" in orchestrator.list_workflows()

    def test_init_lightweight_template(self):
        """Test initialization with lightweight template."""
        orchestrator = WorkflowOrchestrator(template="lightweight")
        assert orchestrator is not None
        assert "lightweight" in orchestrator.list_workflows()

    def test_init_hotfix_template(self):
        """Test initialization with hotfix template."""
        orchestrator = WorkflowOrchestrator(template="hotfix")
        assert orchestrator is not None
        assert "hotfix" in orchestrator.list_workflows()

    def test_init_invalid_template_raises_error(self):
        """Test initialization with invalid template raises error."""
        with pytest.raises(ValueError, match="Invalid workflow template"):
            WorkflowOrchestrator(template="invalid_template")

    def test_list_workflows(self):
        """Test listing workflows."""
        orchestrator = WorkflowOrchestrator()
        workflows = orchestrator.list_workflows()
        assert len(workflows) == 3
        assert "standard" in workflows
        assert "lightweight" in workflows
        assert "hotfix" in workflows


class TestWorkflowInstance:
    """Test WorkflowInstance lifecycle."""

    def test_start_workflow_standard(self):
        """Test starting standard workflow."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        assert instance.id is not None
        assert instance.workflow_name == "standard"
        assert instance.current_phase == "requirement"
        assert instance.status == WorkflowStatus.RUNNING

    def test_start_workflow_lightweight(self):
        """Test starting lightweight workflow."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("lightweight", {"change_type": "docs"})
        assert instance.workflow_name == "lightweight"
        assert instance.current_phase == "clarify"

    def test_start_workflow_hotfix(self):
        """Test starting hotfix workflow."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("hotfix", {"change_type": "bugfix"})
        assert instance.workflow_name == "hotfix"
        assert instance.current_phase == "diagnose"

    def test_advance_phase(self):
        """Test advancing phase."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test proposal"}
        })
        result = orchestrator.advance_phase(instance.id)
        assert result.success
        assert instance.current_phase == "design"

    def test_advance_phase_with_gate_failure(self):
        """Test advancing phase with gate failure."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        result = orchestrator.advance_phase(instance.id, gate_passed=False)
        assert not result.success
        assert instance.status == WorkflowStatus.PAUSED

    def test_complete_workflow(self):
        """Test completing workflow."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("lightweight", {"change_type": "docs"})

        # Advance through all phases
        orchestrator.advance_phase(instance.id)
        orchestrator.advance_phase(instance.id)
        orchestrator.advance_phase(instance.id)
        orchestrator.advance_phase(instance.id)

        assert instance.status == WorkflowStatus.COMPLETED


class TestTaskRouter:
    """Test TaskRouter functionality."""

    def test_route_bugfix_to_hotfix(self):
        """Test routing bugfix to hotfix."""
        orchestrator = WorkflowOrchestrator()
        metadata = TaskMetadata(
            change_type=ChangeType.BUGFIX,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.LOW
        )
        workflow = orchestrator.route_task(metadata)
        assert workflow == "hotfix"

    def test_route_hotfix_to_hotfix(self):
        """Test routing hotfix to hotfix."""
        orchestrator = WorkflowOrchestrator()
        metadata = TaskMetadata(
            change_type=ChangeType.HOTFIX,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM
        )
        workflow = orchestrator.route_task(metadata)
        assert workflow == "hotfix"

    def test_route_docs_small_low_risk_to_lightweight(self):
        """Test routing docs small low risk to lightweight."""
        orchestrator = WorkflowOrchestrator()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.LOW
        )
        workflow = orchestrator.route_task(metadata)
        assert workflow == "lightweight"

    def test_route_feature_to_standard(self):
        """Test routing feature to standard."""
        orchestrator = WorkflowOrchestrator()
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM
        )
        workflow = orchestrator.route_task(metadata)
        assert workflow == "standard"

    def test_route_high_risk_to_standard(self):
        """Test routing high risk to standard."""
        orchestrator = WorkflowOrchestrator()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.S,
            risk_level=RiskLevel.HIGH
        )
        workflow = orchestrator.route_task(metadata)
        assert workflow == "standard"

    def test_route_large_size_to_standard(self):
        """Test routing large size to standard."""
        orchestrator = WorkflowOrchestrator()
        metadata = TaskMetadata(
            change_type=ChangeType.DOCS,
            change_size=SizeLevel.L,
            risk_level=RiskLevel.LOW
        )
        workflow = orchestrator.route_task(metadata)
        assert workflow == "standard"


class TestExceptionHandler:
    """Test ExceptionHandler functionality."""

    def test_handle_minor_requirement_change(self):
        """Test handling minor requirement change."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        result = orchestrator.handle_exception(
            instance.id,
            ExceptionType.REQUIREMENT_CHANGE,
            SeverityLevel.MINOR
        )
        assert result.handled
        # The action for REQUIREMENT_CHANGE MINOR should be adjust_requirements
        assert result.action_taken in ["adjust_requirements", "log_and_continue"]
        assert not result.rollback_triggered

    def test_handle_critical_quality_gate_failure(self):
        """Test handling critical quality gate failure."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        result = orchestrator.handle_exception(
            instance.id,
            ExceptionType.QUALITY_GATE_FAILURE,
            SeverityLevel.CRITICAL
        )
        assert result.handled
        assert result.rollback_triggered

    def test_handle_production_p1_issue(self):
        """Test handling production P1 issue."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        result = orchestrator.handle_exception(
            instance.id,
            ExceptionType.PRODUCTION_ISSUE,
            SeverityLevel.CRITICAL
        )
        assert result.handled
        assert result.rollback_triggered
        assert instance.status == WorkflowStatus.ROLLED_BACK


class TestWorkflowRegistry:
    """Test WorkflowRegistry functionality."""

    def test_register_custom_workflow(self):
        """Test registering custom workflow."""
        orchestrator = WorkflowOrchestrator()
        custom_workflow = WorkflowConfig(
            name="custom",
            description="Custom workflow",
            phases=[
                PhaseConfig(id="step1", gate="gate1", agent="agent1"),
                PhaseConfig(id="step2", gate="gate2", agent="agent2"),
            ],
            transitions=[
                TransitionRule("step1", "step2", "gate1 passed")
            ]
        )
        orchestrator.register_workflow(custom_workflow)
        assert "custom" in orchestrator.list_workflows()

    def test_start_custom_workflow(self):
        """Test starting custom workflow."""
        orchestrator = WorkflowOrchestrator()
        custom_workflow = WorkflowConfig(
            name="custom",
            description="Custom workflow",
            phases=[
                PhaseConfig(id="step1", gate="gate1", agent="agent1"),
                PhaseConfig(id="step2", gate="gate2", agent="agent2"),
            ],
            transitions=[]
        )
        orchestrator.register_workflow(custom_workflow)
        instance = orchestrator.start_workflow("custom", {})
        assert instance.workflow_name == "custom"
        assert instance.current_phase == "step1"


class TestPhaseExecutor:
    """Test PhaseExecutor functionality."""

    def test_execute_phase_success(self):
        """Test executing phase successfully."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test"}
        })
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert result.gate_passed

    def test_execute_phase_failure(self):
        """Test executing phase with failure."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})
        result = orchestrator.advance_phase(instance.id, gate_passed=False)
        assert not result.success
        assert not result.gate_passed


class TestPersistence:
    """Test instance persistence."""

    def test_save_and_load_instance(self):
        """Test saving and loading instance."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})

        # Save instance
        saved_data = orchestrator.save_instance(instance.id)
        assert saved_data["id"] == instance.id
        assert saved_data["workflow_name"] == "standard"

        # Load instance
        loaded_instance = orchestrator.load_instance(saved_data)
        assert loaded_instance.id == instance.id
        assert loaded_instance.workflow_name == "standard"