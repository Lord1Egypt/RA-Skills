"""
Generic Task Generator for Skills-Coach v2.3.1

Generates realistic test tasks by analyzing ANY skill's SKILL.md specification.
Extracts actual commands, examples, and use cases to create meaningful tests.
"""

import os
import re
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict


@dataclass
class Task:
    """Represents a single test task."""
    task_id: str
    task_type: str  # "standard", "advanced", or "boundary"
    title: str
    background: str
    objective: str
    command: str  # The actual command to execute
    expected_behavior: str
    constraints: List[str]
    workspace_files: Dict[str, str]  # filename -> content


@dataclass
class SpecCheckCriterion:
    """Represents a single evaluation criterion."""
    description: str
    verification_method: str


@dataclass
class SpecCheck:
    """Represents the evaluation criteria for a task."""
    task_id: str
    criteria: List[SpecCheckCriterion]
    total_points: int
    pass_threshold: int
    evaluation_notes: str


class SkillAnalyzer:
    """Analyzes a SKILL.md to extract commands, examples, and capabilities."""

    def __init__(self, skill_md_content: str):
        self.content = skill_md_content
        self.commands = []
        self.examples = []
        self.use_cases = []
        self.skill_name = ""
        self.description = ""

    def analyze(self):
        """Extract all relevant information from SKILL.md."""
        self._extract_metadata()
        self._extract_commands()
        self._extract_examples()
        self._extract_use_cases()

    def _extract_metadata(self):
        """Extract skill name and description from frontmatter."""
        # Extract from YAML frontmatter
        frontmatter_match = re.search(r'^---\s*\n(.*?)\n---', self.content, re.DOTALL | re.MULTILINE)
        if frontmatter_match:
            try:
                metadata = yaml.safe_load(frontmatter_match.group(1))
                self.skill_name = metadata.get('name', '')
                self.description = metadata.get('description', '')
            except:
                pass

    def _extract_commands(self):
        """Extract command examples from code blocks."""
        # Find all bash/shell code blocks
        code_blocks = re.findall(r'```(?:bash|sh|shell)\n(.*?)\n```', self.content, re.DOTALL)

        for block in code_blocks:
            # Split into individual commands
            lines = block.strip().split('\n')
            for line in lines:
                line = line.strip()
                # Skip comments and empty lines
                if line and not line.startswith('#'):
                    # Extract the actual command (remove inline comments)
                    cmd = line.split('#')[0].strip()
                    if cmd:
                        self.commands.append(cmd)

        print(f"✓ Extracted {len(self.commands)} commands")

    def _extract_examples(self):
        """Extract example sections."""
        # Look for ## Example or ## Quick Example sections
        example_sections = re.findall(
            r'##\s+(?:Quick\s+)?Example[s]?\s*\n(.*?)(?=\n##|\Z)',
            self.content,
            re.DOTALL | re.IGNORECASE
        )

        for section in example_sections:
            self.examples.append(section.strip())

    def _extract_use_cases(self):
        """Extract use cases and workflows."""
        # Look for workflow or usage patterns
        workflow_match = re.search(
            r'###\s+(?:Typical\s+)?[Ww]orkflow\s*\n(.*?)(?=\n###|\n##|\Z)',
            self.content,
            re.DOTALL
        )

        if workflow_match:
            workflow = workflow_match.group(1).strip()
            # Extract numbered steps
            steps = re.findall(r'^\d+\.\s+(.+?)$', workflow, re.MULTILINE)
            self.use_cases.extend(steps)


