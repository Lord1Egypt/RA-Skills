#!/usr/bin/env python3
"""
Task Decomposer - Execution Layer
Author: Socneo
Created with Claude Code
Version: 1.0.0

Complex task breakdown.
"""

from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum
import uuid

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class SubTask:
    """Represents a decomposed subtask."""
    id: str
    name: str
    description: str
    task_type: str
    estimated_duration: float  # in minutes
    dependencies: List[str]  # list of subtask IDs
    verification_criteria: List[str]
    required_skills: List[str]
    estimated_complexity: float  # 1-10 scale
    status: TaskStatus = TaskStatus.PENDING
    created_at: datetime = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    actual_duration: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}

@dataclass
class TaskDecompositionResult:
    """Result of task decomposition."""
    original_task: str
    subtasks: List[SubTask]
    total_estimated_duration: float
    critical_path: List[str]
    parallelizable_groups: List[List[str]]
    execution_order: List[str]
    complexity_score: float

class TaskDecomposer:
    """Intelligent task decomposition system."""

    def __init__(self):
        # Task decomposition patterns
        self.decomposition_patterns = {
            'skill_installation': {
                'pattern': ['pre_installation_check', 'dependency_resolution', 'download_files', 'installation', 'configuration', 'verification'],
                'subtasks': {
                    'pre_installation_check': {
                        'description': 'Check system compatibility and prerequisites',
                        'duration': 5,
                        'complexity': 3,
                        'skills': ['system_check', 'compatibility_analysis']
                    },
                    'dependency_resolution': {
                        'description': 'Resolve and install required dependencies',
                        'duration': 10,
                        'complexity': 5,
                        'skills': ['dependency_management', 'package_management']
                    },
                    'download_files': {
                        'description': 'Download required files and resources',
                        'duration': 15,
                        'complexity': 2,
                        'skills': ['network_operations', 'file_management']
                    },
                    'installation': {
                        'description': 'Install the main components',
                        'duration': 20,
                        'complexity': 6,
                        'skills': ['installation_procedures', 'system_integration']
                    },
                    'configuration': {
                        'description': 'Configure installed components',
                        'duration': 10,
                        'complexity': 4,
                        'skills': ['configuration_management', 'parameter_tuning']
                    },
                    'verification': {
                        'description': 'Verify successful installation',
                        'duration': 5,
                        'complexity': 3,
                        'skills': ['testing', 'validation', 'quality_assurance']
                    }
                }
            },
            'skill_audit': {
                'pattern': ['scan_dependencies', 'check_security', 'validate_compliance', 'performance_analysis', 'documentation_review'],
                'subtasks': {
                    'scan_dependencies': {
                        'description': 'Scan and analyze skill dependencies',
                        'duration': 8,
                        'complexity': 4,
                        'skills': ['dependency_analysis', 'security_scanning']
                    },
                    'check_security': {
                        'description': 'Perform security vulnerability assessment',
                        'duration': 15,
                        'complexity': 7,
                        'skills': ['security_analysis', 'vulnerability_scanning']
                    },
                    'validate_compliance': {
                        'description': 'Check compliance with policies and standards',
                        'duration': 12,
                        'complexity': 5,
                        'skills': ['compliance_checking', 'policy_validation']
                    },
                    'performance_analysis': {
                        'description': 'Analyze performance metrics and benchmarks',
                        'duration': 10,
                        'complexity': 6,
                        'skills': ['performance_testing', 'metrics_analysis']
                    },
                    'documentation_review': {
                        'description': 'Review and validate documentation quality',
                        'duration': 6,
                        'complexity': 3,
                        'skills': ['documentation_analysis', 'quality_assessment']
                    }
                }
            },
            'system_maintenance': {
                'pattern': ['system_scan', 'issue_detection', 'priority_assessment', 'repair_execution', 'verification'],
                'subtasks': {
                    'system_scan': {
                        'description': 'Comprehensive system health scan',
                        'duration': 5,
                        'complexity': 3,
                        'skills': ['system_monitoring', 'health_checking']
                    },
                    'issue_detection': {
                        'description': 'Detect and categorize system issues',
                        'duration': 8,
                        'complexity': 4,
                        'skills': ['problem_detection', 'issue_categorization']
                    },
                    'priority_assessment': {
                        'description': 'Assess issue priority and impact',
                        'duration': 5,
                        'complexity': 3,
                        'skills': ['priority_evaluation', 'impact_analysis']
                    },
                    'repair_execution': {
                        'description': 'Execute repairs based on priority',
                        'duration': 20,
                        'complexity': 7,
                        'skills': ['repair_procedures', 'system_operations']
                    },
                    'verification': {
                        'description': 'Verify repair effectiveness',
                        'duration': 5,
                        'complexity': 3,
                        'skills': ['validation', 'testing']
                    }
                }
            }
        }

        # Complexity assessment factors
        self.complexity_factors = {
            'technical_complexity': 0.3,
            'coordination_overhead': 0.25,
            'resource_requirements': 0.2,
            'risk_level': 0.15,
            'novelty': 0.1
        }

        # Task templates for common operations
        self.task_templates = {
            'file_operations': ['backup', 'validate', 'transform', 'verify'],
            'network_operations': ['connectivity_check', 'authentication', 'data_transfer', 'validation'],
            'data_processing': ['extract', 'transform', 'validate', 'load'],
            'system_operations': ['prepare', 'execute', 'monitor', 'cleanup']
        }

    def decompose_task(self, task_name: str, task_description: str, task_type: str = None, complexity_params: Dict[str, float] = None) -> TaskDecompositionResult:
        """Decompose a complex task into manageable subtasks."""

        # Identify task type if not provided
        if not task_type:
            task_type = self._identify_task_type(task_name, task_description)

        # Get decomposition pattern
        if task_type in self.decomposition_patterns:
            subtasks = self._create_subtasks_from_pattern(task_type, task_name, task_description)
        else:
            subtasks = self._create_generic_subtasks(task_name, task_description, complexity_params)

        # Establish dependencies
        self._establish_dependencies(subtasks)

        # Calculate execution metrics
        total_duration = sum(st.estimated_duration for st in subtasks)
        critical_path = self._calculate_critical_path(subtasks)
        parallel_groups = self._identify_parallel_groups(subtasks)
        execution_order = self._determine_execution_order(subtasks)
        complexity_score = self._calculate_complexity_score(subtasks, complexity_params)

        return TaskDecompositionResult(
            original_task=task_name,
            subtasks=subtasks,
            total_estimated_duration=total_duration,
            critical_path=critical_path,
            parallelizable_groups=parallel_groups,
            execution_order=execution_order,
            complexity_score=complexity_score
        )

    def _identify_task_type(self, task_name: str, task_description: str) -> str:
        """Identify the most appropriate task type based on name and description."""
        task_text = (task_name + " " + task_description).lower()

        # Check for skill-related tasks
        if any(keyword in task_text for keyword in ['install', 'skill', 'package', 'deploy']):
            return 'skill_installation'
        elif any(keyword in task_text for keyword in ['audit', 'review', 'check', 'validate']):
            return 'skill_audit'
        elif any(keyword in task_text for keyword in ['maintenance', 'repair', 'fix', 'update']):
            return 'system_maintenance'
        elif any(keyword in task_text for keyword in ['configure', 'setup', 'initialize']):
            return 'configuration'
        elif any(keyword in task_text for keyword in ['monitor', 'watch', 'track']):
            return 'monitoring'
        else:
            return 'general'

    def _create_subtasks_from_pattern(self, task_type: str, task_name: str, task_description: str) -> List[SubTask]:
        """Create subtasks based on predefined patterns."""
        pattern = self.decomposition_patterns[task_type]
        subtasks = []

        for i, step_name in enumerate(pattern['pattern']):
            step_config = pattern['subtasks'][step_name]

            subtask = SubTask(
                id=str(uuid.uuid4()),
                name=f"{task_name}_{step_name}",
                description=f"{step_config['description']} for {task_name}",
                task_type=step_name,
                estimated_duration=step_config['duration'],
                dependencies=[],
                verification_criteria=self._generate_verification_criteria(step_name),
                required_skills=step_config['skills'],
                estimated_complexity=step_config['complexity']
            )

            subtasks.append(subtask)

        return subtasks

    def _create_generic_subtasks(self, task_name: str, task_description: str, complexity_params: Dict[str, float] = None) -> List[SubTask]:
        """Create generic subtasks for unknown task types."""
        # Use basic decomposition strategy
        base_subtasks = [
            SubTask(
                id=str(uuid.uuid4()),
                name=f"{task_name}_preparation",
                description=f"Prepare for {task_name}",
                task_type="preparation",
                estimated_duration=5,
                dependencies=[],
                verification_criteria=["All prerequisites met", "Environment ready"],
                required_skills=["preparation", "setup"],
                estimated_complexity=2
            ),
            SubTask(
                id=str(uuid.uuid4()),
                name=f"{task_name}_execution",
                description=f"Execute {task_name}",
                task_type="execution",
                estimated_duration=15,
                dependencies=[],
                verification_criteria=["Task completed successfully", "No errors occurred"],
                required_skills=["execution", "implementation"],
                estimated_complexity=5
            ),
            SubTask(
                id=str(uuid.uuid4()),
                name=f"{task_name}_verification",
                description=f"Verify {task_name} completion",
                task_type="verification",
                estimated_duration=5,
                dependencies=[],
                verification_criteria=["Results meet expectations", "Quality standards met"],
                required_skills=["verification", "testing"],
                estimated_complexity=3
            )
        ]

        return base_subtasks

    def _generate_verification_criteria(self, step_name: str) -> List[str]:
        """Generate verification criteria for a subtask step."""
        criteria_map = {
            'pre_installation_check': [
                "System meets minimum requirements",
                "No conflicting software detected",
                "Required permissions available"
            ],
            'dependency_resolution': [
                "All dependencies identified",
                "Dependencies successfully installed",
                "No version conflicts detected"
            ],
            'download_files': [
                "All files downloaded successfully",
                "File integrity verified",
                "Downloads completed within timeout"
            ],
            'installation': [
                "Installation completed without errors",
                "All components properly registered",
                "Installation directory structure correct"
            ],
            'configuration': [
                "Configuration files created",
                "Settings applied correctly",
                "Configuration validated"
            ],
            'verification': [
                "Functionality tests passed",
                "Performance within expected range",
                "No errors in logs"
            ]
        }

        return criteria_map.get(step_name, ["Step completed successfully"])

    def _establish_dependencies(self, subtasks: List[SubTask]):
        """Establish dependencies between subtasks."""
        # Create dependency mapping
        task_type_map = {st.task_type: st for st in subtasks}

        # Define dependency rules
        dependency_rules = {
            'dependency_resolution': ['pre_installation_check'],
            'download_files': ['dependency_resolution'],
            'installation': ['download_files'],
            'configuration': ['installation'],
            'verification': ['configuration'],
            'issue_detection': ['system_scan'],
            'priority_assessment': ['issue_detection'],
            'repair_execution': ['priority_assessment'],
            'execution': ['preparation'],
            'verification': ['execution']
        }

        # Apply dependency rules
        for subtask in subtasks:
            if subtask.task_type in dependency_rules:
                for dep_type in dependency_rules[subtask.task_type]:
                    if dep_type in task_type_map:
                        dep_task = task_type_map[dep_type]
                        subtask.dependencies.append(dep_task.id)

    def _calculate_critical_path(self, subtasks: List[SubTask]) -> List[str]:
        """Calculate the critical path through the task dependencies."""
        # Create task lookup
        task_map = {st.id: st for st in subtasks}

        def calculate_path_duration(task_id: str, visited: Set[str] = None) -> float:
            if visited is None:
                visited = set()

            if task_id in visited:
                return 0  # Avoid circular dependencies

            visited.add(task_id)
            task = task_map[task_id]

            if not task.dependencies:
                return task.estimated_duration

            max_dependency_duration = 0
            for dep_id in task.dependencies:
                if dep_id in task_map:
                    dep_duration = calculate_path_duration(dep_id, visited.copy())
                    max_dependency_duration = max(max_dependency_duration, dep_duration)

            return task.estimated_duration + max_dependency_duration

        # Find the path with maximum duration
        max_duration = 0
        critical_path = []

        for task in subtasks:
            duration = calculate_path_duration(task.id)
            if duration > max_duration:
                max_duration = duration
                # Reconstruct the critical path
                critical_path = self._reconstruct_critical_path(task.id, task_map)

        return critical_path

    def _reconstruct_critical_path(self, task_id: str, task_map: Dict[str, SubTask]) -> List[str]:
        """Reconstruct the critical path ending at the given task."""
        if task_id not in task_map:
            return []

        task = task_map[task_id]
        if not task.dependencies:
            return [task_id]

        # Find the dependency with the longest path
        longest_path = []
        max_length = 0

        for dep_id in task.dependencies:
            if dep_id in task_map:
                dep_path = self._reconstruct_critical_path(dep_id, task_map)
                if len(dep_path) > max_length:
                    max_length = len(dep_path)
                    longest_path = dep_path

        return longest_path + [task_id]

    def _identify_parallel_groups(self, subtasks: List[SubTask]) -> List[List[str]]:
        """Identify groups of subtasks that can be executed in parallel."""
        # Create dependency graph
        task_map = {st.id: st for st in subtasks}
        in_degree = {st.id: len(st.dependencies) for st in subtasks}

        parallel_groups = []
        remaining_tasks = set(task_map.keys())

        while remaining_tasks:
            # Find tasks with no remaining dependencies
            current_group = []
            for task_id in list(remaining_tasks):
                if in_degree[task_id] == 0:
                    current_group.append(task_id)

            if not current_group:
                break  # No more parallelizable tasks

            parallel_groups.append(current_group)

            # Remove current group from remaining tasks and update dependencies
            for task_id in current_group:
                remaining_tasks.remove(task_id)
                # Reduce in-degree for dependent tasks
                for other_task in subtasks:
                    if task_id in other_task.dependencies:
                        in_degree[other_task.id] -= 1

        return parallel_groups

    def _determine_execution_order(self, subtasks: List[SubTask]) -> List[str]:
        """Determine the optimal execution order for subtasks."""
        return self._identify_parallel_groups(subtasks)[0] if self._identify_parallel_groups(subtasks) else [st.id for st in subtasks]

    def _calculate_complexity_score(self, subtasks: List[SubTask], complexity_params: Dict[str, float] = None) -> float:
        """Calculate overall complexity score for the task decomposition."""
        if not subtasks:
            return 0.0

        # Base complexity from subtask complexities
        avg_complexity = sum(st.estimated_complexity for st in subtasks) / len(subtasks)

        # Adjust based on number of subtasks
        size_factor = min(len(subtasks) / 10.0, 2.0)  # Cap at 2x multiplier

        # Adjust based on dependencies
        total_dependencies = sum(len(st.dependencies) for st in subtasks)
        dependency_factor = 1 + (total_dependencies / (len(subtasks) * 2))

        # Apply custom complexity parameters if provided
        custom_factor = 1.0
        if complexity_params:
            technical_factor = complexity_params.get('technical_complexity', 1.0)
            coordination_factor = complexity_params.get('coordination_overhead', 1.0)
            resource_factor = complexity_params.get('resource_requirements', 1.0)
            risk_factor = complexity_params.get('risk_level', 1.0)
            novelty_factor = complexity_params.get('novelty', 1.0)

            custom_factor = (
                technical_factor * self.complexity_factors['technical_complexity'] +
                coordination_factor * self.complexity_factors['coordination_overhead'] +
                resource_factor * self.complexity_factors['resource_requirements'] +
                risk_factor * self.complexity_factors['risk_level'] +
                novelty_factor * self.complexity_factors['novelty']
            )

        final_complexity = avg_complexity * size_factor * dependency_factor * custom_factor
        return min(final_complexity, 10.0)  # Cap at 10

    def optimize_decomposition(self, decomposition: TaskDecompositionResult) -> TaskDecompositionResult:
        """Optimize the task decomposition for better efficiency."""
        # Merge very small tasks
        small_task_threshold = 3  # minutes
        small_tasks = [st for st in decomposition.subtasks if st.estimated_duration < small_task_threshold]

        if len(small_tasks) > 1:
            # Group small tasks by type
            task_groups = {}
            for task in small_tasks:
                if task.task_type not in task_groups:
                    task_groups[task.task_type] = []
                task_groups[task.task_type].append(task)

            # Merge tasks within groups
            optimized_subtasks = [st for st in decomposition.subtasks if st.estimated_duration >= small_task_threshold]

            for task_type, tasks in task_groups.items():
                if len(tasks) > 1:
                    merged_task = self._merge_subtasks(tasks, task_type)
                    optimized_subtasks.append(merged_task)
                else:
                    optimized_subtasks.extend(tasks)

            decomposition.subtasks = optimized_subtasks

        # Recalculate metrics
        decomposition.total_estimated_duration = sum(st.estimated_duration for st in decomposition.subtasks)
        decomposition.critical_path = self._calculate_critical_path(decomposition.subtasks)
        decomposition.parallelizable_groups = self._identify_parallel_groups(decomposition.subtasks)

        return decomposition

    def _merge_subtasks(self, tasks: List[SubTask], merged_type: str) -> SubTask:
        """Merge multiple subtasks into a single task."""
        total_duration = sum(st.estimated_duration for st in tasks)
        avg_complexity = sum(st.estimated_complexity for st in tasks) / len(tasks)

        all_dependencies = set()
        for task in tasks:
            all_dependencies.update(task.dependencies)

        all_criteria = []
        for task in tasks:
            all_criteria.extend(task.verification_criteria)

        all_skills = set()
        for task in tasks:
            all_skills.update(task.required_skills)

        return SubTask(
            id=str(uuid.uuid4()),
            name=f"merged_{merged_type}_tasks",
            description=f"Merged {len(tasks)} {merged_type} tasks",
            task_type=f"merged_{merged_type}",
            estimated_duration=total_duration,
            dependencies=list(all_dependencies),
            verification_criteria=all_criteria,
            required_skills=list(all_skills),
            estimated_complexity=avg_complexity
        )

