"""
Integration tests for workflow orchestration.
"""

import pytest
import json
import yaml
import tempfile
import os
from src import WorkflowOrchestrator, WorkflowInstance, WorkflowStatus
from src.models import (
    WorkflowConfig, PhaseConfig, TransitionRule, TaskMetadata,
    ChangeType, SizeLevel, RiskLevel
)
from src.exceptions import ExceptionType, SeverityLevel


class TestSerializationIntegration:
    """Test serialization and deserialization integration."""

    def test_workflow_config_json_serialization(self):
        """Test WorkflowConfig JSON serialization."""
        workflow = WorkflowConfig(
            name="test_workflow",
            description="Test workflow description",
            phases=[
                PhaseConfig(id="phase1", gate="gate1", agent="agent1", required_artifacts=["artifact1.md"]),
                PhaseConfig(id="phase2", gate="gate2", agent="agent2"),
            ],
            transitions=[
                TransitionRule("phase1", "phase2", "gate1 passed")
            ]
        )

        # Serialize to JSON
        json_str = json.dumps(workflow.to_dict(), indent=2)

        # Deserialize from JSON
        loaded_dict = json.loads(json_str)
        loaded_workflow = WorkflowConfig.from_dict(loaded_dict)

        assert loaded_workflow.name == workflow.name
        assert loaded_workflow.description == workflow.description
        assert len(loaded_workflow.phases) == len(workflow.phases)
        assert len(loaded_workflow.transitions) == len(workflow.transitions)

    def test_workflow_config_yaml_serialization(self):
        """Test WorkflowConfig YAML serialization."""
        workflow = WorkflowConfig(
            name="test_workflow",
            description="Test workflow description",
            phases=[
                PhaseConfig(id="phase1", gate="gate1", agent="agent1"),
            ],
            transitions=[]
        )

        # Serialize to YAML
        yaml_str = yaml.dump(workflow.to_dict())

        # Deserialize from YAML
        loaded_dict = yaml.safe_load(yaml_str)
        loaded_workflow = WorkflowConfig.from_dict(loaded_dict)

        assert loaded_workflow.name == workflow.name

    def test_task_metadata_serialization(self):
        """Test TaskMetadata serialization."""
        metadata = TaskMetadata(
            change_type=ChangeType.FEATURE,
            change_size=SizeLevel.M,
            risk_level=RiskLevel.MEDIUM,
            cross_module=True,
            user_keywords=["test", "keyword"]
        )

        # Serialize and deserialize
        json_str = json.dumps(metadata.to_dict())
        loaded_dict = json.loads(json_str)
        loaded_metadata = TaskMetadata.from_dict(loaded_dict)

        assert loaded_metadata.change_type == metadata.change_type
        assert loaded_metadata.change_size == metadata.change_size
        assert loaded_metadata.risk_level == metadata.risk_level

    def test_workflow_instance_serialization(self):
        """Test WorkflowInstance serialization."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test"}
        })

        # Serialize
        instance_dict = instance.to_dict()
        json_str = json.dumps(instance_dict)

        # Deserialize
        loaded_dict = json.loads(json_str)
        loaded_instance = WorkflowInstance.from_dict(loaded_dict)

        assert loaded_instance.id == instance.id
        assert loaded_instance.workflow_name == instance.workflow_name
        assert loaded_instance.status == instance.status


class TestPersistenceIntegration:
    """Test persistence integration."""

    def test_save_to_file_and_load(self):
        """Test saving workflow instance to file and loading."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test"}
        })

        # Save instance data
        instance_data = orchestrator.save_instance(instance.id)

        # Write to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(instance_data, f)
            temp_file = f.name

        # Read from file
        with open(temp_file, 'r') as f:
            loaded_data = json.load(f)

        # Clean up
        os.unlink(temp_file)

        # Load instance
        loaded_instance = orchestrator.load_instance(loaded_data)
        assert loaded_instance.id == instance.id

    def test_persist_workflow_config_to_yaml(self):
        """Test persisting workflow config to YAML file."""
        workflow = WorkflowConfig(
            name="custom_workflow",
            description="Custom workflow for testing",
            phases=[
                PhaseConfig(id="step1", gate="gate1", agent="agent1"),
                PhaseConfig(id="step2", gate="gate2", agent="agent2"),
            ],
            transitions=[
                TransitionRule("step1", "step2", "gate1 passed")
            ]
        )

        # Write to temporary YAML file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(workflow.to_dict(), f)
            temp_file = f.name

        # Read from YAML file
        with open(temp_file, 'r') as f:
            loaded_dict = yaml.safe_load(f)

        # Clean up
        os.unlink(temp_file)

        # Reconstruct workflow
        loaded_workflow = WorkflowConfig.from_dict(loaded_dict)
        assert loaded_workflow.name == workflow.name


