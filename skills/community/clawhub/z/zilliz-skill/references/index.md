
## Prerequisites

1. CLI installed, logged in, and cluster context set (see setup skill).
2. Target collection must exist (see collection skill).

## Commands Reference

All index commands accept an optional `--database <db-name>` flag. If omitted, the database from the current context is used.

### Create an Index

```bash
zilliz index create --collection <collection-name>
# Optional: --database <database-name>
# Or use raw JSON: --body '{"indexParams": [{"fieldName": "vector", "indexType": "AUTOINDEX", "metricType": "COSINE"}]}'
```

### List Indexes

```bash
zilliz index list --collection <collection-name>
# Optional: --database <database-name>
```

### Describe an Index

```bash
zilliz index describe --collection <collection-name> --index-name <index-name>
# Optional: --database <database-name>
```

### Drop an Index

```bash
zilliz index drop --collection <collection-name> --index-name <index-name-to-drop>
# Optional: --database <database-name>
```

## Index Types

Common index types:
- `AUTOINDEX` -- recommended, automatically selects the best index
- `IVF_FLAT`, `IVF_SQ8`, `HNSW` -- manual selection for advanced users

Common metric types:
- `COSINE` -- cosine similarity (default)
- `L2` -- Euclidean distance
- `IP` -- inner product

## Guidance

- On Zilliz Cloud, `AUTOINDEX` is recommended for most use cases.
- An index is required before loading a collection for search.
- Before creating an index, check the collection schema to identify vector fields.
- After creating an index, remind the user to load the collection.
