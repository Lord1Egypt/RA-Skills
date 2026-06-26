# ByteHouse CE (enterprise) SQL templates

These templates are based on the documented Flink SQL connector parameters. `table-name` is the local table on each shard (not the distributed table name).

Parameter notes: `references/bytehouse-ce.md`

## Sink DDL (skeleton)

```sql
CREATE TABLE bh_ce_sink (
  f0 STRING,
  f1 STRING,
  f2 STRING
) WITH (
  'connector' = 'bytehouse-ce',
  'clickhouse.cluster' = '<cluster-name>',
  'clickhouse.shard-discovery.service.host' = '<shard-discovery-host>',
  'username' = '<username>',
  'password' = '<password>',
  'database' = '<database>',
  'table-name' = '<local-table-name>',
  'sink.buffer-flush.interval' = '10 second',
  'sink.buffer-flush.max-rows' = '5000'
);
```

## Example: Datagen -> ByteHouse CE

```sql
CREATE TABLE datagen_src (
  f0 STRING,
  f1 STRING,
  f2 STRING
) WITH (
  'connector' = 'datagen'
);

INSERT INTO bh_ce_sink
SELECT f0, f1, f2 FROM datagen_src;
```
