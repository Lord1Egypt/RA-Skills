# Aliyun CLI Gotchas

Check this table before a call to avoid per-product shape/format differences of same-named
parameters. Everything here is grounded in the real error messages.

## Parameter shape

Get same-named parameter shapes right, or the call returns `InvalidParameter` / `MissingParam`:

- **`InstanceIds`** — ECS (`DescribeInstances`) wants a JSON array string `'["<ecs-id>"]'`; a bare
  string returns `InvalidParameter`.
- **`RunCommand` instance param** — use the `.N` repeated form `--InstanceId.1 <ecs-id>`; a bare
  `--InstanceId` returns `MissingParam.InstanceId`.

## Time parameter format

`StartTime` / `EndTime` use UTC ISO8601, precision per product — the wrong one returns
`InvalidStartTime.Malformed`:

- **RDS `DescribeDBInstancePerformance`** — to the minute, **no seconds**: `YYYY-MM-DDTHH:mmZ`
  (e.g. `2026-09-09T08:00Z`; Python `%Y-%m-%dT%H:%MZ`).

The error message usually states the format that interface expects.

## Response parsing

- **ECS `DescribeInvocations` command output** — add `--IncludeOutput true`; the echo is in
  `Invocations.Invocation[0].InvokeInstances.InvokeInstance[0].Output`, Base64-encoded, decode it;
  poll `InvokeRecordStatus` until `Finished` before reading.
