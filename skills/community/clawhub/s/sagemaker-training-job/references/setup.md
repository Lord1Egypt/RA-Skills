# SageMaker Training — Setup Guide

## Overview

Two IAM roles are involved in SageMaker training:

| Role | Who/What | Purpose |
|------|----------|---------|
| **Role A: Caller** | Your EC2 instance or PC | Submits jobs, uploads code to S3, polls status, downloads results |
| **Role B: Execution** | The SageMaker training container | Reads training data from S3, writes model artifacts, logs to CloudWatch |

Both roles and an S3 bucket must exist before submitting training jobs.
Create them through the AWS Console, CLI, or IaC (Terraform/CloudFormation).

---

## Role A: Caller

Attach this policy to your EC2 instance profile or IAM user.

### IAM Policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "SageMakerJobManagement",
            "Effect": "Allow",
            "Action": [
                "sagemaker:CreateTrainingJob",
                "sagemaker:DescribeTrainingJob",
                "sagemaker:ListTrainingJobs",
                "sagemaker:StopTrainingJob"
            ],
            "Resource": "*"
        },
        {
            "Sid": "PassExecutionRole",
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "arn:aws:iam::ACCOUNT_ID:role/SageMakerTrainingExecutionRole",
            "Condition": {
                "StringEquals": {
                    "iam:PassedToService": "sagemaker.amazonaws.com"
                }
            }
        },
        {
            "Sid": "S3ArtifactAccess",
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR-BUCKET-NAME",
                "arn:aws:s3:::YOUR-BUCKET-NAME/*"
            ]
        },
        {
            "Sid": "ECRImageResolution",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchGetImage",
                "ecr:GetDownloadUrlForLayer"
            ],
            "Resource": "*"
        },
        {
            "Sid": "STSIdentity",
            "Effect": "Allow",
            "Action": "sts:GetCallerIdentity",
            "Resource": "*"
        }
    ]
}
```

Replace `ACCOUNT_ID` and `YOUR-BUCKET-NAME` with your values.

### Permission reference

| Permission | Why |
|-----------|-----|
| `sagemaker:CreateTrainingJob` | Submit training jobs |
| `sagemaker:DescribeTrainingJob` | Poll job status |
| `sagemaker:ListTrainingJobs` | List recent jobs |
| `sagemaker:StopTrainingJob` | Cancel a running job |
| `iam:PassRole` | Hand the execution role to SageMaker (scoped to the specific role) |
| `s3:PutObject` | Upload source code to S3 |
| `s3:GetObject` | Download model artifacts from S3 |
| `s3:DeleteObject` | Clean up old artifacts |
| `s3:ListBucket` | List files in bucket, check bucket existence |
| `ecr:GetAuthorizationToken` | Authenticate to ECR for container images |
| `ecr:BatchGetImage` | Pull pre-built framework container images |
| `ecr:GetDownloadUrlForLayer` | Download container image layers |
| `sts:GetCallerIdentity` | Verify identity and get account ID |

### Attaching to EC2 (instance profile)

On EC2, use an instance profile — boto3 picks it up automatically with no
credentials file needed.

```bash
# 1. Create the role with EC2 trust
aws iam create-role \
  --role-name EC2-SageMaker-Caller \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ec2.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

# 2. Attach the caller policy (save the JSON above as caller-policy.json)
aws iam put-role-policy \
  --role-name EC2-SageMaker-Caller \
  --policy-name SageMakerCallerPolicy \
  --policy-document file://caller-policy.json

# 3. Create and attach instance profile
aws iam create-instance-profile --instance-profile-name EC2-SageMaker-Caller
aws iam add-role-to-instance-profile \
  --instance-profile-name EC2-SageMaker-Caller \
  --role-name EC2-SageMaker-Caller

# 4. Attach to your EC2 instance
aws ec2 associate-iam-instance-profile \
  --instance-id i-XXXXXXXXX \
  --iam-instance-profile Name=EC2-SageMaker-Caller
```

### Using on a personal PC

```bash
aws configure
# Enter: Access Key ID, Secret Access Key, Region, Output format
```

Or environment variables:
```bash
export AWS_ACCESS_KEY_ID=AKIA...
export AWS_SECRET_ACCESS_KEY=...
export AWS_DEFAULT_REGION=us-east-1
```

---

## Role B: SageMaker Execution Role

This is the role SageMaker assumes to run your training container.

**Role name:** `SageMakerTrainingExecutionRole` (or any name you choose —
pass it to `--role` when submitting jobs).

### Trust policy

Allows SageMaker to assume this role:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"Service": "sagemaker.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }
    ]
}
```

