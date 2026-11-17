# Minimal Diagnosis

Read-only. No confirmation required. Stop at the first clearly actionable fault layer, but gather
enough evidence to recommend one action.
Judge in short-circuit order; merge the read-only checks on one ECS into a single Cloud Assistant
script fetched in one round trip to cut round trips.

`<service_name>` comes from the state file's `service_name` field (falls back to `qwencloud-app` when missing).

When a fresh `observe_handoff.json` (from `qwencloud-observe`) exists in the project directory, read
its `fault_layer` and `symptoms` first as a starting point and verify that layer first. It is a hint,
not a conclusion — still verify independently via the checks below before recommending an action;
when the hint conflicts with what you measure, trust the measurement.

## Checks

> A green entry probe is not application/host health. For "slow / intermittent / occasional
> timeout" symptoms, do not conclude from the probe — capture live host CPU/memory/load in the
> step-3 Cloud Assistant script (`top -bn1`, `uptime`, `free -m`) and judge from the measurement.

1. **Public entry** — probe the public address and `/healthz`:

   ```bash
   curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' --max-time 10 "http://<public_ip>/healthz"
   curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' --max-time 10 "http://<public_ip>/"
   ```

2. **ECS status** — `aliyun ecs DescribeInstances`. Stopped → likely a stopped-instance recovery.

3. **App service / Nginx / ports / recent logs** (read-only Cloud Assistant):

   > `<app_port>` comes from the state file `app_port`; when that field is empty, use `8080`. Never
   > substitute an empty string, or the port match degrades into matching any listening port.

   ```bash
   aliyun ecs RunCommand --RegionId <region> --Type RunShellScript --InstanceId.1 <ecs-id> \
     --ContentEncoding Base64 \
     --CommandContent "$(printf '%s' 'systemctl is-active <service_name>; systemctl is-active nginx; ss -ltnp | grep -E ":80|:<app_port>"; nginx -t 2>&1 | tail -n 3; df -h /; uptime; top -bn1 | head -n 12; free -m; journalctl -u <service_name> --since "30 min ago" --no-pager | tail -n 80' | base64)"
   aliyun ecs DescribeInvocations --RegionId <region> --InvokeId <invoke-id> --IncludeOutput true
   ```

   Root filesystem use ≥ 90% (or app failing to write / start with no space) → likely disk reclaim.

   `<service_name>` inactive → likely an app-service restart. `nginx -t` failing / nginx inactive →
   likely Nginx handling.

   CPU pinned near full / load far above the core count while the probe still passes → investigate
   via app-service handling (`recover_app.md`).

   When the port listens internally (`ss` shows 80 / `<app_port>` bound) but the public probe in
   step 1 fails, check the security-group ingress instead of assuming the service is down, using
   `outputs.security_group_id` (fallback: read it from `DescribeInstances`):

   ```bash
   aliyun ecs DescribeSecurityGroupAttribute --RegionId <region> --SecurityGroupId <sg-id> --Direction ingress
   ```

   No ingress rule allowing 80 / 443 → the fault is a closed port, not a dead service.

   When the port listens locally, the security group allows it, but public access still fails, check
   whether the EIP is unbound / overdue (prefer `outputs.eip_allocation_id`; when absent, look it up
   via `--AssociatedInstanceId`):

   ```bash
   aliyun vpc DescribeEipAddresses --RegionId <region> --AllocationId <eip-id>
   ```

   EIP unbound (`Available`) → likely a re-bind. Frozen for non-payment → advise only, outside the
   recovery whitelist.

4. **RDS (if present)** — status, ECS→RDS connectivity, connection pressure, slow SQL
   (`DescribeDBInstances`, `DescribeDBInstancePerformance`, `DescribeSlowLogRecords`). App logs
   showing DB timeout / auth failure / refused / pool waits → likely RDS-related handling.

5. **Certificate (only when the app has a domain)** — when the public entry fails on HTTPS or the
   HTTPS handshake errors, read the certificate expiry (read-only), using `outputs.cert_path`
   (fallback `/etc/qwencloud/certbot/config/live/<domain>/fullchain.pem`):

   ```bash
   openssl x509 -checkend 0 -noout -in <cert_path> || echo EXPIRED
   openssl x509 -enddate -noout -in <cert_path>
   ```

   Expired / expiring / missing cert with an HTTPS failure → likely a certificate re-issue.

## Output

Report: **fault layer · likely cause · evidence · recommended action · impact**. Redact secrets in
all evidence. Do not execute any recovery yet.

## Mapping to recovery

| Diagnosis | Action reference |
|-----------|------------------|
| ECS Stopped | `recover_ecs.md` |
| ECS Running but hung (probe/Cloud Assistant both time out) | `recover_reboot.md` |
| `<service_name>` inactive / pool broken | `recover_app.md` |
| Nginx abnormal | `recover_nginx.md` |
| RDS not running / conn pressure / slow SQL | `recover_rds.md` |
| Certificate expired / HTTPS handshake fails | `recover_cert.md` |
| Root disk near full (≥ 90%) | `recover_disk.md` |
| Security group missing 80 / 443 ingress | `recover_securitygroup.md` |
| EIP unbound | `recover_eip.md` |
| Root disk physically too small (still short after cleanup) | `recover_disk.md` (resize section) |
