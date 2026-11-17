# Recover: Start a Stopped ECS

Applies when diagnosis shows the ECS instance is `Stopped`.

## Confirmation gate

Before doing anything, present and get explicit confirmation:

- Target: ECS `<ecs-id>` in `<region>`.
- Action: start the instance (`StartInstance`).
- Interruption: instance boots; app returns once services are up.
- Version change: none.
- New cost: running instance resumes hourly billing.
- Verification: wait for `Running`, then check `/healthz` and services.
- If it fails: report and stop; do not retry blindly.

If the user declines → change nothing.

## Execute (one action)

```bash
aliyun ecs StartInstance --RegionId <region> --InstanceId <ecs-id>
```

Idempotent: if already `Running`, treat as success.

## Wait for Running

Poll `DescribeInstances` until `Status == Running` (bounded retries). On timeout or an unexpected
state, stop further writes and report.

Then verify and record the audit entry (`workflow.md`).
