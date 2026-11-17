# Error Handling & Constraints

## Error Quick Reference

| Symptom                               | Cause                                      | Resolution                                                                    |
|---------------------------------------|--------------------------------------------|-------------------------------------------------------------------------------|
| Env check: CLI not installed / too old | `aliyun version` fails                     | Tell user to install: https://www.alibabacloud.com/help/en/cli/install-update-alibaba-cloud-cli |
| Env check: Invalid credentials         | `configure list` shows no Valid profile    | Follow `reference/deploy/01_env_check.md` Auth Flow to re-login                         |
| Env check: Identity probe failed       | `GetCallerIdentity` errors                 | Authorization may have expired; go back to Auth Flow and re-login              |
| `InvalidTemplate`                     | YAML syntax error                          | Read Message and fix template                                                 |
| `InsufficientStock`                   | Out of stock                               | Provide 2-3 alternatives (larger instance type / different region)            |
| `InvalidParameter`                    | Password doesn't meet requirements         | Regenerate a strong password                                                  |
| Stack rollback `ROLLBACK_COMPLETE`    | Resource creation failed                   | Use `ListStackResources` to locate the failed resource                        |
| Nginx health check fails but stack succeeds | UserData hasn't finished / Nginx broken | Check `/var/log/qwencloud-bootstrap.log`                                |
| Nginx up but app not started (`app: "manual"` unverified) | App crashed / not started yet | Check `/var/log/$APP_NAME.log` via Cloud Assistant                 |
| `DELETE_FAILED`                       | Resource occupied externally               | Manual cleanup via ROS console                                                |
| Password lost                         | `.local` file accidentally deleted         | Reset password via ECS/RDS console                                            |
| RunCommand timeout                    | Cloud Assistant not responding             | Check ECS status and `DescribeCloudAssistantStatus`                           |
| RunCommand permission denied          | Missing `ecs:RunCommand` permission        | Add `AliyunECSFullAccess` or grant precise permissions                        |
| App not starting after hot update     | Issue with new version artifacts           | Check remote log `/var/log/qwencloud-update.log`, fix and re-run hot update   |
| Cloud Assistant unavailable           | Not installed or not started               | `systemctl start aliyun.service`                                              |
| Security group port 80 not open       | Rule missing                               | Add inbound TCP 80 rule in ECS console                                        |
| Certbot DNS-01 TXT not found          | TXT record not yet propagated              | Wait longer (up to 5min), verify with `dig +short _acme-challenge.DOMAIN TXT` |
| Certbot "too many failed auth"        | Rate limited by Let's Encrypt              | Wait 1 hour, then retry                                                       |
| RDS `InvalidDBInstanceClass`          | Instance class unavailable                 | Check available classes in RDS console                                        |
| RDS availability zone not supported   | ECS has stock but RDS doesn't              | Re-run the stock check (see `reference/deploy/08_check_stock.md`) with `DB_INSTANCE_CLASS` to validate the RDS zone |
| `QuotaExceed.Instance`                | Quota full                                 | Clean up idle instances or request quota increase                             |

## Constraints

**Templates & API**:

- ROS must use `--TemplateURL` (`--TemplateBody` is blocked by WAF)
- Availability zone must come from the in-stock type selected in step 6 (`ZONE_ID`); when RDS is needed, take the ECS ∩ RDS intersection per `reference/deploy/08_check_stock.md`
- `DisableRollback=false` and `from=qwencloud` tag are mandatory
- Never skip `ValidateTemplate`

**Artifacts & OSS**:

- Temporary bucket is recorded in `.qwencloud-deploy`; `delete_stack.sh` depends on it for cleanup

**Passwords**:

- Special characters limited to `!@%^*+=_-` (`& # $ | ;` will break `db.env` source)
- ECS and RDS passwords are generated separately, recorded separately, and never shown in chat

**Health Check**:

- `/healthz` only proves Nginx is alive; app liveness is verified separately by reading its log via Cloud Assistant (not HTTP-probed)

**RDS**:

- MySQL 8.0 only — PG/Redis/MongoDB not supported
- Single AZ; password must not be reused from ECS
- `Fn::Sub` main script uses base64 encoding injection, decoded + sourced at runtime to avoid shell variable conflicts
  with Fn::Sub

## Current Limitations

- Full-stack uses pay-as-you-go only; subscription (prepaid) not supported
- HTTPS always uses DNS-01 validation (TXT record based)
- Single region
## Server Troubleshooting Reference

How to debug ECS issues via Cloud Assistant RunCommand when health checks fail.

## Server Troubleshooting (verify the app via logs)

Two logs to check: `/var/log/qwencloud-bootstrap.log` (UserData bootstrap process), `/var/log/$APP_NAME.log`
(application stdout/stderr).
`$APP_NAME` here is the deploy-time environment variable (the service name); for post-deploy
troubleshooting use the operate skill (which reads `service_name` from the state file).

### Cloud Assistant RunCommand

ECS has a built-in Cloud Assistant — run shell commands directly on the instance:

```bash
# 1. Execute (PlainText — do NOT base64-encode CommandContent)
CID=$(PAGER=cat aliyun ecs RunCommand \
  --RegionId "$REGION" --InstanceId.1 "$INSTANCE_ID" --Type RunShellScript \
  --Timeout 60 --ContentEncoding PlainText \
  --CommandContent "systemctl status $APP_NAME --no-pager; echo ---; tail -n 100 /var/log/$APP_NAME.log" \
  | python3 -c 'import sys,json;print(json.load(sys.stdin)["InvokeId"])')

# 2. Get results (async, poll until Finished)
sleep 8
PAGER=cat aliyun ecs DescribeInvocations --RegionId "$REGION" --InvokeId "$CID" --IncludeOutput true \
  | python3 -c 'import sys,json,base64; d=json.load(sys.stdin); r=d["Invocations"]["Invocation"][0]["InvokeInstances"]["InvokeInstance"][0]; print(base64.b64decode(r["Output"]).decode())'
```

> ⚠️ **Do NOT base64-encode `--CommandContent`**. Despite some documentation examples,
> Cloud Assistant with `--ContentEncoding PlainText` (default) expects a raw shell script
> string. Base64-encoded content will be executed literally as garbled commands.

`<ECS_INSTANCE_ID>` is from `ListStackResources` where `ResourceType=ALIYUN::ECS::Instance` → `PhysicalResourceId`.
Troubleshoot → edit config → `systemctl restart $APP_NAME` → re-read the app log to confirm it started — all via RunCommand.

> ⚠️ `aliyun` CLI **does not have a `--no-pager` argument** (passing it will cause an error). In non-interactive
> environments, use `PAGER=cat aliyun ...` to disable paging.
