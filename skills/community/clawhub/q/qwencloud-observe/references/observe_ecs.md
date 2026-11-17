# Observe ECS

Assess ECS run status and performance over the selected window (15m / 1h / 24h, default 1h).

## Status

```bash
aliyun ecs DescribeInstances --RegionId <region> --InstanceIds '["<ecs-id>"]'
```

Read `Status` (Running / Stopped / …), instance type, and network (public/private IP, bandwidth).
A non-Running instance → `unavailable`; report it and note that the public probe will fail.

## CPU / network / disk metrics

Use CloudMonitor time series over the window:

```bash
aliyun cms DescribeMetricList --Namespace acs_ecs_dashboard --MetricName CPUUtilization \
  --Dimensions '[{"instanceId":"<ecs-id>"}]' --StartTime <start> --EndTime <end> --Period 60
```

Repeat for `networkin` / `networkout` and `diskusage` (disk capacity). Identify:

- sustained high CPU (e.g. average high or repeatedly near 100%) → `degraded`
- abnormal network → `degraded`
- disk capacity risk (near full) → `degraded`

## Memory — 3-tier strategy (state the data source in the result)

The memory trend comes from the CloudMonitor agent (`memory_usedutilization`). The agent is
ensured lazily by observe, not installed at deploy time. Follow the tiers in order:

1. **Agent metric (preferred)** — probe status first; if absent, install via the cloud API and
   poll until ready, then query the memory series:

   ```bash
   aliyun cms DescribeMonitoringAgentStatuses --InstanceIds <ecs-id>
   # When not running, install via API (region = <region>), then poll DescribeMonitoringAgentStatuses until running:
   aliyun cms InstallMonitoringAgent --RegionId <region> --Force true --InstanceIds.1 <ecs-id>
   aliyun cms DescribeMetricList --Namespace acs_ecs_dashboard --MetricName memory_usedutilization \
     --Dimensions '[{"instanceId":"<ecs-id>"}]' --StartTime <start> --EndTime <end> --Period 60
   ```

   Output the same window/series shape as CPU. Data source: **CloudMonitor agent (trend)**.

2. **Snapshot fallback** — if the agent cannot install/is abnormal or the metric returns 403 / empty,
   read a current snapshot via read-only Cloud Assistant (`free -m`). Label it
   **snapshot, no trend**.

3. **Unknown** — if neither path yields data, mark memory `unknown` with the reason. Never
   silently omit it.

## Result

ECS-layer state with evidence: status, average/peak CPU, network, disk headroom, and memory
(with its data-source label).

Report `data_source`: `cloudmonitor` when agent trend metrics are used throughout; `fallback`
when any metric drops to a snapshot (e.g. point-in-time memory).
