#!/usr/bin/env python
"""
Run tests with pytest in the conda environment and generate a report.

Usage:
    python run_tests.py --test-dir "H:\code\Daily\tests" --code-dir "H:\code\Daily" --report "H:\code\Daily\reports\report_20260310.json"
"""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

# Default configuration
DEFAULT_CONDA_PATH = r"C:\anaconda3\condabin\conda.bat"
DEFAULT_ENV = "py311"
PROJECT_DIR = r"H:\code\Daily"

def activate_conda_and_run(command: list) -> tuple[int, str, str]:
    """
    Activate conda environment and run a command.
    Returns (return_code, stdout, stderr)
    """
    # Build command to activate conda env and run the command
    # Note: Path has no spaces, so no quoting needed
    conda_activate_cmd = f'call {DEFAULT_CONDA_PATH} activate {DEFAULT_ENV}'
    full_cmd = f"{conda_activate_cmd} && {' '.join(command)}"

    # Run via cmd.exe
    proc = subprocess.run(
        ["cmd.exe", "/c", full_cmd],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR,
        env=os.environ.copy()
    )

    return proc.returncode, proc.stdout, proc.stderr

def run_tests(test_dir: str, code_dir: str = None, junit_xml: str = None) -> dict:
    """
    Run pytest on the given test directory.

    Args:
        test_dir: Directory containing test files
        code_dir: Directory containing source code (added to PYTHONPATH)
        junit_xml: Optional path for JUnit XML report

    Returns:
        Dictionary with test results and report info
    """
    test_path = Path(test_dir)
    if not test_path.exists():
        return {"error": f"Test directory not found: {test_dir}"}

    # Prepare command
    cmd = ["pytest", str(test_path), "-v", "--tb=short"]
    if junit_xml:
        cmd.extend(["--junit-xml", junit_xml])

    # Set PYTHONPATH to include code directory
    env = os.environ.copy()
    if code_dir:
        pythonpath = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{code_dir};{pythonpath}" if pythonpath else code_dir

    print(f"Running tests in: {test_dir}")
    print(f"Command: {' '.join(cmd)}")

    # Run in conda environment
    returncode, stdout, stderr = activate_conda_and_run(cmd)

    # Parse results
    lines = stdout.split('\n')
    summary_line = [line for line in lines if "passed" in line or "failed" in line or "error" in line]
    summary = summary_line[-1] if summary_line else "No summary found"

    # Count passed/failed
    passed = stdout.count(" PASSED")
    failed = stdout.count(" FAILED")
    errors = stdout.count(" ERROR")

    result = {
        "timestamp": datetime.now().isoformat(),
        "test_dir": str(test_dir),
        "return_code": returncode,
        "passed": passed,
        "failed": failed,
        "errors": errors,
        "summary": summary.strip(),
        "stdout": stdout[-5000:] if len(stdout) > 5000 else stdout,  # Truncate for brevity
        "stderr": stderr[-5000:] if len(stderr) > 5000 else stderr
    }

    return result

def main():
    parser = argparse.ArgumentParser(description="Run pytest in conda environment and generate report")
    parser.add_argument("--test-dir", required=True, help="Directory containing test files")
    parser.add_argument("--code-dir", default=PROJECT_DIR, help="Directory with source code (default: project dir)")
    parser.add_argument("--report", help="Output JSON report path (default: auto-generated in reports/)")

    args = parser.parse_args()

    # Determine report path
    if args.report:
        report_path = Path(args.report)
    else:
        reports_dir = Path(PROJECT_DIR) / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"test_report_{timestamp}.json"

    # Run tests
    results = run_tests(args.test_dir, args.code_dir)

    # Write report
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Test report written to: {report_path}")
    print(f"Results: {results.get('passed', 0)} passed, {results.get('failed', 0)} failed, {results.get('errors', 0)} errors")
    print(f"Summary: {results.get('summary', 'N/A')}")

    # Print to console for immediate feedback
    print("\n--- Test Output ---")
    print(results.get("stdout", "No output"))

    return str(report_path)

if __name__ == "__main__":
    output_report = main()
    print(f"REPORT_PATH:{output_report}")
