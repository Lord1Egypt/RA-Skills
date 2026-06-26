#!/usr/bin/env python3
"""
Real Executor for Skills-Coach v2.3.1

Executes real commands from test tasks and captures outputs.
Includes performance benchmarking and parallel execution support.
"""

import sys
import subprocess
import time
import json
import psutil
import os
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# Import environment checker
try:
    from env_checker import EnvironmentChecker
    ENV_CHECKER_AVAILABLE = True
except ImportError:
    ENV_CHECKER_AVAILABLE = False


class PerformanceMetrics:
    """Tracks performance metrics for command execution."""

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.cpu_percent_start = None
        self.cpu_percent_end = None
        self.memory_start = None
        self.memory_end = None
        self.process = psutil.Process(os.getpid())

    def start(self):
        """Start tracking metrics."""
        self.start_time = time.time()
        self.cpu_percent_start = self.process.cpu_percent()
        self.memory_start = self.process.memory_info().rss / 1024 / 1024  # MB

    def end(self):
        """Stop tracking metrics."""
        self.end_time = time.time()
        self.cpu_percent_end = self.process.cpu_percent()
        self.memory_end = self.process.memory_info().rss / 1024 / 1024  # MB

    def get_metrics(self) -> dict:
        """Get collected metrics."""
        return {
            'execution_time': self.end_time - self.start_time if self.end_time else 0,
            'cpu_percent': self.cpu_percent_end if self.cpu_percent_end else 0,
            'memory_mb': self.memory_end if self.memory_end else 0,
            'memory_delta_mb': (self.memory_end - self.memory_start) if self.memory_end and self.memory_start else 0
        }


