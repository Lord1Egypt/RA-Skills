# Recover: allow security-group ingress

Applies when the port listens locally but the security group is missing an ingress rule for 80 /
443. Only whitelisted ports (80, 443) are opened; never open 22 / 3306 or any other port.

## Confirm the gap first (read-only)

```bash
aliyun ecs DescribeSecurityGroupAttribute --RegionId <region> --SecurityGroupId <sg-id> --Direction ingress
```

Confirm the target port (80 and/or 443) really has no allow rule. If present, no action needed.

## Confirmation gate

- Target: security group `<sg-id>`, region `<region>`.
- Action: add ingress rules allowing tcp 80 / 443 (`AuthorizeSecurityGroup`).
- Interruption: none — inbound only.
- Version change: none.
- Exposure: 80 / 443 become publicly reachable, the expected exposure for a web app. Never open
  other ports.
- New cost: none.
- Verify: `DescribeSecurityGroupAttribute` shows the new rule, then check `/healthz` and home page.
- On failure: report and stop.

Decline → change nothing.

## Execute (one action, once per port as needed)

```bash
aliyun ecs AuthorizeSecurityGroup --RegionId <region> --SecurityGroupId <sg-id> \
  --Permissions.1.IpProtocol tcp --Permissions.1.PortRange 80/80 \
  --Permissions.1.SourceCidrIp 0.0.0.0/0 --Permissions.1.Policy accept
```

Same for `443/443`. Idempotent: if the rule exists, treat as success. Then verify and record the
audit (`workflow.md`).
