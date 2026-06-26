#!/usr/bin/env python
"""
Optimize Python code via profiling and code quality checks.

Usage:
    python optimize_code.py --code "path/to/code.py" --profile "path/to/profile.prof" --report "path/to/opt_report.json"
"""

import argparse
import json
import os
import subprocess
import sys
import pstats
import io
from datetime import datetime
from pathlib import Path
from pathlib import Path

# Default configuration
DEFAULT_CONDA_PATH = r"C:\anaconda3\condabin\conda.bat"
DEFAULT_ENV = "py311"
PROJECT_DIR = r"H:\code\Daily"

def activate_conda_and_run(command: list, cwd: str = None) -> tuple[int, str, str]:
    """Activate conda environment and run a command."""
    if cwd is None:
        cwd = PROJECT_DIR

    # Note: Path has no spaces, so no quoting needed
    conda_activate_cmd = f'call {DEFAULT_CONDA_PATH} activate {DEFAULT_ENV}'
    full_cmd = f"{conda_activate_cmd} && {' '.join(command)}"

    proc = subprocess.run(
        ["cmd.exe", "/c", full_cmd],
        capture_output=True,
        text=True,
        cwd=cwd,
        env=os.environ.copy()
    )

    return proc.returncode, proc.stdout, proc.stderr

def profile_code(code_path: str, profile_output: str = None) -> dict:
    """
    Profile the Python code using cProfile.

    Args:
        code_path: Path to Python file to profile
        profile_output: Path to save raw profile data (default: auto)

    Returns:
        Dictionary with profiling stats
    """
    code_file = Path(code_path)
    if not code_file.exists():
        return {"error": f"Code file not found: {code_file}"}

    if not profile_output:
        profile_dir = Path(PROJECT_DIR) / "profiles"
        profile_dir.mkdir(parents=True, exist_ok=True)
        profile_output = str(profile_dir / f"profile_{code_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.prof")

    print(f"Profiling {code_path}...")

    # Run the code with profiling
    cmd = ["python", "-m", "cProfile", "-o", profile_output, str(code_file)]
    returncode, stdout, stderr = activate_conda_and_run(cmd)

    if returncode != 0:
        return {
            "error": "Profiling failed",
            "returncode": returncode,
            "stderr": stderr,
            "stdout": stdout
        }

    # Parse the profile data
    stats = pstats.Stats(profile_output)
    stats.strip_dirs()

    # Get top time-consuming functions
    top_functions = []
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        # func is (filename, line_number, function_name)
        file_name, line_num, func_name = func
        top_functions.append({
            "function": func_name,
            "file": Path(file_name).name,
            "line": line_num,
            "calls": nc,
            "total_time": tt,
            "cumulative_time": ct
        })

    # Sort by cumulative time
    top_functions.sort(key=lambda x: x["cumulative_time"], reverse=True)

    # Take top 20
    top_20 = top_functions[:20]

    return {
        "profile_file": profile_output,
        "top_functions": top_20,
        "total_functions": len(top_functions),
        "code_file": str(code_file)
    }

def check_code_quality(code_path: str) -> dict:
    """
    Run pylint/flake8 on the code to check quality.

    Returns a dictionary with quality metrics and warnings.
    """
    code_file = Path(code_path)
    if not code_file.exists():
        return {"error": f"Code file not found: {code_file}"}

    print(f"Running code quality checks on {code_path}...")

    results = {
        "pylint": None,
        "flake8": None
    }

    # Try pylint
    try:
        cmd = ["pylint", str(code_file), "--output-format=json"]
        returncode, stdout, stderr = activate_conda_and_run(cmd)
        # Pylint may return non-zero even with valid JSON output. Try to parse if any output.
        output = stdout if stdout.strip() else stderr
        if output.strip():
            try:
                pylint_issues = json.loads(output)
                results["pylint"] = {
                    "status": "success",
                    "issues": pylint_issues,
                    "count": len(pylint_issues)
                }
            except json.JSONDecodeError:
                results["pylint"] = {
                    "status": "parse_error",
                    "raw_output": output[:1000]
                }
        else:
            results["pylint"] = {
                "status": "failed",
                "returncode": returncode,
                "stderr": stderr[:1000]
            }
    except Exception as e:
        results["pylint"] = {"status": "error", "message": str(e)}

    # Try flake8
    try:
        cmd = ["flake8", str(code_file), "--format=json"]
        returncode, stdout, stderr = activate_conda_and_run(cmd)
        # flake8 returns 0 (no issues) or 1 (issues found) but may output to stdout or stderr.
        output = stdout if stdout.strip() else stderr
        if output.strip():
            try:
                flake8_issues = json.loads(output)
                results["flake8"] = {
                    "status": "success",
                    "issues": flake8_issues,
                    "count": len(flake8_issues)
                }
            except json.JSONDecodeError:
                results["flake8"] = {
                    "status": "parse_error",
                    "raw_output": output[:1000]
                }
        else:
            results["flake8"] = {
                "status": "failed",
                "returncode": returncode,
                "stderr": stderr[:1000]
            }
    except Exception as e:
        results["flake8"] = {"status": "error", "message": str(e)}

    return results