class SkillExecutor:
    """Executes real skill commands and captures outputs."""

    def __init__(self, target_skill_path: str, output_dir: str = ".", parallel: bool = False, auto_install: bool = False):
        self.target_skill_path = Path(target_skill_path)
        self.output_dir = Path(output_dir)
        self.skill_name = self.target_skill_path.name
        self.parallel = parallel
        self.auto_install = auto_install
        self.performance_data = {}

        # Paths
        test_tasks_path = Path("tasks/test")
        if not test_tasks_path.is_absolute():
            self.test_tasks_dir = self.output_dir / test_tasks_path
        else:
            self.test_tasks_dir = test_tasks_path

        exec_results_path = Path("exec_results")
        if not exec_results_path.is_absolute():
            self.exec_results_dir = self.output_dir / exec_results_path
        else:
            self.exec_results_dir = exec_results_path

        self.optimized_skill_dir = self.output_dir / f"{self.skill_name}-optimized"

    def load_test_tasks(self):
        """Load all test tasks with their commands."""
        tasks = []
        for task_dir in sorted(self.test_tasks_dir.glob("task_*")):
            task_md = task_dir / "task.md"
            if task_md.exists():
                with open(task_md, 'r', encoding='utf-8') as f:
                    task_content = f.read()

                # Extract command from task.md
                command = self._extract_command(task_content)

                tasks.append({
                    "task_id": task_dir.name,
                    "task_dir": str(task_dir),
                    "task_content": task_content,
                    "command": command
                })
        print(f"✓ Loaded {len(tasks)} test tasks")
        return tasks

    def _extract_command(self, task_content: str) -> str:
        """Extract executable command from task markdown."""
        import re
        # Look for command in code block
        match = re.search(r'```(?:bash|shell|sh)\n(.*?)\n```', task_content, re.DOTALL)
        if match:
            return match.group(1).strip()
        # For documentation tasks, return empty string (no command to execute)
        return ""

    def execute_command(self, command: str, skill_path: Path, result_dir: Path, skill_version: str, task_id: str, task_content: str):
        """Execute a real command and capture output with performance metrics."""
        print(f"  Executing {skill_version} on {task_id}...")

        # Create result directories
        result_dir.mkdir(parents=True, exist_ok=True)
        output_dir = result_dir / "output"
        output_dir.mkdir(exist_ok=True)

        # Replace skill path in command if needed
        if skill_version == "optimized":
            # Update command to use optimized skill path
            command = command.replace(str(self.target_skill_path), str(skill_path))

        # Determine working directory: use workspace if it exists
        # Navigate from exec_results/original/task_001 to tasks/test/task_001/workspace
        run_dir = result_dir.parent.parent.parent  # Go up to run directory
        # Determine if this is a training or test task
        task_set = "train" if task_id.startswith("task_") and int(task_id.split('_')[1]) <= 12 else "test"
        workspace_dir = run_dir / "tasks" / task_set / task_id / "workspace"

        if workspace_dir.exists():
            work_dir = workspace_dir
        else:
            work_dir = output_dir

        # Start performance tracking
        metrics = PerformanceMetrics()
        metrics.start()

        # Execute command
        start_time = time.time()
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
                cwd=work_dir
            )
            exec_time = time.time() - start_time
            status = "SUCCESS" if result.returncode == 0 else "ERROR"
            stdout = result.stdout
            stderr = result.stderr
        except subprocess.TimeoutExpired:
            exec_time = 300
            status = "TIMEOUT"
            stdout = ""
            stderr = "Command timed out after 5 minutes"
        except Exception as e:
            exec_time = time.time() - start_time
            status = "ERROR"
            stdout = ""
            stderr = str(e)

        # End performance tracking
        metrics.end()
        perf_metrics = metrics.get_metrics()

        # Store performance data
        perf_key = f"{skill_version}_{task_id}"
        self.performance_data[perf_key] = perf_metrics

        # Save stdout to result file
        output_file = output_dir / "result.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(stdout)

        # Write run log with performance metrics
        self._write_run_log(result_dir, task_id, skill_version, task_content,
                           command, status, exec_time, stdout, stderr, perf_metrics)

    def _write_run_log(self, result_dir: Path, task_id: str, skill_version: str,
                       task_content: str, command: str, status: str, exec_time: float,
                       stdout: str, stderr: str, perf_metrics: dict = None):
        """Write execution log with performance metrics."""
        run_log = result_dir / "run_log.md"

        perf_section = ""
        if perf_metrics:
            perf_section = f"""
## Performance Metrics
- **Execution Time**: {perf_metrics['execution_time']:.2f}s
- **CPU Usage**: {perf_metrics['cpu_percent']:.1f}%
- **Memory Usage**: {perf_metrics['memory_mb']:.1f} MB
- **Memory Delta**: {perf_metrics['memory_delta_mb']:+.1f} MB
"""

        log_content = f"""# Execution Log: {skill_version} - {task_id}

## Metadata
- **Task**: {task_id}
- **Skill**: {skill_version}
- **Timestamp**: {datetime.now().isoformat()}
- **Execution Time**: {exec_time:.2f}s
- **Status**: {status}
{perf_section}
## Command Executed
```bash
{command}
```

## Task Description
{task_content[:500]}{'...' if len(task_content) > 500 else ''}

## Standard Output
```
{stdout[:2000]}{'...' if len(stdout) > 2000 else ''}
```

## Standard Error
```
{stderr[:2000]}{'...' if len(stderr) > 2000 else ''}
```

## Result
{status} - Command {'completed successfully' if status == 'SUCCESS' else 'failed'}
"""
        with open(run_log, 'w', encoding='utf-8') as f:
            f.write(log_content)

    def execute_all(self):
        """Execute both skill versions on all test tasks."""
        print("\n" + "="*60)
        print("Executing Skills on Test Tasks (REAL EXECUTION)")
        if self.parallel:
            print("Mode: PARALLEL")
        print("="*60)

        # Check environment dependencies
        if ENV_CHECKER_AVAILABLE:
            checker = EnvironmentChecker(self.target_skill_path, auto_install=self.auto_install)
            all_available, missing = checker.check_all_dependencies()
            checker.print_report()

            if not all_available and self.auto_install:
                print("\n→ Attempting to auto-install missing dependencies...")
                if checker.auto_install_missing():
                    print("✓ All dependencies installed successfully")
                else:
                    print("⚠ Some dependencies could not be installed")
                    print("   Continuing with execution...")
            elif not all_available:
                print("\n⚠ Continuing with execution despite missing dependencies...")
                print("   (Some tasks may fail)")
        else:
            print("\n⚠ Environment checker not available, skipping dependency check")

        # Load test tasks
        tasks = self.load_test_tasks()
        if len(tasks) == 0:
            print("ERROR: No test tasks found")
            return False

        # Prepare result directories
        (self.exec_results_dir / "original").mkdir(parents=True, exist_ok=True)
        (self.exec_results_dir / "optimized").mkdir(parents=True, exist_ok=True)

        # Execute original skill
        print(f"\n=== Executing Original Skill ===")
        self._execute_skill_version(tasks, self.target_skill_path, "original")

        # Execute optimized skill
        print(f"\n=== Executing Optimized Skill ===")
        if not self.optimized_skill_dir.exists():
            print(f"ERROR: Optimized skill not found at {self.optimized_skill_dir}")
            return False

        self._execute_skill_version(tasks, self.optimized_skill_dir, "optimized")

        # Save performance summary
        self._save_performance_summary()

        print(f"\n✓ Execution complete!")
        print(f"  Original results: {self.exec_results_dir / 'original'}")
        print(f"  Optimized results: {self.exec_results_dir / 'optimized'}")
        return True

    def _execute_skill_version(self, tasks: list, skill_path: Path, skill_version: str):
        """Execute all tasks for a skill version (parallel or sequential)."""
        # Check and install dependencies for this specific skill version
        if ENV_CHECKER_AVAILABLE and self.auto_install:
            checker = EnvironmentChecker(skill_path, auto_install=self.auto_install)
            all_available, missing = checker.check_all_dependencies()

            if not all_available:
                print(f"  → Installing dependencies for {skill_version}...")
                if checker.auto_install_missing():
                    print(f"  ✓ Dependencies installed for {skill_version}")
                else:
                    print(f"  ⚠ Some dependencies could not be installed for {skill_version}")

        if self.parallel:
            self._execute_parallel(tasks, skill_path, skill_version)
        else:
            self._execute_sequential(tasks, skill_path, skill_version)

    def _execute_sequential(self, tasks: list, skill_path: Path, skill_version: str):
        """Execute tasks sequentially."""
        for task in tasks:
            if not task['command']:
                print(f"  ⚠ Skipping {task['task_id']} - documentation task (no command)")
                # For documentation tasks, create a placeholder result
                result_dir = self.exec_results_dir / skill_version / task['task_id']
                self._create_documentation_result(result_dir, task, skill_version)
                continue

            result_dir = self.exec_results_dir / skill_version / task['task_id']
            self.execute_command(
                task['command'],
                skill_path,
                result_dir,
                skill_version,
                task['task_id'],
                task['task_content']
            )

    def _execute_parallel(self, tasks: list, skill_path: Path, skill_version: str):
        """Execute tasks in parallel using ThreadPoolExecutor."""
        max_workers = min(4, len(tasks))  # Max 4 parallel tasks
        print(f"  Using {max_workers} parallel workers")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {}

            for task in tasks:
                if not task['command']:
                    print(f"  ⚠ Skipping {task['task_id']} - documentation task (no command)")
                    # For documentation tasks, create a placeholder result
                    result_dir = self.exec_results_dir / skill_version / task['task_id']
                    self._create_documentation_result(result_dir, task, skill_version)
                    continue

                result_dir = self.exec_results_dir / skill_version / task['task_id']
                future = executor.submit(
                    self.execute_command,
                    task['command'],
                    skill_path,
                    result_dir,
                    skill_version,
                    task['task_id'],
                    task['task_content']
                )
                futures[future] = task['task_id']

            # Wait for all tasks to complete
            for future in as_completed(futures):
                task_id = futures[future]
                try:
                    future.result()
                except Exception as e:
                    print(f"  ✗ Error executing {task_id}: {e}")

    def _create_documentation_result(self, result_dir: Path, task: dict, skill_version: str):
        """Create placeholder result for documentation tasks."""
        result_dir.mkdir(parents=True, exist_ok=True)
        output_dir = result_dir / "output"
        output_dir.mkdir(exist_ok=True)

        # Create a placeholder output file indicating this is a documentation task
        output_file = output_dir / "result.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Documentation task - evaluated by LLM, not executed\n")

        # Write run log
        run_log = result_dir / "run_log.md"
        log_content = f"""# Execution Log: {skill_version} - {task['task_id']}

## Metadata
- **Task**: {task['task_id']}
- **Skill**: {skill_version}
- **Timestamp**: {datetime.now().isoformat()}
- **Execution Time**: N/A (documentation task)
- **Status**: DOCUMENTATION

## Task Description
{task['task_content']}

## Command Executed
```bash
N/A - Documentation quality evaluation task
```

## Standard Output
```
Documentation task - will be evaluated by LLM for quality
```

## Standard Error
```

```

## Result
DOCUMENTATION - Task requires LLM evaluation, not command execution
"""
        with open(run_log, 'w', encoding='utf-8') as f:
            f.write(log_content)

    def _save_performance_summary(self):
        """Save performance metrics summary."""
        summary_file = self.exec_results_dir / "performance_summary.json"

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(self.performance_data, f, indent=2)

        print(f"\n✓ Performance summary saved: {summary_file}")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Execute skills with real commands')
    parser.add_argument('target_skill_path', help='Path to target skill')
    parser.add_argument('output_dir', nargs='?', default='.', help='Output directory')
    parser.add_argument('--parallel', action='store_true', help='Execute tasks in parallel')
    parser.add_argument('--auto-install', action='store_true', help='Automatically install missing dependencies')

    args = parser.parse_args()

    executor = SkillExecutor(
        args.target_skill_path,
        args.output_dir,
        parallel=args.parallel,
        auto_install=args.auto_install
    )
    success = executor.execute_all()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
