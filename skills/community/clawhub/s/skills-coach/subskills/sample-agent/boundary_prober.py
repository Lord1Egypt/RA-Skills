"""
Capability Boundary Prober for Skills-Coach v2.3.1

Generates tasks that specifically probe skill capability boundaries.
"""

from typing import Dict, List, Tuple
from dataclasses import dataclass
import re


@dataclass
class BoundaryCondition:
    """A boundary condition identified in the skill."""
    category: str  # input_boundaries, output_boundaries, constraint_boundaries, integration_boundaries
    condition: str
    severity: str  # critical, important, minor


class CapabilityBoundaryProber:
    """Analyzes SKILL.md and generates boundary-probing tasks."""

    def __init__(self, skill_content: str):
        self.skill_content = skill_content
        self.boundaries: Dict[str, List[BoundaryCondition]] = {
            'input_boundaries': [],
            'output_boundaries': [],
            'constraint_boundaries': [],
            'integration_boundaries': []
        }

    def analyze_skill_boundaries(self) -> Dict[str, List[BoundaryCondition]]:
        """
        Identify capability boundaries from SKILL.md.

        Returns:
            Dictionary of boundary conditions by category
        """
        lines = self.skill_content.split('\n')

        for i, line in enumerate(lines):
            line_lower = line.lower()

            # Input boundaries
            if any(keyword in line_lower for keyword in ['must', 'required', 'expects', 'input']):
                if 'file' in line_lower or 'path' in line_lower:
                    self.boundaries['input_boundaries'].append(
                        BoundaryCondition('input_boundaries', 'File path validation', 'critical')
                    )
                if 'empty' in line_lower or 'null' in line_lower:
                    self.boundaries['input_boundaries'].append(
                        BoundaryCondition('input_boundaries', 'Empty input handling', 'important')
                    )

            # Output boundaries
            if any(keyword in line_lower for keyword in ['output', 'generate', 'create', 'produce']):
                if 'format' in line_lower or 'structure' in line_lower:
                    self.boundaries['output_boundaries'].append(
                        BoundaryCondition('output_boundaries', 'Output format validation', 'important')
                    )

            # Constraint boundaries
            if any(keyword in line_lower for keyword in ['timeout', 'limit', 'maximum', 'minimum']):
                if 'time' in line_lower:
                    self.boundaries['constraint_boundaries'].append(
                        BoundaryCondition('constraint_boundaries', 'Time limit handling', 'critical')
                    )
                if 'size' in line_lower or 'memory' in line_lower:
                    self.boundaries['constraint_boundaries'].append(
                        BoundaryCondition('constraint_boundaries', 'Resource limit handling', 'important')
                    )

            # Integration boundaries
            if any(keyword in line_lower for keyword in ['api', 'network', 'external', 'dependency']):
                self.boundaries['integration_boundaries'].append(
                    BoundaryCondition('integration_boundaries', 'External dependency handling', 'important')
                )

        # Deduplicate
        for category in self.boundaries:
            seen = set()
            unique = []
            for bc in self.boundaries[category]:
                if bc.condition not in seen:
                    seen.add(bc.condition)
                    unique.append(bc)
            self.boundaries[category] = unique

        return self.boundaries

    def generate_boundary_tasks(self) -> List[Dict]:
        """
        Generate tasks that specifically test boundaries.

        Returns:
            List of boundary task specifications
        """
        tasks = []

        # Minimal input tasks
        if self.boundaries['input_boundaries']:
            tasks.append({
                'task_type': 'boundary_minimal',
                'title': 'Empty Input Handling',
                'objective': 'Test behavior with completely empty or minimal input',
                'constraints': [
                    'Must not crash or throw unhandled exceptions',
                    'Must provide meaningful error message or empty result',
                    'Must complete within reasonable time'
                ],
                'expected_behavior': 'Graceful handling with clear feedback'
            })

        # Maximal input tasks
        if self.boundaries['input_boundaries'] or self.boundaries['constraint_boundaries']:
            tasks.append({
                'task_type': 'boundary_maximal',
                'title': 'Large Volume Input',
                'objective': 'Test behavior with input at or beyond stated limits',
                'constraints': [
                    'Must respect documented limits',
                    'Must handle gracefully if exceeded',
                    'Must not consume excessive resources'
                ],
                'expected_behavior': 'Proper limit enforcement or graceful degradation'
            })

        # Invalid input tasks
        if self.boundaries['input_boundaries']:
            tasks.append({
                'task_type': 'boundary_invalid',
                'title': 'Malformed Input Handling',
                'objective': 'Test behavior with syntactically invalid input',
                'constraints': [
                    'Must validate input before processing',
                    'Must provide clear, actionable error message',
                    'Must not proceed with invalid data'
                ],
                'expected_behavior': 'Input validation with helpful error messages'
            })

        # Resource limit tasks
        if self.boundaries['constraint_boundaries']:
            tasks.append({
                'task_type': 'boundary_resource',
                'title': 'Resource Limit Stress Test',
                'objective': 'Test behavior under resource constraints',
                'constraints': [
                    'Must handle timeout gracefully',
                    'Must not exceed memory limits',
                    'Must provide partial results if possible'
                ],
                'expected_behavior': 'Graceful degradation under resource pressure'
            })

        # Failure mode tasks
        if self.boundaries['integration_boundaries']:
            tasks.append({
                'task_type': 'boundary_failure',
                'title': 'External Dependency Failure',
                'objective': 'Test behavior when external dependencies fail',
                'constraints': [
                    'Must detect and log failures',
                    'Must attempt recovery if possible',
                    'Must not leave system in inconsistent state'
                ],
                'expected_behavior': 'Robust error handling and recovery'
            })

        # Combination tasks
        if len(tasks) >= 2:
            tasks.append({
                'task_type': 'boundary_combination',
                'title': 'Multiple Boundary Conditions',
                'objective': 'Test behavior when multiple boundaries are stressed simultaneously',
                'constraints': [
                    'Must prioritize safety over completeness',
                    'Must fail gracefully if overwhelmed',
                    'Must provide diagnostic information'
                ],
                'expected_behavior': 'Prioritized handling of multiple edge cases'
            })

        return tasks

    def get_boundary_summary(self) -> str:
        """Generate a summary of identified boundaries."""
        summary = "# Capability Boundary Analysis\n\n"

        for category, conditions in self.boundaries.items():
            if conditions:
                summary += f"## {category.replace('_', ' ').title()}\n\n"
                for bc in conditions:
                    summary += f"- **{bc.condition}** ({bc.severity})\n"
                summary += "\n"

        summary += f"## Boundary Task Coverage\n\n"
        summary += f"Generated {len(self.generate_boundary_tasks())} boundary-probing tasks\n"

        return summary


