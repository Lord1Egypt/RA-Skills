# Kafka SQL templates

Use these templates as copy/paste starting points. Replace placeholders like `<brokers>`, `<topic>`, `<group-id>`, and adapt schema/format to your data.

Parameter notes: `references/kafka.md`

## Source: JSON

```sql
CREATE TABLE kafka_source_json (
  order_id BIGINT,
  order_product_id BIGINT,
  order_customer_id BIGINT,
  order_status STRING,
  order_update_time TIMESTAMP(3)
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
```

## Source: CSV

```sql
CREATE TABLE kafka_source_csv (
  order_id BIGINT,
  order_product_id BIGINT,
  order_customer_id BIGINT,
  order_status STRING,
  order_update_time TIMESTAMP(3)
) WITH (
  'connector' = 'kafka',
  'topic' = '<topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'csv',
  'csv.allow-comments' = 'false',
  'csv.ignore-parse-errors' = 'true',
  'csv.field-delimiter' = ',',
  'csv.line-delimiter' = U&'\000A'
);
```

## Source: Avro (skeleton)

```sql
CREATE TABLE kafka_source_avro (
  -- define your schema here
  id BIGINT,
  payload STRING
) WITH (
  'connector' = 'kafka',
  'topic' = '<topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'avro',
  'avro.schema' = '<inline-avro-schema-json>'
);
```

## Source: Debezium JSON (CDC in Kafka topic)

```sql
CREATE TABLE kafka_source_debezium (
  id INT,
  name STRING,
  age INT,
  email STRING,
  update_time TIMESTAMP(3)
) WITH (
  'connector' = 'kafka',
  'topic' = '<cdc-topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'debezium-json',
  'debezium-json.schema-include' = 'false'
);
```

## Sink: JSON

```sql
CREATE TABLE kafka_sink_json (
  order_id BIGINT,
  order_product_id BIGINT,
  order_customer_id BIGINT,
  order_status STRING,
  order_update_time TIMESTAMP(3)
) WITH (
  'connector' = 'kafka',
  'topic' = '<sink-topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'format' = 'json',
  'sink.partitioner' = 'fixed',
  -- Throughput knobs (tune based on load/latency)
  'properties.batch.size' = '524288',
  'properties.linger.ms' = '500',
  'properties.buffer.memory' = '134217728'
);
```

## Security: SASL_PLAINTEXT + PLAIN (example)

```sql
CREATE TABLE kafka_source_sasl_plain (
  order_id BIGINT,
  order_product_id BIGINT,
  order_customer_id BIGINT,
  order_status STRING,
  order_update_time TIMESTAMP(3)
) WITH (
  'connector' = 'kafka',
  'topic' = '<topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json',
  'properties.security.protocol' = 'SASL_PLAINTEXT',
  'properties.sasl.mechanism' = 'PLAIN',
  'properties.sasl.jaas.config' = 'org.apache.flink.kafka.shaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="<username>" password="<password>";'
);
```

## Security: SASL_SSL + SCRAM-SHA-256 (example)

```sql
CREATE TABLE kafka_source_sasl_ssl (
  order_id BIGINT,
  order_product_id BIGINT,
  order_customer_id BIGINT,
  order_status STRING,
  order_update_time TIMESTAMP(3)
) WITH (
  'connector' = 'kafka',
  'topic' = '<topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json',
  'properties.security.protocol' = 'SASL_SSL',
  'properties.ssl.truststore.location' = '<truststore.jks>',
  'properties.ssl.truststore.password' = '<truststore-password>',
  'properties.sasl.mechanism' = 'SCRAM-SHA-256',
  'properties.sasl.jaas.config' = 'org.apache.flink.kafka.shaded.org.apache.kafka.common.security.scram.ScramLoginModule required username="<username>" password="<password>";',
  -- Set to empty string to skip hostname verification if needed
  'properties.ssl.endpoint.identification.algorithm' = ''
);
```

## End-to-end: Source -> Print

```sql
CREATE TABLE kafka_source (
  order_id BIGINT,
  order_product_id BIGINT,
  order_customer_id BIGINT,
  order_status STRING,
  order_update_time TIMESTAMP(3)
) WITH (
  'connector' = 'kafka',
  'topic' = '<topic>',
  'properties.bootstrap.servers' = '<brokers>',
  'properties.group.id' = '<group-id>',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'json'
);

CREATE TABLE print_sink (
  order_id BIGINT,
  order_product_id BIGINT,
  order_customer_id BIGINT,
  order_status STRING,
  order_update_time TIMESTAMP(3)
) WITH (
  'connector' = 'print'
);

INSERT INTO print_sink
SELECT * FROM kafka_source;
```
