# CREATE SINK: Iceberg
Connecting Materialize to an Apache Iceberg table
> **Public Preview:** This feature is in public preview.

Use `CREATE SINK ... INTO ICEBERG CATALOG...` to create Iceberg sinks. Iceberg sinks write data from Materialize into an Iceberg table hosted on
AWS S3 Tables. As data changes in Materialize, your Iceberg tables are
automatically kept up to date.

To create an Iceberg sink, you need:

- An [AWS connection](/sql/create-connection/#aws) for authentication with
  object storage.
- An [Iceberg catalog connection](/sql/create-connection/#iceberg-catalog) to
  specify access parameters to your Iceberg catalog.

## Syntax

**MODE UPSERT:**

```mzsql
CREATE SINK [IF NOT EXISTS] <sink_name>
[IN CLUSTER <cluster_name>]
FROM <item_name>
INTO ICEBERG CATALOG CONNECTION <catalog_connection> (
  NAMESPACE = '<namespace>',
  TABLE = '<table>'
)
USING AWS CONNECTION <aws_connection>
KEY ( <key_col> [, ...] ) [NOT ENFORCED]
MODE UPSERT
WITH (COMMIT INTERVAL = '<interval>')

```

| Syntax element | Description |
| --- | --- |
| `<sink_name>` | The name for the sink.  |
| **IF NOT EXISTS** | Optional. If specified, do not throw an error if a sink with the same name already exists.  |
| **IN CLUSTER** `<cluster_name>` | Optional. The [cluster](/sql/create-cluster) to maintain this sink. If unspecified, defaults to the active cluster.  |
| `<item_name>` | The name of the source, table, or materialized view to sink.  |
| **ICEBERG CATALOG CONNECTION** `<catalog_connection>` | The name of the [Iceberg catalog connection](/sql/create-connection/#iceberg-catalog) to use.  |
| **NAMESPACE** `'<namespace>'` | The Iceberg namespace (database) containing the table.  |
| **TABLE** `'<table>'` | The name of the unpartitioned Iceberg table to write to. If the table doesn't exist, Materialize creates it automatically. For details, see [Iceberg table creation](/sql/create-sink/iceberg/#iceberg-table-creation).  |
| **USING AWS CONNECTION** `<aws_connection>` | The [AWS connection](/sql/create-connection/#aws) for object storage access.  |
| **KEY** ( `<key_col>` [, ...] ) | The columns that uniquely identify rows. Materialize validates that the key is unique unless `NOT ENFORCED` is specified.  |
| **NOT ENFORCED** | Optional. Disable validation of key uniqueness. Use only when you have outside knowledge that the key is unique.  |
| **MODE UPSERT** | Indicates that the sink uses upsert semantics based on the `KEY`.  |
| **COMMIT INTERVAL** `'<interval>'` | How frequently to commit snapshots to Iceberg (e.g., `'60s'`, `'5m'`). See [Commit interval tradeoffs](#commit-interval-tradeoffs).  |

**MODE APPEND:**

```mzsql
CREATE SINK [IF NOT EXISTS] <sink_name>
[IN CLUSTER <cluster_name>]
FROM <item_name>
INTO ICEBERG CATALOG CONNECTION <catalog_connection> (
  NAMESPACE = '<namespace>',
  TABLE = '<table>'
)
USING AWS CONNECTION <aws_connection>
MODE APPEND
WITH (COMMIT INTERVAL = '<interval>')

```

| Syntax element | Description |
| --- | --- |
| `<sink_name>` | The name for the sink.  |
| **IF NOT EXISTS** | Optional. If specified, do not throw an error if a sink with the same name already exists.  |
| **IN CLUSTER** `<cluster_name>` | Optional. The [cluster](/sql/create-cluster) to maintain this sink. If unspecified, defaults to the active cluster.  |
| `<item_name>` | The name of the source, table, or materialized view to sink.  |
| **ICEBERG CATALOG CONNECTION** `<catalog_connection>` | The name of the [Iceberg catalog connection](/sql/create-connection/#iceberg-catalog) to use.  |
| **NAMESPACE** `'<namespace>'` | The Iceberg namespace (database) containing the table.  |
| **TABLE** `'<table>'` | The name of the unpartitioned Iceberg table to write to. If the table doesn't exist, Materialize creates it automatically. For details, see [Iceberg table creation](/sql/create-sink/iceberg/#iceberg-table-creation).  |
| **USING AWS CONNECTION** `<aws_connection>` | The [AWS connection](/sql/create-connection/#aws) for object storage access.  |
| **MODE APPEND** | Writes all changes as data rows instead of using Iceberg delete files. Two extra columns are appended to the Iceberg table: `_mz_diff` (`int`, `+1` for inserts, `-1` for deletes) and `_mz_timestamp` (`long`). An update produces two rows: one with `_mz_diff = -1` (old values) and one with `_mz_diff = +1` (new values). No `KEY` clause is permitted. See [Append mode](#append-mode).  |
| **COMMIT INTERVAL** `'<interval>'` | How frequently to commit snapshots to Iceberg (e.g., `'60s'`, `'5m'`). See [Commit interval tradeoffs](#commit-interval-tradeoffs).  |

## Details

Iceberg sinks continuously stream changes from Materialize to an Iceberg table.
Specifically, Materialize writes data as Parquet files to the object storage
backing your Iceberg catalog.

At each `COMMIT INTERVAL`:

1. All pending writes are flushed to Parquet data files. See [Type
   mapping](#type-mapping).
2. In **upsert** mode, delete files are written for any updates or deletes. See
   [Delete handling](#delete-handling). In **append** mode, no delete files are
   written; all changes are data rows. See [Append mode](#append-mode).
3. A new Iceberg snapshot is committed atomically.

When the snapshot is committed, the data is available to downstream query
engines. See [Commit interval tradeoffs](#commit-interval-tradeoffs).

### Iceberg table creation

If the specified Iceberg table does not exist, Materialize creates the table.
The new Iceberg table:
- Uses the schema derived from your Materialize object.
- Uses Iceberg format version 2.

Materialize creates unpartitioned tables. Partitioned tables are not supported.

See also: [Restrictions and limitations](#restrictions-and-limitations).

### Exactly-once delivery

<p>Iceberg sinks provide <strong>exactly-once delivery</strong>. After a restart,
Materialize resumes from the last committed snapshot without duplicating
data.</p>
<p>Materialize stores progress information in Iceberg snapshot metadata
properties (<code>mz-frontier</code> and <code>mz-sink-version</code>).</p>

### Commit interval tradeoffs

The `COMMIT INTERVAL` setting involves tradeoffs between latency and efficiency:

| Shorter intervals (e.g., < `60s`) | Longer intervals (e.g., `5m`) |
|---------------------------------|-------------------------------|
| Lower latency - data visible sooner | Higher latency - data takes longer to appear |
| More small files - can degrade query performance | Fewer, larger files - better query performance |
| Higher catalog overhead | Lower catalog overhead |
| Higher S3 write costs (more PUT requests) | Lower S3 write costs |

**Recommendations:**
- For production: `60s` to `5m`
- For batch analytics: `5m` to `15m`

> **Note:** Outside of development environments, commit intervals should be at least `60s`.
> Short commit intervals increase catalog overhead and produce many small files.
> Small files will result in degraded query performance. It also increases load on
> the Iceberg metadata, which can result in a degraded catalog and non-responsive
> queries.

### Unique keys

In upsert mode, the Iceberg sink uses upsert semantics based on the `KEY`. The columns you
specify as the `KEY` must uniquely identify rows. Materialize validates that the
key is unique; if it cannot prove uniqueness, you'll receive an error.

If you have outside knowledge that the key is unique, you can bypass validation
using `NOT ENFORCED`. However, if the key is not actually unique, downstream
consumers may see incorrect results.

### Append mode

In append mode (`MODE APPEND`), every change in the Materialize update stream
is written as a data row. No Iceberg delete files are produced. Two extra
columns are appended to the Iceberg table:

| Column | Iceberg type | Description |
|--------|-------------|-------------|
| `_mz_diff` | `int` | `+1` for insertions, `-1` for deletions. |
| `_mz_timestamp` | `long` | The Materialize logical timestamp of the change. |

- An **insert** produces one row with `_mz_diff = +1`.
- A **delete** produces one row with `_mz_diff = -1`.
- An **update** produces two rows: one with `_mz_diff = -1` (the old value) and
  one with `_mz_diff = +1` (the new value). Both carry the same `_mz_timestamp`.

No `KEY` clause is permitted with `MODE APPEND`.

### Type mapping

Materialize converts SQL types to Iceberg/Parquet types:

| SQL type | Iceberg type |
|----------|--------------|
| `boolean` | `boolean` |
| `smallint`, `integer` | `int` |
| `uint2` | `int` |
| `bigint` | `long` |
| `uint4` | `long` |
| `uint8` | `decimal(20, 0)` |
| `real` | `float` |
| `double precision` | `double` |
| `numeric` | `decimal(38, scale)` |
| `date` | `date` |
| `time` | `time` (microsecond) |
| `timestamp` | `timestamp` (microsecond) |
| `timestamptz` | `timestamptz` (microsecond) |
| `text`, `varchar` | `string` |
| `bytea` | `binary` |
| `uuid` | `fixed(16)` |
| `jsonb` | `string` |
| `interval` | `string` |
| `int4range`, `int8range`, `numrange`, `daterange`, `tsrange`, `tstzrange` | `struct` (fields: `lower`, `upper`, `lower_inclusive`, `upper_inclusive`, `empty`) |
| `record` | `struct` |
| `list` | `list` |
| `map` | `map` |

### Restrictions and limitations

- Your S3 Tables bucket must be in the same AWS region as your Materialize
deployment.

- Partitioned tables are not supported.

- Schema evolution of an Iceberg table is not supported. If the <code>SINK FROM</code> object&rsquo;s schema changes, you must drop and recreate the sink.

### Delete handling

> **Note:** Delete handling applies to `MODE UPSERT` only. In `MODE APPEND`, all changes
> are written as data rows. See [Append mode](#append-mode).

Iceberg sinks use a hybrid delete strategy:

- **Position deletes**: Used when a row is inserted and then deleted or updated
  within the same commit interval. Materialize records the exact file path and
  row position.
- **Equality deletes**: Used when deleting or updating a row from a previous
  snapshot. Materialize writes a delete file containing the `KEY` column values.

This means short-lived rows use efficient position deletes, while updates to
older data use equality deletes.

> **Tip:** Consider running [Iceberg compaction](https://iceberg.apache.org/docs/latest/maintenance/#compacting-data-files) periodically to merge delete files and improve query performance.

## Required privileges

- `CREATE` privileges on the containing schema.
- `SELECT` privileges on the item being written out to an external system.
  - NOTE: if the item is a materialized view, then the view owner must also have the necessary privileges to
    execute the view definition.
- `CREATE` privileges on the containing cluster if the sink is created in an existing cluster.
- `CREATECLUSTER` privileges on the system if the sink is not created in an existing cluster.
- `USAGE` privileges on all connections and secrets used in the sink definition.
- `USAGE` privileges on the schemas that all connections and secrets in the
  statement are contained in.

## Troubleshooting

### Sink creation fails with "input compacted past resume upper"

This error occurs when the source data has been compacted beyond the point where
the sink last committed. This can happen after a Materialize backup/restore
operation. You may need to drop and recreate the sink, which will re-snapshot
the entire source relation.

### Commit conflicts

If another process modifies the Iceberg table while Materialize is committing,
you may see commit conflict errors. Materialize will automatically retry, but
if conflicts persist, ensure no other writers are modifying the same table.

## Examples

### Prerequisites: Create connections

To create an Iceberg sink, you need an AWS connection and an Iceberg catalog
connection.

The following example creates an AWS connection and an Iceberg catalog connection:
```mzsql
-- First, create an AWS connection for authentication
CREATE CONNECTION aws_connection
  TO AWS (ASSUME ROLE ARN = 'arn:aws:iam::123456789012:role/MaterializeIceberg');

-- Create the Iceberg catalog connection pointing to S3 Tables
CREATE CONNECTION iceberg_catalog_connection TO ICEBERG CATALOG (
    CATALOG TYPE = 's3tablesrest',
    URL = 'https://s3tables.us-east-1.amazonaws.com/iceberg',
    WAREHOUSE = 'arn:aws:s3tables:us-east-1:123456789012:bucket/my-table-bucket',
    AWS CONNECTION = aws_connection
);

```

### Creating an upsert sink

Using the previously created AWS and Iceberg catalog connection, the
following example creates an Iceberg sink with a composite key:
```mzsql
CREATE SINK user_events_iceberg
  IN CLUSTER analytics_cluster
  FROM user_events
  INTO ICEBERG CATALOG CONNECTION iceberg_catalog_connection (
    NAMESPACE = 'events',
    TABLE = 'user_events'
  )
  USING AWS CONNECTION aws_connection
  KEY (user_id, event_timestamp)
  MODE UPSERT
  WITH (COMMIT INTERVAL = '1m');

```

In upsert mode, the required `KEY` clause uniquely identifies rows; in this
example, it uses a composite key of `user_id` and `event_timestamp`.
Materialize validates that this key is unique in the source data.

### Bypassing unique key validation

If Materialize cannot prove your key is unique but you have outside knowledge
that it is, you can bypass validation by including `NOT ENFORCED` option:

```mzsql
CREATE SINK deduped_sink
  IN CLUSTER my_cluster
  FROM my_source
  INTO ICEBERG CATALOG CONNECTION iceberg_catalog_connection (
    NAMESPACE = 'raw',
    TABLE = 'events'
  )
  USING AWS CONNECTION aws_connection
  KEY (event_id) NOT ENFORCED
  MODE UPSERT
  WITH (COMMIT INTERVAL = '1m');
```

> **Warning:** If the key is not actually unique, downstream consumers may see incorrect
> results.

### Creating an append sink

Create an Iceberg sink in append mode. All changes are written as data
rows with `_mz_diff` and `_mz_timestamp` columns:
```mzsql
CREATE SINK events_log_iceberg
  IN CLUSTER analytics_cluster
  FROM user_events
  INTO ICEBERG CATALOG CONNECTION iceberg_catalog_connection (
    NAMESPACE = 'events',
    TABLE = 'user_events_log'
  )
  USING AWS CONNECTION aws_connection
  MODE APPEND
  WITH (COMMIT INTERVAL = '1m');

```

The Iceberg table will contain all columns from `user_events` plus two
additional columns: `_mz_diff` and `_mz_timestamp`. See [Append
mode](#append-mode).

## Related pages

- [Iceberg sink guide](/serve-results/sink/iceberg/)
- [`SHOW SINKS`](/sql/show-sinks)
- [`DROP SINK`](/sql/drop-sink)
- [`CREATE CONNECTION`](/sql/create-connection)