### Permissions policy

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "S3DataAccess",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::YOUR-BUCKET-NAME",
                "arn:aws:s3:::YOUR-BUCKET-NAME/*"
            ]
        },
        {
            "Sid": "CloudWatchLogs",
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "logs:DescribeLogStreams"
            ],
            "Resource": "arn:aws:logs:*:ACCOUNT_ID:log-group:/aws/sagemaker/*"
        },
        {
            "Sid": "ECRImageAccess",
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        },
        {
            "Sid": "CloudWatchMetrics",
            "Effect": "Allow",
            "Action": ["cloudwatch:PutMetricData"],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "cloudwatch:namespace": "/aws/sagemaker/TrainingJobs"
                }
            }
        }
    ]
}
```

Replace `YOUR-BUCKET-NAME` and `ACCOUNT_ID` with your values.

### Permission reference

| Permission | Why |
|-----------|-----|
| `s3:GetObject` | Read training data and source code from S3 |
| `s3:PutObject` | Write model artifacts (model.tar.gz) to S3 |
| `s3:DeleteObject` | Clean up intermediate artifacts |
| `s3:ListBucket` | List input data files |
| `logs:CreateLogGroup` | Create CloudWatch log group for training |
| `logs:CreateLogStream` | Create log stream per training job |
| `logs:PutLogEvents` | Write training logs (stdout/stderr) |
| `logs:DescribeLogStreams` | Read log stream metadata |
| `ecr:GetAuthorizationToken` | Authenticate to ECR |
| `ecr:BatchCheckLayerAvailability` | Check container image layers |
| `ecr:GetDownloadUrlForLayer` | Download container image layers |
| `ecr:BatchGetImage` | Pull container image manifest |
| `cloudwatch:PutMetricData` | Report training metrics (loss, accuracy) |

### Creating the execution role

```bash
# 1. Create the role
aws iam create-role \
  --role-name SageMakerTrainingExecutionRole \
  --assume-role-policy-document file://trust-policy.json \
  --description "SageMaker training job execution role"

# 2. Attach the permissions policy
aws iam put-role-policy \
  --role-name SageMakerTrainingExecutionRole \
  --policy-name SageMakerTrainingPolicy \
  --policy-document file://execution-policy.json

# 3. Note the ARN for --role flag
aws iam get-role --role-name SageMakerTrainingExecutionRole \
  --query 'Role.Arn' --output text
```

---

## S3 Bucket

Create a dedicated bucket for training artifacts:

```bash
# Create bucket
aws s3 mb s3://my-sagemaker-bucket --region us-east-1

# Block public access (recommended)
aws s3api put-public-access-block \
  --bucket my-sagemaker-bucket \
  --public-access-block-configuration \
    BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```

---

## Python Dependencies

```bash
pip install boto3 sagemaker
```

- `boto3` — required (AWS SDK)
- `sagemaker` — optional but recommended (auto-resolves container image URIs).
  Without it, pass `--image-uri` directly to `sagemaker_train.py`.

---

## Verification

After setup, run the smoke test to verify everything works end-to-end:

```bash
python3 scripts/sagemaker_smoke_test.py \
  --role arn:aws:iam::ACCOUNT_ID:role/SageMakerTrainingExecutionRole \
  --bucket my-sagemaker-bucket
```

Cost: ~$0.01. Takes ~3 minutes.

---

## Spot Training

Use `--spot` for Managed Spot Training — up to 70% cost savings on GPU.
SageMaker handles spot interruptions automatically.

Set `--spot-max-wait` for the maximum time to wait for spot capacity
(default: 7200s = 2h). Job fails if capacity isn't available within this window.

---

## Instance Selection Guide

| Use Case | Instance | GPU | Cost/hr | Notes |
|----------|----------|-----|---------|-------|
| Quick experiments | ml.g4dn.xlarge | T4 16GB | ~$0.74 | Cheapest GPU |
| Standard training | ml.g5.xlarge | A10G 24GB | ~$1.41 | Best price/perf |
| Large models | ml.g5.2xlarge | A10G 24GB | ~$1.89 | More CPU/RAM |
| Heavy training | ml.p3.2xlarge | V100 16GB | ~$4.28 | Tensor cores |
| CPU-only (GBM) | ml.m5.2xlarge | None | ~$0.54 | For tree models |
| CPU-heavy feature eng | ml.c5.4xlarge | None | ~$1.01 | Compute optimized |

For Kaggle-style tabular data, `ml.m5.2xlarge` (CPU) is usually sufficient for
gradient boosting. Use `ml.g5.xlarge` when neural nets are needed.

Prices are approximate us-east-1 on-demand rates. Spot is typically 30-70% less.
