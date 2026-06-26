# Doris sink notes

## Platform constraints

- Doris pipeline sink currently supports Flink 1.16-volcano or above
- The connector can auto-create tables and sync schema changes

## Required / common options

- `fenodes`
- `benodes` (optional)
- `jdbc-url` (optional)
- `username`
- `password`
- `auto-redirect`

## Batch flush options

- `sink.enable.batch-mode`
- `sink.flush.queue-size`
- `sink.buffer-flush.max-rows`
- `sink.buffer-flush.max-bytes`
- `sink.buffer-flush.interval`
- `sink.properties.*`

## Table creation

- `table.create.properties.*`
- Example: `table.create.properties.replication_num: 1`

## Type mapping note

- Character columns are effectively expanded for UTF-8 byte length
- Oversized `CHAR/VARCHAR` can be promoted to `VARCHAR/STRING` on Doris side

