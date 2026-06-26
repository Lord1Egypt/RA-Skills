# Verify Action Script — Mandatory Proof of Action Protocol

Validates that an agent's claimed action actually occurred. This script is the enforcement mechanism for the Anti-Micromanagement Guard. Instead of building "auditor agents" to watch other agents, this script provides deterministic, verifiable proof.

## Purpose

Every time an agent claims "Done," this script runs three checks to verify the claim is real and not an "AI Execution Hallucination" — a documented failure mode where agents confidently report completing actions they never took.

## The Three Verification Checks

| # | Check | What It Validates | Failure Meaning |
|---|-------|-------------------|-----------------|
| 1 | **File Exists** | Does the file exist at the claimed path? | Action was likely hallucinated entirely |
| 2 | **Content Match** | Does the file contain the expected content substring? | Agent wrote wrong data or a placeholder |
| 3 | **Timestamp Fresh** | Was the file modified within the allowed time window? | Agent is referencing a stale pre-existing file |

## Usage

```bash
python verify_action.py --path <file_path> --expected <expected_content> [--max-age <seconds>]
```

**Parameters:**

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--path` | Yes | — | File path the agent claims to have written |
| `--expected` | Yes | — | Expected content substring to verify |
| `--max-age` | No | 300 | Maximum file age in seconds |

**Exit Codes:**
- `0` — All checks passed. Action verified.
- `1` — One or more checks failed. Action NOT verified.

## Output Format

The script prints a JSON report to stdout:

```json
{
  "verification_time": "2026-04-15T10:54:09.462914",
  "claimed_path": "/path/to/file.txt",
  "overall_verdict": "PASS — Action verified",
  "checks": [
    {
      "check": "file_exists",
      "path": "/path/to/file.txt",
      "passed": true,
      "detail": "File found"
    },
    {
      "check": "content_match",
      "passed": true,
      "tail_3_lines": ["line1", "line2", "line3"],
      "detail": "Content verified"
    },
    {
      "check": "timestamp_fresh",
      "passed": true,
      "file_modified": "2026-04-15T10:53:58.278625",
      "age_seconds": 11.2,
      "max_age_seconds": 300,
      "detail": "File modified 11.2s ago"
    }
  ]
}
```

## Source Code

```python
#!/usr/bin/env python3
"""
Verify Action Script — Mandatory Proof of Action Protocol
Validates that an agent's claimed action actually occurred.

Usage:
    python verify_action.py --path <file_path> --expected <expected_content> [--max-age <seconds>]

Returns:
    Exit code 0 if all checks pass, exit code 1 if any check fails.
    Prints a JSON report with pass/fail status for each check.
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime


def verify_file_exists(file_path: str) -> dict:
    """Check 1: Does the file exist at the claimed path?"""
    exists = os.path.isfile(file_path)
    return {
        "check": "file_exists",
        "path": file_path,
        "passed": exists,
        "detail": "File found" if exists else "FILE NOT FOUND — action likely hallucinated"
    }


def verify_content(file_path: str, expected_content: str) -> dict:
    """Check 2: Does the file contain the expected content?"""
    if not os.path.isfile(file_path):
        return {
            "check": "content_match",
            "passed": False,
            "detail": "Cannot verify content — file does not exist"
        }
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            actual = f.read()
        match = expected_content.strip() in actual
        tail_lines = actual.strip().split("\n")[-3:]
        return {
            "check": "content_match",
            "passed": match,
            "tail_3_lines": tail_lines,
            "detail": "Content verified" if match else "CONTENT MISMATCH — agent may have written wrong data"
        }
    except Exception as e:
        return {
            "check": "content_match",
            "passed": False,
            "detail": f"Error reading file: {str(e)}"
        }


def verify_timestamp(file_path: str, max_age_seconds: int = 300) -> dict:
    """Check 3: Was the file modified recently (within max_age_seconds)?"""
    if not os.path.isfile(file_path):
        return {
            "check": "timestamp_fresh",
            "passed": False,
            "detail": "Cannot verify timestamp — file does not exist"
        }
    try:
        mtime = os.path.getmtime(file_path)
        age = time.time() - mtime
        fresh = age <= max_age_seconds
        return {
            "check": "timestamp_fresh",
            "passed": fresh,
            "file_modified": datetime.fromtimestamp(mtime).isoformat(),
            "age_seconds": round(age, 1),
            "max_age_seconds": max_age_seconds,
            "detail": f"File modified {round(age, 1)}s ago" if fresh else f"FILE STALE — modified {round(age, 1)}s ago (max: {max_age_seconds}s)"
        }
    except Exception as e:
        return {
            "check": "timestamp_fresh",
            "passed": False,
            "detail": f"Error checking timestamp: {str(e)}"
        }


def run_verification(file_path: str, expected_content: str, max_age: int) -> dict:
    """Run all three verification checks and produce a report."""
    checks = [
        verify_file_exists(file_path),
        verify_content(file_path, expected_content),
        verify_timestamp(file_path, max_age)
    ]
    all_passed = all(c["passed"] for c in checks)
    report = {
        "verification_time": datetime.now().isoformat(),
        "claimed_path": file_path,
        "overall_verdict": "PASS — Action verified" if all_passed else "FAIL — Action NOT verified",
        "checks": checks
    }
    return report


def main():
    parser = argparse.ArgumentParser(description="Verify agent action proof")
    parser.add_argument("--path", required=True, help="File path the agent claims to have written")
    parser.add_argument("--expected", required=True, help="Expected content substring")
    parser.add_argument("--max-age", type=int, default=300, help="Max file age in seconds (default: 300)")
    args = parser.parse_args()

    report = run_verification(args.path, args.expected, args.max_age)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["overall_verdict"].startswith("PASS") else 1)


if __name__ == "__main__":
    main()
```

## Integration

When using this script within the AI Engineering OS workflow, call it at the end of Phase 3 (Pre-Deployment Audit) for every file the agent claims to have created or modified. If any check fails, the agent's action is rejected and must be re-executed.