def generate_suggestions(profile_data: dict, quality_data: dict) -> list:
    """
    Generate optimization suggestions based on profiling and quality metrics.
    """
    suggestions = []

    # Profiling suggestions
    if "top_functions" in profile_data:
        top = profile_data["top_functions"][:5]
        if top:
            suggestions.append({
                "type": "profile",
                "priority": "high",
                "message": f"Top time-consuming function: {top[0]['function']} (cumulative: {top[0]['cumulative_time']:.4f}s)",
                "details": f"Consider optimizing {top[0]['function']} in {top[0]['file']}:{top[0]['line']}"
            })
            # Check for functions with high call count
            high_call = [f for f in top if f['calls'] > 1000]
            if high_call:
                suggestions.append({
                    "type": "profile",
                    "priority": "medium",
                    "message": f"Functions with high call count detected: {len(high_call)} functions called >1000 times",
                    "details": ", ".join(f"{f['function']}({f['calls']} calls)" for f in high_call[:3])
                })

    # Code quality suggestions
    if quality_data.get("pylint", {}).get("status") == "success":
        pylint_issues = quality_data["pylint"].get("issues", [])
        error_issues = [i for i in pylint_issues if i.get("type") in ("error", "fatal")]
        if error_issues:
            suggestions.append({
                "type": "quality",
                "priority": "high",
                "message": f"Pylint found {len(error_issues)} blocking issues",
                "details": "; ".join(f"{i['message']} ({i['path']}:{i['line']})" for i in error_issues[:3])
            })

        warn_issues = [i for i in pylint_issues if i.get("type") == "warning"]
        if warn_issues:
            suggestions.append({
                "type": "quality",
                "priority": "low",
                "message": f"Pylint warnings: {len(warn_issues)}",
                "details": "Review warnings for code improvement opportunities"
            })

    if quality_data.get("flake8", {}).get("status") == "success":
        flake8_issues = quality_data["flake8"].get("issues", [])
        if flake8_issues:
            suggestions.append({
                "type": "quality",
                "priority": "medium",
                "message": f"Flake8 found {len(flake8_issues)} style issues",
                "details": f"Example: {flake8_issues[0].get('message', 'N/A')}"
            })

    # General suggestions
    suggestions.append({
        "type": "general",
        "priority": "info",
        "message": "Optimization complete. Review profile data for bottlenecks.",
        "details": "Consider algorithmic improvements, caching, or vectorization if applicable."
    })

    return suggestions

def main():
    parser = argparse.ArgumentParser(description="Profile and optimize Python code")
    parser.add_argument("--code", required=True, help="Python file to optimize")
    parser.add_argument("--profile", help="Output path for profile data (optional)")
    parser.add_argument("--report", help="Output JSON report path (optional)")
    parser.add_argument("--run-profile", action="store_true", help="Actually run profiling (may take time)")

    args = parser.parse_args()

    code_path = Path(args.code)
    if not code_path.exists():
        print(f"Error: Code file not found: {code_path}")
        sys.exit(1)

    # Determine report path
    if args.report:
        report_path = Path(args.report)
    else:
        reports_dir = Path(PROJECT_DIR) / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = reports_dir / f"optimization_{timestamp}.json"

    # Collect data
    profile_data = {}
    if args.run_profile:
        profile_data = profile_code(str(code_path), args.profile)
    else:
        profile_data = {"note": "Profiling not run (use --run-profile to enable)"}

    quality_data = check_code_quality(str(code_path))

    # Generate suggestions
    try:
        suggestions = generate_suggestions(profile_data, quality_data)
    except Exception as e:
        suggestions = [{
            "type": "error",
            "priority": "high",
            "message": f"Failed to generate suggestions: {e}",
            "details": "Check profile_data and quality_data for errors."
        }]

    # Assemble report
    report = {
        "timestamp": datetime.now().isoformat(),
        "code_file": str(code_path),
        "profile_data": profile_data,
        "quality_data": quality_data,
        "suggestions": suggestions
    }

    # Write report
    with open(report_path, 'w', encoding='utf-8') as f:
        # Use default=str to handle non-serializable objects
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    print(f"\nOptimization report written to: {report_path}")
    print(f"\nTop suggestions:")

    for s in suggestions[:5]:
        print(f"- [{s['priority']}] {s['message']}")
        if s.get('details'):
            print(f"  Details: {s['details']}")

    return str(report_path)

if __name__ == "__main__":
    output_report = main()
    print(f"REPORT_PATH:{output_report}")
