# Recover: reboot a hung ECS

Applies when the instance is `Running` but public probes and Cloud Assistant commands both keep
timing out (a hung instance). Distinct from starting a stopped instance (see `recover_ecs.md`). Try
restarting the app service first (`recover_app.md`); reboot the instance only when Cloud Assistant
is also unresponsive and you cannot act inside the instance.

## Confirmation gate

- Target: ECS `<ecs-id>`, region `<region>`.
- Action: reboot the instance (`RebootInstance`).
- Interruption: the app is briefly unavailable during the reboot.
- Version change: none.
- New cost: none.
- Verify: wait for `Running`, then check services, `/healthz`, and the home page.
- On failure: report and stop; do not retry blindly.

Decline → change nothing.

## Execute (one action)

```bash
aliyun ecs RebootInstance --RegionId <region> --InstanceId <ecs-id>
```

## Wait for Running

Poll `DescribeInstances` until `Status == Running` (bounded retries). On timeout or an unexpected
state, stop further writes and report. Then verify and record the audit (`workflow.md`).
