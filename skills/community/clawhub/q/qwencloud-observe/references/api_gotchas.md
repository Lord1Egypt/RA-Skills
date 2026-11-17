# Aliyun CLI Gotchas

Check this table before a call to avoid per-product shape/format differences of same-named
parameters. Everything here is grounded in the real error messages.

## Parameter shape

Same-named parameters take different shapes across products — the wrong shape returns
`InvalidParameter` / `MissingParam`:

- **`InstanceIds`** — ECS (`DescribeInstances`) wants a JSON array string `'["<ecs-id>"]'`;
  CMS (`DescribeMonitoringAgentStatuses`) wants a bare string `<ecs-id>`. A bare string to ECS
  returns `InvalidParameter`.
- **`RunCommand` instance param** — use the `.N` repeated form `--InstanceId.1 <ecs-id>`; a bare
  `--InstanceId` returns `MissingParam.InstanceId`.
- **Installing the CloudMonitor agent** — use the API `aliyun cms InstallMonitoringAgent --Force true
  --InstanceIds.1 <ecs-id>` (`.N` form).

## Time parameter format

`StartTime` / `EndTime` use UTC ISO8601, but **precision differs per product** — the wrong one
returns `InvalidStartTime.Malformed`:

- **CMS `DescribeMetricList`** — to the second: `YYYY-MM-DDTHH:mm:ssZ` (e.g. `2026-09-09T08:00:00Z`).
- **RDS `DescribeDBInstancePerformance`** — to the minute, **no seconds**: `YYYY-MM-DDTHH:mmZ`
  (e.g. `2026-09-09T08:00Z`).

Format the time per target API (Python `%Y-%m-%dT%H:%M:%SZ` and `%Y-%m-%dT%H:%MZ` respectively);
the error message usually states the format that interface expects.

## Response parsing

A few response fields are not read directly:

- **CMS `DescribeMetricList` `Datapoints`** — an escaped JSON string (not an array); `json.loads`
  it again to get `[{"timestamp","Average","Maximum",...}]`. An empty string means no datapoints
  in the window.
- **RDS `DescribeDBInstancePerformance`** — values are nested under
  `PerformanceKeys.PerformanceKey[].Values.PerformanceValue[]`, each point `{"Date","Value"}`;
  `Value` is often a comma-separated multi-column string (e.g. QPS,TPS) — split by the columns its
  `Key` defines.
- **ECS `DescribeInvocations` command output** — add `--IncludeOutput true`; the echo is in
  `Invocations.Invocation[0].InvokeInstances.InvokeInstance[0].Output`, Base64-encoded, decode it;
  poll `InvokeRecordStatus` until `Finished` before reading.