def demo_task_decomposer():
    """Demonstrate the task decomposer."""
    decomposer = TaskDecomposer()

    # Test skill installation decomposition
    print("Task Decomposition Demo")
    print("=" * 60)

    task_name = "Install Advanced Analytics Skill"
    task_description = "Install and configure the advanced analytics skill for data processing"

    result = decomposer.decompose_task(task_name, task_description, "skill_installation")

    print(f"Original Task: {result.original_task}")
    print(f"Total Estimated Duration: {result.total_estimated_duration} minutes")
    print(f"Complexity Score: {result.complexity_score:.2f}/10")

    print(f"\nSubtasks ({len(result.subtasks)}):")
    for i, subtask in enumerate(result.subtasks, 1):
        print(f"{i}. {subtask.name}")
        print(f"   Description: {subtask.description}")
        print(f"   Duration: {subtask.estimated_duration} min")
        print(f"   Complexity: {subtask.estimated_complexity}/10")
        print(f"   Dependencies: {len(subtask.dependencies)}")
        print(f"   Skills: {', '.join(subtask.required_skills)}")

    print(f"\nCritical Path: {' -> '.join(result.critical_path)}")
    print(f"Parallel Groups: {len(result.parallelizable_groups)} groups")

if __name__ == "__main__":
    demo_task_decomposer()
