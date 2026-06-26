"""
GRPO Optimizer for Skills-Coach v2.3.1

Implements training-free Group Relative Policy Optimization to improve skill prompts.
Iteratively generates candidate variants, executes them on training tasks, and selects
the best performer based on relative rewards.

v1.2.0: Added multi-level optimization (SKILL.md + code + config)
"""

import os
import json
import time
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import statistics

# Import multi-level optimizer for code-level optimization
try:
    from multi_level_optimizer import MultiLevelOptimizer
    MULTI_LEVEL_AVAILABLE = True
except ImportError:
    MULTI_LEVEL_AVAILABLE = False
    print("Warning: multi_level_optimizer not available, code optimization disabled")


@dataclass
class TaskScore:
    """Score for a single task execution."""
    task_id: str
    score: int
    total: int
    passed: bool
    criteria_results: List[Dict[str, Any]]
    execution_details: Optional[Dict[str, Any]] = None


@dataclass
class VariantPerformance:
    """Performance metrics for a skill variant."""
    variant_id: str
    mutations: List[str]
    task_scores: List[TaskScore]
    total_score: int
    total_possible: int
    percentage: float
    relative_reward: float = 0.0


@dataclass
class OptimizationIteration:
    """Record of a single optimization iteration."""
    iteration: int
    variants: List[VariantPerformance]
    selected_variant_id: str
    selection_rationale: str
    timestamp: str


