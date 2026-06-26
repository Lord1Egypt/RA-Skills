"""Verification gates — deterministic checks on agent output.

Standalone reimplementation inspired by governed-agents verification.
No LLM needed. Pure code. 4 gates:
  1. Files exist + non-empty
  2. Python syntax (AST parse)
  3. Tests pass (subprocess)
  4. Lint clean (subprocess, optional)
"""

import ast
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class GateResult:
    """Result of a single verification gate check."""

    name: str
    passed: bool
    detail: str = ""


@dataclass
class VerificationResult:
    """Aggregated result across all gates."""

    passed: bool = False
    checks: list[GateResult] = field(default_factory=list)
    summary: str = ""

    def add(self, name: str, passed: bool, detail: str = "") -> None:
        """Add a gate check result."""
        self.checks.append(GateResult(name=name, passed=passed, detail=detail))

    def evaluate(self) -> "VerificationResult":
        """Compute overall pass/fail from individual checks."""
        self.passed = all(c.passed for c in self.checks) if self.checks else False
        failed = [c for c in self.checks if not c.passed]
        if failed:
            self.summary = "FAILED: " + "; ".join(
                f"{c.name}: {c.detail}" for c in failed
            )
        else:
            self.summary = f"ALL {len(self.checks)} CHECKS PASSED"
        return self


def verify_files_exist(files: list[str], base_dir: str = ".") -> VerificationResult:
    """Gate 1: Do the required output files actually exist and are non-empty?"""
    result = VerificationResult()
    for f in files:
        path = Path(base_dir) / f
        exists = path.exists()
        size = path.stat().st_size if exists else 0
        if exists and size > 0:
            result.add(f"file_exists:{f}", True, f"{size}B")
        elif exists:
            result.add(f"file_exists:{f}", False, "file is empty (0B)")
        else:
            result.add(f"file_exists:{f}", False, "FILE NOT FOUND")
    return result.evaluate()


def verify_python_syntax(files: list[str], base_dir: str = ".") -> VerificationResult:
    """Gate 2: Does the Python code parse without syntax errors?"""
    result = VerificationResult()
    for f in files:
        if not f.endswith(".py"):
            continue
        path = Path(base_dir) / f
        if not path.exists():
            result.add(f"syntax:{f}", False, "file not found")
            continue
        try:
            source = path.read_text()
            ast.parse(source)
            result.add(f"syntax:{f}", True, "valid Python")
        except SyntaxError as e:
            result.add(f"syntax:{f}", False, f"SyntaxError line {e.lineno}: {e.msg}")
    return result.evaluate()


def verify_tests(
    test_command: str, cwd: str = ".", timeout: int = 60
) -> VerificationResult:
    """Gate 3: Run tests and check they pass."""
    result = VerificationResult()
    try:
        proc = subprocess.run(
            shlex.split(test_command),
            shell=False,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        passed = proc.returncode == 0
        output = (proc.stdout + proc.stderr)[-500:]
        result.add(
            "tests", passed, "all passed" if passed else output.strip()
        )
    except subprocess.TimeoutExpired:
        result.add("tests", False, f"TIMEOUT after {timeout}s")
    except Exception as e:
        result.add("tests", False, str(e))
    return result.evaluate()


def verify_lint(
    files: list[str],
    base_dir: str = ".",
    timeout: int = 15,
    linter: Optional[str] = None,
) -> VerificationResult:
    """Gate 4: Run linter (optional — skipped if no linter available)."""
    result = VerificationResult()

    # Auto-detect linter if not specified
    if linter is None:
        for candidate in ["ruff check", "flake8", "pylint --errors-only"]:
            bin_name = candidate.split()[0]
            check = subprocess.run(
                ["which", bin_name], capture_output=True, text=True
            )
            if check.returncode == 0:
                linter = candidate
                break

    if linter is None:
        result.add("lint", True, "no linter available — skipped")
        return result.evaluate()

    py_files = [f for f in files if f.endswith(".py")]
    if not py_files:
        result.add("lint", True, "no Python files to lint")
        return result.evaluate()

    file_args = " ".join(str(Path(base_dir) / f) for f in py_files)
    cmd = f"{linter} {file_args}"

    try:
        proc = subprocess.run(
            shlex.split(cmd), shell=False, capture_output=True, text=True, timeout=timeout
        )
        passed = proc.returncode == 0
        output = (proc.stdout + proc.stderr)[-300:]
        result.add("lint", passed, "clean" if passed else output.strip())
    except subprocess.TimeoutExpired:
        result.add("lint", False, f"TIMEOUT after {timeout}s")
    except Exception as e:
        result.add("lint", False, str(e))

    return result.evaluate()


def run_full_verification(
    required_files: list[str],
    test_command: Optional[str] = None,
    base_dir: str = ".",
    run_lint: bool = False,
) -> VerificationResult:
    """Run all applicable verification gates.

    Args:
        required_files: Files that must exist.
        test_command: Shell command to run tests (None = skip).
        base_dir: Working directory.
        run_lint: Whether to run lint gate.

    Returns:
        Combined VerificationResult across all gates.
    """
    combined = VerificationResult()

    # Gate 1: Files exist
    if required_files:
        r = verify_files_exist(required_files, base_dir)
        combined.checks.extend(r.checks)

    # Gate 2: Python syntax
    py_files = [f for f in required_files if f.endswith(".py")]
    if py_files:
        r = verify_python_syntax(py_files, base_dir)
        combined.checks.extend(r.checks)

    # Gate 3: Tests
    if test_command:
        r = verify_tests(test_command, base_dir)
        combined.checks.extend(r.checks)

    # Gate 4: Lint (optional)
    if run_lint and py_files:
        r = verify_lint(py_files, base_dir)
        combined.checks.extend(r.checks)

    return combined.evaluate()
