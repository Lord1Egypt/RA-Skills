# Observe · System events and backups

Assess instance system events and data-protection status — "is there planned maintenance" and "is
the data backed up". All read-only.

## ECS system events

```bash
aliyun ecs DescribeInstanceHistoryEvents --RegionId <region> --InstanceId <ecs-id>
```

Read planned reboots, health maintenance, and upcoming instance retirement. An unfinished impacting
event → availability layer `degraded`; report the event type and scheduled time.

## ECS system-disk snapshots

```bash
aliyun ecs DescribeSnapshots --RegionId <region> --InstanceId <ecs-id>
```

Read snapshot count and latest creation time. No snapshot → surface "no system-disk backup" as a
data-protection risk (a recommendation, not scored).

## RDS backups (only with RDS)

```bash
aliyun rds DescribeBackups --RegionId <region> --DBInstanceId <rds-id>
```

Read latest backup-set time and size. No recent backup → surface a data-protection risk.

## Result

Fold into the availability layer: unfinished system events, latest system-disk snapshot and RDS
backup times. Missing backups are recommendations, not scored.
