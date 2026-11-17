# Recover: Restart the App Service

Applies when `<service_name>` is not running or the connection pool is broken. `<service_name>`
comes from the state file's `service_name` field (falls back to `qwencloud-app` when missing).

## Confirmation gate

- Target: service `<service_name>` on ECS `<ecs-id>`.
- Action: `systemctl restart <service_name>`.
- Interruption: brief — the app restarts.
- Version change: none (code unchanged).
- New cost: none.
- Verification: service stable, then port, `/healthz`, and homepage; for pool issues also confirm
  RDS connections recover.
- If it fails: report the failure step and stop.

Decline → change nothing.

## Execute (one whitelisted recovery command)

```bash
aliyun ecs RunCommand --RegionId <region> --Type RunShellScript --InstanceId.1 <ecs-id> \
  --ContentEncoding Base64 \
  --CommandContent "$(printf '%s' 'systemctl restart <service_name> && sleep 3 && systemctl is-active <service_name>' | base64)"
aliyun ecs DescribeInvocations --RegionId <region> --InvokeId <invoke-id> --IncludeOutput true
```

Idempotent: restart is safe to repeat. Do not chain other changes into the same command.

Then verify and record the audit entry (`workflow.md`).
