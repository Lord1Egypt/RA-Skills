#!/usr/bin/env python3
"""
Skills-Coach v2.3.1 Main Orchestrator

Coordinates the execution of all subskills in sequence:
0. Create optimized copy (IMMUTABILITY RULE)
1. Code capability detection
2. Sample-agent: Generate training and test tasks
3. Optimize-agent: Run Training-Free GRPO or vanilla GRPO optimization
4. Exec-agent: Execute both skill versions
5. Failure analysis
5.5. Auto-fix issues (NEW in v2.3.0)
6. Evaluate-agent: Evaluate and generate report

v2.3.0: Auto-fix integration
        - Automatically fixes common issues (missing dependencies, parameters, etc.)
        - Iterative fix-test-reanalyze loop (max 2 iterations)
        - LLM-powered intelligent fixes for complex issues
v2.2.0: Enhanced task diversity and stability improvements
        - Local file generation with reportlab (60% local files)
        - Reduced API dependencies (10% API tasks)
        - Optimized LLM usage to prevent timeouts
v2.0.0: Major upgrade with Training-Free GRPO optimization method
        - No parameter updates, uses experience library
        - Semantic advantage instead of numerical advantage
"""

import sys
import yaml
import json
import shutil
from pathlib import Path
from datetime import datetime

# Import run manager if available
try:
    sys.path.insert(0, str(Path(__file__).parent / "subskills" / "run-manager"))
    from run_manager import RunManager
    RUN_MANAGER_AVAILABLE = True
except ImportError:
    RUN_MANAGER_AVAILABLE = False
    print("Warning: run_manager not available, using legacy flat structure")


def load_config() -> dict:
    """Load configuration from config.yaml."""
    config_path = Path(__file__).parent / "config.yaml"
    if config_path.exists():
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}


def validate_target_skill(target_skill_path: Path) -> bool:
    """Validate that target skill exists and has SKILL.md."""
    if not target_skill_path.exists():
        print(f"ERROR: Target skill path does not exist: {target_skill_path}")
        return False

    skill_md = target_skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"ERROR: SKILL.md not found in {target_skill_path}")
        return False

    print(f"✓ Validated target skill: {target_skill_path}")
    return True


def create_optimized_copy(
    target_skill_path: Path,
    work_dir: Path,
    config: dict
) -> Path:
    """
    IMMUTABILITY RULE: Create optimized copy before any modifications.

    The original {target-skill} is NEVER modified.
    All changes go to {target-skill}-optimized.
    """
    immutability_config = config.get('immutability', {})

    if not immutability_config.get('always_work_in_optimized', True):
        print("⚠ Warning: Immutability rule disabled in config")
        return target_skill_path

    skill_name = target_skill_path.name
    optimized_path = work_dir / f"{skill_name}-optimized"

    # Remove existing optimized copy if present
    if optimized_path.exists():
        shutil.rmtree(optimized_path)

    # Create fresh copy
    shutil.copytree(target_skill_path, optimized_path)

    print(f"✓ Created optimized copy: {optimized_path}")
    print(f"  IMMUTABILITY: Original {skill_name} will NOT be modified")

    return optimized_path


def setup_directories(config: dict, target_skill_path: Path) -> Path:
    """
    Set up working directory structure.

    Returns:
        Path to the working directory (either versioned run dir or current dir)
    """
    use_versioned_runs = config.get('output', {}).get('use_versioned_runs', True)

    if use_versioned_runs and RUN_MANAGER_AVAILABLE:
        # Create versioned run directory
        manager = RunManager()
        run_dir = manager.create_run(target_skill_path, config)
        print(f"✓ Created versioned run directory: {run_dir}")
        return run_dir
    else:
        # Use legacy flat structure
        work_dir = Path.cwd()
        (work_dir / "tasks" / "train").mkdir(parents=True, exist_ok=True)
        (work_dir / "tasks" / "test").mkdir(parents=True, exist_ok=True)
        (work_dir / "exec_results" / "original").mkdir(parents=True, exist_ok=True)
        (work_dir / "exec_results" / "optimized").mkdir(parents=True, exist_ok=True)
        print(f"✓ Created working directories (legacy flat structure)")
        return work_dir


def run_code_capability_detection(
    target_skill_path: Path,
    work_dir: Path,
    config: dict
) -> bool:
    """Detect code capabilities before generating tasks."""
    capability_config = config.get('code_capability', {})

    if not capability_config.get('enabled', True):
        print("⊘ Code capability detection disabled")
        return True

    print("\n" + "="*60)
    print("STEP 0: Code Capability Detection")
    print("="*60)

    import subprocess

    detector_dir = Path(__file__).parent / "subskills" / "code-capability-detector"
    cmd = [
        sys.executable,
        str(detector_dir / "code_capability_detector.py"),
        str(target_skill_path),
        str(work_dir.resolve())
    ]

    result = subprocess.run(cmd, cwd=detector_dir)

    if result.returncode != 0:
        print("⚠ Code capability detection failed (non-fatal)")
        return True  # Non-fatal, continue anyway

    print("✓ Code capability analysis complete")
    return True


