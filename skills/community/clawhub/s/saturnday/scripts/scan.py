#!/usr/bin/env python3
"""Saturnday skill scanner for OpenClaw.

Scans a skill directory using saturnday scan and returns structured results.
Requires: pip install saturnday

Usage:
    python scripts/scan.py <skill-directory-path> [--format json|text] [--output <dir>]
"""

import json
import subprocess
import sys
import tempfile
from pathlib import Path


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


def run_scan(skill_path: str, output_dir: str | None = None, fmt: str = "json") -> dict:
    """Run saturnday scan on a skill directory.

    Args:
        skill_path: Path to the skill directory to scan.
        output_dir: Optional output directory for evidence. Uses temp dir if None.
        fmt: Output format — 'json', 'markdown', or 'both'.

    Returns:
        Dict with disposition, findings count, and output path.

    Raises:
        RuntimeError: If saturnday is not installed or scan fails to execute.
    """
    skill_path_resolved = Path(skill_path).resolve()
    if not skill_path_resolved.is_dir():
        raise RuntimeError(f"Not a directory: {skill_path_resolved}")

    if not check_saturnday_installed():
        raise RuntimeError(
            "saturnday is not installed. Install with: pip install saturnday"
        )

    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="saturnday-scan-")

    # saturnday scan accepts: json, markdown, both
    scan_fmt = fmt if fmt in ("json", "markdown", "both") else "json"
    cmd = [
        "saturnday", "scan",
        "--skill", str(skill_path_resolved),
        "--output", output_dir,
        "--format", scan_fmt,
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300,
    )

    # Parse output for disposition
    output_text = result.stdout + result.stderr
    disposition = "PASS" if result.returncode == 0 else "FAIL"

    # Try to read the report.json if it exists
    report_path = Path(output_dir) / "report.json"
    report_data = {}
    if report_path.exists():
        try:
            report_data = json.loads(report_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass

    # Extract findings count from nested summary or top level
    findings_count = report_data.get("total_findings", 0)
    if findings_count == 0:
        summary = report_data.get("summary", {})
        findings_count = summary.get("total_findings", 0)

    return {
        "disposition": disposition,
        "exit_code": result.returncode,
        "findings_count": findings_count,
        "output_dir": output_dir,
        "output": output_text.strip(),
        "report": report_data,
    }


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/scan.py <skill-directory-path> [--format json|text] [--output <dir>]")
        return 2

    skill_path = sys.argv[1]
    output_dir = None

    # Simple arg parsing
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_dir = args[i + 1]
            i += 2
        else:
            i += 1

    try:
        result = run_scan(skill_path, output_dir=output_dir)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2))

    return 0 if result["disposition"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
