#!/usr/bin/env python3
"""List recent SageMaker training jobs with status and cost info.

Usage:
    sagemaker_list.py [--status Completed|InProgress|Failed|Stopped] [--max 10] [--region us-east-1]
"""

import argparse
import os
import sys
from datetime import datetime, timezone

try:
    import boto3
except ImportError:
    print("ERROR: boto3 not installed. Run: pip install boto3", file=sys.stderr)
    sys.exit(1)


def main():
    p = argparse.ArgumentParser(description="List SageMaker training jobs")
    p.add_argument("--status", help="Filter by status")
    p.add_argument("--max", type=int, default=10, help="Max results")
    p.add_argument("--region", default=None)
    args = p.parse_args()

    region = args.region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    sm = boto3.client("sagemaker", region_name=region)

    params = {"MaxResults": args.max, "SortBy": "CreationTime", "SortOrder": "Descending"}
    if args.status:
        params["StatusEquals"] = args.status

    resp = sm.list_training_jobs(**params)
    jobs = resp.get("TrainingJobSummaries", [])

    if not jobs:
        print("No training jobs found.")
        return

    print(f"{'Job Name':<45} {'Status':<12} {'Instance':<18} {'Duration':<10} {'Created'}")
    print("-" * 110)

    for job in jobs:
        name = job["TrainingJobName"]
        status = job["TrainingJobStatus"]
        created = job["CreationTime"].strftime("%Y-%m-%d %H:%M")

        # Get details for instance type and duration
        detail = sm.describe_training_job(TrainingJobName=name)
        instance = detail["ResourceConfig"]["InstanceType"]
        duration = detail.get("TrainingTimeInSeconds", 0)
        dur_str = f"{duration // 60}m{duration % 60}s" if duration else "-"

        print(f"{name:<45} {status:<12} {instance:<18} {dur_str:<10} {created}")


if __name__ == "__main__":
    main()