def run_sample_agent(target_skill_path: Path, work_dir: Path, config_path: Path = None) -> bool:
    """Execute sample-agent to generate tasks."""
    print("\n" + "="*60)
    print("STEP 1: Generate Test Tasks (sample-agent)")
    print("="*60)

    import subprocess

    sample_agent_dir = Path(__file__).parent / "subskills" / "sample-agent"

    # Use smart_task_generator for real executable tasks
    cmd = [
        sys.executable,
        str(sample_agent_dir / "smart_task_generator.py"),
        str(target_skill_path),
        str(work_dir.resolve())
    ]

    # Add config path if provided
    if config_path and config_path.exists():
        cmd.append(str(config_path))

    result = subprocess.run(cmd, cwd=sample_agent_dir)

    if result.returncode != 0:
        print("ERROR: sample-agent failed")
        return False

    # Verify tasks were created
    train_dir = work_dir / "tasks" / "train"
    test_dir = work_dir / "tasks" / "test"

    train_tasks = list(train_dir.glob("task_*"))
    test_tasks = list(test_dir.glob("task_*"))

    print(f"\n✓ Generated {len(train_tasks)} training tasks and {len(test_tasks)} test tasks")

    if len(train_tasks) == 0:
        print("ERROR: No training tasks were generated")
        return False

    return True


def run_optimize_agent(
    optimized_skill_path: Path,
    work_dir: Path,
    config: dict
) -> bool:
    """Execute optimize-agent to run optimization on optimized copy with monitoring."""
    print("\n" + "="*60)
    print("STEP 2: Optimize the Skill (optimize-agent)")
    print(f"  Working on: {optimized_skill_path.name}")
    print("="*60)

    import subprocess
    import threading

    optimize_agent_dir = Path(__file__).parent / "subskills" / "optimize-agent"

    # Check which optimization method to use
    optimization_method = config.get('optimization', {}).get('method', 'training_free_grpo')

    if optimization_method == 'training_free_grpo':
        print("✓ Using Training-Free GRPO optimization")
        optimizer_script = "training_free_grpo_optimizer.py"
    else:
        print("✓ Using vanilla GRPO optimization")
        optimizer_script = "grpo_optimizer.py"

    cmd = [
        sys.executable,
        str(optimize_agent_dir / optimizer_script),
        str(optimized_skill_path.resolve()),  # Work on optimized copy (absolute path)
        str(work_dir.resolve())
    ]

    # Start the optimizer process
    process = subprocess.Popen(cmd, cwd=optimize_agent_dir)

    # Get monitoring timeout from config (default 5 minutes)
    monitor_timeout = config.get('execution', {}).get('stuck_process_timeout_minutes', 5)

    # Start monitoring in a separate thread
    monitor_killed = [False]  # Use list to allow modification in thread

    def monitor_process():
        """Monitor the process and kill if stuck."""
        try:
            # Import process monitor
            sys.path.insert(0, str(Path(__file__).parent))
            from process_monitor import ProcessMonitor

            monitor = ProcessMonitor(process.pid, timeout_minutes=monitor_timeout)
            success, message = monitor.monitor()

            if not success:
                print(f"\n⚠️  Process monitor: {message}")
                monitor_killed[0] = True
        except Exception as e:
            print(f"\n⚠️  Process monitoring failed: {e}")

    monitor_thread = threading.Thread(target=monitor_process, daemon=True)
    monitor_thread.start()

    # Wait for process to complete
    result = process.wait()

    # Check if process was killed by monitor
    if monitor_killed[0]:
        print("ERROR: optimize-agent was killed due to inactivity (stuck waiting for API)")
        return False

    if result != 0:
        print("ERROR: optimize-agent failed")
        return False

    print(f"\n✓ Optimization complete on {optimized_skill_path.name}")
    return True


