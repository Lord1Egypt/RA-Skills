
## Prerequisites

1. CLI installed and logged in (see setup skill).
2. No cluster context required -- these are control-plane operations.

## Commands Reference

### Create a Cluster

```bash
# Serverless cluster
zilliz cluster create \
  --name <cluster-name> \
  --type serverless \
  --project-id <project-id> \
  --region <region-id>

# Free-tier cluster
zilliz cluster create \
  --name <cluster-name> \
  --type free \
  --project-id <project-id> \
  --region <region-id>

# Dedicated cluster
zilliz cluster create \
  --name <cluster-name> \
  --type dedicated \
  --project-id <project-id> \
  --region <region-id> \
  --cu-type <Performance-optimized|Capacity-optimized> \
  --cu-size <cu-size>
```

To find available project IDs, cloud providers, and regions:

```bash
zilliz project list
zilliz cluster providers
zilliz cluster regions --cloud-id <aws|gcp|azure>
```

### List Clusters

```bash
zilliz cluster list
# Pagination: --page-size <n> --page <n>
# Fetch all pages: --all
```

### Describe a Cluster

```bash
zilliz cluster describe --cluster-id <cluster-id>
```

### Modify a Cluster

```bash
zilliz cluster modify --cluster-id <cluster-id-to-modify>
# Optional: --cu-size <number-of-compute-units>, --replica <number-of-replicas>
# Or use raw JSON: --body '{"cuSize": 2, "replica": 2}'
```

### Suspend a Cluster

```bash
zilliz cluster suspend --cluster-id <cluster-id-to-suspend>
```

### Resume a Cluster

```bash
zilliz cluster resume --cluster-id <cluster-id-to-resume>
```

### Delete a Cluster

```bash
zilliz cluster delete --cluster-id <cluster-id-to-delete>
```

### List Cloud Providers

```bash
zilliz cluster providers
```

### List Regions

```bash
zilliz cluster regions
# Optional: --cloud-id <aws|gcp|azure>
```

## Guidance

- Before creating a cluster, help the user choose a region by running `zilliz cluster providers` and `zilliz cluster regions`.
- Cluster creation is **asynchronous**. After `cluster create`, the cluster status will be `CREATING`. Poll with `zilliz cluster describe --cluster-id <id>` until the status becomes `RUNNING` before proceeding with data-plane operations.
- Before deleting a cluster, always confirm with the user -- this is irreversible.
- After creating a cluster, suggest setting it as the active context with `zilliz context set --cluster-id <id>`.
- When a cluster is suspended, remind the user it must be resumed before data-plane operations.
- Different cluster types have different capabilities. See the "Cluster Type Differences" table in the setup skill for details.
