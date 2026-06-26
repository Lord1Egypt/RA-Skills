# GCP Monitoring & Logging

Monitor Cloud Monitoring dashboards and Cloud Logging saved queries across GCP projects.

## Table of Contents

- [Monitoring & Logging Entity Types](#monitoring--logging-entity-types)
- [Monitoring Dashboard Inventory](#monitoring-dashboard-inventory)
- [Logging Configuration](#logging-configuration)

## Monitoring & Logging Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, gcp.project.id`

| Entity type | Description |
|---|---|
| `GCP_MONITORING_GOOGLEAPIS_COM_DASHBOARD` | Cloud Monitoring dashboards |
| `GCP_LOGGING_GOOGLEAPIS_COM_SAVEDQUERY` | Cloud Logging saved queries |

## Monitoring Dashboard Inventory

List all Cloud Monitoring dashboards:

```dql
smartscapeNodes "GCP_MONITORING_GOOGLEAPIS_COM_DASHBOARD"
| fields name, gcp.project.id
```

Count dashboards by project:

```dql
smartscapeNodes "GCP_MONITORING_GOOGLEAPIS_COM_DASHBOARD"
| summarize count(), by: {gcp.project.id}
```

Find dashboards in a specific project:

```dql-template
smartscapeNodes "GCP_MONITORING_GOOGLEAPIS_COM_DASHBOARD"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| fields name
```

## Logging Configuration

List all Cloud Logging saved queries:

```dql
smartscapeNodes "GCP_LOGGING_GOOGLEAPIS_COM_SAVEDQUERY"
| fields name, gcp.project.id
```

Count saved queries by project:

```dql
smartscapeNodes "GCP_LOGGING_GOOGLEAPIS_COM_SAVEDQUERY"
| summarize count(), by: {gcp.project.id}
```

Count all monitoring and logging resources by type:

```dql
smartscapeNodes "GCP_MONITORING_GOOGLEAPIS_COM_DASHBOARD", "GCP_LOGGING_GOOGLEAPIS_COM_SAVEDQUERY"
| summarize count(), by: {type, gcp.project.id}
```
