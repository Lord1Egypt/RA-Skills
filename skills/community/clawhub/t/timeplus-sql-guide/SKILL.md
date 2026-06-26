---
name: timeplus-sql-guide
description: >
  Write and execute Timeplus streaming SQL for real-time analytics. Use this skill
  when the user wants to create streams, run streaming queries, build materialized
  views, ingest data, send data to sinks, write UDFs, or simulate data with random
  streams. Executes SQL via the ClickHouse-compatible HTTP interface on port 8123
  using environment variables TIMEPLUS_HOST, TIMEPLUS_USER, and TIMEPLUS_PASSWORD.
  Covers full Timeplus SQL syntax including window functions, JOINs, CTEs, UDFs,
  data types, aggregations, and all DDL/DML statements.s
compatibility: >
  Requires curl. Set environment variables: TIMEPLUS_HOST (hostname or IP of
  Timeplus server), TIMEPLUS_USER (username, default: 'default'),
  TIMEPLUS_PASSWORD (password). Port 8123 must be accessible. For streaming
  ingest, port 3218 must also be accessible.
metadata:
  author: timeplus-io
  version: "1.1.0"
  docs: https://docs.timeplus.com
  github: https://github.com/timeplus-io/proton
  openclaw:
    requires:
      env:
        - TIMEPLUS_HOST
        - TIMEPLUS_USER
        - TIMEPLUS_PASSWORD
      bins:
        - curl
    primaryEnv: TIMEPLUS_PASSWORD
---

# Timeplus Streaming SQL Guide

You are an expert in **Timeplus** — a high-performance real-time streaming analytics
platform built on a streaming SQL engine (Proton). You write correct, efficient
Timeplus SQL and execute it via the ClickHouse-compatible HTTP API.

## Quick Reference

| Task | Reference |
|------|-----------|
| Get data in | `references/INGESTION.md` |
| Transform data | `references/TRANSFORMATIONS.md` |
| Send data out | `references/SINKS.md` |
| Full SQL syntax, types, functions | `references/SQL_REFERENCE.md` |
| Random streams (simulated data) | `references/RANDOM_STREAMS.md` |
| Python & JavaScript UDFs | `references/UDFS.md` |
| Python Table Functions | `references/Python_TABLE_FUNCTION.md` |
| EMIT clauses & UDAF emit control | `references/EMIT_AND_UDAF.md` |

---

## Executing SQL

### Environment Setup

Always use these environment variables — never hardcode credentials:

```
- TIMEPLUS_HOST       # hostname or IP
- TIMEPLUS_USER       # username
- TIMEPLUS_PASSWORD   # password (can be empty)
```

### Running SQL via curl (port 8123)

Port 8123 is the ClickHouse-compatible HTTP interface. Use it for **all DDL and
historical queries** (CREATE, DROP, INSERT, SELECT from `table(...)`). 
Always use username password with -u option

NOTE, if the curl returns nothing, it is not an error, it means the query returns no records. You can check the HTTP status code to confirm success (200 OK) or failure (4xx/5xx).

```bash
# Standard pattern — pipe SQL into curl
echo "YOUR SQL HERE" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**Health check:**
```bash
curl "http://${TIMEPLUS_HOST}:8123/"
# Returns: Ok.
```

**DDL example — create a stream:**
```bash
echo "CREATE STREAM IF NOT EXISTS sensor_data (
  device_id string,
  temperature float32,
  ts datetime64(3, 'UTC') DEFAULT now64(3, 'UTC')
) SETTINGS logstore_retention_ms=86400000" | \
curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**Historical query with JSON output:**
```bash
echo "SELECT * FROM table(sensor_data) LIMIT 10" | \
curl "http://${TIMEPLUS_HOST}:8123/?default_format=JSONEachRow" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**Insert data:**
```bash
echo "INSERT INTO sensor_data (device_id, temperature) VALUES ('dev-1', 23.5), ('dev-2', 18.2)" | \
curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

### Streaming Ingest via REST API (port 3218)

For pushing event batches into a stream:

```bash
curl -s -X POST "http://${TIMEPLUS_HOST}:3218/proton/v1/ingest/streams/sensor_data" \
  -H "Content-Type: application/json" \
  -d '{
    "columns": ["device_id", "temperature"],
    "data": [
      ["dev-1", 23.5],
      ["dev-2", 18.2],
      ["dev-3", 31.0]
    ]
  }'
```

### Output Formats

Append `?default_format=<format>` to the URL:

| Format | Use Case |
|--------|----------|
| `TabSeparated` | Default, human-readable |
| `JSONEachRow` | One JSON object per line |
| `JSONCompact` | Compact JSON array |
| `CSV` | Comma-separated |
| `Vertical` | Column-per-line, for inspection |

---

## Core Concepts

### Streaming vs Historical Queries

```sql
-- STREAMING: Continuous, never ends. Default behavior.
SELECT device_id, temperature FROM sensor_data;

-- HISTORICAL: Bounded, returns immediately. Use table().
SELECT device_id, temperature FROM table(sensor_data) LIMIT 100;

-- HISTORICAL + FUTURE: All past events + all future events
SELECT * FROM sensor_data WHERE _tp_time >= earliest_timestamp();
```

### ORDER BY and LIMIT on Streaming Queries

A streaming query result is **unbounded** — new rows arrive forever — so the
familiar `ORDER BY` / `LIMIT` semantics from batch SQL do not apply directly:

- **`ORDER BY` is not allowed on a non-windowed streaming query.** Sorting
  requires a finite input. You can only use `ORDER BY` when the upstream is
  bounded: a `table(...)` historical query, or a windowed aggregation
  (`tumble`/`hop`/`session`) where each window closure produces a finite batch
  that gets sorted per window.
