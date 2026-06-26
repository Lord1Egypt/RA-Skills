# MySQL source notes

## Version and dependency

- MySQL CDC support requires Flink 1.16-volcano or above on the platform
- For this repo/CLI workflow, CDC drafts are constrained to `FLINK_VERSION_1_16`
- Due to compliance requirements, users need to upload the MySQL JDBC driver themselves
- Recommended driver version: `8.0.27`

## Required options

- `hostname`
- `port`
- `username`
- `password`
- `tables`
- `server-id`

## Common options

- `tables.exclude`: excludes after `tables`
- `schema-change.enabled`: whether to emit schema change events, default `true`
- `scan.incremental.snapshot.chunk.size`: chunk size for snapshot split
- `scan.snapshot.fetch.size`: max rows fetched each time during snapshot
- `scan.startup.mode`: `initial`, `earliest-offset`, `latest-offset`, `specific-offset`, `timestamp`, `snapshot`
- `connect.timeout`
- `connect.max-retries`
- `connection.pool.size`
- `jdbc.properties.*`
- `heartbeat.interval`
- `debezium.*`

## Tables regex note

`tables` supports regex. Dot (`.`) is treated as the database/table separator, so when you want regex-dot semantics, escape it.

Examples:

- `app_db\\.orders_.*`
- `db0\\.\\*`
- `db1\\.user_table_[0-9]+`

## Server ID note

- `server-id` can be an integer or a range
- For incremental snapshot mode, prefer a range such as `5401-5404`
- The server id must be unique in the MySQL cluster

