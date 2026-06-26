# Tencent Cloud Sub-User Permission Configuration Guide

**Important**: For security, use sub-user credentials instead of master account keys.

---

## Permission Policy Templates

### Policy 1: Resource Administrator (Recommended)

This policy grants full management permissions for CVM, Lighthouse, and COS (excluding delete and finance permissions).

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "cvm:Describe*", "cvm:RunInstances", "cvm:StartInstances",
        "cvm:StopInstances", "cvm:RestartInstances", "cvm:ModifyInstancesAttribute",
        "cvm:RenewInstances", "vpc:DescribeSecurityGroups", "vpc:CreateSecurityGroup",
        "lighthouse:Describe*", "lighthouse:CreateInstance", "lighthouse:StartInstances",
        "lighthouse:StopInstances", "lighthouse:RestartInstances",
        "lighthouse:ModifyInstancesAttribute", "lighthouse:RenewInstance",
        "name/cos:GetBucket", "name/cos:PutBucket", "name/cos:ListBucket",
        "name/cos:GetObject", "name/cos:PutObject", "name/cos:DeleteObject",
        "name/cos:PutBucketLifecycle", "name/cos:GetBucketLifecycle"
      ],
      "resource": "*"
    }
  ]
}
```

---

### Policy 2: Read-Only Viewer

Query permissions only, suitable for monitoring and auditing purposes.

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "cvm:Describe*", "lighthouse:Describe*",
        "name/cos:GetBucket", "name/cos:ListBucket", "name/cos:GetObject"
      ],
      "resource": "*"
    }
  ]
}
```

---

### Policy 3: CVM Specialist

CVM cloud server management only.

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "cvm:Describe*", "cvm:RunInstances", "cvm:StartInstances",
        "cvm:StopInstances", "cvm:RestartInstances", "cvm:ModifyInstancesAttribute",
        "cvm:RenewInstances", "vpc:DescribeSecurityGroups"
      ],
      "resource": "*"
    }
  ]
}
```

---

### Policy 4: Lighthouse Specialist

Lightweight application server management only.

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "lighthouse:Describe*", "lighthouse:CreateInstance",
        "lighthouse:StartInstances", "lighthouse:StopInstances",
        "lighthouse:RestartInstances", "lighthouse:ModifyInstancesAttribute",
        "lighthouse:RenewInstance"
      ],
      "resource": "*"
    }
  ]
}
```

---

### Policy 5: COS Specialist

Object storage management only.

```json
{
  "version": "2.0",
  "statement": [
    {
      "effect": "allow",
      "action": [
        "name/cos:GetBucket", "name/cos:PutBucket", "name/cos:ListBucket",
        "name/cos:GetObject", "name/cos:PutObject", "name/cos:DeleteObject",
        "name/cos:PutBucketLifecycle", "name/cos:GetBucketLifecycle"
      ],
      "resource": "*"
    }
  ]
}
```

---

## Configuration Steps

1. Visit https://console.cloud.tencent.com/cam/policy
2. Click "Create Custom Policy"
3. Paste the policy template above
4. Enter policy name, click "OK"
5. Visit https://console.cloud.tencent.com/cam/user to create sub-user
6. Associate policy to sub-user
7. Copy SecretId and SecretKey to .env file

---

## Security Best Practices

- Use sub-user keys, not master account
- Add .env to .gitignore
- Rotate keys regularly (90 days)
- Set minimum permissions
- Do not commit keys to Git
- Do not grant finance permissions

---

## Documentation

- [Skill Description](../SKILL.md)
- [CAM User Management](https://cloud.tencent.com/document/product/598)
