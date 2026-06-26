---
name: sagemaker-training-job
description: Submit ML training jobs to AWS SageMaker — package code, upload to S3, launch on GPU/CPU instances, poll status, download artifacts. Use when training machine learning models that need more compute than the local machine (GPU training, large datasets, parallel experiments). Supports PyTorch, TensorFlow, scikit-learn, XGBoost/LightGBM. Handles spot instances for cost savings. Triggers on "train on SageMaker", "GPU training", "submit training job", "cloud training", "SageMaker", "remote training".
metadata: {"openclaw": {"requires": {"bins": ["python3"]}, "primaryEnv": "AWS_DEFAULT_REGION", "homepage": "https://github.com/zyyhhxx/OpenClawSkill-sagemaker-training-job"}}
---

# SageMaker Training

Submit ML training jobs to AWS SageMaker from the command line. Supports PyTorch,
TensorFlow, scikit-learn, and XGBoost with managed spot training for cost savings.

## Prerequisites

- `boto3` Python package installed (`pip install boto3`). `sagemaker` recommended.
- **AWS credentials** available — EC2 instance profile (recommended), or `aws configure` / env vars (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
- S3 bucket for training artifacts
- Two IAM roles configured — see `references/setup.md` for exact policies:
  - **Role A (Caller):** SageMaker job management + S3 access + ECR image pull
  - **Role B (Execution):** S3 data access + CloudWatch logs + ECR images

## Security Notes

- **AWS credentials** are never logged, embedded in scripts, or uploaded to S3.
  boto3 resolves credentials from the standard chain (instance profile → env → config file).
- **Source packaging** excludes `.git`, `.env`, `venv`, `__pycache__`, and other
  non-essential files. Use `--source-dir` to explicitly scope what gets packaged.
  Always review `--dry-run` output before submitting to production.
- **IAM scope:** Both caller and execution role policies should be scoped to your
  specific S3 bucket and SageMaker execution role ARN. See `references/setup.md`.

## Quick Start

### 1. Write a training script

Follow the SageMaker training script contract: read data from `SM_CHANNEL_TRAIN`,
save model to `SM_MODEL_DIR`. See `references/training-scripts.md` for templates.

### 2. Submit a training job

```bash
python3 scripts/sagemaker_train.py \
  --job-name my-experiment-001 \
  --script ./train.py \
  --role arn:aws:iam::ACCOUNT:role/SageMakerRole \
  --bucket my-sagemaker-bucket \
  --instance-type ml.g5.xlarge \
  --spot \
  --framework pytorch \
  --input-data s3://my-bucket/data/train/ \
  --hyperparameters '{"epochs":"50","lr":"0.001"}' \
  --output-dir ./results
```

The script packages your code, uploads to S3, submits the job, polls until
complete, and downloads model artifacts to `--output-dir`.

### 3. Check cost

```bash
# Estimate before running
python3 scripts/sagemaker_cost.py --instance-type ml.g5.xlarge --duration 3600 --spot

# Check actual cost after job completes
python3 scripts/sagemaker_cost.py --job-name my-experiment-001
```

### 4. List recent jobs

```bash
python3 scripts/sagemaker_list.py --max 5
python3 scripts/sagemaker_list.py --status Failed
```

## Key Options

| Flag | Purpose | Default |
|------|---------|---------|
| `--spot` | Managed spot training (up to 70% savings) | off |
| `--instance-type` | Compute instance | ml.g5.xlarge |
| `--max-runtime` | Kill job after N seconds | 3600 |
| `--framework` | pytorch, tensorflow, sklearn, xgboost | pytorch |
| `--image-uri` | Custom Docker image (overrides framework) | auto |
| `--requirements` | requirements.txt for extra deps | none |
| `--dry-run` | Print config without submitting | off |
| `--no-wait` | Submit and exit without polling | off |
| `--resume JOB` | Reconnect to a running/completed job (skip submission) | — |
| `--source-dir` | Directory with all training code | script's parent |
| `--input-data` | S3 input(s), format: `channel:s3://...` | none |
| `--env` | JSON environment variables | {} |

## Instance Selection

For tabular/Kaggle workloads:
- **Gradient boosting** (LightGBM/XGBoost): `ml.m5.2xlarge` (CPU, $0.54/hr)
- **Small neural nets**: `ml.g4dn.xlarge` (T4, $0.74/hr) — cheapest GPU
- **Standard deep learning**: `ml.g5.xlarge` (A10G, $1.41/hr) — best price/performance
- **Heavy training**: `ml.p3.2xlarge` (V100, $4.28/hr)

Always use `--spot` for non-urgent training — typical savings of 30-70%.

## Workflow Integration

For autonomous agents running training jobs in a loop:

1. Prepare data locally or upload to S3
2. Write training script following the contract in `references/training-scripts.md`
3. Use `--dry-run` first to validate config
4. Submit with `sagemaker_train.py` — it blocks until completion by default
5. Results download automatically to `--output-dir`
6. Parse metrics from the output for experiment tracking

For parallel experiments, use `--no-wait` and poll with `sagemaker_list.py`.

## Smoke Test

Verify the entire pipeline works end-to-end (~$0.01, takes ~3 min):

```bash
python3 scripts/sagemaker_smoke_test.py \
  --role arn:aws:iam::ACCOUNT:role/SageMakerTrainingExecutionRole \
  --bucket my-sagemaker-bucket
```

This runs a local pre-flight, submits a minimal job to SageMaker, verifies
the downloaded model artifact, and checks cost. Use `--keep` to preserve output files.
