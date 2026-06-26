
## Prerequisites

1. CLI installed, logged in, and cluster context set (see setup skill).

## Commands Reference

All collection commands accept an optional `--database <db-name>` flag to target a non-default database. If omitted, the database from the current context is used.

### Create a Collection

```bash
zilliz collection create --name <collection-name> --dimension <vector-dimension>
# Optional:
#   --metric-type <COSINE|L2|IP>
#   --id-type <Int64|VarChar>
#   --auto-id <true|false>
#   --primary-field <primary-key-field-name>
#   --vector-field <vector-field-name>
#   --database <database-name>
# Or use raw JSON: --body '{"schema": {"fields": [{"fieldName": "id", "dataType": "Int64", "isPrimary": true}, {"fieldName": "vector", "dataType": "FloatVector", "elementTypeParams": {"dim": "768"}}]}}'
```

### List Collections

```bash
zilliz collection list
# Optional: --database <database-name>
```

### Describe a Collection

```bash
zilliz collection describe --name <collection-name>
# Optional: --database <database-name>
```

### Drop a Collection

```bash
zilliz collection drop --name <collection-name-to-drop>
# Optional: --database <database-name>
```

### Rename a Collection

```bash
zilliz collection rename --name <current-collection-name> --new-name <new-collection-name>
# Optional: --database <current-database-name>, --new-database <target-database-name>
```

### Load a Collection

```bash
zilliz collection load --name <collection-name>
# Optional: --database <database-name>
```

### Release a Collection

```bash
zilliz collection release --name <collection-name>
# Optional: --database <database-name>
```

### Get Load State

```bash
zilliz collection get-load-state --name <collection-name>
# Optional: --database <database-name>
```

### Get Statistics

```bash
zilliz collection get-stats --name <collection-name>
# Optional: --database <database-name>
```

### Check if a Collection Exists

```bash
zilliz collection has --name <collection-name>
# Optional: --database <database-name>
```

### Flush a Collection

```bash
zilliz collection flush --name <collection-name>
# Optional: --database <database-name>
```

### Compact a Collection

```bash
zilliz collection compact --name <collection-name>
# Optional: --database <database-name>
```

### Collection Aliases

#### Create an Alias

```bash
zilliz alias create --collection <target-collection-name> --alias <alias-name>
# Optional: --database <database-name>
```

#### List Aliases

```bash
zilliz alias list --database <database-name>
# Optional: --collection <filter-by-collection-name>
```

#### Describe an Alias

```bash
zilliz alias describe --alias <alias-name>
# Optional: --database <database-name>
```

#### Alter an Alias

```bash
zilliz alias alter --collection <new-target-collection> --alias <alias-name-to-reassign>
# Optional: --database <database-name>
```

#### Drop an Alias

```bash
zilliz alias drop --alias <alias-name-to-drop>
# Optional: --database <database-name>
```

## Guidance

- When the user wants to create a collection, ask about their use case to recommend appropriate dimension, metric type, and schema.
- Before dropping a collection, always confirm with the user -- this deletes all data.
- A collection must be loaded before it can be searched or queried.
- After creating a collection, suggest loading it if the user plans to query immediately.
- Use `describe` to inspect schema before performing vector operations.