def integrate_boundary_tasks(
    standard_tasks: List,
    advanced_tasks: List,
    boundary_tasks: List
) -> Tuple[List, List]:
    """
    Integrate boundary tasks into training and test sets.

    New distribution:
    - Training (16 tasks): 6 standard + 4 advanced + 6 boundary
    - Test (10 tasks): 4 standard + 3 advanced + 3 boundary

    Args:
        standard_tasks: List of standard tasks
        advanced_tasks: List of advanced tasks
        boundary_tasks: List of boundary tasks

    Returns:
        Tuple of (training_tasks, test_tasks)
    """
    # Training set: 6 standard + 4 advanced + 6 boundary
    training = (
        standard_tasks[:6] +
        advanced_tasks[:4] +
        boundary_tasks[:6]
    )

    # Test set: 4 standard + 3 advanced + 3 boundary
    test = (
        standard_tasks[6:10] +
        advanced_tasks[4:7] +
        boundary_tasks[6:9]
    )

    return training, test


if __name__ == "__main__":
    # Test the boundary prober
    sample_skill = """
    ---
    name: test-skill
    ---

    # Test Skill

    ## Input
    - Must provide a valid file path
    - Input must not be empty
    - Maximum file size: 10MB

    ## Output
    - Generates JSON format output
    - Must complete within 30 seconds

    ## Dependencies
    - Requires network access to external API
    """

    prober = CapabilityBoundaryProber(sample_skill)
    boundaries = prober.analyze_skill_boundaries()

    print("Identified Boundaries:")
    for category, conditions in boundaries.items():
        if conditions:
            print(f"\n{category}:")
            for bc in conditions:
                print(f"  - {bc.condition} ({bc.severity})")

    print("\n" + "="*60)
    print(prober.get_boundary_summary())

    print("\n" + "="*60)
    print("Generated Boundary Tasks:")
    for i, task in enumerate(prober.generate_boundary_tasks(), 1):
        print(f"\n{i}. {task['title']} ({task['task_type']})")
        print(f"   Objective: {task['objective']}")
