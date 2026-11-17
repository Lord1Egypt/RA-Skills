#!/usr/bin/env python3
"""Run test coverage and emit a concise summary of uncovered lines.

Supports Python (pytest-cov / coverage.py) and JavaScript/TypeScript
(jest / vitest). Pure stdlib; shells out to the project's test runner.

Usage:
    python3 scripts/run_coverage.py ./src --lang python
    python3 scripts/run_coverage.py ./src --lang js
"""
import argparse
import json
import os
import shutil
import subprocess
import sys


def run(cmd):
    print(f"+ {' '.join(cmd)}", file=sys.stderr)
    return subprocess.run(cmd, capture_output=True, text=True)


def python_coverage(path):
    if shutil.which("pytest"):
        res = run([
            sys.executable, "-m", "pytest", f"--cov={path}",
            "--cov-report=term-missing", f"--cov-report=annotate:cov_annotate",
        ])
    elif shutil.which("coverage") or shutil.which("python3"):
        # Fallback: coverage.py if available
        run([sys.executable, "-m", "coverage", "run", "-m", "pytest"])
        res = run([sys.executable, "-m", "coverage", "report", "-m"])
    else:
        print("ERROR: pytest not found. `pip install pytest pytest-cov`", file=sys.stderr)
        return 2
    print(res.stdout)
    if res.stderr:
        print(res.stderr, file=sys.stderr)
    missing = [ln for ln in res.stdout.splitlines() if "%" in ln and ("-" in ln or "," in ln)]
    if missing:
        print("\n=== Uncovered (file  coverage  missing-lines) ===")
        for ln in missing:
            print(ln)
        print("\nAnnotated sources in: cov_annotate/  (lines marked '!' are untested)")
    return res.returncode


def detect_js_runner(root="."):
    """Return 'jest' or 'vitest' based on what the project actually uses.

    Probing `shutil.which("npx")` is useless here: npx always exists and will
    happily download whichever runner you name, so a naive probe picks vitest
    even in a jest repo and then dies on jest-only flags. Look at the installed
    binaries and package.json instead.
    """
    for name in ("jest", "vitest"):
        if os.path.exists(os.path.join(root, "node_modules", ".bin", name)):
            return name
    pkg_path = os.path.join(root, "package.json")
    if os.path.exists(pkg_path):
        try:
            with open(pkg_path, encoding="utf-8") as fh:
                pkg = json.load(fh)
        except (OSError, ValueError):
            pkg = {}
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        for name in ("jest", "vitest"):
            if name in deps:
                return name
        test_script = str(pkg.get("scripts", {}).get("test", ""))
        for name in ("jest", "vitest"):
            if name in test_script:
                return name
    for name in ("jest", "vitest"):
        if os.path.exists(os.path.join(root, f"{name}.config.js")) or os.path.exists(
            os.path.join(root, f"{name}.config.ts")
        ):
            return name
    return "jest"


def js_coverage(path):
    if not shutil.which("npx"):
        print("ERROR: npx not found. Install Node.js, jest or vitest.", file=sys.stderr)
        return 2
    runner_name = detect_js_runner()
    print(f"detected JS test runner: {runner_name}", file=sys.stderr)
    # The include flag is runner-specific; passing jest's flag to vitest is a
    # hard CACError, and vice versa.
    if runner_name == "vitest":
        cmd = ["npx", "vitest", "run", "--coverage", f"--coverage.include={path}/**"]
    else:
        cmd = [
            "npx",
            "jest",
            "--coverage",
            f"--collectCoverageFrom={path}/**",
            "--coverageReporters=text",
        ]
    res = run(cmd)
    print(res.stdout)
    if res.stderr:
        print(res.stderr, file=sys.stderr)
    # jest prints a coverage table; surface lines containing a % and file path
    table = [ln for ln in res.stdout.splitlines() if "%" in ln and ("|" in ln or "File" in ln)]
    if table:
        print("\n=== Coverage table (excerpt) ===")
        print("\n".join(table[:40]))
    return res.returncode


def main():
    ap = argparse.ArgumentParser(description="Run test coverage and summarize uncovered lines.")
    ap.add_argument("path", help="package/module path to measure")
    ap.add_argument("--lang", choices=["python", "js"], required=True)
    args = ap.parse_args()
    if args.lang == "python":
        return python_coverage(args.path)
    return js_coverage(args.path)


if __name__ == "__main__":
    sys.exit(main())
