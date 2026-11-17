"""
Example 3: Custom workflow and persistence.
"""

from workflow_orchestration.src import WorkflowOrchestrator
from workflow_orchestration.src.models import WorkflowConfig, PhaseConfig, TransitionRule
import json


def main():
    orchestrator = WorkflowOrchestrator()

    # Register custom workflow
    custom_workflow = WorkflowConfig(
        name="my_custom_workflow",
        description="Custom workflow for specific project",
        phases=[
            PhaseConfig(id="step1", gate="validation_gate", agent="validator_agent"),
            PhaseConfig(id="step2", gate="execution_gate", agent="executor_agent"),
            PhaseConfig(id="step3", gate="completion_gate", agent="completer_agent"),
        ],
        transitions=[
            TransitionRule("step1", "step2", "validation_gate passed"),
            TransitionRule("step2", "step3", "execution_gate passed"),
        ]
    )

    orchestrator.register_workflow(custom_workflow)
    print(f"Registered workflow: {custom_workflow.name}")
    print(f"Available workflows: {orchestrator.list_workflows()}")

    # Start custom workflow
    instance = orchestrator.start_workflow("my_custom_workflow", {
        "project": "example_project"
    })

    print(f"\nStarted instance: {instance.id}")
    print(f"Current phase: {instance.current_phase}")

    # Advance through custom phases
    for i in range(3):
        result = orchestrator.advance_phase(instance.id, gate_passed=True)
        print(f"Phase {i+1}: {result.phase_id} - Success: {result.success}")

    # Save instance state
    instance_data = orchestrator.save_instance(instance.id)
    print(f"\nSaved instance data: {json.dumps(instance_data, indent=2)}")

    # Load instance
    loaded_instance = orchestrator.load_instance(instance_data)
    print(f"\nLoaded instance: {loaded_instance.id}")
    print(f"Workflow: {loaded_instance.workflow_name}")
    print(f"Status: {loaded_instance.status.value}")


if __name__ == "__main__":
    main()