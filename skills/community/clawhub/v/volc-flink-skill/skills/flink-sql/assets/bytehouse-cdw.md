# ByteHouse CDW (cloud data warehouse) SQL templates

These templates mirror the "Gateway connection" parameter set used in the official docs for the Flink SQL connector driver.

Parameter notes: `references/bytehouse-cdw.md`

## Sink DDL

```sql
CREATE TABLE bh_cdw_sink (
  id STRING NOT NULL,
  event_time STRING,
  content ARRAY<DECIMAL(20, 0)>,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'bytehouse-cdw',
  'jdbc.enable-gateway-connection' = 'true',
  'bytehouse.gateway.region' = 'VOLCANO_PRIVATE',
  'bytehouse.gateway.host' = 'tenant-<tenant-id>-<region>.bytehouse.ivolces.com',
  'bytehouse.gateway.port' = '19000',
  'bytehouse.gateway.api-token' = '<api-token>',
  'bytehouse.gateway.virtual-warehouse' = '<virtual-warehouse-id>',
  'database' = '<database>',
  'table-name' = '<table-name>'
);
```

## Example: Datagen -> ByteHouse CDW

```sql
CREATE TABLE bh_de_source (
  id BIGINT NOT NULL,
  time TIMESTAMP(0),
  content ARRAY<DECIMAL(20, 0)>
) WITH (
  'connector' = 'datagen'
);

INSERT INTO bh_cdw_sink (id, event_time, content)
SELECT
  CAST(id AS STRING),
  CAST(time AS STRING),
  content
FROM bh_de_source;
```
