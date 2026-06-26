#!/usr/bin/env python3
"""Saturnday governed execution for OpenClaw.

Runs the full saturnday pipeline: plan → execute → govern → evidence.
Requires: pip install saturnday

Usage:
    python scripts/run.py <project-directory> --brief "description" [--backend claude-cli]
"""

import json
import os
import subprocess
import sys
from pathlib import Path


VALID_BACKENDS = {"claude-cli", "codex-cli", "cursor-cli", "openai", "anthropic"}


def check_saturnday_installed() -> bool:
    """Verify saturnday is installed and accessible."""
    try:
        result = subprocess.run(
            ["saturnday", "version"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def ensure_git_repo(project_path: Path) -> None:
    """Initialize git if the project directory is not already a repo."""
    if not (project_path / ".git").exists():
        subprocess.run(
            ["git", "init"],
            cwd=str(project_path),
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", "init"],
            cwd=str(project_path),
            capture_output=True,
            check=True,
        )


def detect_backend() -> str | None:
    """Detect which AI coder backends are available."""
    checks = {
        "claude-cli": "claude",
        "codex-cli": "codex",
        "cursor-cli": "agent",
    }
    for backend, binary in checks.items():
        try:
            result = subprocess.run(
                ["which", binary],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                return backend
        except FileNotFoundError:
            continue

    # Check API backends
    if os.environ.get("OPENAI_API_KEY"):
        return "openai"
    if os.environ.get("ANTHROPIC_API_KEY"):
        return "anthropic"

    return None


def run_plan(project_path: str, brief: str, backend: str) -> dict:
    """Generate a plan from a brief.

    Args:
        project_path: Path to the project directory.
        brief: Natural-language project description.
        backend: AI coder backend to use.

    Returns:
        Dict with plan path and plan summary.
    """
    project = Path(project_path).resolve()
    project.mkdir(parents=True, exist_ok=True)
    ensure_git_repo(project)

    cmd = [
        "saturnday", "plan",
        "--brief", brief,
        "--repo", str(project),
        "--backend", backend,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
        cwd=str(project),
    )

    output_text = result.stdout + result.stderr

    plan_path = project / "plan.json"
    plan_data = {}
    if plan_path.exists():
        try:
            plan_data = json.loads(plan_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    return {
        "success": result.returncode == 0,
        "plan_path": str(plan_path) if plan_path.exists() else None,
        "tickets": len(plan_data.get("tickets", [])),
        "phases": len(plan_data.get("phases", [])),
        "output": output_text.strip(),
    }


def run_execute(project_path: str, backend: str) -> dict:
    """Execute a plan under governance.

    Args:
        project_path: Path to the project directory containing plan.json.
        backend: AI coder backend to use.

    Returns:
        Dict with pass/fail/skip counts, DoD status, and evidence path.
    """
    project = Path(project_path).resolve()
    plan_path = project / "plan.json"

    if not plan_path.exists():
        raise RuntimeError(f"No plan.json found in {project}. Run planning first.")

    cmd = [
        "saturnday", "run",
        "--plan", str(plan_path),
        "--repo", str(project),
        "--backend", backend,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=28800,  # 8 hours — complex projects need time
        cwd=str(project),
    )

    output_text = result.stdout + result.stderr

    # Parse results from output
    passed = 0
    failed = 0
    skipped = 0
    dod_met = False

    for line in output_text.splitlines():
        stripped = line.strip()
        if "Passed:" in stripped and "Failed:" in stripped:
            parts = stripped.split()
            for i, part in enumerate(parts):
                if part == "Passed:" and i + 1 < len(parts):
                    try:
                        passed = int(parts[i + 1])
                    except ValueError:
                        pass
                if part == "Failed:" and i + 1 < len(parts):
                    try:
                        failed = int(parts[i + 1])
                    except ValueError:
                        pass
                if part == "Skipped:" and i + 1 < len(parts):
                    try:
                        skipped = int(parts[i + 1])
                    except ValueError:
                        pass
        if "DoD:" in stripped and "MET" in stripped and "NOT" not in stripped:
            dod_met = True

    return {
        "success": result.returncode == 0,
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "dod_met": dod_met,
        "exit_code": result.returncode,
        "output": output_text.strip(),
    }


def run_full(project_path: str, brief: str, backend: str) -> dict:
    """Run the full pipeline: plan then execute.

    Args:
        project_path: Path to the project directory.
        brief: Natural-language project description.
        backend: AI coder backend to use.

    Returns:
        Dict with plan and execution results.
    """
    print(f"=== Saturnday Run ===")
    print(f"Project: {project_path}")
    print(f"Backend: {backend}")
    print(f"Brief: {brief[:100]}{'...' if len(brief) > 100 else ''}")
    print()

    # Stage 1: Plan
    print("--- stage: planning ---")
    plan_result = run_plan(project_path, brief, backend)
    if not plan_result["success"]:
        print(f"Planning failed:\n{plan_result['output']}")
        return {"stage": "plan", "error": "Planning failed", **plan_result}

    print(f"Plan generated: {plan_result['tickets']} tickets, {plan_result['phases']} phases")
    print()

    # Stage 2: Execute
    print("--- stage: execute ---")
    exec_result = run_execute(project_path, backend)
    print(f"Passed: {exec_result['passed']}  Failed: {exec_result['failed']}  Skipped: {exec_result['skipped']}")
    print(f"DoD: {'MET' if exec_result['dod_met'] else 'NOT MET'}")

    return {
        "stage": "complete",
        "plan": plan_result,
        "execution": exec_result,
        "dod_met": exec_result["dod_met"],
    }


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/run.py <project-dir> --brief \"description\" [--backend claude-cli]")
        return 2

    project_path = sys.argv[1]
    brief = None
    backend = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--brief" and i + 1 < len(args):
            brief = args[i + 1]
            i += 2
        elif args[i] == "--backend" and i + 1 < len(args):
            backend = args[i + 1]
            i += 2
        else:
            i += 1

    if not brief:
        print("Error: --brief is required", file=sys.stderr)
        return 2

    if not check_saturnday_installed():
        print("Error: saturnday is not installed. Install with: pip install saturnday", file=sys.stderr)
        return 2

    if backend and backend not in VALID_BACKENDS:
        print(f"Error: invalid backend '{backend}'. Valid: {', '.join(sorted(VALID_BACKENDS))}", file=sys.stderr)
        return 2

    if not backend:
        backend = detect_backend()
        if not backend:
            print("Error: no AI coder backend detected. Install claude, codex, or agent CLI.", file=sys.stderr)
            return 2
        print(f"Detected backend: {backend}")

    result = run_full(project_path, brief, backend)
    print()
    print(json.dumps(result, indent=2, default=str))

    if result.get("dod_met"):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
