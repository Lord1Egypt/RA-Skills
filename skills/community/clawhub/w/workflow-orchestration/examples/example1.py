"""
Example 1: Basic workflow orchestration.
"""

from workflow_orchestration.src import WorkflowOrchestrator
from workflow_orchestration.src.models import TaskMetadata, ChangeType, SizeLevel, RiskLevel


def main():
    # Initialize orchestrator
    orchestrator = WorkflowOrchestrator(template="standard")

    # Start workflow
    instance = orchestrator.start_workflow("standard", {
        "change_type": "feature",
        "change_size": "m",
        "risk_level": "medium"
    })

    print(f"Started workflow: {instance.workflow_name}")
    print(f"Instance ID: {instance.id}")
    print(f"Current phase: {instance.current_phase}")

    # Advance through phases
    phases_artifacts = [
        {"proposal.md": "Feature proposal"},
        {"design.md": "Design document", "tasks.md": "Task breakdown"},
        {},  # development
        {"review_findings": "Code review findings"},
        {"test_plan": "Test plan"},
        {"verification-report.md": "Verification report"},
        {"retrospective.md": "Retrospective"},
        {},  # archive
    ]

    for i, artifacts in enumerate(phases_artifacts):
        instance.artifacts = artifacts
        result = orchestrator.advance_phase(instance.id, gate_passed=True)

        print(f"Phase {i+1}: {result.phase_id} - Success: {result.success}")
        if result.success:
            print(f"  → Next phase: {instance.current_phase}")

    print(f"Workflow status: {instance.status.value}")


if __name__ == "__main__":
    main()