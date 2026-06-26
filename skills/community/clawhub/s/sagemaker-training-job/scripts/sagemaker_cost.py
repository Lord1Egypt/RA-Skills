#!/usr/bin/env python3
"""Estimate cost for a SageMaker training job based on instance type and duration.

Usage:
    sagemaker_cost.py --instance-type ml.g5.xlarge --duration 3600 [--spot] [--region us-east-1]
    sagemaker_cost.py --job-name my-training-job [--region us-east-1]
"""

import argparse
import os
import sys

try:
    import boto3
except ImportError:
    print("ERROR: boto3 not installed. Run: pip install boto3", file=sys.stderr)
    sys.exit(1)

# On-demand prices per hour (us-east-1, approximate as of 2025)
# Source: https://aws.amazon.com/sagemaker/pricing/
PRICES_PER_HOUR = {
    # GPU instances
    "ml.g4dn.xlarge": 0.736,
    "ml.g4dn.2xlarge": 1.12,
    "ml.g4dn.4xlarge": 1.94,
    "ml.g4dn.8xlarge": 3.49,
    "ml.g4dn.12xlarge": 5.87,
    "ml.g5.xlarge": 1.408,
    "ml.g5.2xlarge": 1.888,
    "ml.g5.4xlarge": 2.848,
    "ml.g5.8xlarge": 4.768,
    "ml.g5.12xlarge": 7.248,
    "ml.g5.24xlarge": 12.288,
    "ml.g6.xlarge": 0.98,
    "ml.g6.2xlarge": 1.52,
    "ml.g6.4xlarge": 2.61,
    "ml.p3.2xlarge": 4.284,
    "ml.p3.8xlarge": 14.688,
    "ml.p4d.24xlarge": 40.836,
    # CPU instances
    "ml.m5.large": 0.134,
    "ml.m5.xlarge": 0.269,
    "ml.m5.2xlarge": 0.538,
    "ml.m5.4xlarge": 1.075,
    "ml.m6i.xlarge": 0.282,
    "ml.m6i.2xlarge": 0.564,
    "ml.c5.xlarge": 0.253,
    "ml.c5.2xlarge": 0.506,
    "ml.c5.4xlarge": 1.013,
}

SPOT_DISCOUNT = 0.70  # Spot is typically ~30-70% cheaper; use conservative 30% savings


def main():
    p = argparse.ArgumentParser(description="SageMaker training cost estimator")
    p.add_argument("--job-name", help="Get cost for a completed training job")
    p.add_argument("--instance-type", help="Instance type for estimation")
    p.add_argument("--instance-count", type=int, default=1)
    p.add_argument("--duration", type=int, help="Duration in seconds")
    p.add_argument("--spot", action="store_true", help="Apply spot discount")
    p.add_argument("--region", default=None)
    args = p.parse_args()

    region = args.region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if args.job_name:
        sm = boto3.client("sagemaker", region_name=region)
        detail = sm.describe_training_job(TrainingJobName=args.job_name)
        instance_type = detail["ResourceConfig"]["InstanceType"]
        instance_count = detail["ResourceConfig"]["InstanceCount"]
        duration = detail.get("BillableTimeInSeconds", detail.get("TrainingTimeInSeconds", 0))
        spot = detail.get("EnableManagedSpotTraining", False)
        status = detail["TrainingJobStatus"]
        print(f"Job: {args.job_name}")
        print(f"Status: {status}")
        print(f"Instance: {instance_type} x {instance_count}")
        print(f"Billable time: {duration}s ({duration/3600:.2f}h)")
        print(f"Spot: {'Yes' if spot else 'No'}")
    else:
        if not args.instance_type or not args.duration:
            print("Provide either --job-name or both --instance-type and --duration", file=sys.stderr)
            sys.exit(1)
        instance_type = args.instance_type
        instance_count = args.instance_count
        duration = args.duration
        spot = args.spot

    price = PRICES_PER_HOUR.get(instance_type)
    if price is None:
        print(f"⚠️  No pricing data for {instance_type}. Check AWS pricing page.")
        return

    hours = duration / 3600
    cost = price * hours * instance_count
    if spot:
        cost *= (1 - SPOT_DISCOUNT)

    print(f"\n💰 Estimated cost: ${cost:.2f}")
    print(f"   Rate: ${price:.3f}/hr {'(spot ~{:.0f}% off)'.format(SPOT_DISCOUNT*100) if spot else '(on-demand)'}")
    print(f"   Duration: {hours:.2f}h x {instance_count} instance(s)")


if __name__ == "__main__":
    main()
