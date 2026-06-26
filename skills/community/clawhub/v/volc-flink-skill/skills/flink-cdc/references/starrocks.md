# StarRocks sink notes

## Platform constraints

- StarRocks pipeline sink currently supports Flink 1.16-volcano or above
- Only primary-key tables are supported
- Exactly-once is not supported; idempotence relies on at-least-once + primary-key table behavior

## Required options

- `jdbc-url`
- `load-url`
- `username`
- `password`

## Common sink options

- `sink.label-prefix`
- `sink.connect.timeout-ms`
- `sink.wait-for-continue.timeout-ms`
- `sink.buffer-flush.max-bytes`
- `sink.buffer-flush.interval-ms`
- `sink.scan-frequency.ms`
- `sink.io.thread-count`
- `sink.at-least-once.use-transaction-stream-load`
- `sink.properties.*`

## Auto create / schema change notes

- `table.create.num-buckets`: required for older StarRocks versions; optional for 2.5+
- `table.create.properties.*`: pass table creation properties
- `table.schema-change.timeout`
- For StarRocks 3.2+, `table.create.properties.fast_schema_evolution = true` can accelerate schema evolution

