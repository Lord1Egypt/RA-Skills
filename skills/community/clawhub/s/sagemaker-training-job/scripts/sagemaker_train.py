#!/usr/bin/env python3
"""Submit a training job to AWS SageMaker, poll until complete, download artifacts.

Usage:
    sagemaker_train.py --job-name <name> \
        --script <path> \
        --role <iam-role-arn> \
        --bucket <s3-bucket> \
        [--instance-type ml.g5.xlarge] \
        [--instance-count 1] \
        [--max-runtime 3600] \
        [--spot] \
        [--spot-max-wait 7200] \
        [--framework pytorch|tensorflow|sklearn|xgboost] \
        [--framework-version 2.5.1] \
        [--py-version py311] \
        [--requirements requirements.txt] \
        [--input-data s3://bucket/prefix/] \
        [--input-channel train] \
        [--hyperparameters '{"lr":"0.001","epochs":"10"}'] \
        [--output-dir ./output] \
        [--poll-interval 30] \
        [--tags '{"project":"kaggle","competition":"optiver"}'] \
        [--env '{"KEY":"VALUE"}']

    # Resume polling a previously submitted job:
    sagemaker_train.py --resume <job-name> \
        --bucket <s3-bucket> \
        [--output-dir ./output] \
        [--poll-interval 30]

Environment:
    AWS_PROFILE / AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY
    AWS_DEFAULT_REGION (default: us-east-1)
"""

import argparse
import json
import os
import sys
import tarfile
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import boto3
    from botocore.exceptions import ClientError
except ImportError:
    print("ERROR: boto3 not installed. Run: pip install boto3", file=sys.stderr)
    sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser(description="SageMaker Training Job Launcher")
    p.add_argument("--job-name", help="Training job name (must be unique)")
    p.add_argument("--script", help="Path to training script (entry point)")
    p.add_argument("--source-dir", help="Directory containing training code (defaults to script's parent)")
    p.add_argument("--role", help="IAM role ARN for SageMaker execution")
    p.add_argument("--bucket", help="S3 bucket for code/data/output")
    p.add_argument("--prefix", default="sagemaker", help="S3 key prefix (default: sagemaker)")

    # Instance config
    p.add_argument("--instance-type", default="ml.g5.xlarge", help="Training instance type")
    p.add_argument("--instance-count", type=int, default=1, help="Number of training instances")
    p.add_argument("--max-runtime", type=int, default=3600, help="Max training time in seconds")
    p.add_argument("--volume-size", type=int, default=30, help="EBS volume size in GB")

    # Spot training
    p.add_argument("--spot", action="store_true", help="Use managed spot training (up to 90% savings)")
    p.add_argument("--spot-max-wait", type=int, default=7200, help="Max wait time for spot in seconds")

    # Framework
    p.add_argument("--framework", default="pytorch", choices=["pytorch", "tensorflow", "sklearn", "xgboost"])
    p.add_argument("--framework-version", help="Framework version (auto-detected if omitted)")
    p.add_argument("--py-version", help="Python version (e.g., py311, py310)")

    # Custom image (overrides framework)
    p.add_argument("--image-uri", help="Custom Docker image URI (overrides --framework)")

    # Data
    p.add_argument("--input-data", action="append", help="Input data S3 URI(s). Format: s3://path or channel:s3://path")
    p.add_argument("--requirements", help="Path to requirements.txt for additional dependencies")

    # Hyperparameters
    p.add_argument("--hyperparameters", default="{}", help="JSON string of hyperparameters")

    # Environment variables
    p.add_argument("--env", default="{}", help="JSON string of environment variables")

    # Output
    p.add_argument("--output-dir", default="./output", help="Local directory for downloaded artifacts")
    p.add_argument("--poll-interval", type=int, default=30, help="Seconds between status polls")

    # Tags
    p.add_argument("--tags", default="{}", help="JSON string of tags")

    # Flags
    p.add_argument("--no-wait", action="store_true", help="Submit and exit without waiting")
    p.add_argument("--no-download", action="store_true", help="Don't download output artifacts")
    p.add_argument("--dry-run", action="store_true", help="Print config without submitting")
    p.add_argument("--region", default=None, help="AWS region (default: from env or us-east-1)")

    # Resume mode
    p.add_argument("--resume", metavar="JOB_NAME", help="Resume polling an existing job (skip submission)")

    args = p.parse_args()

    # Validate required args based on mode
    if args.resume:
        # Resume mode: only need bucket (optional) and output-dir
        pass
    else:
        # Submit mode: need job-name, script, role, bucket
        missing = []
        if not args.job_name: missing.append("--job-name")
        if not args.script: missing.append("--script")
        if not args.role: missing.append("--role")
        if not args.bucket: missing.append("--bucket")
        if missing:
            p.error(f"the following arguments are required: {', '.join(missing)}")

    return args


