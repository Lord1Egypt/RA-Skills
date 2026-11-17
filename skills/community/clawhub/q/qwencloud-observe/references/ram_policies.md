# RAM Policies for qwencloud-observe

All permissions are read-only except `cms:InstallMonitoringAgent` (lazy agent install); Cloud
Assistant commands run by this skill are read-only checks.

## Required permissions

| Action | Purpose |
|--------|---------|
| `ecs:DescribeInstances` | ECS status / spec / network |
| `ecs:RunCommand` | Run service/port/memory-snapshot scripts |
| `ecs:DescribeInvocations` | Read Cloud Assistant command results |
| `cms:DescribeMetricList` | ECS CPU / network / disk / memory time series |
| `cms:DescribeMonitoringAgentStatuses` | Probe CloudMonitor agent status |
| `cms:InstallMonitoringAgent` | Lazily install the CloudMonitor agent (memory trend) |
| `ecs:DescribeSecurityGroupAttribute` | Security-group exposure check (80/443 open, 22/3306 exposed) |
| `ecs:DescribeInstanceHistoryEvents` | ECS system events (planned maintenance / retirement) |
| `ecs:DescribeSnapshots` | System-disk snapshot status |
| `vpc:DescribeEipAddresses` | EIP status and bandwidth |
| `bssopenapi:QueryInstanceBill` | Actual per-instance billing (cost) |
| `bssopenapi:QueryBill` | Bill overview (month-end projection) |
| `rds:DescribeDBInstances` | RDS status (RDS topology) |
| `rds:DescribeDBInstanceAttribute` | RDS spec / storage (RDS topology) |
| `rds:DescribeDBInstancePerformance` | RDS performance series (RDS topology) |
| `rds:DescribeSlowLogRecords` | Slow SQL (RDS topology) |
| `rds:DescribeBackups` | RDS backup status (RDS topology) |

## Policy JSON

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ecs:DescribeInstances",
        "ecs:RunCommand",
        "ecs:DescribeInvocations",
        "cms:DescribeMetricList",
        "cms:DescribeMonitoringAgentStatuses",
        "cms:InstallMonitoringAgent",
        "ecs:DescribeSecurityGroupAttribute",
        "ecs:DescribeInstanceHistoryEvents",
        "ecs:DescribeSnapshots",
        "vpc:DescribeEipAddresses",
        "bssopenapi:QueryInstanceBill",
        "bssopenapi:QueryBill",
        "rds:DescribeDBInstances",
        "rds:DescribeDBInstanceAttribute",
        "rds:DescribeDBInstancePerformance",
        "rds:DescribeSlowLogRecords",
        "rds:DescribeBackups"
      ],
      "Resource": "*"
    }
  ]
}
```

## On permission failure

A `Forbidden.RAM` on any call → mark that layer `unknown` with the missing action, keep checking
the other layers, and list the missing permissions in the report. Do not stop the whole run.