class GenericTaskGenerator:
    """Generates test tasks for ANY skill based on its SKILL.md."""

    def __init__(self, target_skill_path: str, output_dir: str = ".", config_path: str = None):
        self.target_skill_path = Path(target_skill_path)
        self.output_dir = Path(output_dir)
        self.skill_md_content = ""
        self.analyzer = None

        # Load config
        self.config = self._load_config(config_path)
        self.num_training_tasks = self.config.get('task_generation', {}).get('num_training_tasks', 12)
        self.num_test_tasks = self.config.get('task_generation', {}).get('num_test_tasks', 8)

    def _load_config(self, config_path: str = None) -> dict:
        """Load configuration file."""
        if config_path is None:
            current = Path(__file__).parent
            for _ in range(3):
                config_file = current / "config.yaml"
                if config_file.exists():
                    config_path = config_file
                    break
                current = current.parent

        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)

        return {
            'task_generation': {
                'num_training_tasks': 12,
                'num_test_tasks': 8
            }
        }

    def load_skill_specification(self) -> bool:
        """Load and parse the target skill's SKILL.md."""
        skill_md_path = self.target_skill_path / "SKILL.md"

        if not skill_md_path.exists():
            print(f"ERROR: SKILL.md not found at {skill_md_path}")
            return False

        with open(skill_md_path, 'r', encoding='utf-8') as f:
            self.skill_md_content = f.read()

        print(f"✓ Loaded SKILL.md from {skill_md_path}")

        # Analyze the skill
        self.analyzer = SkillAnalyzer(self.skill_md_content)
        self.analyzer.analyze()

        return True

    def _create_task_from_command(self, cmd: str, task_id: str, task_type: str,
                                   complexity: str = "basic") -> Tuple[Task, SpecCheck]:
        """Create a task from a command."""

        # Determine task title and objective based on command
        if complexity == "basic":
            title = f"Basic: {self._describe_command(cmd)}"
            objective = f"Execute command and verify successful completion"
            constraints = [
                "Must execute without errors",
                "Must produce valid output",
                "Must complete within reasonable time"
            ]
            criteria_count = 4
        else:  # advanced
            title = f"Advanced: {self._describe_command(cmd)}"
            objective = f"Execute command with complex parameters and verify robust handling"
            constraints = [
                "Must handle edge cases gracefully",
                "Must validate inputs properly",
                "Must provide comprehensive output",
                "Must maintain performance under load"
            ]
            criteria_count = 5

        task = Task(
            task_id=task_id,
            task_type=task_type,
            title=title,
            background=f"Tests {complexity} functionality of {self.analyzer.skill_name}",
            objective=objective,
            command=cmd,
            expected_behavior="Command executes successfully and produces valid output",
            constraints=constraints,
            workspace_files={}
        )

        # Create evaluation criteria
        criteria = [
            SpecCheckCriterion(
                description="Command executes without errors",
                verification_method="Exit status: SUCCESS"
            ),
            SpecCheckCriterion(
                description="Output is generated",
                verification_method="Output length > 0 bytes"
            ),
            SpecCheckCriterion(
                description="Output format is valid",
                verification_method="Output appears valid"
            ),
            SpecCheckCriterion(
                description="Expected data is present",
                verification_method="Meaningful data present"
            )
        ]

        if complexity == "advanced":
            criteria.append(SpecCheckCriterion(
                description="Handles complex scenarios",
                verification_method="Complex handling verified"
            ))

        speccheck = SpecCheck(
            task_id=task_id,
            criteria=criteria,
            total_points=criteria_count,
            pass_threshold=int(criteria_count * 0.7),
            evaluation_notes=f"Tests {complexity} command execution"
        )

        return task, speccheck

    def _describe_command(self, cmd: str) -> str:
        """Generate a human-readable description of a command."""
        # Extract the main command (first word)
        parts = cmd.split()
        if not parts:
            return "Command execution"

        main_cmd = parts[0]

        # Common command patterns
        if 'open' in cmd or 'goto' in cmd:
            return "Navigate to URL"
        elif 'click' in cmd:
            return "Click element"
        elif 'type' in cmd or 'fill' in cmd:
            return "Input text"
        elif 'screenshot' in cmd:
            return "Capture screenshot"
        elif 'snapshot' in cmd:
            return "Get page snapshot"
        elif 'search' in cmd or 'find' in cmd:
            return "Search operation"
        elif 'install' in cmd:
            return "Install dependencies"
        elif 'status' in cmd:
            return "Check status"
        else:
            return f"Command execution"

    def generate_tasks(self) -> Tuple[List[Task], List[SpecCheck]]:
        """Generate training tasks."""
        tasks = []
        specchecks = []

        if not self.analyzer or not self.analyzer.commands:
            print("⚠ No commands found, generating generic tasks")
            return self._generate_fallback_tasks("train")

        # Generate standard tasks (50%)
        num_standard = self.num_training_tasks // 2
        for i in range(num_standard):
            task_id = f"task_{i+1:03d}"
            cmd_idx = i % len(self.analyzer.commands)
            cmd = self.analyzer.commands[cmd_idx]

            task, speccheck = self._create_task_from_command(
                cmd, task_id, "standard", "basic"
            )
            tasks.append(task)
            specchecks.append(speccheck)
            print(f"✓ Written {task_id} (standard)")

        # Generate advanced tasks (50%)
        num_advanced = self.num_training_tasks - num_standard
        for i in range(num_advanced):
            task_id = f"task_{num_standard + i + 1:03d}"
            cmd_idx = (num_standard + i) % len(self.analyzer.commands)
            cmd = self.analyzer.commands[cmd_idx]

            # Make command more complex for advanced tasks
            if '--' not in cmd and len(cmd.split()) < 3:
                cmd = self._make_command_advanced(cmd)

            task, speccheck = self._create_task_from_command(
                cmd, task_id, "advanced", "advanced"
            )
            tasks.append(task)
            specchecks.append(speccheck)
            print(f"✓ Written {task_id} (advanced)")

        return tasks, specchecks

    def generate_test_tasks(self) -> Tuple[List[Task], List[SpecCheck]]:
        """Generate test tasks."""
        tasks = []
        specchecks = []

        if not self.analyzer or not self.analyzer.commands:
            return self._generate_fallback_tasks("test")

        # Generate standard test tasks
        num_standard = self.num_test_tasks // 2
        for i in range(num_standard):
            task_id = f"task_{i+1:03d}"
            # Use different commands than training
            cmd_idx = (i + self.num_training_tasks) % len(self.analyzer.commands)
            cmd = self.analyzer.commands[cmd_idx]

            task, speccheck = self._create_task_from_command(
                cmd, task_id, "standard", "basic"
            )
            tasks.append(task)
            specchecks.append(speccheck)
            print(f"✓ Written {task_id} (standard)")

        # Generate advanced test tasks
        num_advanced = self.num_test_tasks - num_standard
        for i in range(num_advanced):
            task_id = f"task_{num_standard + i + 1:03d}"
            cmd_idx = (num_standard + i + self.num_training_tasks) % len(self.analyzer.commands)
            cmd = self.analyzer.commands[cmd_idx]

            cmd = self._make_command_advanced(cmd)

            task, speccheck = self._create_task_from_command(
                cmd, task_id, "advanced", "advanced"
            )
            tasks.append(task)
            specchecks.append(speccheck)
            print(f"✓ Written {task_id} (advanced)")

        return tasks, specchecks

    def _make_command_advanced(self, cmd: str) -> str:
        """Add complexity to a command for advanced tasks."""
        # Add common flags/options if not present
        if 'browse' in cmd:
            if 'open' in cmd and 'http' not in cmd:
                return cmd.replace('open', 'open https://example.com')
            elif 'snapshot' in cmd:
                return cmd + ' --format json'

        # Add output flag if applicable
        if '--output' not in cmd and 'install' in cmd:
            return cmd + ' --output json'

        return cmd

    def _generate_fallback_tasks(self, task_set: str) -> Tuple[List[Task], List[SpecCheck]]:
        """Generate generic fallback tasks when no commands found."""
        tasks = []
        specchecks = []

        num_tasks = self.num_training_tasks if task_set == "train" else self.num_test_tasks

        for i in range(num_tasks):
            task_id = f"task_{i+1:03d}"
            task_type = "standard" if i < num_tasks // 2 else "advanced"

            task = Task(
                task_id=task_id,
                task_type=task_type,
                title=f"{task_type.capitalize()}: Generic test",
                background=f"Tests {self.analyzer.skill_name if self.analyzer else 'skill'} functionality",
                objective="Verify skill works as expected",
                command="echo 'No specific command found'",
                expected_behavior="Skill executes successfully",
                constraints=["Must complete without errors"],
                workspace_files={}
            )
            tasks.append(task)

            speccheck = SpecCheck(
                task_id=task_id,
                criteria=[
                    SpecCheckCriterion("Executes successfully", "Check exit code")
                ],
                total_points=1,
                pass_threshold=1,
                evaluation_notes="Generic test"
            )
            specchecks.append(speccheck)

        return tasks, specchecks

    def save_tasks(self, tasks: List[Task], specchecks: List[SpecCheck], task_set: str):
        """Save tasks and specchecks to disk."""
        tasks_dir = self.output_dir / "tasks" / task_set
        tasks_dir.mkdir(parents=True, exist_ok=True)

        for task, speccheck in zip(tasks, specchecks):
            task_dir = tasks_dir / task.task_id
            task_dir.mkdir(exist_ok=True)

            # Save task.md
            task_md = f"""# Task: {task.title}

## Background
{task.background}

## Objective
{task.objective}

## Command to Execute
```bash
{task.command}
```

## Expected Behavior
{task.expected_behavior}

## Constraints
{chr(10).join(f'- {c}' for c in task.constraints)}
"""
            with open(task_dir / "task.md", 'w') as f:
                f.write(task_md)

            # Save speccheck.md
            speccheck_md = f"""# SpecCheck: {task.task_id}

## Evaluation Criteria

"""
            for i, criterion in enumerate(speccheck.criteria, 1):
                speccheck_md += f"""### Criterion {i}: {criterion.description}
**Verification**: {criterion.verification_method}

"""

            speccheck_md += f"""## Scoring
- **Total Points**: {speccheck.total_points}
- **Pass Threshold**: {speccheck.pass_threshold}

## Notes
{speccheck.evaluation_notes}
"""
            with open(task_dir / "speccheck.md", 'w') as f:
                f.write(speccheck_md)

            # Create workspace directory
            workspace_dir = task_dir / "workspace"
            workspace_dir.mkdir(exist_ok=True)

            # Save workspace files
            for filename, content in task.workspace_files.items():
                with open(workspace_dir / filename, 'w') as f:
                    f.write(content)

    def generate_and_save_all(self):
        """Main entry point: generate and save all tasks."""
        if not self.load_skill_specification():
            return False

        print("\n=== Generating Training Tasks ===")
        train_tasks, train_specchecks = self.generate_tasks()

        print("\n=== Generating Test Tasks ===")
        test_tasks, test_specchecks = self.generate_test_tasks()

        self.save_tasks(train_tasks, train_specchecks, "train")
        print(f"✓ Saved {len(train_tasks)} train tasks")

        self.save_tasks(test_tasks, test_specchecks, "test")
        print(f"✓ Saved {len(test_tasks)} test tasks")

        print("\n✓ Task generation complete!")
        return True


def main():
    """CLI entry point."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python generic_task_generator.py <target-skill-path> [output-dir]")
        sys.exit(1)

    target_skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."

    generator = GenericTaskGenerator(target_skill_path, output_dir)
    success = generator.generate_and_save_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
