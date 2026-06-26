
## Prerequisites

1. CLI installed and logged in (see setup skill).
2. Cluster context set for collection-level monitoring (see setup skill).

## Commands Reference

All monitoring commands that target collections accept an optional `--database <db-name>` flag. If omitted, the database from the current context is used.

### Cluster Status

```bash
# Current context
zilliz context current

# Cluster details (status, plan, region, endpoints)
zilliz cluster describe --cluster-id <cluster-id>
```

### Collection Overview

List all collections with their stats:

```bash
# List collections
zilliz collection list
zilliz collection list --database <db-name>

# For each collection, get stats and load state:
zilliz collection get-stats --name <collection-name>
zilliz collection get-load-state --name <collection-name>
```

If the cluster has multiple databases, iterate through each database by running `zilliz database list` first, then `zilliz collection list --database <db-name>` for each.

### Database Overview

```bash
zilliz database list
```

### All Clusters

```bash
zilliz cluster list --all
```

## Presenting Results

When the user asks for a status overview, collect and present information as a summary table:

**Cluster Info:**
- Cluster ID, name, status (RUNNING/SUSPENDED/etc.)
- Plan type, region, create time

**Collections Summary:**
Present as a table with columns:
| Collection | Rows | Load State |
|---|---|---|

Gather this by running `collection list`, then `get-stats` and `get-load-state` for each collection.

## Guidance

- When presenting status, use `--output json` to get machine-readable data, then format it into a readable summary for the user.
- If the cluster is suspended, note this prominently and inform the user that data-plane operations are unavailable.
- For multiple clusters, show a summary table of all clusters first, then drill into the selected one.
