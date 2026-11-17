# Observe Application

Assess whether the deployed application is reachable and its services are up. All Cloud Assistant
commands are **read-only**.

## Public availability

Probe the public address and `/healthz`:

```bash
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' --max-time 10 "http://<public_ip>/healthz"
curl -s -o /dev/null -w '%{http_code} %{time_total}s\n' --max-time 10 "http://<public_ip>/"
```

Record HTTP status, current response time, and failure reason (timeout / connection refused / 5xx).

- 2xx/3xx → application layer `healthy`.
- 5xx or app up but errors → `degraded`.
- Connection refused / timeout → `unavailable`.

## Service + port check (Cloud Assistant, read-only)

Run one read-only script on the ECS instance and fetch its result:

> `<app_port>` comes from the state file `app_port`; when that field is empty, use `8080`. Never
> substitute an empty string, or the match pattern degrades into matching any listening port.

```bash
aliyun ecs RunCommand --RegionId <region> --Type RunShellScript --InstanceId.1 <ecs-id> \
  --ContentEncoding Base64 \
  --CommandContent "$(printf '%s' 'systemctl is-active <service_name>; systemctl is-active nginx; ss -ltnp | grep -E ":80|:<app_port>" || true' | base64)"
```

Then poll:

```bash
aliyun ecs DescribeInvocations --RegionId <region> --InvokeId <invoke-id> --IncludeOutput true
```

Check: `<service_name>` active, `nginx` active (when `nginx_mode` uses it), and the app port /
port 80 listening. `<service_name>` comes from the state file's `service_name`, falling back to
`qwencloud-app` when missing.

## Log summary (read-only)

Summarize recent application logs and Nginx error logs into the main error types — do not dump raw
logs. Read-only tail only, for example:

```bash
journalctl -u <service_name> --since '1 hour ago' --no-pager | tail -n 200
tail -n 200 /var/log/nginx/error.log
```

Redact any AccessKey, token, password, connection-string password, or cookie before reporting.
Report the top error categories and counts, not verbatim secrets.

## Certificate validity (only when the app has a domain)

When `.qwencloud-deploy` has a non-empty `outputs.domain`, read the certificate expiry on the ECS
(read-only Cloud Assistant), using `outputs.cert_path` (fallback
`/etc/qwencloud/certbot/config/live/<domain>/fullchain.pem`):

```bash
openssl x509 -enddate -noout -in <cert_path>
```

Compute the days remaining and score the certificate signal:

- more than 30 days → `healthy`
- 7 to 30 days → `degraded` (renew soon)
- fewer than 7 days, expired, or file missing → `degraded`, and name it in the verdict
  ("certificate expiring / expired")

A degraded certificate does not make the app `unavailable` on its own; fold it into the
application-layer state and call it out. Skip this check cleanly when there is no domain.

## Result

Combine probe + service + logs into one application-layer state with evidence (status code,
response time, which service is down, main error types, and certificate days-remaining when a
domain is set).

A probe only proves the entry is reachable; it is not a health verdict on its own. Judge the
application layer together with the ECS-layer CloudMonitor CPU/memory data points, taking the strictest.
