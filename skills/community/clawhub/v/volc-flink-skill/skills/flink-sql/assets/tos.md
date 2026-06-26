# TOS (filesystem connector) SQL templates

This uses Flink's `filesystem` connector with a `tos://` path.

Parameter notes: `references/tos.md`

## Source: read from TOS

```sql
CREATE TABLE tos_filesystem_source (
  name STRING,
  score INT
) WITH (
  'connector' = 'filesystem',
  'path' = 'tos://<bucket>/<path>/',
  'format' = 'json'
);
```

## Sink: write to TOS (with rolling policy)

Rolling policy controls when files become visible/closed. In practice, it's best paired with checkpoint enabled at job level.

```sql
CREATE TABLE tos_filesystem_sink (
  name STRING,
  score INT
) WITH (
  'connector' = 'filesystem',
  'path' = 'tos://<bucket>/<path>/',
  'sink.rolling-policy.file-size' = '1M',
  'sink.rolling-policy.rollover-interval' = '10 min',
  'sink.rolling-policy.check-interval' = '1 min',
  'format' = 'json'
);
```

## Example: Kafka -> TOS (partitioned)

```sql
CREATE TABLE kafka_source (
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING,
  event_time TIMESTAMP(3)
) WITH (
  'connector' = 'kafka',
  'topic' = '<topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json'
);

CREATE TABLE tos_sink (
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING,
  event_time TIMESTAMP(3),
  dt STRING
) PARTITIONED BY (dt)
WITH (
  'connector' = 'filesystem',
  'path' = 'tos://<bucket>/<path>/',
  'sink.rolling-policy.file-size' = '128MB',
  'sink.rolling-policy.rollover-interval' = '30 min',
  'format' = 'json'
);

INSERT INTO tos_sink
SELECT
  user_id,
  item_id,
  behavior,
  event_time,
  DATE_FORMAT(event_time, 'yyyy-MM-dd') AS dt
FROM kafka_source;
```
