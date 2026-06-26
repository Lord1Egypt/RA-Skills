# Kafka source and sink notes

## Platform constraints

- Kafka pipeline connector currently supports Flink 1.16-volcano or above

## Kafka source

### Source example

```yaml
sources:
- source:
    type: kafka
    name: Kafka Source
    properties.bootstrap.servers: kafka-cnngnlfpk0h8kd7u.kafka.cn-beijing.ivolces.com:9092
    properties.group.id: kafka-cdc-source-test
    topic: cdc-kafka-source-test
    value.format: json
    scan.startup.mode: latest-offset
    table-id.fixed.name: my_tb
    metadata.list: topic,partition,offset,timestamp
    rate-limit-num: 3
```

### Required source options

- `type`: must be `kafka`
- `properties.bootstrap.servers`
- `properties.group.id`
- `value.format`
- One of:
  - `topic`
  - `topic-pattern`
- One of:
  - `table-id.fixed.name`
  - `table-id.dynamic.fields`

### Source common options

- `name`
- `topic`
- `topic-pattern`
- `key.format`: `json` or `none`, default `none`
- `key.fields-prefix`
- `value.format`: currently only `json`, default `json`
- `value.fields-prefix`
- `table-id.fixed.name`
- `table-id.dynamic.fields`
- `scan.startup.mode`: `earliest-offset`, `latest-offset`, `group-offsets`, `timestamp`, `specific-offsets`
- `scan.startup.timestamp-millis`
- `scan.startup.specific-offsets`
- `scan.topic-partition-discovery.interval`: default `5 min`
- `metadata.list`: supports `topic`, `partition`, `offset`, `timestamp`, `headers`, `leader-epoch`, `timestamp-type`
- `rate-limit-num`: default `none`

### Source option rules

- `topic` and `topic-pattern` are mutually exclusive
- `table-id.fixed.name` and `table-id.dynamic.fields` are mutually exclusive
- `table-id.fixed.name` is suitable for a single-table topic
- `table-id.dynamic.fields` is suitable for multi-table payloads, for example `db,table`

## Kafka sink

### Required sink options

- `properties.bootstrap.servers`

### Sink common options

- `topic`
- `value.format`
- `sink.add-tableId-to-header-enabled`
- `sink.custom-header`
- `properties.*`

## Topic behavior

- Sink side:
  - If `topic` is configured, all events go to that topic
  - If `topic` is not configured, the default topic is derived from upstream `namespace.schemaName.tableName`
  - If target topic does not exist, it is created by default

## Output formats

- Source side:
  - `value.format`: currently only `json`
- Sink side:
  - `debezium-json`: default output format
  - `canal-json`: alternate built-in format