class TestWorkflowLifecycleIntegration:
    """Test complete workflow lifecycle integration."""

    def test_standard_workflow_complete_lifecycle(self):
        """Test standard workflow complete lifecycle."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})

        # Simulate advancing through all phases
        artifacts_sequence = [
            {"proposal.md": "proposal"},  # requirement
            {"design.md": "design", "tasks.md": "tasks"},  # design
            {},  # development
            {"review_findings": "findings"},  # code_review
            {"test_plan": "plan"},  # test_planning
            {"verification-report.md": "report"},  # testing
            {"retrospective.md": "retrospective"},  # reflection
            {},  # archive
        ]

        for i, artifacts in enumerate(artifacts_sequence):
            instance.artifacts = artifacts
            result = orchestrator.advance_phase(instance.id, gate_passed=True)

            if i < len(artifacts_sequence) - 1:
                # Should advance to next phase
                assert result.success or instance.status == WorkflowStatus.PAUSED

        # Final status should be COMPLETED
        assert instance.status == WorkflowStatus.COMPLETED

    def test_lightweight_workflow_complete_lifecycle(self):
        """Test lightweight workflow complete lifecycle."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("lightweight", {"change_type": "docs"})

        # Advance through all 4 phases
        for _ in range(4):
            result = orchestrator.advance_phase(instance.id, gate_passed=True)

        assert instance.status == WorkflowStatus.COMPLETED

    def test_hotfix_workflow_complete_lifecycle(self):
        """Test hotfix workflow complete lifecycle."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("hotfix", {"change_type": "bugfix"})

        # Phase 1: diagnose
        instance.artifacts = {"proposal.md": "Bug diagnosis"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)

        # Phase 2: fix
        result = orchestrator.advance_phase(instance.id, gate_passed=True)

        # Phase 3: regression_test
        instance.artifacts = {"verification-report.md": "Regression tests passed"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)

        # Phase 4: reflection (requires retrospective.md)
        instance.artifacts = {"retrospective.md": "Hotfix retrospective"}
        result = orchestrator.advance_phase(instance.id, gate_passed=True)

        # Phase 5: archive (final)
        result = orchestrator.advance_phase(instance.id, gate_passed=True)

        assert instance.status == WorkflowStatus.COMPLETED


class TestExceptionHandlingIntegration:
    """Test exception handling integration."""

    def test_exception_triggers_workflow_pause(self):
        """Test exception triggers workflow pause."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {"change_type": "feature"})

        # Handle exception
        result = orchestrator.handle_exception(
            instance.id,
            ExceptionType.TECHNICAL_DEBT,
            SeverityLevel.MAJOR
        )

        assert instance.status == WorkflowStatus.PAUSED
        assert result.handled

    def test_critical_exception_triggers_rollback(self):
        """Test critical exception triggers rollback."""
        orchestrator = WorkflowOrchestrator()
        instance = orchestrator.start_workflow("standard", {
            "change_type": "feature",
            "artifacts": {"proposal.md": "test"}
        })

        # Advance to design phase
        orchestrator.advance_phase(instance.id, gate_passed=True)
        assert instance.current_phase == "design"

        # Trigger critical exception
        result = orchestrator.handle_exception(
            instance.id,
            ExceptionType.QUALITY_GATE_FAILURE,
            SeverityLevel.CRITICAL
        )

        assert result.rollback_triggered
        assert instance.status == WorkflowStatus.ROLLED_BACK


