"""
Main workflow orchestrator.
"""

import uuid
from typing import Dict, Any, Optional
from .models import WorkflowConfig, WorkflowInstance, WorkflowStatus, PhaseResult, TaskMetadata
from .registry import WorkflowRegistry
from .executor import PhaseExecutor
from .router import TaskRouter
from .exceptions import ExceptionHandler, ExceptionType, SeverityLevel


class WorkflowOrchestrator:
    """Main workflow orchestrator."""

    def __init__(self, template: str = "standard"):
        self.registry = WorkflowRegistry()
        self.executor = PhaseExecutor()
        self.router = TaskRouter()
        self.exception_handler = ExceptionHandler()
        self._instances: Dict[str, WorkflowInstance] = {}

        if not self.registry.validate_workflow(template):
            raise ValueError(f"Invalid workflow template: {template}")

    def start_workflow(self, workflow_name: str, initial_context: Dict[str, Any]) -> WorkflowInstance:
        """Start a workflow instance."""
        workflow = self.registry.get_workflow(workflow_name)
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_name}")

        instance_id = str(uuid.uuid4())[:8]
        first_phase = workflow.phases[0].id

        # Handle None artifacts
        artifacts = initial_context.get("artifacts", {})
        if artifacts is None:
            artifacts = {}

        instance = WorkflowInstance(
            id=instance_id,
            workflow_name=workflow_name,
            current_phase=first_phase,
            status=WorkflowStatus.RUNNING,
            context=initial_context,
            artifacts=artifacts,
            history=[]
        )

        self._instances[instance_id] = instance
        return instance

    def advance_phase(self, instance_id: str, gate_passed: bool = True) -> PhaseResult:
        """Advance workflow to next phase."""
        instance = self._instances.get(instance_id)
        if not instance:
            raise ValueError(f"Instance not found: {instance_id}")

        workflow = self.registry.get_workflow(instance.workflow_name)
        if not workflow:
            raise ValueError(f"Workflow not found: {instance.workflow_name}")

        # Find current phase
        current_phase_config = None
        current_phase_index = -1
        for i, phase in enumerate(workflow.phases):
            if phase.id == instance.current_phase:
                current_phase_config = phase
                current_phase_index = i
                break

        if current_phase_config is None:
            raise ValueError(f"Current phase not found: {instance.current_phase}")

        # Execute current phase
        context = instance.context.copy()
        context["artifacts"] = instance.artifacts
        context[f"{current_phase_config.gate}_passed"] = gate_passed

        phase_result = self.executor.execute_phase(current_phase_config, context)
        instance.history.append(phase_result)

        # Check if can advance to next phase
        if phase_result.success:
            if current_phase_index < len(workflow.phases) - 1:
                next_phase = workflow.phases[current_phase_index + 1]
                instance.current_phase = next_phase.id
            else:
                # This is the last phase, workflow is complete
                instance.status = WorkflowStatus.COMPLETED
        elif not phase_result.success:
            instance.status = WorkflowStatus.PAUSED

        return phase_result

    def handle_exception(self, instance_id: str, exception_type: ExceptionType, severity: SeverityLevel) -> ExceptionResult:
        """Handle an exception in workflow."""
        instance = self._instances.get(instance_id)
        if not instance:
            raise ValueError(f"Instance not found: {instance_id}")

        result = self.exception_handler.handle_exception(exception_type, severity, instance.context)

        if result.rollback_triggered:
            rollback_result = self.exception_handler.trigger_rollback(
                f"{exception_type.value}_{severity.value}",
                instance.context
            )
            instance.current_phase = rollback_result.rollback_to_phase
            instance.status = WorkflowStatus.ROLLED_BACK

        instance.status = WorkflowStatus.PAUSED if not result.rollback_triggered else WorkflowStatus.ROLLED_BACK
        return result

    def get_workflow_status(self, instance_id: str) -> Optional[WorkflowInstance]:
        """Get workflow instance status."""
        return self._instances.get(instance_id)

    def route_task(self, metadata: TaskMetadata) -> str:
        """Route a task to appropriate workflow."""
        return self.router.route_task(metadata)

    def register_workflow(self, workflow_config: WorkflowConfig) -> None:
        """Register a custom workflow."""
        self.registry.register_workflow(workflow_config)

    def list_workflows(self) -> list:
        """List all workflows."""
        return self.registry.list_workflows()

    def save_instance(self, instance_id: str) -> Dict:
        """Save instance state to dict."""
        instance = self._instances.get(instance_id)
        if not instance:
            raise ValueError(f"Instance not found: {instance_id}")
        return instance.to_dict()

    def load_instance(self, data: Dict) -> WorkflowInstance:
        """Load instance from dict."""
        instance = WorkflowInstance.from_dict(data)
        self._instances[instance.id] = instance
        return instance