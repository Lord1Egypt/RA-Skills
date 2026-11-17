# Observe · Public entry and exposure

Assess the EIP public entry and the security-group exposure surface. All read-only. Prefer
`outputs.eip_allocation_id` from the state file; when absent, look it up via
`--AssociatedInstanceId <ecs-id>`.

## EIP status and bandwidth

```bash
aliyun vpc DescribeEipAddresses --RegionId <region> --AllocationId <eip-id>
```

Read `Status` (`InUse` / `Available` / …), the bound instance, bandwidth cap, and `ChargeType`.

- Unbound (`Available`) or frozen for non-payment → `unavailable`; public probes will fail.
- Bound and healthy → check bandwidth next.

Bandwidth time series (namespace `acs_vpc_eip`):

```bash
aliyun cms DescribeMetricList --Namespace acs_vpc_eip \
  --MetricName net_tx.rate --Dimensions '[{"instanceId":"<eip-id>"}]' \
  --StartTime <start> --EndTime <end> --Period 60
```

Repeat for `net_rx.rate`. Sustained egress/ingress near the cap or packet loss → `degraded`.

## Security-group exposure (read-only)

```bash
aliyun ecs DescribeSecurityGroupAttribute --RegionId <region> --SecurityGroupId <sg-id> --Direction ingress
```

- No ingress rule allowing 80 / 443 → a likely cause of public unreachability; flag as a risk.
- 22 (SSH) / 3306 (MySQL) open to `0.0.0.0/0` → exposure risk; `degraded` with a tightening tip.

## Result

Fold into the application/availability evidence: EIP status and bandwidth headroom, exposure risks.
When the EIP is unbound or 80/443 is missing, offer to fix it with `qwencloud-operate`.
