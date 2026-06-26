#!/usr/bin/env python3
"""Smoke test for the sagemaker-training-job skill.

Submits a minimal training job to SageMaker, waits for completion,
downloads artifacts, and verifies the output.

Usage:
    sagemaker_smoke_test.py --role <arn> --bucket <bucket> [--region us-east-1]

Cost: ~$0.01 (ml.m5.large for ~2 min).
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description="Smoke test for sagemaker-training-job skill")
    p.add_argument("--role", required=True, help="SageMaker execution role ARN")
    p.add_argument("--bucket", required=True, help="S3 bucket for artifacts")
    p.add_argument("--region", default="us-east-1")
    p.add_argument("--keep", action="store_true", help="Keep output files after test")
    args = p.parse_args()

    skill_dir = Path(__file__).resolve().parent
    train_script = skill_dir / "test_train.py"
    train_launcher = skill_dir / "sagemaker_train.py"
    cost_script = skill_dir / "sagemaker_cost.py"
    output_dir = Path("/tmp/sagemaker-smoke-test-output")
    job_name = f"smoke-test-{int(__import__('time').time())}"

    python = sys.executable
    errors = []

    # --- Pre-flight ---
    print("=" * 60)
    print("SageMaker Training Job Skill — Smoke Test")
    print("=" * 60)

    print(f"\n  Job name:    {job_name}")
    print(f"  Role:        {args.role}")
    print(f"  Bucket:      {args.bucket}")
    print(f"  Region:      {args.region}")
    print(f"  Instance:    ml.m5.large (cheapest)")
    print(f"  Output:      {output_dir}")

    # --- Step 1: Local test ---
    print(f"\n--- Step 1: Local script test ---")
    local_model_dir = Path("/tmp/sagemaker-smoke-test-local")
    local_model_dir.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        [python, str(train_script), "--epochs", "1", "--model-dir", str(local_model_dir)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ❌ Local test failed:\n{result.stderr}")
        errors.append("local_test")
    else:
        model_file = local_model_dir / "model.json"
        if model_file.exists():
            data = json.loads(model_file.read_text())
            print(f"  ✅ Local test passed — model: {data}")
        else:
            print(f"  ❌ Local test: model.json not created")
            errors.append("local_model")

    # Clean up local test
    import shutil
    shutil.rmtree(local_model_dir, ignore_errors=True)

    if errors:
        print(f"\n❌ Pre-flight failed. Fix local issues before testing SageMaker.")
        sys.exit(1)

    # --- Step 2: SageMaker job ---
    print(f"\n--- Step 2: SageMaker training job ---")
    cmd = [
        python, str(train_launcher),
        "--job-name", job_name,
        "--script", str(train_script),
        "--source-dir", str(skill_dir),
        "--role", args.role,
        "--bucket", args.bucket,
        "--region", args.region,
        "--instance-type", "ml.m5.large",
        "--framework", "sklearn",
        "--max-runtime", "300",
        "--hyperparameters", '{"epochs":"2"}',
        "--output-dir", str(output_dir),
        "--poll-interval", "15",
    ]

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"  ❌ SageMaker job failed (exit code {result.returncode})")
        errors.append("sagemaker_job")
    else:
        # Verify output
        model_file = output_dir / "model" / "model.json"
        if model_file.exists():
            data = json.loads(model_file.read_text())
            if data.get("type") == "smoke-test" and data.get("epochs") == 2:
                print(f"  ✅ Model artifact verified: {data}")
            else:
                print(f"  ❌ Model content unexpected: {data}")
                errors.append("model_content")
        else:
            print(f"  ❌ model.json not found in output")
            errors.append("model_download")

    # --- Step 3: Cost check ---
    print(f"\n--- Step 3: Cost check ---")
    result = subprocess.run(
        [python, str(cost_script), "--job-name", job_name, "--region", args.region],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(result.stdout.strip())
        print(f"  ✅ Cost check passed")
    else:
        print(f"  ❌ Cost check failed:\n{result.stderr}")
        errors.append("cost_check")

    # --- Summary ---
    print(f"\n{'=' * 60}")
    if errors:
        print(f"❌ Smoke test FAILED — issues: {', '.join(errors)}")
        sys.exit(1)
    else:
        print(f"✅ Smoke test PASSED — all checks green")
        print(f"   Job: {job_name}")

    # Cleanup
    if not args.keep:
        shutil.rmtree(output_dir, ignore_errors=True)
        print(f"   Output cleaned up. Use --keep to preserve.")
    else:
        print(f"   Output preserved at {output_dir}")


if __name__ == "__main__":
    main()
