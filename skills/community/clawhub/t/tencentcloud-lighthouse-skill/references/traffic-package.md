# Lighthouse Traffic Package Management

## Query Traffic Packages

```bash
# Query traffic package info for specific instances
tccli lighthouse DescribeInstancesTrafficPackages --region ap-guangzhou \
  --InstanceIds '["lhins-xxxxxxxx"]'
```

## Response Fields

| Field | Description |
|-------|-------------|
| TrafficPackageTotal | Total traffic allowance (bytes) |
| TrafficUsed | Traffic already used (bytes) |
| TrafficPackageRemaining | Remaining traffic (bytes) |
| StartTime | Package start time |
| EndTime | Package end time |

## Usage Tips

- Traffic packages reset monthly based on the instance billing cycle
- Exceeding the traffic limit may result in bandwidth throttling or additional charges depending on the plan
- Monitor traffic usage regularly for instances with high public network traffic
- Use `tccli monitor GetMonitorData` with `WanOuttraffic` / `WanIntraffic` metrics for real-time bandwidth monitoring