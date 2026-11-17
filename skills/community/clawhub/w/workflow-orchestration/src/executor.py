"""
Phase executor for executing and validating phases.
"""

from typing import Dict, Any
from .models import PhaseConfig, PhaseResult


class PhaseExecutor:
    """Phase executor for executing and validating phases."""

    def __init__(self):
        self._gate_results: Dict[str, bool] = {}

    def execute_phase(self, phase: PhaseConfig, context: Dict[str, Any]) -> PhaseResult:
        """Execute a phase and check gate."""
        gate_passed = self.check_gate(phase.gate, context)
        artifacts_valid = self.validate_artifacts(phase.required_artifacts, context.get("artifacts", {}))

        success = gate_passed and artifacts_valid

        return PhaseResult(
            phase_id=phase.id,
            gate_passed=gate_passed,
            artifacts=context.get("artifacts", {}),
            message=f"Phase {phase.id} executed. Gate: {phase.gate}, Passed: {gate_passed}",
            success=success
        )

    def check_gate(self, gate_name: str, context: Dict[str, Any]) -> bool:
        """Check if a gate passes (mock implementation)."""
        # In real implementation, this would call actual gate check logic
        return context.get(f"{gate_name}_passed", True)

    def validate_artifacts(self, required_artifacts: list, existing_artifacts: Dict[str, Any]) -> bool:
        """Validate required artifacts exist."""
        if not required_artifacts:
            return True
        return all(artifact in existing_artifacts for artifact in required_artifacts)

    def set_gate_result(self, gate_name: str, passed: bool) -> None:
        """Set gate result manually (for testing)."""
        self._gate_results[gate_name] = passed

    def get_gate_result(self, gate_name: str) -> bool:
        """Get gate result."""
        return self._gate_results.get(gate_name, True)