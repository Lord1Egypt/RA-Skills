
## Prerequisites

1. CLI installed, logged in, and cluster context set (see setup skill).
2. Target collection must exist and be loaded (see collection skill).

## Commands Reference

All vector commands accept an optional `--database <db-name>` flag to target a non-default database. If omitted, the database from the current context is used.

### Insert Vectors

```bash
zilliz vector insert --collection <collection-name> --data '[{"id": 1, "vector": [0.1, 0.2, ...], "text": "hello"}]'
# Optional: --database <database-name>
# Or use raw JSON: --body '{...}'
```

### Upsert Vectors

```bash
zilliz vector upsert --collection <collection-name> --data '[{"id": 1, "vector": [0.1, 0.2, ...], "text": "hello"}]'
# Optional: --partition <partition-name>, --database <database-name>
# Or use raw JSON: --body '{...}'
```

### Vector Search

```bash
zilliz vector search --collection <collection-name> --data '[[0.1, 0.2, 0.3, ...]]'
# Optional:
#   --anns-field <vector-field-to-search-on>
#   --limit <max-results-to-return>
#   --filter <scalar-filter-expression>
#   --output-fields '["field1", "field2"]'
#   --database <database-name>
```

### Hybrid Search

```bash
zilliz vector hybrid-search \
  --collection <collection-name> \
  --search '[{"data": [[0.1, ...]], "annsField": "dense_vector", "limit": 10}, {"data": [["search text"]], "annsField": "sparse_vector", "limit": 10}]' \
  --rerank '{"strategy": "rrf", "params": {"k": 60}}'
# Optional:
#   --limit <max-results-to-return>
#   --output-fields '["field1", "field2"]'
#   --database <database-name>
# Or use raw JSON: --body '{...}'
```

### Query by Filter

```bash
zilliz vector query --collection <collection-name> --filter <scalar-filter-expression>
# Optional:
#   --limit <max-results-to-return>
#   --output-fields '["field1", "field2"]'
#   --database <database-name>
```

### Get by ID

```bash
zilliz vector get --collection <collection-name> --id '[1, 2, 3]'
# Optional: --output-fields '["field1", "field2"]', --database <database-name>
```

### Delete a Vector

```bash
zilliz vector delete --collection <collection-name> --filter <filter>
# Optional: --partition <partition-name>, --database <database-name>
```

## Filter Expression Syntax

Common filter patterns:

| Expression | Example |
|---|---|
| Comparison | `age > 20` |
| Equality | `status == "active"` |
| IN list | `id in [1, 2, 3]` |
| AND/OR | `age > 20 and status == "active"` |
| String match | `text like "hello%"` |
| Array contains | `tags array_contains "ml"` |

## Guidance

- The `--data` parameter accepts a JSON array of vectors. Each vector is an array of floats.
- Before searching, inspect the collection schema with `zilliz collection describe` to understand field names and vector dimensions.
- The collection must be loaded before search/query operations.
- For search, the `--data` value must match the collection's vector dimension exactly.
- Use `--anns-field` to specify which vector field to search on when the collection has multiple vector fields.
- When the user provides a text query and wants semantic search, explain that they need to convert text to vectors first (using an embedding model) before passing to `--data`.
- For large insert operations, suggest writing data to a JSON file first, then using `zilliz vector insert --collection <name> --data "$(cat data.json)"`.
- Always show `--output-fields` when the user wants specific fields in results.
- Or use `--body` for complex hybrid search configurations.
