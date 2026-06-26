---
name: watadot-aws-s3
description: High-performance S3 management by Watadot Studio. Includes bucket orchestration, sync, and lifecycle management.
metadata:
  openclaw:
    emoji: 🪣
    requires:
      anyBins: [aws]
---

# AWS S3 Skills

Advanced patterns for Amazon Simple Storage Service (S3) utilization.

## 🚀 Core Commands

### Bucket Management
```bash
# List all buckets with creation date
aws s3api list-buckets --query "Buckets[].{Name:Name,Created:CreationDate}" --output table

# Create a bucket with specific region
aws s3 mb s3://<bucket-name> --region <region>
```

### High-Speed Synchronization
```bash
# Intelligent sync (only changed files)
aws s3 sync ./local-dir s3://<bucket-name>/path --delete --exclude "*.tmp"

# Concurrent upload tuning (performance)
aws configure set default.s3.max_concurrent_requests 20
```

### Content Discovery & Filtering
```bash
# Find objects larger than 100MB
aws s3api list-objects-v2 --bucket <bucket-name> --query "Contents[?Size > \`104857600\`].[Key, Size]" --output json

# Total size of a prefix
aws s3 ls s3://<bucket-name>/prefix --recursive --human-readable --summarize | tail -n 2
```

## 🧠 Best Practices
1. **Least Privilege**: Always use IAM policies that restrict access to specific buckets/prefixes.
2. **Versioning**: Enable versioning for critical production data to prevent accidental deletions.
3. **Encrypted at Rest**: Enforce SSE-S3 or SSE-KMS for all sensitive objects.
4. **Lifecycle Policies**: Automate transition to S3 Glacier for aging assets to optimize cost.