class GRPOOptimizer:
    """Training-free GRPO optimizer for skill prompts."""

    def __init__(
        self,
        target_skill_path: str,
        training_tasks_dir: str = "tasks/train",
        output_dir: str = ".",
        num_variants: int = 4,
        min_iterations: int = 3,
        max_iterations: int = 10,
        early_stop_patience: int = 2,
        config: Optional[Dict] = None
    ):
        self.target_skill_path = Path(target_skill_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # If training_tasks_dir is relative, make it relative to output_dir
        training_tasks_path = Path(training_tasks_dir)
        if not training_tasks_path.is_absolute():
            self.training_tasks_dir = self.output_dir / training_tasks_path
        else:
            self.training_tasks_dir = training_tasks_path

        self.num_variants = num_variants
        self.min_iterations = min_iterations
        self.max_iterations = max_iterations
        self.early_stop_patience = early_stop_patience

        # Load config
        self.config = config or self._load_config()

        # Check GRPO execution mode (v1.4.0)
        self.execution_mode = self.config.get('grpo_execution', {}).get('mode', 'simulated')
        if self.execution_mode == 'real':
            print("✓ GRPO real execution mode enabled (slower but accurate)")
        else:
            print("✓ GRPO simulated execution mode (fast)")

        # Initialize multi-level optimizer if enabled
        self.ml_optimizer = None
        if MULTI_LEVEL_AVAILABLE and 'code' in self.config.get('grpo', {}).get('optimization_levels', ['skill_md']):
            self.ml_optimizer = MultiLevelOptimizer(self.target_skill_path)
            print("✓ Multi-level optimizer enabled (SKILL.md + code)")

        self.original_skill_content = ""
        self.current_best_content = ""
        self.current_best_score = 0
        self.iterations: List[OptimizationIteration] = []
        self.no_improvement_count = 0
        self.baseline_scores: List[TaskScore] = []
        self._execution_context: Dict[str, Any] = {}

    def _load_config(self) -> Dict:
        """Load configuration from config.yaml."""
        config_path = Path(__file__).parent.parent.parent / "config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return {
            'grpo': {
                'optimization_levels': ['skill_md'],
                'num_variants': 4,
                'min_iterations': 3,
                'max_iterations': 10
            }
        }

    def load_original_skill(self) -> bool:
        """Load the original SKILL.md content."""
        skill_path = self.target_skill_path / "SKILL.md"

        if not skill_path.exists():
            print(f"ERROR: SKILL.md not found at {skill_path}")
            return False

        with open(skill_path, 'r', encoding='utf-8') as f:
            self.original_skill_content = f.read()
            self.current_best_content = self.original_skill_content

        print(f"✓ Loaded original SKILL.md from {skill_path}")
        return True

    def load_training_tasks(self) -> List[Dict]:
        """Load all training tasks."""
        tasks = []

        for task_dir in sorted(self.training_tasks_dir.glob("task_*")):
            task_md = task_dir / "task.md"
            speccheck_md = task_dir / "speccheck.md"

            if task_md.exists() and speccheck_md.exists():
                with open(task_md, 'r', encoding='utf-8') as f:
                    task_content = f.read()
                with open(speccheck_md, 'r', encoding='utf-8') as f:
                    speccheck_content = f.read()

                tasks.append({
                    "task_id": task_dir.name,
                    "task_dir": task_dir,
                    "task_content": task_content,
                    "speccheck_content": speccheck_content
                })

        print(f"✓ Loaded {len(tasks)} training tasks")
        return tasks

    def compute_baseline_score(self, training_tasks: List[Dict]) -> int:
        """Execute original skill on all training tasks and compute baseline score."""
        print("\n=== Computing Baseline Score ===")

        self._execution_context = {'phase': 'baseline'}
        baseline_scores = []
        for task in training_tasks:
            score = self.execute_and_score_task(
                self.original_skill_content,
                task
            )
            baseline_scores.append(score)
            print(f"  {task['task_id']}: {score.score}/{score.total}")

        self.baseline_scores = baseline_scores
        total_score = sum(s.score for s in baseline_scores)
        total_possible = sum(s.total for s in baseline_scores)
        percentage = (total_score / total_possible * 100) if total_possible > 0 else 0

        self.current_best_score = total_score
        self._execution_context = {}

        print(f"\n✓ Baseline: {total_score}/{total_possible} ({percentage:.1f}%)")
        return total_score

    def generate_variants(self, iteration: int, training_tasks: List[Dict]) -> List[Tuple[str, Dict]]:
        """
        Generate N candidate variants of the current best SKILL.md (and optionally code).

        Args:
            iteration: Current iteration number
            training_tasks: List of training task data

        Returns:
            List of tuples: (variant_skill_md_content, variant_metadata)
            variant_metadata includes: {'mutations': [...], 'code_changes': {...}}
        """
        variants = []
        mutations_applied = []

        # Analyze previous iteration failures if available
        failure_patterns = []
        if self.iterations:
            last_iter = self.iterations[-1]
            best_perf = max(last_iter.variants, key=lambda v: v.total_score)

            # Identify low-scoring tasks
            for task_score in best_perf.task_scores:
                if task_score.score < task_score.total * 0.7:  # Less than 70%
                    failure_patterns.append({
                        'task_id': task_score.task_id,
                        'score': task_score.score,
                        'total': task_score.total,
                        'criteria': task_score.criteria_results
                    })

        # Strategy: Generate more diverse mutations to avoid overfitting
        # IMPORTANT: Always apply mutations, don't fall back to "Minimal change"

        # v1.2.0: Generate code-level variants if multi-level optimizer is available
        code_variants = []
        if self.ml_optimizer:
            code_variants = self.ml_optimizer.generate_code_variants(iteration, failure_patterns)
            print(f"✓ Generated {len(code_variants)} code-level variants")

        # Variant 1: Add explicit validation guidance
        variant1 = self.current_best_content
        mutation1 = []

        # Always add validation section if not present
        if "validation" not in variant1.lower() and iteration <= 3:
            # Find a good insertion point (after description, before main content)
            lines = variant1.split('\n')
            insert_idx = 10  # Default fallback
            for i, line in enumerate(lines):
                if line.startswith('##') and i > 5:  # First section after frontmatter
                    insert_idx = i
                    break

            validation_section = "\n## Input Validation\n\nBefore processing, verify:\n- All required inputs are provided\n- File paths exist and are accessible\n- Configuration values are within valid ranges\n- Dependencies are available\n\n"
            lines.insert(insert_idx, validation_section)
            variant1 = '\n'.join(lines)
            mutation1.append(f"Added input validation section at line {insert_idx}")
        else:
            # Strengthen existing validation
            variant1 = variant1.replace("should validate", "MUST validate")
            variant1 = variant1.replace("may check", "MUST check")
            mutation1.append("Strengthened validation language (should→MUST)")

        variants.append((variant1, {'mutations': mutation1, 'code_changes': {}}))
        mutations_applied.append(mutation1)

        # Variant 2: Add error handling guidance OR apply code-level mutation
        variant2 = self.current_best_content
        mutation2 = []
        code_changes2 = {}

        if code_variants and len(code_variants) > 0:
            # Use first code variant
            code_variant = code_variants[0]
            variant2 = code_variant.get('skill_md', variant2)
            code_changes2 = code_variant.get('code_changes', {})
            mutation2.append(f"Code-level: {code_variant.get('description', 'Applied code mutation')}")
        elif "error" not in variant2.lower() or iteration >= 2:
            # Add error handling section
            error_section = "\n## Error Handling\n\n**Core Principles**:\n1. Never crash - catch and log all errors\n2. Provide actionable error messages\n3. Attempt recovery when possible\n4. Return partial results rather than nothing\n\n"
            variant2 += error_section
            mutation2.append("Added error handling principles section")
        else:
            # Enhance existing error handling
            variant2 = variant2.replace("handle errors", "gracefully handle errors with clear messages")
            mutation2.append("Enhanced error handling descriptions")

        variants.append((variant2, {'mutations': mutation2, 'code_changes': code_changes2}))
        mutations_applied.append(mutation2)

        # Variant 3: Add concrete examples OR apply second code-level mutation
        variant3 = self.current_best_content
        mutation3 = []
        code_changes3 = {}

        if code_variants and len(code_variants) > 1:
            # Use second code variant
            code_variant = code_variants[1]
            variant3 = code_variant.get('skill_md', variant3)
            code_changes3 = code_variant.get('code_changes', {})
            mutation3.append(f"Code-level: {code_variant.get('description', 'Applied code mutation')}")
        elif "example" not in variant3.lower():
            example_section = "\n## Usage Example\n\n```bash\n# Basic usage\n<command-to-invoke-skill> <typical-arguments>\n\n# Expected output:\n# <sample-output>\n```\n\n"
            variant3 += example_section
            mutation3.append("Added usage example section")
        else:
            # Add more detail to existing examples
            variant3 = variant3.replace("Example:", "Example (with expected output):")
            mutation3.append("Enhanced existing examples with output expectations")

        variants.append((variant3, {'mutations': mutation3, 'code_changes': code_changes3}))
        mutations_applied.append(mutation3)

        # Variant 4: Strengthen constraints and rules
        variant4 = self.current_best_content
        mutation4 = []
        code_changes4 = {}

        # Make language more prescriptive
        changes = 0
        if "should" in variant4:
            variant4 = variant4.replace("should ", "MUST ")
            changes += variant4.count("MUST ") - self.current_best_content.count("MUST ")
            mutation4.append(f"Strengthened {changes} 'should' statements to 'MUST'")

        if "may" in variant4:
            variant4 = variant4.replace("may ", "SHOULD ")
            changes = variant4.count("SHOULD ") - self.current_best_content.count("SHOULD ")
            mutation4.append(f"Strengthened {changes} 'may' statements to 'SHOULD'")

        if not mutation4:
            # Add constraints section
            constraints_section = "\n## Constraints\n\n- MUST complete within reasonable time (< 5 minutes)\n- MUST handle missing or invalid inputs gracefully\n- MUST produce output in specified format\n- SHOULD log progress for long-running operations\n\n"
            variant4 += constraints_section
            mutation4.append("Added explicit constraints section")

        variants.append((variant4, {'mutations': mutation4, 'code_changes': code_changes4}))
        mutations_applied.append(mutation4)

        # Store mutations for logging
        self._current_mutations = mutations_applied

        return variants[:self.num_variants]

    def execute_and_score_task(self, skill_content: str, task: Dict) -> TaskScore:
        """
        Execute a skill variant on a single task and score the output.

        Args:
            skill_content: The SKILL.md content to execute
            task: Task data dictionary

        Returns:
            TaskScore object with results
        """
        # Parse speccheck criteria
        criteria = self.parse_speccheck_criteria(task['speccheck_content'])

        # Check execution mode
        if self.execution_mode == 'real':
            # Real execution mode - actually run the command
            return self._execute_real(skill_content, task, criteria)
        else:
            # Simulated execution mode - fast deterministic scoring
            return self._execute_simulated(skill_content, task, criteria)

    def _execute_real(self, skill_content: str, task: Dict, criteria: List[str]) -> TaskScore:
        """Execute task with real command execution."""
        import re
        import shutil
        import subprocess
        import tempfile

        task_id = task['task_id']
        task_dir = task['task_dir']
        artifact_dir = self._get_execution_artifact_dir(task_id)
        task_md_path = Path(task_dir) / "task.md"

        command = None
        if task_md_path.exists():
            with open(task_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
                match = re.search(r'```(?:bash|shell|sh)\n(.*?)\n```', content, re.DOTALL)
                if match:
                    command = match.group(1).strip()

        if not command:
            reason = f"No executable command found in {task_md_path.name}"
            simulated_score = self._execute_simulated(skill_content, task, criteria)
            metadata = self._build_execution_details(
                mode_requested='real',
                actual_mode='simulated',
                task=task,
                artifact_dir=artifact_dir,
                reason=reason,
            )
            paths = self._write_execution_artifacts(
                artifact_dir,
                command=None,
                metadata=metadata,
                stdout="",
                stderr=reason + "\n",
            )
            metadata.update(paths)
            with open(artifact_dir / 'result.json', 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            simulated_score.execution_details = metadata
            return simulated_score

        with tempfile.TemporaryDirectory() as temp_skill_dir:
            temp_skill_path = Path(temp_skill_dir)

            if self.target_skill_path.is_dir():
                for item in self.target_skill_path.iterdir():
                    if item.is_file():
                        shutil.copy2(item, temp_skill_path / item.name)
                    elif item.is_dir() and item.name not in ['.git', '__pycache__', '.pytest_cache']:
                        shutil.copytree(item, temp_skill_path / item.name, dirs_exist_ok=True)

            skill_path = temp_skill_path / "SKILL.md"
            with open(skill_path, 'w', encoding='utf-8') as f:
                f.write(skill_content)

            try:
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=self.config.get('execution', {}).get('timeout_per_task', 300),
                    cwd=temp_skill_path
                )

                artifact_dir.mkdir(parents=True, exist_ok=True)
                for item in temp_skill_path.iterdir():
                    if item.name in ['SKILL.md', '.git', '__pycache__', '.pytest_cache']:
                        continue
                    destination = artifact_dir / item.name
                    if item.is_file():
                        shutil.copy2(item, destination)
                    elif item.is_dir():
                        shutil.copytree(item, destination, dirs_exist_ok=True)

                score = 0
                total = len(criteria)
                criteria_results = []

                for criterion in criteria:
                    satisfied = False
                    evidence = ""
                    criterion_lower = criterion.lower()

                    if "executes without errors" in criterion_lower or "command executes" in criterion_lower:
                        satisfied = result.returncode == 0
                        evidence = f"Exit code: {result.returncode}"
                    elif "output is generated" in criterion_lower or "produces output" in criterion_lower:
                        satisfied = len(result.stdout) > 0 or len(list(artifact_dir.glob('*'))) > 0
                        evidence = f"Stdout: {len(result.stdout)} bytes, Files: {len(list(artifact_dir.glob('*')))}"
                    elif "format" in criterion_lower or "valid" in criterion_lower:
                        satisfied = len(result.stdout) > 100
                        evidence = f"Output length: {len(result.stdout)} bytes"
                    elif "data" in criterion_lower or "content" in criterion_lower:
                        satisfied = len(result.stdout) > 200
                        evidence = f"Substantial output: {len(result.stdout)} bytes"
                    elif "complex" in criterion_lower:
                        satisfied = result.returncode == 0 and len(result.stdout) > 500
                        evidence = f"Complex handling: exit={result.returncode}, output={len(result.stdout)} bytes"
                    else:
                        satisfied = result.returncode == 0
                        evidence = f"Command succeeded: {result.returncode == 0}"

                    if satisfied:
                        score += 1

                    criteria_results.append({
                        'criterion': criterion,
                        'satisfied': satisfied,
                        'evidence': evidence
                    })

                passed = score >= (total * 0.7)
                metadata = self._build_execution_details(
                    mode_requested='real',
                    actual_mode='real',
                    task=task,
                    artifact_dir=artifact_dir,
                    command=command,
                    returncode=result.returncode,
                )
                paths = self._write_execution_artifacts(
                    artifact_dir,
                    command=command,
                    metadata=metadata,
                    stdout=result.stdout,
                    stderr=result.stderr,
                )
                metadata.update(paths)
                with open(artifact_dir / 'result.json', 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                return TaskScore(
                    task_id=task_id,
                    score=score,
                    total=total,
                    passed=passed,
                    criteria_results=criteria_results,
                    execution_details=metadata
                )

            except subprocess.TimeoutExpired as e:
                criteria_results = [{
                    'criterion': c,
                    'satisfied': False,
                    'evidence': 'Command timed out'
                } for c in criteria]

                metadata = self._build_execution_details(
                    mode_requested='real',
                    actual_mode='real',
                    task=task,
                    artifact_dir=artifact_dir,
                    command=command,
                    reason='Command timed out',
                    timed_out=True,
                )
                paths = self._write_execution_artifacts(
                    artifact_dir,
                    command=command,
                    metadata=metadata,
                    stdout=e.stdout or "",
                    stderr=e.stderr or "",
                )
                metadata.update(paths)
                with open(artifact_dir / 'result.json', 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                return TaskScore(
                    task_id=task_id,
                    score=0,
                    total=len(criteria),
                    passed=False,
                    criteria_results=criteria_results,
                    execution_details=metadata
                )
            except Exception as e:
                criteria_results = [{
                    'criterion': c,
                    'satisfied': False,
                    'evidence': f'Execution error: {str(e)}'
                } for c in criteria]

                metadata = self._build_execution_details(
                    mode_requested='real',
                    actual_mode='real',
                    task=task,
                    artifact_dir=artifact_dir,
                    command=command,
                    reason=f'Execution error: {str(e)}',
                )
                paths = self._write_execution_artifacts(
                    artifact_dir,
                    command=command,
                    metadata=metadata,
                    stdout="",
                    stderr=f'{str(e)}\n',
                )
                metadata.update(paths)
                with open(artifact_dir / 'result.json', 'w', encoding='utf-8') as f:
                    json.dump(metadata, f, indent=2, ensure_ascii=False)

                return TaskScore(
                    task_id=task_id,
                    score=0,
                    total=len(criteria),
                    passed=False,
                    criteria_results=criteria_results,
                    execution_details=metadata
                )

    def _sanitize_path_component(self, value: str) -> str:
        """Make a safe directory name for execution artifacts."""
        import re

        sanitized = re.sub(r'[^A-Za-z0-9._-]+', '_', value)
        return sanitized.strip('_') or "unknown"

    def _get_execution_artifact_dir(self, task_id: str) -> Path:
        """Return the artifact directory for the current execution context."""
        base_dir = self.output_dir / "grpo_exec"
        iteration = self._execution_context.get('iteration')
        phase = self._execution_context.get('phase', 'run')
        variant_id = self._execution_context.get('variant_id')

        if iteration is not None:
            base_dir = base_dir / f"iteration_{int(iteration):03d}"

        if variant_id:
            base_dir = base_dir / self._sanitize_path_component(variant_id)
        else:
            base_dir = base_dir / self._sanitize_path_component(phase)

        return base_dir / task_id

    def _build_execution_details(
        self,
        *,
        mode_requested: str,
        actual_mode: str,
        task: Dict,
        artifact_dir: Path,
        command: Optional[str] = None,
        reason: Optional[str] = None,
        returncode: Optional[int] = None,
        stdout_path: Optional[str] = None,
        stderr_path: Optional[str] = None,
        metadata_path: Optional[str] = None,
        timed_out: bool = False
    ) -> Dict[str, Any]:
        """Build a consistent execution metadata payload."""
        details: Dict[str, Any] = {
            'mode_requested': mode_requested,
            'actual_mode': actual_mode,
            'task_id': task['task_id'],
            'task_dir': str(task['task_dir']),
            'artifact_dir': str(artifact_dir),
            'timed_out': timed_out,
        }

        if command is not None:
            details['command'] = command
        if reason:
            details['reason'] = reason
        if returncode is not None:
            details['returncode'] = returncode
        if stdout_path:
            details['stdout_path'] = stdout_path
        if stderr_path:
            details['stderr_path'] = stderr_path
        if metadata_path:
            details['metadata_path'] = metadata_path

        iteration = self._execution_context.get('iteration')
        variant_id = self._execution_context.get('variant_id')
        phase = self._execution_context.get('phase')
        if iteration is not None:
            details['iteration'] = iteration
        if variant_id:
            details['variant_id'] = variant_id
        if phase:
            details['phase'] = phase

        return details

    def _write_execution_artifacts(
        self,
        artifact_dir: Path,
        *,
        command: Optional[str],
        metadata: Dict[str, Any],
        stdout: str = "",
        stderr: str = ""
    ) -> Dict[str, str]:
        """Persist execution artifacts for observability."""
        artifact_dir.mkdir(parents=True, exist_ok=True)
        paths: Dict[str, str] = {}

        if command is not None:
            command_path = artifact_dir / 'command.sh'
            with open(command_path, 'w', encoding='utf-8') as f:
                f.write(command)
                if not command.endswith('\n'):
                    f.write('\n')
            paths['command_path'] = str(command_path)

        stdout_path = artifact_dir / 'stdout.txt'
        with open(stdout_path, 'w', encoding='utf-8') as f:
            f.write(stdout)
        paths['stdout_path'] = str(stdout_path)

        stderr_path = artifact_dir / 'stderr.txt'
        with open(stderr_path, 'w', encoding='utf-8') as f:
            f.write(stderr)
        paths['stderr_path'] = str(stderr_path)

        metadata_path = artifact_dir / 'result.json'
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        paths['metadata_path'] = str(metadata_path)

        return paths

    def _execute_simulated(self, skill_content: str, task: Dict, criteria: List[str]) -> TaskScore:
        """Execute task with simulated scoring (fast, deterministic)."""
        import random
        import hashlib

        task_id = task['task_id']

        # IMPORTANT: Use deterministic seed for reproducibility
        seed_string = skill_content + task_id
        seed_hash = hashlib.md5(seed_string.encode()).hexdigest()
        seed = int(seed_hash[:8], 16)  # Use first 8 hex chars as seed
        random.seed(seed)

        score = 0
        total = len(criteria)
        criteria_results = []

        # Simple heuristic scoring based on skill content
        for criterion in criteria:
            satisfied = False

            # Check if skill addresses common issues
            if "error" in criterion.lower() and "error handling" in skill_content.lower():
                satisfied = True
            elif "output" in criterion.lower() and "save" in skill_content.lower():
                satisfied = True
            elif "markdown" in criterion.lower() and "markdown" in skill_content.lower():
                satisfied = True
            elif "category" in criterion.lower() and "category" in skill_content.lower():
                satisfied = True
            elif "feed" in criterion.lower() and "feed" in skill_content.lower():
                satisfied = True
            else:
                # Default: 60% pass rate for unmatched criteria
                # Now deterministic based on seed
                satisfied = random.random() > 0.4

            if satisfied:
                score += 1

            criteria_results.append({
                'criterion': criterion,
                'satisfied': satisfied,
                'evidence': 'Simulated check based on skill content'
            })

        passed = score >= (total * 0.7)

        details = self._build_execution_details(
            mode_requested=self.execution_mode,
            actual_mode='simulated',
            task=task,
            artifact_dir=self._get_execution_artifact_dir(task_id),
            reason='Deterministic simulated scoring based on skill content',
        )

        return TaskScore(
            task_id=task_id,
            score=score,
            total=total,
            passed=passed,
            criteria_results=criteria_results,
            execution_details=details
        )

    def evaluate_variants(
        self,
        variants: List[Tuple[str, Dict]],
        training_tasks: List[Dict],
        iteration: int
    ) -> List[VariantPerformance]:
        """Execute and score all variants on all training tasks."""
        print(f"\n=== Evaluating {len(variants)} Variants ===")

        performances = []

        for i, (variant_content, variant_metadata) in enumerate(variants):
            variant_id = f"v{iteration}-{chr(97 + i)}"  # v1-a, v1-b, etc.
            print(f"\nVariant {variant_id}:")

            self._execution_context = {
                'phase': 'variant_evaluation',
                'iteration': iteration,
                'variant_id': variant_id,
            }

            # Apply code changes if present
            if variant_metadata.get('code_changes'):
                print(f"  Code changes: {len(variant_metadata['code_changes'])} files")

            task_scores = []
            for task in training_tasks:
                score = self.execute_and_score_task(variant_content, task)
                task_scores.append(score)
                print(f"  {task['task_id']}: {score.score}/{score.total}")

            total_score = sum(s.score for s in task_scores)
            total_possible = sum(s.total for s in task_scores)
            percentage = (total_score / total_possible * 100) if total_possible > 0 else 0

            # Get mutations from metadata
            mutations = variant_metadata.get('mutations', [f"Mutation {i+1}"])

            performance = VariantPerformance(
                variant_id=variant_id,
                mutations=mutations,
                task_scores=task_scores,
                total_score=total_score,
                total_possible=total_possible,
                percentage=percentage
            )
            performances.append(performance)

            print(f"  Total: {total_score}/{total_possible} ({percentage:.1f}%)")

        self._execution_context = {}
        return performances

    def compute_relative_rewards(self, performances: List[VariantPerformance]):
        """Compute GRPO relative rewards for each variant."""
        scores = [p.total_score for p in performances]
        mean_score = statistics.mean(scores)
        std_score = statistics.stdev(scores) if len(scores) > 1 else 1.0

        for performance in performances:
            raw_reward = performance.total_score - mean_score
            performance.relative_reward = raw_reward / std_score if std_score > 0 else 0.0

        print(f"\nRelative Rewards (μ={mean_score:.1f}, σ={std_score:.1f}):")
        for p in performances:
            print(f"  {p.variant_id}: {p.relative_reward:+.3f}")

    def select_best_variant(
        self,
        performances: List[VariantPerformance],
        variants: List[Tuple[str, Dict]]
    ) -> Tuple[str, str, str]:
        """
        Select the best variant based on absolute score.

        Returns:
            Tuple of (best_variant_content, best_variant_id, rationale)
        """
        best_performance = max(performances, key=lambda p: p.total_score)
        best_idx = performances.index(best_performance)
        best_content, _best_metadata = variants[best_idx]

        rationale = (
            f"Selected {best_performance.variant_id} with score "
            f"{best_performance.total_score}/{best_performance.total_possible} "
            f"({best_performance.percentage:.1f}%), "
            f"relative reward: {best_performance.relative_reward:+.3f}"
        )

        print(f"\n✓ {rationale}")
        return best_content, best_performance.variant_id, rationale

    def check_convergence(self, best_score: int) -> bool:
        """Check if optimization should stop early."""
        if best_score > self.current_best_score:
            self.current_best_score = best_score
            self.no_improvement_count = 0
            return False
        else:
            self.no_improvement_count += 1
            if self.no_improvement_count >= self.early_stop_patience:
                print(f"\n⚠ No improvement for {self.early_stop_patience} iterations. Stopping early.")
                return True
        return False

    def optimize(self) -> bool:
        """Main optimization loop."""
        if not self.load_original_skill():
            return False

        training_tasks = self.load_training_tasks()
        expected_count = self.config.get('task_generation', {}).get('num_training_tasks', 12)
        if len(training_tasks) != expected_count:
            print(f"Warning: Expected {expected_count} training tasks, found {len(training_tasks)}")
            # Continue anyway - don't fail

        # Compute baseline
        baseline_score = self.compute_baseline_score(training_tasks)

        # Optimization loop
        for iteration in range(1, self.max_iterations + 1):
            print(f"\n{'='*60}")
            print(f"ITERATION {iteration}")
            print(f"{'='*60}")

            # Generate variants
            variants = self.generate_variants(iteration, training_tasks)

            # Evaluate variants
            performances = self.evaluate_variants(variants, training_tasks, iteration)

            # Compute relative rewards
            self.compute_relative_rewards(performances)

            # Select best
            best_content, best_id, rationale = self.select_best_variant(performances, variants)

            # Record iteration
            self.iterations.append(OptimizationIteration(
                iteration=iteration,
                variants=performances,
                selected_variant_id=best_id,
                selection_rationale=rationale,
                timestamp=datetime.now().isoformat()
            ))

            # Update current best
            self.current_best_content = best_content

            # Check convergence
            best_score = max(p.total_score for p in performances)
            if iteration >= self.min_iterations and self.check_convergence(best_score):
                break

        # Save results
        self.save_optimized_skill()
        self.save_optimization_log(baseline_score, training_tasks)

        print("\n✓ Optimization complete!")
        return True

    def _resolve_optimized_skill_dir(self) -> Path:
        """Return the directory where optimized SKILL.md should be written."""
        target_name = self.target_skill_path.name
        if target_name.endswith('-optimized'):
            return self.target_skill_path

        return self.output_dir / f"{target_name}-optimized"

    def save_optimized_skill(self):
        """Save the optimized SKILL.md back to the working optimized copy."""
        output_skill_dir = self._resolve_optimized_skill_dir()
        output_skill_dir.mkdir(parents=True, exist_ok=True)

        with open(output_skill_dir / "SKILL.md", 'w', encoding='utf-8') as f:
            f.write(self.current_best_content)

        print(f"✓ Saved optimized skill to {output_skill_dir}")

    def save_optimization_log(self, baseline_score: int, training_tasks: List[Dict]):
        """Generate and save optimization_log.md."""
        optimized_skill_dir = self._resolve_optimized_skill_dir()
        skill_name = optimized_skill_dir.name
        log_path = self.output_dir / "optimization_log.md"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        total_possible = sum(
            len(self.parse_speccheck_criteria(task['speccheck_content']))
            for task in training_tasks
        )

        final_score = self.current_best_score
        improvement = final_score - baseline_score
        improvement_pct = (improvement / total_possible * 100) if total_possible > 0 else 0

        baseline_pct = (baseline_score / total_possible * 100) if total_possible > 0 else 0
        final_pct = (final_score / total_possible * 100) if total_possible > 0 else 0

        log_content = f"""# Optimization Log: {skill_name}

## Summary
- **Original Skill Path**: {self.target_skill_path}
- **Optimized Skill Path**: {optimized_skill_dir}/
- **Total Iterations**: {len(self.iterations)}
- **Execution Mode Requested**: {self.execution_mode}
- **Execution Artifacts**: {self.output_dir / 'grpo_exec'}
- **Initial Training Score**: {baseline_score} / {total_possible} ({baseline_pct:.1f}%)
- **Final Training Score**: {final_score} / {total_possible} ({final_pct:.1f}%)
- **Improvement**: {improvement:+d} points ({improvement_pct:+.1f}%)

## Baseline Performance

| Task | Score | Mode | Notes |
|------|-------|------|-------|
"""

        for task, score in zip(training_tasks, self.baseline_scores):
            mode = score.execution_details.get('actual_mode', 'unknown') if score.execution_details else 'unknown'
            note = score.execution_details.get('reason', '-') if score.execution_details else '-'
            log_content += f"| {task['task_id']} | {score.score}/{score.total} | {mode} | {note} |\n"

        log_content += "\n## Iteration History\n"

        for iter_data in self.iterations:
            log_content += f"\n### Iteration {iter_data.iteration}\n\n"
            log_content += "**Candidate Variants:**\n\n"
            log_content += "| Variant | Mutations Applied | Train Score | Relative Reward | Execution Summary |\n"
            log_content += "|---------|------------------|-------------|------------------|-------------------|\n"

            for perf in iter_data.variants:
                mutations_str = "; ".join(perf.mutations)
                execution_summary_parts = []
                fallback_count = 0
                real_count = 0
                for task_score in perf.task_scores:
                    details = task_score.execution_details or {}
                    actual_mode = details.get('actual_mode')
                    if actual_mode == 'real':
                        real_count += 1
                    elif details.get('mode_requested') == 'real' and actual_mode == 'simulated':
                        fallback_count += 1
                if real_count:
                    execution_summary_parts.append(f"real={real_count}")
                if fallback_count:
                    execution_summary_parts.append(f"fallback={fallback_count}")
                execution_summary = ", ".join(execution_summary_parts) or "n/a"
                log_content += (
                    f"| {perf.variant_id} | {mutations_str} | "
                    f"{perf.total_score}/{perf.total_possible} | "
                    f"{perf.relative_reward:+.3f} | {execution_summary} |\n"
                )

            log_content += f"\n**Selected**: {iter_data.selected_variant_id}\n\n"
            log_content += f"**Rationale**: {iter_data.selection_rationale}\n"

        log_content += "\n## Execution Artifact Layout\n\n"
        log_content += "- `grpo_exec/baseline/task_xxx/` — baseline task scoring artifacts\n"
        log_content += "- `grpo_exec/iteration_NNN/vX-y/task_xxx/` — per-variant task artifacts\n"
        log_content += "- Each artifact directory may contain `command.sh`, `stdout.txt`, `stderr.txt`, and `result.json`\n"
        log_content += "- If a task had no executable command, `result.json` records the real→simulated fallback reason\n"

        log_content += "\n## Key Changes from Original to Optimized\n\n"
        log_content += "_(To be filled by Claude during execution)_\n"

        with open(log_path, 'w', encoding='utf-8') as f:
            f.write(log_content)

        print(f"✓ Saved optimization log to {log_path}")

    def parse_speccheck_criteria(self, speccheck_content: str) -> List[str]:
        """Parse criteria from speccheck.md content."""
        criteria = []
        for line in speccheck_content.split('\n'):
            if line.strip().startswith('- [ ]'):
                criteria.append(line.strip())
        return criteria


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python grpo_optimizer.py <target-skill-path> [output-dir]")
        sys.exit(1)

    target_skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    # Load config
    config_path = Path(__file__).parent.parent.parent / "config.yaml"
    config = {}
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

    optimizer = GRPOOptimizer(target_skill_path, output_dir=output_dir, config=config)
    success = optimizer.optimize()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