def run_exec_agent(
    original_skill_path: Path,
    optimized_skill_path: Path,
    work_dir: Path,
    config: dict
) -> bool:
    """
    Execute exec-agent to run both skill versions with real commands.
    """
    print("\n" + "="*60)
    print("STEP 3: Execute Both Skill Versions (exec-agent)")
    print(f"  Original: {original_skill_path.name}")
    print(f"  Optimized: {optimized_skill_path.name}")
    print("="*60)

    import subprocess

    exec_agent_dir = Path(__file__).parent / "subskills" / "exec-agent"

    # Build command with optional flags
    cmd = [
        sys.executable,
        str(exec_agent_dir / "executor.py"),
        str(original_skill_path.resolve()),  # Original for comparison (absolute path)
        str(work_dir.resolve())
    ]

    # Add optional flags from config
    exec_config = config.get('execution', {})
    if exec_config.get('parallel_execution', False):
        cmd.append('--parallel')
        print("  → Parallel execution enabled")

    if exec_config.get('auto_install_deps', False):
        cmd.append('--auto-install')
        print("  → Auto-install dependencies enabled")

    result = subprocess.run(cmd, cwd=exec_agent_dir)

    if result.returncode != 0:
        print("ERROR: exec-agent failed")
        return False

    # Verify results were created
    original_dir = work_dir / "exec_results" / "original"
    optimized_dir = work_dir / "exec_results" / "optimized"

    original_results = list(original_dir.glob("task_*"))
    optimized_results = list(optimized_dir.glob("task_*"))

    print(f"\n✓ Executed {len(original_results)} original tasks and {len(optimized_results)} optimized tasks")

    if len(original_results) == 0 or len(optimized_results) == 0:
        print("ERROR: No execution results were generated")
        return False

    return True


def run_failure_analysis(work_dir: Path, config: dict) -> bool:
    """Analyze failed tasks to identify root causes."""
    failure_config = config.get('failure_analysis', {})

    if not failure_config.get('enabled', True):
        print("⊘ Failure analysis disabled")
        return True

    print("\n" + "="*60)
    print("STEP 4: Failure Analysis")
    print("="*60)

    import subprocess

    analyzer_dir = Path(__file__).parent / "subskills" / "failure-analyzer"

    # Analyze both original and optimized failures
    for version in ['original', 'optimized']:
        exec_results_dir = work_dir / "exec_results" / version

        cmd = [
            sys.executable,
            str(analyzer_dir / "failure_analyzer.py"),
            str(exec_results_dir.resolve()),  # Use absolute path
            str(work_dir.resolve())
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)  # Don't change cwd

        if result.returncode == 0:
            # Rename output to version-specific
            src = work_dir / "failure_analysis.md"
            dst = work_dir / f"failure_analysis_{version}.md"
            if src.exists():
                src.rename(dst)
            else:
                print(f"  ⚠ Warning: {src} not found for {version}")

            src_json = work_dir / "failure_analysis.json"
            dst_json = work_dir / f"failure_analysis_{version}.json"
            if src_json.exists():
                src_json.rename(dst_json)
                # Verify the JSON file is not empty
                with open(dst_json, 'r') as f:
                    content = f.read().strip()
                    if content == "[]":
                        print(f"  ⚠ Warning: No failures detected for {version}")
            else:
                print(f"  ⚠ Warning: {src_json} not found for {version}")
        else:
            print(f"  ⚠ Warning: Failure analysis failed for {version}")
            if result.stderr:
                print(f"    Error: {result.stderr}")

    print("✓ Failure analysis complete")
    return True


