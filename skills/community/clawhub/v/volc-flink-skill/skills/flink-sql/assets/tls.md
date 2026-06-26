# TLS (Log Service) via Kafka protocol SQL templates

TLS can be consumed/written via Kafka protocol. These templates focus on the required Kafka security settings and TLS-specific topic conventions.

Parameter notes: `references/tls.md`

## Source: consume from TLS

Notes:
1. Consumer `topic` must be `out-<tls-topic-id>`.
2. Consumer port is typically `9093`.
3. Auth uses `SASL_SSL` + `PLAIN` with JAAS:
   - `username`: `<tls-project-id>`
   - `password`: `<ak>#<sk>`

```sql
CREATE TABLE tls_kafka_source (
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'kafka',
  'topic' = 'out-<tls-topic-id>',
  'properties.bootstrap.servers' = 'tls-<region>.ivolces.com:9093',
  'properties.security.protocol' = 'SASL_SSL',
  'properties.sasl.mechanism' = 'PLAIN',
  'properties.sasl.jaas.config' = 'org.apache.flink.kafka.shaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="<tls-project-id>" password="<ak>#<sk>";',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'latest-offset',
  'format' = 'json'
);
```

## Sink: write to TLS

Notes:
1. Producer `topic` must be `<tls-topic-id>` (NO `out-` prefix).
2. Producer port is typically `9094`.
3. MUST disable idempotence: `properties.enable.idempotence = false`.

```sql
CREATE TABLE tls_kafka_sink (
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'kafka',
  'topic' = '<tls-topic-id>',
  'properties.bootstrap.servers' = 'tls-<region>.ivolces.com:9094',
  'properties.enable.idempotence' = 'false',
  'properties.security.protocol' = 'SASL_SSL',
  'properties.sasl.mechanism' = 'PLAIN',
  'properties.sasl.jaas.config' = 'org.apache.flink.kafka.shaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="<tls-project-id>" password="<ak>#<sk>";',
  'format' = 'json'
);
```

## Example: TLS source -> print

```sql
CREATE TABLE print_sink (
  user_id BIGINT,
  item_id BIGINT,
  behavior STRING
) WITH (
  'connector' = 'print'
);

INSERT INTO print_sink
SELECT * FROM tls_kafka_source;
```
