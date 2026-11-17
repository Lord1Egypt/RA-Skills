# Wait for Stack + Health Check (Step 12)

Single command: poll GetStack to terminal state → extract Outputs → nginx health check → output structured JSON. (App liveness is verified separately via Cloud Assistant, not HTTP-probed.)

---

## Invocation

```bash
python3 scripts/wait_and_probe.py \
  --region "$REGION" \
  --stack-id "$STACK_ID" \
  --has-app
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--region` | Region ID | (required) |
| `--stack-id` | Stack ID | (required) |
| `--has-app` | Flag `app: "manual"` so the agent verifies the app via Cloud Assistant | omit = skip |
| `--max-wait` | Max wait seconds | 1200 (20 min); pass 2700 (45 min) with RDS |
| `--probe-retries` | Health check retry count | 15 |
| `--probe-interval` | Base health check retry interval seconds (grows per attempt, capped at 12s) | 4 |

> For static-only projects (`app_type = static-only`), omit `--has-app`.

### About wait durations

- Without RDS: ECS+EIP is usually ready in 2-5 minutes, so the 1200s default is already generous — no need to raise it.
- With RDS: RDS creation takes ~10-30 minutes, pass `--max-wait 2700`.
- `--max-wait` must be **greater than** step 11's `TIMEOUT_MIN` (the ROS-side timeout, default 15 min / 40 min with RDS).
  Once ROS fails the stack, this script immediately reads the `CREATE_FAILED`/`ROLLBACK_*` terminal state and returns — it never idles until `--max-wait`.
- The nginx `/healthz` check starts **immediately** after the stack reaches a terminal state: when nginx is already up it passes on the first probe with zero wait. Failed attempts back off at 4/8/12s (capped at 12s), giving a ~2.5-minute retry window across 15 attempts — enough for slow cases like installing Nginx.
- A single `aliyun` CLI call exceeding 30s is treated as a transient error and retried instead of aborting the whole wait.

---

## Output Format (stdout JSON)

### Success

```json
{
  "status": "ok",
  "public_ip": "47.xx.xx.xx",
  "instance_id": "i-xxx",
  "outputs": {"PublicIp": "...", "EcsInstanceIds": "i-xxx"},
  "health": {"nginx": "pass", "app": "manual"},
  "elapsed_seconds": 180
}
```

> `app: "manual"` means nginx is up but app liveness is **not** HTTP-probed
> (external probes give false negatives, e.g. Spring Boot 500 on an unmapped
> path). Verify the app via Cloud Assistant — see below.

### Failure

```json
{
  "status": "failed",
  "stage": "health_check",
  "error": "Nginx health check failed after 15 retries",
  "public_ip": "47.xx.xx.xx",
  "instance_id": "i-xxx",
  "outputs": {...},
  "health": {"nginx": "fail", "app": "skip"},
  "elapsed_seconds": 210
}
```

`stage` values: `stack_create` (stack creation failed/timeout), `extract_outputs` (cannot extract IP), `health_check` (nginx probe failed).

---

## Agent Decision Logic

| Output status | Action |
|---------------|--------|
| `ok` | Use `public_ip`, `instance_id`, `outputs` → proceed to step 13 (record state) |
| `failed` + stage=`stack_create` | Run `aliyun ros ListStackResources` to find failed resource, see `reference/rules/rule_error_handling.md` |
| `failed` + stage=`health_check` | Nginx never came up — use Cloud Assistant to check `/var/log/qwencloud-bootstrap.log` |

On `ok` with `app: "manual"`, verify the app before recording success: use Cloud Assistant to read the app log and judge whether it started (a clean startup line / listening port = up). `INSTANCE_ID` = the ECS instance from `ListStackResources`; `$APP_NAME` is the service name set at deploy time.

```bash
CID=$(PAGER=cat aliyun ecs RunCommand --RegionId "$REGION" --InstanceId.1 "$INSTANCE_ID" \
  --Type RunShellScript --Timeout 60 --ContentEncoding PlainText \
  --CommandContent "systemctl status $APP_NAME; echo ---; tail -n 100 /var/log/$APP_NAME.log" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["InvokeId"])')
sleep 8
PAGER=cat aliyun ecs DescribeInvocations --RegionId "$REGION" --InvokeId "$CID" --IncludeOutput true \
  | python3 -c 'import sys,json,base64;d=json.load(sys.stdin);r=d["Invocations"]["Invocation"][0]["InvokeInstances"]["InvokeInstance"][0];print(base64.b64decode(r["Output"]).decode())'
```

---

## Heartbeat

The script prints heartbeat messages to stderr for user feedback:
- `[heartbeat] Waited 60s, current status: CREATE_IN_PROGRESS`
- `[heartbeat] Stack created successfully! IP: 47.xx.xx.xx, starting health check...`
- `[heartbeat] Nginx health check passed (attempt 3)`

---

## Health Check Failure Troubleshooting

Use Cloud Assistant to check logs (see `reference/rules/rule_error_handling.md`):
- `/var/log/qwencloud-bootstrap.log` — UserData bootstrap process
- `/var/log/$APP_NAME.log` — Application stdout/stderr
