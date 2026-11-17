# Observe RDS

Only when the state file has a non-null `outputs.db_instance_id`. Skip cleanly otherwise.

## Status + spec

```bash
aliyun rds DescribeDBInstances --RegionId <region> --DBInstanceId <rds-id>
aliyun rds DescribeDBInstanceAttribute --RegionId <region> --DBInstanceId <rds-id>
```

Read instance status, class/spec, and storage capacity. A non-running instance → `unavailable`.

## Performance

```bash
aliyun rds DescribeDBInstancePerformance --RegionId <region> --DBInstanceId <rds-id> \
  --Key MySQL_ThreadStatus,MySQL_QPSTPS,MySQL_IOPS,MySQL_MemCpuUsage,MySQL_Space,MySQL_RowLockCurrentWaits \
  --StartTime <start> --EndTime <end>
```

Cover CPU/memory, connections, QPS/TPS, IOPS, space usage, and row-lock waits. Flag:

- connections near the instance limit → `degraded`
- high row-lock waits → `degraded`
- space near full → `degraded`

Reference: https://help.aliyun.com/en/rds/developer-reference/performance-parameters

## Slow SQL (redacted)

```bash
aliyun rds DescribeSlowLogRecords --RegionId <region> --DBInstanceId <rds-id> \
  --StartTime <start> --EndTime <end> --PageSize 30
```

Output SQL **templates** (or redacted SQL), execution time, and impact. Never show literal
parameter values; length-limit each entry.

Reference: https://help.aliyun.com/zh/rds/developer-reference/api-rds-2014-08-15-describeslowlogrecords

## Correlate with application logs

Tie RDS findings to the application-log signals: database timeout, auth failure, connection
refused, connection-pool waits.

## Result

RDS-layer state with evidence: status, connections trend, QPS/TPS, space, row-lock waits, and the
top redacted slow-SQL templates.
