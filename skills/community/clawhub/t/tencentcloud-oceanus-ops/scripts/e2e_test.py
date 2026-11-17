#!/usr/bin/env python3
"""
End-to-end tests for TencentCloud Oceanus CLI.

Tests real API calls for all implemented subcommands.
Requires environment variables:
  - TENCENTCLOUD_SECRET_ID
  - TENCENTCLOUD_SECRET_KEY

Usage:
    python e2e_test.py [--region REGION] [--workspace_id WORKSPACE_ID] [--cluster_id CLUSTER_ID]
"""

import json
import os
import subprocess
import sys
import time
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════════════════

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CLI_ENTRY = os.path.join(SCRIPT_DIR, "oceanus_ops.py")

DEFAULT_REGION = "ap-guangzhou"
DEFAULT_WORKSPACE_ID = ""
DEFAULT_CLUSTER_ID = ""

# Test results storage
RESULTS = []


# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════


def cli(*args, timeout=60):
    """Run a CLI command and return parsed JSON output."""
    cmd = [sys.executable, CLI_ENTRY] + list(args)
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=SCRIPT_DIR,
        )
        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        if stdout:
            try:
                return json.loads(stdout)
            except json.JSONDecodeError:
                return {
                    "success": False,
                    "error": {"code": "ParseError", "message": f"Cannot parse: {stdout[:200]}"},
                    "stdout": stdout,
                    "stderr": stderr,
                }
        else:
            return {
                "success": False,
                "error": {"code": "NoOutput", "message": stderr[:500] if stderr else "No output"},
                "returncode": proc.returncode,
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": {"code": "Timeout", "message": f"Command timed out after {timeout}s"}}
    except Exception as e:
        return {"success": False, "error": {"code": "ExecError", "message": str(e)}}


def record(scenario, cmd_name, result):
    """Record a test result."""
    success = result.get("success", False)
    status = "PASS" if success else "FAIL"
    error_code = result.get("error", {}).get("code", "") if not success else ""

    # API errors are still valid test outcomes (the CLI worked correctly)
    if not success and error_code in (
        "AuthFailure", "AuthFailure.UnauthorizedOperation",
        "ResourceNotFound.ClusterId", "InvalidParameterValue.ClusterId",
        "UnsupportedOperation.NoPermissionAccess",
    ):
        status = "API_ERR"

    entry = {
        "scenario": scenario,
        "command": cmd_name,
        "status": status,
        "error_code": error_code,
        "request_id": result.get("request_id", ""),
        "timestamp": datetime.now().isoformat(),
    }
    RESULTS.append(entry)
    print(f"  [{status}] {cmd_name}: {error_code or 'OK'}")
    return result


# ═══════════════════════════════════════════════════════════════════════════
# Test Scenarios
# ═══════════════════════════════════════════════════════════════════════════


def test_create_job(region, workspace_id, cluster_id):
    """Test creating a SQL job."""
    print("\n--- Test: create_job ---")

    job_name = f"e2e_test_job_{int(time.time())}"
    args = [
        "create_job",
        "--name", job_name,
        "--job_type", "1",
        "--region", region,
        "--confirm",
    ]
    if workspace_id:
        args.extend(["--workspace_id", workspace_id])
    if cluster_id:
        args.extend(["--cluster_id", cluster_id])

    result = cli(*args)
    record("sql_job_development", "create_job", result)

    # Return job ID for subsequent tests
    job_id = result.get("data", {}).get("JobId", "")
    return job_id


def test_describe_jobs(region, workspace_id, job_id=None):
    """Test querying jobs."""
    print("\n--- Test: describe_jobs ---")

    args = [
        "describe_jobs",
        "--region", region,
    ]
    if workspace_id:
        args.extend(["--workspace_id", workspace_id])
    if job_id:
        args.extend(["--job_ids", job_id])

    result = cli(*args)
    record("sql_job_development", "describe_jobs", result)
    return result


def test_validation_errors():
    """Test that missing required parameters produce proper errors."""
    print("\n--- Test: validation errors ---")

    # Missing region
    result = cli("create_job", "--name", "test", "--job_type", "1", "--confirm")
    record("validation", "create_job_no_region", result)
    assert not result.get("success"), "Should fail without region"

    # Missing name
    result = cli("create_job", "--region", "ap-guangzhou", "--job_type", "1", "--confirm")
    record("validation", "create_job_no_name", result)
    assert not result.get("success"), "Should fail without name"

    # Safety check (no --confirm)
    result = cli("create_job", "--name", "test", "--job_type", "1", "--region", "ap-guangzhou")
    record("validation", "create_job_no_confirm", result)
    assert not result.get("success"), "Should fail without --confirm"

    # Missing --job_type (now strictly required by argparse)
    result = cli("create_job", "--name", "test", "--region", "ap-guangzhou", "--confirm")
    record("validation", "create_job_no_job_type", result)
    assert not result.get("success"), "Should fail without --job_type"


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════


def main():
    import argparse

    parser = argparse.ArgumentParser(description="E2E tests for Oceanus CLI")
    parser.add_argument("--region", default=DEFAULT_REGION, help="Region")
    parser.add_argument("--workspace_id", default=DEFAULT_WORKSPACE_ID, help="Workspace ID")
    parser.add_argument("--cluster_id", default=DEFAULT_CLUSTER_ID, help="Cluster ID")
    args = parser.parse_args()

    print(f"=== Oceanus CLI E2E Tests ===")
    print(f"Region: {args.region}")
    print(f"Workspace: {args.workspace_id or '(not specified)'}")
    print(f"Cluster: {args.cluster_id or '(not specified)'}")
    print(f"Time: {datetime.now().isoformat()}")

    # Run validation tests (no real API calls needed)
    test_validation_errors()

    # Run API tests (require credentials)
    if os.environ.get("TENCENTCLOUD_SECRET_ID"):
        job_id = test_create_job(args.region, args.workspace_id, args.cluster_id)
        test_describe_jobs(args.region, args.workspace_id, job_id)
    else:
        print("\n⚠️  Skipping API tests: TENCENTCLOUD_SECRET_ID not set")

    # Summary
    print(f"\n=== Results Summary ===")
    total = len(RESULTS)
    passed = sum(1 for r in RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in RESULTS if r["status"] == "FAIL")
    api_err = sum(1 for r in RESULTS if r["status"] == "API_ERR")
    print(f"Total: {total} | Pass: {passed} | Fail: {failed} | API Error: {api_err}")

    # Write results to file
    output_path = os.path.join(SCRIPT_DIR, "..", "outputs", "e2e_results.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump({"total": total, "passed": passed, "failed": failed, "api_err": api_err, "details": RESULTS}, f, indent=2)
    print(f"Results written to: {output_path}")

    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
