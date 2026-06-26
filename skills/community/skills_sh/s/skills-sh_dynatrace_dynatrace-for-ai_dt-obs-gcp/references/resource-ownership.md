# GCP Resource Ownership

Track resource ownership using GCP labels and organizational structure across all GCP entity types.

## Table of Contents

- [Label-Based Resource Ownership](#label-based-resource-ownership)
- [Organization-Level Overview](#organization-level-overview)
- [Label Discovery](#label-discovery)

## Label-Based Resource Ownership

GCP uses labels (key-value pairs) for resource organization and ownership tracking. Labels are exposed via the `tags:gcp_labels` attribute on smartscape nodes.

Find all GCP resources that have labels assigned:

```dql
smartscapeNodes "GCP_*"
| filter isNotNull(`tags:gcp_labels`)
| fields name, gcp.project.id, `tags:gcp_labels`
```

Filter resources by a specific label:

```dql-template
smartscapeNodes "GCP_*"
| filter isNotNull(`tags:gcp_labels`)
| filter contains(toString(`tags:gcp_labels`), "<LABEL_KEY>")
| fields name, gcp.project.id, `tags:gcp_labels`
```

Summarize resources by label for ownership reporting:

```dql-template
smartscapeNodes "GCP_*"
| filter isNotNull(`tags:gcp_labels`)
| filter contains(toString(`tags:gcp_labels`), "<LABEL_KEY>")
| summarize count(), by: {gcp.project.id, type}
```

### Common Ownership Labels

| Label key | Use case | Typical values |
|---|---|---|
| `team` | Team-level allocation | Team names |
| `owner` | Individual accountability | Email or username |
| `cost-center` | Financial chargeback | Cost center codes |
| `environment` | Environment segmentation | `production`, `staging`, `dev` |
| `application` | Application ownership | Application names |
| `project` | Project-based grouping | Project identifiers |

### Instance-Level Label Extraction

For Compute Engine instances, labels are also available inside `gcp.object`:

```dql
smartscapeNodes "GCP_COMPUTE_GOOGLEAPIS_COM_INSTANCE"
| parse gcp.object, "JSON:gcpjson"
| fieldsAdd labels = gcpjson[configuration][resource][labels]
| fields name, labels
```

## Organization-Level Overview

Summarize resources by GCP organization — use for multi-org visibility:

```dql
smartscapeNodes "GCP_*"
| summarize count(), by: {gcp.organization.id}
```

Break down organization resources by project:

```dql
smartscapeNodes "GCP_*"
| summarize count(), by: {gcp.organization.id, gcp.project.id}
| sort `count()`, direction: "descending"
```

## Label Discovery

Find resources with no labels — useful for label compliance auditing:

```dql
smartscapeNodes "GCP_*"
| filter isNull(`tags:gcp_labels`)
| summarize count(), by: {type, gcp.project.id}
```

Calculate label coverage across resource types:

```dql
smartscapeNodes "GCP_*"
| fieldsAdd has_labels = if(isNotNull(`tags:gcp_labels`), 1)
| summarize
    total = count(),
    with_labels = sum(has_labels),
    by: {type}
| fieldsAdd label_coverage_pct = (with_labels * 100.0) / total
| sort label_coverage_pct asc
```
