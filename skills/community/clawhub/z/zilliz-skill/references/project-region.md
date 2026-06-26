
## Prerequisites

1. CLI installed and logged in (see setup skill).

## Commands Reference

### Projects

#### Create a Project

```bash
zilliz project create --name <project-name> --plan <Free|Serverless|Standard|Enterprise>
```

#### List Projects

```bash
zilliz project list
```

#### Describe a Project

```bash
zilliz project describe --project-id <project-id>
```

#### Upgrade a Project

```bash
zilliz project upgrade --project-id <project-id>
# Optional: --plan <Serverless|Standard|Enterprise>
```

### Volumes

#### Create a Volume

```bash
zilliz volume create \
  --project-id <project-id> \
  --region <cloud-region> \
  --name <volume-name>
```

#### List Volumes

```bash
zilliz volume list --project-id <project-id>
# Pagination: --page-size <n> --page <n>
# Fetch all pages: --all
```

#### Delete a Volume

```bash
zilliz volume delete --name <volume-name-to-delete>
```

## Guidance

- When the user wants to create a cluster, they need a project ID and region ID first. Guide them through `zilliz project list` and `zilliz cluster regions` (see cluster skill).
- Project `upgrade` does not include `Free` as a valid target plan -- only Serverless, Standard, and Enterprise.
- Before deleting a volume, confirm with the user.
