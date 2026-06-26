#!/usr/bin/env python3
"""Run the repo release verification chain from one entry point."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Step:
    name: str
    command: list[str]
    cwd: str


@dataclass(frozen=True)
class StepResult:
    name: str
    command: str
    cwd: str
    ok: bool
    returncode: int
    stdout: str
    stderr: str


def command_string(command: list[str], root: Path | None = None) -> str:
    normalized = list(command)
    if normalized and Path(normalized[0]).resolve() == Path(sys.executable).resolve():
        normalized[0] = "python"
    if root is not None:
        repo_root = root.resolve()
        for index, token in enumerate(normalized[1:], start=1):
            try:
                token_path = Path(token).resolve()
            except OSError:
                continue
            try:
                normalized[index] = token_path.relative_to(repo_root).as_posix()
            except ValueError:
                continue
    return subprocess.list2cmdline(normalized)


def resolve(root: Path, relative_path: str) -> Path:
    return (root / relative_path).resolve()


def build_steps(root: Path, args: argparse.Namespace) -> list[Step]:
    python = sys.executable
    steps: list[Step] = []

    if not args.skip_cleanup:
        steps.append(
            Step(
                name="cleanup-generated",
                command=[python, str(resolve(root, "scripts/clean-generated.py")), "--root", str(root)],
                cwd=str(root),
            )
        )

    if not args.skip_pytest:
        steps.append(
            Step(
                name="pytest",
                command=[python, "-m", "pytest", "-q", f"--basetemp={args.basetemp}"],
                cwd=str(root),
            )
        )

    if not args.skip_evals:
        steps.append(
            Step(
                name="report-evals",
                command=[
                    python,
                    str(resolve(root, "scripts/run-report-evals.py")),
                    "--root",
                    str(root),
                    "--packet-dir",
                    str(resolve(root, args.packet_dir)),
                ],
                cwd=str(root),
            )
        )

    if not args.skip_late_context_evals:
        steps.append(
            Step(
                name="late-context-evals",
                command=[
                    python,
                    str(resolve(root, "scripts/run-late-context-evals.py")),
                    "--root",
                    str(root),
                    "--format",
                    "json",
                    "--json-out",
                    str(resolve(root, args.late_context_json_out)),
                ],
                cwd=str(root),
            )
        )

    if not args.skip_doc_sync:
        steps.append(
            Step(
                name="doc-sync",
                command=[
                    python,
                    str(resolve(root, "check-doc-sync.py")),
                    "--root",
                    str(root),
                    "--dry-run",
                ],
                cwd=str(root),
            )
        )

    if not args.skip_export_smoke:
        output = resolve(root, args.export_output)
        output.parent.mkdir(parents=True, exist_ok=True)
        steps.append(
            Step(
                name="export-smoke",
                command=[
                    python,
                    str(resolve(root, "scripts/export-image.py")),
                    str(resolve(root, args.export_fixture)),
                    "--mode",
                    "desktop",
                    "--output",
                    str(output),
                ],
                cwd=str(root),
            )
        )

    if not args.skip_cleanup:
        steps.append(
            Step(
                name="cleanup-generated-final",
                command=[python, str(resolve(root, "scripts/clean-generated.py")), "--root", str(root)],
                cwd=str(root),
            )
        )

    return steps


def dry_run_payload(steps: list[Step]) -> dict[str, object]:
    return {
        "steps": [
            {
                "name": step.name,
                "command": command_string(step.command, Path(step.cwd)),
                "cwd": step.cwd,
            }
            for step in steps
        ]
    }


def run_steps(steps: list[Step]) -> list[StepResult]:
    results: list[StepResult] = []
    for index, step in enumerate(steps):
        completed = subprocess.run(
            step.command,
            cwd=step.cwd,
            capture_output=True,
            text=True,
            timeout=900,
        )
        results.append(
            StepResult(
                name=step.name,
                command=command_string(step.command, Path(step.cwd)),
                cwd=step.cwd,
                ok=completed.returncode == 0,
                returncode=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
            )
        )
        if completed.returncode != 0:
            for cleanup_step in steps[index + 1 :]:
                if not cleanup_step.name.startswith("cleanup-generated"):
                    continue
                cleanup_completed = subprocess.run(
                    cleanup_step.command,
                    cwd=cleanup_step.cwd,
                    capture_output=True,
                    text=True,
                    timeout=900,
                )
                results.append(
                    StepResult(
                        name=cleanup_step.name,
                        command=command_string(cleanup_step.command, Path(cleanup_step.cwd)),
                        cwd=cleanup_step.cwd,
                        ok=cleanup_completed.returncode == 0,
                        returncode=cleanup_completed.returncode,
                        stdout=cleanup_completed.stdout,
                        stderr=cleanup_completed.stderr,
                    )
                )
            break
    return results


def print_text_results(results: list[StepResult]) -> int:
    failures = 0
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"{status} {result.name}")
        print(f"  cwd: {result.cwd}")
        print(f"  cmd: {result.command}")
        if result.stdout.strip():
            print("  stdout:")
            for line in result.stdout.strip().splitlines():
                print(f"    {line}")
        if result.stderr.strip():
            print("  stderr:")
            for line in result.stderr.strip().splitlines():
                print(f"    {line}")
        if not result.ok:
            failures += 1
    print()
    print(f"Summary: {len(results) - failures} passed, {failures} failed.")
    return 0 if failures == 0 else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format.")
    parser.add_argument("--dry-run", action="store_true", help="Print the verification plan without running it.")
    parser.add_argument("--skip-pytest", action="store_true", help="Skip the full pytest run.")
    parser.add_argument("--skip-evals", action="store_true", help="Skip scripts/run-report-evals.py.")
    parser.add_argument("--skip-late-context-evals", action="store_true", help="Skip scripts/run-late-context-evals.py.")
    parser.add_argument("--skip-doc-sync", action="store_true", help="Skip check-doc-sync.py.")
    parser.add_argument("--skip-export-smoke", action="store_true", help="Skip the screenshot export smoke check.")
    parser.add_argument("--skip-cleanup", action="store_true", help="Skip generated cache cleanup before/after verification.")
    parser.add_argument("--basetemp", default=".tmp/pytest", help="Pytest base temp path relative to repo root.")
    parser.add_argument(
        "--packet-dir",
        default=".tmp/verify-release/eval-packets",
        help="Eval packet output dir relative to repo root.",
    )
    parser.add_argument(
        "--late-context-json-out",
        default=".tmp/verify-release/late-context-evals.json",
        help="Output path for late-context eval JSON, relative to repo root.",
    )
    parser.add_argument(
        "--export-fixture",
        default="tests/fixtures/minimal_report.html",
        help="HTML file used for export smoke verification, relative to repo root.",
    )
    parser.add_argument(
        "--export-output",
        default=".tmp/verify-release/export-smoke-desktop.png",
        help="Output path for the export smoke image, relative to repo root.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    steps = build_steps(root, args)

    if args.dry_run:
        payload = dry_run_payload(steps)
        if args.format == "json":
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            for step in payload["steps"]:
                print(f"PLAN {step['name']}")
                print(f"  cwd: {step['cwd']}")
                print(f"  cmd: {step['command']}")
        return 0

    results = run_steps(steps)
    payload = {
        "steps": [asdict(result) for result in results],
        "summary": {
            "total": len(steps),
            "executed": len(results),
            "failed": sum(1 for result in results if not result.ok),
        },
    }
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0 if payload["summary"]["failed"] == 0 and payload["summary"]["executed"] == payload["summary"]["total"] else 1
    return print_text_results(results)


if __name__ == "__main__":
    sys.exit(main())
