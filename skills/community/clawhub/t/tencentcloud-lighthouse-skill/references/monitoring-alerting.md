# Lighthouse Monitoring and Alerting

## Query Monitoring Data

The monitoring namespace for Lighthouse is `QCE/LIGHT_HOUSE`.

### Supported Metrics

| Metric | Description |
|--------|-------------|
| CpuUsage | CPU utilization (%) |
| MemUsage | Memory utilization (%) |
| LanOuttraffic | Private network outbound bandwidth |
| LanIntraffic | Private network inbound bandwidth |
| WanOuttraffic | Public network outbound bandwidth |
| WanIntraffic | Public network inbound bandwidth |

### Query Examples

```bash
# CPU utilization over a time range
tccli monitor GetMonitorData --region ap-guangzhou \
  --Namespace QCE/LIGHT_HOUSE \
  --MetricName CpuUsage \
  --Instances '[{"Dimensions":[{"Name":"InstanceId","Value":"lhins-xxxxxxxx"}]}]' \
  --Period 300 \
  --StartTime "2026-03-24T00:00:00+08:00" \
  --EndTime "2026-03-24T12:00:00+08:00"

# Memory utilization (latest)
tccli monitor GetMonitorData --region ap-guangzhou \
  --Namespace QCE/LIGHT_HOUSE \
  --MetricName MemUsage \
  --Instances '[{"Dimensions":[{"Name":"InstanceId","Value":"lhins-xxxxxxxx"}]}]' \
  --Period 300
```

### Parameters

- `Period`: Data granularity in seconds (60, 300, 3600, 86400)
- `StartTime` / `EndTime`: ISO 8601 format with timezone
- `Instances`: Array of instance dimension filters

## Create Alarm Policy

```bash
tccli monitor CreateAlarmPolicy --region ap-guangzhou \
  --Module monitor \
  --PolicyName "CPU-High-Load" \
  --Namespace QCE/LIGHT_HOUSE \
  --Conditions '{"IsUnionRule":false,"Rules":[{"MetricName":"CpuUsage","Period":300,"Operator":"Ge","Value":"80","ContinuePeriod":3,"NoticeFrequency":3600,"IsPowerNotice":0}]}'
```

> Use `tccli monitor CreateAlarmPolicy --help` to check the latest parameter schema before creating policies.

## Workflow

1. First get the InstanceId via `tccli lighthouse DescribeInstances`
2. Query monitoring data with appropriate time range and period
3. For alerting, create alarm policies with reasonable thresholds