# Transform notes

Official doc:
https://nightlies.apache.org/flink/flink-cdc-docs-release-3.4/docs/core-concept/transform/

## What transform does

`transform` helps you:

- select / drop / compute columns (projection)
- filter out unnecessary records (filter)
- optionally provide sink table creation hints (primary keys, partition keys, table options)
- optionally convert events after transform (for example, soft delete)

## Parameters

Each transform rule supports:

- `source-table` (required): source table id, supports regular expressions
- `projection` (optional): SQL-like select clause
- `filter` (optional): SQL-like where clause
- `primary-keys` (optional): sink table primary keys, comma-separated
- `partition-keys` (optional): sink table partition keys, comma-separated
- `table-options` (optional): options used when auto-creating sink tables
- `converter-after-transform` (optional): convert DataChangeEvent after transform, e.g. `SOFT_DELETE`
- `description` (optional): human-readable description

## Hidden columns (metadata fields)

Transform supports hidden columns for metadata when explicitly referenced.

Common ones:

- `__namespace_name__`
- `__schema_name__`
- `__table_name__`
- `__data_event_type__`

Some connectors may expose additional metadata via `metadata.list` in the source config.

## Examples

### 1) Projection and filter

```yaml
transform:
  - source-table: mydb\\.orders
    projection: "order_id, user_id, amount"
    filter: "amount > 0"
    description: keep only positive orders
```

### 2) Add identifier and op type

```yaml
transform:
  - source-table: .*
    projection: "*, __data_event_type__ AS op_type, __namespace_name__ || '.' || __schema_name__ || '.' || __table_name__ AS identifier"
    description: add identifier and op type
```

### 3) Soft delete (convert DELETE to INSERT)

Use `SOFT_DELETE` together with `__data_event_type__`:

```yaml
transform:
  - source-table: .*
    projection: "*, __data_event_type__ AS op_type"
    converter-after-transform: SOFT_DELETE
    description: convert delete to insert with op_type = '-D'
```

### 4) Table creation hints (when supported)

```yaml
transform:
  - source-table: mydb\\.orders
    primary-keys: "order_id"
    partition-keys: "dt"
    table-options: "bucket=4,changelog-producer=none"
    description: provide keys and table options for auto create
```

## Notes

- `source-table` is regex-based; escape dot if you mean a literal dot.
- `projection` and `filter` are parsed by Calcite-like SQL rules; keep them simple and explicit.
