
## Prerequisites

1. CLI installed and logged in (see setup skill).
2. Target collection must exist on the target cluster.

## Commands Reference

### Start an Import Job

```bash
zilliz import start --cluster-id <target-cluster-id> --collection <target-collection-name>
# Or use raw JSON: --body '{"files": [["s3://bucket/path/data.parquet"]]}'
```

### List Imports

```bash
zilliz import list --cluster-id <cluster-id>
# Optional: --database <database-name>
```

### Check Import Status

```bash
zilliz import status --job-id <import-job-id> --cluster-id <cluster-id>
```

## Integration Setup

Import requires a cloud storage integration to access data files. The `integration-id` is configured in the Zilliz Cloud console under **Project Settings > Integrations**. Ensure the integration has read access to the source bucket and path.

Supported file formats: Parquet, JSON, CSV.

## Guidance

- Import jobs run asynchronously. After starting a job, use `import status` to track progress.
- The data files must be accessible from Zilliz Cloud (e.g., S3, GCS with proper integration configured).
- The collection schema must match the data file structure.