# --- Default framework versions ---
FRAMEWORK_DEFAULTS = {
    "pytorch": {"version": "2.5.1", "py": "py311", "training_image_scope": "training"},
    "tensorflow": {"version": "2.16.1", "py": "py310", "training_image_scope": "training"},
    "sklearn": {"version": "1.2-1", "py": "py3", "training_image_scope": "training"},
    "xgboost": {"version": "1.7-1", "py": "py3", "training_image_scope": "training"},
}


def resolve_image_uri(framework, version, py_version, region, instance_type):
    """Resolve the SageMaker pre-built framework image URI."""
    try:
        # SageMaker SDK v3
        from sagemaker.core.image_uris import retrieve
    except ImportError:
        try:
            # SageMaker SDK v2
            from sagemaker.image_uris import retrieve
        except ImportError:
            raise ImportError("sagemaker SDK not found. Install: pip install sagemaker")
    return retrieve(
        framework=framework,
        region=region,
        version=version,
        py_version=py_version,
        instance_type=instance_type,
        image_scope="training",
    )


# Patterns to exclude from source packaging
SOURCE_EXCLUDE_PATTERNS = {
    "__pycache__", ".pyc", ".pyo", ".git", ".gitignore",
    ".env", ".venv", "venv", "node_modules", ".DS_Store",
    ".ipynb_checkpoints", "__MACOSX", ".eggs", "*.egg-info",
}


def _should_exclude(path_str):
    """Check if a file path matches any exclusion pattern."""
    parts = Path(path_str).parts
    for part in parts:
        for pattern in SOURCE_EXCLUDE_PATTERNS:
            if pattern in part:
                return True
    return False


def package_source(script_path, source_dir, requirements_path):
    """Package training source code into a tar.gz for S3 upload.

    Only includes Python files, requirements.txt, and common data formats.
    Excludes .git, .env, venv, __pycache__, and other non-essential files.
    """
    script_path = Path(script_path).resolve()
    if source_dir:
        source_dir = Path(source_dir).resolve()
    else:
        source_dir = script_path.parent

    tmp = tempfile.NamedTemporaryFile(suffix=".tar.gz", delete=False)
    included = []
    excluded = []
    with tarfile.open(tmp.name, "w:gz") as tar:
        for f in source_dir.rglob("*"):
            if not f.is_file():
                continue
            rel = f.relative_to(source_dir)
            if _should_exclude(str(rel)):
                excluded.append(str(rel))
                continue
            tar.add(f, arcname=rel)
            included.append(str(rel))
        if requirements_path:
            req = Path(requirements_path).resolve()
            if req.exists():
                tar.add(req, arcname="requirements.txt")
                included.append("requirements.txt")

    if excluded:
        print(f"  Source package: {len(included)} files included, {len(excluded)} excluded")
    else:
        print(f"  Source package: {len(included)} files")

    return tmp.name, script_path.name


def upload_to_s3(s3, local_path, bucket, key):
    """Upload a file to S3."""
    print(f"  Uploading to s3://{bucket}/{key} ...")
    s3.upload_file(local_path, bucket, key)
    return f"s3://{bucket}/{key}"