class TestRoutingIntegration:
    """Test routing integration."""

    def test_routing_from_metadata_to_workflow(self):
        """Test routing from metadata to workflow."""
        orchestrator = WorkflowOrchestrator()

        # Test various routing scenarios
        test_cases = [
            (ChangeType.BUGFIX, SizeLevel.S, RiskLevel.LOW, "hotfix"),
            (ChangeType.DOCS, SizeLevel.XS, RiskLevel.LOW, "lightweight"),
            (ChangeType.FEATURE, SizeLevel.M, RiskLevel.MEDIUM, "standard"),
            (ChangeType.CONFIG, SizeLevel.S, RiskLevel.HIGH, "standard"),
        ]

        for change_type, size, risk, expected_workflow in test_cases:
            metadata = TaskMetadata(
                change_type=change_type,
                change_size=size,
                risk_level=risk
            )
            routed_workflow = orchestrator.route_task(metadata)
            assert routed_workflow == expected_workflow


class TestMultiInstanceIntegration:
    """Test multiple workflow instances integration."""

    def test_multiple_instances_same_workflow(self):
        """Test multiple instances of same workflow."""
        orchestrator = WorkflowOrchestrator()

        # Start multiple instances
        instances = [
            orchestrator.start_workflow("standard", {"change_type": "feature", "id": i})
            for i in range(3)
        ]

        # Verify all instances are unique
        ids = [inst.id for inst in instances]
        assert len(set(ids)) == 3

        # Advance all instances
        for inst in instances:
            inst.artifacts = {"proposal.md": "test"}
            result = orchestrator.advance_phase(inst.id, gate_passed=True)
            assert result.success

    def test_multiple_instances_different_workflows(self):
        """Test multiple instances of different workflows."""
        orchestrator = WorkflowOrchestrator()

        # Start instances of different workflows
        standard_inst = orchestrator.start_workflow("standard", {"change_type": "feature"})
        lightweight_inst = orchestrator.start_workflow("lightweight", {"change_type": "docs"})
        hotfix_inst = orchestrator.start_workflow("hotfix", {"change_type": "bugfix"})

        # Verify different workflows
        assert standard_inst.workflow_name == "standard"
        assert lightweight_inst.workflow_name == "lightweight"
        assert hotfix_inst.workflow_name == "hotfix"

        # Advance each instance
        standard_inst.artifacts = {"proposal.md": "test"}
        orchestrator.advance_phase(standard_inst.id, gate_passed=True)
        assert standard_inst.current_phase == "design"

        orchestrator.advance_phase(lightweight_inst.id, gate_passed=True)
        assert lightweight_inst.current_phase == "update"

        orchestrator.advance_phase(hotfix_inst.id, gate_passed=True)
        assert hotfix_inst.current_phase == "fix"


class TestConfigurationPersistenceIntegration:
    """Test configuration persistence integration."""

    def test_custom_workflow_registration_and_persistence(self):
        """Test custom workflow registration and persistence."""
        orchestrator = WorkflowOrchestrator()

        # Register custom workflow
        custom_workflow = WorkflowConfig(
            name="custom_persist_test",
            description="Custom workflow for persistence test",
            phases=[
                PhaseConfig(id="step1", gate="gate1", agent="agent1"),
                PhaseConfig(id="step2", gate="gate2", agent="agent2"),
            ],
            transitions=[]
        )
        orchestrator.register_workflow(custom_workflow)

        # Verify registration
        assert "custom_persist_test" in orchestrator.list_workflows()

        # Start instance
        instance = orchestrator.start_workflow("custom_persist_test", {})

        # Save and load
        instance_data = orchestrator.save_instance(instance.id)
        loaded_instance = orchestrator.load_instance(instance_data)

        assert loaded_instance.workflow_name == "custom_persist_test"