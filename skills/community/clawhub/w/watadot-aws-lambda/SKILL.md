---
name: watadot-aws-lambda
description: Serverless compute orchestration by Watadot Studio. Manage functions, triggers, and cloud rendering.
metadata:
  openclaw:
    emoji: λ
    requires:
      anyBins: [aws]
---

# AWS Lambda Skills

Architectural patterns for serverless execution and orchestration.

## 🚀 Core Commands

### Function Lifecycle
```bash
# List all functions with runtime and memory info
aws lambda list-functions --query "Functions[].{Name:FunctionName,Runtime:Runtime,Memory:MemorySize}" --output table

# Invoke a function synchronously with payload
aws lambda invoke --function-name <name> --payload '{"key": "value"}' --cli-binary-format raw-in-base64-out response.json
```

### Deployment & Configuration
```bash
# Update function code via ZIP
aws lambda update-function-code --function-name <name> --zip-file fileb://function.zip

# Update environment variables
aws lambda update-function-configuration --function-name <name> --environment "Variables={KEY=VALUE,ENV=PROD}"
```

### Performance & Scaling
```bash
# Check concurrency limits and usage
aws lambda get-account-settings --query "AccountLimit"

# Put provisioned concurrency (warm start optimization)
aws lambda put-provisioned-concurrency-config --function-name <name> --qualifier <alias> --provisioned-concurrent-executions 5
```

## 🧠 Best Practices
1. **Layer Management**: Offload heavy dependencies (like FFmpeg or Chromium) into Lambda Layers to keep deployment packages small.
2. **Timeout Strategy**: Set aggressive timeouts to prevent runaway costs from stuck executions.
3. **IAM Execution Role**: Ensure the role has *exactly* the permissions needed for S3/DynamoDB access—no more.
4. **Monitoring**: Use CloudWatch Insights to trace latencies and cold starts.