def build_training_params(args, image_uri, source_s3_uri, entry_point):
    """Build the CreateTrainingJob API parameters."""
    hyperparameters = json.loads(args.hyperparameters)
    # SageMaker requires string values for hyperparameters
    hyperparameters = {k: str(v) for k, v in hyperparameters.items()}
    hyperparameters["sagemaker_program"] = entry_point
    hyperparameters["sagemaker_submit_directory"] = source_s3_uri

    tags_dict = json.loads(args.tags)
    tags = [{"Key": k, "Value": v} for k, v in tags_dict.items()]

    env_vars = json.loads(args.env)

    output_path = f"s3://{args.bucket}/{args.prefix}/output"

    params = {
        "TrainingJobName": args.job_name,
        "AlgorithmSpecification": {
            "TrainingImage": image_uri,
            "TrainingInputMode": "File",
        },
        "RoleArn": args.role,
        "OutputDataConfig": {"S3OutputPath": output_path},
        "ResourceConfig": {
            "InstanceType": args.instance_type,
            "InstanceCount": args.instance_count,
            "VolumeSizeInGB": args.volume_size,
        },
        "StoppingCondition": {"MaxRuntimeInSeconds": args.max_runtime},
        "HyperParameters": hyperparameters,
    }

    if env_vars:
        params["Environment"] = env_vars

    if tags:
        params["Tags"] = tags

    # Spot training
    if args.spot:
        params["EnableManagedSpotTraining"] = True
        params["StoppingCondition"]["MaxWaitTimeInSeconds"] = args.spot_max_wait

    # Input data channels
    if args.input_data:
        channels = []
        for item in args.input_data:
            if ":" in item and item.split(":")[0].isalpha() and not item.startswith("s3:"):
                channel_name, s3_uri = item.split(":", 1)
            else:
                channel_name = "train"
                s3_uri = item
            channels.append({
                "ChannelName": channel_name,
                "DataSource": {
                    "S3DataSource": {
                        "S3DataType": "S3Prefix",
                        "S3Uri": s3_uri,
                        "S3DataDistributionType": "FullyReplicated",
                    }
                },
            })
        params["InputDataConfig"] = channels

    return params


def wait_for_job(sm, job_name, poll_interval):
    """Poll training job until terminal state. Returns final status."""
    print(f"\nPolling job '{job_name}' every {poll_interval}s ...")
    terminal = {"Completed", "Failed", "Stopped"}

    while True:
        resp = sm.describe_training_job(TrainingJobName=job_name)
        status = resp["TrainingJobStatus"]
        secondary = resp.get("SecondaryStatus", "")
        elapsed = ""
        if "TrainingStartTime" in resp:
            delta = datetime.now(timezone.utc) - resp["TrainingStartTime"].astimezone(timezone.utc)
            elapsed = f" [{int(delta.total_seconds())}s elapsed]"

        print(f"  [{datetime.now(timezone.utc).strftime('%H:%M:%S')}] {status} / {secondary}{elapsed}")

        if status in terminal:
            return resp

        time.sleep(poll_interval)