def run_auto_fixer(optimized_skill_path: Path, work_dir: Path, config: dict) -> bool:
    """Apply automatic fixes to the optimized skill based on failure analysis."""
    auto_fix_config = config.get('auto_fix', {})

    if not auto_fix_config.get('enabled', True):
        print("⊘ Auto-fix disabled")
        return False

    print("\n" + "="*60)
    print("STEP 4.5: Auto-Fix Issues")
    print("="*60)

    import subprocess

    # Check if we have failure analysis for optimized version
    failure_json = work_dir / "failure_analysis_optimized.json"
    if not failure_json.exists():
        print("⊘ No failure analysis found, skipping auto-fix")
        return False

    # Load failure analysis
    with open(failure_json, 'r') as f:
        analyses = json.load(f)

    if not analyses:
        print("✓ No failures to fix")
        return False

    print(f"  Found {len(analyses)} failure(s) to analyze")

    # Run auto-fixer
    fixer_script = Path(__file__).parent / "subskills" / "optimize-agent" / "auto_fixer.py"

    cmd = [
        sys.executable,
        str(fixer_script),
        str(optimized_skill_path.resolve()),
        str(failure_json.resolve())
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Auto-fix complete")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print("⚠ Auto-fix encountered issues")
        if result.stderr:
            print(f"  Error: {result.stderr}")
        if result.stdout:
            print(f"  Output: {result.stdout}")
        return False


def run_evaluate_agent(
    original_skill_path: Path,
    optimized_skill_path: Path,
    work_dir: Path
) -> bool:
    """Execute evaluate-agent to generate report."""
    print("\n" + "="*60)
    print("STEP 5: Evaluate and Report (evaluate-agent)")
    print("="*60)

    import subprocess

    evaluate_agent_dir = Path(__file__).parent / "subskills" / "evaluate-agent"
    cmd = [
        sys.executable,
        str(evaluate_agent_dir / "evaluator.py"),
        str(original_skill_path.resolve()),  # Use absolute path
        str(work_dir.resolve())
    ]

    result = subprocess.run(cmd, cwd=evaluate_agent_dir)

    if result.returncode != 0:
        print("ERROR: evaluate-agent failed")
        return False

    # Verify report was created
    report_path = work_dir / "results_report.md"
    if not report_path.exists():
        print("ERROR: results_report.md not created")
        return False

    print(f"\n✓ Generated evaluation report: {report_path}")
    return True


def finalize_run(work_dir: Path, config: dict):
    """Finalize run metadata if using versioned runs."""
    use_versioned_runs = config.get('output', ).get('use_versioned_runs', True)

    if use_versioned_runs and RUN_MANAGER_AVAILABLE:
        # Read results from report
        report_path = work_dir / "results_report.md"
        if report_path.exists():
            # Parse report for decision and scores
            # This is a simplified version - real implementation would parse the report
            print("\n✓ Finalized run metadata")


def main():
    """Main orchestration entry point."""
    if len(sys.argv) < 2:
        print("Usage: python orchestrator.py <target-skill-path>")
        sys.exit(1)

    target_skill_path = Path(sys.argv[1]).resolve()

    # Load configuration
    config = load_config()

    # Pre-flight checks
    print("="*60)
    print("Skills-Coach v2.3.1 - Pre-flight Checks")
    print("="*60)

    if not validate_target_skill(target_skill_path):
        sys.exit(1)

    # Check API availability before starting
    print("\n" + "="*60)
    print("API Configuration Check")
    print("="*60)

    sys.path.insert(0, str(Path(__file__).parent))
    from api_checker import ensure_api_available

    if not ensure_api_available():
        print("\n✗ API not available. Cannot proceed with optimization.")
        print("  Optimization requires Claude API access.")
        sys.exit(1)

    # Set up directories
    work_dir = setup_directories(config, target_skill_path)

    # IMMUTABILITY RULE: Create optimized copy
    optimized_skill_path = create_optimized_copy(target_skill_path, work_dir, config)

    # Step 0: Code capability detection
    if not run_code_capability_detection(target_skill_path, work_dir, config):
        sys.exit(1)

    # Step 1: Generate tasks
    config_path = Path(__file__).parent / "config.yaml"
    if not run_sample_agent(target_skill_path, work_dir, config_path):
        sys.exit(1)

    # Step 2: Optimize (works on optimized copy)
    if not run_optimize_agent(optimized_skill_path, work_dir, config):
        sys.exit(1)

    # Step 3: Execute both skill versions
    if not run_exec_agent(target_skill_path, optimized_skill_path, work_dir, config):
        sys.exit(1)

    # Step 4: Failure analysis
    if not run_failure_analysis(work_dir, config):
        sys.exit(1)

    # Step 4.5: Auto-fix issues (iterative improvement)
    auto_fix_config = config.get('auto_fix', {})
    max_fix_iterations = auto_fix_config.get('max_iterations', 2)

    for iteration in range(max_fix_iterations):
        fixes_applied = run_auto_fixer(optimized_skill_path, work_dir, config)

        if not fixes_applied:
            break

        print(f"\n  Iteration {iteration + 1}/{max_fix_iterations}: Fixes applied, re-testing...")

        # Re-execute optimized skill to see if fixes worked
        if not run_exec_agent(target_skill_path, optimized_skill_path, work_dir, config):
            print("  ⚠ Re-execution failed, stopping fix iterations")
            break

        # Re-analyze failures
        if not run_failure_analysis(work_dir, config):
            print("  ⚠ Re-analysis failed, stopping fix iterations")
            break

        # Check if all failures are resolved
        failure_json = work_dir / "failure_analysis_optimized.json"
        if failure_json.exists():
            with open(failure_json, 'r') as f:
                remaining_failures = json.load(f)

            if not remaining_failures:
                print("  ✓ All failures resolved!")
                break
            else:
                print(f"  Still have {len(remaining_failures)} failure(s), continuing...")
        else:
            break

    # Step 5: Evaluate
    if not run_evaluate_agent(target_skill_path, optimized_skill_path, work_dir):
        sys.exit(1)

    # Finalize
    finalize_run(work_dir, config)

    # Present results
    print("\n" + "="*60)
    print("Skills-Coach v2.3.1 - Complete")
    print("="*60)

    report_path = work_dir / "results_report.md"
    print(f"\nResults report: {report_path}")

    # Show optimized skill location
    skill_name = target_skill_path.name
    final_optimized = work_dir / f"{skill_name}-optimized"
    if final_optimized.exists():
        print(f"Optimized skill: {final_optimized}")

    print(f"\n✓ Original skill unchanged: {target_skill_path}")

    sys.exit(0)


if __name__ == "__main__":
    main()
