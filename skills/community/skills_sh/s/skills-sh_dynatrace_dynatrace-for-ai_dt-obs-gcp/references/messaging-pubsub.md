# GCP Messaging (Pub/Sub)

Monitor Pub/Sub topics and messaging infrastructure across GCP projects.

## Table of Contents

- [Messaging Entity Types](#messaging-entity-types)
- [Topic Discovery](#topic-discovery)
- [Topic Distribution by Project](#topic-distribution-by-project)

## Messaging Entity Types

All these types support the standard discovery pattern: `smartscapeNodes "<TYPE>" | fields name, gcp.project.id, gcp.region`

| Entity type | Description |
|---|---|
| `GCP_PUBSUB_GOOGLEAPIS_COM_TOPIC` | Pub/Sub topics |

## Topic Discovery

List all Pub/Sub topics:

```dql
smartscapeNodes "GCP_PUBSUB_GOOGLEAPIS_COM_TOPIC"
| fields name, gcp.project.id, gcp.region
```

Find topics in a specific project:

```dql-template
smartscapeNodes "GCP_PUBSUB_GOOGLEAPIS_COM_TOPIC"
| filter gcp.project.id == "<GCP_PROJECT_ID>"
| fields name, gcp.region
```

Find topics by name pattern:

```dql-template
smartscapeNodes "GCP_PUBSUB_GOOGLEAPIS_COM_TOPIC"
| filter contains(name, "<TOPIC_NAME_PATTERN>")
| fields name, gcp.project.id, gcp.region
```

## Topic Distribution by Project

Count Pub/Sub topics per project:

```dql
smartscapeNodes "GCP_PUBSUB_GOOGLEAPIS_COM_TOPIC"
| summarize count(), by: {gcp.project.id}
```

Count topics by project and region:

```dql
smartscapeNodes "GCP_PUBSUB_GOOGLEAPIS_COM_TOPIC"
| summarize count(), by: {gcp.project.id, gcp.region}
```
