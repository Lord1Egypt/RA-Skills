# Scheduled Tasks in Timeplus

Scheduled Tasks allow you to run historical SQL queries (bounded) on a recurring interval. This is primarily used for periodic reporting, data rollups, or snapshots.

## Key Concept
A **Scheduled Task** executes a `SELECT ... FROM table(stream_name)` query at a set frequency. It does not run continuously like a Materialized View.

## Creating a Task
Tasks are created using the `EVERY` keyword to define the interval.

### Syntax
```sql
CREATE OR REPLACE TASK <task_name>
SCHEDULE <interval> -- e.g., 1h, 30m, 1d
TIMEOUT <interval> -- e.g., 30s
INTO <target_stream_or_external_table>
AS
  <Historical SELECT query>;
```

### Examples

#### 1. Hourly Rollup
Calculate the average metric every hour and save it to a summary stream.
```sql
CREATE TASK hourly_sensor_summary
SCHEDULE 1h
TIMEOUT 30s
AS 
SELECT 
    to_start_of_hour(now()) as log_time,
    device_id, 
    avg(temperature) as avg_temp 
FROM table(sensor_data) 
WHERE _tp_time >= now() - 1h
INTO summary_stream;
```

#### 2. Daily Snapshot
Count unique users from the previous day and send to an external table.
```sql
CREATE TASK daily_user_count
SCHEDULE 1d
TIMEOUT 30s
AS 
SELECT 
    yesterday() as report_date,
    count(distinct user_id) as active_users
FROM table(user_logins)
WHERE to_date(_tp_time) = yesterday()
INTO clickhouse_external_table;
```

## Task Management

| Action | SQL Command |
| --- | --- |
| **List Tasks** | `SHOW TASKS` |
| **Check Definition** | `SHOW CREATE TASK task_name` |
| **Delete Task** | `DROP TASK task_name` |
| **Pause Task** | `SYSTEM PAUSE TASK task_name` |
| **Resume Task** | `SYSTEM RESUME TASK task_name` |

## Notes
- **Intervals:** Supported units include `s` (seconds), `m` (minutes), `h` (hours), and `d` (days).
- **Historical Context:** Ensure your query uses `table(stream_name)` and appropriate `WHERE` clauses to bound the data processed in each run.
