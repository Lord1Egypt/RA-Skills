"""
End-to-end tests for workflow orchestration.
"""

import pytest
from src import WorkflowOrchestrator, WorkflowStatus
from src.models import TaskMetadata, ChangeType, SizeLevel, RiskLevel, WorkflowConfig, PhaseConfig, TransitionRule
from src.exceptions import ExceptionType, SeverityLevel


class TestStandardWorkflowE2E:
    """Test standard workflow end-to-end."""

    def test_standard_8_phase_workflow_complete(self):
        """Test standard workflow with all 8 phases."""
        orchestrator = WorkflowOrchestrator()

        # Start workflow
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "change_size": "m",
            "risk_level": "medium"
        })

        # Verify initial state
        assert instance.workflow_name == "standard"
        assert instance.current_phase == "requirement"
        assert instance.status == WorkflowStatus.RUNNING

        # Phase 1: requirement
        instance.artifacts = {"proposal.md": "Initial proposal for feature X"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "design"
        assert len(instance.history) == 1

        # Phase 2: design
        instance.artifacts = {
            "design.md": "Technical design document",
            "tasks.md": "Implementation task breakdown"
        }
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "development"
        assert len(instance.history) == 2

        # Phase 3: development (no required artifacts)
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "code_review"
        assert len(instance.history) == 3

        # Phase 4: code_review
        instance.artifacts = {"review_findings": "Code review completed, approved"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "test_planning"
        assert len(instance.history) == 4

        # Phase 5: test_planning
        instance.artifacts = {"test_plan": "Test plan with unit and integration tests"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "testing"
        assert len(instance.history) == 5

        # Phase 6: testing
        instance.artifacts = {"verification-report.md": "All tests passed"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "reflection"
        assert len(instance.history) == 6

        # Phase 7: reflection
        instance.artifacts = {"retrospective.md": "Retrospective completed"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "archive"
        assert len(instance.history) == 7

        # Phase 8: archive (final phase)
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert instance.status == WorkflowStatus.COMPLETED
        assert len(instance.history) == 8


class TestLightweightWorkflowE2E:
    """Test lightweight workflow end-to-end."""

    def test_lightweight_4_phase_workflow_complete(self):
        """Test lightweight workflow with all 4 phases."""
        orchestrator = WorkflowOrchestrator()

        # Start workflow
        instance = orchestrator.start_workflow("lightweight", {
            "change_type": "docs",
            "change_size": "xs",
            "risk_level": "low"
        })

        # Verify initial state
        assert instance.workflow_name == "lightweight"
        assert instance.current_phase == "clarify"

        # Phase 1: clarify
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "update"

        # Phase 2: update
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "verify"

        # Phase 3: verify
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "archive"

        # Phase 4: archive (final)
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert instance.status == WorkflowStatus.COMPLETED
        assert len(instance.history) == 4


class TestHotfixWorkflowE2E:
    """Test hotfix workflow end-to-end."""

    def test_hotfix_5_phase_workflow_complete(self):
        """Test hotfix workflow with all 5 phases."""
        orchestrator = WorkflowOrchestrator()

        # Start workflow
        instance = orchestrator.start_workflow("hotfix", {
            "change_type": "bugfix",
            "change_size": "s",
            "risk_level": "medium"
        })

        # Verify initial state
        assert instance.workflow_name == "hotfix"
        assert instance.current_phase == "diagnose"

        # Phase 1: diagnose
        instance.artifacts = {"proposal.md": "Bug diagnosis report"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "fix"

        # Phase 2: fix
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "regression_test"

        # Phase 3: regression_test
        instance.artifacts = {"verification-report.md": "Regression tests passed"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "reflection"

        # Phase 4: reflection
        instance.artifacts = {"retrospective.md": "Hotfix retrospective"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "archive"

        # Phase 5: archive (final)
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert instance.status == WorkflowStatus.COMPLETED
        assert len(instance.history) == 5


class TestRealScenarioE2E:
    """Test real-world scenario end-to-end."""

    def test_feature_development_with_gate_failure_and_recovery(self):
        """Test feature development with gate failure and recovery."""
        orchestrator = WorkflowOrchestrator()

        # Start workflow
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "project": "e-commerce-platform"
        })

        # Phase 1: requirement (gate passes)
        instance.artifacts = {"proposal.md": "Add product recommendation engine"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "design"

        # Phase 2: design (gate fails)
        instance.artifacts = {
            "design.md": "Machine learning model design",
            "tasks.md": "Implementation tasks"
        }
        result = orchestrator.advance_phase(instance.id, gate_passed=False)
        assert not result.success
        assert instance.status == WorkflowStatus.PAUSED
        assert instance.current_phase == "design"  # Stays in design

        # Recovery: retry design phase
        instance.status = WorkflowStatus.RUNNING
        instance.artifacts = {
            "design.md": "Improved design document",
            "tasks.md": "Updated task breakdown"
        }
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert result.success
        assert instance.current_phase == "development"
        assert instance.status == WorkflowStatus.RUNNING

    def test_hotfix_with_critical_exception(self):
        """Test hotfix with critical exception triggering rollback."""
        orchestrator = WorkflowOrchestrator()

        # Start hotfix workflow
        instance = orchestrator.start_workflow("hotfix", {
            "change_type": "bugfix",
            "bug_id": "BUG-123",
            "severity": "P1"
        })

        # Phase 1: diagnose
        instance.artifacts = {"proposal.md": "Critical payment bug diagnosis"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert instance.current_phase == "fix"

        # Phase 2: fix (trigger critical exception)
        instance.artifacts = {"fix_implemented": True}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert instance.current_phase == "regression_test"

        # Trigger critical exception during regression testing
        result = orchestrator.handle_exception(
            instance.id,
            ExceptionType.PRODUCTION_ISSUE,
            SeverityLevel.CRITICAL
        )

        assert result.rollback_triggered
        assert instance.status == WorkflowStatus.ROLLED_BACK


class TestMultiRoundInteractionE2E:
    """Test multi-round interaction end-to-end."""

    def test_multiple_workflow_instances_parallel(self):
        """Test multiple workflow instances running in parallel."""
        orchestrator = WorkflowOrchestrator()

        # Start 3 different workflows
        standard_inst = orchestrator.start_workflow("standard", {"change_type": "feature", "id": "FEAT-1"})
        lightweight_inst = orchestrator.start_workflow("lightweight", {"change_type": "docs", "id": "DOC-1"})
        hotfix_inst = orchestrator.start_workflow("hotfix", {"change_type": "bugfix", "id": "BUG-1"})

        # Verify all instances started
        assert standard_inst.status == WorkflowStatus.RUNNING
        assert lightweight_inst.status == WorkflowStatus.RUNNING
        assert hotfix_inst.status == WorkflowStatus.RUNNING

        # Advance each workflow independently
        standard_inst.artifacts = {"proposal.md": "Feature proposal"}
        orchestrator.advance_phase(standard_inst.id, gate_passed=True)
        assert standard_inst.current_phase == "design"

        orchestrator.advance_phase(lightweight_inst.id, gate_passed=True)
        assert lightweight_inst.current_phase == "update"

        hotfix_inst.artifacts = {"proposal.md": "Bug diagnosis"}
        orchestrator.advance_phase(hotfix_inst.id, gate_passed=True)
        assert hotfix_inst.current_phase == "fix"

        # Continue advancing
        standard_inst.artifacts = {"design.md": "Design", "tasks.md": "Tasks"}
        orchestrator.advance_phase(standard_inst.id, gate_passed=True)
        assert standard_inst.current_phase == "development"

        # Complete lightweight workflow
        orchestrator.advance_phase(lightweight_inst.id, gate_passed=True)
        orchestrator.advance_phase(lightweight_inst.id, gate_passed=True)
        orchestrator.advance_phase(lightweight_inst.id, gate_passed=True)
        assert lightweight_inst.status == WorkflowStatus.COMPLETED

        # Check all instances still exist
        assert orchestrator.get_workflow_status(standard_inst.id) is not None
        assert orchestrator.get_workflow_status(lightweight_inst.id) is not None
        assert orchestrator.get_workflow_status(hotfix_inst.id) is not None

    def test_workflow_instance_persistence_and_recovery(self):
        """Test workflow instance persistence and recovery."""
        orchestrator = WorkflowOrchestrator()

        # Start workflow
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "Initial proposal"}
        })

        # Advance to design phase
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        assert instance.current_phase == "design"

        # Save instance state
        instance_data = orchestrator.save_instance(instance.id)

        # Create new orchestrator (simulate restart)
        new_orchestrator = WorkflowOrchestrator()

        # Load instance from saved data
        loaded_instance = new_orchestrator.load_instance(instance_data)

        # Verify state preserved
        assert loaded_instance.id == instance.id
        assert loaded_instance.workflow_name == "standard"
        assert loaded_instance.current_phase == "design"
        assert loaded_instance.status == WorkflowStatus.RUNNING
        assert len(loaded_instance.history) == 1

        # Continue advancing in new orchestrator
        loaded_instance.artifacts = {"design.md": "Design", "tasks.md": "Tasks"}
        result = new_orchestrator.advance_phase(loaded_instance.id, gate_passed=True)
        assert result.success
        assert loaded_instance.current_phase == "development"