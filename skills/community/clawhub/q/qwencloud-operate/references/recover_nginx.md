# Recover: Nginx

Applies when Nginx is abnormal. **Always validate config before reload/restart.**

## Step 1 — Validate config (read-only)

```bash
aliyun ecs RunCommand --RegionId <region> --Type RunShellScript --InstanceId.1 <ecs-id> \
  --ContentEncoding Base64 --CommandContent "$(printf '%s' 'nginx -t 2>&1' | base64)"
aliyun ecs DescribeInvocations --RegionId <region> --InvokeId <invoke-id> --IncludeOutput true
```

- **`nginx -t` fails** → STOP. Do not reload/restart. Return the error location and remediation
  advice. This is a hard gate.
- **`nginx -t` passes** → proceed to the confirmation gate.

## Step 2 — Confirmation gate

- Target: Nginx on ECS `<ecs-id>`.
- Action: reload (preferred) or restart Nginx.
- Interruption: reload is near-zero; restart is brief.
- Version change: none.
- New cost: none.
- Verification: `/healthz` and homepage.
- If it fails: report and stop.

Decline → change nothing.

## Step 3 — Execute (one whitelisted command, only after `nginx -t` passed)

```bash
aliyun ecs RunCommand --RegionId <region> --Type RunShellScript --InstanceId.1 <ecs-id> \
  --ContentEncoding Base64 --CommandContent "$(printf '%s' 'nginx -t && systemctl reload nginx && systemctl is-active nginx' | base64)"
```

Idempotent. Then verify and record the audit entry (`workflow.md`).
