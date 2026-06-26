# Paimon SQL templates

These templates focus on common table patterns and the "catalog + database + table" workflow. Replace placeholders like `<region>`, `<tos-bucket>`, `<las-catalog>`, and credentials.

Parameter notes: `references/paimon.md`

## Catalog (FileSystem)

```sql
CREATE CATALOG paimon_catalog WITH (
  'type' = 'paimon',
  'warehouse' = 'tos://<tos-bucket>/paimon/warehouse'
);

USE CATALOG paimon_catalog;
```

## Catalog (LAS / Hive metastore)

```sql
CREATE CATALOG paimon_las_catalog WITH (
  'type' = 'paimon',
  'metastore' = 'hive',
  'is-las' = 'true',
  'hive.client.las.region.name' = '<region>',
  'hive.metastore.uris' = 'thrift://lakeformation.las.<region>.ivolces.com:48869',
  'hive.hms.client.is.public.cloud' = 'true',
  'hive.client.las.ak' = '<ak>',
  'hive.client.las.sk' = '<sk>',
  'catalog.properties.metastore.catalog.default' = '<las-catalog>',
  'warehouse' = 'tos://<tos-bucket>/paimon/warehouse'
);

USE CATALOG paimon_las_catalog;
```

## Database

```sql
CREATE DATABASE IF NOT EXISTS test_db;
USE test_db;
```

## Append table (no primary key)

```sql
CREATE TABLE IF NOT EXISTS append_table (
  id BIGINT,
  name STRING,
  amount DECIMAL(10, 2),
  event_time TIMESTAMP(3),
  dt STRING
) PARTITIONED BY (dt)
WITH (
  'changelog-producer' = 'none'
);
```

## Primary key table (non-partitioned)

```sql
CREATE TABLE IF NOT EXISTS primary_key_table (
  word STRING,
  cnt BIGINT,
  PRIMARY KEY (word) NOT ENFORCED
) WITH (
  'bucket' = '4',
  'changelog-producer' = 'input'
);
```

## Primary key table (partitioned)

```sql
CREATE TABLE IF NOT EXISTS primary_key_partitioned (
  word STRING,
  cnt BIGINT,
  dt STRING,
  hh STRING,
  PRIMARY KEY (dt, hh, word) NOT ENFORCED
) PARTITIONED BY (dt, hh)
WITH (
  'bucket' = '4',
  'changelog-producer' = 'none',
  'metastore.partitioned-table' = 'true'
);
```

## Partial update table (wide table pattern)

```sql
CREATE TABLE IF NOT EXISTS partial_update_table (
  uid INT,
  username STRING,
  reg_time TIMESTAMP(3),
  logintypes ARRAY<ROW<logintype STRING, bind_time TIMESTAMP(3)>>,
  last_bind_time TIMESTAMP(3),
  vip_is_valid BOOLEAN,
  vip_start_time TIMESTAMP(3),
  vip_end_time TIMESTAMP(3),
  PRIMARY KEY (uid) NOT ENFORCED
) WITH (
  'bucket' = '4',
  'merge-engine' = 'partial-update',
  'changelog-producer' = 'lookup',
  'fields.last_bind_time.sequence-group' = 'logintypes',
  'fields.logintypes.aggregate-function' = 'nested_update',
  'fields.logintypes.nested-key' = 'logintype'
);
```

## Aggregate table

```sql
CREATE TABLE IF NOT EXISTS aggregate_table (
  window_start TIMESTAMP(3),
  window_end TIMESTAMP(3),
  category STRING,
  item_id BIGINT,
  total_amount DECIMAL(10, 2),
  cnt BIGINT,
  dt STRING,
  PRIMARY KEY (window_start, window_end, category, item_id, dt) NOT ENFORCED
) PARTITIONED BY (dt)
WITH (
  'bucket' = '4',
  'changelog-producer' = 'lookup',
  'merge-engine' = 'aggregation',
  'fields.total_amount.aggregate-function' = 'sum',
  'fields.cnt.aggregate-function' = 'sum',
  'fields.total_amount.ignore-retract' = 'true',
  'fields.cnt.ignore-retract' = 'true'
);
```

## Read Paimon table -> Print

```sql
CREATE TABLE print_result (
  word STRING,
  cnt BIGINT
) WITH (
  'connector' = 'print'
);

INSERT INTO print_result
SELECT * FROM primary_key_table;
```

## Example: Kafka -> Paimon (append, partitioned by dt)

```sql
CREATE TABLE kafka_source (
  id BIGINT,
  name STRING,
  amount DECIMAL(10, 2),
  event_time TIMESTAMP(3)
) WITH (
  'connector' = 'kafka',
  'topic' = '<topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json',
  'json.fail-on-missing-field' = 'false',
  'json.ignore-parse-errors' = 'true'
);

CREATE TABLE IF NOT EXISTS paimon_append_sink (
  id BIGINT,
  name STRING,
  amount DECIMAL(10, 2),
  event_time TIMESTAMP(3),
  dt STRING
) PARTITIONED BY (dt)
WITH (
  'bucket' = '4',
  'changelog-producer' = 'none'
);

INSERT INTO paimon_append_sink
SELECT
  id,
  name,
  amount,
  event_time,
  DATE_FORMAT(event_time, 'yyyy-MM-dd') AS dt
FROM kafka_source;
```
