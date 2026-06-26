---
name: watadot-aws-iam
description: IAM security patterns by Watadot Studio. Manage users, roles, and policy verification.
metadata:
  openclaw:
    emoji: 🔐
    requires:
      anyBins: [aws]
---

# AWS IAM Skills

Security-first identity and access management patterns.

## 🚀 Core Commands

### Identity Audit
```bash
# List all users with ARN and creation date
aws iam list-users --query "Users[].{User:UserName,Arn:Arn,Date:CreateDate}" --output table

# Find unused access keys (90+ days)
aws iam list-users --query "Users[].UserName" --output text | xargs -I {} aws iam list-access-keys --user-name {} --query "AccessKeyMetadata[?Status==\`Active\` && CreateDate < \`2025-12-31\`]"
```

### Role Orchestration
```bash
# Assume a role and get temporary credentials
aws sts assume-role --role-arn <role-arn> --role-session-name "OpenClawSession"

# List policies attached to a specific role
aws iam list-attached-role-policies --role-name <role-name> --query "AttachedPolicies[].PolicyName"
```

### Policy Verification
```bash
# Get effective policy document
aws iam get-policy-version --policy-arn <arn> --version-id <id> --query "PolicyVersion.Document"
```

## 🧠 Best Practices
1. **Never use Root**: Use IAM users or SSO roles for daily operations.
2. **Short-lived Credentials**: Prefer `sts assume-role` over permanent access keys.
3. **MFA Enforcement**: Enable Multi-Factor Authentication for all console and sensitive CLI access.
4. **Access Analyzer**: Regularly run IAM Access Analyzer to find unintended public or cross-account access.
