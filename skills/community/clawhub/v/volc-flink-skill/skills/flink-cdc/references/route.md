# Route (table mapping) notes

Official doc:
https://nightlies.apache.org/flink/flink-cdc-docs-release-3.4/docs/core-concept/route/

## What route does

`route` defines a list of rules that:

- match upstream `source-table` (supports regular expressions)
- map them to downstream `sink-table`

The most typical scenario is merging sharding tables, or routing many upstream
tables to a single sink table.

## Parameters

Each route rule supports:

- `source-table` (required): Source table id, supports regex
- `sink-table` (required): Sink table id, supports symbol replacement
- `replace-symbol` (optional): Special symbol in `sink-table` used for pattern replacing
- `description` (optional): Human-readable description

## Examples

### 1) Route one table to one table

```yaml
route:
  - source-table: mydb.web_order
    sink-table: ods_db.ods_web_order
    description: sync table to one destination table
```

### 2) Route multiple source tables to one sink table (regex)

```yaml
route:
  - source-table: mydb\\..*
    sink-table: ods_db.ods_web_order
    description: merge sharding tables to one destination table
```

### 3) Pattern replacement in routing rules

`replace-symbol` enables copying the original table name into the sink table id.

```yaml
route:
  - source-table: source_db\\..*
    sink-table: sink_db.<>
    replace-symbol: <>
    description: route all tables in source_db to sink_db with same table name
```

## Notes

- `source-table` uses regex. If you mean a literal dot between `db.table`, escape it.
- A `route` module contains a list of `source-table`/`sink-table` rules.