def download_artifacts(s3, bucket, prefix, output_dir):
    """Download model artifacts from S3 to local directory."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    paginator = s3.get_paginator("list_objects_v2")
    count = 0
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            rel = key[len(prefix):].lstrip("/")
            if not rel:
                continue
            local = output_dir / rel
            local.parent.mkdir(parents=True, exist_ok=True)
            print(f"  Downloading {key} -> {local}")
            s3.download_file(bucket, key, str(local))
            count += 1

    # Auto-extract model.tar.gz if present
    model_tar = output_dir / "output" / "model.tar.gz"
    if model_tar.exists():
        extract_dir = output_dir / "model"
        extract_dir.mkdir(exist_ok=True)
        print(f"  Extracting model.tar.gz -> {extract_dir}")
        with tarfile.open(model_tar, "r:gz") as tar:
            tar.extractall(extract_dir)

    return count


def main():
    args = parse_args()
    region = args.region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    # Resume mode: skip submission, just poll and download
    if args.resume:
        session = boto3.Session(region_name=region)
        sm = session.client("sagemaker")
        s3 = session.client("s3")
        print(f"Resuming poll for job '{args.resume}' ...")
        result = wait_for_job(sm, args.resume, args.poll_interval)
        status = result["TrainingJobStatus"]
        if status == "Completed" and not args.no_download:
            bucket = args.bucket or result["OutputDataConfig"]["S3OutputPath"].replace("s3://", "").split("/")[0]
            prefix_parts = result["OutputDataConfig"]["S3OutputPath"].replace("s3://", "").split("/", 1)
            output_prefix = f"{prefix_parts[1]}/{args.resume}" if len(prefix_parts) > 1 else args.resume
            print(f"\nDownloading artifacts ...")
            count = download_artifacts(s3, bucket, output_prefix, args.output_dir)
            print(f"  Downloaded {count} file(s) to {args.output_dir}/")
        elif status == "Failed":
            print(f"\n❌ Job failed: {result.get('FailureReason', 'Unknown')}", file=sys.stderr)
            sys.exit(1)
        return

    # Resolve framework image
    if args.image_uri:
        image_uri = args.image_uri
    else:
        fw = FRAMEWORK_DEFAULTS[args.framework]
        version = args.framework_version or fw["version"]
        py_version = args.py_version or fw["py"]
        try:
            image_uri = resolve_image_uri(args.framework, version, py_version, region, args.instance_type)
        except Exception as e:
            print(f"ERROR resolving image URI: {e}", file=sys.stderr)
            print("Install sagemaker SDK: pip install sagemaker", file=sys.stderr)
            print("Or pass --image-uri directly.", file=sys.stderr)
            sys.exit(1)

    # Package source code
    print("Packaging source code ...")
    tar_path, entry_point = package_source(args.script, args.source_dir, args.requirements)
    source_key = f"{args.prefix}/source/{args.job_name}/sourcedir.tar.gz"

    # Build training params
    session = boto3.Session(region_name=region)
    s3 = session.client("s3")

    source_s3_uri = f"s3://{args.bucket}/{source_key}"
    params = build_training_params(args, image_uri, source_s3_uri, entry_point)

    if args.dry_run:
        print("\n=== DRY RUN — Training Job Config ===")
        print(json.dumps(params, indent=2, default=str))
        print(f"\nSource package: {tar_path}")
        print(f"Would upload to: {source_s3_uri}")
        os.unlink(tar_path)
        return

    # Upload source
    upload_to_s3(s3, tar_path, args.bucket, source_key)
    os.unlink(tar_path)

    # Submit training job
    sm = session.client("sagemaker")
    print(f"\nSubmitting training job '{args.job_name}' ...")
    try:
        sm.create_training_job(**params)
        print("  Job submitted successfully.")
    except ClientError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    if args.no_wait:
        print(f"\n--no-wait: Job submitted. Check status with:")
        print(f"  aws sagemaker describe-training-job --training-job-name {args.job_name}")
        return

    # Wait for completion
    result = wait_for_job(sm, args.job_name, args.poll_interval)
    status = result["TrainingJobStatus"]

    if status == "Completed":
        print(f"\n✅ Training completed successfully.")
        if result.get("BillableTimeInSeconds"):
            print(f"   Billable time: {result['BillableTimeInSeconds']}s")
        if result.get("TrainingTimeInSeconds"):
            print(f"   Total training time: {result['TrainingTimeInSeconds']}s")

        # Download artifacts
        if not args.no_download:
            model_s3 = result.get("ModelArtifacts", {}).get("S3ModelArtifacts", "")
            if model_s3:
                # Parse S3 URI
                parts = model_s3.replace("s3://", "").split("/", 1)
                dl_bucket, dl_prefix = parts[0], parts[1] if len(parts) > 1 else ""
                # Download the broader output prefix (includes model + any other outputs)
                output_prefix = f"{args.prefix}/output/{args.job_name}"
                print(f"\nDownloading artifacts from s3://{args.bucket}/{output_prefix} ...")
                count = download_artifacts(s3, args.bucket, output_prefix, args.output_dir)
                print(f"  Downloaded {count} file(s) to {args.output_dir}/")
        else:
            print("  Skipping artifact download (--no-download).")

        # Print metrics if available
        metrics = result.get("FinalMetricDataList", [])
        if metrics:
            print("\n📊 Final Metrics:")
            for m in metrics:
                print(f"   {m['MetricName']}: {m['Value']}")

    elif status == "Failed":
        reason = result.get("FailureReason", "Unknown")
        print(f"\n❌ Training FAILED: {reason}", file=sys.stderr)
        sys.exit(1)

    elif status == "Stopped":
        print(f"\n⚠️  Training was stopped.")
        sys.exit(1)


if __name__ == "__main__":
    main()
