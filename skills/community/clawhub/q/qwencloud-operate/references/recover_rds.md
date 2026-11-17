# Recover: RDS-related Handling

Identify the RDS-side condition, then act at the safe layer. Keep the same metric definitions as
`qwencloud-observe`.

## Identify

- RDS not running
- Connection timeout / auth failure / connection refused
- Connections too high
- Slow SQL / row-lock waits

Use read-only `DescribeDBInstances`, `DescribeDBInstancePerformance`, `DescribeSlowLogRecords`.

## Safe action

- **Connection-pool exhaustion driven by the app** → prefer restarting the app service
  (`recover_app.md`) to rebuild connections, then verify RDS connections recover.
- **RDS not running / instance-level issues / high connections not caused by the app / slow SQL /
  lock waits** → do **not** mutate the RDS instance. Output the evidence and the recommended next
  step (e.g. optimize slow SQL, raise connection cap in the console, or scale) and stop.

## Output

RDS evidence with the same metric definitions as observe, plus the recommended next step. Any
write goes through the app-service path (`recover_app.md`) with its confirmation gate; verify RDS
connection recovery afterward (`workflow.md`).
