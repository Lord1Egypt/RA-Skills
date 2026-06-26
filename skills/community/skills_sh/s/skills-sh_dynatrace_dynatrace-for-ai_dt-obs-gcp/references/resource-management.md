# GCP Resource Management

Analyze GCP resource distribution across regions, projects, and organizational hierarchy.

## Table of Contents

- [Resource Management Entity Types](#resource-management-entity-types)
- [Region Inventory](#region-inventory)
- [Resource Distribution by Project](#resource-distribution-by-project)
- [Resource Distribution by Region](#resource-distribution-by-region)

## Resource Management Entity Types

| Entity type | Description |
|---|---|
| `GCP_REGION` | GCP regions where resources are deployed |

## Region Inventory

List all GCP regions with monitored resources:

```dql
smartscapeNodes "GCP_REGION"
| fields name, id
```

## Resource Distribution by Project

Count all GCP resources by project — use for understanding project-level resource sprawl:

```dql
smartscapeNodes "GCP_*"
| summarize count(), by: {gcp.project.id}
| sort `count()`, direction: "descending"
```

Break down resources by type within a specific project:

```dql-template
smartscapeNodes "GCP_*"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| summarize count(), by: {type}
| sort `count()`, direction: "descending"
```

Count distinct resource types per project:

```dql
smartscapeNodes "GCP_*"
| summarize
    type_count = countDistinct(type),
    total_resources = count(),
    by: {gcp.project.id}
| sort total_resources, direction: "descending"
```

## Resource Distribution by Region

Count all GCP resources by region:

```dql
smartscapeNodes "GCP_*"
| summarize count(), by: {gcp.region}
| sort `count()`, direction: "descending"
```

Find resource types spanning multiple regions:

```dql
smartscapeNodes "GCP_*"
| summarize
    region_count = countDistinct(gcp.region),
    total_resources = count(),
    by: {type}
| filter region_count > 1
| sort region_count, direction: "descending"
```

View resource distribution across projects and regions:

```dql
smartscapeNodes "GCP_*"
| summarize count(), by: {gcp.project.id, gcp.region}
| sort `count()`, direction: "descending"
```
