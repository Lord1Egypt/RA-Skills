# RAM Policies for qwencloud-operate

Read permissions for diagnosis + verification; write permissions for the confirmed recovery
actions only.

## Required permissions

| Action | Type | Purpose |
|--------|------|---------|
| `ecs:DescribeInstances` | read | ECS status during diagnosis/verification |
| `ecs:DescribeInvocations` | read | Read Cloud Assistant results |
| `ecs:DescribeSecurityGroupAttribute` | read | Ingress rule check (80 / 443 allowed) |
| `ecs:DescribeDisks` | read | Get root disk ID (resize prerequisite) |
| `vpc:DescribeEipAddresses` | read | EIP binding-state diagnosis |
| `rds:DescribeDBInstances` | read | RDS status (RDS topology) |
| `rds:DescribeDBInstancePerformance` | read | RDS performance (RDS topology) |
| `rds:DescribeSlowLogRecords` | read | Slow SQL (RDS topology) |
| `ecs:StartInstance` | write | Start a stopped ECS |
| `ecs:RebootInstance` | write | Reboot a hung ECS |
| `ecs:AuthorizeSecurityGroup` | write | Allow 80 / 443 ingress rules |
| `ecs:ResizeDisk` | write | Resize the root disk (still short after cleanup) |
| `vpc:AssociateEipAddress` | write | Re-bind an unbound EIP |
| `ecs:RunCommand` | write | Run whitelisted recovery commands (app / Nginx) |
| `alidns:AddDomain` | write | Ensure the AliDNS zone exists (cert re-issue) |
| `alidns:DescribeDomainRecords` | read | Look up the `_acme-challenge` TXT record (cert re-issue) |
| `alidns:AddDomainRecord` | write | Create the DNS-01 TXT record (cert re-issue) |
| `alidns:UpdateDomainRecord` | write | Update the DNS-01 TXT record (cert re-issue) |
| `alidns:DeleteDomainRecord` | write | Clean up the TXT record after issuance (cert re-issue) |

## Policy JSON

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:DescribeInstances",
        "ecs:DescribeInvocations",
        "ecs:DescribeSecurityGroupAttribute",
        "ecs:DescribeDisks",
        "vpc:DescribeEipAddresses",
        "rds:DescribeDBInstances",
        "rds:DescribeDBInstancePerformance",
        "rds:DescribeSlowLogRecords",
        "ecs:StartInstance",
        "ecs:RebootInstance",
        "ecs:AuthorizeSecurityGroup",
        "ecs:ResizeDisk",
        "vpc:AssociateEipAddress",
        "ecs:RunCommand",
        "alidns:AddDomain",
        "alidns:DescribeDomainRecords",
        "alidns:AddDomainRecord",
        "alidns:UpdateDomainRecord",
        "alidns:DeleteDomainRecord"
      ],
      "Resource": "*"
    }
  ]
}
```

## On permission failure

A `Forbidden.RAM` on a write action → stop before the write, report the missing permission, and do
not attempt the recovery. A failure on a read action → report the unknown item and continue the
rest of the diagnosis.