- **`LIMIT n` on a streaming query terminates the query after `n` rows.** It is
  not "top n by some order" — it is a hard stop. Pair `LIMIT` with a window
  (`LIMIT n BY window_start`) or use streaming-native top-k aggregates
  (`top_k`, `min_k`, `max_k`) for per-window ranking.
- For historical queries (`SELECT ... FROM table(stream)`), `ORDER BY` and
  `LIMIT` work the normal way.

See `references/TRANSFORMATIONS.md` → **Top-N per Window** for the recommended
patterns.

### The `_tp_time` Column

Every stream has a built-in `_tp_time datetime64(3, 'UTC')` event-time column.
It defaults to ingestion time. You can set a custom event-time column via
`SETTINGS event_time_column='your_column'` when creating the stream.

### Stream Modes

| Mode | Created With | Behavior |
|------|-------------|----------|
| `append` | `CREATE STREAM` (default) | Immutable log, new rows only |
| `versioned_kv` | `+ SETTINGS mode='versioned_kv'` | Latest value per primary key |
| `changelog_kv` | `+ SETTINGS mode='changelog_kv'` | Insert/Update/Delete tracking |
| `mutable` | `CREATE MUTABLE STREAM` | Row-level UPDATE/DELETE (Enterprise) |

---

## Common Patterns

### Pattern 1: Create stream → insert → query
```bash
# 1. Create stream
echo "CREATE STREAM IF NOT EXISTS orders (
  order_id string,
  product string,
  amount float32,
  region string
)" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-

# 2. Insert data
echo "INSERT INTO orders VALUES ('o-1','Widget',19.99,'US'), ('o-2','Gadget',49.99,'EU')" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-

# 3. Query historical data
echo "SELECT region, sum(amount) FROM table(orders) GROUP BY region" | \
  curl "http://${TIMEPLUS_HOST}:8123/?default_format=JSONEachRow" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

### Pattern 2: Window aggregation (streaming)
```bash
echo "SELECT window_start, region, sum(amount) AS revenue
FROM tumble(orders, 1m)
GROUP BY window_start, region
EMIT AFTER WATERMARK AND DELAY 5s" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

### Pattern 3: Materialized view pipeline
```bash
echo "CREATE MATERIALIZED VIEW IF NOT EXISTS mv_revenue_by_region
INTO revenue_by_region AS
SELECT window_start, region, sum(amount) AS total
FROM tumble(orders, 5m)
GROUP BY window_start, region" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

### Pattern 4: Random stream for testing
```bash
echo "CREATE RANDOM STREAM IF NOT EXISTS mock_sensors (
  device_id string DEFAULT 'device-' || to_string(rand() % 10),
  temperature float32 DEFAULT 20 + (rand() % 30),
  status string DEFAULT ['ok','warn','error'][rand() % 3 + 1]
) SETTINGS eps=5" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

---

## Error Handling

Common errors and fixes:

| Error | Cause | Fix |
|-------|-------|-----|
| `Connection refused` | Wrong host/port | Check `TIMEPLUS_HOST` and port 8123 is open |
| `Authentication failed` | Wrong credentials | Check `TIMEPLUS_USER` / `TIMEPLUS_PASSWORD` |
| `Stream already exists` | Duplicate CREATE | Use `CREATE STREAM IF NOT EXISTS` |
| `Unknown column` | Typo or wrong stream | Run `DESCRIBE stream_name` to check schema |
| `Streaming query timeout` | Using streaming on port 8123 | Wrap with `table()` for historical query |
| `Type mismatch` | Wrong data type | Use explicit cast: `cast(val, 'float32')` |
| `Watermark with delay is only supported with streaming window function` | `EMIT ... WITH DELAY` on a plain `GROUP BY` | Drop the EMIT clause (plain GROUP BY already emits on update), or wrap the source in `tumble()`/`hop()`/`session()` |

**Inspect a stream:**
```bash
echo "DESCRIBE sensor_data" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**List all streams:**
```bash
echo "SHOW STREAMS" | curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

**Explain a query:**
```bash
echo "EXPLAIN SELECT * FROM tumble(sensor_data, 1m) GROUP BY window_start" | \
  curl "http://${TIMEPLUS_HOST}:8123/" \
  -u "${TIMEPLUS_USER}:${TIMEPLUS_PASSWORD}" \
  --data-binary @-
```

---

## When to Read Reference Files

Load the relevant reference file when the user's request requires deeper knowledge:

- Creating or modifying **streams, external streams, sources** → `references/INGESTION.md`
- **Window functions, JOINs, CTEs, materialized views, aggregations** → `references/TRANSFORMATIONS.md`
- **Sinks, external tables, Kafka output, webhooks** → `references/SINKS.md`
- **Data types, full function catalog, query settings, all DDL** → `references/SQL_REFERENCE.md`
- **Simulating data, random streams, test data generation** → `references/RANDOM_STREAMS.md`
- **Writing Python UDFs, JavaScript UDFs, remote UDFs, SQL lambdas** → `references/UDFS.md`
- **Python Table Functions** → `references/Python_TABLE_FUNCTION.md`
- **EMIT clause vocabulary, `EMIT AFTER SESSION CLOSE` / `KEY EXPIRE`, event-terminated session windows, UDAF `has_customized_emit`, `MAXSPAN`/`TIMEOUT` constraints** → `references/EMIT_AND_UDAF.md`
- **Scheduled Tasks** → `references/TASK.md`
- **Alerts** → `references/ALERT.md`

