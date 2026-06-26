#!/usr/bin/env python3
"""Saturnday governance runner for OpenClaw.

Runs full or staged governance checks on a git repository using saturnday.
Requires: pip install saturnday

Usage:
    python scripts/guard.py <repo-path> [--staged] [--policy <path>]
"""

import json
import subprocess
import sys
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


def run_governance(
    repo_path: str,
    *,
    staged: bool = False,
    policy_path: str | None = None,
) -> dict:
    """Run saturnday governance on a repository.

    Args:
        repo_path: Path to the git repository.
        staged: If True, check only staged changes. If False, full repo scan.
        policy_path: Optional path to .saturnday-policy.yaml.

    Returns:
        Dict with disposition, checks run, findings, and evidence path.

    Raises:
        RuntimeError: If saturnday is not installed or repo is invalid.
    """
    repo = Path(repo_path).resolve()
    if not repo.is_dir():
        raise RuntimeError(f"Not a directory: {repo}")
    if not (repo / ".git").exists():
        raise RuntimeError(f"Not a git repository: {repo}")

    if not check_saturnday_installed():
        raise RuntimeError(
            "saturnday is not installed. Install with: pip install saturnday"
        )

    cmd = ["saturnday", "governance", "--repo", str(repo)]

    if staged:
        cmd.append("--staged")
    else:
        cmd.append("--full")

    if policy_path:
        cmd.extend(["--policy", policy_path])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
    )

    output_text = result.stdout + result.stderr
    disposition = "PASS" if result.returncode == 0 else "FAIL"

    # Parse findings count from output
    findings_count = 0
    evidence_path = ""
    for line in output_text.splitlines():
        line_stripped = line.strip()
        if line_stripped.startswith("Total findings:"):
            try:
                findings_count = int(line_stripped.split(":")[1].strip())
            except (ValueError, IndexError):
                pass
        if line_stripped.startswith("Evidence:"):
            evidence_path = line_stripped.split(":", 1)[1].strip()

    return {
        "disposition": disposition,
        "exit_code": result.returncode,
        "findings_count": findings_count,
        "evidence_path": evidence_path,
        "output": output_text.strip(),
    }


def main() -> int:
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python scripts/guard.py <repo-path> [--staged] [--policy <path>]")
        return 2

    repo_path = sys.argv[1]
    staged = False
    policy_path = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--staged":
            staged = True
            i += 1
        elif args[i] == "--policy" and i + 1 < len(args):
            policy_path = args[i + 1]
            i += 2
        else:
            i += 1

    try:
        result = run_governance(repo_path, staged=staged, policy_path=policy_path)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(result, indent=2))
    return 0 if result["disposition"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
